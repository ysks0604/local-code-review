@echo off
rem Windows用: Pythonスクリプトを実行し、結果を clip コマンドでクリップボードに送る
rem 引数がある場合はそのままPythonスクリプトに渡す (%*)
rem 文字化け対策（UTF-8出力をWindowsのclipに渡すため、一瞬だけコードページをUTF-8[65001]に変更）

chcp 65001 > nul
python generate_review_prompt.py %* | clip
chcp 932 > nul

echo [Success] レビュー用プロンプトをクリップボードにコピーしました！ (Windows clip)