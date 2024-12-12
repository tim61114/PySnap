from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView


class RouterSnap(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="input",
                required=True,
                type_hint=str,
                description="Text to measure"
            )
        ]

    # Define as much output views as needed
    @property
    def output_views(self):
        return [
            OutputView(
                name="output1",
                type_hint=str,
                description="Text longer than 10 characters"
            ),
            OutputView(
                name="output2",
                type_hint=str,
                description="Text shorter than 10 characters"
            )
        ]

    def process(self, inputs):
        # Send to output based on input conditions, conditions can be whatever
        if len(inputs["input"]) > 10:
            return {"output1": inputs["input"]}
        else:
            return {"output2": inputs["input"]}
