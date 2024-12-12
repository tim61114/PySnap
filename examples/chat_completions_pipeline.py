from examples.snaps.openai.chat_completions import OpenAIChatCompletions
from pysnap.core.pipeline import Pipeline


def main():
    pipeline = Pipeline()
    openai_cc_snap = OpenAIChatCompletions()
    pipeline.add_snap(openai_cc_snap)
    pipeline.execute({"prompt": "What is the meaning of life?"})
    result = pipeline.get_output()
    print(result)


if __name__ == "__main__":
    main()
