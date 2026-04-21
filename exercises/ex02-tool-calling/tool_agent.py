"""
练习 2（第二步）：带工具调用的 Agent

目标：实现单次工具调用循环 —— 模型请求工具 → 执行工具 → 结果回传 → 模型生成最终回复。
参考：hermes-agent/run_agent.py 中 _execute_tool_calls() 和 run_conversation() 的逻辑。

运行方式：
    python tool_agent.py --mock           # 使用 mock
    python tool_agent.py                  # 使用真实 API
    python tool_agent.py --message "..."  # 自定义消息
"""

import argparse
import json
import sys

from tool_registry import ToolRegistry


# ============================================================================
# 系统提示词
# ============================================================================

SYSTEM_PROMPT = (
    "你是一个智能 AI 助手，可以使用工具来帮助用户。"
    "当用户询问天气时，请使用 get_weather 工具获取信息。"
    "当用户需要计算时，请使用 calculate 工具。"
    "请根据工具返回的结果，用自然语言回答用户。"
)


# ============================================================================
# 工具定义
# ============================================================================

def get_weather(city: str) -> str:
    """获取指定城市的天气信息（模拟实现）。"""
    weather_data = {
        "北京": "北京今天晴，气温 25°C，空气质量良好。",
        "上海": "上海今天多云，气温 28°C，湿度较高。",
        "深圳": "深圳今天阵雨，气温 30°C，注意带伞。",
    }
    return weather_data.get(city, f"{city}的天气数据暂不可用。")


def calculate(expression: str) -> str:
    """计算数学表达式（简单实现）。"""
    try:
        # 安全限制：只允许数字和基本运算符
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符。"
        result = eval(expression)  # 仅用于教学，生产环境不应使用 eval
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"


# 工具 schema 定义
TOOL_SCHEMAS = [
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
                        "description": "城市名称，如'北京'、'上海'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
]


# ============================================================================
# 核心函数
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


def setup_registry() -> ToolRegistry:
    """创建并注册所有工具。"""
    registry = ToolRegistry()
    registry.register("get_weather", TOOL_SCHEMAS[0], get_weather)
    registry.register("calculate", TOOL_SCHEMAS[1], calculate)
    return registry


def chat_with_tools(client, registry: ToolRegistry, user_message: str) -> str:
    """
    带工具调用的单轮对话。

    完整流程：
    1. 构建 messages，附带工具 schema 调用 API
    2. 检查模型是否请求了工具调用
    3. 如果是 → 执行工具 → 将结果回传 → 再次调用 API 获取最终回复
    4. 如果否 → 直接返回模型回复

    在 hermes-agent 中，这个流程在 run_conversation() 中实现，
    支持多轮工具调用、并行执行、错误恢复等高级特性。
    这里我们只实现最基础的单次工具调用。

    参数：
        client: API 客户端
        registry: 工具注册表
        user_message: 用户消息

    返回：
        Agent 的最终回复
    """
    # 构建初始 messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # ------------------------------------------------------------------
    # TODO 4：调用 API，传入工具 schema
    # ------------------------------------------------------------------
    # 提示：使用 registry.get_definitions() 获取工具 schema 列表，
    #   然后传给 API 的 tools 参数：
    #
    #   tools = registry.get_definitions()
    #   response = client.chat.completions.create(
    #       model="gpt-4o-mini",
    #       messages=messages,
    #       tools=tools,           # ← 关键：传入工具定义
    #       temperature=0.7,
    #   )
    # ------------------------------------------------------------------
    tools = []       # ← 替换：使用 registry.get_definitions()
    response = None  # ← 替换：调用 API，传入 tools 参数

    if response is None:
        return "⚠️ API 未调用 — 请完成 TODO 4（调用 API 并传入工具 schema）"

    assistant_message = response.choices[0].message

    # ------------------------------------------------------------------
    # TODO 5：检测模型是否请求了工具调用
    # ------------------------------------------------------------------
    # 提示：检查 assistant_message.tool_calls 是否存在且非空
    #
    #   if assistant_message.tool_calls:
    #       # 模型请求了工具调用，进入工具执行流程
    #       ...
    #   else:
    #       # 模型直接回复，无需工具调用
    #       return assistant_message.content
    #
    # 在 hermes-agent 中，finish_reason == "tool_calls" 也用于判断。
    # ------------------------------------------------------------------
    has_tool_calls = False  # ← 替换：检查 assistant_message.tool_calls

    if not has_tool_calls:
        return assistant_message.content or ""

    # ------------------------------------------------------------------
    # TODO 6：解析 tool_call 并执行工具
    # ------------------------------------------------------------------
    # 提示：遍历 assistant_message.tool_calls，对每个 tool_call：
    #   1. 获取工具名称：tool_call.function.name
    #   2. 解析参数：json.loads(tool_call.function.arguments)
    #   3. 调用 registry.dispatch(name, arguments) 执行工具
    #   4. 打印工具调用信息（方便调试）
    #
    # 示例：
    #   for tool_call in assistant_message.tool_calls:
    #       name = tool_call.function.name
    #       arguments = json.loads(tool_call.function.arguments)
    #       print(f"🔧 调用工具：{name}({json.dumps(arguments, ensure_ascii=False)})")
    #       result = registry.dispatch(name, arguments)
    #       print(f"📎 工具结果：{result}")
    # ------------------------------------------------------------------

    # 将 assistant 消息（含 tool_calls）加入 messages
    # 注意：必须将 assistant 的原始消息加入，API 需要看到完整的对话历史
    messages.append({
        "role": "assistant",
        "content": assistant_message.content or "",
        "tool_calls": [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
            }
            for tc in assistant_message.tool_calls
        ]
    })

    # ------------------------------------------------------------------
    # TODO 7：将工具结果回传给模型
    # ------------------------------------------------------------------
    # 提示：对每个 tool_call，添加一条 role="tool" 的消息：
    #
    #   for tool_call in assistant_message.tool_calls:
    #       name = tool_call.function.name
    #       arguments = json.loads(tool_call.function.arguments)
    #       result = registry.dispatch(name, arguments)
    #       messages.append({
    #           "role": "tool",
    #           "tool_call_id": tool_call.id,
    #           "content": result,
    #       })
    #
    # 然后再次调用 API 获取最终回复：
    #   final_response = client.chat.completions.create(
    #       model="gpt-4o-mini",
    #       messages=messages,
    #       temperature=0.7,
    #   )
    #   return final_response.choices[0].message.content
    #
    # 在 hermes-agent 中，工具结果通过 _execute_tool_calls() 处理，
    # 支持并行执行和错误恢复。
    # ------------------------------------------------------------------
    return ""  # ← 替换：添加工具结果消息，再次调用 API，返回最终回复


# ============================================================================
# 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="练习 2：工具调用基础")
    parser.add_argument("--mock", action="store_true", help="使用 mock 客户端")
    parser.add_argument("--message", type=str, default="北京今天天气怎么样？",
                        help="用户消息")
    args = parser.parse_args()

    client = create_client(use_mock=args.mock)
    registry = setup_registry()

    print(f"👤 用户：{args.message}")
    reply = chat_with_tools(client, registry, args.message)
    print(f"🤖 Agent 回复：{reply}")


if __name__ == "__main__":
    main()
