from django.urls import path
from .views import AllocatedAmountListCreateAPIView, AllocatedAmountDetailUpdateDeleteAPIView, SponsorListAPIView, SponsorDetailUpdateAPIView,\
    StudentListCreateAPIView, StudentDetailUpdateDeleteAPIView

urlpatterns = [
    # Sponsor URLs
    path('sponsors/', SponsorListAPIView.as_view(), name='sponsor_list'),
    path('sponsors/<uuid:id>/', SponsorDetailUpdateAPIView.as_view(), name='sponsor_detail_update_delete'),

    # Student URLs
    path('students/', StudentListCreateAPIView.as_view(), name='student_list_create'),
    path('students/<uuid:id>/',StudentDetailUpdateDeleteAPIView.as_view(), name='student_detail_update_delete'),

    path('students/<uuid:student_id>/allocated-amounts/', AllocatedAmountListCreateAPIView.as_view(),
         name='allocated-amount-list-create'),
    path('students/<uuid:student_id>/allocated-amounts/<uuid:sponsor_id>/',
         AllocatedAmountDetailUpdateDeleteAPIView.as_view(), name='allocated-amount-detail-update-delete'),
]
