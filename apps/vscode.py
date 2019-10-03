import re
from talon.voice import Context, Key, press, Str
import talon.clip as clip
from ..misc.utils import parse_words_as_integer, repeat_function, optional_numerals, numerals, text, KeyComplete, press_wait, wait_press


context = Context("VSCode", bundle="com.microsoft.VSCode")

POPUP_WAIT_S = .75


def VSCodeTabComplete(actions):
    return KeyComplete('tab', POPUP_WAIT_S)(actions)


def go_to_line(line_number):
    press_wait("ctrl-g", 0.1)
    if(line_number is not None):
        Str(str(line_number))(None)
        wait_press("enter", 0.1)


def jump_to_line(m):
    line_number = parse_words_as_integer(m._words[3:])

    # Zeroth line should go to first line
    if line_number == 0:
        line_number = 1

    go_to_line(line_number)


def jump_tabs(m, goBackwards=False):
    number_of_tabs = parse_words_as_integer(m._words[1:])

    if number_of_tabs is None:
        return

    for i in range(0, number_of_tabs):
        if(goBackwards):
            press("cmd-alt-left")
        else:
            press("cmd-alt-right")


def jump_to_next_word_instance(m, is_forward=True):
    press("escape")
    press("cmd-f")
    Str(" ".join([str(s) for s in m.dgndictation[0]._words]))(None)
    if(is_forward):
        press("return")
    else:
        press("shift-return")


def jump_to_previous_word_instance(m):
    jump_to_next_word_instance(m, is_forward=False)


def select_lines(start_line, number_of_lines):
    press("ctrl-g")
    Str(str(start_line))(None)
    press("enter")
    for i in range(0, number_of_lines + 1):
        press("shift-down")

    # We're now on the line below where we want. Go back one to end up in the right spot
    press("shift-left")


def parse_line_ranges(m):
    divider = 0
    for word in m._words:
        if str(word) == "through":
            break
        divider += 1
    line_number_from = int(str(parse_words_as_integer(m._words[2:divider])))
    line_number_until = int(str(parse_words_as_integer(m._words[divider + 1:])))
    number_of_lines = line_number_until - line_number_from
    return (line_number_from, number_of_lines)


def select_and_modify_lines(m, action=None):
    line_number_start, number_of_lines = parse_line_ranges(m)
    select_lines(line_number_start, number_of_lines)
    if action is not None:
        wait_press(action, .1)


def find_word_in_files(m):
    press("escape")
    press("cmd-shift-f")
    Str(" ".join([str(s) for s in m.dgndictation[0]._words]))(None)
    press("return")


def jump_in_or_out(is_jump_out=False):
    boundary_match_in = r'''['"`\(\{\[<]'''
    boundary_match_out = r'''['"`\)\}\]>]'''
    boundary_match = boundary_match_out if is_jump_out else boundary_match_in
    old_clip_value = clip.get()
    press("cmd-shift-down")
    press_wait("cmd-c", .05)
    press_wait("left", .05)
    remaining_text = clip.get()
    clip.set(old_clip_value)
    first_boundary_match = re.search(boundary_match, remaining_text)
    if first_boundary_match is None:
        return
    # cursor over to the found key text
    for i in range(0, first_boundary_match.start()):
        press_wait("right", .001)

    press_wait("right", .001)


