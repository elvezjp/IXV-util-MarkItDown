# IXV-util-MarkItDown
[English README](./README_en.md) is available.

<img width="1745" height="684" alt="ixv-util" src="https://github.com/user-attachments/assets/b4cca023-74f7-4068-897f-4558690fdbdd" />


IXV-util-MarkItDown は、Microsoft MarkItDown をベースにした Markdown 変換ツールを、Windows の単一実行ファイル（`.exe`）および macOS アプリケーション（`.app`）としてバンドルしたクロスプラットフォーム CLI ユーティリティです。MarkItDown モードでは `.docx` に限らず、MarkItDown ライブラリがサポートする PDF などのファイル形式も Markdown に変換できます。

---

# IXV および IXV-util シリーズについて
## IXV（イクシブ）とは
IXV は、株式会社エルブズが開発している次世代の AI 開発支援プラットフォームです。AI 技術を活用して、要件定義から設計、実装、テスト、運用までのソフトウェア開発プロセス全体を支援することを目指しています。

## IXV-util シリーズとは
IXV-util シリーズは、IXV の開発過程で生まれた、日常の開発業務を支援するための軽量なユーティリティツール群です。
これらのツールは、IXV プラットフォームの一部としてだけでなく、単体でも利用可能で、開発者の日々の作業効率を向上させることを目的としています。
またIXV-util-MarkItDownは、オープンソースで提供されており、開発者コミュニティとの協力を通じて継続的に改善されています。

---

# 私たちがMarkdownに注目する理由
私たちは、日本の開発現場でたくさんのドキュメントを作成してきました。
さまざまな時代のツール、例えばWordやExcelなどは、構造的な解析や再利用、プログラムによる処理が非常に困難でした。
表面的には整って見える一方で、コンピュータから見たときには構造が曖昧で、自動処理やAIによる活用に大きな壁がありました。
Markdownは、プレーンテキストに非常に近く、最小限のマークアップや書式指定で済みますが、それでも文書の重要な構造を表現する手段を提供します。
現在利用可能な主たる大規模言語モデル（LLM）の多くは、ネイティブにMarkdownを「話す」能力があり、多くの場合、指示されなくてもMarkdownを使って応答を返します。
人間とAIのやり取りに着目した時、Markdown形式のテキストが、着目すべきファイル形式であろうと私たちは考えています。

---

## 特徴

- **高品質変換**：Microsoft MarkItDown のコア機能を利用し、画像・表・リスト・数式などを適切に Markdown に変換
- **クロスプラットフォーム**：Windows (`.exe`) / macOS（`.app`）でネイティブに動作
- **シンプル CLI**：GUI を持たず、スクリプトや CI/CD への組み込みも容易
- **一括処理**：複数ファイルのバッチ変換をサポート
- **オープンソース**：MIT ライセンスで自由にカスタマイズ可能

---

## 動作モード

本ツールには 2 つの動作モードがあります：

1. **MarkItDown モード**: Microsoft MarkItDown の完全な機能を使用
   - 画像、表、リスト、数式などの高度な変換に対応
   - 拡張子チェックを行わず、MarkItDown ライブラリがサポートする PDF や PPTX などのファイル形式を処理

2. **NoMarkItDown モード**: シンプルな独自実装
   - `.docx` ファイルからの基本的なテキスト抽出のみ（他の拡張子はエラー）
   - 軽量で高速な動作

プログラムを起動すると、どちらのモードを使用するか選択できます。

---

## インストール

### Windows

