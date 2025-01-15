from snaps.openai.chat_completions import OpenAIChatCompletions
from snaps.text_generator_snap import TextGeneratorSnap
from pysnap.core.pipeline import Pipeline


def main():
    pipeline = Pipeline()
    text_generator_snap = TextGeneratorSnap(text="Where can I visit in San Francisco?")
    openai_cc_snap = OpenAIChatCompletions(model="gpt-4o")
    pipeline.add_snap(openai_cc_snap)
    pipeline.add_snap(text_generator_snap)
    pipeline.connect(text_generator_snap, "text", openai_cc_snap, "prompt")
    pipeline.execute()
    pipeline.get_output()


if __name__ == "__main__":
    main()
