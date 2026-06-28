# Name, Set, RGB, and Hex values of Miniature Paints

This repo is a collection of hobby/miniature painting paints from some of the most popular brands around the world.

I forked the original repo from Arcturus5404/miniature-paints, who had made a significant amount of progress, but has not updated the repo in several years. I needed a clean and up to date dataset for a project I wanted to work on.

The original paint list was scraped by Arcturus5404 from the [Miniature Painter Pro](https://miniaturepainterpro.app/) team.

Feel free to use or improve any of these paints in your own personal projects. Also feel free to submit PR's

> [!IMPORTANT]
> Whilst I have reviewed the original list of paint colours, and take as much care as I can determining the hex and RGB values for any of the paints are as accurate as possible, without official information from the brands themselves they are approximations. This is especially true for colour-shifting paints, which have no single colour — their swatches are generated from the manufacturer's colour descriptions and are only an approximation of how the paint actually shifts. Please refer to the brand's website or videos for a closer look at the colours and how they behave.

> [!NOTE]
> I am not affiliated in any way with the [Miniature Painter Pro](https://miniaturepainterpro.app/) team or app, nor am I affiliated with any of the brands shared here. So far, all knowledge of paints has been gathered from publicly available websites or product catalogues. I have contacted several brands for an up to date catalogue/spreadsheet. See the [Thanks](#thanks) section below to see who responded!

> [!NOTE]
> There's a lot of paints! Tens of thousands of them! I have been feeding the latest product catalogues into Claude and asking it to pull out all the paints and the sets they belong to. After I process and verify the output, Claude then updates the tables in the markdown files. AI can make mistakes, and so can I, so there may be errors. I verify as much as possible, but if a mistake slips through feel free to open a PR and I'll correct it. 
>
>There's still an awful lot of legwork involved. Claude is basically my unpaid intern.

## Tasks

[The expanded Tasks file is here](TODO.md)

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
  - [ ] Warhammer Colour


## JSON

At the root of this repo I have added a single JSON file that contains all brands and paints, and I have also included a JSON file for each brand individually for ease of use. These files are built every time I update the paints in the MD files and push to the repo through a worker action. 

The `paints/*.md` tables are the single source of truth; everything below is generated from them by `scripts/build_paints.py`.

Every output file is described by a formal [JSON Schema](https://json-schema.org/) (Draft 2020-12) under [`schema/`](schema/): [`schema/paints.schema.json`](schema/paints.schema.json) for the aggregate and [`schema/brand.schema.json`](schema/brand.schema.json) for the per-brand files. Each data file links to its schema via a relative `$schema` reference, so editors like VS Code validate it automatically.

### Top level — `paints.json`

```jsonc
{
  "$schema": "./schema/paints.schema.json",   // relative link to the schema
  "schema": "miniature-paints/v3",            // version tag
  "brandCount": 33,
  "paintCount": 11938,
  "brands": {
    "AK": { /* brand object */ },     // keyed by file stem (paints/<stem>.md)
    "Acrilex": { /* brand object */ },
    // ...
  }
}
```

The per-brand files `json/<stem>.json` each contain a single **brand object** (without the `brandCount`/`brands` wrapper). Each one is prefixed with its own `$schema` and `schema` keys so the file is self-identifying; the brand objects embedded under `brands` in `paints.json` omit those two keys (the aggregate already carries them).

### Brand object

```jsonc
{
  "$schema": "../schema/brand.schema.json",   // standalone files only
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
|  <a href="paints/AK.md"> <img src="logos/AK.png" height="70" /> <br/> AK</a>|  <a href="paints/Acrilex.md"> <img src="logos/Acrilex.png" height="70" /> <br/> Acrilex</a>|
|  <a href="paints/AppleBarrel.md"> <img src="logos/AppleBarrel.png" height="70" /> <br/> Apple Barrel</a>|  <a href="paints/Army_Painter.md"> <img src="logos/Army_Painter.png" height="70" /> <br/> Army Painter</a>|  <a href="paints/Arteza.md"> <img src="logos/Arteza.png" height="70" /> <br/> Arteza</a>|
|  <a href="paints/CoatDArmes.md"> <img src="logos/CoatDArmes.png" height="70" /> <br/> Coat D Armes</a>|  <a href="paints/Creature.md"> <img src="logos/Creature.png" height="70" /> <br/> Creature</a>| <a href="paints/Duncan.md"> <img src="logos/Duncan.png" height="70" /> <br/> Two Thin Coats</a>|  <a href="paints/FolkArt.md"> <img src="logos/FolkArt.png" height="70" /> <br/> Folk Art</a>|  <a href="paints/Foundry.md"> <img src="logos/Foundry.png" height="70" /> <br/> Foundry</a>|
|  <a href="paints/Golden.md"> <img src="logos/Golden.png" height="70" /> <br/> Golden</a>|  <a href="paints/GreenStuffWorld.md"> <img src="logos/GreenStuffWorld.png" height="70" /> <br/> Green Stuff World</a>|  <a href="paints/Humbrol.md"> <img src="logos/Humbrol.png" height="70" /> <br/> Humbrol</a>|
|  <a href="paints/Italeri.md"> <img src="logos/Italeri.png" height="70" /> <br/> Italeri</a>|  <a href="paints/KimeraKolors.md"> <img src="logos/KimeraKolors.png" height="70" /> <br/> Kimera Kolors</a>|  <a href="paints/Liquitex.md"> <img src="logos/Liquitex.png" height="70" /> <br/> Liquitex</a>|
|  <a href="paints/Mig.md"> <img src="logos/Mig.png" height="70" /> <br/> Mig</a>|  <a href="paints/MissionModels.md"> <img src="logos/MissionModels.png" height="70" /> <br/> Mission Models</a>|  <a href="paints/Monument.md"> <img src="logos/Monument.png" height="70" /> <br/> Monument</a>|
|  <a href="paints/MrHobby.md"> <img src="logos/MrHobby.png" height="70" /> <br/> Mr Hobby</a>|  <a href="paints/MrPaint.md"> <img src="logos/MrPaint.png" height="70" /> <br/> Mr Paint</a>|  <a href="paints/P3.md"> <img src="logos/P3.png" height="70" /> <br/> P3</a>|
|  <a href="paints/Pantone.md"> <img src="logos/Pantone.png" height="70" /> <br/> Pantone</a>|  <a href="paints/RAL.md"> <img src="logos/RAL.png" height="70" /> <br/> RAL</a>|  <a href="paints/Reaper.md"> <img src="logos/Reaper.png" height="70" /> <br/> Reaper</a>|
|  <a href="paints/Revell.md"> <img src="logos/Revell.png" height="70" /> <br/> Revell</a>|  <a href="paints/Scale75.md"> <img src="logos/Scale75.png" height="70" /> <br/> Scale75</a>|  <a href="paints/Tamiya.md"> <img src="logos/Tamiya.png" height="70" /> <br/> Tamiya</a>|
|  <a href="paints/TomColor.md"> <img src="logos/TomColor.png" height="70" /> <br/> Tom Color</a>|  <a href="paints/TurboDork.md"> <img src="logos/TurboDork.png" height="70" /> <br/> Turbo Dork</a>|  <a href="paints/Vallejo.md"> <img src="logos/Vallejo.png" height="70" /> <br/> Vallejo</a>|
|  <a href="paints/Warcolours.md"> <img src="logos/Warcolours.png" height="70" /> <br/> Warcolours</a>| <a href="paints/Warhammer_Colour.md"> <img src="logos/Warhammer_Colour.png" height="70" /> <br/> Warhammer Colour</a>||
<!-- END -->

## Thanks

### Turbo Dork
❤️ A huge thank you to Greg over at Turbo Dork for supplying an up to date list of their products in an easy to use spreadsheet! Your help is very much appreciated
