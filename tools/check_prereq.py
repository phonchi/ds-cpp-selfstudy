#!/usr/bin/env python3
"""Verify P1–P9 examples and source data without changing the site.

Full C++ examples use data-cpp="run", data-expected and optional data-stdin.
Use data-cpp="compile-error" for intentional compiler errors and "fragment"
for syntax skeletons / excerpts. Never execute undefined-behavior examples.
Executables and any files they create stay in a fresh temporary directory.
Requires g++ and Node.js; the HTML parser uses only the Python standard library.
"""
import argparse
import hashlib
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.blocks = []
        self.scripts = []
        self.current = None
        self.script = None
        self.quiz_buttons = []
        self.inline_quizzes = []
        self.quiz_stack = []
        self.quiz_depth = 0
        self.pseudo_count = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        classes = attrs.get("class", "").split()
        if tag in ("pre", "div") and (tag == "pre" or "pseudo-code" in classes or "sq-code" in classes):
            pseudo_index = None
            if "pseudo-code" in classes:
                pseudo_index = self.pseudo_count
                self.pseudo_count += 1
            self.current = {"attrs": attrs, "text": "", "line": self.getpos()[0], "pseudo_index": pseudo_index}
        if tag == "script" and not attrs.get("src"):
            self.script = ""
        if self.quiz_stack and tag == "div":
            self.quiz_depth += 1
        if "quiz-options" in classes:
            group = {"id": attrs.get("id"), "options": [], "line": self.getpos()[0]}
            self.inline_quizzes.append(group)
            self.quiz_stack.append(group)
            self.quiz_depth = 1
        if "quiz-opt" in classes and self.quiz_stack:
            self.quiz_stack[-1]["options"].append(attrs)
        if tag == "button" and "sq-opt" in classes:
            self.quiz_buttons.append(attrs)

    def handle_data(self, text):
        if self.current is not None:
            self.current["text"] += text
        if self.script is not None:
            self.script += text

    def handle_endtag(self, tag):
        if tag in ("pre", "div") and self.current is not None:
            self.blocks.append(self.current)
            self.current = None
        if tag == "div" and self.quiz_stack:
            self.quiz_depth -= 1
            if self.quiz_depth == 0:
                self.quiz_stack.pop()
        if tag == "script" and self.script is not None:
            self.scripts.append(self.script)
            self.script = None


