from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.ChannelListView.as_view(), name='list'),
    path('add/', views.ChannelCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.ChannelUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ChannelDeleteView.as_view(), name='delete'),
]
