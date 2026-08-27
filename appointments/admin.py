from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'appointment_date',
        'appointment_time',
        'status',
        'created_at',
    )
    list_filter = ('status', 'appointment_date')
    search_fields = ('user__username', 'user__email', 'reason')
    list_editable = ('status',)
    ordering = ('appointment_date', 'appointment_time')
