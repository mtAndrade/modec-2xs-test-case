from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vessels.models import Vessel, Equipment
from tests import test_utils
from django.utils.crypto import get_random_string
import json


class EquipmentAcceptanceTests(APITestCase):
    base_url = f"/vessels/{test_utils.VESSEL_CODE}/equipments/"

    def setUp(self):
        test_utils.populate_test_db()

    def test_create_equipment(self):
        """
        Ensure we can create a new equipment with active status.
        """
        new_code = get_random_string(5)
        data = {'code': new_code, 'name':'test_name', 'location':'test_location'}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Equipment.objects.filter(code=new_code).exists())
        self.assertEqual(Equipment.objects.filter(code=new_code).get().vessel.code, test_utils.VESSEL_CODE)
        self.assertEqual(Equipment.objects.filter(code=new_code).get().status, "active")

    def test_unique_equipment_code(self):
        """
        Ensure we can't create a equipment with a pre-existing code.
        """
        data = {'code': test_utils.EQUIPMENT_CODE, 'name':'test_name', 'location':'test_location'}
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deactivate_one_equipment(self):
        """
        Ensure we can deactivate one equipment.
        """
        data = [test_utils.EQUIPMENT_CODE]
        deactivate_url = '/equipments/deactivate/'
        response = self.client.patch(deactivate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.get(code=test_utils.EQUIPMENT_CODE).status, "inactive")

    def test_deactivate_multiple_equipments(self):
        """
        Ensure we can deactivate more than one equipment.
        """
        data = [test_utils.EQUIPMENT_CODE, test_utils.EQUIPMENT_CODE_2]
        deactivate_url = '/equipments/deactivate/'
        response = self.client.patch(deactivate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.get(code=test_utils.EQUIPMENT_CODE).status, "inactive")
        self.assertEqual(Equipment.objects.get(code=test_utils.EQUIPMENT_CODE_2).status, "inactive")

    def test_deactivate_equipments_with_invalid_code(self):
        """
        Ensure batch deactivate only when all equipments codes are valid.
        """
        data = [test_utils.EQUIPMENT_CODE, test_utils.EQUIPMENT_CODE_2, "invalid_code"]
        deactivate_url = '/equipments/deactivate/'
        response = self.client.patch(deactivate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Equipment.objects.get(code=test_utils.EQUIPMENT_CODE).status, "active")
        self.assertEqual(Equipment.objects.get(code=test_utils.EQUIPMENT_CODE_2).status, "active")

    def test_list_all_active_equipments_from_vessel(self):
        """
        Ensure we can list all active equipment from a vessel
        """
        response = self.client.get(self.base_url)
        test_vessel = test_utils.get_vessel(code=test_utils.VESSEL_CODE)

        self.assertEqual(
            len(json.loads(response.content)),
            len(Equipment.objects.filter(vessel=test_vessel, status="active")))
        
    def test_list_only_active_equipments_from_vessel(self):
        """
        Ensure we can list all active equipment from a vessel
        """
        test_vessel = test_utils.get_vessel(code=test_utils.VESSEL_CODE)
        Equipment.objects.create(
                    code=get_random_string(8),
                    name='test_name',
                    location='test_location',
                    vessel=test_vessel,
                    status="inactive")
        response = self.client.get(self.base_url)
        inactive_equipments = Equipment.objects.filter(vessel=test_vessel, status='inactive')
        self.assertEqual(
            len(json.loads(response.content)),
            len(Equipment.objects.filter(vessel=test_vessel, status="active")))
        self.assertTrue(len(inactive_equipments) > 0 )