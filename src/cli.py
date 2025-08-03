import argparse
import os
import sys

try:
    from . import __version__
except ImportError:  # pragma: no cover - fallback for isolated execution
    __version__ = "0.1.0"
import zipfile
import xml.etree.ElementTree as ET
from markitdown import MarkItDown


def choose_mode() -> str:
    """Prompt the user to select conversion mode."""
    while True:
        choice = input(
            "Select mode: [1] MarkItDown (full) / [2] NoMarkItDown (simple): "
        ).strip()
        if choice in {"1", "2"}:
            return choice
        print("Please enter 1 or 2.")


def parse_args(argv):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Convert files to Markdown.")
    parser.add_argument("files", nargs="+", help="Input files")
    parser.add_argument("-o", "--output", help="Output file name (single input only)")
    parser.add_argument("-d", "--directory", help="Output directory")
    parser.add_argument(
        "--mode",
        choices=["markitdown", "nomarkitdown"],
        help="Conversion mode (skip prompt)",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    if args.output and len(args.files) > 1:
        parser.error("--output can only be used with a single input file")

    return args


def get_output_path(input_path, args):
    """Get output path based on arguments."""
    if args.output:
        return args.output
    
    name = os.path.splitext(os.path.basename(input_path))[0] + ".md"
    if args.directory:
        return os.path.join(args.directory, name)
    else:
        return os.path.join(os.path.dirname(input_path), name)


def write_output(content, output_path):
    """Write content to output file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def run_markitdown(input_path):
    """Convert file using MarkItDown."""
    md = MarkItDown()
    result = md.convert(str(input_path))
    return result.text_content


def run_nomarkitdown(input_path):
    """Extract text from docx file (NoMarkItDown mode)."""
    # Check if file is a docx file
    if not input_path.lower().endswith('.docx'):
        raise ValueError(f"Warning: NoMarkItDown mode only supports .docx files. Skipping: {input_path}")
    
    with zipfile.ZipFile(input_path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for p in tree.iterfind(".//w:p", ns):
        texts = [t.text for t in p.iterfind(".//w:t", ns) if t.text]
        if texts:
            paragraphs.append("".join(texts))
    return "\n\n".join(paragraphs)


def process_files(args, converter_func):
    """Process files using the specified converter function."""
    if args.directory:
        os.makedirs(args.directory, exist_ok=True)

    for input_path in args.files:
        try:
            content = converter_func(input_path)
            output_path = get_output_path(input_path, args)
            write_output(content, output_path)
            print(f"Converted: {input_path} -> {output_path}")
        except Exception as e:
            print(f"Error converting {input_path}: {e}")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    mode = args.mode

    if mode is None:
        choice = choose_mode()
        mode = "markitdown" if choice == "1" else "nomarkitdown"

    if mode == "markitdown":
        process_files(args, run_markitdown)
    else:
        process_files(args, run_nomarkitdown)


if __name__ == "__main__":
    main()
