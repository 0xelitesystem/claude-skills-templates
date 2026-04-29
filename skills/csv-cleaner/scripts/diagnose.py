#!/usr/bin/env python3
"""
diagnose.py - Inspect a CSV or TSV file and report quality issues.

Usage:
    python diagnose.py <path-to-file>

Output: human-readable report on stdout. Exit code 0 on success, 1 on
unrecoverable input errors, 2 on usage errors.
"""

import csv
import io
import sys
from collections import Counter
from pathlib import Path


def detect_encoding(path: Path) -> str:
    """Try common encodings; return the first that decodes cleanly."""
    candidates = ["utf-8-sig", "utf-8", "latin-1", "utf-16", "cp1252"]
    raw = path.read_bytes()
    for enc in candidates:
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return "unknown"


def detect_dialect(sample: str):
    """Sniff delimiter and quoting from a sample. Fall back to comma."""
    try:
        return csv.Sniffer().sniff(sample, delimiters=",\t;|")
    except csv.Error:
        class FallbackDialect(csv.Dialect):
            delimiter = ","
            quotechar = '"'
            doublequote = True
            skipinitialspace = False
            lineterminator = "\n"
            quoting = csv.QUOTE_MINIMAL
        return FallbackDialect


def has_header(sample: str) -> bool:
    try:
        return csv.Sniffer().has_header(sample)
    except csv.Error:
        return False


def infer_type(values):
    """Best-effort type inference for a column."""
    types_seen = set()
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if s == "":
            continue
        if s.lower() in ("true", "false"):
            types_seen.add("bool")
            continue
        try:
            int(s)
            types_seen.add("int")
            continue
        except ValueError:
            pass
        try:
            float(s)
            types_seen.add("float")
            continue
        except ValueError:
            pass
        if any(c in s for c in "-/") and 8 <= len(s) <= 10:
            types_seen.add("date?")
            continue
        types_seen.add("string")

    if not types_seen:
        return "empty"
    if len(types_seen) == 1:
        return types_seen.pop()
    if types_seen == {"int", "float"}:
        return "float"
    return "mixed(" + ",".join(sorted(types_seen)) + ")"


def is_null(v) -> bool:
    if v is None:
        return True
    s = str(v).strip().lower()
    return s in ("", "na", "null", "n/a", "none", "nan")


def main(path_str: str) -> int:
    path = Path(path_str)
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 1

    encoding = detect_encoding(path)
    print(f"## File: {path.name}")
    print(f"Encoding: {encoding}")
    print(f"Size: {path.stat().st_size} bytes")
    print()

    if encoding == "unknown":
        print("Cannot decode with common encodings. Stop here and ask user.")
        return 1

    text = path.read_text(encoding=encoding)
    if not text.strip():
        print("File is empty.")
        return 0

    sample = text[:4096]
    dialect = detect_dialect(sample)
    print(f"Delimiter: {repr(dialect.delimiter)}")
    print(f"Quote char: {repr(dialect.quotechar)}")
    print(f"Has header (sniffed): {has_header(sample)}")
    print()

    reader = csv.reader(io.StringIO(text), dialect=dialect)
    rows = list(reader)
    if not rows:
        print("File has no parseable rows.")
        return 0

    header = rows[0]
    data = rows[1:]
    print("## Structure")
    print(f"Header columns: {len(header)}")
    print(f"Data rows: {len(data)}")

    counts = Counter(len(r) for r in data)
    print(f"Column count distribution: {dict(counts)}")
    if len(counts) > 1:
        print("WARNING: rows have inconsistent column counts.")
    print()

    print("## Headers")
    if len(set(header)) != len(header):
        dupes = [h for h, c in Counter(header).items() if c > 1]
        print(f"WARNING: duplicate header names: {dupes}")
    has_spaces = [h for h in header if " " in h]
    has_caps = [h for h in header if h != h.lower()]
    if has_spaces:
        print(f"Headers with spaces: {has_spaces}")
    if has_caps:
        print(f"Headers with uppercase: {has_caps}")
    print()

    print("## Columns")
    for i, name in enumerate(header):
        col_values = [r[i] if i < len(r) else None for r in data]
        nulls = sum(1 for v in col_values if is_null(v))
        col_type = infer_type(col_values)
        null_pct = (nulls / len(data) * 100) if data else 0
        print(f"  [{i}] {name}: type={col_type}, nulls={nulls} ({null_pct:.1f}%)")
    print()

    seen = set()
    exact_dupes = 0
    for r in data:
        key = tuple(r)
        if key in seen:
            exact_dupes += 1
        seen.add(key)
    print("## Duplicates")
    print(f"Exact duplicate rows: {exact_dupes}")

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
