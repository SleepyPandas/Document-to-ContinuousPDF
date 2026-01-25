"""
Utility functions for document processing.
"""


from urllib.parse import unquote, urlparse
from pathlib import Path
import time


_HTML_EXTENSIONS = {".html", ".htm"}
_MARKDOWN_EXTENSIONS = {".md", ".markdown"}

def timer(func):
    """
    Decorator to measure the execution time of a function.
    """

    def wrapper(*args, **kwargs):
        # 1. Start timer
        start_time = time.perf_counter()

        result = func(*args, **kwargs)
        # 2. End timer / Logging
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Compiled in: {elapsed_time:.5f} seconds")

        return result

    return wrapper


def path_from_input(input_path):
    if isinstance(input_path, Path):
        return input_path
    if isinstance(input_path, str) and input_path.startswith("file://"):
        parsed = urlparse(input_path)
        raw_path = unquote(parsed.path)
        if raw_path.startswith("/") and len(raw_path) > 2 and raw_path[2] == ":":
            raw_path = raw_path[1:]
        return Path(raw_path)
    return Path(input_path)


def detect_input_type(input_path):
    suffix = path_from_input(input_path).suffix.lower()
    if suffix in _HTML_EXTENSIONS:
        return "html"
    if suffix in _MARKDOWN_EXTENSIONS:
        return "markdown"
    raise ValueError(
        "Unsupported input type. Supported extensions: .html, .htm, .md, .markdown"
    )


def to_file_url(input_path):
    if isinstance(input_path, str) and input_path.startswith("file://"):
        return input_path

    resolved_path = Path(input_path).expanduser()
    if not resolved_path.is_absolute():
        resolved_path = (Path.cwd() / resolved_path).resolve()
    else:
        resolved_path = resolved_path.resolve()

    if not resolved_path.exists():
        raise FileNotFoundError(f"Input file not found: {resolved_path}")

    return resolved_path.as_uri()
