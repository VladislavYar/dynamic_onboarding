import copy

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from onboarding.constants import (MAX_LEN_FIELD_TYPE, MAX_LEN_HELP_TEXT,
                                  MAX_LEN_NAMESPACE, MAX_LEN_QUESTION,
                                  MAX_LEN_REGEXP, TYPES_FIELDS)

User = get_user_model()


class Survey(BaseModel):
    """Модель опроса."""

    class Meta(BaseModel.Meta):
        verbose_name = _('Опрос')
        verbose_name_plural = _('Опросы')


class SurveyData(models.Model):
    """Модель данных по опросу."""

    survey = models.ForeignKey(
        to=Survey,
        related_name='surveys_data',
        on_delete=models.CASCADE,
        verbose_name=_('Опрос'),
        help_text=_('Опрос'),
        db_comment=_('Опрос'),
        )
    user = models.ForeignKey(
        to=User,
        related_name='surveys_data',
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
        help_text=_('Клиент'),
        db_comment=_('Клиент'),
        )
    datetime = models.DateTimeField(
        verbose_name=_('Дата и время опроса'),
        help_text=_('Дата и время опроса'),
        db_comment=_('Дата и время опроса'),
        auto_now_add=True,
    )
    data = models.JSONField(
        verbose_name=_('Данные из опроса'),
        help_text=_('Данные из опроса'),
        db_comment=_('Данные из опроса'),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _('Данные по опросу')
        verbose_name_plural = _('Данные по опросу')

    def __str__(self) -> str:
        return f'{self.survey} | {self.user}'


class SurveyUserStatus(models.Model):
    """Модель статуса пользователя в опросе."""

    main_survey = models.ForeignKey(
        to=Survey,
        related_name='surveys_users_status',
        on_delete=models.CASCADE,
        verbose_name=_('Начальный опрос'),
        help_text=_('Начальный опрос'),
        db_comment=_('Начальный опрос'),
        null=True,
        blank=True,
        )
    callback_surveys = models.ManyToManyField(
                            to=Survey,
                            verbose_name=_('Последующие вопросы'),
                            help_text=_('Последующие вопросы'),
                        )
    user = models.ForeignKey(
        to=User,
        related_name='surveys_users_status',
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
        help_text=_('Клиент'),
        db_comment=_('Клиент'),
        )
    datetime = models.DateTimeField(
        verbose_name=_('Дата и время опроса'),
        help_text=_('Дата и время опроса'),
        db_comment=_('Дата и время опроса'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Статус пользователя в опросе')
        verbose_name_plural = _('Статусы пользователей в опросах')

    def __str__(self) -> str:
        return f'{self.main_survey} | {self.user}'


class MainSurvey(models.Model):
    """Модель начального опроса."""

    main_survey = models.ForeignKey(
        to=Survey,
        related_name='main_surveys',
        on_delete=models.CASCADE,
        verbose_name=_('Начальный опрос'),
        help_text=_('Начальный опрос'),
        db_comment=_('Начальный опрос'),
        )

    namespace = models.CharField(
        max_length=MAX_LEN_NAMESPACE,
        verbose_name=_('Namespace страницы опроса'),
        help_text=_('Namespace страницы опроса'),
        db_comment=_('Namespace страницы опроса'),
    )

    class Meta:
        verbose_name = _('Начальный опрос')
        verbose_name_plural = _('Начальные опросы')

    def __str__(self) -> str:
        return f'{self.main_survey} | {self.namespace}'


class FieldType(BaseModel):
    """Модель типа поля опроса."""

    field_type = models.CharField(
        max_length=MAX_LEN_FIELD_TYPE,
        verbose_name=_('Тип поля'),
        help_text=_('Тип поля'),
        db_comment=_('Тип поля'),
        unique=True,
    )
    many = models.BooleanField(
        verbose_name=_('Множетсвенные значения'),
        help_text=_('Множетсвенные значения'),
        db_comment=_('Множетсвенные значения'),
        default=False,
    )
    regexp = models.CharField(
        max_length=MAX_LEN_REGEXP,
        verbose_name=_('Регулярное выражение'),
        help_text=_('Регулярное выражение'),
        db_comment=_('Регулярное выражение'),
        null=True,
        blank=True,
        )

    class Meta(BaseModel.Meta):
        verbose_name = _('Тип поля')
        verbose_name_plural = _('Типы полей')

    def __str__(self) -> str:
        return f'{self.name} | {self.many}'

    def _validate_many_regexp(self, many: bool, regexp: str | None) -> None:
        """
        Валидация на множественность при регулярном выражении.
        """
        if many and regexp:
            raise ValidationError(
                _('Тип поля не может быть одновременно '
                  'множественным и с регулярным выражением.')
                )

    def _validate_type_in_types_fields(
            self, field_type: str, regexp: str | None
            ) -> None:
        """Проверка наличия типа поля в 'TYPES_FIELDS'."""
        if not regexp and field_type not in TYPES_FIELDS.keys():
            raise ValidationError(
                _('Такого типа поля не существует. '
                  'Напишите регулярное выражение.')
                )

    def clean(self, *args, **kwargs) -> None:
        """Валидация по нескольким полям."""
        self._validate_type_in_types_fields(self.field_type, self.regexp)
        self._validate_many_regexp(self.many, self.regexp)


class SurveyField(BaseModel):
    """Модель поля опроса."""

    question = models.CharField(
        max_length=MAX_LEN_QUESTION,
        verbose_name=_('Вопрос'),
        help_text=_('Вопрос'),
        db_comment=_('Вопрос'),
        null=True,
        blank=True,
    )
    field_type = models.ForeignKey(
        to=FieldType,
        on_delete=models.PROTECT,
        related_name='survey_fields',
        verbose_name=_('Тип поля'),
        help_text=_('Тип поля'),
        db_comment=_('Тип поля'),
        )
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name='survey_fields',
        verbose_name=_('Опрос'),
        help_text=_('Опрос'),
        db_comment=_('Опрос'),
        )
    help_text = models.CharField(
        max_length=MAX_LEN_HELP_TEXT,
        verbose_name=_('Текст помощи'),
        help_text=_('Текст помощи'),
        db_comment=_('Текст помощи'),
        null=True,
        blank=True,
        )
    required = models.BooleanField(
        verbose_name=_('Флаг обязательного поля'),
        help_text=_('Флаг обязательного поля'),
        db_comment=_('Флаг обязательного поля'),
        default=False,
    )

    class Meta(BaseModel.Meta):
        verbose_name = _('Поле опроса')
        verbose_name_plural = _('Поля опроса')


class Choice(BaseModel):
    """Модель значения поля."""

    error_message = _('Опрос "{}" вызывает бесконечный цикл ответов.')

    survey_field = models.ForeignKey(
        to=SurveyField,
        related_name='choices',
        on_delete=models.CASCADE,
        verbose_name=_('Значение поля'),
        help_text=_('Значение поля'),
        db_comment=_('Значение поля'),
        )
    survey = models.ForeignKey(
        to=Survey,
        related_name='сhoices',
        on_delete=models.SET_NULL,
        verbose_name=_('Онбординг'),
        help_text=_('Онбординг'),
        db_comment=_('Онбординг'),
        null=True,
        blank=True,
        )

    def _validate_repetition(
            self, survey_field: SurveyField, survey: Survey
            ) -> None:
        """Валидация на повторение опросов."""
        choices = self.survey_field.survey.survey_fields.exclude(
            id=self.survey_field.id
            ).values_list('choices', flat=True)
        child_surveys = Choice.objects.filter(id__in=choices).values_list(
            'survey', flat=True
            )
        error_message = _('Опрос "{}" уже добавлен в другое поле.')
        if self.survey.id in child_surveys:
            raise ValidationError(error_message.format(self.survey))

    def _validate_looping(
            self, parent_surveys: list[int], check_survey: int
            ) -> None:
        """Валидация на зацикливание опросов."""
        if check_survey in parent_surveys:
            raise ValidationError(self.error_message.format(self.survey))
        сhoices = Choice.objects.filter(
            survey_field__in=Survey.objects.get(
                id=check_survey
                ).survey_fields.all()
            )
        if not сhoices:
            return
        parent_surveys.append(check_survey)
        for child_survey in filter(
            None, сhoices.values_list('survey', flat=True)
        ):
            self._validate_looping(copy.deepcopy(parent_surveys), child_survey)

    def clean(self, *args, **kwargs) -> None:
        """Валидация по нескольким полям."""
        if not self.survey:
            return
        self._validate_repetition(self.survey_field, self.survey)
        if self.survey:
            self._validate_looping(
                [self.survey_field.survey.id], self.survey.id
                )

    class Meta(BaseModel.Meta):
        unique_together = ('survey_field', 'survey',)
        verbose_name = _('Значение поля')
        verbose_name_plural = _('Значения поля')
