from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/<meetingID>', views.create_meeting, name='create'),
    path('joinmeeting/<meetingID>',views.join_meeting, name='join'),
    path('endmeeting/<meetingID>',views.end_meeting, name='end'),
    path('infomeeting/<meetingID>',views.info_meeting, name='info'),
    path('attjoin', views.attjoin, name='attjoin'),
]
