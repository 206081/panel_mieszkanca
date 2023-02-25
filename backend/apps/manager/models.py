import random
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class BillType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name


class IssueStatus(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "Issue statuses"

    def __str__(self):
        return self.name


class IssueType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class IssueFilter:
    pass


class Issue(models.Model):
    list_display = ("issue_type", "user")
    search_fields = ("issue_status",)

    issue_type = models.ForeignKey(IssueType, on_delete=models.PROTECT, null=True, related_name="issue_type")
    issue_status = models.ForeignKey(
        IssueStatus,
        on_delete=models.PROTECT,
        null=True,
        related_name="issue_status",
        default=1,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        related_name="user",
        on_delete=models.CASCADE,
        null=True,
    )
    description = models.TextField(default="")
    summary = models.TextField(default="")

    def __str__(self):
        return f"{self.issue_type.name} - {self.issue_status.name} - {self.user}"


class HousingAssociation(models.Model):
    name = models.CharField(verbose_name="HousingName", max_length=254, unique=True)

    def __str__(self):
        return "-".join(self.name.split())

    def get_general_info(self):
        return {
            "id": self.pk,
            "name": self.name,
        }


class HousingBill(models.Model):
    bill_type = models.ForeignKey(BillType, on_delete=models.PROTECT, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    housing = models.ForeignKey(HousingAssociation, on_delete=models.PROTECT, null=True)


def _account():
    return round(random.random() * 10**26)


class Apartment(models.Model):
    address = models.CharField(verbose_name="ApartmentAddress", max_length=100, unique=True)
    housing = models.ForeignKey(HousingAssociation, on_delete=models.PROTECT)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Owners", related_name="owners")
    area = models.FloatField(null=False, blank=False, default=0.0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name="Registered at", auto_now_add=timezone.now)
    occupant = models.IntegerField(default=0)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    predictions = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    account = models.DecimalField(max_digits=26, decimal_places=0, default=_account)

    def __str__(self):
        return f"{self.address}"

    def get_general_info(self):
        return {
            "id": self.pk,
            "name": self.address,
            "owners": [str(u) for u in self.owners.all()],
            "area": self.area,
            "balance": self.balance,
            "interest": self.interest,
            "occupant": self.occupant,
            "predictions": self.predictions,
        }


class Bill(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0)
    start_date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    end_date = models.DateField(default=timezone.now)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
    is_balanced = models.BooleanField(default=False)
    bill_type = models.ForeignKey(BillType, on_delete=models.PROTECT, null=True)
    _prediction_bills = ["Woda ciepła", "Woda zimna i ścieki"]
    _occupant_bills = ["Odpady komunalne"]
    _meters = ["Eksploatacja", "Centralne ogrzewanie", "Fundusz remontowy"]

    def __str__(self):
        return f"{self.bill_type.name} - {self.start_date}-{self.end_date} - {self.apartment.address}"

    def save(self, *args, **kwargs):
        if self.bill_type.name in self._prediction_bills:
            self.price = round(self.apartment.predictions * self.bill_type.price, 2)
            self.amount = self.apartment.predictions
        elif self.bill_type.name in self._occupant_bills:
            self.price = round(self.apartment.occupant * self.bill_type.price, 2)
            self.amount = self.apartment.occupant
        elif self.bill_type.name in self._meters:
            self.price = round(Decimal(self.apartment.area) * self.bill_type.price, 2)
            self.amount = self.apartment.area
        else:
            self.price = round(self.bill_type.price * self.amount, 2)

        if not self.is_balanced:
            self.apartment.balance -= self.price
            self.is_balanced = True
        self.apartment.save()
        super().save(*args, **kwargs)

    def get_general_info(self):
        return {
            "id": self.pk,
            "amount": self.amount,
            "cost": self.price,
            "period": f"{self.start_date} - {self.end_date}",
            "is_balanced": self.is_balanced,
            "unit_cost": self.bill_type.price,
            "unit": self.bill_type.unit,
            "bill_type": self.bill_type.name,
        }


class Income(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.apartment.address} - {self.amount} zł"

    def save(self, *args, **kwargs):
        self.apartment.balance += self.amount
        self.apartment.save()
        super().save(*args, **kwargs)


class News(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    housing = models.ManyToManyField(HousingAssociation, blank=True)
    apartment = models.ManyToManyField(Apartment, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    def get_news(self):
        return {
            "title": self.title,
            "text": self.text,
        }

    class Meta:
        verbose_name_plural = "News"


class Files(models.Model):
    pdf = models.FileField(upload_to="store/pdfs/")

    def __str__(self):
        return self.pdf
