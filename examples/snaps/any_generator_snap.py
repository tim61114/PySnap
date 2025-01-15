from typing import Any

from pysnap.core.snap import Snap
from pysnap.core.views import OutputView


class AnyGeneratorSnap(Snap):
    content: Any
    def __init__(self, content: Any):
        super().__init__()
        self.content = content
        
    
    @property
    def input_views(self):
        return []

    @property
    def output_views(self):
        return [
            OutputView(
                name="output",
                type_hint=Any,
                description="Any output"
            )
        ]

    def process(self, inputs):
        return {"output": self.content}
