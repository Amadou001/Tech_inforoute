from django.urls import path
from . import views

urlpatterns = [
    path('datasets/', views.dataset_list, name='dataset-list'),
    path('datasets/<int:pk>/', views.dataset_detail, name='dataset-detail'),
]
