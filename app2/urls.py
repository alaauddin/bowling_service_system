from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('section/<int:section_id>/', views.section_overview, name='section_overview'),
    path('lane/<int:lane_id>/errors/', views.lane_errors, name='lane_errors'),
    path('my_repairs/', views.my_repairs, name='my_repairs'),
    path('note/<int:note_id>/edit/', views.edit_note_pending_app2, name='edit_note_pending_app2'),
    path('broken_lane_resolves/', views.broken_lane_resolves, name='broken_lane_resolves'),
    path('all_error_logs/', views.all_error_logs, name='all_error_logs'),
    path('all_errors/', views.all_errors, name='all_errors'),
    path('error/add/', views.add_error, name='add_error'),
    path('error/<int:error_id>/edit/', views.edit_error, name='edit_error'),
    path('all_daily_check_list/', views.all_daily_check_list, name='all_daily_check_list'),
]
