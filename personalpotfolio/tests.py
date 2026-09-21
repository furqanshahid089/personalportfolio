from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class PortfolioViewsTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Furqan Shahid')

    def test_contact_message_is_saved(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test Visitor',
            'email': 'visitor@email.com',
            'message': 'This is a valid test message.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'ok': True,
            'message': 'Thanks, your message has been sent successfully.',
        })
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_contact_message_is_rejected(self):
        response = self.client.post(reverse('contact'), {
            'name': '',
            'email': 'not-an-email',
            'message': 'short',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)
