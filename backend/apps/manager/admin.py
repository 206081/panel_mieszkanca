from django.contrib import admin

from apps.manager.models import (Apartment, Bill, BillType, HousingAssociation, HousingBill, Income, Issue, IssueStatus,
                                 IssueType, News)


class IssueAdmin(admin.ModelAdmin):
    list_display = ("issue_type", "user")
    list_filter = ("user",)


class IncomeAdmin(admin.ModelAdmin):
    list_filter = ("apartment",)


admin.site.register(Issue, IssueAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(
    [
        HousingAssociation,
        Apartment,
        News,
        Bill,
        BillType,
        IssueType,
        IssueStatus,
        HousingBill,
    ]
)
