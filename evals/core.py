import copy
import json
from string import Template
import time

from evals.inference import open_ai_inference

from evals import models


def run_evals(message_contexts, constructors, foundation_models):

    run = models.Run.objects.create()

    assembled_constructors = dict()
    for k, v in constructors.items():
        assembled_constructors[k] = "\n".join([value.text for value in v])

    for message_context in message_contexts:
        for foundation_model in foundation_models:

            model_output_json, model_output_text, complete_prompt, input_tokens, output_tokens, latency = generate_response(
                message_context.messages,
                assembled_constructors,
                foundation_model
            )

            result = models.GeneratedResult.objects.create(
                run=run,
                foundation_model=foundation_model,
                message_context=message_context,
                completed_system_prompt=complete_prompt,

                chat=json.dumps(message_context.messages),
                model_output_text=model_output_text,
                model_output=model_output_json,

                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency=latency,
            )

            for k, v in constructors.items():
                field_name = k
                related_manager = getattr(result, field_name)
                for instance in v:
                    related_manager.add(instance)
                result.save()


def generate_response(messages, constructor_values, foundation_model: models.FoundationModel):

    prompt = constructor_values['instructions']

    constructed = Template(prompt).substitute(**constructor_values)
    inference_messages = copy.deepcopy(messages)
    inference_messages.insert(0, {'role': 'system', 'content': constructed})

    # TODO: make this dependent on FoundationModelFamily
    formatted_prompt = format_messages_to_prompt(inference_messages)

    # TODO: clean this up: build this into a class for portability
    if foundation_model.family == models.FoundationModelFamily.OPEN_AI:
        response, latency = open_ai_inference(inference_messages, foundation_model.variant)
        input_token_count = response.dict()['usage']['prompt_tokens']
        output_token_count = response.dict()['usage']['completion_tokens']
        return response.dict(), response.choices[0].message.content, formatted_prompt, input_token_count, output_token_count, latency

    elif foundation_model.family == models.FoundationModelFamily.BEDROCK:
        response, latency = bedrock_inference(constructed, messages, foundation_model.variant)
        input_token_count = response['usage']['input_tokens']
        output_token_count = response['usage']['output_tokens']
        return response, response.get('content')[0]['text'], formatted_prompt, input_token_count, output_token_count, latency

    else:
        raise Exception("Invalid foundation model")


def format_messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        # Build the prefix with optional timestamp
        prefix = f"{message['role'].capitalize()}: "
        if 'timestamp' in message:
            prefix = f"[{message['timestamp']}] {prefix}"

        # Handle newlines and apply markdown transformation if necessary
        formatted_content = message['content']
        if message['role'] == 'assistant':
            formatted_content = apply_markdown(formatted_content)

        prompt += f"{prefix}{formatted_content} "

    return prompt.strip()


def apply_markdown(content):
    # Placeholder for markdown processing, for example:
    content = content.replace("**", "")  # Removing markdown bold as a simplistic example
    return content
