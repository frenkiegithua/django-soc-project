from rest_framework.permissions import BasePermission

ANALYST_GROUP = "SOC Analyst"
LEAD_GROUP = "SOC Lead"

# Alert statuses that count as handled. Anything else keeps the incident blocked.
HANDLED_ALERT_STATUSES = ("RESOLVED", "FALSE_POSITIVE")


def is_lead(user):
    """Superusers count as leads so the Django admin is never locked out."""
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=LEAD_GROUP).exists()
    )


def is_soc_member(user):
    return user.is_authenticated and (
        is_lead(user) or user.groups.filter(name=ANALYST_GROUP).exists()
    )


def can_assign(user, incident, new_assignee):
    """
    Leads can do anything.
    Analysts can claim an unassigned incident for themselves,
    and can unassign themselves from an incident they own.
    Everything else (taking over or moving someone else's incident) is lead-only.
    """
    if is_lead(user):
        return True
    if new_assignee == user:
        return incident.assigned_to in (None, user)
    if new_assignee is None:
        return incident.assigned_to == user
    return False


def can_resolve(user, incident):
    """Leads can resolve any incident. Analysts only the ones they own."""
    return is_lead(user) or incident.assigned_to == user


def open_alert_count(incident):
    """Number of linked alerts that are not yet handled."""
    return incident.alerts.exclude(status__in=HANDLED_ALERT_STATUSES).count()


class IsSOCMember(BasePermission):
    message = "You must belong to the SOC Analyst or SOC Lead group."

    def has_permission(self, request, view):
        return is_soc_member(request.user)
