from django.urls import include, path
from rest_framework_nested import routers
from vessels import views

router = routers.SimpleRouter()
router.register(r'vessels', views.VesselViewSet)

vessel_router = routers.NestedSimpleRouter(router, r'vessels', lookup="vessel")
vessel_router.register(r'equipments', views.EquipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(vessel_router.urls)),
    path('equipments/deactivate/', views.EquipmentViewSet.as_view({"patch": "deactivate"}))
]