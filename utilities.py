from charset_normalizer import from_bytes
    
def stripEmptyTrailingLines(string):
    lines = str.splitlines(string, keepends=True)
    while lines and lines[-1].strip() == "":
        lines.pop()
    return "".join(lines)


def getLines(string: str, max_lines: int):
    lines = string.splitlines(keepends=True)
    i = 0
    result = ""
    while i < max_lines:
        try:
            result += lines[i]
        except IndexError:
            break
        i += 1
    return result

def readChunk(path, max_bytes: int=8192):
    try:
        with path.open('rb') as file:
            return file.read(max_bytes)
    except Exception:
        return b''

def stringChunk(chunk):
    return str(from_bytes(chunk).best())