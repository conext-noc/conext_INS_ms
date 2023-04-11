from django.urls import path
from .views import INS,CHECK

urlpatterns = [
    path("", INS.as_view()),
    path("check/", CHECK.as_view()),
]
