from django.contrib.auth.models import User
from vessels.models import Vessel, Equipment


VESSEL_CODE='MV102'
EQUIPMENT_CODE='5310B9D7'
EQUIPMENT_CODE_2='1210B9D7'

def populate_test_db():
    """
    Adds records to an empty test database
    """
    vessel = Vessel.objects.create(code=VESSEL_CODE)
    Equipment.objects.create(
                            code=EQUIPMENT_CODE,
                            name='compressor',
                            location='Brasil',
                            vessel=vessel)
    Equipment.objects.create(
                            code=EQUIPMENT_CODE_2,
                            name='compressor',
                            location='Brasil',
                            vessel=vessel)

def get_vessel(code=None):
    """ 
    Returns a vessel, may be specified by its code 
    """
    if code:
        return Vessel.objects.get(pk=code)
    return Vessel.objects.all().first()

