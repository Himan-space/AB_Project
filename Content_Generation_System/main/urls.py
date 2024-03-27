from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    #path('api/data', MonthlyChartData.as_view()),
    path('home', index, name='home'),
    path('download/<str:file_type>', download, name='download'),
]