from django.conf import settings
from django.db import models
from django.utils.text import slugify


class HousingAssociation(models.Model):
    name = models.CharField(verbose_name="HousingName", max_length=254, unique=True)


class Apartment(models.Model):
    address = models.CharField(verbose_name="ApartmentAddress", max_length=100, unique=True)
    housing = models.ForeignKey(HousingAssociation, on_delete=models.PROTECT)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Owners", related_name="owners")
    slug = models.SlugField(max_length=40)
    area = models.FloatField(null=False, blank=False, default=0.0)
    balance = models.FloatField(null=False, blank=False, default=0.0)

    def __str__(self):
        return f"{self.address}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super().save(*args, **kwargs)

    def get_general_info(self):
        return {
            "id": self.pk,
            "address": self.address,
            "owners": [u.id for u in self.owners.all()],
        }


class Bills(models.Model):
    name = models.CharField(verbose_name="BillName", max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    is_paid = models.BooleanField()
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return f"{self.name} - {self.start_date}-{self.end_date}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super().save(*args, **kwargs)

    def get_general_info(self):
        return {
            "id": self.pk,
            "name": self.name,
            "amount": round(self.price * self.amount, 2),
            "unit": self.unit,
            "period": f"{self.start_date}-{self.end_date}",
            "is_paid": self.is_paid,
        }


class News(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
