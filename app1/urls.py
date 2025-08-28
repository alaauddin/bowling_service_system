


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    path('lane/<int:lane_id>/', views.lane_detail, name='lane_detail'),
    path('lane/<int:lane_id>/add_errorlog/', views.add_errorlog, name='add_errorlog'),
    path('lane/<int:lane_id>/add_note/', views.add_note_pending, name='add_note_pending'),
    path('note/<int:note_id>/edit/', views.edit_note_pending, name='edit_note_pending'),
    path('section/<int:section_id>/add_checklist/', views.add_daily_checklist, name='add_daily_checklist'),
    path('checklist/<int:checklist_id>/edit/', views.edit_daily_checklist, name='edit_daily_checklist'),
]