from django.contrib import admin

from . import models


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
