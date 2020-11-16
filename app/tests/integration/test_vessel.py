from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vessels.models import Vessel, Equipment
from tests import test_utils
from django.utils.crypto import get_random_string
import json

class VesselAcceptanceTests(APITestCase):
    base_url = '/vessels/'

    def setUp(self):
        test_utils.populate_test_db()

    def test_create_vessel(self):
        """
        Ensure we can create a new vessel object.
        """
        new_code = get_random_string(5)
        data = {'code': new_code}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vessel.objects.filter(code=new_code).exists())

    def test_unique_vessel_code(self):
        """
        Ensure we can't create a vessel with a pre-existing code
        """
        data = {'code': test_utils.VESSEL_CODE}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_vessels(self):
        """
        Ensure we can list all vessels
        """
        response = self.client.get(self.base_url)
        self.assertEqual(len(json.loads(response.content)), len(Vessel.objects.all()))
        