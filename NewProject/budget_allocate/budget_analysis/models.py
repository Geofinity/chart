from django.db import models
from django.core.exceptions import ValidationError
from federal.models import Municipality, Ward

# Choices for federal levels
LEVEL_CHOICES = [
    (2, "Municipality"),
    (1, "Ward"),
]

# Choices for fiscal years
FISCAL_YEAR_CHOICES = [
    ('79-80', '79-80'),
    ('80-81', '80-81'),
    ('81-82', '81-82'),
]

# Choices for fund types
FUND_TYPE = [
    ('1', 'CAPITAL'),
    ('2', 'RECURRENT'),
    ('3', 'FINANCING'),
]

class Sector(models.Model):
    sector_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Sectors"

    def __str__(self):
        return f"Sector {self.sector_name}"

class SubSector(models.Model):
    subsector_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "SubSectors"

    def __str__(self):
        return f"SubSector {self.subsector_name}"


class BudgetAllocation(models.Model):
    federal_level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=1
    )
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, null=True, blank=True, related_name="municipality_allocations"
    )
    ward = models.ForeignKey(
        Ward, on_delete=models.CASCADE, null=True, blank=True, related_name="ward_allocations"
    )

    # Other fields
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='sector', null=True, blank=True)
    sub_sector = models.ForeignKey(SubSector, on_delete=models.CASCADE, related_name='subsector', null=True, blank=True)
    budgetsubhead = models.CharField(max_length=255,null=True, blank=True)
    programnamenp = models.CharField(max_length=255,null=True, blank=True)
    fiscal_year = models.CharField(
        max_length=50,
        choices=FISCAL_YEAR_CHOICES,
        default='79-80'
    )
    fund_type = models.CharField(
        max_length=50,
        choices=FUND_TYPE,
        default='1'
    )
    economic_code = models.IntegerField(default=2000)  
    economic_code_name = models.CharField(max_length=50,null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2)
    cofog = models.IntegerField(default=100000)  
    cofog_name = models.CharField(max_length=50,null=True, blank=True)
    source_level = models.CharField(max_length=50,null=True, blank=True)
    source_name = models.CharField(max_length=50,null=True, blank=True)
    revenue_item = models.CharField(max_length=50,null=True, blank=True)
    support_type = models.CharField(max_length=50,null=True, blank=True)
    expenditure_amount = models.IntegerField(default=100000)  
    description = models.TextField(null=True, blank=True)

    def clean(self):
        """
        Ensure only one of municipality or ward is filled based on the selected federal level.
        """
        selected_fields = {
            2: self.municipality,
            1: self.ward,
        }

        for level, field in selected_fields.items():
            if self.federal_level == level and not field:
                raise ValidationError(f"You must select a {LEVEL_CHOICES[level - 1][1]}.")
            if self.federal_level != level and field:
                raise ValidationError(f"You cannot select {LEVEL_CHOICES[level - 1][1]} for the chosen federal level.")

    def __str__(self):
        location = self.ward or self.municipality or "N/A"
        return f"{self.sector} - {self.fiscal_year} - {location}"
