from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProvinceViewSet, DistrictViewSet, MunicipalityViewSet, WardViewSet,
    SectorViewSet, SubSectorViewSet, BudgetAllocationViewSet
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'municipalities', MunicipalityViewSet, basename='municipality')
router.register(r'wards', WardViewSet, basename='ward')
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'sub-sectors', SubSectorViewSet, basename='subsector')
router.register(r'budget-allocations', BudgetAllocationViewSet, basename='budget-allocation')

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
