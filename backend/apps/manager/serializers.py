from collections import defaultdict

from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from apps.manager.models import Apartment, Bill, BillType, HousingAssociation, News


class HousingAssociationCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_null=False,
    )

    class Meta:
        model = HousingAssociation
        fields = ("id", "name")


class HousingAssociationListSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)

    def get_housing(self):
        housing = HousingAssociation.objects.get(Q(pk=self.validated_data["pk"]))
        return housing.get_general_info() if housing else []

    def get_housings(self):
        return [housing.get_general_info() for housing in HousingAssociation.objects.all()]

    class Meta:
        model = HousingAssociation
        fields = ("pk",)


class ApartmentListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pk = serializers.IntegerField(required=False)

    def get_all_apartments(self):
        apartments = Apartment.objects.filter(Q(owners__id=self.validated_data["user"].pk))
        apartments = {apartment.pk: apartment.get_general_info() for apartment in apartments}
        return {"apartments": apartments}

    class Meta:
        model = Apartment
        fields = ("user", "pk")


class WholeInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_all(self):
        housing = defaultdict(list)

        for apartment in Apartment.objects.filter(Q(owners__id=self.validated_data["user"].pk)):
            housing[apartment.housing.name].append(apartment.get_general_info())
            housing[apartment.housing.name][-1].update({"bills": []})
            for bill in Bill.objects.filter(Q(apartment__id=apartment.id)):
                housing[apartment.housing.name][-1]["bills"].append(bill.get_general_info())

        # for news in News.objects.filter(Q(apartment__id=apartment.pk) | Q(housing__id=apartment.housing.pk)):
        #     housing.update({"news": news.get_news()})

        data = [{"name": key, "data": value} for key, value in housing.items()]

        return data

    class Meta:
        model = Apartment
        fields = ("user",)


class BillSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    bill_type = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=BillType.objects.all(),
        required=True,
        allow_empty=False,
        allow_null=False,
    )

    start_date = serializers.DateField()

    class Meta:
        model = Bill
        fields = ("id", "amount", "apartment", "start_date", "end_date", "bill_type")


data = [
    {
        "name": "TestHousing3",
        "data": [
            {
                "id": 1,
                "address": "Piotrkowska 1",
                "owners": ["b@vp.pl - Ksinski B", "a@vp.pl - Becadlo A"],
                "area": 55.0,
                "balance": -52.0,
                "bills": [
                    {
                        "id": 2,
                        "name": "Prąd",
                        "amount": 0.02,
                        "unit": "MWh",
                        "period": "2023-02-01 - 2023-02-28",
                        "is_paid": False,
                        "bill_type": "Prąd",
                    },
                    {
                        "id": 1,
                        "name": "Woda",
                        "amount": 0.1,
                        "unit": "m³",
                        "period": "2023-02-01 - 2023-02-28",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 3,
                        "name": "Woda",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-18 - 2023-02-28",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 4,
                        "name": "Prąd",
                        "amount": 50.0,
                        "unit": "MWh",
                        "period": "2023-02-01 - 2023-02-28",
                        "is_paid": False,
                        "bill_type": "Prąd",
                    },
                    {
                        "id": 9,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-28 - 2023-02-18",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 10,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-28 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 11,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-28 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 12,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-28 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 13,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-28 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                ],
            }
        ],
    },
    {
        "name": "TestHousing",
        "data": [
            {
                "id": 2,
                "address": "Hetmanska",
                "owners": ["a@vp.pl - Becadlo A"],
                "area": 54.3,
                "balance": 0.0,
                "bills": [
                    {
                        "id": 15,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-18 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 16,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-19 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 17,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-19 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                    {
                        "id": 18,
                        "name": "",
                        "amount": 0.0,
                        "unit": "m³",
                        "period": "2023-02-19 - 2023-02-19",
                        "is_paid": False,
                        "bill_type": "Woda",
                    },
                ],
            }
        ],
        "news": {"title": "Podwyżka opłat", "text": "W związku z szalejącą inflacją bla bla"},
    },
]
