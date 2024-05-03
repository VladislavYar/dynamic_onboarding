import json

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.utils.html import format_html
from django.utils.safestring import SafeText

from onboarding.inlines import ChoiceInline
from onboarding.models import (FieldType, MainSurvey, Survey, SurveyData,
                               SurveyField, SurveyUserStatus)


class BaseModel(admin.ModelAdmin):
    """Базовая админ панель."""

    search_fields = [
        'name',
    ]


class ProtectionAddDeleteBaseModel(admin.ModelAdmin):
    """Базовая модель запрета добавления и редактирования"""

    # def has_add_permission(
    #         self, request: WSGIRequest,
    #         obj: Model | None = None,
    #         ) -> bool:
    #     """Запрещает добавление объекта."""
    #     return False

    # def has_delete_permission(
    #         self, request: WSGIRequest,
    #         obj: Model | None = None,
    #         ) -> bool:
    #     """Запрещает удаление объекта."""
    #     return False


@admin.register(SurveyUserStatus)
class SurveyUserStatusAdmin(ProtectionAddDeleteBaseModel):
    """Админ панель статуса пользователя в опросе."""

    list_display = tuple(
        field.name for field in SurveyUserStatus._meta.get_fields()
        if not field.many_to_many
        )
    readonly_fields = tuple(
        field.name for field in SurveyUserStatus._meta.get_fields()
        )


@admin.register(MainSurvey)
class MainSurveyAdmin(ProtectionAddDeleteBaseModel):
    """Админ панель главного опроса на странице."""

    list_display = tuple(
        field.name for field in MainSurvey._meta.get_fields()
        )
    readonly_fields = ('namespace',)


@admin.register(SurveyData)
class SurveyDataAdmin(ProtectionAddDeleteBaseModel):
    """Админ панель данных по опросу."""

    list_display = ('survey', 'user', 'datetime',)
    readonly_fields = [
        field.name for field in SurveyData._meta.get_fields()
    ] + ['display_data']
    fields = ('survey', 'user', 'datetime', 'display_data')

    @admin.display(
            description=SurveyData._meta.get_field(
                'data'
                ).verbose_name
            )
    def display_data(self, obj: SurveyData) -> SafeText:
        """Вывод данных в виде списка."""
        data = json.loads(obj.data)
        display_list = []
        for name, values in data.items():
            display_list += [f'<p>{name}:</p><ol>']
            if isinstance(values, list):
                display_list += [f'<li>{value}</li>' for value in values]
            else:
                display_list += [f'<li>{values}</li>']
            display_list += ['</ol>']
        return format_html(''.join(display_list))


@admin.register(Survey)
class SurveyAdmin(BaseModel):
    """Админ панель опроса."""

    list_display = ('name', 'slug')
    fields = ('name',)


@admin.register(FieldType)
class FieldTypeAdmin(BaseModel):
    """Админ панель типа поля опроса."""

    list_display = ('name', 'field_type', 'many', 'regexp')
    list_filter = ('many',)


@admin.register(SurveyField)
class SurveyFieldAdmin(BaseModel):
    """Админ панель поля опроса."""

    list_display = ('name', 'survey', 'question', 'field_type',)
    list_filter = ('field_type__many', 'survey', 'field_type',)
    change_form_template = 'admin/change_form.html'

    inlines = (ChoiceInline, )

    class Media:
        js = (
            'js/jquery-3.7.1.min.js',
        )

    def get_readonly_fields(
            self, request: WSGIRequest,
            obj: SurveyField | None = None,
            ) -> list[None] | tuple[str]:
        """Изменяет поля для редактирования."""
        if obj:
            return ('field_type',)
        return []

    def counts_statistics(
            self, json_data: list[str],
            stats_choices: list | str,
            slug: str,
            ) -> None:
        """Считает статистику."""
        for data in json_data:
            select_values = json.loads(data).get(slug)
            if not isinstance(select_values, list):
                stats_choices[select_values][0] += 1
                continue
            for select_value in select_values:
                stats_choices[select_value][0] += 1

    def change_view(
            self, request: WSGIRequest, object_id: str,
            form_url: str = '', extra_context: dict | None = None,
            ):
        """Добавление данных для графика."""
        extra_context = extra_context or {}
        field = SurveyField.objects.get(id=object_id)
        choices = field.choices.all()
        if len(choices) <= 1:
            return super().change_view(
                request, object_id, form_url, extra_context
                )
        json_data = SurveyData.objects.filter(
            survey=field.survey
            ).values_list('data', flat=True)
        stats_choices = {
            choice.slug: [0, choice.name] for choice in choices
            }
        self.counts_statistics(json_data, stats_choices, field.slug)
        extra_context['graph'] = {
            'name': field.name, 'stats_choices': stats_choices.values()
            }
        return super().change_view(request, object_id, form_url, extra_context)
