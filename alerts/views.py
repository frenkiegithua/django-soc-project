from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Alert
from .forms import AlertForm

def alert_list(request):
    """Display all alerts from the database, with optional filtering."""
    alerts = Alert.objects.all()
    
    # Filter by severity (optional GET parameter)
    severity = request.GET.get('severity')
    if severity:
        alerts = alerts.filter(severity=severity)
    
    # Filter by status (optional GET parameter)
    status = request.GET.get('status')
    if status:
        alerts = alerts.filter(status=status)
    
    context = {
        'alerts': alerts,
        'severity_filter': severity,
        'status_filter': status,
    }
    return render(request, 'alerts/alert_list.html', context)


def create_alert(request):
    """Handle alert creation via form submission."""
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            # Save the alert to the database
            alert = form.save()
            
            # Show success message
            messages.success(request, f"Alert '{alert.event}' created successfully!")
            
            # Redirect to alert list
            return redirect('alert_list')
    else:
        form = AlertForm()
    
    context = {'form': form}
    return render(request, 'alerts/create_alert.html', context)