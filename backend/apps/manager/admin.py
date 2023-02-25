from django.contrib import admin

from apps.manager.models import (Apartment, Bill, BillType, HousingAssociation, HousingBill, Income, Issue, IssueStatus,
                                 IssueType, News)

# Register your models here.
admin.site.register(
    [
        HousingAssociation,
        Apartment,
        News,
        Bill,
        BillType,
        IssueType,
        Issue,
        IssueStatus,
        Income,
        HousingBill,
    ]
)
