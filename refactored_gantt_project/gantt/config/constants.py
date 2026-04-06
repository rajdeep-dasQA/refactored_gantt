"""
Global constants: colours, priority palette, and calendar settings.
All hex values are stored WITHOUT the leading 'FF' alpha prefix;
the style helpers in renderer/styles.py add it when building openpyxl objects.
"""

# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------
WORK_DAYS: list[int] = [0, 1, 2, 3, 4]   # Monday–Friday (weekday() indices)

# ---------------------------------------------------------------------------
# Colour tokens
# ---------------------------------------------------------------------------
HDR_BG   = "4B5320"   # dark-olive header background
HDR_FG   = "FFFFFF"   # header foreground (white)
ALT_ROW  = "F5F5F5"   # alternate row background
WHITE    = "FFFFFF"
BORDER_C = "CCCCCC"   # default thin-border colour
INFO_BG  = "D9E1F2"   # info-box background
INFO_FG  = "1F3864"   # info-box text colour
INFO_BD  = "4472C4"   # info-box border colour

# ---------------------------------------------------------------------------
# Priority palette  {priority_int: (bg_hex, fg_hex)}
# ---------------------------------------------------------------------------
PRIORITY_COLORS: dict[int, tuple[str, str]] = {
    1: ("4CAF82", "FFFFFF"),   # green
    2: ("5B9BD5", "FFFFFF"),   # blue
    3: ("ED7D31", "FFFFFF"),   # orange
    4: ("FFC000", "000000"),   # yellow
    5: ("70AD47", "FFFFFF"),   # olive-green
}
DEFAULT_COLOR: tuple[str, str] = ("9E9E9E", "FFFFFF")   # grey fallback

# Convenience: bar fill colour keyed by priority
BAR_COLORS: dict[int, str] = {p: bg for p, (bg, _) in PRIORITY_COLORS.items()}
DEFAULT_BAR: str = DEFAULT_COLOR[0]

# ---------------------------------------------------------------------------
# Sheet / layout defaults
# ---------------------------------------------------------------------------
FONT_NAME           = "Calibri"
COL_W_SUMMARY       = 36
COL_W_ASSIGNEE      = 18
COL_W_PRIORITY      = 8
COL_W_HOURS         = 10
COL_W_DAY_PERIOD    = 7
COL_W_WEEK_PERIOD   = 9
ROW_H_TITLE         = 28
ROW_H_HEADER        = 34
ROW_H_TASK          = 18
ROW_H_TOTAL         = 20
ROW_H_LEGEND        = 14
ROW_H_CONFIG        = 20
