from django.forms import (CharField, DateField, DateTimeField, EmailField,
                          IntegerField, TimeField, URLField)

from onboarding.fields import CastomChoiceField, CastomMultipleChoiceField

MAX_LEN_FIELD_TYPE = 30
MAX_LEN_HELP_TEXT = 255
MAX_LEN_QUESTION = 255
MAX_LEN_NAMESPACE = 255
MAX_LEN_REGEXP = 255
TYPES_FIELDS = {
    'checkbox': CastomMultipleChoiceField,
    'date': DateField,
    'datetime-local': DateTimeField,
    'email': EmailField,
    'number': IntegerField,
    'radio': CastomChoiceField,
    'text': CharField,
    'time': TimeField,
    'url': URLField,
}
