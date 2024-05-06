from .views import ForexViewSet,OrderViewSet,FileStorageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'forex', ForexViewSet, basename='forex')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'filestorage', FileStorageViewSet, basename='filestorage')

urlpatterns = router.urls
