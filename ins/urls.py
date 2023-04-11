from django.urls import path
from .views import SCH,CHECK

urlpatterns = [
    path("", SCH.as_view()),
    path("check/", CHECK.as_view()),
    path("<int:id>/", SCH.as_view(), name='contract')
]
