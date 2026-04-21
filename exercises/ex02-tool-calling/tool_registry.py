"""
练习 2（第一步）：简化版工具注册表

参考：hermes-agent/tools/registry.py 中的 ToolRegistry 类。
hermes-agent 的注册表支持 AST 静态分析自动发现、线程安全、工具集组合等高级特性。
这里我们实现一个最简化的版本，只关注核心的注册、查询和分发功能。

运行方式：
    python tool_registry.py    # 运行自测
"""

import json
import sys
from typing import Callable, Dict, List, Optional, Any


class ToolRegistry:
    """
    简化版工具注册表。

    在 hermes-agent 中，ToolRegistry 是一个单例，管理 40+ 工具的注册和分发。
    它使用 ToolEntry 数据类存储每个工具的元数据（名称、schema、处理函数等）。

    这里我们简化为一个字典，key 是工具名称，value 包含 schema 和 handler。
    """

    def __init__(self):
        # 内部存储：{工具名称: {"schema": {...}, "handler": callable}}
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, schema: dict, handler: Callable) -> None:
        """
        注册一个工具。

        在 hermes-agent 中，ToolRegistry.register() 接收 ToolEntry 的所有字段
        （name, toolset, schema, handler, check_fn 等）。
        这里我们只需要 name、schema 和 handler。

        参数：
            name: 工具名称（如 "get_weather"）
            schema: 工具的 JSON Schema 定义（OpenAI function calling 格式）
            handler: 工具的处理函数，接收关键字参数，返回字符串结果

        示例：
            registry.register(
                name="get_weather",
                schema={"type": "function", "function": {"name": "get_weather", ...}},
                handler=get_weather_handler,
            )
        """
        # --------------------------------------------------------------
        # TODO 1：将工具存入 self._tools 字典
        # --------------------------------------------------------------
        # 提示：将 name 作为 key，将 schema 和 handler 打包为字典作为 value
        #   self._tools[name] = {"schema": schema, "handler": handler}
        # --------------------------------------------------------------
        pass  # ← 替换这一行

    def get_definitions(self) -> List[dict]:
        """
        获取所有已注册工具的 schema 列表。

        在 hermes-agent 中，ToolRegistry.get_definitions() 接收一个工具名称集合，
        返回匹配的工具 schema 列表。这里我们简化为返回所有工具的 schema。

        返回：
            工具 schema 列表，可直接传给 API 的 tools 参数

        示例返回值：
            [
                {"type": "function", "function": {"name": "get_weather", ...}},
                {"type": "function", "function": {"name": "calculate", ...}},
            ]
        """
        # --------------------------------------------------------------
        # TODO 2：返回所有工具的 schema 列表
        # --------------------------------------------------------------
        # 提示：遍历 self._tools，收集每个工具的 "schema" 字段
        #   return [tool_info["schema"] for tool_info in self._tools.values()]
        # --------------------------------------------------------------
        return []  # ← 替换这一行

    def dispatch(self, name: str, arguments: dict) -> str:
        """
        根据工具名称分发调用。

        在 hermes-agent 中，ToolRegistry.dispatch() 查找工具并调用其 handler，
        还处理了工具不存在、执行异常等情况。
        这里我们实现基础版本。

        参数：
            name: 工具名称
            arguments: 工具参数字典

        返回：
            工具执行结果（字符串）

        异常：
            KeyError: 工具未注册
        """
        # --------------------------------------------------------------
        # TODO 3：查找并调用工具的 handler
        # --------------------------------------------------------------
        # 提示：
        #   1. 从 self._tools 中查找 name 对应的工具
        #   2. 如果工具不存在，抛出 KeyError
        #   3. 调用 handler，传入 arguments 作为关键字参数
        #   4. 返回 handler 的结果
        #
        # 示例：
        #   tool_info = self._tools[name]
        #   handler = tool_info["handler"]
        #   return handler(**arguments)
        # --------------------------------------------------------------
        return ""  # ← 替换这一行


# ============================================================================
# 自测
# ============================================================================

if __name__ == "__main__":
    # 定义一个测试工具
    def get_weather(city: str) -> str:
        return f"{city}今天晴，气温 25°C。"

    weather_schema = {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    }

    # 测试注册表
    registry = ToolRegistry()
    registry.register("get_weather", weather_schema, get_weather)

    # 测试 get_definitions
    definitions = registry.get_definitions()
    if len(definitions) != 1:
        print(f"❌ get_definitions() 期望返回 1 个工具定义，实际 {len(definitions)} 个 — 请完成 TODO 1 和 TODO 2")
        sys.exit(1)
    print("✅ get_definitions() 正确返回 1 个工具定义")

    # 测试 dispatch
    result = registry.dispatch("get_weather", {"city": "北京"})
    if not result or "北京" not in result:
        print(f"❌ dispatch() 期望结果包含'北京'，实际：'{result}' — 请完成 TODO 3")
        sys.exit(1)
    print(f"✅ dispatch() 正确执行：{result}")

    print("\n🎉 工具注册表自测全部通过！")
