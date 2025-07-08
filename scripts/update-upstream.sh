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

# 更新用のブランチ名を生成
UPDATE_BRANCH="update-upstream-$(date +%Y%m%d-%H%M%S)"
echo "更新用ブランチを作成: $UPDATE_BRANCH"
git checkout -b "$UPDATE_BRANCH"

echo "上流リポジトリの最新情報を取得中..."
git fetch markitdown-upstream main

echo ""
echo "変更を取り込み中..."
if git subtree pull --prefix=upstream markitdown-upstream main --squash -m "chore: Update upstream Microsoft MarkItDown"; then
    echo ""
    echo "✅ 正常に更新が完了しました！"
    echo ""
    echo "現在のブランチ: $UPDATE_BRANCH"
    echo ""
    echo "次の手順:"
    echo "1. 動作確認を行ってください"
    echo "2. 問題がなければ、以下のコマンドでmainブランチにマージしてください:"
    echo ""
    echo "   git checkout $CURRENT_BRANCH"
    echo "   git merge --no-ff $UPDATE_BRANCH"
    echo ""
    echo "3. マージ後、不要になったブランチを削除:"
    echo "   git branch -d $UPDATE_BRANCH"
    echo ""
    echo "変更内容を確認するには以下のコマンドを実行してください:"
    echo "  git log -1 --stat"
else
    echo ""
    echo "❌ 更新中にエラーが発生しました。"
    echo "コンフリクトが発生している可能性があります。"
    echo "git status で状態を確認してください。"
    echo ""
    echo "コンフリクトを解決後、以下のコマンドでmainブランチにマージしてください:"
    echo "  git checkout $CURRENT_BRANCH"
    echo "  git merge --no-ff $UPDATE_BRANCH"
    exit 1
fi