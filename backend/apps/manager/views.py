from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.manager.serializers import ApartmentListSerializer, HousingAssociationListSerializer


class ApartmentViewSet(ViewSet):
    def list(self, request):
        serializer = ApartmentListSerializer(data=request.data.copy(), context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.get_all_apartments(),
            },
        )

class HousingAssociationViewSet(ViewSet):
    pass
