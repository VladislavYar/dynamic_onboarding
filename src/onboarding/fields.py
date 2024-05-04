from django.forms import (CheckboxSelectMultiple, ChoiceField,
                          MultipleChoiceField)
from django.forms.widgets import RadioSelect


class CastomChoiceField(ChoiceField):
    """Кастомное поле выбора."""

    widget = RadioSelect


class CastomMultipleChoiceField(MultipleChoiceField):
    """Кастомное поле множественного выбора."""

    widget = CheckboxSelectMultiple
