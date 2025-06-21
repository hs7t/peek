import typer
from pathlib import Path
from rich.console import Console

import config
from errorHandling import closeWithError
from fileActions import fetchMatchingFiles, listTextFiles
from display import printFilePreviewTable


console = Console()
app = typer.Typer()
debugMode = False

@app.command()
def peek(
        query: str = typer.Option("", help="A file name to look for."), 
        directory: str = typer.Option(".", "-d", "--directory", help="A directory to look for files in."), 
        sorting: str = typer.Option("recency", "-s", "--sorting", help="A property by which to sort files: 'recency'/'size'/'alphabetic'."),
        pattern: str = typer.Option("*", "-p", "--pattern", help="A glob-style pattern to filter files by."),
        verbose: bool = typer.Option(False, "-v", "--verbose", help="Print more lines per file."),
        line_numbers: bool = typer.Option(False, "-l", "--linenumbers", help="Display line numbers in preview."),
        debug_flag: bool = typer.Option(False, "-db", "--debug", help="Enable debugging mode.")
    ):
    config.debugMode = debug_flag

    workingDir = Path(directory).resolve()
    if not workingDir.exists():
        closeWithError(f"It seems the directory '{dir}' does not exist.", 1)
        return
    if not workingDir.is_dir():
        closeWithError(f"The path '{dir}' is not a directory.")
        return
    
    try:
        filesInDir = listTextFiles(workingDir, pattern=pattern, sorting=sorting)
        matchingFiles = fetchMatchingFiles(filesInDir, query=query)
    except Exception as e:
        closeWithError()
        return
    if verbose == True:
        printFilePreviewTable(matchingFiles, console, file_max_lines=50, show_line_numbers=line_numbers)
    else:
        printFilePreviewTable(matchingFiles, console, show_line_numbers=line_numbers)

if __name__ == "__main__":
    app()
