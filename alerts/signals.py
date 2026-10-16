from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Alert


def build_dashboard_stats():
    """Single source of truth for the dashboard numbers."""
    critical = Alert.objects.filter(severity="CRITICAL", status="OPEN").count()
    high = Alert.objects.filter(severity="HIGH", status="OPEN").count()
    total_open = Alert.objects.filter(status="OPEN").count()
    return {
        "critical_open": critical,
        "high_open": high,
        "total_open": total_open,
        "needs_immediate_attention": critical > 0,
    }


@receiver(post_save, sender=Alert)
def push_dashboard_update(sender, instance, created, **kwargs):
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