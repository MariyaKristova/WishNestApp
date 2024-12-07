from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from WishNestApp.events.models import Event
from WishNestApp.wishnests.models import Wishnest

UserModel = get_user_model()

class WishnestViewsTestCase(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='testuser@test.com',
            password='123qwe456asd',
        )
        self.user2 = UserModel.objects.create_user(
            email='testuser2@test.com',
            password='123qwe456asd',
        )

        self.event = Event.objects.create(
            user=self.user,
            occasion="Birthday",
            date="2024-12-30",
            time="19:00:00",
            location="Playground Paradise",
            description="A fun birthday party!"
        )

        self.wishnest = Wishnest.objects.create(
            title="Toy Car",
            user=self.user,
            event=self.event
        )

    def test_wishnest_add_view(self):
        self.client.login(email='testuser@test.com', password='123qwe456asd')

        url = reverse('wishnest-add', kwargs={'event_pk': self.event.pk})
        data = {
            'title': 'Lego Set'
        }
        response = self.client.post(url, data)

        self.assertEqual(Wishnest.objects.count(), 2)
        wishnest = Wishnest.objects.last()
        self.assertEqual(wishnest.title, 'Lego Set')
        self.assertEqual(wishnest.event, self.event)
        self.assertEqual(wishnest.user, self.user)
        self.assertRedirects(response, reverse('wishnest-details', kwargs={'pk': wishnest.pk}))

    def test_wishnest_add_view_unauthorized_user(self):
        self.client.login(email='testuser2@test.com', password='123qwe456asd')
        url = reverse('wishnest-add', kwargs={'event_pk': self.event.pk})
        data = {
            'title': 'Lego Set'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_wishnest_details_view(self):
        self.client.login(email='testuser@test.com', password='123qwe456asd')
        url = reverse('wishnest-details', kwargs={'pk': self.wishnest.pk})
        response = self.client.get(url)
        self.assertContains(response, self.wishnest.title)

    def test_wishnest_delete_view_authorized_user(self):
        self.client.login(email='testuser@test.com', password='123qwe456asd')

        self.assertTrue(Wishnest.objects.filter(pk=self.wishnest.pk).exists())

        url = reverse('wishnest-delete', kwargs={'pk': self.wishnest.pk})  # Only pass pk here
        response = self.client.post(url)

        self.assertFalse(Wishnest.objects.filter(pk=self.wishnest.pk).exists())

        self.assertRedirects(response, reverse('event-details', kwargs={'pk': self.event.pk}))

    def test_wishnest_delete_view_unauthorized_user(self):
        self.client.login(email='testuser2@test.com', password='123qwe456asd')

        url = reverse('wishnest-delete', kwargs={'pk': self.wishnest.pk})  # Only pass pk here
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)
