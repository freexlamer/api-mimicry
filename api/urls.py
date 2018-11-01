from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(
    r'feed',
    views.FeedViewSet,
    base_name='feed'
)
router.register(
    r'rentals',
    views.RentalViewSet,
    base_name='rentals'
)


urlpatterns = [
    url(r'^', include(router.urls)),

]
