from talon.voice import Context, Key, press
from ..misc.utils import (parse_words_as_integer, insert,
                          is_filetype, CursorText, numerals, sentence_text, text)

MARKDOWN_EXTENSIONS = (".md", "README")

context = Context("markdown", func=is_filetype(MARKDOWN_EXTENSIONS))


def handle_headings(m):
    heading_depth = parse_words_as_integer(m._words[1:2])
    if heading_depth is None:
        return
    insert('#' * heading_depth + ' ')
    if(len(m._words) > 2):
        sentence_text(m)


def handle_ordered_list(m):
    list_number = parse_words_as_integer(m._words[2:])
    if list_number is None:
        return
    insert("{}. ".format(list_number))


def handle_code_block(m):
    press("enter")
    press("enter")
    insert("```")
    press('up')
    insert("```")
    if m.dgndictation[0] and len(m.dgndictation[0]._words) > 0:
        text(m)


context.keymap({
    "heading" + numerals + "[<dgndictation>]": handle_headings,
    "italics": CursorText("_{.}_ "),
    "bold": CursorText("**{.}** "),
    "strikethrough": CursorText("~{.}~ "),
    "metallic": CursorText("**_{.}_** "),
    "pre": CursorText("`{.}` "),
    "code block [<dgndictation>]": handle_code_block,
    "block (quotes | quote)": "> ",
    "checkbox": "- [ ]",
    "list": "- ",
    "ordered list" + numerals: handle_ordered_list,
    "horizontal rule": [Key("enter"), "_________________", Key("enter")],
    "link": CursorText("[{.}]()"),
    "image": CursorText("![{.}]()"),
    "character escape": Key("\\")
})
