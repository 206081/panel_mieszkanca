from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.manager.models import Apartment, Bill, HousingAssociation
from apps.manager.serializers import (ApartmentListSerializer, BillSerializer, HousingAssociationCreateSerializer,
                                      HousingAssociationListSerializer, WholeInfoSerializer)


class HousingAssociationViewSet(ViewSet):
    queryset = HousingAssociation.objects.all()

    def create(self, request):
        serializer = HousingAssociationCreateSerializer(data=request.data.copy())
        serializer.is_valid(raise_exception=False)
        serializer.save()
        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        serializer = HousingAssociationListSerializer(data=request.data.copy(), context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.get_housings(),
            },
        )

    def retrieve(self, request, pk):
        modified_data = request.data.copy()

        modified_data["pk"] = pk

        serializer = HousingAssociationListSerializer(data=modified_data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.get_housing(),
            },
        )

    @action(detail=False)
    def all_housing(self, request):
        modified_data = request.data.copy()

        serializer = HousingAssociationListSerializer(data=modified_data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.get_housings(),
            },
        )


class ApartmentViewSet(ViewSet):
    def list(self, request):
        serializer = ApartmentListSerializer(data=request.data.copy(), context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.get_all_apartments(),
            },
        )


class BillViewSet(ViewSet):
    def create(self, request, apartment_pk=None):
        modified_data = request.data.copy()
        modified_data["apartment"] = apartment_pk

        if not request.data.get("start_date", "") and (apartment := Apartment.objects.get(id=apartment_pk)):
            last_bill_date = (
                Bill.objects.filter(Q(bill_type__id=request.data.get("bill_type", "")) & Q(apartment=apartment))
                .order_by("end_date")
                .last()
                .end_date
            )

            modified_data["start_date"] = last_bill_date or apartment.created_at

        serializer = BillSerializer(data=modified_data, context={"request": self.request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class WholeInfoViewSet(ViewSet):
    def list(self, request):
        modified_data = request.data.copy()

        serializer = WholeInfoSerializer(data=modified_data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.get_all(),
            }
        )