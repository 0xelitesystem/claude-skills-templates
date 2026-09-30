"""Tests for skills/csv-cleaner/scripts/diagnose.py.

Run from the repo root with the standard library only:

    python -B -m unittest discover -s tests -v
"""

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills" / "csv-cleaner" / "scripts" / "diagnose.py"
)


def load_diagnose():
    # Keep the skill folder clean: no __pycache__ next to the script.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("diagnose", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = previous


diagnose = load_diagnose()

ESC = "\x1b"
BEL = "\x07"

# Characters a terminal acts on: C0 except tab and newline, DEL, C1, bidi.
CONTROL_CHARS = (
    [chr(c) for c in range(0x20) if chr(c) not in "\t\n"]
    + [chr(c) for c in range(0x7F, 0xA0)]
    + [chr(c) for c in (0x061C, 0x200E, 0x200F)]
    + [chr(c) for c in range(0x202A, 0x202F)]
    + [chr(c) for c in range(0x2066, 0x206A)]
)


def run_main(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = diagnose.main(str(path))
    return rc, buf.getvalue()


def raw_controls(text):
    return sorted({hex(ord(ch)) for ch in text if ch in CONTROL_CHARS})


class TerminalEscapeInjectionTest(unittest.TestCase):
    """claude-skills-templates-1: file-derived text must not reach the
    terminal with raw control characters in it."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_crafted_header_escape_sequences_are_neutralised(self):
        # The exact payload from the finding: OSC 0 window title, OSC 52
        # clipboard write, then cursor-up plus erase-line six times.
        header = (
            "id" + ESC + "]0;pwned" + BEL
            + ESC + "]52;c;d2hvYW1p" + BEL
            + (ESC + "[1A" + ESC + "[2K") * 6
            + "FAKE"
        )
        path = self.dir / "evil.csv"
        with open(path, "w", newline="", encoding="utf-8") as fh:
            fh.write('"' + header + '",name,name\n1,a\n1,a\n2,b,c\n')

        rc, out = run_main(path)

        self.assertEqual(rc, 0)
        self.assertEqual(raw_controls(out), [])
        # The header is still shown, with the controls visible as escapes.
        self.assertIn(
            "  [0] id\\x1b]0;pwned\\x07\\x1b]52;c;d2hvYW1p\\x07"
            + "\\x1b[1A\\x1b[2K" * 6
            + "FAKE: type=int, nulls=0 (0.0%)",
            out,
        )
        # The warnings the skill relies on are still printed.
        self.assertIn("WARNING: rows have inconsistent column counts.", out)
        self.assertIn("WARNING: duplicate header names: ['name']", out)

    def test_every_control_class_in_a_header_is_escaped(self):
        header = "a" + "".join(CONTROL_CHARS) + "z"
        path = self.dir / "controls.csv"
        with open(path, "w", newline="", encoding="utf-8") as fh:
            fh.write('"' + header + '",b\n1,2\n3,4\n')

        rc, out = run_main(path)

        self.assertEqual(rc, 0)
        self.assertEqual(raw_controls(out), [])
        self.assertIn("\\x1b", out)
        self.assertIn("\\x7f", out)
        self.assertIn("\\x9b", out)
        self.assertIn("\\u202e", out)
        self.assertIn("\\u2066", out)
        self.assertIn("\\u061c", out)

    def test_filename_in_not_found_message_is_escaped(self):
        # The file does not need to exist, so this works on every OS.
        name = "missing" + ESC + "]0;pwned" + BEL + "‮.csv"
        rc, out = run_main(self.dir / name)

        self.assertEqual(rc, 1)
        self.assertEqual(raw_controls(out), [])
        self.assertIn("missing\\x1b]0;pwned\\x07\\u202e.csv", out)

    def test_filename_in_report_title_is_escaped(self):
        # U+202E is a legal filename character on Windows, macOS and Linux.
        name = "report‮gpj.csv"
        path = self.dir / name
        path.write_bytes(b"a,b\n1,2\n3,4\n")

        rc, out = run_main(path)

        self.assertEqual(rc, 0)
        self.assertEqual(raw_controls(out), [])
        self.assertIn("## File: report\\u202egpj.csv\n", out)


class NormalOutputUnchangedTest(unittest.TestCase):
    """Ordinary files must produce byte-for-byte the same report as before."""

    def test_normal_report_is_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv"
            path.write_bytes(
                (
                    "ID,Full Name,Café,Café,Score\n"
                    "1,Ann Lee,Paris,Paris,3.5\n"
                    "2,Bob,,Lyon,4\n"
                    "2,Bob,,Lyon,4\n"
                    "3,Zoë,NA,Nice,x\n"
                    "4,Dee,Rome\n"
                ).encode("utf-8")
            )
            rc, out = run_main(path)

        expected = (
            "## File: sample.csv\n"
            "Encoding: utf-8-sig\n"
            "Size: 113 bytes\n"
            "\n"
            "Delimiter: ','\n"
            "Quote char: '\"'\n"
            "Has header (sniffed): False\n"
            "\n"
            "## Structure\n"
            "Header columns: 5\n"
            "Data rows: 5\n"
            "Column count distribution: {5: 4, 3: 1}\n"
            "WARNING: rows have inconsistent column counts.\n"
            "\n"
            "## Headers\n"
            "WARNING: duplicate header names: ['Café']\n"
            "Headers with spaces: ['Full Name']\n"
            "Headers with uppercase: ['ID', 'Full Name', 'Café', 'Café', 'Score']\n"
            "\n"
            "## Columns\n"
            "  [0] ID: type=int, nulls=0 (0.0%)\n"
            "  [1] Full Name: type=string, nulls=0 (0.0%)\n"
            "  [2] Café: type=string, nulls=3 (60.0%)\n"
            "  [3] Café: type=string, nulls=1 (20.0%)\n"
            "  [4] Score: type=mixed(float,int,string), nulls=1 (20.0%)\n"
            "\n"
            "## Duplicates\n"
            "Exact duplicate rows: 1\n"
        )
        self.assertEqual(rc, 0)
        self.assertEqual(out, expected)


if __name__ == "__main__":
    unittest.main()
