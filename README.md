# Git Commit Message Generator

這是一個使用 Python 和 Anthropic Claude API 生成 Git commit msg的工具。它可以根據已暫存的變更自動生成多個候選的 commit
msg，讓你選擇最合適的一條，或者輸入自定義的 commit msg。

## 功能特點

- 自動獲取 Git 倉庫中已暫存的變更列表
- 使用 Anthropic Claude API 生成多個候選的 commit msg
- 支持使用方向鍵上下選擇 commit msg
- 支持輸入自定義的 commit msg
- 在提交前進行確認，避免意外提交
- 支持指定 Git 倉庫的路徑

## 安裝

1. Git Clone
2. 安裝需要的 Python package

```bash
  pip install -r requirements.txt
```

3. 設置 Anthropic Claude API 金鑰

請訪問 [Anthropic Claude API](https://claude.anthropic.com/) 獲取 API 金鑰，並將將你的 Anthropic Claude API
金鑰設置為名為 `CLAUDE_API_KEY` 的環境變量。

```bash
  export "CLAUDE_API_KEY=your_api_key"
```

## 使用

```bash
    python git_commit_message_generator.py /path/to/your/repo
```

將 `/path/to/your/repo` 替換為你的 Git 倉庫的實際路徑。

1. 腳本將獲取已暫存的變更，並使用 Anthropic Claude API 生成候選的 commit msg。

2. 使用方向鍵上下選擇你喜歡的 commit msg，然後按 Enter 鍵確認。你也可以選擇 "0. 自定義commit msg" 選項，然後輸入自己的commit
   msg。

3. 確認是否要使用選擇的 commit msg進行提交。輸入 'y' 或直接按 Enter 鍵確認提交，輸入 'n' 取消提交。

4. 如果確認提交，腳本將使用選擇的 commit msg執行 Git 提交操作。

## 貢獻

歡迎對此項目進行貢獻!如果你有任何改進或新功能的想法，請創建一個 Pull Request。