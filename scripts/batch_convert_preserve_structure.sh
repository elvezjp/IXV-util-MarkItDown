#!/bin/bash

# 使用方法を表示する関数
show_usage() {
    echo "使用方法: $0 <入力ディレクトリ> <出力ディレクトリ> [拡張子]"
    echo "例: $0 ./input_docs ./output_docs docx"
    echo "拡張子を指定しない場合はdocxがデフォルトで使用されます"
    exit 1
}

# 引数チェック
if [ $# -lt 2 ]; then
    show_usage
fi

# 変数の設定
INPUT_DIR="$1"
OUTPUT_DIR="$2"
EXTENSION="${3:-docx}"  # デフォルトはdocx
CONVERTER="./dist/IXV-util-MarkItDown"

# 入力ディレクトリの存在確認
if [ ! -d "$INPUT_DIR" ]; then
    echo "エラー: 入力ディレクトリ '$INPUT_DIR' が存在しません"
    exit 1
fi

# コンバータの存在確認
if [ ! -f "$CONVERTER" ]; then
    echo "エラー: コンバータ '$CONVERTER' が見つかりません"
    exit 1
fi

# 出力ディレクトリが存在しない場合は作成
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "出力ディレクトリ '$OUTPUT_DIR' を作成します..."
    mkdir -p "$OUTPUT_DIR"
fi

# 変換したファイル数のカウンタ
converted_count=0
error_count=0

echo "================================================"
echo "変換開始"
echo "入力ディレクトリ: $INPUT_DIR"
echo "出力ディレクトリ: $OUTPUT_DIR"
echo "対象拡張子: .$EXTENSION"
echo "================================================"

# 指定された拡張子のファイルを再帰的に検索して処理
find "$INPUT_DIR" -type f -name "*.$EXTENSION" | while read -r file_path; do
    # 入力ディレクトリからの相対パスを取得
    relative_path="${file_path#$INPUT_DIR/}"

    # 出力ファイルのディレクトリパスを生成
    output_dir="$OUTPUT_DIR/$(dirname "$relative_path")"

    echo "変換中: $relative_path"

    # 実行するコマンドを表示
    echo "  コマンド: $CONVERTER --mode markitdown --directory \"$output_dir\" \"$file_path\""

    # IXV-util-MarkItDownを実行（--directoryオプションを使用）
    if "$CONVERTER" --mode markitdown --directory "$output_dir" "$file_path"; then
        output_path="$output_dir/$(basename "${file_path%.$EXTENSION}.md")"
        echo "  ✓ 成功: $output_path"
        ((converted_count++))
    else
        echo "  ✗ エラー: $file_path の変換に失敗しました"
        ((error_count++))
    fi
done

echo "================================================"
echo "変換完了"
echo "成功: $converted_count ファイル"
echo "エラー: $error_count ファイル"
echo "================================================"