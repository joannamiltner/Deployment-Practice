from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('favorite/<destination_id>', views.favorite),
    path('description/<destination_id>', views.description),
    path('create_trip', views.create_trip),
    path('add', views.add),
    path('logout', views.logout),
    path('traveldashboard', views.traveldashboard),
    path('createuser', views.createuser),    
    path('login', views.login)
]
