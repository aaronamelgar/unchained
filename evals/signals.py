from django.db.models.signals import post_migrate
from django.dispatch import receiver
from evals.models import Evaluator

from evals.registry import evaluation_registry


@receiver(post_migrate)
def create_default_evaluators(sender, **kwargs):
    if sender.name == 'evals':  # Check if the sender is your app
        for name, func in evaluation_registry.items():
            instance, created = Evaluator.objects.get_or_create(name=name)
            if created:
                print(f"{name} created in the database")

