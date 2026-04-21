"""
Mock 客户端 — 模拟多轮工具调用的 OpenAI Chat Completions API 响应。

模拟场景：模型可能在多轮中连续调用不同工具，最终生成综合回复。
"""

import json
import re


class MockFunctionCall:
    """模拟 tool_call 中的 function 对象。"""

    def __init__(self, name: str, arguments: str):
        self.name = name
        self.arguments = arguments


class MockToolCall:
    """模拟 tool_call 对象。"""

    _counter = 0

    def __init__(self, name: str, arguments: dict):
        MockToolCall._counter += 1
        self.id = f"call_mock_{MockToolCall._counter:03d}"
        self.type = "function"
        self.function = MockFunctionCall(
            name, json.dumps(arguments, ensure_ascii=False)
        )


class MockMessage:
    """模拟 message 对象。"""

    def __init__(self, content: str = None, role: str = "assistant",
                 tool_calls: list = None):
        self.content = content
        self.role = role
        self.tool_calls = tool_calls


class MockChoice:
    """模拟 choice 对象。"""

    def __init__(self, message: MockMessage, finish_reason: str = "stop"):
        self.message = message
        self.finish_reason = finish_reason
        self.index = 0


class MockUsage:
    """模拟 usage 对象。"""

    def __init__(self):
        self.prompt_tokens = 150
        self.completion_tokens = 80
        self.total_tokens = 230


class MockCompletion:
    """模拟 Chat Completions API 响应。"""

    def __init__(self, message: MockMessage, finish_reason: str = "stop"):
        self.id = "mock-completion-003"
        self.object = "chat.completion"
        self.model = "mock-gpt-4o-mini"
        self.choices = [MockChoice(message, finish_reason)]
        self.usage = MockUsage()


class MockCompletions:
    """
    模拟 client.chat.completions 接口。

    行为逻辑：
    - 分析 messages 中已有的 tool 结果，决定是否需要更多工具调用
    - 当所有需要的信息都已获取时，生成最终综合回复
    """

    def _extract_user_message(self, messages: list) -> str:
        """提取最初的用户消息。"""
        for msg in messages:
            if msg.get("role") == "user":
                return msg.get("content", "")
        return ""

    def _get_completed_tools(self, messages: list) -> dict:
        """收集已完成的工具调用结果。"""
        results = {}
        for msg in messages:
            if msg.get("role") == "tool":
                tool_call_id = msg.get("tool_call_id", "")
                results[tool_call_id] = msg.get("content", "")
        return results

    def _get_called_tool_names(self, messages: list) -> list:
        """收集已调用过的工具名称。"""
        names = []
        for msg in messages:
            if msg.get("role") == "assistant" and msg.get("tool_calls"):
                for tc in msg["tool_calls"]:
                    if isinstance(tc, dict):
                        names.append(tc.get("function", {}).get("name", ""))
                    else:
                        names.append(tc.function.name)
        return names

    def _plan_tool_calls(self, user_message: str, called_names: list) -> list:
        """根据用户消息和已调用的工具，规划下一批工具调用。"""
        planned = []

        # 检测需要天气查询的城市
        cities = ["北京", "上海", "深圳", "广州", "杭州"]
        for city in cities:
            if city in user_message:
                # 检查是否已经查询过这个城市
                already_called = False
                for name in called_names:
                    if name == "get_weather":
                        already_called = True
                        break
                if not already_called or called_names.count("get_weather") < user_message.count(city):
                    planned.append(
                        MockToolCall("get_weather", {"city": city})
                    )

        # 去重：如果已经调用过相同参数的工具，跳过
        # 简化处理：按城市去重
        seen_cities = set()
        for name in called_names:
            # 从 messages 中找到对应的参数
            pass  # 简化处理

        # 检测需要计算
        calc_keywords = ["计算", "算", "+", "-", "*", "/", "等于"]
        if any(kw in user_message for kw in calc_keywords):
            if "calculate" not in called_names:
                # 提取数学表达式
                expression = ""
                # 尝试从用户消息中提取数字和运算符
                parts = re.findall(r'[\d.]+\s*[+\-*/]\s*[\d.]+', user_message)
                if parts:
                    expression = parts[0]
                else:
                    expression = "".join(
                        c for c in user_message if c in "0123456789+-*/.() "
                    ).strip()
                if expression:
                    planned.append(
                        MockToolCall("calculate", {"expression": expression})
                    )

        # 检测需要时间查询
        time_keywords = ["时间", "几点", "现在"]
        if any(kw in user_message for kw in time_keywords):
            if "get_time" not in called_names:
                planned.append(
                    MockToolCall("get_time", {"timezone": "Asia/Shanghai"})
                )

        return planned

    def create(self, model: str = "gpt-4o-mini", messages: list = None,
               tools: list = None, temperature: float = 0.7,
               **kwargs) -> MockCompletion:
        """模拟多轮工具调用的 API 响应。"""
        messages = messages or []
        user_message = self._extract_user_message(messages)
        tool_results = self._get_completed_tools(messages)
        called_names = self._get_called_tool_names(messages)

        # 规划需要的工具调用
        planned = self._plan_tool_calls(user_message, called_names)

        if planned and tools:
            # 还有工具需要调用
            msg = MockMessage(content=None, tool_calls=planned)
            return MockCompletion(msg, finish_reason="tool_calls")

        # 所有工具调用完成，生成最终回复
        if tool_results:
            results_text = "；".join(tool_results.values())
            reply = f"综合以上信息：{results_text} 希望这些信息对你有帮助！"
        else:
            reply = "这个问题我可以直接回答，不需要使用工具。请问你想了解什么？"

        return MockCompletion(MockMessage(content=reply))


class MockChat:
    """模拟 client.chat 接口。"""

    def __init__(self):
        self.completions = MockCompletions()


class MockOpenAI:
    """模拟 OpenAI 客户端（支持多轮工具调用）。"""

    def __init__(self, api_key: str = "mock-key", **kwargs):
        self.chat = MockChat()
        self.api_key = api_key
