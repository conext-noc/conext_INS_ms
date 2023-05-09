from django.urls import path
from .views import INS

urlpatterns = [
    path("", INS.as_view())
]
