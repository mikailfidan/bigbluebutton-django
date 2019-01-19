from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/<meetingID>', views.create_meeting, name='create'),
    path('join_meeting/<meetingID>',views.join_meeting, name='join'),
    path('end_meeting/<meetingID>',views.end_meeting, name='end'),
]
