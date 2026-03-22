from django.urls import path
from . import views

urlpatterns = [
    path('', views.diet_home, name='diet'),
    path('save/', views.save_diet_plan, name='save_diet_plan'),
]
