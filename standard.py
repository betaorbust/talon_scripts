from talon.voice import Word, Context, Key, Str, press
from talon import app, clip, ui
# from talon_init import TALON_HOME, TALON_PLUGINS, TALON_USER
# import string
# from .ems_utils import surround, parse_words, parse_word, sentence_text, text, word
from .misc.utils import surround, parse_words, parse_word, text, word
# from talon.engine import engine


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
    "configs",
    "spotify",
    "utils",
]

ctx.keymap(
    {
        "more <dgndictation> [over]": [" ", text],
        "dragon words": "<dgnwords>",
        "slap": Key("enter"),
        "clap": Key("escape"),
        # "cd": "cd ",
        # "talon logs": " tail -f ~/.talon/talon.log",
        #         "grep": "grep ",
        #         "elle less": "ls ",
        #         "(ssh | sh)": "ssh ",
        #         "diff": "diff ",
        #         "dot pie": ".py",
        #         "run make (durr | dear)": "mkdir ",
        #         "(jay son | jason )": "json",
        #         "(http | htp)": "http",
        #         "md5": "md5",
        #         "word queue": "queue",
        #         "word eye": "eye",
        #         # 'next app': Key('cmd-tab'),
        #         # 'last app': Key('cmd-shift-tab'),
        #         "next tab": Key("ctrl-tab"),
        #         "new tab": Key("cmd-t"),
        #         "last tab": Key("ctrl-shift-tab"),
        #         "next space": Key("cmd-alt-ctrl-right"),
        #         "last space": Key("cmd-alt-ctrl-left"),
        "(page | scroll) up": Key("pgup"),
        "(page | scroll) [down]": Key("pgdown"),
        "copy": Key("cmd-c"),
        "cut": Key("cmd-x"),
        "paste": Key("cmd-v"),
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
        "copy active bundle": copy_bundle,
        "wipe": Key("backspace"),
    }
)
