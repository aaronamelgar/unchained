import time

from openai import OpenAI

client = OpenAI()


def open_ai_inference(prompt, variant):

    start = time.time()
    response = client.chat.completions.create(
                model=variant,
                messages=prompt,
                # tools=functions,
                temperature=0.7,
                tool_choice=None
            )
    end = time.time()
    timedelta_ms = (end - start) * 1000  # Calculate the time difference in milliseconds

    return response, timedelta_ms
