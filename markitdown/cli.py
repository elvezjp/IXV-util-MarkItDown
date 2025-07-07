import argparse
import os
from . import __version__
import zipfile
import xml.etree.ElementTree as ET

def extract_text(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = []
    for p in tree.iterfind('.//w:p', ns):
        texts = [t.text for t in p.iterfind('.//w:t', ns) if t.text]
        if texts:
            paragraphs.append(''.join(texts))
    return '\n\n'.join(paragraphs)

def convert_file(input_path, output_path):
    text = extract_text(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def main(argv=None):
    parser = argparse.ArgumentParser(description='Convert .docx files to Markdown.')
    parser.add_argument('files', nargs='+', help='Input .docx files')
    parser.add_argument('-o', '--output', help='Output file name (single input only)')
    parser.add_argument('-d', '--directory', help='Output directory')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    args = parser.parse_args(argv)

    if args.output and len(args.files) > 1:
        parser.error('--output can only be used with a single input file')

    if args.directory:
        os.makedirs(args.directory, exist_ok=True)

    if args.output:
        convert_file(args.files[0], args.output)
        return

    for path in args.files:
        name = os.path.splitext(os.path.basename(path))[0] + '.md'
        if args.directory:
            out = os.path.join(args.directory, name)
        else:
            out = os.path.join(os.path.dirname(path), name)
        convert_file(path, out)

if __name__ == '__main__':
    main()
