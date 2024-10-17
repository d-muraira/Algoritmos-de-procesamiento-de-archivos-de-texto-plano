from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('autocompletar/', views.autocompletar_view, name='autocompletar'),
    path('lcs/', views.lcs, name="lcs"),
    path('manacher/',views.Manacher, name='manacher'),
]