from snaps.text_length_snap import TextLengthSnap
from snaps.text_uppercase_snap import TextUppercaseSnap
from pysnap.core.pipeline import Pipeline


def main():
    # Create a new pipeline instance
    pipeline = Pipeline()
    
    # Create instances of Snaps
    uppercase_snap = TextUppercaseSnap()
    length_snap = TextLengthSnap()
    length_snap2 = TextLengthSnap()
    
    # Add snaps to the pipeline
    pipeline.add_snap(uppercase_snap)
    pipeline.add_snap(length_snap)
    pipeline.add_snap(length_snap2)
    
    # Connect snaps in the pipeline
    # Connect the output of uppercase_snap to the input of length_snap
    pipeline.connect(uppercase_snap, "uppercase_text", length_snap, "text")
    pipeline.connect(length_snap, "text_length", length_snap2, "text")
    
    # Execute the pipeline with initial input
    pipeline.execute({"text": "hello world"})
    pipeline.get_output()


if __name__ == "__main__":
    main()
