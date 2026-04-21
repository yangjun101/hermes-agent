# hermes-agent 技术分析文档

> 基于 hermes-agent 源码的深度逆向分析，按 Agentic Design Patterns 章节结构组织

## 📖 阅读指南

本文档系列对 [hermes-agent](https://github.com/NousResearch/hermes-agent) 的源码进行深度分析，并将其设计决策映射到 *Agentic Design Patterns* 一书的理论框架。每个章节遵循统一模板：

```
概述 → 源码分析 → 架构图（Mermaid） → Agentic Design Patterns 映射 → 小结
```

建议按章节顺序阅读。第 0 章提供整体架构鸟瞰，后续章节逐层深入。

## 📑 目录

| 章节 | 标题 | 核心源码 | 设计模式映射 |
|------|------|----------|-------------|
| [Ch0](ch00-architecture-overview.md) | 整体架构概览 | 全部模块 | 全书概览 |
| [Ch1](ch01-prompt-engineering.md) | Prompt Engineering | prompt_builder.py, prompt_caching.py, context_references.py | Ch1 提示链, 附录A |
| [Ch2](ch02-agent-loop.md) | Agent Loop | run_agent.py, agent_loop.py, model_tools.py | Ch5 工具使用, 附录F |
| [Ch3](ch03-context-engine.md) | Context Engine | context_engine.py, context_compressor.py | Ch16 资源感知优化 |
| [Ch4](ch04-memory-management.md) | Memory 管理 | memory_manager.py, memory_provider.py, hermes_state.py | Ch8 记忆管理 |
| [Ch5](ch05-tool-system.md) | 工具系统 | registry.py, toolsets.py, model_tools.py, 40+ 工具 | Ch5 工具使用, Ch10 MCP |
| [Ch6](ch06-routing-and-resilience.md) | 路由与容错 | smart_model_routing.py, error_classifier.py, retry_utils.py, credential_pool.py | Ch2 路由, Ch12 异常处理 |
| [Ch7](ch07-multi-agent-collaboration.md) | 多智能体协作 | delegate_tool.py | Ch3 并行化, Ch6 规划, Ch7 多智能体 |
| [Ch8](ch08-security-and-guardrails.md) | 安全与护栏 | prompt_builder.py, context_references.py, memory_manager.py | Ch18 护栏, Ch13 人机协同 |
| [Ch9](ch09-other-patterns.md) | 其他设计模式 | skill_utils.py, trajectory_compressor.py, anthropic_adapter.py, insights.py, usage_pricing.py, clarify_tool.py | Ch4, Ch9, Ch11, Ch13, Ch17, Ch19 |

## 🏗️ hermes-agent 七层架构速览

```
┌─────────────────────────────────────────────────┐
│  第 7 层：子代理层 (Sub-Agent)                    │
│  delegate_tool.py                                │
├─────────────────────────────────────────────────┤
│  第 6 层：路由与容错层 (Routing & Resilience)      │
│  smart_model_routing.py, error_classifier.py,    │
│  retry_utils.py, credential_pool.py              │
├─────────────────────────────────────────────────┤
│  第 5 层：工具系统层 (Tool System)                 │
│  registry.py, toolsets.py, model_tools.py,       │
│  tools/*.py (40+ 工具)                           │
├─────────────────────────────────────────────────┤
│  第 4 层：记忆管理层 (Memory Management)           │
│  memory_manager.py, memory_provider.py,          │
│  hermes_state.py                                 │
├─────────────────────────────────────────────────┤
│  第 3 层：上下文引擎层 (Context Engine)            │
│  context_engine.py, context_compressor.py        │
├─────────────────────────────────────────────────┤
│  第 2 层：Prompt 工程层 (Prompt Engineering)       │
│  prompt_builder.py, prompt_caching.py,           │
│  context_references.py                           │
├─────────────────────────────────────────────────┤
│  第 1 层：核心引擎层 (Core Engine)                 │
│  run_agent.py, agent_loop.py, model_tools.py     │
└─────────────────────────────────────────────────┘
```

## 📚 参考资源

- **hermes-agent 源码**：`hermes-agent/` 目录
- **Agentic Design Patterns**：`agentic-design-patterns-main/` 目录
- **渐进式练习课程**：`exercises/` 目录
