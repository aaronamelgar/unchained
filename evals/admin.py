from django.contrib import admin
from .models import GeneratedResult, MessageContext, Evaluator
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class GeneratedResultAdmin(admin.ModelAdmin):
    list_display = ('pretty_chat', 'model_output_text', 'reference_output', 'human_rating')
    list_editable = ('human_rating',)
    fields = (
        'human_rating',
        'model_output_text',
        'pretty_chat',
        'foundation_model',
        'message_context',
        'input_tokens',
        'output_tokens',
        'latency',
        'examples',
        'research',
        'personalization',
        'instructions',
        'completed_system_prompt',
    )

    class Media:
        css = {
            'all': ('css/generated_results.css',)
        }

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = [f.name for f in self.model._meta.fields if f.name != 'human_rating']
        readonly_fields.append('pretty_chat')
        return readonly_fields

    def pretty_chat(self, obj):
        return format_html(
            '<pre style="white-space: pre-wrap; max-width: 90%; overflow-wrap: break-word; font-family-primary: "Segoe UI", system-ui, Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji",;">{}</pre>',
            obj.pretty_chat()
        )

    def reference_output(self, obj):
        return obj.message_context.reference_output

    pretty_chat.short_description = "Chat Context"


class TagListFilter(admin.SimpleListFilter):
    title = _('tags')  # Display title for the filter
    parameter_name = 'tag'  # URL query parameter

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. Each tuple contains a tag's slug or ID as the first element
        and the tag name as the second element.
        """
        tags = model_admin.model.tags.get_queryset()  # Adjust this query to match your tag setup
        return [(tag.slug, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected tag.
        """
        if self.value():
            # Adjust the filter lookup to match your related field setup
            return queryset.filter(tags__name__in=[self.value()])


class EvaluatorListFilter(admin.SimpleListFilter):
    title = _('evaluator')  # Display title for the filter
    parameter_name = 'evaluator'  # URL parameter used to filter

    def lookups(self, request, model_admin):
        # Retrieve all Evaluator instances and create lookup pairs
        evaluators = Evaluator.objects.all()
        return [(evaluator.name, evaluator.name) for evaluator in evaluators]

    def queryset(self, request, queryset):
        if self.value():
            # Return the queryset of MessageContexts that are linked to the selected Evaluator
            return queryset.filter(evaluators__name=self.value())
        return queryset


class EvaluatorInline(admin.TabularInline):
    model = Evaluator.subjects.through  # Access the through model for the many-to-many relationship
    extra = 1  # How many rows to show by default


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'pretty_chat', 'reference_output', 'tag_list', 'evaluator_list')
    list_filter = (TagListFilter, EvaluatorListFilter)
    inlines = [EvaluatorInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def evaluator_list(self, obj):
        return ", ".join([evaluator.name for evaluator in obj.evaluators.all()])

    def pretty_chat(self, obj):
        return format_html(
            '<pre style="white-space: pre-wrap; max-width: 90%; overflow-wrap: break-word; font-family-primary: "Segoe UI", system-ui, Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji",;">{}</pre>',
            obj.pretty_chat()
        )

    pretty_chat.short_description = "Chat Messages"


admin.site.register(GeneratedResult, GeneratedResultAdmin)
admin.site.register(MessageContext, MessagesAdmin)
