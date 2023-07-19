from django.urls import path
from .views import INS, INSDashboard

urlpatterns = [
    path("", INS.as_view()),
    path("dashboard", INSDashboard.as_view()),
]
