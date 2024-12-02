from examples.snaps.text_length_snap import TextLengthSnap
from examples.snaps.text_uppercase_snap import TextUppercaseSnap
from pysnap.core.pipeline import Pipeline
from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView
from typing import Dict, Any, List

class ConditionSnap(Snap):
    def __init__(self):
        self._input_views = [InputView(name="input")]
        self._output_views = [OutputView(name="contains_a"), OutputView(name="does_not_contain_a")]

    @property
    def input_views(self) -> List[InputView]:
        return self._input_views

    @property
    def output_views(self) -> List[OutputView]:
        return self._output_views

    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        input_data = inputs.get("input", "")
        if "a" in input_data:
            return {"contains_a": input_data}
        else:
            return {"does_not_contain_a": input_data}

# Example usage
def main():
    pipeline = Pipeline()

    condition_snap = ConditionSnap()
    uppercase_snap = TextUppercaseSnap()
    length_snap = TextLengthSnap()

    pipeline.add_snap(condition_snap)
    pipeline.add_snap(uppercase_snap)
    pipeline.add_snap(length_snap)

    pipeline.connect(condition_snap, "contains_a", uppercase_snap, "text")
    pipeline.connect(condition_snap, "does_not_contain_a", length_snap, "text")
    input_data_list = [{"input": "example data"}, {"input": "not this one"}, {"input": "hello world"}]
    output_list = []

    for input_data in input_data_list:
        output = pipeline.execute(input_data)
        output_list.append(output)

    print("Output List:", output_list)

if __name__ == "__main__":
    main()
