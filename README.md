# IXV-util-MarkItDown

IXV-util-MarkItDown は、Microsoft MarkItDown をベースにした `.docx` → Markdown 変換ツールを、Windows の単一実行ファイル（`.exe`）および macOS アプリケーション（`.app`）としてバンドルしたクロスプラットフォーム CLI ユーティリティです。

---

## 特徴

- **高品質変換**：Microsoft MarkItDown のコア機能を利用し、画像・表・リスト・数式などを適切に Markdown に変換  
- **クロスプラットフォーム**：Windows (`.exe`) / macOS（`.app`）でネイティブに動作  
- **シンプル CLI**：GUI を持たず、スクリプトや CI/CD への組み込みも容易  
- **一括処理**：複数ファイルのバッチ変換をサポート  
- **オープンソース**：MIT ライセンスで自由にカスタマイズ可能  

---

## インストール

### Windows

1. [Releases](https://github.com/your-org/IXV-util-MarkItDown/releases) から最新版の `IXV-util-MarkItDown-<version>-win.exe` をダウンロード  
2. 任意のフォルダに配置し、必要であれば PATH 環境変数に追加  
3. コマンドプロンプトまたは PowerShell で以下を実行  
   ```bat
   markitdown input.docx -o output.md
   ```

### macOS

1. [Releases](https://github.com/your-org/IXV-util-MarkItDown/releases) から `IXV-util-MarkItDown-<version>.dmg` をダウンロード  
2. DMG をマウントし、`Applications` フォルダにドラッグ＆ドロップ  
3. ターミナルで以下を実行  
   ```bash
   markitdown input.docx -o output.md
   ```

---

## 使い方

```bash
# 単一ファイル変換
markitdown input.docx -o output.md

# 複数ファイル一括変換
markitdown *.docx -d docs/markdown

# 変換オプション一覧
markitdown --help
```

- `-o, --output` : 出力ファイル名を指定  
- `-d, --directory` : 出力先ディレクトリを指定（存在しない場合は作成）  
- `-v, --version` : バージョン表示  
- `-h, --help`    : ヘルプ表示  

---

## 開発／ビルド方法

### 前提

- Python 3.7 以上  
- pip, git  

### リポジトリのクローン

```bash
git clone https://github.com/your-org/IXV-util-MarkItDown.git
cd IXV-util-MarkItDown
pip install -e .
```

### Windows 用 `.exe` のビルド

```bash
pip install pyinstaller
pyinstaller --onefile wrapper.py   --name markitdown.exe   --icon resources/app.ico   --add-data "templates;templates"
```

- 出力：`dist/markitdown.exe`

### macOS 用 `.app` のビルド

```bash
pip install py2app
python setup.py py2app
```

- 出力：`dist/IXV-util-MarkItDown.app`

---

## 配布／アップデート

- バイナリは GitHub Releases で公開  
- Windows：Inno Setup / NSIS でインストーラ化推奨  
- macOS：`hdiutil create` で `.dmg` 化  
- 自動アップデートには Sparkle（macOS）や自作アップデータ（Windows）を利用可能

---

## 貢献

1. Issue を立ててください  
2. リポジトリを Fork → ブランチを作成  
3. Pull Request を送信  

詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) を参照

---

## ライセンス

MIT License © 2025 IXV Team

---

## 謝辞

- [Microsoft MarkItDown](https://github.com/microsoft/MarkItDown)  
- [PyInstaller](https://www.pyinstaller.org/)  
- [py2app](https://github.com/ronaldoussoren/py2app)  
- アイコン素材：Font Awesome、Google Material Icons  
