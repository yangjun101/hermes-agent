"""
Mock 客户端 — 模拟 OpenAI Chat Completions API 的响应。

无需真实 API key 即可运行练习。响应格式与 OpenAI API 完全一致。
"""


class MockMessage:
    """模拟 API 响应中的 message 对象。"""

    def __init__(self, content: str, role: str = "assistant"):
        self.content = content
        self.role = role
        self.tool_calls = None


class MockChoice:
    """模拟 API 响应中的 choice 对象。"""

    def __init__(self, message: MockMessage, finish_reason: str = "stop"):
        self.message = message
        self.finish_reason = finish_reason
        self.index = 0


class MockUsage:
    """模拟 API 响应中的 usage 对象。"""

    def __init__(self):
        self.prompt_tokens = 42
        self.completion_tokens = 28
        self.total_tokens = 70


class MockCompletion:
    """模拟 Chat Completions API 的响应对象。"""

    def __init__(self, content: str):
        self.id = "mock-completion-001"
        self.object = "chat.completion"
        self.model = "mock-gpt-4o-mini"
        self.choices = [MockChoice(MockMessage(content))]
        self.usage = MockUsage()


class MockCompletions:
    """模拟 client.chat.completions 接口。"""

    # 预定义的回复映射
    RESPONSES = {
        "你好": "你好！我是一个 AI 助手，很高兴认识你。有什么我可以帮助你的吗？",
        "介绍": "我是一个智能 AI 助手，可以回答问题、编写代码、分析信息等。我用中文与你交流，力求简洁有用。",
        "default": "这是一个很好的问题！作为 AI 助手，我会尽力帮助你。请告诉我更多细节，我可以提供更具体的帮助。",
    }

    def create(self, model: str = "gpt-4o-mini", messages: list = None,
               temperature: float = 0.7, **kwargs) -> MockCompletion:
        """
        模拟 Chat Completions API 的 create 方法。

        根据用户消息内容返回预定义的回复。
        """
        # 提取最后一条用户消息
        user_message = ""
        if messages:
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    user_message = msg.get("content", "")
                    break

        # 匹配预定义回复
        reply = self.RESPONSES["default"]
        for keyword, response in self.RESPONSES.items():
            if keyword != "default" and keyword in user_message:
                reply = response
                break

        return MockCompletion(reply)


class MockChat:
    """模拟 client.chat 接口。"""

    def __init__(self):
        self.completions = MockCompletions()


class MockOpenAI:
    """
    模拟 OpenAI 客户端。

    使用方式与真实客户端完全一致：
        client = MockOpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[...],
        )
        print(response.choices[0].message.content)
    """

    def __init__(self, api_key: str = "mock-key", **kwargs):
        self.chat = MockChat()
        self.api_key = api_key
