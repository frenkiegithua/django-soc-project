from django.shortcuts import render
from django.http import HttpResponse

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
            'id' : 3,
            'source_ip' : '192.0.2.100',
            'destination_ip' : '10.0.0.25',
            'severity' : 'Medium',
            'event' : 'Failed login attempts from external IP',
            'timestamp' : '2026-09-26 17:20:00'
        }
    ]
    
    context = {
        'alerts': alerts,
        'total_alerts': len(alerts),
    }
    
    return render(request, 'alerts/alert_list.html', context)