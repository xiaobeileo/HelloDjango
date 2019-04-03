
from django.urls import path
from . import views

app_name = 'pools'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(), name='results' ),


    # path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name = 'detail'),
    #
    # #note:here must be <int:question_id>, if there are space will be error
    # path('results/<int:question_id>/', views.results, name='results'),
    path('vote/<int:question_id>/', views.vote, name='Vote'),

]
