from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.
def alert_list(request):
    """
      View that displays a list of security alerts.
      This is where we'll eventually alerts from the database.
    """
    alerts = [
        {
            'id' : 1,
            'source_ip' : '192.168.1.100',
            'destination_ip' : '10.0.0.50',
            'severity' : 'High',
            'event' : 'suspicious port scan detected',
            'timestamp' : '2026-09-26 17:30:00'
        },
        {
            'id' : 2,
            'source_ip' : '203.0.113.45',
            'destination_ip' : '10.0.0.1',
            'severity' : 'Critical',
            'event' : 'SQL injection attempt detected',
            'timestamp' : '2026-09-26 17:25:00'
        }
    ]

    html = """
    <h1>Soc Alert Dashboard</h1>
    <p>Total Alerts: {}</p>
    <ul>
    """.format(len(alerts))

    for alert in alerts:
        html += """
        <li>
            <strong>{}</strong> |
            severity: {} |
            source: {} |
            destination: {} |
            time: {} |
        </li>
        """.format(alert['event'], alert['severity'], alert['source_ip'], alert['destination_ip'], alert['timestamp'])
        html += "</ul>"
        return HttpResponse(html)    