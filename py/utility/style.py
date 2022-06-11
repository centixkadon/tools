
ANSI_BEL  = "\x07"
ANSI_BS   = "\x08"
ANSI_HT   = "\x09"
ANSI_LF   = "\x0a"
ANSI_FF   = "\x0c"
ANSI_CR   = "\x0d"
ANSI_ESC  = "\x1b"

ANSI_SS2  = f"{ANSI_ESC}N"
ANSI_SS3  = f"{ANSI_ESC}O"
ANSI_DCS  = f"{ANSI_ESC}P"
ANSI_CSI  = f"{ANSI_ESC}["
ANSI_ST   = f"{ANSI_ESC}\\"
ANSI_OSC  = f"{ANSI_ESC}]"
ANSI_SOS  = f"{ANSI_ESC}X"
ANSI_PM   = f"{ANSI_ESC}^"
ANSI_APC  = f"{ANSI_ESC}_"

ANSI_CUU  = f"{ANSI_CSI}{{n}}A"
ANSI_CUD  = f"{ANSI_CSI}{{n}}B"
ANSI_CUF  = f"{ANSI_CSI}{{n}}C"
ANSI_CUB  = f"{ANSI_CSI}{{n}}D"
ANSI_CNL  = f"{ANSI_CSI}{{n}}E"
ANSI_CPL  = f"{ANSI_CSI}{{n}}F"
ANSI_CHA  = f"{ANSI_CSI}{{n}}G"
ANSI_CUP  = f"{ANSI_CSI}{{n}};{{m}}H"
ANSI_ED   = f"{ANSI_CSI}{{n}}J"
ANSI_EL   = f"{ANSI_CSI}{{n}}K"
ANSI_SU   = f"{ANSI_CSI}{{n}}S"
ANSI_SD   = f"{ANSI_CSI}{{n}}T"
ANSI_HVP  = f"{ANSI_CSI}{{n}};{{m}}f"
ANSI_SGR  = f"{ANSI_CSI}{{n}}m"



def format_sgr(n:str):
  return ANSI_SGR.format(n=n)



