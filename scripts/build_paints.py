#!/usr/bin/env python3
"""Build paints.json from the per-brand markdown tables in paints/.

Each paints/<Brand>.md file holds:
  * an H1 title  -> brand displayName
  * a "Brand Details" key/value table -> company / address / contact info
  * a paints table (Name, [Code], Set, R, G, B, Hex) -> the paint list

The generated paints.json is fully derived from these files, so the markdown
is the single source of truth. Run this whenever a brand .md file changes.
"""
import os, re, json, glob
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAINTS_DIR = os.path.join(ROOT, "paints")
OUT_PATH = os.path.join(ROOT, "paints.json")

HEX_RE = re.compile(r'#([0-9A-Fa-f]{6})')

# Brand Details table field -> location in the brand object.
# ("address", k) nests under address; (None, k) sits at brand top level.
DETAIL_MAP = {
    "company":  (None, "company"),
    "address":  ("address", "street"),
    "city":     ("address", "city"),
    "postcode": ("address", "postcode"),
    "country":  ("address", "country"),
    "email":    (None, "contactEmail"),
    "contact form": (None, "contactForm"),
    "website":  (None, "website"),
    "phone":    (None, "phone"),
    "updated catalogue requested": (None, "updatedCatalogueRequested"),
}


def fix(s):
    """Repair latin1-mis-decoded utf-8 mojibake if present."""
    try:
        return s.encode('latin1').decode('utf-8')
    except Exception:
        return s


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def cells(line):
    return [c.strip() for c in line.split('|')[1:-1]]


def parse_details(lines):
    """Return dict of lowercased field -> value from the Brand Details table."""
    out = {}
    start = next((i for i, l in enumerate(lines)
                  if l.strip().lower() == '## brand details'), None)
    if start is None:
        return out
    # find the '| Field | Value |' header after the heading
    hdr = next((i for i in range(start, min(start + 6, len(lines)))
                if lines[i].startswith('|') and 'Field' in lines[i] and 'Value' in lines[i]), None)
    if hdr is None:
        return out
    for l in lines[hdr + 2:]:
        if not l.startswith('|'):
            break
        c = cells(l)
        if len(c) >= 2 and c[0]:
            out[c[0].strip().lower()] = fix(c[1].strip())
    return out


def parse_paints(lines, brand_slug):
    header_idx = next((i for i, l in enumerate(lines)
                       if l.startswith('|') and 'Name' in l and 'Hex' in l), None)
    if header_idx is None:
        return []
    header = cells(lines[header_idx])

    paints, used_ids = [], set()
    for l in lines[header_idx + 2:]:
        if not l.startswith('|'):
            break
        c = cells(l)
        if not any(c):
            continue
        row = dict(zip(header, c))

        name = fix(row.get('Name', '').strip())
        code = fix(row.get('Code', '').strip()) if 'Code' in header else ''
        code = code or None
        setv = fix(row.get('Set', '').strip()) or None

        def to_int(v):
            v = (v or '').strip()
            return int(v) if v.isdigit() else None
        R, G, B = to_int(row.get('R')), to_int(row.get('G')), to_int(row.get('B'))

        m = HEX_RE.search(row.get('Hex', ''))
        hexv = '#' + m.group(1).upper() if m else None

        base = f"{brand_slug}-{slug(code) if code else slug(name)}"
        pid, n = base, 2
        while pid in used_ids:
            pid = f"{base}-{n}"
            n += 1
        used_ids.add(pid)

        paints.append({
            "id": pid,
            "name": name,
            "code": code,
            "set": setv,
            "hex": hexv,
            "rgb": {"r": R, "g": G, "b": B} if None not in (R, G, B) else None,
        })
    return paints


def build():
    brands = OrderedDict()
    total = 0
    for path in sorted(glob.glob(os.path.join(PAINTS_DIR, '*.md'))):
        stem = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding='utf-8') as f:
            lines = f.read().split('\n')
        lines = [l.rstrip('\r') for l in lines]

        display = next((fix(l[2:].strip()) for l in lines if l.startswith('# ')), stem)
        details = parse_details(lines)
        paints = parse_paints(lines, slug(stem))

        brand = OrderedDict()
        brand["displayName"] = display
        brand["company"] = ""
        brand["address"] = {"street": "", "city": "", "postcode": "", "country": ""}
        brand["contactEmail"] = ""
        brand["contactForm"] = ""
        brand["website"] = ""
        brand["phone"] = ""
        brand["updatedCatalogueRequested"] = ""
        for field, (group, key) in DETAIL_MAP.items():
            val = details.get(field, "")
            if group is None:
                brand[key] = val
            else:
                brand[group][key] = val
        brand["paintCount"] = len(paints)
        brand["paints"] = paints

        brands[stem] = brand
        total += len(paints)

    doc = OrderedDict()
    doc["schema"] = "miniature-paints/v1"
    doc["brandCount"] = len(brands)
    doc["paintCount"] = total
    doc["brands"] = brands
    return doc


def main():
    doc = build()
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"Wrote {OUT_PATH}: {doc['brandCount']} brands, {doc['paintCount']} paints")


if __name__ == "__main__":
    main()
