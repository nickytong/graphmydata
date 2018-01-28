from rest_framework import serializers
from .models import SimpleRandomization
class SimpleRandomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleRandomization