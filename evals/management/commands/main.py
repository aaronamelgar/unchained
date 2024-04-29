import os

from django.core.management import BaseCommand

from evals.core import run_evals
from evals import models
from evals import evaluators


class Command(BaseCommand):
    """
    :return:
    """

    def handle(self, *args, **options):
        message_contexts = models.MessageContext.objects.all()
        constructors = {
            'instructions': models.Instruction.objects.all(),
            'personalization': models.Personalization.objects.all(),
            'examples': models.Example.objects.all(),
            'research': models.Augmentation.objects.all(),
        }

        run_evals(message_contexts, constructors)


