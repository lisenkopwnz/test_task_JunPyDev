from rest_framework.serializers import ModelSerializer

from finance.models import Revenue


class RevenueSerializer(ModelSerializer):
    """Сериализатор для модели Revenue. Включает все поля модели."""

    class Meta:
        model = Revenue
        fields = '__all__'
