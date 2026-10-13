from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)


def send_incident_email(incident):
    """Send email notification when incident is created."""
    try:
        subject = f"[SOC ALERT] Incident #{incident.id}: {incident.title}"
        
        # Create email body
        message = f"""
        Incident Created: {incident.title}
        Severity: {incident.severity}
        Status: {incident.status}
        Description: {incident.description}
        
        Linked Alerts: {incident.alerts.count()}
        Created by: {incident.created_by.username if incident.created_by else 'System'}
        
        View incident: http://localhost:8000/admin/alerts/incident/{incident.id}/change/
        """
        
        # Send email to all staff users
        staff_emails = [user.email for user in incident.created_by.groups.filter(name='SOC Team').values('user__email') if user.email]
        
        if staff_emails:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                staff_emails,
                fail_silently=True
            )
            logger.info(f"Email sent for incident {incident.id}")
    except Exception as e:
        logger.error(f"Failed to send email for incident {incident.id}: {e}")


def send_to_slack(incident):
    """Send incident notification to Slack."""
    if not settings.SLACK_WEBHOOK_URL:
        return
    
    try:
        payload = {
            "text": f"🚨 New Incident: {incident.title}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Incident #{incident.id}*\n*Severity:* {incident.severity}\n*Status:* {incident.status}\n*Description:* {incident.description}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Linked Alerts:* {incident.alerts.count()}\n*Created by:* {incident.created_by.username if incident.created_by else 'System'}"
                    }
                }
            ]
        }
        
        response = requests.post(settings.SLACK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"Slack notification sent for incident {incident.id}")
        else:
            logger.error(f"Slack notification failed: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send Slack notification: {e}")


def send_escalation_webhook(incident):
    """Send incident to external systems (ticketing, SOAR, etc)."""
    if not incident.severity in ['CRITICAL', 'HIGH']:
        return
    
    try:
        payload = {
            "incident_id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "alerts_count": incident.alerts.count(),
            "created_at": incident.created_at.isoformat(),
            "created_by": incident.created_by.username if incident.created_by else None
        }
        
        # Send to your external system
        # response = requests.post('https://your-ticketing-system.com/api/incidents', json=payload)
        logger.info(f"Escalation webhook prepared for incident {incident.id}")
    except Exception as e:
        logger.error(f"Failed to send escalation webhook: {e}")