# Generated by Django 5.0.4 on 2024-04-26 21:47

import django.db.models.deletion
import django_jsonform.models.fields
import taggit.managers
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Augmentation',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Evaluator',
            fields=[
                ('name', models.CharField(choices=[('gpt-4-turbo-preview', 'Gpt 4 Turbo Preview')], max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FoundationModel',
            fields=[
                ('family', models.CharField(choices=[('open-ai', 'Open Ai')], max_length=50)),
                ('variant', models.CharField(choices=[('gpt-4-turbo-preview', 'Gpt 4 Turbo Preview')], max_length=50, primary_key=True, serialize=False)),
                ('input_token_cost', models.FloatField(default=0.0)),
                ('output_token_cost', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MessageContext',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('messages', django_jsonform.models.fields.JSONField()),
                ('reference_output', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personalization',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneratedResult',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_system_prompt', models.TextField(null=True)),
                ('chat', models.JSONField(null=True)),
                ('model_output_text', models.TextField(null=True)),
                ('model_output', models.JSONField(null=True)),
                ('human_rating', models.IntegerField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four')], null=True)),
                ('examples', models.ManyToManyField(to='evals.example')),
                ('foundation_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evals.foundationmodel')),
                ('research', models.ManyToManyField(to='evals.augmentation')),
                ('instructions', models.ManyToManyField(to='evals.instruction')),
                ('message_context', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='evals.messagecontext')),
                ('personalization', models.ManyToManyField(to='evals.personalization')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evals.run')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationResult',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(null=True)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evals.evaluator')),
                ('generated_result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evals.generatedresult')),
            ],
        ),
        migrations.AddField(
            model_name='evaluator',
            name='subjects',
            field=models.ManyToManyField(related_name='evaluators', to='evals.messagecontext'),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=32, verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='personalization',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='evals.Tag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='messagecontext',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='evals.Tag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='instruction',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='evals.Tag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='example',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='evals.Tag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='augmentation',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='evals.Tag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]