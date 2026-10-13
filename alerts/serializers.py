from rest_framework import serializers
from .models import Alert, Incident


# ============================================================================
# ALERT SERIALIZERS
# ============================================================================

class AlertSerializer(serializers.ModelSerializer):
    """Serializes Alert model to/from JSON."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    modified_by_username = serializers.CharField(source='modified_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Alert
        fields = [
            'id', 'event', 'source_ip', 'destination_ip', 
            'source_port', 'destination_port', 'protocol',
            'severity', 'status', 'timestamp', 'event_time', 'notes',
            'created_by', 'created_by_username', 'modified_by', 'modified_by_username'
        ]
        read_only_fields = ['id', 'timestamp', 'created_by', 'modified_by']


class AlertDetailSerializer(serializers.ModelSerializer):
    """Extended serializer with all fields for detail views."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    modified_by_username = serializers.CharField(source='modified_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'created_by', 'modified_by']


# ============================================================================
# INCIDENT SERIALIZERS
# ============================================================================

class IncidentSerializer(serializers.ModelSerializer):
    """Serializes Incident model to/from JSON."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True, allow_null=True, required=False)
    
    class Meta:
        model = Incident
        fields = [
            'id', 'title', 'description', 'severity', 'status',
            'alerts', 'created_by', 'created_by_username', 
            'assigned_to', 'assigned_to_username', 
            'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 
            'created_by', 'created_by_username', 'assigned_to_username'
        ]