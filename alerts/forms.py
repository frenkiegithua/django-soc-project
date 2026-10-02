from django import forms
from .models import Alert

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['event', 'source_ip', 'destination_ip', 'source_port', 'destination_port', 'protocol', 'severity', 'status', 'event_time', 'notes']
        widgets = {
            'event': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Brute force SSH attempt'}),
            'source_ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.100'}),
            'destination_ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10.0.0.5'}),
            'source_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'destination_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 22, 443, 3306'}),
            'protocol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TCP, UDP, ICMP'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'event_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Analyst notes...'}),
        }