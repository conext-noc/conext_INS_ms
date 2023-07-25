from django.urls import path
from .views import INS, INSDashboard, NewOnus

urlpatterns = [
    path("", INS.as_view()),
    path("onus", NewOnus.as_view()),
    path("dashboard", INSDashboard.as_view()),
]
