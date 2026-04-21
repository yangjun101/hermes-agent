"""
练习 1：Hello Agent — 你的第一个 AI Agent

目标：实现一个最简单的单轮 LLM 对话程序。
参考：hermes-agent/run_agent.py 中 AIAgent 类的基础调用部分。

运行方式：
    python hello_agent.py --mock          # 使用 mock（无需 API key）
    python hello_agent.py                 # 使用真实 API（需要 OPENAI_API_KEY）
    python hello_agent.py --message "你好"  # 自定义用户消息
"""

import argparse
import sys


# ============================================================================
# 系统提示词
# ============================================================================
# 在 hermes-agent 中，系统提示词由 prompt_builder.py 模块化组装。
# 这里我们使用一个简化版本，定义 Agent 的基本身份。

SYSTEM_PROMPT = (
    "你是一个智能 AI 助手。你乐于助人、知识渊博、回答简洁。"
    "你用中文回答用户的问题。"
)


# ============================================================================
# 核心函数
# ============================================================================

def create_client(use_mock: bool = False):
    """
    创建 OpenAI 兼容的 API 客户端。

    在 hermes-agent 中，客户端在 AIAgent.__init__() 中创建，
    支持多种提供商（OpenAI、Anthropic、Ollama 等）。
    这里我们只使用最基础的 OpenAI 客户端。

    参数：
        use_mock: 是否使用 mock 客户端（无需真实 API key）

    返回：
        OpenAI 客户端实例
    """
    if use_mock:
        from mock_client import MockOpenAI
        return MockOpenAI()

    # 真实客户端
    try:
        from openai import OpenAI
    except ImportError:
        print("❌ 请先安装 openai 库：pip install openai")
        sys.exit(1)

    return OpenAI()  # 自动从环境变量 OPENAI_API_KEY 读取密钥


def chat(client, user_message: str) -> str:
    """
    发送单轮对话请求并返回 Agent 的回复。

    在 hermes-agent 中，这对应 AIAgent.chat() 方法的核心逻辑：
    1. 构建 messages 列表
    2. 调用 Chat Completions API
    3. 提取 assistant 的回复

    参数：
        client: OpenAI 兼容的 API 客户端
        user_message: 用户输入的消息

    返回：
        Agent 的回复文本
    """

    # ------------------------------------------------------------------
    # TODO 1：构建 messages 列表
    # ------------------------------------------------------------------
    # 提示：messages 是一个列表，包含两个字典：
    #   - 第一个字典：role="system"，content=SYSTEM_PROMPT
    #   - 第二个字典：role="user"，content=user_message
    #
    # 参考 OpenAI Chat Completions API 文档：
    #   messages = [
    #       {"role": "system", "content": "..."},
    #       {"role": "user", "content": "..."},
    #   ]
    # ------------------------------------------------------------------
    messages = []  # ← 替换这一行，构建包含 system 和 user 消息的列表

    # ------------------------------------------------------------------
    # TODO 2：调用 Chat Completions API
    # ------------------------------------------------------------------
    # 提示：使用 client.chat.completions.create() 方法
    #   response = client.chat.completions.create(
    #       model="gpt-4o-mini",    # 模型名称
    #       messages=messages,       # 上面构建的消息列表
    #       temperature=0.7,         # 控制随机性（0=确定性，1=更随机）
    #   )
    #
    # 在 hermes-agent 中，模型名称通过配置传入，支持多种模型。
    # 这里我们硬编码使用 gpt-4o-mini。
    # ------------------------------------------------------------------
    response = None  # ← 替换这一行，调用 API 获取响应

    # ------------------------------------------------------------------
    # TODO 3：从响应中提取 assistant 的回复文本
    # ------------------------------------------------------------------
    # 提示：API 响应的结构如下：
    #   response.choices[0].message.content  → assistant 的回复文本
    #   response.choices[0].finish_reason    → 结束原因（"stop" 表示正常结束）
    #
    # 在 hermes-agent 中，_build_assistant_message() 方法负责解析响应。
    # ------------------------------------------------------------------
    reply = ""  # ← 替换这一行，从 response 中提取回复文本

    return reply


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序入口。"""
    parser = argparse.ArgumentParser(description="练习 1：Hello Agent")
    parser.add_argument("--mock", action="store_true", help="使用 mock 客户端")
    parser.add_argument("--message", type=str, default="你好！请介绍一下你自己。",
                        help="用户消息")
    args = parser.parse_args()

    # 创建客户端
    client = create_client(use_mock=args.mock)

    # 发送消息并获取回复
    print(f"👤 用户：{args.message}")
    reply = chat(client, args.message)
    print(f"🤖 Agent 回复：{reply}")


if __name__ == "__main__":
    main()
