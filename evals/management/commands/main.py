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
        os.system("python manage.py makemigrations")

        # message_contexts = models.MessageContext.objects.all()
        # constructors = {
        #     'instructions': models.Instruction.objects.all(),
        #     'personalization': models.Personalization.objects.all(),
        #     'examples': models.Example.objects.all(),
        #     'augmentation': models.Augmentation.objects.all(),
        # }
        # foundation_models = models.FoundationModel.objects.all()
        # run_evals(message_contexts, constructors, foundation_models)


