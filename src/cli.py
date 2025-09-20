import argparse
import os
import sys
import warnings
import signal
from datetime import datetime
from pathlib import Path
import time

try:
    from . import __version__
except ImportError:  # pragma: no cover - fallback for isolated execution
    __version__ = "0.1.0"
import zipfile
import xml.etree.ElementTree as ET

# Suppress pydub warning since we don't use audio/video features (#41, PR#44)
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv", category=RuntimeWarning)
    from markitdown import MarkItDown
try:
    from ixv_util_common.ascii_logo.ascii_logo import display_project_logo
except ImportError as exc:
    raise ImportError(
        "ixv-util-common がインストールされていません。依存関係をインストールしてください。"
    ) from exc

try:
    from .image_extractor import extract_and_save_images, count_base64_images
except ImportError:
    from image_extractor import extract_and_save_images, count_base64_images


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
    parser.add_argument("-v", "--version", action="version", version=__version__)

    # Mode selection option
    parser.add_argument(
        "--mode",
        choices=["markitdown", "nomarkitdown"],
        help="Select mode non-interactively (markitdown or nomarkitdown)",
    )
    
    # Image handling options
    parser.add_argument(
        "--no-save-images", 
        action="store_true", 
        help="Keep images as base64 data URIs in markdown (default: save as separate files)"
    )
    
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


def run_markitdown(input_path, save_images=True, output_path=None):
    """Convert file using MarkItDown with configurable image handling."""
    md = MarkItDown()
    
    if save_images:
        # Convert with base64 images first, then extract and save them
        result = md.convert(str(input_path), keep_data_uris=True)
        content = result.text_content
        
        if output_path and count_base64_images(content) > 0:
            content = extract_and_save_images(content, output_path)
            print(f"Extracted and saved {count_base64_images(result.text_content)} images to images/")
        
        return content
    else:
        # Keep base64 images embedded
        result = md.convert(str(input_path), keep_data_uris=True)
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


def process_files(args, converter_func, log_file=None):
    """Process files using the specified converter function."""
    if args.directory:
        os.makedirs(args.directory, exist_ok=True)

    def _append_log(text: str) -> None:
        if log_file and log_file.exists():
            with log_file.open("a", encoding="utf-8") as f:
                f.write(text + "\n")

    save_images = not args.no_save_images
    total_files = len(args.files)
    processed_files = 0
    error_files = 0
    processing_start_time = datetime.now()

    # Log processing start
    mode = "markitdown" if converter_func == run_markitdown else "nomarkitdown"
    _append_log(f"markitdown_start: {processing_start_time.isoformat()}, files: {total_files}, mode: {mode}")
    print(f"Processing {total_files} files using {mode} mode...")

    for input_path in args.files:
        file_start_time = time.perf_counter()
        try:
            output_path = get_output_path(input_path, args)

            if converter_func == run_markitdown:
                content = converter_func(input_path, save_images=save_images, output_path=output_path)
            else:
                content = converter_func(input_path)

            write_output(content, output_path)
            file_duration = time.perf_counter() - file_start_time
            processed_files += 1

            _append_log(f"file_result: file={input_path}, status=success, duration={file_duration:.3f}s")
            print(f"Converted: {input_path} -> {output_path} ({file_duration:.3f}s)")
        except Exception as e:
            file_duration = time.perf_counter() - file_start_time
            error_files += 1

            _append_log(f"file_result: file={input_path}, status=error, duration={file_duration:.3f}s, error=\"{str(e)}\"")
            print(f"Error converting {input_path}: {e} ({file_duration:.3f}s)")

    processing_duration = (datetime.now() - processing_start_time).total_seconds()
    print(f"\nProcessing completed: {processed_files} successful, {error_files} errors")
    print(f"Processing time: {processing_duration:.2f}s")

    return processing_duration


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # Initialize timing and logging
    start_time = datetime.now()
    processing_start_time = None
    log_file = Path.cwd() / "execution.log"
    exit_logged = False

    def _append_log(text: str) -> None:
        with log_file.open("a", encoding="utf-8") as f:
            f.write(text + "\n")

    # Initialize log file if it doesn't exist
    if not log_file.exists():
        with log_file.open("w", encoding="utf-8") as f:
            f.write("# IXV-util-MarkItDown 実行ログ\n")
            f.write("# このファイルはIXV-util-MarkItDown実行時の各種タイミング情報を記録します。\n")
            f.write("# \n")
            f.write("# ログフォーマット:\n")
            f.write("#   start: プログラム開始時刻\n")
            f.write("#   markitdown_start: 処理開始時刻, files: 対象ファイル数, mode: 変換モード\n")
            f.write("#   file_result: file=ファイル名, status=成功/失敗, duration=処理時間(秒)\n")
            f.write("#   end: プログラム終了時刻, total_duration: 全体実行時間(秒), processing_duration: 処理時間(秒)\n")
            f.write("#" + "=" * 70 + "\n\n")

    # Display ASCII logo
    display_project_logo(display_name="IXV-util-MarkItDown")

    _append_log(f"start: {start_time.isoformat()}")
    print(f"IXV-util-MarkItDown started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def _exit_handler() -> None:
        nonlocal exit_logged
        if exit_logged:
            return
        exit_logged = True

        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()

        if processing_start_time is not None:
            processing_duration = (end_time - processing_start_time).total_seconds()
            _append_log(
                f"end: {end_time.isoformat()}, total_duration: {total_duration:.2f}s, processing_duration: {processing_duration:.2f}s"
            )
            print(
                f"Total execution time: {total_duration:.2f}s (processing: {processing_duration:.2f}s)"
            )
        else:
            _append_log(f"end: {end_time.isoformat()}, total_duration: {total_duration:.2f}s")
            print(f"Total execution time: {total_duration:.2f}s")

    def _handle_signal(signum, frame):
        _exit_handler()
        sys.exit(1)

    # Register signal handlers for graceful shutdown
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _handle_signal)
        except ValueError:
            pass

    try:
        args = parse_args(argv)

        if args.mode:
            mode = args.mode
        else:
            choice = choose_mode()
            mode = "markitdown" if choice == "1" else "nomarkitdown"

        processing_start_time = datetime.now()

        if mode == "markitdown":
            process_duration = process_files(args, run_markitdown, log_file)
        else:
            process_duration = process_files(args, run_nomarkitdown, log_file)

        # Normal exit
        sys.exit(0)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        _exit_handler()


if __name__ == "__main__":
    main()
