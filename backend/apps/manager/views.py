from django.db.models import Q
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.manager.models import Apartment, Bill, HousingAssociation
from apps.manager.serializers import (ApartmentListSerializer, BillSerializer, HousingAssociationCreateSerializer,
                                      HousingAssociationListSerializer, IssuesListSerializer, IssuesSerializer,
                                      ReportSerializer, WholeInfoSerializer)


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

    @action(methods=["POST"], detail=True)
    def report(self, request, pk):
        modified_data = request.data.copy()

        modified_data["apartment"] = pk
        print(modified_data)
        serializer = ReportSerializer(data=modified_data, context={"request": self.request})
        print("is good2")
        serializer.is_valid(raise_exception=True)
        print("is good3")

        return FileResponse(serializer.get_file(), as_attachment=True)


class BillViewSet(ViewSet):
    def create(self, request, apartment_pk=None):
        modified_data = request.data.copy()

        if not request.data.get("start_date", ""):
            try:
                modified_data["start_date"] = Apartment.objects.get(
                    Q(id=apartment_pk) & (Q(owners=self.request.user.id))
                ).created_at.date()
            except Apartment.DoesNotExist:
                apartment_pk = 0

            try:
                modified_data["start_date"] = (
                    Bill.objects.filter(Q(bill_type__id=request.data.get("bill_type", "")) & Q(apartment=apartment_pk))
                    .last()
                    .end_date
                )
            except:
                pass

        modified_data["apartment"] = apartment_pk

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
        print(modified_data)
        serializer = WholeInfoSerializer(data=modified_data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        data = serializer.get_all()
        data.sort(key=lambda x: x["name"])
        return Response(status=status.HTTP_200_OK, data=data)


class IssueViewSet(ViewSet):
    def list(self, request):
        serializer = IssuesListSerializer(data=request.data.copy(), context={"request": self.request})

        serializer.is_valid(raise_exception=True)
        return Response(
            data=serializer.get_all(),
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        modified_data = request.data.copy()

        serializer = IssuesSerializer(data=modified_data, context={"request": self.request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
