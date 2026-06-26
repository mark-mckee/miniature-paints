#!/usr/bin/env python3
"""One-off migration: append empty 'Pot Size' and 'Description' columns to the
paint table in every paints/<Brand>.md file.

Idempotent: a file whose paint header already contains 'Pot Size' is skipped, so
re-running is safe. Only the paint table is touched; the Brand Details table above
it is never in range (the walk starts at the paint header). Run once:

    python scripts/migrate_add_columns.py
"""
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAINTS_DIR = os.path.join(ROOT, "paints")


def is_table_row(line):
    return line.startswith('|')


def cell_count(line):
    # cells between the outer pipes, matching build_paints.cells()
    return len(line.split('|')[1:-1])


def migrate_file(path):
    """Return number of data rows migrated, or None if skipped."""
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    lines = raw.split('\n')
    stripped = [l.rstrip('\r') for l in lines]

    header_idx = next((i for i, l in enumerate(stripped)
                       if is_table_row(l) and 'Name' in l and 'Hex' in l), None)
    if header_idx is None:
        return None
    if 'Pot Size' in stripped[header_idx]:
        return None  # already migrated

    def append_cells(line, suffix):
        # every table line ends with a single '|'; append the new cells after it
        assert line.rstrip().endswith('|')
        return line.rstrip() + suffix

    out = list(stripped)
    out[header_idx] = append_cells(out[header_idx], 'Pot Size|Description|')
    out[header_idx + 1] = append_cells(out[header_idx + 1], '---|---|')
    expected = cell_count(out[header_idx])

    rows = 0
    i = header_idx + 2
    while i < len(out) and is_table_row(out[i]):
        out[i] = append_cells(out[i], '||')  # two empty cells
        assert cell_count(out[i]) == expected, \
            f"{path}: row {i} has {cell_count(out[i])} cells, expected {expected}"
        rows += 1
        i += 1

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    return rows


def main():
    total = 0
    migrated = skipped = 0
    for path in sorted(glob.glob(os.path.join(PAINTS_DIR, '*.md'))):
        n = migrate_file(path)
        name = os.path.basename(path)
        if n is None:
            print(f"  skip  {name}")
            skipped += 1
        else:
            print(f"  ok    {name}: {n} rows")
            migrated += 1
            total += n
    print(f"\nMigrated {migrated} files ({skipped} skipped), {total} data rows total")


if __name__ == "__main__":
    main()
