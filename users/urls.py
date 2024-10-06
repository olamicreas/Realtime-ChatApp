from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login', views.login_view, name='Login'),
    
    path('chat/', include('chat.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)