from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('api/', include('lottery.api.urls')),
    path('', TemplateView.as_view(template_name='home.html'))
]
