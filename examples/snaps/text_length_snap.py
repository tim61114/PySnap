from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class TextLengthSnap(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="text",
                required=True,
                type_hint=str,
                description="Text to measure"
            )
        ]

    @property
    def output_views(self):
        return [
            OutputView(
                name="text_length",
                type_hint=str,
                description="Length of the input text"
            )
        ]

    def process(self, inputs):
        return {
            "text_length": str(len(inputs["text"]))
        }