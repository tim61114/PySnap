from openai import OpenAI

from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class OpenAIToolCalls(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="prompt",
                required=True,
                type_hint=list,
                description="Prompt to send to the endpoint"
            )
        ]

    @property
    def output_views(self):
        return [
            OutputView(
                name="response",
                type_hint=list,
                description="Response from the model"
            )
        ]

    def process(self, inputs):
        messages = inputs["messages"]
        client = OpenAI()

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string"}
                        },
                    },
                },
            }
        ]

        # messages should be something like this:
        # [{"role": "user", "content": "What's the weather like in Paris today?"}]

        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        return {"response": chat_completion.choices[0].message.tool_calls}
