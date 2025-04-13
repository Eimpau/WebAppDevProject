from rest_framework import serializers

from .models import Machine

class MachineWarningSerializer(serializers.Serializer):
    """
    Serializer for the Machine model.
    This serializer class is used to change status state of a machine.
    """
    id = serializers.IntegerField()  # Assuming the machine is identified by an ID.
    status = serializers.ChoiceField(choices=[('Warning', 'Warning'), ('Fault', 'Fault'), ('OK', 'OK')])


class MachineStatusSerializer(serializers.ModelSerializer):
     """
     Serializer for the Machine model.
     This serializer converts the Machine model to a JSON format with specific fields needed for the REST API.
     """
     class Meta:
         model = Machine
         # Only display the necessary fields in the API response.
         fields = ['id', 'name', 'status', 'updated_at']