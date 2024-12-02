from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class TextUppercaseSnap(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="text",
                required=True,
                type_hint=str,
                description="Text to be uppercased"
            )
        ]

    @property
    def output_views(self):
        return [
            OutputView(
                name="uppercase_text",
                type_hint=str,
                description="Uppercased text"
            )
        ]

    def process(self, inputs):
        return {
            "uppercase_text": inputs["text"].upper()
        }