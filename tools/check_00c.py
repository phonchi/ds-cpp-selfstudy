#!/usr/bin/env python3
"""Validate the Windows VS Code lesson and compile its anonymous project patterns."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "00c_vscode_windows.html"


class LessonParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.current_pre: str | None = None
        self.pre_text: dict[str, list[str]] = {}
        self.images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "pre" and data.get("id"):
            self.current_pre = data["id"]
            self.pre_text[self.current_pre] = []
        if tag == "img" and data.get("src"):
            self.images.append(data["src"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre":
            self.current_pre = None

    def handle_data(self, data: str) -> None:
        if self.current_pre:
            self.pre_text[self.current_pre].append(data)


def fail(message: str) -> None:
    raise SystemExit(f"00C CHECK FAILED: {message}")


def parse_lesson() -> tuple[dict[str, dict], list[str], str]:
    source = PAGE.read_text(encoding="utf-8")
    parser = LessonParser()
    parser.feed(source)
    expected = {"tasks-json", "launch-json", "properties-json"}
    if set(parser.pre_text) != expected:
        fail(f"JSON block ids are {sorted(parser.pre_text)}, expected {sorted(expected)}")
    configs = {}
    for key, chunks in parser.pre_text.items():
        try:
            configs[key] = json.loads("".join(chunks))
        except json.JSONDecodeError as exc:
            fail(f"{key} is not valid JSON: {exc}")
    return configs, parser.images, source


def validate_configs(configs: dict[str, dict]) -> None:
    task = configs["tasks-json"]["tasks"][0]
    launch = configs["launch-json"]["configurations"][0]
    props = configs["properties-json"]["configurations"][0]

    if task["label"] != launch["preLaunchTask"]:
        fail("tasks label and launch preLaunchTask differ")
    compiler = task["command"].replace("\\", "/")
    intellisense = props["compilerPath"].replace("\\", "/")
    debugger = launch["miDebuggerPath"].replace("\\", "/")
    if compiler != intellisense:
        fail("tasks command and IntelliSense compilerPath differ")
    if compiler.rsplit("/", 1)[0] != debugger.rsplit("/", 1)[0]:
        fail("g++ and gdb do not come from the same bin directory")

    args = task["args"]
    for flag in ("-std=c++17", "-Wall", "-Wextra", "-g"):
        if flag not in args:
            fail(f"tasks args are missing {flag}")
    sources = [arg for arg in args if arg.endswith(".cpp")]
    if len(sources) < 2 or any("*" in src for src in sources):
        fail("multi-file task must explicitly list at least two .cpp files")


def validate_assets(images: list[str]) -> None:
    expected = {
        "assets/00c/cpp-extension.png",
        "assets/00c/msys2-toolchain.jpg",
        "assets/00c/debug-breakpoint.png",
    }
    if set(images) != expected:
        fail(f"image set is {sorted(images)}, expected {sorted(expected)}")
    for rel in expected:
        path = ROOT / rel
        head = path.read_bytes()[:8] if path.exists() else b""
        if not (head == b"\x89PNG\r\n\x1a\n" or head.startswith(b"\xff\xd8\xff")):
            fail(f"{rel} is missing or is not a PNG/JPEG image")


def validate_scope(source: str) -> None:
    public_files = [
        "00a_why_code.html",
        "00b_setup.html",
        "00c_vscode_windows.html",
        "index.html",
        "README.md",
        "HANDOFF.md",
    ]
    numbered_homework = re.compile(
        r"\bHW\s*0?[1-5]\b|Homework\s*0?[1-5]\b|作業\s*(?:[1-5一二三四五])",
        re.I,
    )
    for rel in public_files:
        if numbered_homework.search((ROOT / rel).read_text(encoding="utf-8")):
            fail(f"{rel} leaks a numbered, unreleased homework reference")
    required = [
        "00b_setup.html#windows",
        "g++ --version",
        "gdb --version",
        "tasks.json",
        "launch.json",
        "c_cpp_properties.json",
        "multiple definition",
        "undefined reference",
    ]
    missing = [text for text in required if text not in source]
    if missing:
        fail(f"lesson is missing required concepts: {missing}")


def run(command: list[str], cwd: Path) -> str:
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if proc.returncode:
        fail(f"command failed: {' '.join(command)}\n{proc.stderr}")
    return proc.stdout.strip()


def executable(root: Path, name: str) -> Path:
    for candidate in (root / name, root / f"{name}.exe"):
        if candidate.exists():
            return candidate
    fail(f"compiler did not create {name} or {name}.exe")


def compile_anonymous_patterns(require_gdb: bool = False) -> None:
    compiler = shutil.which("g++")
    if not compiler:
        fail("g++ is required to validate the anonymous examples")
    with tempfile.TemporaryDirectory(prefix="check-00c-") as raw:
        root = Path(raw)
        (root / "MyClass.h").write_text(
            "#pragma once\nclass MyClass { public: int value() const; };\n",
            encoding="utf-8",
        )
        (root / "MyClass.cpp").write_text(
            '#include "MyClass.h"\nint MyClass::value() const { return 42; }\n',
            encoding="utf-8",
        )
        (root / "main.cpp").write_text(
            '#include <iostream>\n#include "MyClass.h"\n'
            'int main(){ MyClass x; std::cout << x.value() << "\\n"; }\n',
            encoding="utf-8",
        )
        run(
            [compiler, "-std=c++17", "-Wall", "-Wextra", "-g", "-I.",
             "main.cpp", "MyClass.cpp", "-o", "multi"],
            root,
        )
        multi = executable(root, "multi")
        if run([str(multi)], root) != "42":
            fail("ordinary header + implementation pattern returned the wrong output")

        (root / "support.cpp").write_text("int supplied(){ return 7; }\n", encoding="utf-8")
        (root / "provided_entry.cpp").write_text(
            '#include <iostream>\n#include "support.cpp"\n'
            'int main(){ std::cout << supplied() << "\\n"; }\n',
            encoding="utf-8",
        )
        run(
            [compiler, "-std=c++17", "-Wall", "-Wextra", "-g",
             "provided_entry.cpp", "-o", "provided"],
            root,
        )
        provided = executable(root, "provided")
        if run([str(provided)], root) != "7":
            fail("provided-template include pattern returned the wrong output")

        (root / "input.txt").write_text("course-data\n", encoding="utf-8")
        (root / "args.cpp").write_text(
            "#include <fstream>\n#include <iostream>\n#include <string>\n"
            "int main(int argc,char** argv){ if(argc<3) return 2; "
            "std::ifstream in(argv[1]); std::string s; in>>s; "
            "std::cout<<s<<' '<<argv[2]<<'\\n'; }\n",
            encoding="utf-8",
        )
        run([compiler, "-std=c++17", "-Wall", "-Wextra", "-g", "args.cpp", "-o", "args"], root)
        args_program = executable(root, "args")
        if run([str(args_program), "input.txt", "--nogui"], root) != "course-data --nogui":
            fail("args + working-directory pattern returned the wrong output")

        target = run([compiler, "-dumpmachine"], root)
        if "mingw" in target:
            run(
                [compiler, "-std=c++17", "-Wall", "-Wextra", "-g", "args.cpp",
                 "-o", "win-link-smoke", "-lgdi32"],
                root,
            )
            executable(root, "win-link-smoke")

        debugger = shutil.which("gdb")
        if require_gdb and not debugger:
            fail("--require-gdb was set but gdb is unavailable")
        if debugger:
            transcript = run(
                [debugger, "--batch", "-ex", "break main", "-ex", "run",
                 "-ex", "info locals", str(multi)],
                root,
            )
            if "Breakpoint" not in transcript:
                fail("gdb batch smoke test did not stop at main")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-gdb",
        action="store_true",
        help="fail unless the GDB batch smoke test can run (used by Windows CI)",
    )
    args = parser.parse_args()
    configs, images, source = parse_lesson()
    validate_configs(configs)
    validate_assets(images)
    validate_scope(source)
    compile_anonymous_patterns(require_gdb=args.require_gdb)
    suffix = ", GDB smoke" if shutil.which("gdb") else ""
    print(f"00C CHECK OK: 3 JSON configs, 3 attributed images, 3 compiled patterns{suffix}")


if __name__ == "__main__":
    main()
