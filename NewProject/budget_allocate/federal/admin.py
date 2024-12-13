
from django.contrib import admin
from .models import Province, District, Municipality, Ward
from django.contrib import admin, messages
from budget_analysis.models import BudgetAllocation
import pandas as pd

admin.site.register(Province)
admin.site.register(District)
admin.site.register(Municipality)
admin.site.register(Ward)


## for accessing excel file

