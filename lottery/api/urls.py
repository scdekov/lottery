from rest_framework.routers import DefaultRouter

from django.urls import path

from lottery.api.views import TicketsView, GameViewSet


router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')


urlpatterns = [
    path('tickets/', TicketsView.as_view(), name='tickets'),
] + router.urls
