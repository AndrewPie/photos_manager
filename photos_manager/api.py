from photos_app.api_views import PhotoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"photos", PhotoViewSet, basename="photo")
