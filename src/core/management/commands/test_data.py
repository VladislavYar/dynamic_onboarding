from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from onboarding.models import FieldType, MainSurvey, Survey

User = get_user_model()


class Command(BaseCommand):

    help = 'Добавляет тестовые данные в БД.'

    def _add_fields_types(self) -> list[FieldType]:
        """Добавляет тестовые типы кнопок в БД."""
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
        fields_types = []
        for field_type, values in types_names.items():
            fields_types.append(
                FieldType(
                    field_type=field_type,
                    name=values[0],
                    many=values[1],
                    )
                )
        return FieldType.objects.bulk_create(fields_types)

    def _add_surveys(self):
        """Добавление опросов."""
        surveys = []
        for i in range(1, 6):
            for j in range(1, 16):
                surveys.append(Survey(name=f'Опрос {i}-{j}'))
        return Survey.objects.bulk_create(surveys)

    def handle(self, *args, **options):
        self._add_fields_types()
        surveys = self._add_surveys()
        MainSurvey(
            main_survey=surveys[0],
            namespace='onboarding:index',
            ).save()
