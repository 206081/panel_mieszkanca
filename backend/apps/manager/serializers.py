from collections import defaultdict

from django.db.models import Q
from rest_framework import serializers

from apps.manager.models import Apartment, Bill, HousingAssociation, News


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

        for news in News.objects.filter(Q(apartment__id=apartment.pk) | Q(housing__id=apartment.housing.pk)):
            housing.update({"news": news.get_news()})

        return housing

    class Meta:
        model = Apartment
        fields = ("user",)