class color_type:

  def __init__(self, *args, color_attrs:dict[str,str], color_prefix:str, **kwargs):
    self._color_attrs = color_attrs
    self._color_prefix = color_prefix

  @property
  def default_attr(self):
    return self._color_attrs["default_attr"]

  @property
  def black_attr(self):
    return self._color_attrs["black_attr"]

  @property
  def red_attr(self):
    return self._color_attrs["red_attr"]

  @property
  def green_attr(self):
    return self._color_attrs["green_attr"]

  @property
  def yellow_attr(self):
    return self._color_attrs["yellow_attr"]

  @property
  def blue_attr(self):
    return self._color_attrs["blue_attr"]

  @property
  def magenta_attr(self):
    return self._color_attrs["magenta_attr"]

  @property
  def cyan_attr(self):
    return self._color_attrs["cyan_attr"]

  @property
  def white_attr(self):
    return self._color_attrs["white_attr"]

  @property
  def bright_black_attr(self):
    return self._color_attrs["bright_black_attr"]

  @property
  def bright_red_attr(self):
    return self._color_attrs["bright_red_attr"]

  @property
  def bright_green_attr(self):
    return self._color_attrs["bright_green_attr"]

  @property
  def bright_yellow_attr(self):
    return self._color_attrs["bright_yellow_attr"]

  @property
  def bright_blue_attr(self):
    return self._color_attrs["bright_blue_attr"]

  @property
  def bright_magenta_attr(self):
    return self._color_attrs["bright_magenta_attr"]

  @property
  def bright_cyan_attr(self):
    return self._color_attrs["bright_cyan_attr"]

  @property
  def bright_white_attr(self):
    return self._color_attrs["bright_white_attr"]

  def rgb_attr(self, r:int, g:int, b:int):
    if not 0 <= r < 6:
      raise KeyError("red should be in [0, 6)")
    if not 0 <= g < 6:
      raise KeyError("green should be in [0, 6)")
    if not 0 <= b < 6:
      raise KeyError("blue should be in [0, 6)")
    return f"{self._color_prefix};5;{r * 36 + g * 6 + b + 16}"

  def gray_attr(self, s:int):
    if not 0 <= s < 24:
      raise KeyError("scale should be in [0, 24)")
    return f"{self._color_prefix};5;{s + 232}"

  def rgb24_attr(self, r:int, g:int, b:int):
    if not 0 <= r < 256:
      raise KeyError("red should be in [0, 256)")
    if not 0 <= g < 256:
      raise KeyError("green should be in [0, 256)")
    if not 0 <= b < 256:
      raise KeyError("blue should be in [0, 256)")
    return f"{self._color_prefix};2;{r};{g};{b}"

  @property
  def default(self):
    return format_sgr(self.default_attr)

  @property
  def black(self):
    return format_sgr(self.black_attr)

  @property
  def red(self):
    return format_sgr(self.red_attr)

  @property
  def green(self):
    return format_sgr(self.green_attr)

  @property
  def yellow(self):
    return format_sgr(self.yellow_attr)

  @property
  def blue(self):
    return format_sgr(self.blue_attr)

  @property
  def magenta(self):
    return format_sgr(self.magenta_attr)

  @property
  def cyan(self):
    return format_sgr(self.cyan_attr)

  @property
  def white(self):
    return format_sgr(self.white_attr)

  @property
  def bright_black(self):
    return format_sgr(self.bright_black_attr)

  @property
  def bright_red(self):
    return format_sgr(self.bright_red_attr)

  @property
  def bright_green(self):
    return format_sgr(self.bright_green_attr)

  @property
  def bright_yellow(self):
    return format_sgr(self.bright_yellow_attr)

  @property
  def bright_blue(self):
    return format_sgr(self.bright_blue_attr)

  @property
  def bright_magenta(self):
    return format_sgr(self.bright_magenta_attr)

  @property
  def bright_cyan(self):
    return format_sgr(self.bright_cyan_attr)

  @property
  def bright_white(self):
    return format_sgr(self.bright_white_attr)

  def rgb(self, r:int, g:int, b:int):
    return format_sgr(self.rgb_attr(r, g, b))

  def gray(self, s:int):
    return format_sgr(self.gray_attr(s))

  def rgb24(self, r:int, g:int, b:int):
    return format_sgr(self.rgb_attr(r, g, b))

  def __getitem__(self, key):
    return getattr(self, key)



class foreground_type(color_type):

  def __init__(self):
    super().__init__(color_attrs={
      "default_attr":         "39",
      "black_attr":           "30",
      "red_attr":             "31",
      "green_attr":           "32",
      "yellow_attr":          "33",
      "blue_attr":            "34",
      "magenta_attr":         "35",
      "cyan_attr":            "36",
      "white_attr":           "37",
      "bright_black_attr":    "90",
      "bright_red_attr":      "91",
      "bright_green_attr":    "92",
      "bright_yellow_attr":   "93",
      "bright_blue_attr":     "94",
      "bright_magenta_attr":  "95",
      "bright_cyan_attr":     "96",
      "bright_white_attr":    "97",
    }, color_prefix="38")

foreground = foreground_type()

class background_type(color_type):

  def __init__(self):
    super().__init__(color_attrs={
      "default_attr":         "49",
      "black_attr":           "40",
      "red_attr":             "41",
      "green_attr":           "42",
      "yellow_attr":          "43",
      "blue_attr":            "44",
      "magenta_attr":         "45",
      "cyan_attr":            "46",
      "white_attr":           "47",
      "bright_black_attr":    "100",
      "bright_red_attr":      "101",
      "bright_green_attr":    "102",
      "bright_yellow_attr":   "103",
      "bright_blue_attr":     "104",
      "bright_magenta_attr":  "105",
      "bright_cyan_attr":     "106",
      "bright_white_attr":    "107",
    }, color_prefix="48")

background = background_type()



