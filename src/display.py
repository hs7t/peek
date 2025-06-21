from rich import box
from rich.table import Table
from rich.syntax import Syntax
from utilities import getLines, stripEmptyTrailingLines, stringChunk

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

def getLanguageForFilename(filename: str):
    try:
        return get_lexer_for_filename(filename)
    except ClassNotFound:
        return "text"

def syntaxHighlight(string, filename, show_line_numbers=False):
    language = getLanguageForFilename(filename)
    highlightedStr = Syntax(string, language, background_color="default", theme="solarized-dark", line_numbers=show_line_numbers)
    return highlightedStr

def printFilePreviewTable(files, console, file_max_lines=4, show_line_numbers= False):
    table = Table(show_header=True, header_style="green", box=box.ROUNDED)
    separator = "[dim]" + "·" * 3 + "[/dim]\n"

    table.add_column("File")
    table.add_column("Preview")

    for file in files:
        filename = file["path"].name
        chunk_content = stringChunk(file["chunk"])
        file_preview = syntaxHighlight(stripEmptyTrailingLines(getLines(chunk_content, file_max_lines)), filename, show_line_numbers=show_line_numbers)

        table.add_row(filename, file_preview)
        if show_line_numbers == True:
            table.add_row("", separator)
    console.print(table)
