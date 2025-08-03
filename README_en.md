# IXV-util-MarkItDown

IXV-util-MarkItDown bundles Microsoft MarkItDown into a cross-platform CLI utility available as a standalone executable (`.exe`) for Windows and an application (`.app`) for macOS. In MarkItDown mode it accepts not only `.docx` but also other formats supported by the library, such as PDF, and converts them to Markdown.

---

# About IXV and IXV-util Series

## What is IXV?
IXV is a next-generation AI development support platform developed by Elves Inc. It aims to support the entire software development process from requirements definition to design, implementation, testing, and operation by leveraging AI technology.

## What is the IXV-util Series?
The IXV-util series is a collection of lightweight utility tools born from the IXV development process, designed to support daily development tasks.

These tools can be used not only as part of the IXV platform but also independently, with the goal of improving developers' daily work efficiency.

They are also provided as open source and are continuously improved through collaboration with the developer community.

---

# Why Markdown?
We have created many documents in software development projects. Legacy tools such as Word and Excel are difficult to parse and reuse programmatically. They look organized on the surface, but their underlying structure is ambiguous, making automated processing and AI utilization challenging. Markdown is close to plain text, requiring only minimal markup while still expressing important document structure. Modern large language models can speak Markdown natively and often respond in Markdown without being asked. We believe Markdown is the file format of note for interactions between humans and AI.

---

## Features

- **High-quality conversion**: Uses the core functions of Microsoft MarkItDown to properly convert images, tables, lists, formulas, etc. into Markdown.
- **Cross-platform**: Runs natively on Windows (`.exe`) and macOS (`.app`).
- **Simple CLI**: No GUI, easy to incorporate into scripts or CI/CD.
- **Batch processing**: Supports converting multiple files at once.
- **Open source**: Customizable freely under the MIT license.

---

## Modes of operation

The tool has two modes:

1. **MarkItDown mode**: Uses the full Microsoft MarkItDown functionality.
   - Supports advanced conversion of images, tables, lists, formulas, and more.
   - Does not check file extensions and can handle any format supported by MarkItDown, such as PDF or PPTX.

2. **NoMarkItDown mode**: Simple built-in implementation.
   - Extracts only basic text.
   - Lightweight and fast.

By default the program prompts you to choose a mode at startup. Specify `--mode` to skip the prompt.

---

## Installation

### Windows

1. Download the latest `IXV-util-MarkItDown-<version>-win.exe` from [Releases](https://github.com/elvezjp/IXV-util-MarkItDown/releases).
2. Place it in any folder and add it to your PATH if necessary.
3. Run the following in Command Prompt or PowerShell:
   ```bat
   ixv-util-markitdown input.docx -o output.md
   ```
   *In MarkItDown mode you may also specify other formats like `input.pdf`.*

### macOS

1. Download `IXV-util-MarkItDown-<version>.dmg` from [Releases](https://github.com/elvezjp/IXV-util-MarkItDown/releases).
2. Mount the DMG and drag the application to your `Applications` folder.
3. Run the following in Terminal:
   ```bash
   ixv-util-markitdown input.docx -o output.md
   ```
   *In MarkItDown mode you may also specify other formats like `input.pdf`.*

---

## Usage

When executed without `--mode`, you are asked to choose **MarkItDown mode** or **NoMarkItDown mode**. After choosing, specify your input as follows:

```bash
# Convert a single file
ixv-util-markitdown input.docx -o output.md

# Batch convert multiple files
ixv-util-markitdown *.docx -d docs/markdown

# List options
ixv-util-markitdown --help
```

*MarkItDown mode also accepts non-`.docx` files such as `input.pdf`.*

### Non-interactive mode

```bash
# Run in MarkItDown mode
ixv-util-markitdown input.docx --mode markitdown

# Run in NoMarkItDown mode
ixv-util-markitdown input.docx --mode nomarkitdown
```

- `--mode` : Choose conversion mode without a prompt (`markitdown` or `nomarkitdown`).
- `-o, --output` : Specify the output file name.
- `-d, --directory` : Specify the output directory (creates it if it doesn't exist).
- `-v, --version` : Display version.
- `-h, --help`    : Show help.

Mode selection is not required when only displaying help (`--help`) or version information (`--version`).

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
# Install PyInstaller
uv pip install pyinstaller

# Build
pyinstaller --onefile wrapper.py --name ixv-util-markitdown.exe
```

- Output: `dist/ixv-util-markitdown.exe`

### Build `.app` for macOS

```bash
# Install PyInstaller (included in dev dependencies)
uv sync

# Build (using macOS spec file)
uv run pyinstaller scripts/IXV-util-MarkItDown-mac.spec
```

- Output: `dist/IXV-util-MarkItDown.app`
- Note: Use `scripts/IXV-util-MarkItDown-mac.spec` to properly bundle the markitdown library dependencies

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

---

## Distribution / Updates

- Binaries are published on GitHub Releases.
- Windows: use Inno Setup / NSIS to create installers.
- macOS: create `.dmg` with `hdiutil create`.
- Automatic updates can be implemented with Sparkle on macOS or a custom updater on Windows.

---

## Contributing

1. Open an issue.
2. Fork the repository and create a branch.
3. Submit a Pull Request.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## License

MIT License © 2025 Elvez, Inc.

---

## Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/MarkItDown)
- [PyInstaller](https://www.pyinstaller.org/)
- Icon sources: Font Awesome, Google Material Icons
