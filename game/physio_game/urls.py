from django.contrib import admin
from django.urls import path, include
# from physio_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("physio_app.urls")),
    
    
]
