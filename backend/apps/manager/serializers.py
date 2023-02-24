from collections import OrderedDict
from typing import Callable

from django.db.models import Q
from rest_framework import serializers

from apps.manager.models import Apartment, Bill, BillType, HousingAssociation, Issue, IssueType, News


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


class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if default_factory is not None and not isinstance(default_factory, Callable):
            raise TypeError("first argument must be callable")
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = (self.default_factory,)
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy

        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return "OrderedDefaultDict(%s, %s)" % (self.default_factory, OrderedDict.__repr__(self))


class WholeInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    @staticmethod
    def get_rents(apartment):
        rents = []
        bills = Bill._prediction_bills + Bill._occupant_bills + Bill._meters + ["Zaliczka na CO"]
        for bill in Bill.objects.filter(Q(apartment__id=apartment.id) & Q(bill_type__name__in=bills)):
            rents.append(bill.get_general_info())
        return rents

    def get_all(self):
        housing = DefaultOrderedDict(list)

        for apartment in Apartment.objects.filter(Q(owners__id=self.validated_data["user"].pk)):
            housing[apartment.housing.name].append(apartment.get_general_info())
            housing[apartment.housing.name][-1].update({"bills": []})
            housing[apartment.housing.name][-1].update({"news": []})
            housing[apartment.housing.name][-1].update({"rent": []})
            for bill in Bill.objects.filter(Q(apartment__id=apartment.id)):
                housing[apartment.housing.name][-1]["bills"].append(bill.get_general_info())

            for news in News.objects.filter(
                Q(apartment__id=apartment.pk) | Q(housing__id=apartment.housing.pk)
            ).distinct():
                housing[apartment.housing.name][-1]["news"].append(news.get_news())

            for rent in self.get_rents(apartment):
                housing[apartment.housing.name][-1]["rent"].append(rent)

        data = [{"name": key, "data": sorted(value, key=lambda x: x["id"])} for key, value in housing.items()]

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


class IssuesSerializer(serializers.ModelSerializer):
    issue_type = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=IssueType.objects.all(),
        required=True,
        allow_empty=False,
        allow_null=False,
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ("id", "issue_type", "description", "user")


class IssuesListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_all(self):
        return [
            {"type": issue.issue_type.name, "status": issue.issue_status.name, "description": issue.description}
            for issue in Issue.objects.filter(user=self.validated_data["user"])
        ]

    class Meta:
        model = Issue
        fields = ("id", "issue_status", "issue_type", "description", "user")
