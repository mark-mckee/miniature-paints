#!/usr/bin/env python3
"""Rebuild paints/TurboDork.md from the updated catalogue CSV.

- Adds a Code column; fills Pot Size (22ml) and Description for every paint.
- Metallic paints: carry the EXISTING hex/rgb from the current TurboDork.md
  (matched by normalized name); CSV colour values are ignored.
- Colour-shift paints (turboshift/zenishift): no single colour. Their description
  is resolved to ordered hex stops (scripts/color_language.py), a gradient swatch
  PNG is written to swatches/turbodork/<slug>.png, and the Hex cell references the
  image plus the stop hexes as backtick codes.

The markdown is the source of truth; run scripts/build_paints.py afterwards to
regenerate paints.json / json/TurboDork.json.

Usage:
    python scripts/build_turbodork.py [CSV_PATH] [--dry-run]
"""
import os, re, sys, csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color_language import resolve  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(ROOT, "paints", "TurboDork.md")
SWATCH_DIR = os.path.join(ROOT, "swatches", "turbodork")

HEADER = "|Name|Code|Set|R|G|B|Hex|Pot Size|Description|"
SEPARATOR = "|---|---|---|---|---|---|---|---|---|"

# CSV (new) name -> existing TurboDork.md name, where they differ.
RENAME = {
    "Apple Seed": "Appleseed",
    "Black ICE": "Black Ice",
    "Multi Pass": "Multipass",
    "Tin": "Tin Star",
}


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower())


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def cells(line):
    return [c.strip() for c in line.split('|')[1:-1]]


def hex_to_rgb(h):
    h = h.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def read_md(path):
    with open(path, encoding='utf-8') as f:
        return [l.rstrip('\r') for l in f.read().split('\n')]


def parse_existing(lines):
    """Return (pre_lines, existing_by_norm_name, post_lines).

    pre_lines: everything up to and including the line before the paint header.
    post_lines: the footer block after the table.
    existing: {norm(name): {'name','r','g','b','hex'}}
    """
    hidx = next(i for i, l in enumerate(lines)
                if l.startswith('|') and 'Name' in l and 'Hex' in l)
    header = cells(lines[hidx])
    pre = lines[:hidx]
    existing = {}
    i = hidx + 2
    while i < len(lines) and lines[i].startswith('|'):
        row = dict(zip(header, cells(lines[i])))
        name = row.get('Name', '')
        m = re.search(r'#([0-9A-Fa-f]{6})', row.get('Hex', ''))
        existing[norm(name)] = {
            'name': name,
            'r': row.get('R', ''), 'g': row.get('G', ''), 'b': row.get('B', ''),
            'hex': '#' + m.group(1).upper() if m else '',
        }
        i += 1
    post = lines[i:]
    return pre, existing, post


def hex_cell_single(hexv):
    h = hexv.lstrip('#').upper()
    return f"![#{h}](https://placehold.co/15x15/{h}/{h}.png) `#{h}`"


def gradient_png(stops, path, w=60, h=15):
    from PIL import Image
    cols = [hex_to_rgb(s) for s in stops]
    n = len(cols)
    img = Image.new("RGB", (w, h))
    px = img.load()
    for x in range(w):
        if n == 1:
            r, g, b = cols[0]
        else:
            t = x / (w - 1) * (n - 1)
            i = min(int(t), n - 2)
            f = t - i
            (r0, g0, b0), (r1, g1, b1) = cols[i], cols[i + 1]
            r = round(r0 + (r1 - r0) * f)
            g = round(g0 + (g1 - g0) * f)
            b = round(b0 + (b1 - b0) * f)
        for y in range(h):
            px[x, y] = (r, g, b)
    img.save(path)


def hex_cell_shift(slug_name, stops):
    img = f'<img src="../swatches/turbodork/{slug_name}.png" height="15" />'
    codes = ' '.join(f'`{s}`' for s in stops)
    return f'{img} {codes}'


def esc(s):
    return s.replace('|', '\\|')


def main():
    args = [a for a in sys.argv[1:] if a != '--dry-run']
    dry = '--dry-run' in sys.argv
    csv_path = args[0] if args else os.path.join(
        os.path.dirname(SWATCH_DIR), "turbo-dork-paints.csv")
    if not os.path.isfile(csv_path):
        sys.exit(f"CSV not found: {csv_path}")

    with open(csv_path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    metallic = [r for r in rows if r['set'].strip().lower() == 'metallic']
    shift = [r for r in rows if r['set'].strip().lower() != 'metallic']

    lines = read_md(MD_PATH)
    pre, existing, post = parse_existing(lines)

    out_rows = []

    # --- metallic: carry existing hex/rgb, matched by normalized name ---
    for r in metallic:
        new_name = r['name'].strip()
        old_name = RENAME.get(new_name, new_name)
        ex = existing.get(norm(old_name))
        if ex is None:
            sys.exit(f"No existing colour for metallic {new_name!r} (looked up {old_name!r})")
        out_rows.append('|'.join([
            '', esc(new_name), r['code'].strip(), 'Metallic',
            ex['r'], ex['g'], ex['b'], hex_cell_single(ex['hex']),
            '22ml', esc(r['description'].strip()), '',
        ]))

    # --- colour-shift: resolve stops, generate gradient swatch ---
    if not dry:
        os.makedirs(SWATCH_DIR, exist_ok=True)
    swatches = 0
    for r in shift:
        name = r['name'].strip()
        stops = resolve(r['description'].strip())
        sl = slug(name)
        if dry:
            print(f"  {name}: {stops}")
        else:
            gradient_png(stops, os.path.join(SWATCH_DIR, f"{sl}.png"))
            swatches += 1
        setv = r['set'].strip().capitalize()
        out_rows.append('|'.join([
            '', esc(name), r['code'].strip(), setv,
            '', '', '', hex_cell_shift(sl, stops),
            '22ml', esc(r['description'].strip()), '',
        ]))

    # integrity: every row has 9 cells
    ncols = len(cells(HEADER))
    for r in out_rows:
        assert len(cells(r)) == ncols, f"row has {len(cells(r))} cells: {r}"

    if dry:
        print(f"\nDry run OK: {len(metallic)} metallic + {len(shift)} shift "
              f"= {len(out_rows)} rows, all stops resolved.")
        return

    new_lines = pre + [HEADER, SEPARATOR] + out_rows + post
    with open(MD_PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(new_lines))

    print(f"Wrote {MD_PATH}: {len(metallic)} metallic + {len(shift)} shift "
          f"= {len(out_rows)} rows; {swatches} swatches in {SWATCH_DIR}")


if __name__ == "__main__":
    main()
