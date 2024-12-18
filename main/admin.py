from django.contrib import admin
from .models import User, Service, Reservation, Feedback

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(Feedback)
