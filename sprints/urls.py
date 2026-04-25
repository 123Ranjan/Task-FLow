from django.urls import path
from . import views

urlpatterns = [
    path('sprints/', views.get_sprints, name='get_sprints'),
    path('sprints/create/', views.create_sprint, name='create_sprint'),
    path('sprints/byBoard/<int:board_id>/', views.get_sprints_by_board, name='get_sprints_by_board'),
    path('sprints/<int:sprint_id>/issues/', views.get_sprint_issues, name='get_sprint_issues'),
    path('sprints/<int:sprint_id>/start/', views.start_sprint, name='start_sprint'),
    path('sprints/<int:sprint_id>/close/', views.close_sprint, name='close_sprint'),
    path('sprints/<int:sprint_id>/delete/', views.delete_sprint, name='delete_sprint'),  # ✅ FIXED
]