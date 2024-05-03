import time
import json

from openai import OpenAI
import boto3


def open_ai_inference(prompt, variant):

    client = OpenAI()

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


def bedrock_inference(system_prompt, messages, modelId):

    session = boto3.Session(region_name='us-west-2')
    brt = session.client(service_name='bedrock-runtime', region_name='us-west-2')

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "max_tokens": 1000,
            "messages": messages
        }
    )
    accept = 'application/json'
    contentType = 'application/json'

    start = time.time()
    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    end = time.time()
    timedelta_ms = (end - start) * 1000  # Calculate the time difference in milliseconds

    response_body = json.loads(response.get('body').read())
    return response_body, timedelta_ms

