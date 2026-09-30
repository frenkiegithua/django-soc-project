from django.contrib import admin
from .models import Alert

class AlertAdmin(admin.ModelAdmin):
    list_display = ('event', 'source_ip', 'destination_ip', 'severity', 'status', 'timestamp')
    list_filter = ('severity', 'status', 'timestamp')
    search_fields = ('event', 'source_ip', 'destination_ip', 'notes')
    fieldsets = (
        ('Alert Info', {
            'fields': ('event', 'protocol')
        }),
        ('IPs & Ports', {
            'fields': ('source_ip', 'source_port', 'destination_ip', 'destination_port')
        }),
        ('Severity & Status', {
            'fields': ('severity', 'status')
        }),
        ('Timing', {
            'fields': ('timestamp', 'event_time')
        }),
        ('Analysis', {
            'fields': ('notes',)
        }),
    )
    readonly_fields = ('timestamp',)

admin.site.register(Alert, AlertAdmin)