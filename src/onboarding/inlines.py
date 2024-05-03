from django.contrib import admin

from onboarding.models import Choice


class ChoiceInline(admin.TabularInline):
    """Inline значений поля."""

    model = Choice
    template = 'inlines/tabular.html'
    can_delete = False
    extra = 1

    class Media:
        js = ('js/inlines.js',)
