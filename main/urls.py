from django.urls import path
from .views import SponsorViewSet, UniversityViewSet, StudentViewSet, AllocatedAmountViewSet

urlpatterns = [
    # Homiy API yo'llari
    path('sponsors/', SponsorViewSet.as_view({'post': 'create', 'get': 'list'}), name='sponsor-list-create'),
    path('sponsors/<int:pk>/', SponsorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sponsor-detail'),

    # Universitet API yo'llari
    path('universities/', UniversityViewSet.as_view({'post': 'create', 'get': 'list'}), name='university-list-create'),
    path('universities/<int:pk>/', UniversityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='university-detail'),

    # Talaba API yo'llari
    path('students/', StudentViewSet.as_view({'post': 'create', 'get': 'list'}), name='student-list-create'),
    path('students/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='student-detail'),

    # Ajratilgan mablag' API yo'llari
    path('allocated-amounts/', AllocatedAmountViewSet.as_view({'post': 'create', 'get': 'list'}), name='allocated-amount-list-create'),
    path('allocated-amounts/<int:pk>/', AllocatedAmountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='allocated-amount-detail'),
]
