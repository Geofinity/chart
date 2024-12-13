from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from federal.models import Province, District, Municipality, Ward
from budget_analysis.models import BudgetAllocation, Sector, SubSector
from .serializers import (
    ProvinceSerializer, DistrictSerializer, MunicipalitySerializer,
    WardSerializer, BudgetAllocationSerializer, SectorSerializer, SubSectorSerializer
)

class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne']
    search_fields = ['name_en', 'name_ne']

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne', 'province']
    search_fields = ['name_en', 'name_ne']

class MunicipalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne', 'district']
    search_fields = ['name_en', 'name_ne']

class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ward_number', 'municipality']
    search_fields = ['name_en', 'name_ne']

class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class SubSectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubSector.objects.all()
    serializer_class = SubSectorSerializer

class BudgetAllocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BudgetAllocation.objects.all()
    serializer_class = BudgetAllocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['federal_level', 'fiscal_year', 'ward', 'municipality', 'sector', 'sub_sector']
    search_fields = ['description']
