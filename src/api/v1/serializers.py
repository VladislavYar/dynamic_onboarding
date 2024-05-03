import json

from django.contrib.auth import get_user_model
from rest_framework import serializers

from onboarding.models import Survey, SurveyData

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        fields = ('id', 'email')
        model = User


class SurveySerializer(serializers.ModelSerializer):
    """Сериализатор опросов."""

    class Meta:
        fields = '__all__'
        model = Survey


class SurveyDataSerializer(serializers.ModelSerializer):
    """Сериализатор данных по опросам."""
    survey = SurveySerializer()
    user = UserSerializer()
    data = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = SurveyData

    def get_data(self, obj: SurveyData) -> str:
        """Сериализация в формат JSON."""
        return json.loads(obj.data)
