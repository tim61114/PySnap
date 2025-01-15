from examples.snaps.any_generator_snap import AnyGeneratorSnap
from examples.snaps.openai.tool_calling import OpenAIToolCalling
from pysnap.core.pipeline import Pipeline


def main():
    pipeline = Pipeline()
    content = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant with tools."},
            {"role": "user", "content": "What's the weather in San Francisco?"}
        ]
    }

    any_generator_snap = AnyGeneratorSnap(content=content)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                },
            },
        }
    ]
    openai_tc_snap = OpenAIToolCalling(tools)
    pipeline.add_snap(any_generator_snap)
    pipeline.add_snap(openai_tc_snap)
    pipeline.connect(any_generator_snap, "output", openai_tc_snap, "input")
    pipeline.execute()
    pipeline.get_output()

if __name__ == "__main__":
    main()