class display_type:

  def __init__(self, *args, display_attrs:dict[str,str], **kwargs):
    self._display_attrs = display_attrs

  @property
  def reset_attr(self):
    return self._display_attrs["reset_attr"]

  @property
  def bold_attr(self):
    return self._display_attrs["bold_attr"]

  @property
  def italic_attr(self):
    return self._display_attrs["italic_attr"]

  @property
  def underline_attr(self):
    return self._display_attrs["underline_attr"]

  @property
  def blink_attr(self):
    return self._display_attrs["blink_attr"]

  @property
  def reverse_attr(self):
    return self._display_attrs["reverse_attr"]

  @property
  def hidden_attr(self):
    return self._display_attrs["hidden_attr"]

  @property
  def strike_attr(self):
    return self._display_attrs["strike_attr"]

  @property
  def bold_off_attr(self):
    return self._display_attrs["bold_off_attr"]

  @property
  def italic_off_attr(self):
    return self._display_attrs["italic_off_attr"]

  @property
  def underline_off_attr(self):
    return self._display_attrs["underline_off_attr"]

  @property
  def blink_off_attr(self):
    return self._display_attrs["blink_off_attr"]

  @property
  def reverse_off_attr(self):
    return self._display_attrs["reverse_off_attr"]

  @property
  def hidden_off_attr(self):
    return self._display_attrs["hidden_off_attr"]

  @property
  def strike_off_attr(self):
    return self._display_attrs["strike_off_attr"]

  @property
  def reset(self):
    return format_sgr(self.reset_attr)

  @property
  def bold(self):
    return format_sgr(self.bold_attr)

  @property
  def italic(self):
    return format_sgr(self.italic_attr)

  @property
  def underline(self):
    return format_sgr(self.underline_attr)

  @property
  def blink(self):
    return format_sgr(self.blink_attr)

  @property
  def reverse(self):
    return format_sgr(self.reverse_attr)

  @property
  def hidden(self):
    return format_sgr(self.hidden_attr)

  @property
  def strike(self):
    return format_sgr(self.strike_attr)

  @property
  def bold_off(self):
    return format_sgr(self.bold_off_attr)

  @property
  def italic_off(self):
    return format_sgr(self.italic_off_attr)

  @property
  def underline_off(self):
    return format_sgr(self.underline_off_attr)

  @property
  def blink_off(self):
    return format_sgr(self.blink_off_attr)

  @property
  def reverse_off(self):
    return format_sgr(self.reverse_off_attr)

  @property
  def hidden_off(self):
    return format_sgr(self.hidden_off_attr)

  @property
  def strike_off(self):
    return format_sgr(self.strike_off_attr)

display = display_type(display_attrs={
  "reset_attr": "0",
  "bold_attr": "1",
  "italic_attr": "3",
  "underline_attr": "4",
  "blink_attr": "5",
  "reverse_attr": "7",
  "hidden_attr": "8",
  "strike_attr": "9",
  "bold_off_attr": "22",
  "italic_off_attr": "23",
  "underline_off_attr": "24",
  "blink_off_attr": "25",
  "reverse_off_attr": "27",
  "hidden_off_attr": "28",
  "strike_off_attr": "29",
})



