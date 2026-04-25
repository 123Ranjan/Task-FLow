from django.urls import path
from .views import *

urlpatterns = [
    # Issue endpoints
    path('issues/create/', create_issue, name='create-issue'),
    path('issues/<int:id>/', get_issue, name='get-issue'),
    path('issues/backlog/', backlog, name='backlog'),
    path('issues/<int:id>/assign-sprint/', assign_to_sprint, name='assign-sprint'),
    path('issues/<int:id>/move-to-board/', move_to_board, name='move-to-board'),  # ✅ Keep one
    path('issues/<int:id>/status/', update_issue_status, name='update-status'),
    path('issues/<int:id>/move-backlog/', move_to_backlog, name='move-backlog'),

    # Comment endpoints
    path('issues/<int:issue_id>/comments/', get_comments, name='get-comments'),
    path('issues/<int:issue_id>/add-comment/', add_comment, name='add-comment'),

    # Board card endpoints
    path('boardCard/board/<int:board_id>/', get_board_cards, name='board-cards'),
    path('boardCard/<int:card_id>/move/<int:column_id>/', move_card, name='move-card'),
]