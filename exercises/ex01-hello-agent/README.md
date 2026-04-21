# 练习 1：Hello Agent — 你的第一个 AI Agent

## 🎯 学习目标

1. 理解 OpenAI 兼容 Chat Completions API 的基本调用方式
2. 理解 `messages` 列表的结构（`role` + `content`）
3. 理解系统提示词（system prompt）如何定义 Agent 的行为
4. 能够独立完成一个最简单的单轮 LLM 对话程序

## 📋 前置知识

- Python 基础语法（函数、字典、列表）
- 了解 HTTP API 的基本概念
- 了解 JSON 数据格式

## 💡 核心概念

### 什么是 AI Agent？

AI Agent 的最小形态就是一个**能接收用户输入、调用 LLM、返回响应**的程序。在 hermes-agent 中，这个最基础的调用发生在 `run_agent.py` 的 `AIAgent` 类中——它通过 OpenAI 兼容的 Chat Completions API 与 LLM 通信。

### messages 结构

Chat Completions API 使用 `messages` 列表来组织对话：

```python
messages = [
    {"role": "system", "content": "你是一个有帮助的助手。"},   # 系统提示词
    {"role": "user", "content": "你好！"},                    # 用户消息
    # {"role": "assistant", "content": "..."}                 # 模型回复（由 API 返回）
]
```

- `system`：定义 Agent 的身份和行为准则
- `user`：用户的输入
- `assistant`：模型的回复

### hermes-agent 中的对应实现

在 hermes-agent 的 `run_agent.py` 中：
- `AIAgent.__init__()` 初始化 OpenAI 客户端
- `AIAgent._build_system_prompt()` 组装系统提示词
- `AIAgent.chat()` 发送消息并获取回复

本练习你将实现这个流程的最简化版本。

## 📁 文件结构

```
ex01-hello-agent/
├── README.md           ← 你正在看的文件
├── hello_agent.py      ← 代码框架（需要你填写 TODO）
└── mock_client.py      ← mock 替代方案（无需 API key）
```

## 🔧 你需要做什么

打开 `hello_agent.py`，完成所有标记为 `TODO` 的部分：

1. **TODO 1**：构建 `messages` 列表（包含 system 和 user 消息）
2. **TODO 2**：调用 Chat Completions API
3. **TODO 3**：从 API 响应中提取 assistant 的回复文本

## ✅ 验证方法

```bash
# 使用 mock 运行（无需 API key）
python hello_agent.py --mock

# 期望输出类似：
# 🤖 Agent 回复：你好！我是一个 AI 助手，很高兴认识你。有什么我可以帮助你的吗？
```

如果使用真实 API：
```bash
export OPENAI_API_KEY="your-key"
python hello_agent.py
```

## 📖 hermes-agent 源码参考

- **文件**：`hermes-agent/run_agent.py`
- **关键部分**：
  - `AIAgent.__init__()` — 客户端初始化
  - `AIAgent._build_system_prompt()` — 系统提示词组装
  - `AIAgent.chat()` — 单轮对话入口

## 🎯 扩展挑战（可选）

1. 修改系统提示词，让 Agent 扮演不同角色（如翻译官、代码审查员）
2. 添加命令行参数，让用户可以自定义系统提示词
3. 尝试不同的 `temperature` 参数，观察输出变化
