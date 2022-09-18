from django.urls import path
from . import views

# insert urls here

app_name = 'regis'
urlpatterns = [
	path('form/<str:cfield>', views.index, name='index'),
	path('data/<str:cfield>', views.data, name='data'),
	path('archive/<str:cfield>/<str:objectkey>', views.archive, name='archive')
]