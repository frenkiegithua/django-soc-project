from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Alert, Incident


def build_dashboard_stats():
    """Single source of truth for every dashboard number."""
    critical = Alert.objects.filter(severity="CRITICAL", status="OPEN").count()
    high = Alert.objects.filter(severity="HIGH", status="OPEN").count()
    total_open = Alert.objects.filter(status="OPEN").count()
    open_incidents = Incident.objects.exclude(status__in=["RESOLVED", "CLOSED"]).count()

    return {
        "critical_open": critical,
        "high_open": high,
        "total_open": total_open,
        "open_incidents": open_incidents,
        "needs_immediate_attention": critical > 0,
    }


def broadcast_dashboard():
    """Push current stats to every connected dashboard."""
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "dashboard_update",
            "data": build_dashboard_stats(),
        },
    )


@receiver(post_save, sender=Alert)
def alert_changed(sender, instance, created, **kwargs):
    broadcast_dashboard()


@receiver(post_save, sender=Incident)
def incident_changed(sender, instance, created, **kwargs):
    broadcast_dashboard()