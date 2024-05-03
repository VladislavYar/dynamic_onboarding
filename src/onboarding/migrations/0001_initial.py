# Generated by Django 5.0.4 on 2024-05-03 00:33

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=255, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=300, populate_from='name', unique=True, verbose_name='Slug-название')),
                ('field_type', models.CharField(db_comment='Тип поля', help_text='Тип поля', max_length=30, unique=True, verbose_name='Тип поля')),
                ('many', models.BooleanField(db_comment='Множетсвенные значения', default=False, help_text='Множетсвенные значения', verbose_name='Множетсвенные значения')),
                ('regexp', models.CharField(blank=True, db_comment='Регулярное выражение', help_text='Регулярное выражение', max_length=255, null=True, verbose_name='Регулярное выражение')),
            ],
            options={
                'verbose_name': 'Тип поля',
                'verbose_name_plural': 'Типы полей',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=255, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=300, populate_from='name', unique=True, verbose_name='Slug-название')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.CharField(db_comment='Namespace страницы опроса', help_text='Namespace страницы опроса', max_length=255, verbose_name='Namespace страницы опроса')),
                ('main_survey', models.ForeignKey(db_comment='Начальный опрос', help_text='Начальный опрос', on_delete=django.db.models.deletion.CASCADE, related_name='main_surveys', to='onboarding.survey', verbose_name='Начальный опрос')),
            ],
            options={
                'verbose_name': 'Начальный опрос',
                'verbose_name_plural': 'Начальные опросы',
            },
        ),
        migrations.CreateModel(
            name='SurveyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, db_comment='Дата и время опроса', help_text='Дата и время опроса', verbose_name='Дата и время опроса')),
                ('data', models.JSONField(db_comment='Данные из опроса', help_text='Данные из опроса', verbose_name='Данные из опроса')),
                ('survey', models.ForeignKey(db_comment='Опрос', help_text='Опрос', on_delete=django.db.models.deletion.CASCADE, related_name='surveys_data', to='onboarding.survey', verbose_name='Опрос')),
                ('user', models.ForeignKey(db_comment='Клиент', help_text='Клиент', on_delete=django.db.models.deletion.CASCADE, related_name='surveys_data', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Данные по опросу',
                'verbose_name_plural': 'Данные по опросу',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=255, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=300, populate_from='name', unique=True, verbose_name='Slug-название')),
                ('question', models.CharField(blank=True, db_comment='Вопрос', help_text='Вопрос', max_length=255, null=True, verbose_name='Вопрос')),
                ('help_text', models.CharField(blank=True, db_comment='Текст помощи', help_text='Текст помощи', max_length=255, null=True, verbose_name='Текст помощи')),
                ('required', models.BooleanField(db_comment='Флаг обязательного поля', default=False, help_text='Флаг обязательного поля', verbose_name='Флаг обязательного поля')),
                ('field_type', models.ForeignKey(db_comment='Тип поля', help_text='Тип поля', on_delete=django.db.models.deletion.PROTECT, related_name='survey_fields', to='onboarding.fieldtype', verbose_name='Тип поля')),
                ('survey', models.ForeignKey(db_comment='Опрос', help_text='Опрос', on_delete=django.db.models.deletion.CASCADE, related_name='survey_fields', to='onboarding.survey', verbose_name='Опрос')),
            ],
            options={
                'verbose_name': 'Поле опроса',
                'verbose_name_plural': 'Поля опроса',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyUserStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, db_comment='Дата и время опроса', help_text='Дата и время опроса', verbose_name='Дата и время опроса')),
                ('callback_surveys', models.ManyToManyField(help_text='Последующие вопросы', to='onboarding.survey', verbose_name='Последующие вопросы')),
                ('main_survey', models.ForeignKey(blank=True, db_comment='Начальный опрос', help_text='Начальный опрос', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='surveys_users_status', to='onboarding.survey', verbose_name='Начальный опрос')),
                ('user', models.ForeignKey(db_comment='Клиент', help_text='Клиент', on_delete=django.db.models.deletion.CASCADE, related_name='surveys_users_status', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Статус пользователя в опросе',
                'verbose_name_plural': 'Статусы пользователей в опросах',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Название', help_text='Название', max_length=255, verbose_name='Название')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, db_comment='Slug-название', editable=False, help_text='Slug-название', max_length=300, populate_from='name', unique=True, verbose_name='Slug-название')),
                ('survey', models.ForeignKey(blank=True, db_comment='Онбординг', help_text='Онбординг', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='сhoices', to='onboarding.survey', verbose_name='Онбординг')),
                ('survey_field', models.ForeignKey(db_comment='Значение поля', help_text='Значение поля', on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='onboarding.surveyfield', verbose_name='Значение поля')),
            ],
            options={
                'verbose_name': 'Значение поля',
                'verbose_name_plural': 'Значения поля',
                'abstract': False,
                'unique_together': {('survey_field', 'survey')},
            },
        ),
    ]
