import os
import subprocess
import argparse
import readchar

import anthropic

# 設置 Anthropic API 密鑰
api_key = os.environ.get("ANTHROPIC_API_KEY")


# 獲取已暫存的變更列表
def get_staged_changes(repo_path):
    output = subprocess.check_output(["git", "-C", repo_path, "diff", "--staged"])
    changed_files = output.decode("utf-8").splitlines()
    return changed_files


# 使用 Anthropic Claude 生成提交信息
def generate_commit_messages(changes, num_messages=5):
    prompt = f"""以下是我這次在 git 變更的列表:

{changes}

請根據這些修改,用英文生成{num_messages}條簡潔的 Git commit message,總結本次提交的主要內容。
每條提交信息應以 feat、fix、docs、style、refactor、perf、test 或 chore 開頭,
說明提交的類型,然後用冒號和空格分隔,再簡要描述提交的內容,例如:'feat: update README.md'
請用換行符分隔每條提交信息。"""

    client = anthropic.Client(api_key=api_key)

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}"
            }
        ]
    )

    commit_messages = response.content[0].text.split("\n")
    # remove empty strings
    commit_messages = [message for message in commit_messages if message]
    return commit_messages


def select_commit_message(commit_messages):
    selected_index = 0

    commit_messages.append("自定義提交信息")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("請使用方向鍵上下選擇提交信息,按Enter鍵確認:")
        for i, message in enumerate(commit_messages):
            prefix = "> " if i == selected_index else "  "
            print(f"{prefix}{i + 1}. {message}")

        key = readchar.readkey()
        if key == readchar.key.UP:
            selected_index = (selected_index - 1) % (len(commit_messages) + 1)
        elif key == readchar.key.DOWN:
            selected_index = (selected_index + 1) % (len(commit_messages) + 1)
        elif key == readchar.key.ENTER:
            break

    if selected_index == len(commit_messages) - 1:
        return input("請輸入自定義的提交信息: ")
    else:
        return commit_messages[selected_index]


def confirm_commit(selected_message):
    while True:
        print(f"\n選擇的提交信息: {selected_message}")
        confirm = input("是否確認使用此提交信息進行提交? [Y/n]: ")
        if confirm.lower() == 'y' or confirm == '':
            return True
        elif confirm.lower() == 'n':
            return False
        else:
            print("無效的輸入,請輸入 'y' 或 'n'。")


def main():
    parser = argparse.ArgumentParser(description="生成 Git 提交信息")
    parser.add_argument("repo_path", help="Git 倉庫路徑")
    args = parser.parse_args()

    repo_path = args.repo_path

    # 獲取已暫存的變更
    staged_changes = get_staged_changes(repo_path)

    if staged_changes:
        # 將變更列表轉換為字符串
        changes_str = "\n".join(staged_changes)

        # 生成提交信息
        commit_messages = generate_commit_messages(changes_str)

        # 使用方向鍵選擇提交信息
        selected_message = select_commit_message(commit_messages)

        # 確認是否要使用選擇的提交信息進行提交
        if confirm_commit(selected_message):
            # 執行 Git 提交
            subprocess.run(["git", "-C", repo_path, "commit", "-m", selected_message])
            print("Git 提交已完成。")
        else:
            print("Git 提交已取消。")
    else:
        print("沒有已暫存的變更,無需生成提交信息。")


if __name__ == "__main__":
    main()