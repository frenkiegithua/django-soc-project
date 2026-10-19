from .models import AuditLog


def record_change(actor, target, field, old, new, action="update"):
    """Write one audit row. Skips the write if nothing actually changed."""
    old_str = None if old is None else str(old)
    new_str = None if new is None else str(new)

    if old_str == new_str:
        return None

    return AuditLog.objects.create(
        actor=actor,
        action=action,
        target_type=target.__class__.__name__,
        target_id=target.pk,
        field=field,
        old_value=old_str,
        new_value=new_str,
    )