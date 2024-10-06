from django.urls import path
from django.conf import settings

from . import views
from .views import EditPost

urlpatterns = [
    path('', views.index, name='index'),
    path('message/<str:username>', views.message_view, name='message'),
    path('logout/', views.loggout, name='loggout'),
    path('unread/', views.unread_message, name='unread'),
    path('profile/', views.post_view, name='profile'),
    path('edit/<int:pk>', EditPost.as_view(), name='edit'),
    path('online/', views.online_user, name='online'),
    path('search/', views.search, name='search')
]


# If you need a Region object for the foreign key


state = State.objects.create(
    name="Lagos",
    capital="Ikeja",
    code="LA",
    latitude=6.5244,
    longitude=3.3792,

    is_selected=False,
    is_active=True
)
