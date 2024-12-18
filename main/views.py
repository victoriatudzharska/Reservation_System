from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework import generics

from .forms import UserRegistrationForm, ReservationForm, FeedbackForm, UserProfileForm
from .models import Service, Reservation, Feedback
from .serializers import FeedbackSerializer, ReservationSerializer, ServiceSerializer


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Service List View
@login_required(login_url='register')
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})


# Reservation Create View
@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, 'Reservation created successfully!')
            return redirect('reservations')
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})


# User Reservations List View
@login_required
def reservations_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations_list.html', {'reservations': reservations})


# Feedback Create View
@login_required
def create_feedback(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if hasattr(reservation, 'feedback'):
        messages.error(request, "Feedback already exists for this reservation.")
        return redirect('reservations')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.reservation = reservation
            feedback.save()
            messages.success(request, "Your feedback was submitted successfully!")
            return redirect('reservations')
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form, 'reservation': reservation})


# User Profile Update View
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('update_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile_update.html', {'form': form})


def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "The reservation was successfully deleted.")
        return redirect('reservations')
    return render(request, 'reservation_confirm_delete.html', {'reservation': reservation})


def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation_form.html', {'form': form})


# ----- Class-Based Views -----

# Service List View (CBV)
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'


# Service Detail View (CBV)
class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'
    login_url = 'login'


# Reservation Create View (CBV)
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('reservations')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Reservation created successfully!')
        return super().form_valid(form)


# Reservation Update View (CBV)
class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('reservations')

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


# Reservation Delete View (CBV)
class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservations')

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

def custom_logout(request):
    return None

# API
class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# API
class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# API
class ReservationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# API
class ReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# API
class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

