from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('join', views.join_meeting, name='join'),
    path('join_get/<meeting_id>/<moderator_pw>/<full_name>',views.get_join_meeting, name='join_get'),
    path('end_meeting/<meeting_id>/<moderator_pw>',views.end_meeting, name='end_meeting'),


]
