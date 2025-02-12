from django.urls import path
from .views import RegisterView, LoginView, ChangePasswordView, ProfileView, ProfileEditView, LogoutView

app_name = "users"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