context.keymap(
    {

        # Navigating Interface
        "explore tab": Key("shift-cmd-e"),
        "search tab": Key("shift-cmd-f"),
        "debug tab": Key("shift-cmd-d"),
        "source control tab": Key("shift-ctrl-g"),
        "extensions tab": Key("shift-cmd-x"),
        "(toggle | show | hide) panel": Key("cmd-j"),

        # tabbing
        "next tab": Key("cmd-alt-right"),
        "last tab": Key("cmd-alt-left"),
        "new tab": Key("cmd-n"),
        "jump" + numerals: jump_tabs,
        "jump back" + numerals: lambda m: jump_tabs(m, goBackwards=True),

        # editing
        "bracken": [Key("cmd-shift-ctrl-right")],
        # various
        "comment": Key("cmd-shift-7"),
        "search all": Key("cmd-shift-f"),
        "(drop-down | drop)": Key("ctrl-space"),


        # File management
        "[open] command palette": Key("cmd-shift-p"),
        "Open [file] [<dgndictation>]": [Key("cmd-p"), text],
        "Save [file]": Key("cmd+s"),

        # Search
        "find next <dgndictation>": jump_to_next_word_instance,
        "find in files": Key('cmd-shift-f'),
        "(search | find) [file]": Key("cmd-f"),
        "(Find | Jump [to]) next <dgndictation>": jump_to_next_word_instance,
        "(Find | Jump [to]) previous <dgndictation>": jump_to_previous_word_instance,


        # Tab management
        "nexta": Key("cmd-alt-right"),
        "text tab": Key("cmd-alt-right"),
        "prexta": Key("cmd-alt-left"),
        "previous tab": Key("cmd-alt-left"),
        "Close tab": Key("cmd-w"),

        # moving around a file
        "(go | jump) to line" + optional_numerals: jump_to_line,
        "move line up" + optional_numerals: repeat_function(2, "alt-up"),
        "move line down" + optional_numerals: repeat_function(2, "alt-down"),
        "jump in": lambda m: jump_in_or_out(False),
        "jump out": lambda m: jump_in_or_out(True),

        "Go to definition": Key("f12"),
        # "Go to required definition": R(Key("c-f12:2, c-right:5, left/50, f12"), rdescript="Visual Studio Code: Go to Required Definition"),
        "Go to (top | first line)": Key("cmd-up"),
        "Go to ( bottom | last line)": Key("cmd-down"),
        "ee-ol": Key("end"),
        "beol": Key("home"),
        "[Go] back" + optional_numerals: repeat_function(0, "alt-left"),
        "[Go] forward" + optional_numerals: repeat_function(0, "alt-right"),

        # Formatting
        "indent": Key("tab"),
        "Unindent": Key("shift-tab"),
        "Comment": Key("cmd-/"),
        "Block comment": Key("shift-alt-a"),
        "format document": Key("shift-alt-f"),
        "format selection": [Key("cmd-k"), Key("cmd-f")],

        # Editing
        "select lines" + optional_numerals + "(until|through)" + optional_numerals: lambda m: select_and_modify_lines(m),
        "select line": Key("cmd-l"),
        "delete line": Key("shift-cmd-k"),
        "delete lines" + optional_numerals + "(until|through)" + optional_numerals: lambda m: select_and_modify_lines(m, 'delete'),
        "copy lines" + optional_numerals + "(until|through)" + optional_numerals: lambda m: select_and_modify_lines(m, 'cmd-c'),
        "cut lines" + optional_numerals + "(until|through)" + optional_numerals: lambda m: select_and_modify_lines(m, 'cmd-x'),

        # "expand selection [<n> [(times|time)]]": R(Key("sa-right"), rdescript="VSC: expand selection") * Repeat(extra="n"),
        # "shrink selection [<n> [(times|time)]]": R(Key("sa-left"), rdescript="VSC: shrink selection") * Repeat(extra="n"),
        "expand selection": Key("ctrl-shift-cmd-right"),
        "shrink selection": Key("ctrl-shift-cmd-left"),
        "select previous" + numerals + "words": repeat_function(2, "alt-shift-left"),
        "select next" + numerals + "words": repeat_function(2, "alt-shift-right"),

        # Clipboard
        "clone": Key("alt-shift-down"),

        # Window Management
        "[toggle] Zen mode": [Key("cmd-k"), Key("z")],

        # Debugging
        "[toggle] breakpoint": Key("f9"),
        # "step over [<n>]": R(Key("f10/50") * Repeat(extra="n"), rdescript="Visual Studio Code:Step Over"),
        "step over": Key("f10"),
        "step into": Key("f11"),
        "step out [of]": Key("shift-f11"),
        "resume": Key("f5"),
    }
)
