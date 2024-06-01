from django.contrib import admin
from .models import Doctor, Patient, Visit, Specialization, Service

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Service)
admin.site.register(Specialization)
