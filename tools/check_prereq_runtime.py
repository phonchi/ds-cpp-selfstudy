#!/usr/bin/env python3
"""Compile and run the legacy C++ examples embedded in prerequisite pages.

This complements check_prereq.py: it exercises the original ``.pseudo-code``
blocks, including pages that predate the ``data-cpp`` metadata convention.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import hashlib
import signal
from pathlib import Path
import re
import subprocess
import tempfile

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "data/prereq_fidelity_contract.json"
UNSAFE = {"p1#6", "p2#3", "p3#13", "p3#21"}
EXPECTED_NONZERO = {"p1#22", "p5#2", "p7#7"}
EXPECTED_LINK_FAILURE = {"p1#21"}

# These examples intentionally print addresses, timings, implementation-defined
# capacities/diagnostics, or pseudo-random values.  Their stable facts are
# checked below instead of comparing a machine-specific transcript.
DYNAMIC_KEYS = {
    "p5#4", "p5#16", "p9#12", "p1#5", "p1#14", "p1#16", "p1#22", "p2#22", "p3#4",
    "p4#1", "p4#3", "p4#5", "p4#6", "p4#7", "p5#0", "p5#2", "p5#6", "p5#7", "p5#8",
    "p5#10", "p5#14", "p6#0", "p6#7", "p7#5", "p7#7",
}


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def page_number(path):
    return re.match(r"p(\d+)_", path.name).group(1)


def own_expected(block):
    """Return the adjacent expected output without crossing into another example."""
    section = block.find_parent("section")
    for node in block.find_all_next():
        if node is block:
            continue
        if node.name in ("div", "pre") and "pseudo-code" in node.get("class", []):
            return ""
        if node.name and "expected-out" in node.get("class", []):
            if node.find_parent("section") != section:
                return ""
            pre = node.select_one("pre")
            return pre.get_text() if pre else ""
        if node.name == "section" and node is not section:
            return ""
    return ""


def dynamic_output_ok(key, stdout, stderr):
    text = stdout + "\n" + stderr
    if key == "p5#4":
        rows = stdout.splitlines()
        expected_rows = [
            "起始 size=3 [ 31 17 93 ]",
            "push_back(26) size=4 [ 31 17 93 26 ]",
            "pop_back() size=3 [ 31 17 93 ]",
            "insert(begin) size=4 [ 54 31 17 93 ]",
            "erase(begin+1) size=3 [ 54 17 93 ]",
        ]
        capacity = re.search(r"clear\(\) 之後\s+size=0\s+capacity=(\d+)", stdout)
        return ([normalize(row) for row in rows[:5]] == expected_rows
                and capacity is not None and int(capacity.group(1)) >= 4)
    if key == "p5#16":
        return 'stoi("1453") + 1 = 1454' in stdout and 'string(1, c) + "X" = 1X' in stdout
    if key == "p9#12":
        return "42 / hello" in stdout and "sizeof(Box<int>)" in stdout and "sizeof(Box<string>)" in stdout
    if key == "p1#14":
        faces = [int(x) for x in re.findall(r"點數\s+([1-6])", stdout)]
        return len(faces) == 3
    if key == "p1#16":
        return all(x in stdout for x in ("int 範圍", "unsigned 0 - 1", "先轉 long long"))
    if key == "p2#22":
        return stdout.count("total = 100010000") == 3 and stdout.count("seconds =") == 3
    if key == "p3#4":
        addresses = re.findall(r"0x[0-9a-fA-F]+", stdout)
        return "改了 r 之後 x = 99" in stdout and len(addresses) >= 2 and addresses[0] == addresses[1]
    if key.startswith("p4#"):
        return "runtime error:" not in stderr
    if key == "p5#6":
        return "兩份長度 5000 5000" in stdout
    if key == "p5#10":
        return "before: first = 31" in stdout and "new pointer reads 31" in stdout
    if key == "p5#14":
        return "內容相同 1" in stdout
    if key == "p6#0":
        return ("N=100000" in stdout and "Q=1000" in stdout
                and stdout.count("命中 0") >= 2 and "耗時" in stdout)
    if key == "p6#7":
        return ("map 走訪" in stdout
                and "apple durian fig guava kiwi lychee mango pear" in stdout
                and "bucket_count" in stdout)
    if key == "p7#5":
        return "caught out_of_range" in stdout and "continue" in stdout
    if key in EXPECTED_NONZERO:
        return True
    return "runtime error:" not in text


def collect(selected):
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    jobs, skipped = [], []
    for path in sorted(ROOT.glob("p[1-9]_*.html")):
        chapter = f"p{page_number(path)}"
        if selected and chapter not in selected:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        blocks = soup.select(".pseudo-code")
        support = {
            name: blocks[index].get_text()
            for name, index in contract.get("legacy_cpp_support", {}).get(path.name, {}).items()
        }
        for index, block in enumerate(blocks):
            index = int(block.get("data-audit-index", index))
            key = f"{chapter}#{index}"
            code = block.get_text()
            mode = contract.get("legacy_cpp_exceptions", {}).get(f"{path.name}#{index}", "")
            if not re.search(r"\bint\s+main\s*\(", code):
                continue
            if mode in ("diagnostic-text", "compile-error"):
                skipped.append({"key": key, "reason": mode})
                continue
            if key in UNSAFE:
                skipped.append({"key": key, "reason": "unsafe"})
                continue
            jobs.append({"key": key, "page": path.name, "code": code,
                         "support": support, "expected": own_expected(block)})
    return jobs, skipped


def run_job(job):
    key = job["key"]
    identity = {"key": key, "page": job["page"]}
    with tempfile.TemporaryDirectory(prefix=f"prereq-runtime-{key.replace('#', '-')}-") as raw:
        folder = Path(raw)
        source = folder / "example.cpp"
        source.write_text(job["code"], encoding="utf-8")
        for name, value in job["support"].items():
            (folder / name).write_text(value, encoding="utf-8")
        command = ["g++", "-std=c++17", "-O0", "-Wall", "-Wextra", "-pedantic",
                   "-fsanitize=undefined", "-fno-sanitize-recover=all",
                   str(source), "-o", str(folder / "example")]
        compiled = subprocess.run(command, cwd=folder, capture_output=True, text=True)
        if key in EXPECTED_LINK_FAILURE:
            ok = compiled.returncode != 0 and "undefined reference" in compiled.stderr and "addUp" in compiled.stderr
            return {**identity, "ok": ok, "stage": "expected-link-failure",
                    "exit": compiled.returncode, "stderr": compiled.stderr[:2000]}
        if compiled.returncode:
            return {**identity, "ok": False, "stage": "compile-link", "exit": compiled.returncode,
                    "stderr": compiled.stderr[:2000]}
        try:
            result = subprocess.run([str(folder / "example")], cwd=folder,
                                    input="12\nHello there\n", capture_output=True,
                                    text=True, timeout=4)
        except subprocess.TimeoutExpired:
            return {**identity, "ok": False, "stage": "timeout"}
        exit_ok = result.returncode == -signal.SIGABRT and "runtime error:" not in result.stderr if key in EXPECTED_NONZERO else result.returncode == 0
        if key in DYNAMIC_KEYS:
            output_ok = dynamic_output_ok(key, result.stdout, result.stderr)
            comparison = "dynamic"
        elif job["expected"]:
            output_ok = normalize(result.stdout) == normalize(job["expected"])
            comparison = "normalized"
        else:
            output_ok = True
            comparison = "none"
        return {**identity, "ok": exit_ok and output_ok, "stage": "run",
                "exit": result.returncode, "stdout": result.stdout,
                "stderr": result.stderr[:2000], "comparison": comparison,
                "expected": job["expected"], "exit_ok": exit_ok, "output_ok": output_ok}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", nargs="+", help="p1 ... p9 (comma-separated values accepted)")
    parser.add_argument("--report", type=Path, help="write detailed JSON report")
    args = parser.parse_args()
    selected = None
    if args.pages:
        selected = {item for group in args.pages for item in group.split(",")}
        invalid = selected - {f"p{i}" for i in range(1, 10)}
        if invalid:
            parser.error(f"unknown pages: {', '.join(sorted(invalid))}")
    jobs, skipped = collect(selected)
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(run_job, jobs))
    failures = [item for item in results if not item["ok"]]
    report = {"root": str(ROOT), "page_sha256": {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob("p[1-9]_*.html"))}, "summary": {"cases": len(results), "executed": sum(r["stage"] == "run" for r in results), "expected_link_failures": sum(r["stage"] == "expected-link-failure" and r["ok"] for r in results),
              "passed": len(results) - len(failures), "failed": len(failures),
              "skipped": len(skipped)}, "failures": failures,
              "skipped": skipped, "results": results}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Runtime:", ", ".join(f"{k}={v}" for k, v in report["summary"].items()))
    for failure in failures:
        print(f"FAIL {failure['key']} [{failure['stage']}]")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
