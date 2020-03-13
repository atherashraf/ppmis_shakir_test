from django.urls import path
from .views import *


urlpatterns = [
    path('jqx/grid_table_data/<str:table_name>/', get_jqx_grid_table_data, name='jqx_grid_table_data'),
]
