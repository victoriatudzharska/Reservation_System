from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Service, Reservation, Feedback

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2']

# Service Form
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'e.g., 01:00:00 for 1 hour'})
        }

# Reservation Form
class ReservationForm(forms.ModelForm):
    reservation_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    reservation_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Reservation
        fields = ['service', 'reservation_date', 'reservation_time']

# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
        }

# User Profile Form
class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'date_of_birth']