class style_type:

  _foreground_colors = [color.removesuffix("_attr") for color in foreground._color_attrs]
  _background_colors = ["bg_" + color.removesuffix("_attr") for color in background._color_attrs]

  def __init__(self, *args, style=None, bold:str|None=None, italic:str|None=None, underline:str|None=None, blink:str|None=None, reverse:str|None=None, hidden:str|None=None, strike:str|None=None, fg:str|None=None, bg:str|None=None, **kwargs):

    if isinstance(style, __class__):
      self._bold        = style._bold
      self._italic      = style._italic
      self._underline   = style._underline
      self._blink       = style._blink
      self._reverse     = style._reverse
      self._hidden      = style._hidden
      self._strike      = style._strike
      self._fg          = style._fg
      self._bg          = style._bg
    else:
      self._bold        = ""
      self._italic      = ""
      self._underline   = ""
      self._blink       = ""
      self._reverse     = ""
      self._hidden      = ""
      self._strike      = ""
      self._fg          = ""
      self._bg          = ""

    if bold        is not None: self._bold        = bold
    if italic      is not None: self._italic      = italic
    if underline   is not None: self._underline   = underline
    if blink       is not None: self._blink       = blink
    if reverse     is not None: self._reverse     = reverse
    if hidden      is not None: self._hidden      = hidden
    if strike      is not None: self._strike      = strike
    if fg          is not None: self._fg          = fg
    if bg          is not None: self._bg          = bg

  @property
  def _fmt(self):
    fmt = ""
    if self._bold:        fmt += f";{self._bold}"
    if self._italic:      fmt += f";{self._italic}"
    if self._underline:   fmt += f";{self._underline}"
    if self._blink:       fmt += f";{self._blink}"
    if self._reverse:     fmt += f";{self._reverse}"
    if self._hidden:      fmt += f";{self._hidden}"
    if self._strike:      fmt += f";{self._strike}"
    if self._fg:          fmt += f";{self._fg}"
    if self._bg:          fmt += f";{self._bg}"
    return fmt.removeprefix(";")

  def __str__(self):
    fmt = self._fmt
    return format_sgr(fmt)

  def __repr__(self):
    return f"<{__class__.__module__}.{__class__.__name__} bold={self._bold} italic={self._italic} underline={self._underline} blink={self._blink} reverse={self._reverse} hidden={self._hidden} strike={self._strike} fg={self._fg} bg={self._bg}>"

  @property
  def bold_clear(self):
    return __class__(style=self, bold="")

  @property
  def italic_clear(self):
    return __class__(style=self, italic="")

  @property
  def underline_clear(self):
    return __class__(style=self, underline="")

  @property
  def blink_clear(self):
    return __class__(style=self, blink="")

  @property
  def reverse_clear(self):
    return __class__(style=self, reverse="")

  @property
  def hidden_clear(self):
    return __class__(style=self, hidden="")

  @property
  def strike_clear(self):
    return __class__(style=self, strike="")

  @property
  def fg_clear(self):
    return __class__(style=self, fg="")

  @property
  def bg_clear(self):
    return __class__(style=self, bg="")

  @property
  def bold(self):
    return __class__(style=self, bold=display.bold_attr)

  @property
  def italic(self):
    return __class__(style=self, italic=display.italic_attr)

  @property
  def underline(self):
    return __class__(style=self, underline=display.underline_attr)

  @property
  def blink(self):
    return __class__(style=self, blink=display.blink_attr)

  @property
  def reverse(self):
    return __class__(style=self, reverse=display.reverse_attr)

  @property
  def hidden(self):
    return __class__(style=self, hidden=display.hidden_attr)

  @property
  def strike(self):
    return __class__(style=self, strike=display.strike_attr)

  @property
  def bold_off(self):
    return __class__(style=self, bold=display.bold_off_attr)

  @property
  def italic_off(self):
    return __class__(style=self, italic=display.italic_off_attr)

  @property
  def underline_off(self):
    return __class__(style=self, underline=display.underline_off_attr)

  @property
  def blink_off(self):
    return __class__(style=self, blink=display.blink_off_attr)

  @property
  def reverse_off(self):
    return __class__(style=self, reverse=display.reverse_off_attr)

  @property
  def hidden_off(self):
    return __class__(style=self, hidden=display.hidden_off_attr)

  @property
  def strike_off(self):
    return __class__(style=self, strike=display.strike_off_attr)

  @property
  def default(self):
    return __class__(style=self, fg=foreground.default_attr)

  @property
  def black(self):
    return __class__(style=self, fg=foreground.black_attr)

  @property
  def red(self):
    return __class__(style=self, fg=foreground.red_attr)

  @property
  def green(self):
    return __class__(style=self, fg=foreground.green_attr)

  @property
  def yellow(self):
    return __class__(style=self, fg=foreground.yellow_attr)

  @property
  def blue(self):
    return __class__(style=self, fg=foreground.blue_attr)

  @property
  def magenta(self):
    return __class__(style=self, fg=foreground.magenta_attr)

  @property
  def cyan(self):
    return __class__(style=self, fg=foreground.cyan_attr)

  @property
  def white(self):
    return __class__(style=self, fg=foreground.white_attr)

  @property
  def bright_black(self):
    return __class__(style=self, fg=foreground.bright_black_attr)

  @property
  def bright_red(self):
    return __class__(style=self, fg=foreground.bright_red_attr)

  @property
  def bright_green(self):
    return __class__(style=self, fg=foreground.bright_green_attr)

  @property
  def bright_yellow(self):
    return __class__(style=self, fg=foreground.bright_yellow_attr)

  @property
  def bright_blue(self):
    return __class__(style=self, fg=foreground.bright_blue_attr)

  @property
  def bright_magenta(self):
    return __class__(style=self, fg=foreground.bright_magenta_attr)

  @property
  def bright_cyan(self):
    return __class__(style=self, fg=foreground.bright_cyan_attr)

  @property
  def bright_white(self):
    return __class__(style=self, fg=foreground.bright_white_attr)

  def rgb(self, r:int, g:int, b:int):
    return __class__(style=self, fg=foreground.rgb_attr(r, g, b))

  def gray(self, s:int):
    return __class__(style=self, fg=foreground.gray_attr(s))

  def rgb24(self, r:int, g:int, b:int):
    return __class__(style=self, fg=foreground.rgb24_attr(r, g, b))

  @property
  def bg_default(self):
    return __class__(style=self, bg=background.default_attr)

  @property
  def bg_black(self):
    return __class__(style=self, bg=background.black_attr)

  @property
  def bg_red(self):
    return __class__(style=self, bg=background.red_attr)

  @property
  def bg_green(self):
    return __class__(style=self, bg=background.green_attr)

  @property
  def bg_yellow(self):
    return __class__(style=self, bg=background.yellow_attr)

  @property
  def bg_blue(self):
    return __class__(style=self, bg=background.blue_attr)

  @property
  def bg_magenta(self):
    return __class__(style=self, bg=background.magenta_attr)

  @property
  def bg_cyan(self):
    return __class__(style=self, bg=background.cyan_attr)

  @property
  def bg_white(self):
    return __class__(style=self, bg=background.white_attr)

  @property
  def bg_bright_black(self):
    return __class__(style=self, bg=background.bright_black_attr)

  @property
  def bg_bright_red(self):
    return __class__(style=self, bg=background.bright_red_attr)

  @property
  def bg_bright_green(self):
    return __class__(style=self, bg=background.bright_green_attr)

  @property
  def bg_bright_yellow(self):
    return __class__(style=self, bg=background.bright_yellow_attr)

  @property
  def bg_bright_blue(self):
    return __class__(style=self, bg=background.bright_blue_attr)

  @property
  def bg_bright_magenta(self):
    return __class__(style=self, bg=background.bright_magenta_attr)

  @property
  def bg_bright_cyan(self):
    return __class__(style=self, bg=background.bright_cyan_attr)

  @property
  def bg_bright_white(self):
    return __class__(style=self, bg=background.bright_white_attr)

  def bg_rgb(self, r:int, g:int, b:int):
    return __class__(style=self, bg=background.rgb_attr(r, g, b))

  def bg_gray(self, s:int):
    return __class__(style=self, bg=background.gray_attr(s))

  def bg_rgb24(self, r:int, g:int, b:int):
    return __class__(style=self, bg=background.rgb24_attr(r, g, b))

  def __call__(self, s:str):
    if not s:
      return ""

    fmt = self._fmt
    if fmt:
      return f"{format_sgr(fmt)}{s}{display.reset}"
    return s

  def __getitem__(self, key:str):
    r:style_type = getattr(self, key)
    return r

style = style_type()
