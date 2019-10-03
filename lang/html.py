from talon.voice import Context, Key, press
import talon.clip as clip
from ..misc.utils import (
    text,
    parse_words,
    # parse_words_as_integer,
    insert,
    # word,
    # join_words,
    is_filetype,
)

FILETYPES = (".html", ".jsx", ".erb")

context = Context("html", func=is_filetype(FILETYPES))


def remove_spaces_around_dashes(m):
    words = parse_words(m)
    s = " ".join(words)
    s = s.replace(" – ", "-")
    insert(s)


def CursorText(s):
    left, right = s.split("{.}", 1)
    return [left + right, Key(" ".join(["left"] * len(right)))]


# Adapted from select_text_to_right_of_cursor in generic_editor.py by jcooper-korg from talon slack. Will figure out a more elegant solution later.
def skip_tag_right(m):
    key = ">"
    old = clip.get()
    press("shift-end", wait=2000)
    press("cmd-c", wait=2000)
    press("left", wait=2000)
    text_right = clip.get()
    clip.set(old)
    result = text_right.find(key)
    if result == -1:
        return
    # cursor over to the found key text
    for i in range(0, result):
        press("right", wait=0)
    # now select the matching key text
    for i in range(0, len(key)):
        press("shift-right")
    press("right", wait=0)


# Adapted from select_text_to_left_of_cursor in generic_editor.py by jcooper-korg from talon slack. Will figure out a more elegant solution later.
def skip_tag_left(m):
    old = clip.get()
    key = "<"
    press("shift-home", wait=2000)
    press("cmd-c", wait=2000)
    press("right", wait=2000)
    text_left = clip.get()
    clip.set(old)
    result = text_left.rfind(key)
    if result == -1:
        return
    # cursor over to the found key text
    for i in range(0, len(text_left) - result):
        press("left", wait=0)
    # now select the matching key text
    for i in range(0, len(key)):
        press("shift-right")
    press("left", wait=0)


context.keymap(
    {
        # Elements: Use "tag" or "ellie" as the main trigger word
        # Use this for any missing elements unti they're added
        "tag custom <dgndictation>": [
            "<",
            text,
            "></",
            text,
            ">",
            Key("alt-left alt-left left left"),
        ],
        "tag html": CursorText("<html>{.}</html>"),
        "tag title": CursorText("<title>{.}</title>"),
        "tag head": CursorText("<head>{.}</head>"),
        "tag body": CursorText("<body>{.}</body>"),
        "tag header": CursorText("<header>{.}</header>"),
        "tag open header": "<header>",
        "tag close header": "</header>",
        "tag main": CursorText("<main>{.}</main>"),
        "tag open main": "<main>",
        "tag close main": "</main>",
        "tag article": CursorText("<article>{.}</article>"),
        "tag open article": "<article>",
        "tag close article": "</article>",
        "tag footer": CursorText("<footer>{.}</footer>"),
        "tag open footer": "<footer>",
        "tag close footer": "</footer>",
        "tag div": CursorText("<div>{.}</div>"),
        "tag open div": "<div>",
        "tag close div": "</div>",
        "tag span": CursorText("<span>{.}</span>"),
        "tag open span": "<span>",
        "tag close span": "</span>",
        "tag table": CursorText("<table>{.}</table>"),
        "tag table head": CursorText("<thead>{.}</thead>"),
        "tag table body": CursorText("<tbody>{.}</tbody>"),
        "tag table row": CursorText("<tr>{.}</tr>"),
        "tag table cell": CursorText("<td>{.}</td>"),
        #  parse_words_as_integer doesn't seem to work so we'll do it the bad way for now
        # 'tag heading <dgndictation>': ['<h', parse_words_as_integer, '></h', parse_words_as_integer, '>'],
        "tag heading one": CursorText("<h1>{.}</h1>"),
        "tag heading two": CursorText("<h2>{.}</h2>"),
        "tag heading three": CursorText("<h3>{.}</h3>"),
        "tag heading four": CursorText("<h4>{.}</h4>"),
        "tag heading five": CursorText("<h5>{.}</h5>"),
        "tag heading six": CursorText("<h6>{.}</h6>"),
        "(tag paragraph | tag pee)": CursorText("<p>{.}</p>"),
        "(tag yule | tag un-list | tag un-ordered list)": CursorText("<ul>{.}</ul>"),
        "(tag open un-ordered list | tag open un-list)": "<ul>",
        "(tag close un-ordered list | tag close un-list)": "</ul>",
        "(tag list item | tag lie)": CursorText("<li>{.}</li>"),
        "(tag open list item | tag open lie)": "<li>",
        "(tag close list item | tag close lie)": "</li>",
        "tag link": CursorText('<a href="" alt="">{.}</a>'),
        "tag open link": CursorText('<a href="{.}" alt="">'),
        "tag close link": CursorText("{.}</a>"),
        "tag image": CursorText('<img src="{.}" alt="" title="" />'),
        "tag her": "<hr>",
        "tag burr": "<br>",
        # Attributes - example: "tag div addy class box" will output "<div class="box"></div>
        "addy class <dgndictation>": [
            Key("left"),
            ' class=""',
            Key("left"),
            remove_spaces_around_dashes,
            Key("right right"),
        ],
        "addy ID <dgndictation>": [
            Key("left"),
            ' id=""',
            Key("left"),
            remove_spaces_around_dashes,
            Key("right right"),
        ],
        # Moving Around between tags
        "skip tag right": skip_tag_right,
        "skip tag left": skip_tag_left,
    }
)
