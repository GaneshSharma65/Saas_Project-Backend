from django.urls import path
from . import views

urlpatterns = [
     path("assessments/add/", views.add_assessment),
    path("scores/add/", views.add_score),
     path("scores/update/<int:score_id>/", views.update_score),
    path("scores/delete/<int:score_id>/", views.delete_score),
    path("progress/<int:project_id>/<int:week>/", views.weekly_progress),
    path("report/student/<int:project_id>/<int:student_id>/", views.student_progress_report),
]