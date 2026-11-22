#!/usr/bin/env python3
"""Check tracked and untracked ledger text receipts without changing them.

This checks simple inline local Markdown targets and JSON/CSV syntax, not claim truth, provenance,
secrets or the meaning of a query result. Run from any directory inside the repo.
"""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)')


def main():
    result = subprocess.run(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        cwd=ROOT, stdout=subprocess.PIPE, check=True,
    )
    paths = sorted({ROOT / name for name in result.stdout.decode().split('\0') if name})
    errors = []
    counts = {'md': 0, 'json': 0, 'csv': 0}
    for path in paths:
        if not path.is_file():
            continue
        suffix = path.suffix.lower().lstrip('.')
        if suffix not in counts:
            continue
        counts[suffix] += 1
        rel = path.relative_to(ROOT)
        try:
            if suffix == 'json':
                def reject_constant(value):
                    raise ValueError(f'invalid JSON constant: {value}')
                json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)
            elif suffix == 'csv':
                with path.open(encoding='utf-8', newline='') as stream:
                    list(csv.reader(stream, strict=True))
            else:
                text = path.read_text(encoding='utf-8')
                # Skip fenced examples; they are not necessarily live links.
                text = re.sub(r'(?ms)^\s*(```+|~~~+).*?^\s*\1\s*$', '', text)
                for target in LINK.findall(text):
                    target = target.strip()
                    if target.startswith('<') and target.endswith('>'):
                        target = target[1:-1]
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    candidate = (path.parent / unquote(parsed.path)).resolve()
                    if not candidate.exists():
                        errors.append(f'{rel}: missing local link {target}')
        except (OSError, UnicodeError, ValueError, csv.Error) as exc:
            errors.append(f'{rel}: {exc}')
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {counts['md']} Markdown, {counts['json']} JSON, and {counts['csv']} CSV files; {len(errors)} error(s).")
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
