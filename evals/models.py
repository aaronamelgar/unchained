import uuid
import json

from django.db import models
from django_jsonform.models.fields import JSONField
from taggit.managers import TaggableManager

from evals.tag import Tag
from evals.registry import evaluation_registry


class FoundationModelFamily(models.TextChoices):
    OPEN_AI = 'open-ai'
    BEDROCK = 'bedrock'


class FoundationModelVariant(models.TextChoices):
    GPT_4_TURBO_PREVIEW = 'gpt-4-turbo-preview'
    CLAUDE_SONNET = 'anthropic.claude-3-sonnet-20240229-v1:0'


class FoundationModel(models.Model):
    family = models.CharField(max_length=50, choices=FoundationModelFamily.choices, null=False)
    variant = models.CharField(max_length=50, choices=FoundationModelVariant.choices, primary_key=True, null=False)
    input_token_cost = models.FloatField(default=0.0)
    output_token_cost = models.FloatField(default=0.0)

    def __str__(self):
        return self.variant


class Run(models.Model):
    id = models.CharField(primary_key=True, null=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MessageContext(models.Model):

    MESSAGES_SCHEMA = {
        'type': 'array',
        'items': {
            'type': 'dict',
            'keys': {
                'role': {
                    'type': 'string',
                    'choices': ['user', 'assistant']
                },
                'content': {
                    'type': 'string'
                },
            }
        }
    }

    name = models.CharField(primary_key=True, null=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    messages = JSONField(schema=MESSAGES_SCHEMA)
    reference_output = models.TextField(null=True, blank=True)

    tags = TaggableManager(blank=True, through=Tag)

    def __str__(self):
        return self.name

    def pretty_chat(self):
        return json.dumps(self.messages, indent=4)


class PromptConstructor(models.Model):
    name = models.CharField(primary_key=True, null=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    tags = TaggableManager(blank=True, through=Tag)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Instruction(PromptConstructor):
    pass


class Example(PromptConstructor):
    pass


class Personalization(PromptConstructor):
    pass


class Augmentation(PromptConstructor):
    pass


class RatingChoices(models.TextChoices):
    ONE = 1, 'One'
    TWO = 2, 'Two'
    THREE = 3, 'Three'
    FOUR = 4, 'Four'


class GeneratedResult(models.Model):

    id = models.CharField(primary_key=True, null=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    foundation_model = models.ForeignKey(FoundationModel, on_delete=models.CASCADE)

    message_context = models.ForeignKey(MessageContext, on_delete=models.CASCADE, default=True)
    instructions = models.ManyToManyField(Instruction)
    examples = models.ManyToManyField(Example)
    augmentation = models.ManyToManyField(Augmentation)
    personalization = models.ManyToManyField(Personalization)

    completed_system_prompt = models.TextField(null=True)
    chat = models.JSONField(null=True)
    model_output_text = models.TextField(null=True)
    model_output = models.JSONField(null=True)
    human_rating = models.IntegerField(
        choices=RatingChoices.choices,
        null=True,
    )

    input_tokens = models.IntegerField(null=True)
    output_tokens = models.IntegerField(null=True)
    latency = models.IntegerField(null=True)

    def pretty_chat(self):
        return json.dumps(json.loads(self.chat), indent=4)


class Evaluator(models.Model):
    name = models.CharField(max_length=50, choices=FoundationModelVariant.choices, primary_key=True)
    subjects = models.ManyToManyField(MessageContext, related_name='evaluators')

    def __str__(self):
        return self.name

    def generate_score(self, generated_result):
        function = evaluation_registry[self.name]
        return function(generated_result)

    def evaluate(self, generated_result):
        pass


class EvaluationResult(models.Model):
    id = models.CharField(primary_key=True, null=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    generated_result = models.ForeignKey(GeneratedResult, null=True, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)

    def evaluate(self):
        eval_score = self.evaluator.generate_score(self.generated_result)
        self.score = eval_score
        self.save()

