from colossus.apps.core import views as core_views
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('saml', views.ssoLogin, name="sso_login"),
    path('attrs/', views.attributes, name="attrs"),
    path('metadata/', views.metadata, name="metadata"),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('setup/', core_views.setup, name='setup'),
    path('setup/account/', core_views.setup_account, name='setup_account'),
]
