from django.urls import path
from .views import SponsorApplicationAPIView

urlpatterns = [
    path('apply-sponsor/', SponsorApplicationAPIView.as_view(), name='apply_sponsor'),
]
