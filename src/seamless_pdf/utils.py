"""
Utility functions for document processing.
"""


from urllib.parse import unquote, urlparse
from pathlib import Path
import time

# THIS IS USED FOR MD HTML STYLING

css_style = """
<style>
    body {
        box-sizing: border-box;
        min-width: 200px;
        max-width: 980px;
        margin: 0 auto;
        padding: 45px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
        font-size: 16px;
        line-height: 1.5;
        color: #24292e;
    }
    
    h1, h2, h3 { margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25; }
    h1, h2 { padding-bottom: 0.3em; border-bottom: 1px solid #eaecef; }
    h1 { font-size: 2em; }
    h2 { font-size: 1.5em; }
    h3 { font-size: 1.25em; }

    /* Code Blocks */
    pre { background-color: #f6f8fa; border-radius: 6px; padding: 16px; overflow: auto; }
    code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 85%; background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; }
    pre > code { background-color: transparent; padding: 0; }

    /* Blockquotes */
    blockquote { padding: 0 1em; color: #6a737d; border-left: 0.25em solid #dfe2e5; margin: 0; }
    
    /* Links */
    a { color: #0366d6; text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* Tables (GitHub style) */
    table { border-spacing: 0; border-collapse: collapse; display: block; width: max-content; max-width: 100%; overflow: auto; }
    tr { border-top: 1px solid #c6cbd1; background-color: #fff; }
    tr:nth-child(2n) { background-color: #f6f8fa; }
    th, td { padding: 6px 13px; border: 1px solid #dfe2e5; }
    th { font-weight: 600; }
</style>
"""


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
