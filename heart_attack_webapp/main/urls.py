from . import views

from django.urls import path


urlpatterns = [
    path('', views.MainFormView.as_view(), name='index'),
    path('results', views.ResultsView.as_view(), name='results')
]
