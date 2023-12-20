# physio_game/urls.py
from django.contrib import admin
from django.urls import path
from physio_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index_li', views.index_li, name='index_li'),
    path('', views.index, name='index'),
    path('dash', views.dashboard),
    path('emailsaving', views.email),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('game_selection/', views.game_selection, name='game_selection'),
    path('physio_category/', views.physio_category, name='physio_category'),
    path('physio_category/General_Wellness', views.general_well),
    path('physio_category/Cardiac', views.cardiac),
    path('physio_category/Falls_Prevention', views.fall_prevention),
    path('physio_category/Orthopedic', views.orthopedic),
    path('chat', views.chat, name='chat'),
    path('physio_category/head_game_1', views.head_game_1),
    path('physio_category/shoulder_game_1', views.shoulder_game_1),
    path('physio_category/shoulder_game_2', views.shoulder_game_2),
    path('physio_category/shoulder_ex/', views.shoulder_ex, name='shoulder_ex'),
    path('physio_category/shoulder_exercise_data/', views.shoulder_exercise_data, name='shoulder_exercise_data'),
    path('physio_category/shoulderwin', views.shoulderwin),
    path('physio_category/leg_ex/', views.leg_ex, name='leg_ex'),
    path('physio_category/legwin', views.legwin),
    path('physio_category/leg_exercise_data/', views.leg_exercise_data, name='leg_exercise_data'),   
]
