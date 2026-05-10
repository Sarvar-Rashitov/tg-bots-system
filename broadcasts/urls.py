from django.urls import path
from . import views

app_name = 'broadcasts'

urlpatterns = [
    path('', views.BroadcastListView.as_view(), name='list'),
    path('add/', views.BroadcastCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.BroadcastUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BroadcastDeleteView.as_view(), name='delete'),
    path('<int:pk>/send/', views.BroadcastSendView.as_view(), name='send'),
]
