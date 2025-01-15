from pysnap.core.snap import Snap
from pysnap.core.views import OutputView


class TextGeneratorSnap(Snap):
    content = ""
    def __init__(self, text: str):
        super().__init__()
        self.content = text
        
    
    @property
    def input_views(self):
        return []

    @property
    def output_views(self):
        return [
            OutputView(
                name="text",
                type_hint=str,
                description="Text to output"
            )
        ]

    def process(self, inputs):
        return {"text": self.content}
