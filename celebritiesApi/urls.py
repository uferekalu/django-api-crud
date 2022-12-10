from django.urls import path
from . import views

urlpatterns = [
    path('api/celebs', views.celebrities_list),
    path('api/celebs/<int:id>', views.celebrity_detail)
]