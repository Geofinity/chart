from django.contrib import admin, messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
import pandas as pd
from .models import BudgetAllocation, Sector
from federal.models import Province, District, Municipality, Ward
from .forms import ExcelUploadForm
admin.site.register(BudgetAllocation)
admin.site.register(Sector)
