import csv
import re
import os
from django.core.management.base import BaseCommand
from federal.models import Province, District, Municipality, Ward
from budget_analysis.models import BudgetAllocation, Sector, SubSector

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='Path to the CSV file, e.g., /home/ashish-dhakal/charts/NewProject/budget_allocate/budget_data.csv'
        )

    def create_province(self, stream):
            try:
                print(stream)
                for province in stream:
                    print(province)
                    province, _ = Province.objects.get_or_create(
                                    name_en=province,
                                    name_ne=province
                                )
                    province.save()
                    self.stdout.write(self.style.SUCCESS(f"Provice added: {province}"))
            except:
                self.stdout.write(self.style.ERROR(f"{province} already exists"))
                
        
    def create_district(self, stream):
        for district_vals in stream:
            try:
                name_en, name_np, province_name = list(district_vals)
                print(f"Processing: {name_en}, {name_np}, {province_name}")

                try:
                    province = Province.objects.get(name_en=province_name)
                    print(f"Found Province: {province}")
                except Province.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Province '{province_name}' does not exist. Skipping..."))
                    continue

                district, created = District.objects.get_or_create(
                    name_en=name_en,
                    name_ne=name_np,
                    province=province
                )
                if created:
                    print("New district created.")
                    self.stdout.write(self.style.SUCCESS(f"District added: {district}"))
                else:
                    print("District already exists.")
                    self.stdout.write(self.style.WARNING(f"District already exists: {district}"))
            
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error unpacking district values: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))



    def create_municipality(self, stream):
        for municipality_vals in stream:
            try:
                LGNameEn, LGnameNp, DistrictNameEn= list(municipality_vals)
                try:
                    district = District.objects.get(name_en=DistrictNameEn)
                    print(f"Found District: {district}")
                except District.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"District does not exist. Skipping..."))
                    continue

                municipality, created = Municipality.objects.get_or_create(
                    name_en=LGNameEn, name_ne=LGnameNp, district=district)
                if created:
                    print("New municipality created.")
                    self.stdout.write(self.style.SUCCESS(f"Municipality added: {municipality}"))
                else:
                    print("Municipality already exists.")
                    self.stdout.write(self.style.WARNING(f"Municipality already exists: {municipality}"))
            
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error unpacking district values: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))

    def create_ward(self, stream):
        for ward_vals in stream:
            try:
                ward_number, LGNameEn= list(ward_vals)
                try:
                    municipality= Municipality.objects.get(municipality=LGNameEn)
                    print(f"Found Municipality: {municipality}")
                except Municipality.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Municipality does not exist. Skipping..."))
                    continue

                ward, created = Ward.objects.get_or_create(
                    ward=ward_number, municipality=municipality)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"ward added: {ward}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Ward already exists"))
            
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error unpacking district values: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))


    def handle(self, *args, **kwargs):
        file_path = kwargs['file']  # Get file path from command arguments
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            province_stream= set()
            district_stream = set()
            municipality_stream = set()
            ward_stream = set()

            for row in reader:
                province_stream.add(row["Province"])
                district_stream.add((row["DistrictNameEn"],row["DistrictNameNp"],row["Province"]))
                municipality_stream.add((row["LGNameEn"],row["LGnameNp"], row["DistrictNameEn"]))
                ward_stream.add((row["Ward"], row["LGNameEn"]))

            # self.create_province(province_stream)
            # self.create_district(district_stream)
            # self.create_municipality(municipality_stream)
            self.create_ward(ward_stream)


