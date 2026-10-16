from django.contrib import admin
from .models import Alert, Incident


class AlertAdmin(admin.ModelAdmin):
    list_display = ('event', 'source_ip', 'destination_ip', 'severity', 'status', 'timestamp')
    list_filter = ('severity', 'status', 'timestamp')
    search_fields = ('event', 'source_ip', 'destination_ip', 'notes')
    fieldsets = (
        ('Alert Info', {'fields': ('event', 'protocol')}),
        ('IPs & Ports', {'fields': ('source_ip', 'source_port', 'destination_ip', 'destination_port')}),
        ('Severity & Status', {'fields': ('severity', 'status')}),
        ('Timing', {'fields': ('timestamp', 'event_time')}),
        ('Analysis', {'fields': ('notes',)}),
    )
    readonly_fields = ('timestamp',)


class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'status', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('severity', 'status', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('alerts',)


admin.site.register(Alert, AlertAdmin)
admin.site.register(Incident, IncidentAdmin)