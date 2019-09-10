from talon.voice import Context, Key

# Available in all contexts
ctx = Context("Magnet")

ctx.keymap(
    {
        # Full-screen
        "snap (max | Max)": Key("ctrl-alt-m"),
        "snap restore": Key("ctrl-alt-r"),
        "snap center": Key("ctrl-alt-c"),
        # Screen halves
        "snap top half": Key("ctrl-alt-up"),
        "snap right half": Key("ctrl-alt-right"),
        "snap bottom half": Key("ctrl-alt-down"),
        "snap left half": Key("ctrl-alt-left"),
        # Screen thirds
        "snap left third": Key("ctrl-alt-d"),
        "snap center third": Key("ctrl-alt-f"),
        "snap right third": Key("ctrl-alt-g"),
        "snap right two (thirds | third)": Key("ctrl-alt-t"),
        "snap left two (thirds | third)": Key("ctrl-alt-e"),
        # Quarters are implicit

        "snap top left [quarter]": Key("ctrl-alt-u"),
        "snap top right [quarter]": Key("ctrl-alt-i"),
        "snap bottom left [quarter]": Key("ctrl-alt-j"),
        "snap bottom right [quarter]": Key("ctrl-alt-k"),
    }
)
