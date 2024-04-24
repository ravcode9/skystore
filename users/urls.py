from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, RegisterMessageView, PasswordRecoveryView

app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/confirm/<str:token>/', email_verification, name='email_verification'),
    path('register/message/', RegisterMessageView.as_view(), name='register_message'),
    path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
]
