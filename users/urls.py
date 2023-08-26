from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('roles/', views.RoleGroupListAPIView.as_view(), name='role_group'),
    path('list/', views.UserListView.as_view(), name='get_users_list'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/',views.UserProfileView.as_view(), name='profile'),
    path('profile/user_profile/',views.UserProfileShowView.as_view(), name='user_profile'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', views.UserPasswordResetView.as_view(), name='reset-password'),
    path('create-student-coordinators/', views.StudentCoordinatorBulkCreateAPIView.as_view(), name='create-student-coordinators'),
]