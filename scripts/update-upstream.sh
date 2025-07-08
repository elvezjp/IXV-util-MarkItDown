#!/bin/bash

# Microsoft MarkItDownの最新変更を取り込むスクリプト

set -e

echo "=== Microsoft MarkItDown の最新変更を取り込みます ==="
echo ""

# リモートが存在するか確認
if ! git remote | grep -q "^markitdown-upstream$"; then
    echo "リモート 'markitdown-upstream' が見つかりません。追加します..."
    git remote add markitdown-upstream https://github.com/microsoft/markitdown.git
    echo "リモートを追加しました。"
    echo ""
fi

# 現在のブランチを保存
CURRENT_BRANCH=$(git branch --show-current)
echo "現在のブランチ: $CURRENT_BRANCH"
echo ""

# 作業ツリーがクリーンか確認
if [[ -n $(git status --porcelain) ]]; then
    echo "エラー: 作業ツリーに未コミットの変更があります。"
    echo "変更をコミットまたはスタッシュしてから再実行してください。"
    exit 1
fi

echo "上流リポジトリの最新情報を取得中..."
git fetch markitdown-upstream main

echo ""
echo "変更を取り込み中..."
if git subtree pull --prefix=upstream markitdown-upstream main --squash -m "chore: Update upstream Microsoft MarkItDown"; then
    echo ""
    echo "✅ 正常に更新が完了しました！"
    echo ""
    echo "変更内容を確認するには以下のコマンドを実行してください:"
    echo "  git log -1 --stat"
else
    echo ""
    echo "❌ 更新中にエラーが発生しました。"
    echo "コンフリクトが発生している可能性があります。"
    echo "git status で状態を確認してください。"
    exit 1
fi