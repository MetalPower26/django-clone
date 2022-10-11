from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
	path('', views.landing, name='landing'),
	path('perlombaan/', views.perlombaan, name='perlombaan'),
	path('teknis/<str:cfield>', views.teknis, name='teknis'),
]