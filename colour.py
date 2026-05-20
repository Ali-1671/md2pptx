"""
colour
"""

from pptx.dml.color import RGBColor, MSO_THEME_COLOR
import re

RGBRegex = re.compile("#([0-9a-fA-F]{6})")

_THEME_COLOUR_MAP = {
    "NONE": MSO_THEME_COLOR.NOT_THEME_COLOR,
    "ACCENT 1": MSO_THEME_COLOR.ACCENT_1,
    "ACCENT 2": MSO_THEME_COLOR.ACCENT_2,
    "ACCENT 3": MSO_THEME_COLOR.ACCENT_3,
    "ACCENT 4": MSO_THEME_COLOR.ACCENT_4,
    "ACCENT 5": MSO_THEME_COLOR.ACCENT_5,
    "ACCENT 6": MSO_THEME_COLOR.ACCENT_6,
    "BACKGROUND 1": MSO_THEME_COLOR.BACKGROUND_1,
    "BACKGROUND 2": MSO_THEME_COLOR.BACKGROUND_2,
    "DARK 1": MSO_THEME_COLOR.DARK_1,
    "DARK 2": MSO_THEME_COLOR.DARK_2,
    "FOLLOWED HYPERLINK": MSO_THEME_COLOR.FOLLOWED_HYPERLINK,
    "HYPERLINK": MSO_THEME_COLOR.HYPERLINK,
    "LIGHT 1": MSO_THEME_COLOR.LIGHT_1,
    "LIGHT 2": MSO_THEME_COLOR.LIGHT_2,
    "TEXT 1": MSO_THEME_COLOR.TEXT_1,
    "TEXT 2": MSO_THEME_COLOR.TEXT_2,
    "MIXED": MSO_THEME_COLOR.MIXED,
}

def setColour(x, colour):
    colourType, colourValue = colour
    if colourType == "Theme":
        x.theme_color = colourValue
    else:
        x.rgb = RGBColor.from_string(colourValue[1:])


def parseThemeColour(value):
    themeColour = _THEME_COLOUR_MAP.get(value.upper())

    if themeColour is None:
        raise ValueError(f"Unknown theme colour: {value!r}")

    return themeColour


def parseColour(value):
    if value[0] == "#":
        return ("RGB", value)
    else:
        return ("Theme", parseThemeColour(value))

def parseRGB(str):
    if RGBmatch := RGBRegex.match(str):
        # Matches
        return (True, RGBmatch.group(1))
    else:
        return (False, "")

