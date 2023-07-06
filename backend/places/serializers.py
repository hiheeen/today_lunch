from rest_framework.serializers import ModelSerializer
from .models import Place
from users.serializers import UserSerializer

class PlaceSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Place
        fields = "__all__"
