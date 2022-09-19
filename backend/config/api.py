from rest_framework_nested import routers

from apps.users.views import UserViewSet

# Settings
router = routers.DefaultRouter()
router.trailing_slash = "/?"

# Users API
router.register(r"users", UserViewSet)
