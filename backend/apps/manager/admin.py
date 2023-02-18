from django.contrib import admin

from apps.manager.models import Apartment, Bill, HousingAssociation, News, BillType

# Register your models here.
admin.site.register([HousingAssociation, Apartment, News, Bill, BillType])
