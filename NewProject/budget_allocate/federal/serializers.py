from rest_framework import serializers
from federal.models import Province, District, Municipality, Ward
from budget_analysis.models import BudgetAllocation, Sector, SubSector

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name_en', 'name_ne']

class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = District
        fields = ['id', 'name_en', 'name_ne', 'province']

class MunicipalitySerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Municipality
        fields = ['id', 'name_en', 'name_ne', 'lg_code', 'district']

class WardSerializer(serializers.ModelSerializer):
    municipality = MunicipalitySerializer()

    class Meta:
        model = Ward
        fields = ['id', 'ward_number', 'name_en', 'name_ne', 'municipality']

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'sector_name']

class SubSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        fields = ['id', 'subsector_name']

class BudgetAllocationSerializer(serializers.ModelSerializer):
    ward = WardSerializer()
    municipality = MunicipalitySerializer()
    sector = SectorSerializer()
    sub_sector = SubSectorSerializer()

    class Meta:
        model = BudgetAllocation
        fields = [
            'id', 'federal_level', 'ward', 'municipality',
            'sector', 'sub_sector', 'fiscal_year', 'fund_type',
            'budget_amount', 'description'
        ]
