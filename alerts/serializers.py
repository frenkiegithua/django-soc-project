from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    """Serializes Alert model to/from JSON."""
    
    class Meta:
        model = Alert
        fields = [
            'id', 'event', 'source_ip', 'destination_ip', 
            'source_port', 'destination_port', 'protocol',
            'severity', 'status', 'timestamp', 'event_time', 'notes'
        ]
        read_only_fields = ['id', 'timestamp']  # Can't edit these via API


class AlertDetailSerializer(serializers.ModelSerializer):
    """Extended serializer with all fields for detail views."""
    
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']