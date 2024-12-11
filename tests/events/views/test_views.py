from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from WishNestApp.events.models import Event
from django.contrib.auth.models import Permission

UserModel = get_user_model()

class EventViewsTestCase(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='testuser@test.com',
            password='123qwe456asd',
        )
        self.user2 = UserModel.objects.create_user(
            email='testuser2@test.com',
            password='123qwe456asd',
        )
        self.superuser = UserModel.objects.create_superuser(
            email='superuser@test.com',
            password='123qwe456asd'
        )

    def test_create_event(self):
        self.client.login(email='testuser@test.com', password='123qwe456asd')
        url = reverse('event-create')
        data = {
            'occasion': 'Birthday',
            'date': '2024-12-30',
            'time': '19:00:00',
            'location': 'Playground Paradise',
            'description': 'A fun birthday party!'
        }
        response = self.client.post(url, data)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.occasion, 'Birthday')
        self.assertEqual(event.location, 'Playground Paradise')
        self.assertRedirects(response, reverse('dashboard'))

    def test_event_detail_view(self):
        event = Event.objects.create(
            user=self.user,
            occasion="Birthday",
            date="2024-12-30",
            time="19:00:00",
            location="Playground Paradise",
            description="A fun birthday party!"
        )

        url = reverse('event-details', kwargs={'pk': event.pk})
        response = self.client.get(url)

        self.assertContains(response, 'Playground Paradise')
        self.assertContains(response, 'A fun birthday party!')
        self.assertContains(response, 'Birthday')
        self.assertEqual(response.status_code, 200)

    def test_event_edit_view_permissions(self):
        event = Event.objects.create(
            user=self.user,
            occasion="Birthday",
            date="2024-12-30",
            time="19:00:00",
            location="Playground Paradise",
            description="A fun birthday party!"
        )

        url = reverse('event-edit', kwargs={'pk': event.pk})
        data = {
            'occasion': 'Wedding',
            'date': '2025-05-15',
            'time': '16:00:00',
            'location': 'Beach Resort',
            'description': 'A beautiful wedding event!'
        }
        response = self.client.post(url, data)

        self.assertRedirects(response, f'/accounts/login/?next={url}')
        self.client.login(email='superuser@test.com', password='123qwe456asd')
        response = self.client.post(url, data)
        event.refresh_from_db()
        self.assertEqual(event.occasion, 'Wedding')
        self.assertRedirects(response, reverse('event-details', kwargs={'pk': event.pk}))

    def test_event_delete_view_permissions(self):
        event = Event.objects.create(
            user=self.user,
            occasion="Birthday",
            date="2024-12-30",
            time="19:00:00",
            location="Playground Paradise",
            description="A fun birthday party!"
        )

        url = reverse('event-delete', kwargs={'pk': event.pk})
        response = self.client.post(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')


    def test_event_delete_view_permissions_admin(self):
        self.user2.user_permissions.add(Permission.objects.get(codename='delete_event'))

        event = Event.objects.create(
            user=self.user,
            occasion="Birthday",
            date="2024-12-30",
            time="19:00:00",
            location="Playground Paradise",
            description="A fun birthday party!"
        )

        self.client.login(email='testuser2@test.com', password='123qwe456asd')
        url = reverse('event-delete', kwargs={'pk': event.pk})
        response = self.client.post(url)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())
        self.assertRedirects(response, reverse('dashboard'))
