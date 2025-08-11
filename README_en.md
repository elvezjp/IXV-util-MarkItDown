# IXV-util-MarkItDown
[日本語版README](./README.md) is available.

<img width="1745" height="684" alt="ixv-util" src="https://github.com/user-attachments/assets/b4cca023-74f7-4068-897f-4558690fdbdd" />


IXV-util-MarkItDown is a cross-platform CLI utility that bundles Microsoft MarkItDown-based Markdown conversion tools as standalone executables (`.exe`) for Windows and macOS applications (`.app`). In MarkItDown mode, it can convert not only `.docx` but also other file formats supported by the MarkItDown library, such as PDF, to Markdown.

---

# About IXV and IXV-util Series

## What is IXV?
IXV is a next-generation AI development support platform developed by Elves Inc. It aims to support the entire software development process from requirements definition to design, implementation, testing, and operation by leveraging AI technology.

## What is the IXV-util Series?
The IXV-util series is a collection of lightweight utility tools born from the IXV development process, designed to support daily development tasks.
These tools can be used not only as part of the IXV platform but also independently, with the goal of improving developers' daily work efficiency.
IXV-util-MarkItDown is also provided as open source and is continuously improved through collaboration with the developer community.

---

# Why We Focus on Markdown
We have created many documents in Japanese development environments over the years. Various tools from different eras, such as Word and Excel, were extremely difficult to structurally analyze, reuse, or process programmatically. While they appeared well-organized on the surface, their structure was ambiguous from a computer's perspective, creating significant barriers to automated processing and AI utilization.

Markdown is very close to plain text, requiring minimal markup or formatting while still providing a means to express important document structure. Many of the major large language models (LLMs) currently available have the native ability to "speak" Markdown, and often return responses in Markdown even without being instructed to do so.

When focusing on human-AI interaction, we believe that Markdown format text is the file format that deserves attention.

---

## Features

- **High-quality conversion**: Uses the core functions of Microsoft MarkItDown to properly convert images, tables, lists, formulas, etc. into Markdown
- **Cross-platform**: Runs natively on Windows (`.exe`) / macOS (`.app`)
- **Simple CLI**: No GUI, easy to incorporate into scripts or CI/CD
- **Batch processing**: Supports converting multiple files at once
- **Open source**: Customizable freely under the MIT license

---

## Operating Modes

This tool has two operating modes:

1. **MarkItDown Mode**: Uses the complete functionality of Microsoft MarkItDown
   - Supports advanced conversion of images, tables, lists, formulas, and more
   - Does not perform extension checking, and processes file formats supported by the MarkItDown library such as PDF and PPTX

2. **NoMarkItDown Mode**: Simple proprietary implementation
   - Basic text extraction only from `.docx` files (other extensions will error)
   - Lightweight and fast operation

You can select which mode to use when starting the program.

## Supported File Formats

MarkItDown mode can convert the following file formats to Markdown:

- Word: `.docx`
- PDF: `.pdf`
- PowerPoint: `.pptx`
- Excel: `.xlsx`, `.xls`
- CSV: `.csv`
- Plain text/Markdown/JSON: `.txt`, `.text`, `.md`, `.markdown`, `.json`, `.jsonl`
- Images: `.jpg`, `.jpeg`, `.png`
- Audio/Video: `.wav`, `.mp3`, `.m4a`, `.mp4`
- Jupyter Notebook: `.ipynb`
- E-books: `.epub`
- Outlook emails: `.msg`
- Archives: `.zip`
- HTML pages and websites (YouTube, Wikipedia, Bing search results, etc.)
- RSS/Atom/Generic XML: `.rss`, `.atom`, `.xml`

NoMarkItDown mode only supports `.docx` files.

---

## Download

