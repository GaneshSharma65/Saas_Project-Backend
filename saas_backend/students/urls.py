from django.urls import path
from . import views

urlpatterns = [
    path('students/add/', views.add_student),
    path('students/list/', views.list_students),
    path('students/update/<int:student_id>/', views.update_student),
    path('students/delete/<int:student_id>/', views.delete_student),


]
