from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='monitor_home'),
    # URL for system stats
    path('system-stats/', views.get_system_stats, name='system_stats'),

    # URL for process list
    path('processes/', views.get_process_list, name='process_list'),

    # URL for killing a process
    path('kill/', views.kill_process, name='kill_process'),
]
