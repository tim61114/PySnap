from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView
from openai import OpenAI


class OpenAIChatCompletions(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="prompt",
                required=True,
                type_hint=str,
                description="Prompt to send to the endpoint"
            )
        ]

    @property
    def output_views(self):
        return [
            OutputView(
                name="response",
                type_hint=str,
                description="Response from the model"
            )
        ]

    def process(self, inputs):
        prompt = inputs["prompt"]
        # OpenAI pulls the API key from the environment variable OPENAI_API_KEY by default.
        # You can also pass the key directly to the OpenAI constructor.
        client = OpenAI()

        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return {"response": chat_completion.choices[0].message.content}
