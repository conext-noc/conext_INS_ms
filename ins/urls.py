from django.urls import path
from .views import INS, INSDashboard

urlpatterns = [
    path("", INS.as_view()),
    path("install-dashboard", INSDashboard.as_view()),
]
