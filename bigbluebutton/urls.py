from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/<meetingID>', views.create_meeting, name='create'),
    path('join', views.join_meeting, name='join'),
    path('join_get/<meeting_id>/<moderator_pw>/<full_name>',views.get_join_meeting, name='join_get'),
    path('end_meeting/<meetingID>',views.end_meeting, name='end'),
]
