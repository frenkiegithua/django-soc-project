from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
import csv
import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Alert, Incident
from .forms import AlertForm
from .serializers import AlertSerializer, AlertDetailSerializer, IncidentSerializer
from .signals import build_dashboard_stats

logger = logging.getLogger(__name__)


# ============================================================================
# WEB VIEWS (browser)
# ============================================================================

def alert_list(request):
    """Display alerts with search, filtering, sorting, and pagination."""
    alerts = Alert.objects.all()

    search_query = request.GET.get("q", "")
    if search_query:
        alerts = alerts.filter(
            Q(event__icontains=search_query)
            | Q(source_ip__icontains=search_query)
            | Q(destination_ip__icontains=search_query)
            | Q(notes__icontains=search_query)
        )

    severity = request.GET.get("severity")
    if severity:
        alerts = alerts.filter(severity=severity)

    status_filter = request.GET.get("status")
    if status_filter:
        alerts = alerts.filter(status=status_filter)

    sort_by = request.GET.get("sort", "-timestamp")
    if sort_by in ["-timestamp", "timestamp", "-severity", "severity", "-event", "event"]:
        alerts = alerts.order_by(sort_by)

    alerts = alerts.values_list(
        "id", "event", "source_ip", "destination_ip",
        "destination_port", "protocol", "severity", "status", "timestamp",
    )

    paginator = Paginator(alerts, 10)
    page = request.GET.get("page", 1)

    try:
        alerts_page = paginator.page(page)
    except PageNotAnInteger:
        alerts_page = paginator.page(1)
    except EmptyPage:
        alerts_page = paginator.page(paginator.num_pages)

    context = {
        "alerts": alerts_page,
        "search_query": search_query,
        "severity_filter": severity,
        "status_filter": status_filter,
        "sort_by": sort_by,
        "paginator": paginator,
        "page_obj": alerts_page,
    }
    return render(request, "alerts/alert_list.html", context)


def create_alert(request):
    """Handle alert creation via form submission."""
    if request.method == "POST":
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save()
            messages.success(request, f"Alert '{alert.event}' created successfully!")
            return redirect("alert_list")
    else:
        form = AlertForm()

    return render(request, "alerts/create_alert.html", {"form": form})


@login_required
def dashboard(request):
    """Real-time SOC dashboard. Requires a logged-in session; no API token in the page."""
    return render(request, "alerts/dashboard.html")


# ============================================================================
# REST API VIEWS
# ============================================================================

class AlertViewSet(viewsets.ModelViewSet):
    """REST API for Alert management (requires authentication)."""

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AlertDetailSerializer
        return AlertSerializer

    def get_queryset(self):
        queryset = Alert.objects.all()

        severity = self.request.query_params.get("severity")
        if severity:
            queryset = queryset.filter(severity=severity)

        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search_query = self.request.query_params.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(event__icontains=search_query)
                | Q(source_ip__icontains=search_query)
                | Q(destination_ip__icontains=search_query)
                | Q(notes__icontains=search_query)
            )

        ordering = self.request.query_params.get("ordering", "-timestamp")
        if ordering in ["-timestamp", "timestamp", "-severity", "severity", "-event", "event"]:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="export/csv", permission_classes=[IsAuthenticated])
    def export_csv(self, request):
        alerts = self.get_queryset()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="alerts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow([
            "ID", "Event", "Source IP", "Destination IP",
            "Source Port", "Destination Port", "Protocol",
            "Severity", "Status", "Timestamp", "Event Time", "Notes",
            "Created By", "Modified By",
        ])

        for alert in alerts:
            writer.writerow([
                alert.id, alert.event, alert.source_ip, alert.destination_ip,
                alert.source_port or "", alert.destination_port or "", alert.protocol,
                alert.severity, alert.status, alert.timestamp, alert.event_time or "",
                alert.notes,
                alert.created_by.username if alert.created_by else "",
                alert.modified_by.username if alert.modified_by else "",
            ])

        return response

    @action(detail=False, methods=["post"], url_path="webhook", permission_classes=[AllowAny])
    def webhook(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            notes = serializer.validated_data.get("notes", "")
            serializer.validated_data["notes"] = f"{notes} [Webhook from {request.META.get('REMOTE_ADDR')}]"

            system_user, _ = User.objects.get_or_create(username="webhook_system")
            serializer.save(created_by=system_user)

            return Response(
                {"status": "success", "id": serializer.data["id"]},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        alert = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Alert.STATUS_CHOICES):
            return Response(
                {"error": f"Invalid status. Valid options: {list(dict(Alert.STATUS_CHOICES).keys())}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        alert.status = new_status
        alert.modified_by = request.user
        alert.save()
        return Response(self.get_serializer(alert).data)


class IncidentViewSet(viewsets.ModelViewSet):
    """REST API for Incident management (requires authentication)."""

    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        incident = serializer.save(created_by=self.request.user)

        try:
            from .notifications import send_incident_email, send_to_slack, send_escalation_webhook
            send_incident_email(incident)
            send_to_slack(incident)
            send_escalation_webhook(incident)
        except Exception as e:
            logger.error(f"Notification error for incident {incident.id}: {e}")

    @action(detail=True, methods=["patch"])
    def resolve(self, request, pk=None):
        incident = self.get_object()
        incident.status = "RESOLVED"
        incident.resolved_at = timezone.now()
        incident.save()
        return Response(self.get_serializer(incident).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def alert_stats(request):
    """Alert statistics for dashboard."""
    total = Alert.objects.count()
    critical = Alert.objects.filter(severity="CRITICAL").count()
    high = Alert.objects.filter(severity="HIGH").count()
    medium = Alert.objects.filter(severity="MEDIUM").count()
    low = Alert.objects.filter(severity="LOW").count()
    open_alerts = Alert.objects.filter(status="OPEN").count()
    resolved = Alert.objects.filter(status="RESOLVED").count()

    return Response({
        "total": total,
        "by_severity": {"critical": critical, "high": high, "medium": medium, "low": low},
        "by_status": {"open": open_alerts, "resolved": resolved},
        "percentage_critical": round((critical / total * 100) if total > 0 else 0, 2),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def alert_count(request):
    """Real-time open counts. Same payload the WebSocket pushes."""
    return Response(build_dashboard_stats())