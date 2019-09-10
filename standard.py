from talon.voice import Word, Context, Key, Str, press
from talon import app, clip, ui
from talon_init import TALON_HOME, TALON_PLUGINS, TALON_USER
import string
from .ems_utils import surround, parse_words, parse_word, sentence_text, text, word
from talon.engine import engine


# def engine_update(j):
#     engine.cmd("g.update", name="dragon", enabled=False)


# engine.register("ready", engine_update)


def rot13(i, word, _):
    out = ""
    for c in word.lower():
        if c in string.ascii_lowercase:
            c = chr((((ord(c) - ord("a")) + 13) % 26) + ord("a"))
        out += c
    return out


formatters = {
    "dunder": (True, lambda i, word, _: "__%s__" % word if i == 0 else word),
    "camel": (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    "snake": (True, lambda i, word, _: word.lower() if i == 0 else "_" + word.lower()),
    "smash": (True, lambda i, word, _: word),
    "kebab": (True, lambda i, word, _: word if i == 0 else "-" + word),
    "pack": (True, lambda i, word, _: word if i == 0 else "::" + word),
    "title": (False, lambda i, word, _: word.capitalize()),
    "allcaps": (False, lambda i, word, _: word.upper()),
    "dubstring": (False, surround('"')),
    "string": (False, surround("'")),
    "padded": (False, surround(" ")),
    "rot-thirteen": (False, rot13),
}


def FormatText(m):
    fmt = []
    if m._words[-1] == "over":
        m._words = m._words[:-1]
    for w in m._words:
        if isinstance(w, Word):
            fmt.append(w.word)
    try:
        words = parse_words(m)
    except AttributeError:
        with clip.capture() as s:
            press("cmd-c")
        words = s.get().split(" ")
        if not words:
            return

    tmp = []
    spaces = True
    for i, w in enumerate(words):
        w = parse_word(w)
        for name in reversed(fmt):
            smash, func = formatters[name]
            w = func(i, w, i == len(words) - 1)
            spaces = spaces and not smash
        tmp.append(w)
    words = tmp

    sep = " "
    if not spaces:
        sep = ""
    Str(sep.join(words))(None)


def copy_bundle(m):
    bundle = ui.active_app().bundle
    clip.set(bundle)
    app.notify("Copied app bundle", body="{}".format(bundle))


ctx = Context("standard")

ctx.vocab = [
    "docker",
    "talon",
    "pragma",
    "pragmas",
    "vim",
    "configs",
    "spotify",
    "upsert",
    "utils",
]

keymap = {}
keymap.update(
    {
        "phrase <dgndictation> [over]": text,
        "(say | speak) <dgndictation>++ [over]": text,
        "sentence <dgndictation> [over]": sentence_text,
        "comma <dgndictation> [over]": [", ", text],
        "period <dgndictation> [over]": [". ", sentence_text],
        "more <dgndictation> [over]": [" ", text],
        "word <dgnwords>": word,
        "(%s)+ <dgndictation> [over]" % (" | ".join(formatters)): FormatText,
        "dragon words": "<dgnwords>",
        "slap": Key("enter"),
        "cd": "cd ",
        "talon logs": "cd {} && tail -f talon.log\n".format(TALON_HOME),
        "grep": "grep ",
        "elle less": "ls ",
        "(ssh | sh)": "ssh ",
        "diff": "diff ",
        "dot pie": ".py",
        "run make (durr | dear)": "mkdir ",
        "(jay son | jason )": "json",
        "(http | htp)": "http",
        "md5": "md5",
        "word queue": "queue",
        "word eye": "eye",
        "next window": Key("cmd-`"),
        "previous window": Key("cmd-shift-`"),
        # 'next app': Key('cmd-tab'),
        # 'last app': Key('cmd-shift-tab'),
        "next tab": Key("ctrl-tab"),
        "new tab": Key("cmd-t"),
        "last tab": Key("ctrl-shift-tab"),
        "next space": Key("cmd-alt-ctrl-right"),
        "last space": Key("cmd-alt-ctrl-left"),
        "zoom [in]": Key("cmd-+"),
        "zoom out": Key("cmd--"),
        "(page | scroll) up": Key("pgup"),
        "(page | scroll) [down]": Key("pgdown"),
        "copy": Key("cmd-c"),
        "cut": Key("cmd-x"),
        "paste": Key("cmd-v"),
        "flock off": Key("escape"),
        "menu help": Key("cmd-shift-?"),
        "spotlight": Key("cmd-space"),
        "(undo | under | skunks)": Key("cmd-z"),
        "redo": Key("cmd-shift-z"),
        "(crap | clear | scratch )": Key("cmd-backspace"),
        "more bright": Key("brightness_up"),
        "less bright": Key("brightness_down"),
        "volume up": Key("volume_up"),
        "volume down": Key("volume_down"),
        "mute": Key("mute"),
        "play next": Key("next"),
        "play previous": Key("previous"),
        "(play | pause)": Key("space"),  # spotify
        "copy active bundle": copy_bundle,
        "wipe": Key("backspace"),
        "(pad | padding ) ": ["  ", Key("left")],
        "funny": "ha ha",
    }
)

ctx.keymap(keymap)
