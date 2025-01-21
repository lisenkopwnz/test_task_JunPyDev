from rest_framework.serializers import ModelSerializer

from finance.models import Revenue


class RevenueSerializer(ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'