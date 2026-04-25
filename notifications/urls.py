from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/<int:id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/<int:id>/', views.delete_notification, name='delete_notification'),
    path('notifications/create/', views.create_notification, name='create_notification'),
]