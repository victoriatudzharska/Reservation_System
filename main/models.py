from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.utils import timezone

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.username

# Service Model
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.DurationField(help_text="Duration of the service (e.g., 01:00:00 for 1 hour)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Reservation Model
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField(default=timezone.now)
    reservation_time = models.TimeField()
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.service.name} on {self.reservation_date}"

# Feedback Model
class Feedback(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveSmallIntegerField(help_text="Rate from 1 to 5")
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.reservation.service.name} by {self.reservation.user.username}"
