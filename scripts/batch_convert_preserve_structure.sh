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

# 対象ファイルの数を取得
total_files=$(find "$INPUT_DIR" -type f -name "*.$EXTENSION" | wc -l | tr -d ' ')

# ファイルが見つからない場合の処理
if [ "$total_files" -eq 0 ]; then
    echo "エラー: 対象となる .$EXTENSION ファイルが見つかりませんでした"
    exit 1
fi

# 一時ファイルを作成してカウンタを保持
temp_file=$(mktemp)
echo "0 0" > "$temp_file"

echo "================================================"
echo "変換開始"
SECONDS=0  # 経過時間計測開始
echo "入力ディレクトリ: $INPUT_DIR"
echo "出力ディレクトリ: $OUTPUT_DIR"
echo "対象拡張子: .$EXTENSION"
echo "対象ファイル数: $total_files"
echo "================================================"

# 指定された拡張子のファイルを再帰的に検索して処理
current_file=0
find "$INPUT_DIR" -type f -name "*.$EXTENSION" | while IFS= read -r file_path; do
    ((current_file++))

    # カウンタを読み込み
    read converted_count error_count < "$temp_file"
    # 入力ディレクトリからの相対パスを取得
    relative_path="${file_path#$INPUT_DIR/}"

    # 出力ファイルのパスを生成
    output_dir="$OUTPUT_DIR/$(dirname "$relative_path")"
    output_path="$output_dir/$(basename "$file_path").md"

    # 出力ディレクトリを作成
    mkdir -p "$output_dir"

    echo "[$current_file/$total_files] 変換中: $relative_path"

    # 実行するコマンドを表示
    echo "  コマンド: $CONVERTER --mode markitdown --output \"$output_path\" \"$file_path\""

    # IXV-util-MarkItDownを実行（--outputオプションを使用）
    if "$CONVERTER" --mode markitdown --output "$output_path" "$file_path"; then
        echo "  ✓ 成功: $output_path"
        ((converted_count++))
    else
        echo "  ✗ エラー: $file_path の変換に失敗しました"
        ((error_count++))
    fi

    # カウンタを一時ファイルに保存
    echo "$converted_count $error_count" > "$temp_file"
done

# 最終的なカウンタを読み込み
read converted_count error_count < "$temp_file"

# 一時ファイルを削除
rm -f "$temp_file"

elapsed=$SECONDS
hours=$((elapsed / 3600))
minutes=$(((elapsed % 3600) / 60))
seconds=$((elapsed % 60))

echo "================================================"
echo "変換完了"
echo "成功: $converted_count / $total_files ファイル"
echo "エラー: $error_count / $total_files ファイル"
printf "所要時間: %02d時間%02d分%02d秒\n" "$hours" "$minutes" "$seconds"
echo "================================================"
