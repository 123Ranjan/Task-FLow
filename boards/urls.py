from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.get_boards, name='get_boards'),
    path('boards/create_board/', views.create_board, name='create_board'),
    path('boards/<int:id>/', views.get_board_details, name='get_board_details'),
    path('boards/<int:id>/issues/', views.get_board_issues, name='get_board_issues'),
    path('boards/<int:id>/columns/', views.get_board_columns, name='get_board_columns'),
    path('boards/<int:id>/columns/create/', views.create_board_column, name='create_board_column'),
    path('boards/<int:id>/delete/', views.delete_board, name='delete_board'),
]