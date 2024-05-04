import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from onboarding.models import (Choice, FieldType, MainSurvey, Survey,
                               SurveyField)

User = get_user_model()


class Command(BaseCommand):

    help = 'Добавляет тестовые данные в БД.'
    types_names = {
            'checkbox': ('Флажки', True),
            'date': ('Дата', False),
            'datetime-local': ('Местная дата и время', False),
            'email': ('Электронная почта', False),
            'number': ('Число', False),
            'radio': ('Переключатель', True),
            'text': ('Текст', False),
            'time': ('Время', False),
            'url': ('Веб-адрес', False),
        }

    def _add_fields_types(self) -> list[FieldType]:
        """Добавляет тестовые типы кнопок в БД."""
        fields_types = []
        for field_type, values in self.types_names.items():
            fields_types.append(
                FieldType(
                    field_type=field_type,
                    name=values[0],
                    many=values[1],
                    )
                )
        return FieldType.objects.bulk_create(fields_types)

    def _add_surveys(self) -> Survey:
        """Добавление опросов."""
        surveys = []
        for i in range(1, 21):
            surveys.append(Survey(name=f'Опрос №{i}'))
        return Survey.objects.bulk_create(surveys)

    def _add_survey_fields(self) -> None:
        """Добавление полей опросов."""
        types = list(self.types_names.keys())
        fields = {
            1: [2, 20, 9],
            2: [3, 8, 11, [17, 18, 19]],
            3: [4, 6, 11],
            4: [5, 6, [11, 8]],
            5: [7, [6, 10], [12, 11, 19]],
            6: [12, 10, 7],
            7: [10, 9],
            8: [9, 10],
            9: [10],
            10: [12],
            }
        count = 0
        choices = []
        for survey, child_surveys in fields.items():
            survey = Survey.objects.get(id=survey)
            for child_survey in child_surveys:
                count += 1
                if not isinstance(child_survey, list):
                    survey_field = SurveyField(
                        survey=survey,
                        field_type=FieldType.objects.get(
                            field_type=random.choice(types)
                            ),
                        question=f'Вопрос №{count}?',
                        help_text=f'Текст помощи №{count}',
                        name=f'Поле №{count}',
                        required=random.choice([True, False]),
                        )
                    survey_field.save()
                    child_survey = Survey.objects.get(id=child_survey)
                    choices.append(
                        Choice(
                            survey_field=survey_field,
                            survey=child_survey,
                            name=f'Выбор №{count}',
                            )
                        )
                    continue
                survey_field = SurveyField(
                    survey=survey,
                    field_type=FieldType.objects.get(
                            field_type=random.choice(['checkbox', 'radio'])
                            ),
                    question=f'Вопрос №{count}?',
                    help_text=f'Текст помощи №{count}',
                    name=f'Поле №{count}',
                    required=random.choice([True, False]),
                    )
                survey_field.save()
                for ch_su in child_survey:
                    ch_su = Survey.objects.get(id=ch_su)
                    choices.append(
                        Choice(
                            survey_field=survey_field,
                            survey=ch_su,
                            name=f'Выбор №{count}',
                            )
                        )
                    count += 1
        Choice.objects.bulk_create(choices)

    def handle(self, *args, **options):
        self._add_fields_types()
        surveys = self._add_surveys()
        MainSurvey(
            main_survey=surveys[0],
            namespace='onboarding:index',
            ).save()
        self._add_survey_fields()
