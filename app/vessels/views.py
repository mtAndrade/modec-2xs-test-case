from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from vessels import models, serializers
import logging


logger = logging.getLogger(__name__)


class VesselViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    """
    queryset = models.Vessel.objects.all().order_by('-created_at')
    serializer_class = serializers.VesselSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows equipments to be viewed or edited.
    """
    queryset = models.Equipment.objects.all().order_by('-created_at')
    serializer_class = serializers.EquipmentSerializer

    def get_queryset(self):
        return models.Equipment.objects.filter(
            vessel=self.kwargs['vessel_pk'],
            status="active").order_by('-created_at')
    
    def create(self, request, vessel_pk=None):
        request.data['vessel'] = vessel_pk
        if "status" in request.data and request.data['status'] != "active":
            return Response(data={"message": "Cannot create a deactivated equipment"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)
    
    @action(detail=True, methods=['patch'])
    def deactivate(self, request):
        equipments_to_deactivate = models.Equipment.objects.filter(code__in=request.data)
        if len(equipments_to_deactivate) < len(request.data):
            return Response(
                data={"message": "One or more equipments where not found. Check for invalid codes and try again"},
                status=status.HTTP_400_BAD_REQUEST)
        equipments_to_deactivate.update(status="inactive")
        return Response(status=status.HTTP_204_NO_CONTENT)