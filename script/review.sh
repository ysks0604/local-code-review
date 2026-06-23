#!/bin/bash

# Pythonスクリプトを実行し、結果をOSのクリップボードに送る
# 引数がある場合はそのままPythonスクリプトに渡す ("$@")

if [[ "$OSTYPE" == "darwin"* ]]; then
    python3 generate_review_prompt.py "$@" | pbcopy
    echo "[Success] レビュー用プロンプトをクリップボードにコピーしました！(Mac pbcopy)"
else
    # Linux環境
    if command -v xclip >/dev/null 2>&1; then
        python3 generate_review_prompt.py "$@" | xclip -selection clipboard
        echo "[Success] レビュー用プロンプトをクリップボードにコピーしました！(Linux xclip)"
    elif command -v xsel >/dev/null 2>&1; then
        python3 generate_review_prompt.py "$@" | xsel --clipboard --input
        echo "[Success] レビュー用プロンプトをクリップボードにコピーしました！(Linux xsel)"
    else
        echo "[Error] クリップボード用のコマンド（xclip または xsel）が見つかりません。" >&2
        python3 generate_review_prompt.py "$@"
    fi
fi