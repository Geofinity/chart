from django.db import models

class Province(models.Model):
    name_en = models.CharField(max_length=255, unique=True, verbose_name="Province Name (English)",default="bagmati")
    name_ne = models.CharField(max_length=255, unique=True, verbose_name="Province Name (Nepali)",default="bagmati")

    class Meta:
        verbose_name_plural = "Provinces"

    def __str__(self):
        return f"{self.name_en} / {self.name_ne}"


class District(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="District Name (English)",default="kathmandu")
    name_ne = models.CharField(max_length=255, verbose_name="District Name (Nepali)",default="kathmandu")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('name_en', 'province')
        verbose_name_plural = "Districts"
        

    def __str__(self):
        return f"{self.name_en} / {self.name_ne}, {self.province.name_en}"


class Municipality(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="Municipality Name (English)",default="kathmandu")
    name_ne = models.CharField(max_length=255, verbose_name="Municipality Name (Nepali)",default="kathmandu")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='municipalities')
    lg_code = models.CharField(max_length=255, verbose_name="Local Government Code",default=1001)

    class Meta:
        unique_together = ('name_en', 'district')
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return f"{self.name_en} / {self.name_ne}, {self.district.name_en}"


class Ward(models.Model):
    ward_number = models.PositiveIntegerField(verbose_name="Ward Number",default=1)
    name_en = models.CharField(max_length=255, verbose_name="Ward Name (English)",default=1)
    name_ne = models.CharField(max_length=255, verbose_name="Ward Name (Nepali)",default=1)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='wards')

    class Meta:
        unique_together = ('ward_number', 'municipality')
        verbose_name_plural = "Wards"

    def __str__(self):
        return f"Ward {self.ward_number}: {self.name_en} / {self.name_ne}, {self.municipality.name_en}"
