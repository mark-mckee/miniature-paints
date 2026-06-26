#!/usr/bin/env python3
"""Resolve Turbo Dork colour-shift descriptions into ordered sRGB hex stops.

The descriptions use ISCC-NBS-style "universal colour language" (a modifier such as
vivid/deep/light plus a hue such as "bluish green"), with 2-3 stops joined by " to "
or "<a> through <b> to <c>". These hex values are deliberate, hand-picked
*approximations* of the ISCC-NBS centroids — good enough for a decorative gradient
swatch, not colorimetric reference values.
"""
import re

# Two effect descriptions that name no discrete stops.
PASTEL_RAINBOW = ["#FBD6D6", "#FBEFD0", "#D8F2CE", "#CFEFEF", "#D6DBF6", "#ECD6F2"]
FULL_RAINBOW = ["#FF3B30", "#FF9500", "#FFCC00", "#34C759", "#0A84FF", "#5E5CE6", "#AF52DE"]

# "<modifier> <hue>" -> approximate sRGB hex. Covers exactly the vocabulary in the
# 40 Turbo Dork turboshift/zenishift descriptions.
COLOR_STOPS = {
    # blue-greens / greens
    "strong bluish green": "#0E8F7E",
    "brilliant bluish green": "#1FB89B",
    "vivid bluish green": "#00A887",
    "moderate bluish green": "#3E8E80",
    "brilliant green": "#27B463",
    "deep greenish blue": "#0A6E86",
    "dark greenish blue": "#16586B",
    "light greenish blue": "#7FC6D6",
    "vivid greenish blue": "#0093B5",
    "brilliant greenish blue": "#1FA9C9",
    # yellow-greens / olives
    "light yellowish green": "#BFE6A0",
    "moderate yellowish green": "#6FA85C",
    "vivid yellowish green": "#5FBF3F",
    "moderate yellow green": "#7E9B3C",
    "pale yellow green": "#C3CCA0",
    "deep yellow green": "#5C7A1E",
    "moderate olive green": "#5C5E2A",
    "moderate olive": "#6E6A2E",
    "light olive": "#A9A05A",
    "light olive brown": "#9C7E3E",
    "greyish olive brown": "#6E5F47",
    "deep yellowish green": "#2F7A3A",
    # yellows / golds
    "strong orange yellow": "#E8A21E",
    "vivid orange yellow": "#FFB300",
    "deep yellow": "#D9A100",
    "dark yellow": "#B8902A",
    "light greenish yellow": "#EFE9A0",
    "brilliant yellow": "#FBE251",
    "moderate yellow gold": "#C9A23A",
    "strong greenish yellow": "#C9C71E",
    # oranges
    "brilliant orange": "#FF8A33",
    "strong orange": "#E8731E",
    "deep reddish orange": "#C5391B",
    "moderate reddish orange": "#C75B3C",
    "light orange yellow": "#FFCB7A",
    # reds / pinks
    "deep purplish red": "#9E1E4E",
    "vivid reddish purple": "#A111A6",
    "deep red": "#A41020",
    "dark purplish red": "#6E1430",
    "very deep reddish purple": "#5E0E40",
    "strong purplish red": "#B01E63",
    "strong pink": "#F07AA0",
    "deep purplish pink": "#D14A8C",
    "brilliant purplish pink": "#F06FB6",
    "pale purplish pink": "#E9BFD2",
    "light yellowish pink": "#F6C7B0",
    "light purplish pink": "#E3A8C6",
    # purples / violets
    "dark purple": "#4A2168",
    "strong purple": "#7A2E9E",
    "moderate purple": "#7E4F94",
    "vivid purple": "#9B1FB0",
    "brilliant purple": "#A24FCB",
    "strong violet": "#5E2E9E",
    "light violet": "#B79AD6",
    "very light violet": "#D8C7EE",
    "vivid violet": "#8A1FD6",
    "pale purple": "#B3A0C4",
    "deep purple": "#3E1A66",
    "very deep black purple": "#2A0E3A",
    # purplish blues / blues
    "strong purplish blue": "#3B3FB0",
    "vivid purplish blue": "#2A2FD6",
    "vivid blue": "#1763E0",
    "strong blue": "#1F6FC4",
    "deep blue": "#103C9E",
    "very light blue": "#BFD8F2",
}

_TAIL_RE = re.compile(r'\s*(effect\s+)?shifting metallic\s*$', re.I)


def resolve(description):
    """Return the ordered list of hex stops for a colour-shift description.

    Raises KeyError on any colour phrase missing from COLOR_STOPS so the
    vocabulary stays exhaustive.
    """
    d = description.strip().lower().replace('-', ' ')
    d = re.sub(r'\s+', ' ', d)
    if 'mother of pearl' in d or 'nacre' in d or 'pastel rainbow' in d:
        return list(PASTEL_RAINBOW)
    if 'rainbow' in d:
        return list(FULL_RAINBOW)
    d = _TAIL_RE.sub('', d)
    parts = re.split(r'\s+through\s+|\s+to\s+', d)
    stops = []
    for p in parts:
        p = p.strip()
        if p not in COLOR_STOPS:
            raise KeyError(f"unknown colour stop {p!r} in {description!r}")
        stops.append(COLOR_STOPS[p])
    return stops
