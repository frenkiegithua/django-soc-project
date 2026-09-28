from django import forms

class AlertForm(forms.Form):
    """
    Form for creating new security alert.
    """
    event = forms.CharField(
        label = 'Alert Event',
        max_length= 200,
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder' : 'e.g Suspicious port scan detected'
        })
    )

    source_ip = forms.GenericIPAddressField(
        label= 'Source IP Address',
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder' : 'e.g., 192.168.1.100'
        })
    )

    destination_ip = forms.GenericIPAddressField(
        label = 'Destination IP Address',
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 10.0.0.50'
        })
    )

    severity = forms.ChoiceField(
        label='Severity Level',
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Critical', 'Critical'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    timestamp = forms.DateTimeField(
        label='Alert Timestamp',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
