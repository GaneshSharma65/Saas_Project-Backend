from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('projects/create/', views.create_project),
    path('projects/list/', views.list_projects),
]
