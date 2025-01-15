from typing import Optional, List, Dict

from openai import OpenAI

from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class OpenAIToolCalling(Snap):
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_MESSAGES_FIELD = "messages"
    tools: List[Dict]
    messages_field: str
    def __init__(self, tools: Optional[List[Dict]], model: Optional[str] = DEFAULT_MODEL, messages_field: Optional[str] = DEFAULT_MESSAGES_FIELD):
        super().__init__()
        self.tools = tools
        self.model = model
        self.messages_field = messages_field
    @property
    def input_views(self):
        return [
            InputView(
                name="input",
                required=True,
                type_hint=None,
                description="Input provided for the Tool calling snap"
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
        content = inputs["input"]
        messages = content[self.messages_field]
        client = OpenAI()

        # tools = [
        #     {
        #         "type": "function",
        #         "function": {
        #             "name": "get_weather",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {
        #                     "location": {"type": "string"}
        #                 },
        #             },
        #         },
        #     }
        # ]

        # messages should be something like this:
        # [{"role": "user", "content": "What's the weather like in Paris today?"}]

        chat_completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools
        )

        return {"response": chat_completion.choices[0].message.tool_calls}
