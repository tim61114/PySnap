import json
from typing import Optional, List, Dict, Tuple

from openai import OpenAI

from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class OpenAIToolCallingAuto(Snap):
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_MESSAGES_FIELD = "messages"
    tools: List[Dict]
    tooldefs = Dict[str, Tuple]
    messages_field: str
    def __init__(self, tooldefs: Dict[str, Tuple], model: Optional[str] = DEFAULT_MODEL, messages_field: Optional[str] = DEFAULT_MESSAGES_FIELD, passthrough: Optional[bool] = False):
        super().__init__(passthrough)
        self.tools = [tool for (tool, _) in tooldefs.values()]
        self.tooldefs = tooldefs
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

        while chat_completion.choices[0].finish_reason != "stop":
            if chat_completion.choices[0].finish_reason == "tool_calls":
                tool_call = chat_completion.choices[0].message.tool_calls[0]
                args = json.loads(tool_call.function.arguments)

                result = self.tooldefs[tool_call.function.name][1](**args)
                messages.append(chat_completion.choices[0].message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                chat_completion = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools
                )

        return {"response": chat_completion.choices[0].message.content}
    
