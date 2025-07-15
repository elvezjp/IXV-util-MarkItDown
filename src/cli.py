import argparse
import os
import sys

try:
    from . import __version__
except ImportError:  # pragma: no cover - fallback for isolated execution
    __version__ = "0.1.0"
from markitdown import MarkItDown


def parse_args(argv):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Convert files to Markdown.")
    parser.add_argument("files", nargs="+", help="Input files")
    parser.add_argument("-o", "--output", help="Output file name (single input only)")
    parser.add_argument("-d", "--directory", help="Output directory")
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


def process_files(args):
    """Process files using MarkItDown."""
    if args.directory:
        os.makedirs(args.directory, exist_ok=True)

    for input_path in args.files:
        try:
            content = run_markitdown(input_path)
            output_path = get_output_path(input_path, args)
            write_output(content, output_path)
            print(f"Converted: {input_path} -> {output_path}")
        except Exception as e:
            print(f"Error converting {input_path}: {e}")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)
    process_files(args)


if __name__ == "__main__":
    main()
