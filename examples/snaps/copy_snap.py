from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class CopySnap(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="input",
                required=True,
                type_hint=None,
                description="Input text"
            )
        ]

    # Define as much output views as needed
    @property
    def output_views(self):
        return [
            OutputView(
                name="output1",
                type_hint=None,
                description="Output copy1"
            ),
            OutputView(
                name="output2",
                type_hint=None,
                description="Output copy2"
            )
        ]

    def process(self, inputs):
        output = {}
        for ov in self.output_views:
            output[ov.name] = inputs["input"]

        return output
