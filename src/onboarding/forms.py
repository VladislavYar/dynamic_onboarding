import json

from django import forms

from onboarding.constants import TYPES_FIELDS
from onboarding.models import (Choice, FieldType, Survey, SurveyData,
                               SurveyField, SurveyUserStatus)
from users.models import User


class OnboardingForm(forms.Form):
    """Форма онбординга."""

    surveys_names = None

    def _field_formation(self, field: SurveyField, survey: Survey) -> None:
        """Формирует поле."""
        field_type: FieldType = field.field_type
        params = {
            'required': field.required,
            'help_text': field.help_text,
            'label': field.name,
            'template_name': field.question,
            }
        if field_type.regexp:
            params['regex'] = field_type.regexp
            self.fields[
                f'{survey.slug}__{field.slug}'
                ] = forms.RegexField(**params)
        elif field_type.field_type in TYPES_FIELDS:
            if field_type.many:
                params['choices'] = field.choices.values_list(
                    'slug', 'name',
                    )
            else:
                params['widget'] = forms.TextInput(
                            attrs={'type': field_type.field_type}
                            )
            self.fields[
                f'{survey.slug}__{field.slug}'
                ] = TYPES_FIELDS[field_type.field_type](**params)

    def _add_fileds(self, surveys: tuple[Survey]) -> None:
        """Добавление полей опросов."""
        self.surveys_names = {}
        for survey in surveys:
            fields = survey.survey_fields.all()
            if fields:
                self.surveys_names[survey.slug] = survey.name
            for field in fields:
                self._field_formation(field, survey)

    def prepares_data(
            self, json_data: dict, callback_surveys: set
            ) -> tuple[dict, set]:
        """Подготавливает коллекции с данными."""
        for slug, value in self.cleaned_data.items():
            if not value:
                continue
            keys = slug.split('__')
            if isinstance(value, list):
                json_data[keys[0]][keys[1]] = value
                callback_surveys = callback_surveys | set(
                    filter(None, Choice.objects.filter(
                        slug__in=value
                        ).values_list('survey', flat=True)
                    ))
                continue
            json_data[keys[0]][keys[1]] = str(value)
            survey = SurveyField.objects.get(
                slug=keys[1]
                ).choices.all().first().survey
            if not survey:
                continue
            callback_surveys.add(survey.id)
        return json_data, callback_surveys

    def _serializes_data(
            self, user: User,
            main_survey: Survey,
            ) -> tuple[set[Survey], dict[str, str]]:
        """Обрабатывает данные для сохранения в БД."""
        json_data, callback_surveys = self.prepares_data(
            {survey: {} for survey in self.surveys_names}, set()
            )
        surveys_user_status = SurveyUserStatus.objects.create(
            user=user, main_survey=main_survey
            )
        surveys_data = [
            SurveyData(
                survey=Survey.objects.get(slug=survey),
                data=json.dumps(values), user=user,
                ) for survey, values in json_data.items()
            ]
        return surveys_user_status, surveys_data, callback_surveys

    def save(self, user: User, main_survey: Survey) -> None:
        """Сохраняет данные в БД."""
        surveys_user_status, surveys_data, callback_surveys = (
            self._serializes_data(user, main_survey)
            )
        surveys_user_status.save()
        for id in callback_surveys:
            surveys_user_status.callback_surveys.add(id)
        SurveyData.objects.bulk_create(surveys_data)

    def __init__(self, surveys=None, *args, **kwargs):
        """Формирование полей формы."""
        super().__init__(*args, **kwargs)
        self._add_fileds(surveys)
