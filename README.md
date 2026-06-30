# Name, Set, RGB, and Hex values of Miniature Paints

**33 brands · 11,812 paints**

This is a collection of hobby/miniature -painting paints from some of the most popular brands around the world.

I forked the original repo from Arcturus5404/miniature-paints, who had made a significant amount of progress, but has not updated the repo in several years. I needed a clean and up to date dataset for my own paint/supplies inventory app.

The original paint list was scraped by Arcturus5404 from the [Miniature Painter Pro](https://miniaturepainterpro.app/) team.

Feel free to use or improve any of these paints in your own personal projects. This repo will remain free for you to use in your projects, all I ask is a credit.

## RGB & HEX
Unless otherwise stated, the RGB/Hex values for all paints are an approximation, as most manufacturers hold the spectral info secret. For the most part, the values have been sampled from product images either from the brands website or product catalogue.

## Tasks

- [X] Add contact information for each brand where possible
- [ ] Update all paint sets to match the current product catalogues
  - [X] AK
  - [X] Acrilex
  - [ ] Apple Barrel
  - [ ] Army Painter
  - [ ] Arteza
  - [ ] Coat D'Armes
  - [ ] Creature Caster
  - [X] Duncan Rhodes' Two Thin Coats
  - [ ] Golden
  - [ ] Green Stuff World
  - [ ] Humbrol
  - [ ] Italeri
  - [ ] Kimera Kolors
  - [X] Liquitex
  - [ ] Mig
  - [ ] Mission Models
  - [ ] Monument Hobbies
  - [ ] Mr Hobby
  - [ ] Mr Paint
  - [X] P3
  - [ ] Pantone
  - [ ] RAL
  - [ ] Reaper
  - [X] Revell
  - [ ] Scale75
  - [ ] Tamiya
  - [ ] Tom Color
  - [X] Turbo Dork
  - [ ] Vallejo
  - [ ] Warcolours
  - [X] Warhammer Colour


## JSON & Markdown

The `paints/markdown/*.md` tables are the single source of truth; everything below is generated from them by `scripts/build_paints.py`. The aggregate `paints.json` lives at the root of the `/paints` directory, and the per-brand files live in `paints/json/`. See [`paints/README.md`](paints/README.md) for a per-brand index.

Every output file is described by a formal [JSON Schema](https://json-schema.org/) (Draft 2020-12) under [`schema/`](schema/): [`schema/paints.schema.json`](schema/paints.schema.json) for the aggregate and [`schema/brand.schema.json`](schema/brand.schema.json) for the per-brand files. Each data file links to its schema via a relative `$schema` reference, so editors like VS Code validate it automatically.

### Top level — `paints.json`

```jsonc
{
  "$schema": "../schema/paints.schema.json",  // relative link to the schema
  "schema": "miniature-paints/v3",            // version tag
  "brandCount": 33,
  "paintCount": 11812,
  "brands": {
    "AK": { /* brand object */ },     // keyed by file stem (paints/<stem>.md)
    "Acrilex": { /* brand object */ },
    // ...
  }
}
```

The per-brand files `paints/json/<stem>.json` each contain a single **brand object** (without the `brandCount`/`brands` wrapper). Each one is prefixed with its own `$schema` and `schema` keys so the file is self-identifying; the brand objects embedded under `brands` in `paints.json` omit those two keys (the aggregate already carries them).

### Brand object

```jsonc
{
  "$schema": "../../schema/brand.schema.json",   // standalone files only
  "schema": "miniature-paints/v3",            // standalone files only
  "displayName": "Acrilex",
  "company": "Acrilex Tintas Especiais S.A.",
  "address": { "street": "", "city": "", "postcode": "", "country": "" },
  "contactEmail": "...",
  "contactForm": "...",
  "website": "...",
  "phone": "...",
  "updatedCatalogueRequested": "25/06/2026",   // string, may be ""
  "paintCount": 95,
  "paints": [ /* paint objects */ ]
}
```

### Paint object

```jsonc
{
  "id": "acrilex-831",          // string, unique within a brand: "<brand-slug>-<code|name-slug>"
  "name": "Almond",             // string
  "code": "831",                // string | null  (null for brands with no code column)
  "set": "Acrilex Paints",      // string | null
  "hex": "#D97037",             // string | null  — single colour (null for colour-shift paints)
  "rgb": { "r": 217, "g": 112, "b": 55 },   // object | null  (r/g/b are integers)
  "shiftColors": null,          // string[] | null — ordered hex stops for colour-shift paints
  "potSizes": [                 // object[] | null
    { "raw": "37ml",  "value": 37,  "unit": "ml" },
    { "raw": "60ml",  "value": 60,  "unit": "ml" },
    { "raw": "250ml", "value": 250, "unit": "ml" }
  ],
  "description": null           // string | null
}
```

#### Field notes

- `hex` and `shiftColors` are mutually exclusive: a normal paint has `hex` set and `shiftColors: null`; a colour-shift paint has `hex: null` and `shiftColors` as an array of hex stops.
- `rgb` is `null` if any of R/G/B is missing or non-numeric in the source table.
- `potSizes` is an array when one or more sizes are known, or `null` when no size is recorded. Each entry is `{ raw, value, unit }`; if a size string can't be parsed, `value`/`unit` are `null` but `raw` is preserved. Single-size brands are 1-element arrays.

> [!NOTE]
> The `schema` field is versioned. `v3` renamed the former singular `potSize` object to the `potSizes` array — consumers reading pot sizes should expect an array (or `null`).

## Paints by brand

<!-- START -->
|  |  |  |
| :---: | :---: | :---: |
|  <a href="paints/markdown/AK.md"> <img src="logos/AK.png" height="70" /> <br/> AK</a>|  <a href="paints/markdown/Acrilex.md"> <img src="logos/Acrilex.png" height="70" /> <br/> Acrilex</a>|
|  <a href="paints/markdown/AppleBarrel.md"> <img src="logos/AppleBarrel.png" height="70" /> <br/> Apple Barrel</a>|  <a href="paints/markdown/Army_Painter.md"> <img src="logos/Army_Painter.png" height="70" /> <br/> Army Painter</a>|  <a href="paints/markdown/Arteza.md"> <img src="logos/Arteza.png" height="70" /> <br/> Arteza</a>|
|  <a href="paints/markdown/CoatDArmes.md"> <img src="logos/CoatDArmes.png" height="70" /> <br/> Coat D Armes</a>|  <a href="paints/markdown/Creature.md"> <img src="logos/Creature.png" height="70" /> <br/> Creature</a>| <a href="paints/markdown/Duncan.md"> <img src="logos/Duncan.png" height="70" /> <br/> Two Thin Coats</a>|  <a href="paints/markdown/FolkArt.md"> <img src="logos/FolkArt.png" height="70" /> <br/> Folk Art</a>|  <a href="paints/markdown/Foundry.md"> <img src="logos/Foundry.png" height="70" /> <br/> Foundry</a>|
|  <a href="paints/markdown/Golden.md"> <img src="logos/Golden.png" height="70" /> <br/> Golden</a>|  <a href="paints/markdown/GreenStuffWorld.md"> <img src="logos/GreenStuffWorld.png" height="70" /> <br/> Green Stuff World</a>|  <a href="paints/markdown/Humbrol.md"> <img src="logos/Humbrol.png" height="70" /> <br/> Humbrol</a>|
|  <a href="paints/markdown/Italeri.md"> <img src="logos/Italeri.png" height="70" /> <br/> Italeri</a>|  <a href="paints/markdown/KimeraKolors.md"> <img src="logos/KimeraKolors.png" height="70" /> <br/> Kimera Kolors</a>|  <a href="paints/markdown/Liquitex.md"> <img src="logos/Liquitex.png" height="70" /> <br/> Liquitex</a>|
|  <a href="paints/markdown/Mig.md"> <img src="logos/Mig.png" height="70" /> <br/> Mig</a>|  <a href="paints/markdown/MissionModels.md"> <img src="logos/MissionModels.png" height="70" /> <br/> Mission Models</a>|  <a href="paints/markdown/Monument.md"> <img src="logos/Monument.png" height="70" /> <br/> Monument</a>|
|  <a href="paints/markdown/MrHobby.md"> <img src="logos/MrHobby.png" height="70" /> <br/> Mr Hobby</a>|  <a href="paints/markdown/MrPaint.md"> <img src="logos/MrPaint.png" height="70" /> <br/> Mr Paint</a>|  <a href="paints/markdown/P3.md"> <img src="logos/P3.png" height="70" /> <br/> P3</a>|
|  <a href="paints/markdown/Pantone.md"> <img src="logos/Pantone.png" height="70" /> <br/> Pantone</a>|  <a href="paints/markdown/RAL.md"> <img src="logos/RAL.png" height="70" /> <br/> RAL</a>|  <a href="paints/markdown/Reaper.md"> <img src="logos/Reaper.png" height="70" /> <br/> Reaper</a>|
|  <a href="paints/markdown/Revell.md"> <img src="logos/Revell.png" height="70" /> <br/> Revell</a>|  <a href="paints/markdown/Scale75.md"> <img src="logos/Scale75.png" height="70" /> <br/> Scale75</a>|  <a href="paints/markdown/Tamiya.md"> <img src="logos/Tamiya.png" height="70" /> <br/> Tamiya</a>|
|  <a href="paints/markdown/TomColor.md"> <img src="logos/TomColor.png" height="70" /> <br/> Tom Color</a>|  <a href="paints/markdown/TurboDork.md"> <img src="logos/TurboDork.png" height="70" /> <br/> Turbo Dork</a>|  <a href="paints/markdown/Vallejo.md"> <img src="logos/Vallejo.png" height="70" /> <br/> Vallejo</a>|
|  <a href="paints/markdown/Warcolours.md"> <img src="logos/Warcolours.png" height="70" /> <br/> Warcolours</a>| <a href="paints/markdown/Warhammer_Colour.md"> <img src="logos/Warhammer_Colour.png" height="70" /> <br/> Warhammer Colour</a>||
<!-- END -->

## Thanks

### Turbo Dork
❤️ A huge thank you to Greg over at Turbo Dork for supplying an up to date list of their products in an easy to use spreadsheet, and for their permission and support to include their paints here. Your help is very much appreciated.

❤️ A huge thank you to Jesper over at The Army Painter for providing me with an up to date spreadsheet of all their current paints and sets. Thank you for your support.

## Notes
> [!NOTE]
> I am not affiliated in any way with the [Miniature Painter Pro](https://miniaturepainterpro.app/) team or app, nor am I affiliated with any of the brands shared here.

> [!NOTE]
> There's a lot of paints! Tens of thousands of them! I have been feeding the latest product catalogues into Claude and asking it to pull out all the paints and the sets they belong to. After I process and verify the output, Claude then updates the tables in the markdown files. AI can make mistakes, and so can I, so there may be errors. I verify as much as possible, but if a mistake slips through feel free to open a PR and I'll correct it. 
>
>There's still an awful lot of legwork involved. Claude is basically my unpaid intern.