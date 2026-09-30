from django.db import models

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
    
    class Meta:
        ordering = ['-timestamp']  # Newest first
        indexes = [
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event} - {self.severity} ({self.source_ip})"



