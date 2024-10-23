from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Subscription

class SubscriptionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.subscription_data = {
            'subscription_type': 'Premium',
            'price': 9.99,
            'duration': 30,
            'user_id': self.user.id,
            'start_date': '2024-11-01',
        }

    def test_create_subscription(self):
        response = self.client.post('/api/subscriptions/', self.subscription_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_subscriptions(self):
        Subscription.objects.create(**self.subscription_data)
        response = self.client.get('/api/subscriptions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subscription_type'], 'Premium')

    def test_update_subscription(self):
        subscription = Subscription.objects.create(**self.subscription_data)
        updated_data = {
            'subscription_type': 'Gold',
            'price': 14.99,
            'duration': 60,
        }
        response = self.client.put(f'/api/subscriptions/{subscription.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription.refresh_from_db()
        self.assertEqual(subscription.subscription_type, 'Gold')

    def test_delete_subscription(self):
        subscription = Subscription.objects.create(**self.subscription_data)
        response = self.client.delete(f'/api/subscriptions/{subscription.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)