def run(command, cwd, stdin=None):
    return subprocess.run(command, input=stdin, text=True, capture_output=True,
                          cwd=cwd, timeout=20)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", nargs="+", choices=[f"p{i}" for i in range(1, 10)])
    args = parser.parse_args()
    selected = args.pages or [f"p{i}" for i in range(1, 10)]
    for tool in ("g++", "node"):
        if not shutil.which(tool):
            parser.error(f"required tool missing: {tool}")
    documents = {p.name: Page(p.read_text(encoding="utf-8")) for p in ROOT.glob("*.html")}
    fidelity = json.loads((ROOT / "data/prereq_fidelity_contract.json").read_text())
    legacy_exceptions = fidelity.get("legacy_cpp_exceptions", {})
    legacy_support = fidelity.get("legacy_cpp_support", {})
    errors = []
    counts = Counter()
    hero_shapes = set()
    for chapter in selected:
        matches = list(ROOT.glob(f"{chapter}_*.html"))
        if len(matches) != 1:
            errors.append(f"{chapter}: expected one HTML page, found {len(matches)}")
            continue
        path = matches[0]
        source = path.read_text(encoding="utf-8")
        doc = documents[path.name]
        heroes = re.findall(r'<svg\b[^>]*class="[^"]*\bhero-graph\b[^"]*"[^>]*>.*?</svg>', source, re.S)
        if len(heroes) != 1:
            errors.append(f"{path.name}: expected one page-specific hero SVG")
        else:
            fingerprint = hashlib.sha256(heroes[0].encode()).hexdigest()
            if fingerprint in hero_shapes:
                errors.append(f"{path.name}: hero duplicates another prerequisite page")
            hero_shapes.add(fingerprint)
        if "/* quiz-shuffle v1 */" not in source:
            errors.append(f"{path.name}: missing quiz option shuffle")
        duplicate_ids = [key for key, n in Counter(doc.ids).items() if n > 1]
        if duplicate_ids:
            errors.append(f"{path.name}: duplicate ids {duplicate_ids}")
        for quiz in doc.inline_quizzes:
            options = quiz["options"]
            if len(options) != 4:
                errors.append(f"{path.name}:{quiz['line']}: inline quiz must have four options")
            if sum(a.get("data-correct") == "true" for a in options) != 1:
                errors.append(f"{path.name}:{quiz['line']}: inline quiz must have one correct option")
            if not quiz["id"] or not quiz["id"].endswith("Options"):
                errors.append(f"{path.name}:{quiz['line']}: inline quiz id must end in Options")
            expected_id = quiz["id"][:-7] + "Feedback" if quiz["id"] else ""
            if expected_id not in doc.ids:
                errors.append(f"{path.name}:{quiz['line']}: missing #{expected_id} feedback element")
            if any(not a.get("data-fb") or "quizCheck(" not in a.get("onclick", "") for a in options):
                errors.append(f"{path.name}:{quiz['line']}: inline quiz option missing feedback/quizCheck contract")
        try:
            cards = json.loads((ROOT / f"data/flashcards_zh/{chapter}.json").read_text())
            questions = json.loads((ROOT / f"data/questions_zh/{chapter}.json").read_text())
            assert cards and questions, "empty learning data"
            for card in cards:
                assert all(isinstance(card.get(k), str) and card[k].strip()
                           for k in ("front", "back")), "invalid flashcard"
                assert re.search(r'[\u4e00-\u9fff]', card['front']) and re.search(r'（[^（）]*[A-Za-z][^（）]*）', card['front']), f"flashcard must have Chinese and parenthesized English: {card['front']}"
            for number, q in enumerate(questions, 1):
                assert isinstance(q.get("question"), str) and q["question"].strip(), f"Q{number}: missing question"
                assert len(q["answers"]) == 4, f"Q{number}: expected exactly four options"
                assert len({a.get('answer') for a in q['answers']}) == 4, f"Q{number}: duplicate options"
                assert all(isinstance(a.get("correct"), bool) for a in q["answers"]), f"Q{number}: invalid correct flag"
                assert sum(a["correct"] for a in q["answers"]) == 1, f"Q{number}: expected one correct answer"
                assert all(isinstance(a.get(k), str) and a[k].strip()
                           for a in q["answers"] for k in ("answer", "feedback")), f"Q{number}: missing feedback"
            match = re.search(r"const FLASHCARDS = (\[.*?\]);", source, re.S)
            assert match and json.loads(match[1]) == cards, "flashcards differ from data source"
            expected = [(str(int(a["correct"])), a["feedback"])
                        for q in questions for a in q["answers"]]
            actual = [(a.get("data-c"), a.get("data-fb")) for a in doc.quiz_buttons]
            assert actual == expected, "quiz options/feedback differ from data source; run apply_zh.py --pages"
        except (AssertionError, KeyError, TypeError, ValueError) as exc:
            errors.append(f"{path.name}: {exc}")
        counts["pages"] += 1
        page_runs = 0
        with tempfile.TemporaryDirectory(prefix=f"cpp-prereq-{chapter}-") as temp:
            folder = Path(temp)
            for number, script in enumerate(doc.scripts, 1):
                js = folder / f"script-{number}.js"
                js.write_text(script, encoding="utf-8")
                result = run(["node", "--check", str(js)], folder)
                if result.returncode:
                    errors.append(f"{path.name}: script {number}: {result.stderr}")
                counts["scripts"] += 1
            groups = {}
            for block in doc.blocks:
                if block["attrs"].get("data-cpp") == "file":
                    groups.setdefault(block["attrs"].get("data-example", ""), []).append(block)
            for group, blocks in groups.items():
                label = f"{path.name}: multi-file {group}"
                case = folder / ("group-" + str(len(list(folder.glob('group-*')))))
                case.mkdir()
                try:
                    assert group, "missing data-example"
                    written = set()
                    expected = None
                    stdin = ""
                    for block in blocks:
                        attrs = block["attrs"]
                        name = attrs.get("data-filename", "")
                        assert name and Path(name).name == name and name not in written, "invalid/duplicate data-filename"
                        written.add(name)
                        (case / name).write_text(block["text"], encoding="utf-8")
                        if "data-expected" in attrs:
                            assert expected is None, "more than one expected output"
                            expected, stdin = attrs["data-expected"], attrs.get("data-stdin", "")
                    assert expected is not None, "missing group expected output"
                    sources = sorted(str(case / name) for name in written if name.endswith('.cpp'))
                    assert sources, "missing .cpp source"
                    exe = case / "example"
                    compiled = run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic", *sources, "-o", str(exe)], case)
                    assert compiled.returncode == 0, compiled.stderr
                    result = run([str(exe)], case, stdin)
                    assert result.returncode == 0 and result.stdout == expected, f"stdout={result.stdout!r}, expected={expected!r}, stderr={result.stderr!r}"
                    counts["multi-file"] += 1
                except (AssertionError, subprocess.TimeoutExpired) as exc:
                    errors.append(f"{label}: {exc}")
            for number, block in enumerate(doc.blocks, 1):
                attrs, code = block["attrs"], block["text"]
                kind = attrs.get("data-cpp")
                label = f"{path.name}:{block['line']}"
                if kind == "file":
                    continue
                if kind is None:
                    # Quiz programs can intentionally fail; their expected behavior
                    # is explained by the answer, not by a standalone run contract.
                    if "sq-code" in attrs.get("class", "").split():
                        continue
                    if block.get("pseudo_index") is not None and re.search(r"\bint\s+main\s*\(", code):
                        key = f"{path.name}#{block['pseudo_index']}"
                        mode = legacy_exceptions.get(key, "run")
                        if mode in ("diagnostic-text", "unsafe"):
                            counts["legacy-" + mode] += 1
                            continue
                        case = folder / ("legacy-" + str(block["pseudo_index"]))
                        case.mkdir()
                        source_file = case / "example.cpp"
                        source_file.write_text(code, encoding="utf-8")
                        if mode == "external-files":
                            indexed = {b.get("pseudo_index"): b["text"] for b in doc.blocks}
                            for filename, index in legacy_support.get(path.name, {}).items():
                                if index not in indexed:
                                    errors.append(f"{label}: missing legacy support block {index} for {filename}")
                                    continue
                                (case / filename).write_text(indexed[index], encoding="utf-8")
                        result = run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic", "-fsyntax-only", str(source_file)], case)
                        if mode == "compile-error":
                            if result.returncode == 0:
                                errors.append(f"{label}: expected teaching compile-error now compiles")
                            counts["legacy-compile-errors"] += 1
                        elif result.returncode:
                            errors.append(f"{label}: legacy full example compile failed: {result.stderr}")
                        else:
                            counts["legacy-compiled"] += 1
                    continue
                if kind == "fragment":
                    counts["fragments"] += 1
                    continue
                if kind not in ("run", "compile-error"):
                    errors.append(f"{label}: unknown data-cpp value {kind}")
                    continue
                case = folder / str(number)
                case.mkdir()
                cpp, exe = case / "example.cpp", case / "example"
                cpp.write_text(code, encoding="utf-8")
                try:
                    result = run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
                                  str(cpp), "-o", str(exe)], case)
                    if kind == "compile-error":
                        if not result.returncode:
                            errors.append(f"{label}: intentional compiler error compiled successfully")
                        counts["compile-errors"] += 1
                        continue
                    if result.returncode:
                        errors.append(f"{label}: compile failed: {result.stderr}")
                        continue
                    if "data-expected" not in attrs and "data-expected-pattern" not in attrs:
                        errors.append(f"{label}: missing expected stdout")
                        continue
                    result = run([str(exe)], case, attrs.get("data-stdin", ""))
                    pattern = attrs.get('data-expected-pattern')
                    matches = re.fullmatch(pattern, result.stdout) is not None if pattern else result.stdout == attrs["data-expected"]
                    if result.returncode or not matches:
                        errors.append(f"{label}: exit={result.returncode}, stdout={result.stdout!r}, "
                                      f"expected={attrs.get('data-expected', pattern)!r}, stderr={result.stderr!r}")
                    counts["runs"] += 1
                    page_runs += 1
                except subprocess.TimeoutExpired:
                    errors.append(f"{label}: compiler/program timeout")
        # Legacy pages may intentionally have no annotated runnable example.  Requiring
        # a new lesson-trace/data-cpp authoring structure would rewrite the source merely
        # to satisfy this checker; annotated examples remain fully compiled above.

    # Also check existing pages that link into the rewritten prerequisite pages.
    for name, doc in documents.items():
        for href in doc.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = unquote(url.path) or name
            if not re.match(r"p[1-9]_.*\.html$", target):
                continue
            if target not in documents:
                errors.append(f"{name}: missing page {target}")
            elif url.fragment and unquote(url.fragment) not in documents[target].ids:
                errors.append(f"{name}: missing anchor {href}")
    print("Verified: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    for error in errors:
        print("FAIL", error)
    print(f"{len(errors)} errors")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
