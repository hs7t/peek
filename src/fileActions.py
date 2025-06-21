from utilities import readChunk
from thefuzz import fuzz
from charset_normalizer import is_binary

def listTextFiles(directory, pattern="*", sorting="recency"):
    """
    Return the paths of all files in a given directory matching a 
    pattern (default "*")
    """

    results = []
    for p in directory.iterdir():
        if p.match(pattern) and p.is_file():
            results.append(p)

    if sorting == "recency":
        results = sorted(results, key=lambda p: p.stat().st_mtime, reverse=True)
    elif sorting == "size":
        results = sorted(results, key=lambda p: p.stat().st_size, reverse=True)
    elif sorting == "alphabetic":
        results = sorted(results, key=lambda p: p.name)
        
    return results

def fetchMatchingFiles(paths, query = "", precision_ratio=70, max_file_bytes=8192):
    """
    Fuzzy-match a query (str), if existent, to the filenames of each path, returning
    all paths that can pass with a given precision ratio (default 70)
    """
    results = []
    for path in paths:
        chunk = readChunk(path)

        if query != "":
            match_ratio = fuzz.ratio(query.lower(), path.name.lower())
        else:
            match_ratio = 100

        if (match_ratio >= precision_ratio) and not (is_binary(chunk)):
            results.append({
                "path": path,
                "chunk": chunk
            })
    return results