Download the latest executable file for your environment from [Releases](https://github.com/elvezjp/IXV-util-MarkItDown/releases).

- **Windows (x86)**: `IXV-util-MarkItDown-windows-x86.exe`
- **macOS (x86)**: `IXV-util-MarkItDown-macos-x86`
- **macOS (ARM64)**: `IXV-util-MarkItDown-macos-arm64`

---

## Usage

**MarkItDown mode** and **NoMarkItDown mode** selection prompts will be displayed.

*In MarkItDown mode, you can also specify files other than `.docx` such as `input.pdf`.*

### Windows

```bash
# Convert a single file
IXV-util-MarkItDown.exe input.docx

# Batch convert multiple files
IXV-util-MarkItDown.exe *.docx

# Specify output directory
IXV-util-MarkItDown.exe inputs/*.docx -d outputs

# List conversion options
IXV-util-MarkItDown.exe --help
```

### macOS

```bash
# Grant execute permissions (first time only)
chmod +x IXV-util-MarkItDown

# macOS may display security dialogs on first run.
# Grant permission through "System Settings" → "Privacy & Security".
# Select "Open" when running again.

# Convert a single file
./IXV-util-MarkItDown input.docx

# Batch convert multiple files
./IXV-util-MarkItDown *.docx

# Specify output directory
./IXV-util-MarkItDown inputs/*.docx -d outputs

# List conversion options
./IXV-util-MarkItDown --help
```

#### Important Notes

macOS may display **security dialogs on first run**.

1. If you see a dialog saying '"IXV-util-MarkItDown" cannot be opened because the developer cannot be verified':
   - Open "System Settings" → "Privacy & Security"
   - In the Security section, find '"IXV-util-MarkItDown" was blocked from use because it is not from an identified developer' and click "Allow Anyway"
   - Enter your password to confirm

2. If you see a "cannot verify the developer" dialog when running again:
   - Click "Open"

<img height="300" alt="20250811プライバシーとセキュリティ設定" src="https://github.com/user-attachments/assets/82488961-3294-4cd2-a669-385d2a0434c1" />
<img height="300" alt="20250811アプリ実行許可" src="https://github.com/user-attachments/assets/fe23d278-4a18-4df5-8bd6-3bb5ee3a2098" />

### Non-interactive Mode

Use the `--mode` option to skip the mode selection prompt.

```bash
# Run in MarkItDown mode
IXV-util-MarkItDown input.docx --mode markitdown

# Run in NoMarkItDown mode
IXV-util-MarkItDown input.docx --mode nomarkitdown
```

### Command Options

- `--mode` : Specify operation mode non-interactively (`markitdown` or `nomarkitdown`)
- `-o, --output` : Specify the output file name
- `-d, --directory` : Specify the output directory (creates it if it doesn't exist)
- `--no-save-images` : Embed images as base64 data URIs in markdown (default: save as separate files)
- `-v, --version` : Display version
- `-h, --help`    : Show help

### Image Handling

In **MarkItDown mode**, images contained in documents can be processed in two ways:

#### 1. Image File Saving Mode (Default)
```bash
# Save images as separate files (recommended)
IXV-util-MarkItDown document.docx -o output.md
```

- Images are saved to an `images/` directory
- Files are named: `{filename}_image1.png`, `{filename}_image2.jpg`, etc.
- Referenced from markdown with relative paths: `![alt text](images/output_image1.png)`
- **Benefits**: Smaller markdown file size and improved readability

#### 2. Base64 Embedding Mode
```bash
# Embed images as base64 data in markdown
IXV-util-MarkItDown document.docx -o output.md --no-save-images
```

- Image data is directly embedded in markdown as base64 format
- Self-contained single file makes sharing easier
- **Note**: Results in larger file sizes and difficult text editor handling

#### Image Management for Multiple Files
```bash
# Batch convert multiple files
IXV-util-MarkItDown *.docx -d outputs
```

Each file gets a filename prefix to prevent filename conflicts:
```
outputs/
├── document1.md
├── document2.md
└── images/
    ├── document1_image1.png
    ├── document1_image2.jpg
    └── document2_image1.png
```

---

## Development / Build

### Prerequisites

- Python 3.10 or later
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- git

### Clone the repository

```bash
git clone https://github.com/elvezjp/IXV-util-MarkItDown.git
cd IXV-util-MarkItDown

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up Python environment and install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Build `.exe` for Windows

```bash
# PyInstaller is included in dev-dependencies
uv sync

# Build
pyinstaller --onefile wrapper.py --name IXV-util-MarkItDown.exe
```

- Output: `dist/IXV-util-MarkItDown.exe`

### Build single executable for macOS

```bash
# PyInstaller is included in dev-dependencies
uv sync

# Build (using macOS spec file)
uv run pyinstaller scripts/IXV-util-MarkItDown-mac.spec
```

- Output: `dist/IXV-util-MarkItDown`
- Note: Always use `scripts/IXV-util-MarkItDown-mac.spec` to properly bundle the markitdown library dependencies

---

## About the CLI implementation

The CLI implemented in `src/cli.py` performs different actions depending on the selected mode:

### MarkItDown mode
- Uses full Microsoft MarkItDown functionality.
- Executes code from `upstream/packages/markitdown`.
- Supports advanced conversion of images, tables, lists, formulas, etc.

### NoMarkItDown mode
- Uses a simple internal implementation.
- Parses docx files with Python's `zipfile` and `xml.etree.ElementTree`.
- Extracts paragraphs and text from `word/document.xml`.
- Outputs basic text as Markdown.

### Code structure
```
src/
├── __init__.py          # Version information
└── cli.py              # Main CLI implementation
    ├── choose_mode()    # Mode selection prompt
    ├── run_markitdown() # Execute MarkItDown mode
    ├── run_nomarkitdown()   # Execute NoMarkItDown mode
    ├── process_files()   # Common file processing logic
    └── main()           # CLI entry point
```

## About upstream

This project includes [Microsoft MarkItDown](https://github.com/microsoft/markitdown) as a git subtree in the `upstream/` directory, allowing you to incorporate updates from the original repository while applying custom extensions.

### How to pull upstream updates

Always use a dedicated branch for pulling updates and merge it into `main` after confirming operation.

```bash
# Add the remote (once)
git remote add markitdown-upstream https://github.com/microsoft/markitdown.git

# Create and checkout a branch for updates
git checkout -b update-upstream-$(date +%Y%m%d)

# Pull the latest changes
git subtree pull --prefix=upstream markitdown-upstream main --squash

# You can also use the provided script (which creates a branch internally)
./scripts/update-upstream.sh

# After verifying, merge into main
git checkout main
git merge --no-ff update-upstream-$(date +%Y%m%d)
```

#### Command explanation

- `--prefix=upstream`: Specifies the directory where the subtree is placed (`upstream/`).
- `markitdown-upstream`: Remote repository name (added above).
- `main`: Branch to pull from (Microsoft MarkItDown's main branch).
- `--squash`: Pulls all upstream commits as a single commit to keep the project history clean.

### Merge procedure if conflicts occur

If you have modified files under `upstream/` in this project, conflicts may arise when pulling updates.

#### Manual merge steps

1. **Attempt to update**
   ```bash
   git subtree pull --prefix=upstream markitdown-upstream main --squash
   ```
2. **If conflicts occur**
   ```bash
   # Check the status
   git status

   # Edit conflicting files to resolve them

   # Stage the resolved files
   git add upstream/path/to/conflicted-file

   # Commit after resolving all conflicts
   git commit
   ```
3. **Strategies for keeping your changes while updating upstream**
   - **Option 1**: Prefer upstream changes and manage your modifications in separate files or directories.
   - **Option 2**: Create a patch file and reapply it after the update.
     ```bash
     # Save your changes as a patch
     git diff upstream/ > my-changes.patch

     # Update upstream
     git subtree pull --prefix=upstream markitdown-upstream main --squash

     # Apply the patch
     git apply my-changes.patch
     ```

#### Recommended development flow

1. **Avoid modifying the `upstream/` directory whenever possible**
   - Implement custom extensions in a separate directory (e.g., `src/extensions/`).
   - Implement by inheriting or extending the upstream code.

2. **If you must modify upstream**
   - Document your changes, e.g., in `docs/upstream-modifications.md`.
   - Periodically check differences with upstream:
     `git diff markitdown-upstream/main HEAD -- upstream/`

#### Upstream modification history

- **2025-08-06**: Fixed issue where empty cells in Excel XLSX/XLS files were displayed as `NaN` (commit: 9185bb7)
  - Modified `upstream/packages/markitdown/src/markitdown/converters/_xlsx_converter.py`
  - Added `na_rep=""` parameter to pandas `to_html` method

---

## Distribution / Updates

- Binaries are planned to be published on GitHub Releases
- Windows: Inno Setup / NSIS installer creation recommended
- macOS: `.dmg` creation with `hdiutil create`
- Automatic updates can use Sparkle (macOS) or custom updater (Windows)

---

## Contributing

1. Open an issue.
2. Fork the repository and create a branch.
3. Submit a Pull Request.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## License

MIT License © 2025 Elvez, Inc. For details, see [LICENSE](./LICENSE).

This project is based on [Microsoft MarkItDown](https://github.com/microsoft/MarkItDown) (MIT License).

---

## Acknowledgments

We would like to express our sincere gratitude to the following contributors for making this project possible.

### Microsoft MarkItDown Team
The high-quality document conversion functionality at the core of this tool is based on the excellent achievements of the [Microsoft MarkItDown](https://github.com/microsoft/MarkItDown) project. We are deeply grateful for making this available as open source, enabling the conversion of documents with complex elements such as images, tables, and formulas to Markdown.

### Development Tools & Library Providers
- **[PyInstaller](https://www.pyinstaller.org/) Development Team**: Thank you for enabling the creation of cross-platform standalone executables.
- **Python Community**: The rich library ecosystem made efficient development possible.

### Open Source Community
IXV-util-MarkItDown is provided as open source under the MIT License and is continuously improved through collaboration with many developers. We are grateful to all who contribute bug reports, feature suggestions, and code contributions.

### Japanese Development Community
The vast document assets created over the years using various tools such as Word and Excel, and the needs from the field to convert them to formats suitable for the AI era, have been the driving force behind this project. We pay respect to the knowledge and experience cultivated in Japanese development environments.

We believe that Markdown will play an important bridging role in the future where human-AI collaboration becomes commonplace. We hope this tool will help make the daily work of many developers even slightly more efficient, allowing more time to be devoted to creative activities.
