"""
练习 3：多轮对话循环 — 完整的 Agent Loop

目标：实现一个支持多轮工具调用的 Agent Loop。
      模型可以连续调用多个工具，直到认为任务完成后自然停止。

参考：
    - hermes-agent/environments/agent_loop.py 中 HermesAgentLoop.run()
    - hermes-agent/run_agent.py 中 AIAgent.run_conversation()

运行方式：
    python agent_loop.py --mock
    python agent_loop.py
    python agent_loop.py --message "比较北京和上海的天气"
"""

import argparse
import json
import sys
from typing import List, Dict, Any, Optional


# ============================================================================
# 系统提示词
# ============================================================================

SYSTEM_PROMPT = (
    "你是一个智能 AI 助手，可以使用工具来帮助用户。"
    "你可以连续调用多个工具来完成复杂任务。"
    "当你获得了足够的信息后，请用自然语言综合回答用户。"
)

# 最大迭代次数（防止无限循环）
# 在 hermes-agent 中，HermesAgentLoop 的 max_turns 默认为 30
MAX_ITERATIONS = 10


# ============================================================================
# 工具定义（复用练习 2 的工具）
# ============================================================================

def get_weather(city: str) -> str:
    """获取指定城市的天气信息。"""
    weather_data = {
        "北京": "北京今天晴，气温 25°C，空气质量良好。",
        "上海": "上海今天多云，气温 28°C，湿度较高。",
        "深圳": "深圳今天阵雨，气温 30°C，注意带伞。",
        "广州": "广州今天多云转晴，气温 29°C。",
        "杭州": "杭州今天小雨，气温 22°C。",
    }
    return weather_data.get(city, f"{city}的天气数据暂不可用。")


def calculate(expression: str) -> str:
    """计算数学表达式。"""
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符。"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"


def get_time(timezone: str = "Asia/Shanghai") -> str:
    """获取指定时区的当前时间（模拟）。"""
    times = {
        "Asia/Shanghai": "2025-01-15 14:30:00 CST",
        "America/New_York": "2025-01-15 01:30:00 EST",
        "Europe/London": "2025-01-15 06:30:00 GMT",
    }
    return times.get(timezone, f"{timezone} 时区的时间数据暂不可用。")


# 工具注册表（简化版，直接使用字典）
TOOLS = {
    "get_weather": {
        "handler": get_weather,
        "schema": {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "城市名称"}
                    },
                    "required": ["city"]
                }
            }
        }
    },
    "calculate": {
        "handler": calculate,
        "schema": {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "计算数学表达式",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "数学表达式"}
                    },
                    "required": ["expression"]
                }
            }
        }
    },
    "get_time": {
        "handler": get_time,
        "schema": {
            "type": "function",
            "function": {
                "name": "get_time",
                "description": "获取指定时区的当前时间",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "时区名称，如 Asia/Shanghai",
                            "default": "Asia/Shanghai"
                        }
                    },
                    "required": []
                }
            }
        }
    },
}


def get_tool_schemas() -> List[dict]:
    """获取所有工具的 schema 列表。"""
    return [tool["schema"] for tool in TOOLS.values()]


def dispatch_tool(name: str, arguments: dict) -> str:
    """分发工具调用。"""
    if name not in TOOLS:
        return f"错误：未知工具 '{name}'"
    return TOOLS[name]["handler"](**arguments)


# ============================================================================
# 核心：Agent Loop
# ============================================================================

def create_client(use_mock: bool = False):
    """创建 API 客户端。"""
    if use_mock:
        from mock_client import MockOpenAI
        return MockOpenAI()
    try:
        from openai import OpenAI
    except ImportError:
        print("❌ 请先安装 openai 库：pip install openai")
        sys.exit(1)
    return OpenAI()


