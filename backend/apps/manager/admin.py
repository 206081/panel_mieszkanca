from django.contrib import admin

from apps.manager.models import Apartment, Bill, BillType, HousingAssociation, News

# Register your models here.
admin.site.register([HousingAssociation, Apartment, News, Bill, BillType])
