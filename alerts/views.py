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