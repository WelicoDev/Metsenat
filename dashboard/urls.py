from django.urls import path
from . import views

urlpatterns = [
    path('sponsors/', views.SponsorListAPIView.as_view(), name='sponsor-list'),
    path('sponsors/<int:id>/', views.SponsorDetailUpdateAPIView.as_view(), name='sponsor-detail'),
    path('students/', views.StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('students/<int:id>/', views.StudentDetailUpdateDeleteAPIView.as_view(), name='student-detail-update-delete'),
    path('students/<int:student_id>/allocated-amounts/', views.AllocatedAmountListCreateAPIView.as_view(), name='allocated-amount-list-create'),
    path('students/<int:student_id>/allocated-amounts/<int:sponsor_id>/', views.AllocatedAmountDetailUpdateDeleteAPIView.as_view(), name='allocated-amount-detail-update-delete'),
    path('allocated-amount-summary/', views.AllocatedAmountSummaryAPIView.as_view(), name='allocated-amount-summary'),
]
