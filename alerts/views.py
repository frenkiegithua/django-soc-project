from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Alert
from .forms import AlertForm

def alert_list(request):
    """Display alerts with search, filtering, sorting, and pagination."""
    
    # Start with all alerts
    alerts = Alert.objects.all()
    
    # SEARCH: Filter by event, source_ip, destination_ip, or notes
    search_query = request.GET.get('q', '')
    if search_query:
        alerts = alerts.filter(
            Q(event__icontains=search_query) |
            Q(source_ip__icontains=search_query) |
            Q(destination_ip__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # FILTER: By severity
    severity = request.GET.get('severity')
    if severity:
        alerts = alerts.filter(severity=severity)
    
    # FILTER: By status
    status = request.GET.get('status')
    if status:
        alerts = alerts.filter(status=status)
    
    # SORT: Order by timestamp (newest first) or severity
    sort_by = request.GET.get('sort', '-timestamp')  # Default: newest first
    if sort_by in ['-timestamp', 'timestamp', '-severity', 'severity', '-event', 'event']:
        alerts = alerts.order_by(sort_by)
    
    # OPTIMIZE: Only fetch fields we use in the template
    # (This prevents N+1 query problem)
    alerts = alerts.values_list(
        'id', 'event', 'source_ip', 'destination_ip', 
        'destination_port', 'protocol', 'severity', 'status', 'timestamp'
    )
    
    # PAGINATION: Show 10 alerts per page
    paginator = Paginator(alerts, 10)
    page = request.GET.get('page', 1)
    
    try:
        alerts_page = paginator.page(page)
    except PageNotAnInteger:
        alerts_page = paginator.page(1)
    except EmptyPage:
        alerts_page = paginator.page(paginator.num_pages)
    
    context = {
        'alerts': alerts_page,
        'search_query': search_query,
        'severity_filter': severity,
        'status_filter': status,
        'sort_by': sort_by,
        'paginator': paginator,
        'page_obj': alerts_page,
    }
    return render(request, 'alerts/alert_list.html', context)


def create_alert(request):
    """Handle alert creation via form submission."""
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save()
            messages.success(request, f"Alert '{alert.event}' created successfully!")
            return redirect('alert_list')
    else:
        form = AlertForm()
    
    context = {'form': form}
    return render(request, 'alerts/create_alert.html', context)

# REST API VIEWS
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AlertSerializer, AlertDetailSerializer
import csv
from django.http import HttpResponse
from datetime import datetime


class AlertViewSet(viewsets.ModelViewSet):
    """
    REST API for Alert management.
    
    Endpoints:
    - GET    /api/alerts/                  - List all alerts
    - POST   /api/alerts/                  - Create new alert
    - GET    /api/alerts/<id>/             - Get alert details
    - PUT    /api/alerts/<id>/             - Update alert
    - DELETE /api/alerts/<id>/             - Delete alert
    - GET    /api/alerts/export/csv/       - Export to CSV
    - POST   /api/alerts/webhook/          - Webhook receiver
    """
    
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]  # In production, use IsAuthenticated
    
    def get_serializer_class(self):
        """Use detailed serializer for detail views."""
        if self.action == 'retrieve':
            return AlertDetailSerializer
        return AlertSerializer
    
    def get_queryset(self):
        """Support filtering via query parameters."""
        queryset = Alert.objects.all()
        
        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search
        search_query = self.request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(event__icontains=search_query) |
                Q(source_ip__icontains=search_query) |
                Q(destination_ip__icontains=search_query) |
                Q(notes__icontains=search_query)
            )
        
        # Sort
        ordering = self.request.query_params.get('ordering', '-timestamp')
        if ordering in ['-timestamp', 'timestamp', '-severity', 'severity', '-event', 'event']:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create alert with validation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='export/csv')
    def export_csv(self, request):
        """Export alerts to CSV format."""
        alerts = self.get_queryset()
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="alerts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow([
            'ID', 'Event', 'Source IP', 'Destination IP',
            'Source Port', 'Destination Port', 'Protocol',
            'Severity', 'Status', 'Timestamp', 'Event Time', 'Notes'
        ])
        
        # Write data rows
        for alert in alerts:
            writer.writerow([
                alert.id, alert.event, alert.source_ip, alert.destination_ip,
                alert.source_port or '', alert.destination_port or '', alert.protocol,
                alert.severity, alert.status, alert.timestamp, alert.event_time or '', alert.notes
            ])
        
        return response
    
    @action(detail=False, methods=['post'], url_path='webhook')
    def webhook(self, request):
        """
        Webhook receiver for SIEM systems (Splunk, ELK, etc).
        
        Expected JSON:
        {
            "event": "Failed login attempt",
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.5",
            "severity": "HIGH",
            "source_port": 54321,
            "destination_port": 22,
            "protocol": "TCP",
            "notes": "Received from Splunk webhook"
        }
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Add webhook source to notes
            notes = serializer.validated_data.get('notes', '')
            serializer.validated_data['notes'] = f"{notes} [Webhook: {request.META.get('REMOTE_ADDR')}]"
            
            self.perform_create(serializer)
            return Response(
                {'status': 'success', 'id': serializer.data['id']},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'status': 'error', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Quick endpoint to update only the status."""
        alert = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Alert.STATUS_CHOICES):
            return Response(
                {'error': f'Invalid status. Valid options: {list(dict(Alert.STATUS_CHOICES).keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alert.status = new_status
        alert.save()
        serializer = self.get_serializer(alert)
        return Response(serializer.data)