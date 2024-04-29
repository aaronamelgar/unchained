from evals.models import GeneratedResult
from evals.registry import register_evaluator


@register_evaluator
def toxicity_score(generated_result: GeneratedResult) -> float:
    return 0.0


@register_evaluator
def string_distance(generated_result: GeneratedResult) -> float:
    return 0.0


@register_evaluator
def contains(generated_result: GeneratedResult) -> float:
    return 1.0 if generated_result.message_context.reference_output in generated_result.model_output_text else 0

