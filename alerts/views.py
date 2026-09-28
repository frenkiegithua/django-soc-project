from django.shortcuts import render
from django.http import HttpResponse
from .forms import AlertForm
from datetime import datetime

def alert_list(request):
    """
    View that displays a list of security alerts.
    """
    alerts = [
        {
            'id': 1,
            'source_ip': '192.168.1.100',
            'destination_ip': '10.0.0.50',
            'severity': 'High',
            'event': 'Suspicious port scan detected',
            'timestamp': '2026-09-26 17:30:00'
        },
        {
            'id': 2,
            'source_ip': '203.0.113.45',
            'destination_ip': '10.0.0.1',
            'severity': 'Critical',
            'event': 'SQL injection attempt detected',
            'timestamp': '2026-09-26 17:25:00'
        },
        {
            'id': 3,
            'source_ip': '192.0.2.100',
            'destination_ip': '10.0.0.25',
            'severity': 'Medium',
            'event': 'Failed login attempts from external IP',
            'timestamp': '2026-09-26 17:20:00'
        }
    ]
    
    context = {
        'alerts': alerts,
        'total_alerts': len(alerts),
    }
    
    return render(request, 'alerts/alert_list.html', context)


def create_alert(request):
    """
    View that handles creating a new security alert.
    GET: Display the form
    POST: Process the form submission
    """
    if request.method == 'POST':
        # User submitted the form
        form = AlertForm(request.POST)
        
        if form.is_valid():
            # Form data is clean and valid
            # Extract the validated data
            event = form.cleaned_data['event']
            source_ip = form.cleaned_data['source_ip']
            destination_ip = form.cleaned_data['destination_ip']
            severity = form.cleaned_data['severity']
            timestamp = form.cleaned_data['timestamp']
            
            # In a real app, save to database here
            # For now, just show success message
            message = f"Alert created: {event} from {source_ip}"
            
            context = {
                'form': form,
                'message': message,
                'success': True
            }
            return render(request, 'alerts/create_alert.html', context)
        else:
            # Form has errors
            context = {
                'form': form,
                'success': False
            }
            return render(request, 'alerts/create_alert.html', context)
    
    else:
        # GET request: Display empty form
        form = AlertForm()
        context = {
            'form': form,
            'success': None
        }
        return render(request, 'alerts/create_alert.html', context)