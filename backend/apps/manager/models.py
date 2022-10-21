from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Apartment(models.Model):
    address = models.CharField(verbose_name="Address", max_length=100, unique=True)
    postal_code = models.CharField(verbose_name="PostalCode", max_length=6)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Owners", related_name="owners")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    account_number = models.IntegerField(blank=False, null=False)
    area = models.IntegerField()

    def __str__(self):
        return f"{self.address}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.address)
        super().save(*args, **kwargs)

    def get_general_info(self):
        return {
            "id": self.pk,
            "address": self.address,
            "owners": [u.id for u in self.owners.all()],
        }


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class TransactionType(models.Model):
    INCOME = 1
    OUTCOME = 2

    Way = (
        (INCOME, "Income"),
        (OUTCOME, "Outcome"),
    )

    way = models.IntegerField(choices=Way)


class Transaction(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT)
    amount = models.IntegerField(blank=False, null=False)
    date = models.DateField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()


class Role(models.Model):
    MEMBER = 1

    _Role = ((MEMBER, "Member"),)

    role = models.IntegerField(choices=_Role, default=MEMBER)


class Member(models.Model):
    name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)


class Management(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
