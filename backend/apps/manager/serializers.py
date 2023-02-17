from django.db.models import Q
from rest_framework import serializers

from apps.manager.models import Apartment, HousingAssociation


class HousingAssociationListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = HousingAssociation
        fields = ["id", "name"]


class ApartmentListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pk = serializers.IntegerField(required=False)

    def get_all_apartments(self):
        apartments = Apartment.objects.filter(Q(owners__id=self.validated_data["user"].pk))
        apartments = {apartment.pk: apartment.get_general_info() for apartment in apartments}
        return {"apartments": apartments}

    class Meta:
        model = Apartment
        fields = ("user", "pk", )
