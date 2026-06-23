import subprocess
import os
import sys

RULE_FILES = [
    'SKILL.md',
    'common.md',
    'language.md',
    'project.md'
]

def get_git_diff():
    """ローカルの変更差分、または指定されたコミット/ブランチの差分を取得する"""
    # コマンドライン引数（ファイル名より後の部分）を取得
    args = sys.argv[1:]
    
    try:
        if args:
            # 引数が指定された場合（例: ./review.sh HEAD~1 等）
            cmd = ['git', 'diff'] + args
            return subprocess.check_output(cmd, text=True, encoding='utf-8', errors='ignore').strip()
        else:
            # 引数がない場合はデフォルト（staged + unstaged）
            diff_unstaged = subprocess.check_output(['git', 'diff'], text=True, encoding='utf-8', errors='ignore')
            diff_staged = subprocess.check_output(['git', 'diff', '--cached'], text=True, encoding='utf-8', errors='ignore')
            return (diff_staged + "\n" + diff_unstaged).strip()
            
    except subprocess.CalledProcessError:
        print("[Error] Gitコマンドの実行に失敗しました。コミットハッシュやブランチ名が正しいか確認してください。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[Error] 差分の取得中にエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    git_diff = get_git_diff()
    if not git_diff:
        print("[Warning] 変更差分（git diff）が検出されませんでした。", file=sys.stderr)
        sys.exit(1)

    prompt_parts = []
    prompt_parts.append("========================================================================")
    prompt_parts.append("# CODE REVIEW INSTRUCTIONS AND RULES")
    prompt_parts.append("ユーザーが提示するコードの差分について、以下のルール、チェックリスト、およびペルソナに従って厳格にレビューしてください。")
    prompt_parts.append("========================================================================\n")

    for filename in RULE_FILES:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    prompt_parts.append(f"### --- START OF FILE: {filename} ---")
                    prompt_parts.append(f.read().strip())
                    prompt_parts.append(f"### --- END OF FILE: {filename} ---\n")
            except Exception as e:
                print(f"[Warning] {filename} の読み込みに失敗しました: {e}", file=sys.stderr)
        else:
            print(f"[Info] ルールファイル {filename} が見つからないためスキップします。", file=sys.stderr)

    prompt_parts.append("========================================================================")
    prompt_parts.append("# TARGET CODE DIFF TO REVIEW")
    prompt_parts.append("以下の変更差分（git diff）に対してレビューを実施し、結果を出力してください。")
    prompt_parts.append("========================================================================\n")
    prompt_parts.append("```diff")
    prompt_parts.append(git_diff)
    prompt_parts.append("```")

    print("\n".join(prompt_parts))

if __name__ == '__main__':
    main()