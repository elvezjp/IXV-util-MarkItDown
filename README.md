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

## 現在の実装状況

**注意**: 現在の実装は独自のシンプルな変換機能のみを提供しており、Microsoft MarkItDown の upstream コードはまだ統合されていません。

### 実装済み機能
- **基本的なテキスト抽出**: .docx ファイルからテキストを抽出し、段落ごとに Markdown 形式で出力
- **クロスプラットフォーム対応**: Python ベースで Windows/macOS/Linux で動作
- **シンプル CLI**: コマンドラインから簡単に使用可能
- **一括処理**: 複数ファイルのバッチ変換をサポート
- **柔軟な出力設定**: 出力ファイル名や出力ディレクトリの指定が可能

### 未実装機能
- 画像の抽出と変換
- 表（テーブル）の構造保持
- リスト（箇条書き・番号付き）の適切な変換
- 数式の変換
- スタイル情報（太字、斜体など）の保持

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

- Python 3.8 以上
- [uv](https://github.com/astral-sh/uv) (Python パッケージマネージャー)
- git

### リポジトリのクローン

```bash
git clone https://github.com/your-org/IXV-util-MarkItDown.git
cd IXV-util-MarkItDown

# uvのインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python環境のセットアップと依存関係のインストール
uv sync

# 開発モードでインストール
uv pip install -e .
```

### Windows 用 `.exe` のビルド

```bash
# PyInstallerをインストール
uv pip install pyinstaller

# ビルド実行
pyinstaller --onefile wrapper.py \
  --name markitdown.exe \
  --icon resources/app.ico \
  --add-data "templates;templates"
```

- 出力：`dist/markitdown.exe`

### macOS 用 `.app` のビルド

```bash
# PyInstallerをインストール（dev-dependenciesに含まれています）
uv sync

# ビルド実行
uv run pyinstaller --onedir --windowed --name MarkItDown --distpath ./dist markitdown/cli.py
```

- 出力：`dist/MarkItDown.app`

---

## 現在の CLI 実装について

現在の CLI は `markitdown/cli.py` に実装されており、以下の処理を行います：

1. **docx ファイルの解析**: Python の `zipfile` と `xml.etree.ElementTree` を使用
2. **テキスト抽出**: `word/document.xml` から段落（`w:p`）とテキスト（`w:t`）要素を抽出
3. **Markdown 出力**: 抽出したテキストを段落ごとに空行で区切って出力

### コード構成

```
markitdown/
├── __init__.py      # バージョン情報
└── cli.py          # メインのCLI実装
    ├── extract_text()    # docxからテキスト抽出
    ├── convert_file()    # ファイル変換処理
    └── main()           # CLI エントリーポイント
```

## upstream について

このプロジェクトは [Microsoft MarkItDown](https://github.com/microsoft/markitdown) を git subtree として `upstream/` ディレクトリに取り込んでいます。これにより、元のリポジトリの更新を取り込みながら、独自の機能拡張を行うことができます。

### 上流の更新を取り込む方法

上流の更新は必ず専用のブランチで行い、動作確認後にmainブランチにマージしてください。

```bash
# 初回のみ: リモートを追加
git remote add markitdown-upstream https://github.com/microsoft/markitdown.git

# 更新用のブランチを作成してチェックアウト
git checkout -b update-upstream-$(date +%Y%m%d)

# 最新の変更を取り込む
git subtree pull --prefix=upstream markitdown-upstream main --squash

# または、用意されたスクリプトを使用（スクリプトも内部でブランチを作成します）
./scripts/update-upstream.sh

# 動作確認後、mainブランチにマージ
git checkout main
git merge --no-ff update-upstream-$(date +%Y%m%d)
```

#### コマンドの説明

- `--prefix=upstream`: subtreeを配置するディレクトリを指定。この場合、`upstream/`ディレクトリ配下に取り込まれます
- `markitdown-upstream`: リモートリポジトリの名前（上記で追加したリモート）
- `main`: 取り込む対象のブランチ名（Microsoft MarkItDownのメインブランチ）
- `--squash`: 取り込む際に、上流リポジトリの全コミット履歴を1つのコミットにまとめます。これにより、プロジェクトのコミット履歴をクリーンに保つことができます

### コンフリクトが発生した場合のマージ手順

IXV-util-MarkItDown側で`upstream/`ディレクトリ内のファイルを独自に修正している場合、上流の更新を取り込む際にコンフリクトが発生することがあります。

#### 手動マージの手順

1. **更新を試みる**
   ```bash
   git subtree pull --prefix=upstream markitdown-upstream main --squash
   ```

2. **コンフリクトが発生した場合**
   ```bash
   # コンフリクトの状態を確認
   git status

   # コンフリクトのあるファイルを編集して解決

   # 解決後、ファイルをステージング
   git add upstream/path/to/conflicted-file

   # すべてのコンフリクトを解決したらコミット
   git commit
   ```

3. **独自の変更を保持しつつ上流の更新を取り込む戦略**
   - **オプション1**: 上流の変更を優先し、独自の変更は別ファイルまたは別ディレクトリで管理
   - **オプション2**: パッチファイルを作成し、更新後に再適用
     ```bash
     # 独自の変更をパッチとして保存
     git diff upstream/ > my-changes.patch

     # 上流を更新
     git subtree pull --prefix=upstream markitdown-upstream main --squash

     # パッチを適用
     git apply my-changes.patch
     ```

#### 推奨される開発フロー

1. **upstream/ディレクトリは可能な限り変更しない**
   - 独自の拡張は別のディレクトリ（例：`src/extensions/`）で行う
   - upstreamのコードを継承・拡張する形で実装

2. **どうしてもupstreamを変更する必要がある場合**
   - 変更内容を文書化し、`docs/upstream-modifications.md`などに記録
   - 定期的に上流との差分を確認：`git diff markitdown-upstream/main HEAD -- upstream/`

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
- アイコン素材：Font Awesome、Google Material Icons
