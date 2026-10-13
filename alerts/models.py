from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    # Severity choices
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('FALSE_POSITIVE', 'False Positive'),
    ]
    
    # Fields
    event = models.CharField(max_length=255, help_text="Type of security event")
    source_ip = models.GenericIPAddressField(help_text="Source IP address")
    destination_ip = models.GenericIPAddressField(help_text="Destination IP address")
    source_port = models.IntegerField(null=True, blank=True)
    destination_port = models.IntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=10, default='TCP', help_text="TCP, UDP, ICMP, etc.")
    
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When alert was created")
    event_time = models.DateTimeField(null=True, blank=True, help_text="When the event occurred")
    
    notes = models.TextField(blank=True, help_text="Analyst notes")
    
    # AUDIT TRAIL: Track who created and modified
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='alerts_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='alerts_modified')
    modified_at = models.DateTimeField(auto_now=True, help_text="Last modification time")
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
            models.Index(fields=['timestamp']),
        ]
        permissions = [
            ('can_resolve_critical', 'Can resolve critical alerts'),
            ('can_export_alerts', 'Can export alerts to CSV'),
        ]
    
    def __str__(self):
        return f"{self.event} - {self.severity} ({self.source_ip})"

from django.utils import timezone
from datetime import timedelta

class AlertAnalytics(models.Model):
    """Track alert statistics for dashboards."""
    date = models.DateField(auto_now_add=True)
    total_alerts = models.IntegerField(default=0)
    critical_alerts = models.IntegerField(default=0)
    high_alerts = models.IntegerField(default=0)
    medium_alerts = models.IntegerField(default=0)
    low_alerts = models.IntegerField(default=0)
    resolved_alerts = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"


class Incident(models.Model):
    """Group related alerts into incidents."""
    INCIDENT_STATUS = [
        ('NEW', 'New'),
        ('INVESTIGATING', 'Investigating'),
        ('CONTAINED', 'Contained'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=Alert.SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=INCIDENT_STATUS, default='NEW')
    alerts = models.ManyToManyField(Alert, related_name='incidents')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"INC-{self.id}: {self.title}"