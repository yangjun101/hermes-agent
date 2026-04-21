# 练习 2：工具调用基础 — 让 Agent 使用工具

## 🎯 学习目标

1. 理解 Function Calling（工具调用）的完整流程
2. 理解工具 schema（JSON Schema）如何描述工具的参数
3. 实现一个简化版的工具注册表（ToolRegistry）
4. 实现单次工具调用循环：模型请求工具 → 执行工具 → 返回结果

## 📋 前置知识

- 完成练习 1（Hello Agent）
- 了解 JSON Schema 基本格式
- 了解 Python 字典和函数作为一等公民的概念

## 💡 核心概念

### 什么是工具调用（Function Calling）？

LLM 本身只能生成文本，但通过工具调用机制，它可以"请求"执行外部函数。流程如下：

```
用户消息 → LLM 判断需要工具 → 返回 tool_calls → 程序执行工具 → 结果回传给 LLM → LLM 生成最终回复
```

### 工具 Schema

每个工具需要一个 JSON Schema 来描述它的名称、功能和参数：

```python
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如'北京'"
                }
            },
            "required": ["city"]
        }
    }
}
```

### hermes-agent 中的对应实现

在 hermes-agent 中：
- `tools/registry.py` 的 `ToolRegistry` 类管理所有工具的注册和分发
- `ToolEntry` 数据类存储工具的元数据（名称、schema、处理函数）
- `ToolRegistry.register()` 注册工具
- `ToolRegistry.get_definitions()` 获取工具 schema 列表
- `ToolRegistry.dispatch()` 根据名称分发工具调用

## 📁 文件结构

```
ex02-tool-calling/
├── README.md            ← 你正在看的文件
├── tool_registry.py     ← 简化版工具注册表（需要你填写 TODO）
├── tool_agent.py        ← 带工具调用的 Agent（需要你填写 TODO）
└── mock_client.py       ← mock 替代方案
```

## 🔧 你需要做什么

### 第一步：完成 `tool_registry.py`

实现简化版的工具注册表：
1. **TODO 1**：实现 `register()` 方法 — 将工具存入注册表
2. **TODO 2**：实现 `get_definitions()` 方法 — 返回所有工具的 schema 列表
3. **TODO 3**：实现 `dispatch()` 方法 — 根据工具名称调用对应的处理函数

### 第二步：完成 `tool_agent.py`

实现单次工具调用循环：
1. **TODO 4**：将工具 schema 传给 API 调用
2. **TODO 5**：检测模型是否请求了工具调用
3. **TODO 6**：解析 tool_call 并执行工具
4. **TODO 7**：将工具结果回传给模型

## ✅ 验证方法

```bash
# 使用 mock 运行
python tool_agent.py --mock

# 期望输出类似：
# 👤 用户：北京今天天气怎么样？
# 🔧 调用工具：get_weather({"city": "北京"})
# 📎 工具结果：北京今天晴，气温 25°C，空气质量良好。
# 🤖 Agent 回复：北京今天天气不错，晴天，气温 25°C，空气质量良好。适合外出活动！
```

## 📖 hermes-agent 源码参考

- **工具注册表**：`hermes-agent/tools/registry.py`
  - `ToolEntry` — 工具元数据
  - `ToolRegistry.register()` — 工具注册
  - `ToolRegistry.get_definitions()` — 获取 schema
  - `ToolRegistry.dispatch()` — 工具分发
- **工具集定义**：`hermes-agent/toolsets.py`
  - `_HERMES_CORE_TOOLS` — 核心工具列表
- **Agentic Design Patterns**：第 5 章（工具使用）

## 🎯 扩展挑战（可选）

1. 添加更多工具（如计算器、翻译器）
2. 实现工具参数验证（检查必填参数是否存在）
3. 实现工具执行错误处理（工具抛出异常时返回错误信息）
