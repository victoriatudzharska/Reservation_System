from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ServiceListView, ServiceDetailView, ReservationCreateView, ReservationUpdateView, \
    ReservationDeleteView, custom_logout, update_profile, ServiceListCreateAPIView, ServiceDetailAPIView, \
    ReservationListCreateAPIView, ReservationDetailAPIView, FeedbackListCreateAPIView

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='service_list'), name='logout'),

    # Services
    path('', ServiceListView.as_view(), name='service_list'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),

    # Reservations
    path('reservations/', views.reservations_list, name='reservations'),
    path('reservations/create/', ReservationCreateView.as_view(), name='create_reservation'),
    path('reservations/update/<int:pk>/', ReservationUpdateView.as_view(), name='update_reservation'),
    path('reservations/delete/<int:pk>/', ReservationDeleteView.as_view(), name='delete_reservation'),
    path('reservations/edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),

    # Feedback
    path('feedback/<int:reservation_id>/', views.create_feedback, name='create_feedback'),

    # Profile
    path('profile/', views.update_profile, name='update_profile'),

    path('api/services/', ServiceListCreateAPIView.as_view(), name='api-services'),
    path('api/services/<int:pk>/', ServiceDetailAPIView.as_view(), name='api-service-detail'),
    path('api/reservations/', ReservationListCreateAPIView.as_view(), name='api-reservations'),
    path('api/reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='api-reservation-detail'),
    path('api/feedback/', FeedbackListCreateAPIView.as_view(), name='api-feedback'),
]