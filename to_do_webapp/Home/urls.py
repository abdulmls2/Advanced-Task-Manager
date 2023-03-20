from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views



urlpatterns=[

path('', views.dashboard, name='dashboard'),
path('Settings', views.Settings, name='Settings'),
path('setting_security', views.setting_security, name='setting_security'),


#creating the newly task
path('create_task', views.create_task, name='create_task'),
path('task_list_view', views.task_list_view, name='task_list_view'),
path('task_edit/<int:id>', views.task_edit, name='task_edit'),
path('task_edit/<int:id>', views.task_edit, name='task_edit'),

path('delete_tasks', views.delete_tasks, name='delete_tasks'),



#calendar view
path('calendar_view', views.calendar_view, name='calendar_view'),
path('all_tasks_calender_view', views.all_tasks_calender_view, name='all_tasks_calender_view'),

#get chart data
path('get_chart_data', views.get_chart_data, name='get_chart_data'),



]