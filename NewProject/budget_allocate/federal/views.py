from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from federal.models import Province, District, Municipality, Ward
from budget_analysis.models import BudgetAllocation, Sector, SubSector
from .serializers import (
    ProvinceSerializer, DistrictSerializer, MunicipalitySerializer,
    WardSerializer, BudgetAllocationSerializer, SectorSerializer, SubSectorSerializer
)
from rest_framework.response import Response
from rest_framework import status
from django_filters import FilterSet, ModelChoiceFilter
from django.db.models import Sum
from rest_framework.decorators import action


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne']
    search_fields = ['name_en', 'name_ne']

    # Custom action to list districts for a certain province
    @action(detail=True, methods=['get'], url_path='districts')
    def get_districts(self, request, pk=None):
        """
        Get all districts for a specific province.
        Example: /api/provinces/1/districts/
        """
        province = self.get_object()  # Get the province by pk
        districts = District.objects.filter(province=province)  # Filter districts by province

        # Serialize the districts data
        district_serializer = DistrictSerializer(districts, many=True)

        return Response(district_serializer.data, status=status.HTTP_200_OK)


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne', 'province']
    search_fields = ['name_en', 'name_ne']

    @action(detail=True, methods=['get'], url_path='municipalities')
    def get_municipalities(self, request, pk=None):
        """
        List all municipalities in the specified district.
        Example: /api/districts/{district_id}/municipalities/
        """
        # Get the district object by ID (pk)
        district = self.get_object()
        # Filter municipalities by the selected district
        municipalities = Municipality.objects.filter(district=district)

        # Serialize the municipalities
        serializer = MunicipalitySerializer(municipalities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class MunicipalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne', 'district']
    search_fields = ['name_en', 'name_ne']

    # Custom action to list wards for a specific municipality
    @action(detail=True, methods=['get'], url_path='wards')
    def get_wards(self, request, pk=None):
        """
        Get all wards for a specific municipality.
        Example: /api/municipalities/1/wards/
        """
        municipality = self.get_object()  # Get the municipality by pk
        wards = Ward.objects.filter(municipality=municipality)  # Filter wards by municipality

        # Serialize the wards data
        ward_serializer = WardSerializer(wards, many=True)

        return Response(ward_serializer.data, status=status.HTTP_200_OK)



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


class BudgetAllocationFilter(FilterSet):
    province = ModelChoiceFilter(
        label="Province",
        field_name="ward__municipality__district__province",
        queryset=Province.objects.all(),
    )
    district = ModelChoiceFilter(
        label="District",
        field_name="ward__municipality__district",
        queryset=District.objects.all(),
    )
    municipality = ModelChoiceFilter(
        label="Municipality",
        field_name="ward__municipality",
        queryset=Municipality.objects.all(),
    )
    ward = ModelChoiceFilter(
        label="Ward",
        field_name="ward",
        queryset=Ward.objects.all(),
    )
    sector = ModelChoiceFilter(
        label="Sector",
        field_name="sector",
        queryset=Sector.objects.all(),
    )
    sub_sector = ModelChoiceFilter(
        label="SubSector",
        field_name="sub_sector",
        queryset=SubSector.objects.all(),
    )

    class Meta:
        model = BudgetAllocation
        fields = []


class BudgetAllocationViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = BudgetAllocation.objects.all()
    serializer_class = BudgetAllocationSerializer
    filterset_class = BudgetAllocationFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description']

    @action(detail=False, methods=['get'], url_path='total-budget')
    def total_budget(self, request, *args, **kwargs):
        """
        Calculate total budget based on filters.
        Example: /api/budget-allocations/total-budget/?province=1&sector=Infrastructure
        """
        filters = {}

        province_id = request.query_params.get('province')
        district_id = request.query_params.get('district')
        municipality_id = request.query_params.get('municipality')
        ward_id = request.query_params.get('ward')
        sector_id = request.query_params.get('sector')
        sub_sector_id = request.query_params.get('sub_sector')

        if province_id:
            filters['ward__municipality__district__province_id'] = province_id
        if district_id:
            filters['ward__municipality__district_id'] = district_id
        if municipality_id:
            filters['ward__municipality_id'] = municipality_id
        if ward_id:
            filters['ward_id'] = ward_id
        if sector_id:
            filters['sector_id'] = sector_id
        if sub_sector_id:
            filters['sub_sector_id'] = sub_sector_id

        total_budget = BudgetAllocation.objects.filter(**filters).aggregate(
            total_budget=Sum('budget_amount')
        )['total_budget']

        if total_budget is None:
            return Response({"message": "No data found for the specified filters."},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"total_budget": total_budget}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='grouped-budget')
    def grouped_budget(self, request, *args, **kwargs):
        """
        Return grouped budget data, e.g., by province, district, etc.
        Example: /api/budget-allocations/grouped-budget/?group_by=province
        """
        group_by = request.query_params.get('group_by')

        if not group_by or group_by not in ['province', 'district', 'municipality', 'ward']:
            return Response({"error": "Invalid or missing 'group_by' parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        group_field_map = {
            'province': 'ward__municipality__district__province__name_en',
            'district': 'ward__municipality__district__name_en',
            'municipality': 'ward__municipality__name_en',
            'ward': 'ward__ward_number',
        }

        grouped_data = BudgetAllocation.objects.values(group_field_map[group_by]).annotate(
            total_budget=Sum('budget_amount')
        ).order_by(group_field_map[group_by])

        return Response(grouped_data, status=status.HTTP_200_OK)
