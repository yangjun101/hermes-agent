# hermes-agent 渐进式练习课程

> 从零到一构建 AI Agent 框架 — 12 个练习，4 个阶段

## 📖 课程简介

本课程通过 12 个渐进式练习，引导你从最简单的单轮 LLM 对话开始，逐步构建一个功能完整的 AI Agent 框架。每个练习独立可运行，并提供 mock 替代方案（无需真实 API key）。

课程设计采用"洋葱模型"——每个练习在前一个练习的基础上增加一层能力，但代码框架独立可运行。

## 🎯 前置要求

- **Python 基础**：熟悉 Python 3.10+ 语法、类、装饰器、异步编程基础
- **API 概念**：了解 HTTP API 调用、JSON 数据格式
- **OpenAI 兼容 API**：了解 Chat Completions API 的基本格式（messages、tools、tool_calls）

## 🗺️ 学习路径

### 第一阶段：基础阶段（练习 1-3）

掌握 AI Agent 的核心骨架：LLM 调用、工具调用、多轮对话循环。

| 练习 | 标题 | 学习目标 | hermes-agent 参考 | 设计模式 |
|------|------|----------|-------------------|----------|
| [练习 1](ex01-hello-agent/) | Hello Agent | 实现最简单的单轮 LLM 对话 | run_agent.py | — |
| [练习 2](ex02-tool-calling/) | 工具调用基础 | 实现工具注册表和单次工具调用 | registry.py, toolsets.py | Ch5 工具使用 |
| [练习 3](ex03-multi-turn/) | 多轮对话循环 | 实现完整的 Agent Loop | agent_loop.py, model_tools.py | Ch5, 附录F |

### 第二阶段：中级阶段（练习 4-6）

学习 Prompt 工程、上下文管理和记忆系统。

| 练习 | 标题 | 学习目标 | hermes-agent 参考 | 设计模式 |
|------|------|----------|-------------------|----------|
| [练习 4](ex04-prompt-engineering/) | Prompt 工程 | 实现模块化系统提示词组装和注入检测 | prompt_builder.py | Ch1 提示链, 附录A |
| [练习 5](ex05-context-compression/) | 上下文压缩 | 实现上下文引擎和默认压缩器 | context_engine.py, context_compressor.py | Ch16 资源感知优化 |
| [练习 6](ex06-memory-system/) | 记忆系统 | 实现记忆提供者和跨会话记忆 | memory_manager.py, memory_provider.py | Ch8 记忆管理 |

### 第三阶段：高级阶段（练习 7-9）

掌握错误处理、子代理委托和安全护栏。

| 练习 | 标题 | 学习目标 | hermes-agent 参考 | 设计模式 |
|------|------|----------|-------------------|----------|
| [练习 7](ex07-error-handling/) | 错误分类与重试 | 实现错误分类器和抖动退避重试 | error_classifier.py, retry_utils.py | Ch12 异常处理 |
| [练习 8](ex08-sub-agents/) | 子代理委托 | 实现隔离上下文和并行执行 | delegate_tool.py | Ch3 并行化, Ch7 多智能体 |
| [练习 9](ex09-guardrails/) | 安全护栏 | 实现注入检测、敏感过滤和上下文围栏 | prompt_builder.py, context_references.py | Ch18 护栏 |

### 第四阶段：整合阶段（练习 10-12）

将所有模块整合为完整框架，并学习生产级优化。

| 练习 | 标题 | 学习目标 | hermes-agent 参考 | 设计模式 |
|------|------|----------|-------------------|----------|
| [练习 10](ex10-smart-routing/) | 智能路由 | 实现简单消息检测和模型路由 | smart_model_routing.py | Ch2 路由 |
| [练习 11](ex11-framework-integration/) | 框架整合 | 整合全部模块为完整 Agent 框架 | run_agent.py（完整版） | 全书 |
| [练习 12](ex12-production-optimization/) | 生产级优化 | 实现提示缓存、凭证池、成本追踪 | prompt_caching.py, credential_pool.py, insights.py | Ch16, Ch19 |

## 📊 复杂度递增

```
练习 1  ★☆☆☆☆  单轮对话
练习 2  ★★☆☆☆  工具调用
练习 3  ★★☆☆☆  多轮循环
练习 4  ★★★☆☆  Prompt 工程
练习 5  ★★★☆☆  上下文压缩
练习 6  ★★★☆☆  记忆系统
练习 7  ★★★★☆  错误处理
练习 8  ★★★★☆  子代理
练习 9  ★★★★☆  安全护栏
练习 10 ★★★★☆  智能路由
练习 11 ★★★★★  框架整合
练习 12 ★★★★★  生产优化
```

## 🔧 运行方式

每个练习目录包含：
- `README.md` — 学习目标、核心概念、验证方法
- 代码框架文件（含 `TODO` 标记）
- `mock_client.py` — mock 替代方案（无需真实 API key）

```bash
# 进入练习目录
cd exercises/ex01-hello-agent/

# 使用 mock 运行
python hello_agent.py --mock

# 使用真实 API 运行（需要 API key）
export OPENAI_API_KEY="your-key"
python hello_agent.py
```

## 📚 参考资源

- **hermes-agent 技术分析文档**：`docs/` 目录
- **hermes-agent 源码**：`hermes-agent/` 目录
- **Agentic Design Patterns**：`agentic-design-patterns-main/` 目录
