from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Service, Reservation, Feedback

User = get_user_model()

class ServiceModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Test Service",
            description="Test description",
            price=50.00,
            duration="01:00:00",
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Test Service")
        self.assertEqual(self.service.price, 50.00)
        self.assertEqual(str(self.service), "Test Service")


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.service = Service.objects.create(
            name="Test Service",
            description="Test description",
            price=50.00,
            duration="01:00:00",
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            service=self.service,
            reservation_date="2024-12-20",
            reservation_time="15:00:00",
            status="Pending",
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.user.username, "testuser")
        self.assertEqual(self.reservation.service.name, "Test Service")
        self.assertEqual(self.reservation.status, "Pending")
        self.assertEqual(
            str(self.reservation), "testuser - Test Service on 2024-12-20"
        )


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.service = Service.objects.create(
            name="Test Service",
            description="Test description",
            price=50.00,
            duration="01:00:00",
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            service=self.service,
            reservation_date="2024-12-20",
            reservation_time="15:00:00",
        )
        self.feedback = Feedback.objects.create(
            reservation=self.reservation,
            rating=5,
            comment="Excellent service!",
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.rating, 5)
        self.assertEqual(self.feedback.comment, "Excellent service!")
        self.assertEqual(
            str(self.feedback), "Feedback for Test Service by testuser"
        )
