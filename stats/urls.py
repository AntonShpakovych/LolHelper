from django.urls import path
from . import views


urlpatterns = [
    path('',views.basic_page,name='stats'),
    path('detail_page/<user>/<region>/',views.detail_page,name='detail_page')
]