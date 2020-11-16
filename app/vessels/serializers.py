from rest_framework import serializers
from vessels import models
import logging


logger = logging.getLogger(__name__)

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = [
            "vessel",
            "name",
            "code",
            "location",
            "status"
        ]


class VesselSerializer(serializers.ModelSerializer):
    equipments = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Vessel
        fields = ["code", "equipments", "created_at", "updated_at"]