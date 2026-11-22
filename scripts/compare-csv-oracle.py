#!/usr/bin/env python3
"""Compare CSV rows with source-first JSON `expected_rows`, preserving multiplicity.

Usage: compare-csv-oracle.py EXPECTATIONS.json ACTUAL.csv col1,col2,...
This compares serialized table tuples; equal tuples can represent multiple AST
entities. The oracle must be independently prepared before results are read.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path


def main():
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    expected_path, actual_path = map(Path, sys.argv[1:3])
    columns = sys.argv[3].split(',')
    if not columns or any(not c for c in columns) or len(columns) != len(set(columns)):
        print('columns must be nonempty and unique', file=sys.stderr)
        return 2
    try:
        spec = json.loads(expected_path.read_text(encoding='utf-8'))
        raw = spec['expected_rows']
        if not isinstance(raw, list) or any(not isinstance(row, list) or len(row) != len(columns) for row in raw):
            raise ValueError('expected_rows must be an array of arrays matching the selected columns')
        with actual_path.open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream, strict=True)
            if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)):
                raise ValueError('CSV header is missing or has duplicate fields')
            if any(column not in reader.fieldnames for column in columns):
                raise ValueError(f'CSV header missing selected columns: {columns}')
            actual = Counter()
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError('CSV row has a different field count than its header')
                actual[tuple(row[column] for column in columns)] += 1
        expected = Counter(tuple(str(value) for value in row) for row in raw)
    except (OSError, UnicodeError, KeyError, ValueError, TypeError, csv.Error) as exc:
        print(f'Cannot compare: {exc}', file=sys.stderr)
        return 2
    if actual != expected:
        for label, diff in [('missing', expected - actual), ('unexpected', actual - expected)]:
            for row, count in sorted(diff.items()):
                print(f'{label} x{count}: {row}', file=sys.stderr)
        return 1
    print(f'Matched {sum(expected.values())} rows including multiplicity; this does not verify underlying AST entity identity.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
