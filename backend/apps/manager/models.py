from django.conf import settings
from django.db import models
from django.utils import timezone


class HousingAssociation(models.Model):
    name = models.CharField(verbose_name="HousingName", max_length=254, unique=True)

    def __str__(self):
        return "-".join(self.name.split())

    def get_general_info(self):
        return {
            "id": self.pk,
            "name": self.name,
        }


class Apartment(models.Model):
    address = models.CharField(verbose_name="ApartmentAddress", max_length=100, unique=True)
    housing = models.ForeignKey(HousingAssociation, on_delete=models.PROTECT)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Owners", related_name="owners")
    area = models.FloatField(null=False, blank=False, default=0.0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name="Registered at", auto_now_add=timezone.now)

    def __str__(self):
        return f"{self.address}"

    def get_general_info(self):
        return {
            "id": self.pk,
            "name": self.address,
            "owners": [str(u) for u in self.owners.all()],
            "area": self.area,
            "balance": self.balance,
        }


class BillType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name


class Bill(models.Model):
    name = models.CharField(verbose_name="BillName", max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(auto_now_add=timezone.now)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True, related_name="apartment")
    is_paid = models.BooleanField(default=False)
    bill_type = models.ForeignKey(BillType, on_delete=models.PROTECT, null=True, related_name="bill_type")

    def __str__(self):
        return f"{self.name} - {self.start_date}-{self.end_date}"

    def save(self, *args, **kwargs):
        self.apartment.balance -= round(self.bill_type.price * self.amount, 2)
        self.apartment.save()
        super().save(*args, **kwargs)

    def get_general_info(self):
        return {
            "id": self.pk,
            "name": self.name,
            "amount": self.amount,
            "cost": round(self.bill_type.price * self.amount, 2),
            "unit_cost": self.bill_type.price,
            "unit": self.bill_type.unit,
            "period": f"{self.start_date} - {self.end_date}",
            "is_paid": self.is_paid,
            "bill_type": self.bill_type.name,
        }


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
