from colossus.apps.core import views as core_views
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('saml', views.ssoLogin, name="sso_login"),
    path('attrs/', views.attributes, name="attrs"),
    path('metadata/', views.metadata, name="metadata"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('setup/', core_views.setup, name='setup'),
    path('setup/account/', core_views.setup_account, name='setup_account'),
]
