from rest_framework.routers import DefaultRouter

from django.urls import path

from lottery.api.views import CreateTicketView, GameViewSet


router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')


urlpatterns = [
    path('tickets/', CreateTicketView.as_view()),
] + router.urls
