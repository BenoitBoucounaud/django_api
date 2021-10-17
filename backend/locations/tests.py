from django.test import TestCase
from rest_framework.test import APIRequestFactory

from locations import views


class RegionViewTests(TestCase):

    def test_get_region(self):
        request = APIRequestFactory().get('/regions/')
        response = views.region_list(request)
        self.assertEqual(response.status_code, 200)

    def test_post_region(self):
        request = APIRequestFactory().post(
            '/regions/', {'code': 91, 'name': 'Essonne'})
        response = views.region_list(request)
        self.assertEqual(response.status_code, 405)

    # No put, patch or delete tests bcs url regions/<int:code> doesn't exist
