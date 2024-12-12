import copy

from examples.snaps.router_snap import RouterSnap
from examples.snaps.text_length_snap import TextLengthSnap
from examples.snaps.text_uppercase_snap import TextUppercaseSnap
from pysnap.core.pipeline import Pipeline

# Example usage
def main():

    # Pipeline visualization
    # RouterSnap ------> TextLengthSnap
    #            ------> TextUppercaseSnap
    pipeline = Pipeline()

    router_snap = RouterSnap()
    uppercase_snap = TextUppercaseSnap()
    length_snap = TextLengthSnap()

    pipeline.add_snap(router_snap)
    pipeline.add_snap(uppercase_snap)
    pipeline.add_snap(length_snap)

    pipeline.connect(router_snap, "output1", uppercase_snap, "text")
    pipeline.connect(router_snap, "output2", length_snap, "text")
    input_data_list = [{"input": "hello"}, {"input": "This is a loooooong sentence"}, {"input": "hello world"}]

    for input_data in input_data_list:
        pipeline_instance = copy.deepcopy(pipeline)
        pipeline_instance.execute(input_data)
        pipeline_instance.get_output()
        print("-" * 50)



if __name__ == "__main__":
    main()
