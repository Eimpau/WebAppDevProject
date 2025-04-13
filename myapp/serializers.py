from rest_framework import serializers

from .models import Machine

class MachineSerializer(serializers.ModelSerializer):
    """
    Serializer for the Machine model.
    This serializer converts the Machine model to a JSON format with specific fields needed for the REST API.
    """
    class Meta:
        model = Machine
        fields = ['id', 'name', 'status', 'updated_at']