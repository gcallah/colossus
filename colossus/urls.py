from django.conf import settings
from django.urls import include, path

from colossus.apps.core import views as core_views
from colossus.apps.accounts import views as account_views


urlpatterns = [
    # path('saml2_auth/', include('django_saml2_auth.urls')),
    # path('accounts/login/', django_saml2_auth.views.signin),
    # path('admin/login/', django_saml2_auth.views.signin),
    path('', core_views.dashboard, name='dashboard'),
    path('', include('colossus.apps.subscribers.urls', namespace='subscribers')),
    path('attrs/', account_views.attributes, name="attrs"),
    path('metadata/', account_views.metadata, name="metadata"),
    path('setup/', core_views.setup, name='setup'),
    path('setup/account/', core_views.setup_account, name='setup_account'),
    path('settings/', core_views.SiteUpdateView.as_view(), name='settings'),
    path('auth/', include('colossus.apps.accounts.urls')),
    path('lists/', include('colossus.apps.lists.urls', namespace='lists')),
    path('notifications/', include('colossus.apps.notifications.urls', namespace='notifications')),
    path('templates/', include('colossus.apps.templates.urls', namespace='templates')),
    path('campaigns/', include('colossus.apps.campaigns.urls', namespace='campaigns')),
    path('<slug:mailing_list_slug>/', core_views.subscribe_shortcut, name='subscribe_shortcut'),
    path('<slug:mailing_list_slug>/unsubscribe/', core_views.unsubscribe_shortcut, name='unsubscribe_shortcut'),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
