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

    @action(detail=False, methods=['get'], url_path='districts-by-name')
    def get_districts_by_name(self, request):
        """
        Get all districts for a specific province by name.
        Example: /api/provinces/districts-by-name/?name=Bagmati
        """
        province_name = request.query_params.get('name')  
        if not province_name:
            return Response({"error": "Province name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch province by name_en
            province = Province.objects.get(name_en=province_name)
        except Province.DoesNotExist:
            return Response({"error": f"Province '{province_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch districts associated with the province
        districts = District.objects.filter(province=province)
        serializer = DistrictSerializer(districts, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne', 'province']
    search_fields = ['name_en', 'name_ne']

    @action(detail=False, methods=['get'], url_path='municipalities-by-name')
    def get_municipalities_by_name(self, request):
        """
        Get all municipalities for a specific district by name.
        Example: /api/districts/municipalities-by-name/?name=Kathmandu
        """
        district_name = request.query_params.get('name')
        if not district_name:
            return Response({"error": "District name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            district = District.objects.get(name_en=district_name)
        except District.DoesNotExist:
            return Response({"error": f"District '{district_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        municipalities = Municipality.objects.filter(district=district)
        serializer = MunicipalitySerializer(municipalities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MunicipalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_en', 'name_ne', 'district']
    search_fields = ['name_en', 'name_ne']

    @action(detail=False, methods=['get'], url_path='wards-by-name')
    def get_wards_by_name(self, request):
        """
        Get all wards for a specific municipality by name.
        Example: /api/municipalities/wards-by-name/?name=Kathmandu
        """
        municipality_name = request.query_params.get('name')
        if not municipality_name:
            return Response({"error": "Municipality name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            municipality = Municipality.objects.get(name_en=municipality_name)
        except Municipality.DoesNotExist:
            return Response({"error": f"Municipality '{municipality_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        wards = Ward.objects.filter(municipality=municipality)
        serializer = WardSerializer(wards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    @action(detail=False, methods=['get'], url_path='list-fiscal-years')
    def list_fiscal_years(self, request, *args, **kwargs):
        """
        Return a list of distinct fiscal years.
        Example: /api/budget-allocations/list-fiscal-years/
        """
        fiscal_years = BudgetAllocation.objects.values('fiscal_year').distinct()

        return Response(fiscal_years, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='total-budget')
    def total_budget(self, request, *args, **kwargs):
        """
        Calculate total budget based on filters.
        Example: /api/budget-allocations/total-budget/?province=Bagmati&sector=Infrastructure
        """
        filters = {}

        province_name = request.query_params.get('province')
        district_name = request.query_params.get('district')
        municipality_name = request.query_params.get('municipality')
        ward_number = request.query_params.get('ward')
        sector_name = request.query_params.get('sector')
        sub_sector_name = request.query_params.get('sub_sector')

        if province_name:
            filters['ward__municipality__district__province__name_en'] = province_name
        if district_name:
            filters['ward__municipality__district__name_en'] = district_name
        if municipality_name:
            filters['ward__municipality__name_en'] = municipality_name
        if ward_number:
            filters['ward__ward_number'] = ward_number
        if sector_name:
            filters['sector__sector_name'] = sector_name
        if sub_sector_name:
            filters['sub_sector__subsector_name'] = sub_sector_name

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
