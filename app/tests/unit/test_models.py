from django.test import TestCase
from vessels.models import Vessel, Equipment
from tests import test_utils
from django.db import IntegrityError


class VesselModelTestCase(TestCase):
    def setUp(self):
        test_utils.populate_test_db()

    def test_vessel_unique_code(self):
        """Vessels have unique codes"""
        with self.assertRaises(Exception) as raised: 
            Vessel.objects.create(code=test_utils.VESSEL_CODE)
        self.assertEqual(IntegrityError, type(raised.exception))

class EquipmentModelTestCase(TestCase):
    def setUp(self):
        test_utils.populate_test_db()

    def test_equipment_unique_code(self):
        """Equipments have unique codes"""
        with self.assertRaises(Exception) as raised: 
            Equipment.objects.create(code=test_utils.EQUIPMENT_CODE,
                                    name='compressor',
                                    location='Brasil',
                                    vessel=test_utils.get_vessel())
        self.assertEqual(IntegrityError, type(raised.exception))
    
    def test_equipment_has_all_fields(self):
        """Equipments must have location, name, code, status and be associated with a vessel"""
        required_fields = [field.name for field in Equipment._meta.get_fields() if not getattr(field, 'blank', False) is True]
        self.assertCountEqual(required_fields, ['location', 'name', 'code', 'vessel', 'status'])

    def test_new_equipment_has_active_status(self):
        """All new Equipments are activated"""
        equipment = Equipment.objects.create(code="t_active",
                                    name='compressor',
                                    location='Brasil',
                                    vessel=test_utils.get_vessel())
        self.assertEqual(equipment.status, "active")