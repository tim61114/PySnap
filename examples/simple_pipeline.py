from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView
from pysnap.core.pipeline import Pipeline

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

class TextLengthSnap(Snap):
    @property
    def input_views(self):
        return [
            InputView(
                name="uppercase_text", 
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
                type_hint=int, 
                description="Length of the input text"
            )
        ]
    
    def process(self, inputs):
        return {
            "text_length": len(inputs["uppercase_text"])
        }

def main():
    # Create a new pipeline instance
    pipeline = Pipeline()
    
    # Create instances of Snaps
    uppercase_snap = TextUppercaseSnap()
    length_snap = TextLengthSnap()
    
    # Add snaps to the pipeline
    pipeline.add_snap(uppercase_snap)
    pipeline.add_snap(length_snap)
    
    # Connect snaps in the pipeline
    # Connect the output of uppercase_snap to the input of length_snap
    pipeline.connect(uppercase_snap, "uppercase_text", length_snap, "uppercase_text")
    
    # Execute the pipeline with initial input
    result = pipeline.execute({"text": "hello world"})
    
    # Print the final result of the pipeline execution
    print(result)

if __name__ == "__main__":
    main()