def run_agent_loop(client, user_message: str) -> str:
    """
    运行完整的 Agent Loop。

    这是本练习的核心函数。它实现了 hermes-agent 中 HermesAgentLoop.run()
    的简化版本：

    1. 构建初始 messages（system + user）
    2. 进入循环：
       a. 调用 API（附带工具 schema）
       b. 如果模型返回 tool_calls → 执行工具，将结果加入 messages，继续循环
       c. 如果模型不返回 tool_calls → 任务完成，返回回复
    3. 如果达到最大迭代次数 → 强制停止

    参数：
        client: API 客户端
        user_message: 用户消息

    返回：
        Agent 的最终回复文本
    """
    # 初始化 messages
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    tool_schemas = get_tool_schemas()
    iteration = 0

    # ------------------------------------------------------------------
    # TODO 1：实现主循环结构
    # ------------------------------------------------------------------
    # 提示：使用 while 循环，条件为 iteration < MAX_ITERATIONS
    #
    #   while iteration < MAX_ITERATIONS:
    #       iteration += 1
    #       print(f"\n--- 第 {iteration} 轮 ---")
    #
    #       ... (TODO 2-4 的代码放在循环内)
    #
    # 在 hermes-agent 中，HermesAgentLoop.run() 使用：
    #   for turn in range(self.max_turns):
    # ------------------------------------------------------------------

    # ↓↓↓ 将以下代码包裹在 while 循环中 ↓↓↓

    # ------------------------------------------------------------------
    # TODO 2：调用 API 并获取 assistant 消息
    # ------------------------------------------------------------------
    # 提示：
    #   response = client.chat.completions.create(
    #       model="gpt-4o-mini",
    #       messages=messages,
    #       tools=tool_schemas,
    #       temperature=0.7,
    #   )
    #   assistant_message = response.choices[0].message
    # ------------------------------------------------------------------
    response = None  # ← 替换
    if response is None:
        return "⚠️ API 未调用 — 请完成 TODO 1 和 TODO 2"
    assistant_message = response.choices[0].message

    # ------------------------------------------------------------------
    # TODO 3：判断循环终止条件
    # ------------------------------------------------------------------
    # 提示：如果 assistant_message 没有 tool_calls，说明模型认为任务完成
    #
    #   if not assistant_message.tool_calls:
    #       # 模型自然停止，返回回复
    #       print(f"\n📊 统计：共 {iteration} 轮对话")
    #       return assistant_message.content or ""
    #
    # 在 hermes-agent 中，还会检查 finish_reason 和其他终止条件。
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # TODO 4：解析并执行所有 tool_calls，将结果加入 messages
    # ------------------------------------------------------------------
    # 提示：
    #   1. 先将 assistant 消息（含 tool_calls）加入 messages
    #   2. 遍历每个 tool_call，执行工具并将结果作为 tool 消息加入
    #
    #   # 步骤 1：加入 assistant 消息
    #   messages.append({
    #       "role": "assistant",
    #       "content": assistant_message.content or "",
    #       "tool_calls": [
    #           {
    #               "id": tc.id,
    #               "type": "function",
    #               "function": {
    #                   "name": tc.function.name,
    #                   "arguments": tc.function.arguments,
    #               }
    #           }
    #           for tc in assistant_message.tool_calls
    #       ]
    #   })
    #
    #   # 步骤 2：执行每个工具并加入结果
    #   for tool_call in assistant_message.tool_calls:
    #       name = tool_call.function.name
    #       arguments = json.loads(tool_call.function.arguments)
    #       print(f"🔧 调用工具：{name}({json.dumps(arguments, ensure_ascii=False)})")
    #
    #       result = dispatch_tool(name, arguments)
    #       print(f"   📎 结果：{result}")
    #
    #       messages.append({
    #           "role": "tool",
    #           "tool_call_id": tool_call.id,
    #           "content": result,
    #       })
    #
    # 在 hermes-agent 中，_execute_tool_calls() 还支持并行执行和错误恢复。
    # ------------------------------------------------------------------

    # ↑↑↑ 以上代码应在 while 循环内 ↑↑↑

    # ------------------------------------------------------------------
    # TODO 5：最大迭代次数保护
    # ------------------------------------------------------------------
    # 提示：如果循环正常退出（达到 MAX_ITERATIONS），返回警告信息
    #
    #   # 这段代码放在 while 循环之后
    #   print(f"\n⚠️ 达到最大迭代次数 ({MAX_ITERATIONS})，强制停止")
    #   return f"[达到最大迭代次数 {MAX_ITERATIONS}，任务可能未完成]"
    #
    # 在 hermes-agent 中，_handle_max_iterations() 处理这种情况，
    # 会尝试让模型生成一个总结性回复。
    # ------------------------------------------------------------------

    return ""


# ============================================================================
# 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="练习 3：多轮对话循环")
    parser.add_argument("--mock", action="store_true", help="使用 mock 客户端")
    parser.add_argument(
        "--message", type=str,
        default="比较北京和上海的天气，然后计算 25 + 28",
        help="用户消息"
    )
    args = parser.parse_args()

    client = create_client(use_mock=args.mock)

    print(f"👤 用户：{args.message}")
    reply = run_agent_loop(client, args.message)
    print(f"\n🤖 Agent 回复：{reply}")


if __name__ == "__main__":
    main()
