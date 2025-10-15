from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('unread/', views.UnreadNotificationListView.as_view(), name='unread-notifications'),
    path('<int:notification_id>/read/', views.NotificationMarkAsReadView.as_view(), name='mark-notification-read'),
    path('mark-all-read/', views.NotificationMarkAllAsReadView.as_view(), name='mark-all-notifications-read'),
    path('count/', views.NotificationCountView.as_view(), name='notification-count'),
]