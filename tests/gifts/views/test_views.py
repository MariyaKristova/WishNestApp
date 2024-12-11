from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from WishNestApp.gifts.models import Gift
from WishNestApp.wishnests.models import Wishnest
from WishNestApp.events.models import Event

UserModel = get_user_model()

class GiftViewsTestCase(TestCase):
    def setUp(self):

        self.user = UserModel.objects.create_user(
            email='testuser@test.com',
            password='123qwe456asd',
        )
        self.user2 = UserModel.objects.create_user(
            email='testuser2@test.com',
            password='123qwe456asd',
        )

        self.event1 = Event.objects.create(
            user=self.user,
            occasion="Birthday",
            date="2024-12-30",
            time="18:00:00",
            location="Party Hall"
        )

        self.event2 = Event.objects.create(
            user=self.user2,
            occasion="Christmas",
            date="2024-12-25",
            time="10:00:00",
            location="Christmas Park"
        )

        self.wishnest1 = Wishnest.objects.create(
            user=self.user,
            title="My Wishnest",
            event=self.event1
        )

        self.wishnest2 = Wishnest.objects.create(
            user=self.user2,
            title="Another Wishnest",
            event=self.event2
        )

        self.gift = Gift.objects.create(
            wishnest=self.wishnest1,
            description="Test Gift",
            price=10.00,
            user=self.user,
        )

        self.client.login(email='testuser@test.com', password='123qwe456asd')

    def test_gift_add(self):
        response = self.client.get(reverse('gift-add', kwargs={'wishnest_pk': self.wishnest1.pk}))
        self.assertEqual(response.status_code, 200)

        data = {
            'description': 'New Gift',
            'price': 15.00,
            'url': 'https://example.com/gift',
        }

        response = self.client.post(reverse('gift-add', kwargs={'wishnest_pk': self.wishnest1.pk}), data)
        self.assertRedirects(response, reverse('wishnest-details', kwargs={'pk': self.wishnest1.pk}))
        self.assertTrue(Gift.objects.filter(description='New Gift').exists())

    def test_gift_add_permission(self):
        response = self.client.get(reverse('gift-add', kwargs={'wishnest_pk': self.wishnest2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_gift_edit(self):
        data = {
            'description': 'Updated Gift',
            'price': 20.00,
            'url': 'https://example.com/updated-gift',
        }

        response = self.client.post(reverse('gift-edit', kwargs={'pk': self.gift.pk}), data)
        self.assertRedirects(response, reverse('gift-details', kwargs={'pk': self.gift.pk}))
        self.gift.refresh_from_db()
        self.assertEqual(self.gift.description, 'Updated Gift')

    def test_gift_edit_permission(self):
        self.client.logout()
        self.client.login(email='testuser2@test.com', password='123qwe456asd')

        data = {
            'description': 'Hacked Gift',
            'price': 30.00,
            'url': 'https://example.com/hacked-gift',
        }

        response = self.client.post(reverse('gift-edit', kwargs={'pk': self.gift.pk}), data)
        self.assertEqual(response.status_code, 403)

    def test_gift_delete(self):
        # Ensure the gift and wishnest are created in setUp
        self.client.login(email='testuser@test.com', password='password123')

        # Send the delete request
        response = self.client.post(reverse('gift-delete', kwargs={'pk': self.gift.pk}))

        # Check if the gift is deleted and the user is redirected to the correct wishnest details page
        self.assertRedirects(response, reverse('wishnest-details', kwargs={'pk': self.wishnest1.pk}))
        self.assertFalse(Gift.objects.filter(pk=self.gift.pk).exists())  # Ensure the gift no longer exists

    def test_gift_delete_permission(self):
        self.client.logout()
        self.client.login(email='testuser2@test.com', password='123qwe456asd')
        response = self.client.post(reverse('gift-delete', kwargs={'pk': self.gift.pk}))
        self.assertEqual(response.status_code, 403)

    def test_gift_details_registration(self):
        response = self.client.get(reverse('gift-details', kwargs={'pk': self.gift.pk}))
        self.assertEqual(response.status_code, 200)
        data = {}
        response = self.client.post(reverse('gift-details', kwargs={'pk': self.gift.pk}), data)
        self.assertRedirects(response, reverse('wishnest-details', kwargs={'pk': self.wishnest1.pk}))
        self.gift.refresh_from_db()
        self.assertTrue(self.gift.is_registered)
        self.assertEqual(self.gift.registered_by_email, self.user.email)
