"""
Mock 客户端 — 模拟带工具调用的 OpenAI Chat Completions API 响应。

模拟两种场景：
1. 模型请求工具调用（返回 tool_calls）
2. 模型直接回复（工具结果回传后的最终回复）
"""

import json


class MockFunctionCall:
    """模拟 tool_call 中的 function 对象。"""

    def __init__(self, name: str, arguments: str):
        self.name = name
        self.arguments = arguments


class MockToolCall:
    """模拟 API 响应中的 tool_call 对象。"""

    def __init__(self, call_id: str, name: str, arguments: dict):
        self.id = call_id
        self.type = "function"
        self.function = MockFunctionCall(name, json.dumps(arguments, ensure_ascii=False))


class MockMessage:
    """模拟 API 响应中的 message 对象。"""

    def __init__(self, content: str = None, role: str = "assistant",
                 tool_calls: list = None):
        self.content = content
        self.role = role
        self.tool_calls = tool_calls


class MockChoice:
    """模拟 API 响应中的 choice 对象。"""

    def __init__(self, message: MockMessage, finish_reason: str = "stop"):
        self.message = message
        self.finish_reason = finish_reason
        self.index = 0


class MockUsage:
    """模拟 usage 对象。"""

    def __init__(self):
        self.prompt_tokens = 100
        self.completion_tokens = 50
        self.total_tokens = 150


class MockCompletion:
    """模拟 Chat Completions API 的响应。"""

    def __init__(self, message: MockMessage, finish_reason: str = "stop"):
        self.id = "mock-completion-002"
        self.object = "chat.completion"
        self.model = "mock-gpt-4o-mini"
        self.choices = [MockChoice(message, finish_reason)]
        self.usage = MockUsage()


class MockCompletions:
    """模拟 client.chat.completions 接口。"""

    def __init__(self):
        self._call_count = 0

    def create(self, model: str = "gpt-4o-mini", messages: list = None,
               tools: list = None, temperature: float = 0.7, **kwargs) -> MockCompletion:
        """
        模拟 Chat Completions API。

        行为逻辑：
        - 第一次调用（有 tools 参数）：检查用户消息，决定是否返回 tool_calls
        - 第二次调用（有 tool 结果）：基于工具结果生成最终回复
        """
        self._call_count += 1

        # 检查是否有 tool 角色的消息（说明是第二次调用，工具结果已回传）
        has_tool_results = any(
            msg.get("role") == "tool" for msg in (messages or [])
        )

        if has_tool_results:
            # 第二次调用：基于工具结果生成最终回复
            tool_results = [
                msg.get("content", "") for msg in messages if msg.get("role") == "tool"
            ]
            combined = "；".join(tool_results)
            reply = f"根据查询结果：{combined} 希望这些信息对你有帮助！"
            return MockCompletion(MockMessage(content=reply))

        # 第一次调用：分析用户消息，决定是否调用工具
        user_message = ""
        for msg in reversed(messages or []):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # 检测是否需要天气工具
        weather_cities = ["北京", "上海", "深圳", "广州", "杭州", "成都"]
        for city in weather_cities:
            if city in user_message and ("天气" in user_message or "气温" in user_message):
                tool_call = MockToolCall(
                    call_id="call_mock_001",
                    name="get_weather",
                    arguments={"city": city},
                )
                msg = MockMessage(content=None, tool_calls=[tool_call])
                return MockCompletion(msg, finish_reason="tool_calls")

        # 检测是否需要计算工具
        calc_keywords = ["计算", "算", "等于", "+", "-", "*", "/"]
        if any(kw in user_message for kw in calc_keywords):
            # 尝试提取表达式
            expression = "".join(
                c for c in user_message if c in "0123456789+-*/.() "
            ).strip()
            if not expression:
                expression = "1 + 1"
            tool_call = MockToolCall(
                call_id="call_mock_002",
                name="calculate",
                arguments={"expression": expression},
            )
            msg = MockMessage(content=None, tool_calls=[tool_call])
            return MockCompletion(msg, finish_reason="tool_calls")

        # 不需要工具，直接回复
        return MockCompletion(
            MockMessage(content="这个问题我可以直接回答，不需要使用工具。")
        )


class MockChat:
    """模拟 client.chat 接口。"""

    def __init__(self):
        self.completions = MockCompletions()


class MockOpenAI:
    """模拟 OpenAI 客户端（支持工具调用）。"""

    def __init__(self, api_key: str = "mock-key", **kwargs):
        self.chat = MockChat()
        self.api_key = api_key
