from snaps.openai.tool_calling_auto_run_tools import OpenAIToolCallingAuto
from snaps.any_generator_snap import AnyGeneratorSnap
from pysnap.core.pipeline import Pipeline


def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny."


def main():
    pipeline = Pipeline()
    content = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant with tools."},
            {"role": "user", "content": "What's the weather in LA?"}
        ]
    }

    any_generator_snap = AnyGeneratorSnap(content=content)
    tools = {
        "get_weather": (
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
            },
            get_weather
        )
    }
    # openai_tc_snap = OpenAIToolCallingAuto(tools, passthrough=True)
    openai_tc_snap = OpenAIToolCallingAuto(tools)
    pipeline.add_snap(any_generator_snap)
    pipeline.add_snap(openai_tc_snap)
    pipeline.connect(any_generator_snap, "output", openai_tc_snap, "input")
    pipeline.execute()
    pipeline.get_output()



if __name__ == "__main__":
    main()
