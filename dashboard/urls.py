from django.urls import path
from . import views

urlpatterns = [
    # Sponsor URLs
    path('sponsors/', views.SponsorListAPIView.as_view(), name='sponsor_list'),
    path('sponsors/<uuid:id>/', views.SponsorDetailUpdateAPIView.as_view(), name='sponsor_detail_update_delete'),

    # Student URLs
    path('students/', views.StudentListCreateAPIView.as_view(), name='student_list_create'),
    path('students/<uuid:id>/', views.StudentDetailUpdateDeleteAPIView.as_view(), name='student_detail_update_delete'),

    # Allocated Amount URLs
    path('students/<uuid:student_id>/allocated-amounts/', views.AllocatedAmountListCreateAPIView.as_view(),
         name='allocated_amount_list_create'),
    path('students/<uuid:student_id>/allocated-amounts/<uuid:sponsor_id>/',
         views.AllocatedAmountDetailUpdateDeleteAPIView.as_view(), name='allocated_amount_detail_update_delete'),
]
