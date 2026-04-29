---
name: csv-cleaner
description: Diagnose and clean messy CSV, TSV, or spreadsheet files. Use whenever the user uploads a CSV or TSV that has data quality issues, asks to "clean", "normalize", "fix", or "deduplicate" tabular data, or hands over a file with encoding problems, broken headers, type inconsistencies, duplicate rows, or missing values. Triggers on "clean this CSV", "fix this data", "this spreadsheet is messy", "deduplicate these rows", or any data-quality request on a tabular file. Always run scripts/diagnose.py before making changes so the cleanup is informed by what is actually broken.
---

# CSV Cleaner

Two-phase workflow: diagnose first, clean second. Never start fixing before knowing what is broken.

## Phase 1: Diagnose

Run `scripts/diagnose.py` on the input file:

```bash
python scripts/diagnose.py <path-to-file>
```

The script reports:

- Encoding (utf-8, latin-1, utf-16, etc.)
- Delimiter (comma, tab, semicolon)
- Quote character and escape behavior
- Header row detection (present, absent, or duplicate)
- Row count
- Column count consistency across rows
- Type inference per column (integer, float, date, string, mixed)
- Null distribution per column
- Duplicate row count

Read the output carefully before doing anything else. The diagnosis tells you which fixes apply.

## Phase 2: Clean

Apply fixes in this order:

1. Fix encoding: re-read with detected encoding, write as utf-8.
2. Normalize line endings to `\n`.
3. Strip BOM and zero-width characters.
4. Fix headers: lowercase, snake_case, replace spaces with underscores, ensure uniqueness.
5. Trim whitespace from every cell.
6. Coerce types where the column is type-consistent.
7. Standardize null representations: empty string, "NA", "null", "n/a" all become empty.
8. Deduplicate exact rows.
9. Validate column count consistency. Flag rows that do not match the header.

Do not silently change data. If a fix alters values, report the count.

## Output

Save the cleaned file as `<original-name>-cleaned.csv` in the same directory. Always utf-8, always comma-delimited, always with a header row.

Then emit a summary:

````
## Diagnosis
<key findings from phase 1>

## Fixes applied
- <fix>: <count of rows or cells affected>
- <fix>: <count>

## Manual review needed
- <issue that the script could not fix safely>
````

## When to refuse

If the file appears to be a different format (Excel binary, JSON, fixed-width), do not try to clean it as CSV. Tell the user what the file actually is and suggest the right tool.

If the file has fewer than 5 rows after deduplication, ask the user whether the input is correct before continuing.
