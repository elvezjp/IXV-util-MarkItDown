import argparse
import os
import sys
import importlib.util

try:
    from . import __version__
except ImportError:  # pragma: no cover - fallback for isolated execution
    __version__ = "0.1.0"
import zipfile
import xml.etree.ElementTree as ET


def choose_mode() -> str:
    """Prompt the user to select conversion mode."""
    while True:
        choice = input(
            "Select mode: [1] MarkItDown (full) / [2] NoMarkItDown (simple): "
        ).strip()
        if choice in {"1", "2"}:
            return choice
        print("Please enter 1 or 2.")


def run_markitdown(argv):
    """Run the upstream MarkItDown CLI."""
    upstream = os.path.join(
        os.path.dirname(__file__), "..", "upstream", "packages", "markitdown", "src"
    )
    upstream = os.path.abspath(upstream)

    # Remove this package to avoid name clashes and import upstream implementation
    sys.modules.pop("markitdown", None)
    sys.path.insert(0, upstream)

    spec = importlib.util.find_spec("markitdown.__main__")
    if spec is None or spec.loader is None:
        raise ImportError("upstream MarkItDown not found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sys.argv = [sys.argv[0]] + (argv or [])
    module.main()


def extract_text(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for p in tree.iterfind(".//w:p", ns):
        texts = [t.text for t in p.iterfind(".//w:t", ns) if t.text]
        if texts:
            paragraphs.append("".join(texts))
    return "\n\n".join(paragraphs)


def convert_file(input_path, output_path):
    text = extract_text(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def run_nomarkitdown(argv):
    """Execute the simple converter bundled with this project."""
    parser = argparse.ArgumentParser(description="Convert .docx files to Markdown.")
    parser.add_argument("files", nargs="+", help="Input .docx files")
    parser.add_argument("-o", "--output", help="Output file name (single input only)")
    parser.add_argument("-d", "--directory", help="Output directory")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    if args.output and len(args.files) > 1:
        parser.error("--output can only be used with a single input file")

    if args.directory:
        os.makedirs(args.directory, exist_ok=True)

    if args.output:
        convert_file(args.files[0], args.output)
        return

    for path in args.files:
        name = os.path.splitext(os.path.basename(path))[0] + ".md"
        if args.directory:
            out = os.path.join(args.directory, name)
        else:
            out = os.path.join(os.path.dirname(path), name)
        convert_file(path, out)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    choice = choose_mode()
    if choice == "1":
        run_markitdown(argv)
        return

    run_nomarkitdown(argv)


if __name__ == "__main__":
    main()