1. [Releases](https://github.com/elvezjp/IXV-util-MarkItDown/releases) から最新版の `IXV-util-MarkItDown-<version>-win.exe` をダウンロード
2. 任意のフォルダに配置し、必要であれば PATH 環境変数に追加
3. コマンドプロンプトまたは PowerShell で以下を実行
   ```bat
   ixv-util-markitdown input.docx -o output.md
   ```
   *MarkItDown モードでは `input.pdf` など他形式も指定できます。*

### macOS

1. [Releases](https://github.com/elvezjp/IXV-util-MarkItDown/releases) から `IXV-util-MarkItDown-<version>.dmg` をダウンロード
2. DMG をマウントし、`Applications` フォルダにドラッグ＆ドロップ
3. ターミナルで以下を実行
   ```bash
   ixv-util-markitdown input.docx -o output.md
   ```
   *MarkItDown モードでは `input.pdf` など他形式も指定できます。*

---

## 使い方

変換したいファイルパスを引数に指定して実行すると、直後に **MarkItDown モード** と **NoMarkItDown モード** の選択プロンプトが表示されます。

```bash
# 単一ファイル変換
ixv-util-markitdown input.docx

# 複数ファイル一括変換
ixv-util-markitdown *.docx

# 出力先のディレクトリを指定
ixv-util-markitdown inputs/*.docx -d outputs

# 変換オプション一覧
ixv-util-markitdown --help
```

*MarkItDown モードでは `input.pdf` のように `.docx` 以外のファイルも指定できます。*
### 非対話モード

`--mode` オプションを指定するとモード選択のプロンプトをスキップできます。

```bash
# MarkItDown モードで実行
ixv-util-markitdown input.docx --mode markitdown

# NoMarkItDown モードで実行
ixv-util-markitdown input.docx --mode nomarkitdown
```


- `--mode` : 非対話モードで動作モードを指定（`markitdown` または `nomarkitdown`）
- `-o, --output` : 出力ファイル名を指定
- `-d, --directory` : 出力先ディレクトリを指定（存在しない場合は作成）
- `-v, --version` : バージョン表示
- `-h, --help`    : ヘルプ表示

---

## 開発／ビルド方法

### 前提

- Python 3.10 以上
- [uv](https://github.com/astral-sh/uv) (Python パッケージマネージャー)
- git

### リポジトリのクローン

```bash
git clone https://github.com/elvezjp/IXV-util-MarkItDown.git
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
# PyInstallerをインストール（dev-dependenciesに含まれています）
uv sync

# ビルド実行
pyinstaller --onefile wrapper.py --name ixv-util-markitdown.exe
```

- 出力：`dist/ixv-util-markitdown.exe`

### macOS 用 `.app` のビルド

```bash
# PyInstallerをインストール（dev-dependenciesに含まれています）
uv sync

# ビルド実行（macOS用specファイルを使用）
uv run pyinstaller scripts/IXV-util-MarkItDown-mac.spec
```

- 出力：`dist/IXV-util-MarkItDown.app`
- 注意：markitdownライブラリの依存関係を適切に同梱するため、必ず`scripts/IXV-util-MarkItDown-mac.spec`を使用してください

---

## CLI 実装について

`src/cli.py` に実装されたCLIは、選択されたモードに応じて以下の処理を行います：

### MarkItDown モード
- Microsoft MarkItDown の完全な機能を使用
- `upstream/packages/markitdown` のコードを実行
- 画像、表、リスト、数式などの高度な変換に対応

### NoMarkItDown モード
- シンプルな独自実装を使用
- Python の `zipfile` と `xml.etree.ElementTree` で docx ファイルを解析
- `word/document.xml` から段落とテキストを抽出
- 基本的なテキストのみを Markdown として出力

### コード構成

```
src/
├── __init__.py          # バージョン情報
└── cli.py              # メインのCLI実装
    ├── choose_mode()    # モード選択プロンプト
    ├── run_markitdown() # MarkItDownモードの実行
    ├── run_nomarkitdown()   # NoMarkItDownモードの実行
    ├── process_files()   # ファイル処理共通ロジック
    └── main()          # CLI エントリーポイント
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

MIT License © 2025 株式会社エルブズ（Elvez, Inc.）

---

## 謝辞

- [Microsoft MarkItDown](https://github.com/microsoft/MarkItDown)
- [PyInstaller](https://www.pyinstaller.org/)
- アイコン素材：Font Awesome、Google Material Icons
