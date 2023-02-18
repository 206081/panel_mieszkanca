from rest_framework_nested import routers

from apps.manager.views import ApartmentViewSet, BillViewSet, HousingAssociationViewSet, WholeInfoViewSet
from apps.users.views import UserViewSet

# Settings
router = routers.DefaultRouter()
router.trailing_slash = "/?"

# Users API
router.register(r"users", UserViewSet)
router.register(r"housing", HousingAssociationViewSet, basename="housing")
router.register(r"apartments", ApartmentViewSet, basename="apartments")
router.register(r"whole", WholeInfoViewSet, basename="whole_info")

apartments_router = routers.NestedSimpleRouter(router, "apartments", lookup="apartment")
apartments_router.register(r"bills", BillViewSet, basename="bills")
