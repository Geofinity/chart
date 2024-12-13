from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProvinceViewSet, DistrictViewSet, MunicipalityViewSet, WardViewSet,
    BudgetAllocationViewSet, SectorViewSet, SubSectorViewSet
)

router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'municipalities', MunicipalityViewSet, basename='municipality')
router.register(r'wards', WardViewSet, basename='ward')
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'subsectors', SubSectorViewSet, basename='subsector')
router.register(r'budget-allocations', BudgetAllocationViewSet, basename='budgetallocation')

urlpatterns = [
    path('', include(router.urls)),
]
