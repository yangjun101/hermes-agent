# 练习 3：多轮对话循环 — 完整的 Agent Loop

## 🎯 学习目标

1. 理解 Agent Loop 的核心设计：循环调用 LLM 直到任务完成
2. 理解循环终止条件：模型不再请求工具调用时停止
3. 理解消息历史管理：如何维护完整的对话上下文
4. 实现一个支持多轮工具调用的完整 Agent Loop

## 📋 前置知识

- 完成练习 1（Hello Agent）和练习 2（工具调用基础）
- 理解 tool_calls 的解析和工具结果回传流程

## 💡 核心概念

### 从单次到多轮

练习 2 中我们实现了单次工具调用：模型调用一个工具，拿到结果后生成回复。但真实场景中，模型可能需要**连续调用多个工具**才能完成任务。例如：

```
用户：比较北京和上海的天气

→ LLM 调用 get_weather(city="北京")
→ LLM 调用 get_weather(city="上海")
→ LLM 综合两个结果，生成最终回复
```

### Agent Loop 的核心逻辑

```python
while True:
    response = call_llm(messages)
    
    if response 有 tool_calls:
        执行工具，将结果加入 messages
        continue  # 继续循环
    else:
        return response.content  # 模型自然停止，返回回复
```

这就是 Agent Loop 的本质——一个**循环**，直到模型认为任务完成（不再请求工具）。

### 安全机制：最大迭代次数

为防止无限循环，需要设置最大迭代次数。在 hermes-agent 中：
- `HermesAgentLoop` 的 `max_turns` 参数默认为 30
- `AIAgent` 的 `IterationBudget` 类追踪迭代预算

### hermes-agent 中的对应实现

- `environments/agent_loop.py` 的 `HermesAgentLoop.run()` — 可复用的多轮工具调用引擎
- `run_agent.py` 的 `AIAgent.run_conversation()` — 完整的对话管理（含错误恢复、上下文压缩等）
- `model_tools.py` 的 `handle_function_call()` — 工具调用分发

## 📁 文件结构

```
ex03-multi-turn/
├── README.md          ← 你正在看的文件
├── agent_loop.py      ← 完整 Agent Loop（需要你填写 TODO）
└── mock_client.py     ← mock 替代方案
```

## 🔧 你需要做什么

打开 `agent_loop.py`，完成所有 TODO：

1. **TODO 1**：实现主循环结构（while 循环 + 迭代计数）
2. **TODO 2**：调用 API 并获取 assistant 消息
3. **TODO 3**：判断循环终止条件（无 tool_calls 时退出）
4. **TODO 4**：解析并执行所有 tool_calls，将结果加入 messages
5. **TODO 5**：实现最大迭代次数保护

## ✅ 验证方法

```bash
# 使用 mock 运行
python agent_loop.py --mock

# 期望输出类似：
# 👤 用户：比较北京和上海的天气，然后计算 25 + 28
# --- 第 1 轮 ---
# 🔧 调用工具：get_weather({"city": "北京"})
# 🔧 调用工具：get_weather({"city": "上海"})
# --- 第 2 轮 ---
# 🔧 调用工具：calculate({"expression": "25 + 28"})
# --- 第 3 轮 ---
# 🤖 Agent 回复：北京今天晴 25°C，上海多云 28°C，两地气温之和为 53°C。
#
# 📊 统计：共 3 轮对话
```

## 📖 hermes-agent 源码参考

- **Agent Loop**：`hermes-agent/environments/agent_loop.py`
  - `HermesAgentLoop.run()` — 核心循环逻辑
  - `AgentResult` — 循环结果数据结构
  - `ToolError` — 工具错误记录
- **工具编排**：`hermes-agent/model_tools.py`
  - `handle_function_call()` — 工具调用分发
- **迭代预算**：`hermes-agent/run_agent.py`
  - `IterationBudget` — 迭代次数管理
- **Agentic Design Patterns**：第 5 章（工具使用）、附录 F（推理引擎内部机制）

## 🎯 扩展挑战（可选）

1. 支持并行工具调用（模型一次返回多个 tool_calls 时同时执行）
2. 添加工具执行错误处理（工具失败时将错误信息回传给模型）
3. 添加对话历史的 token 计数，当接近上限时发出警告
4. 实现交互式模式：循环接收用户输入，支持多轮人机对话
