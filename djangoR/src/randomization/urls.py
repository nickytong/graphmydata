from django.conf.urls import include, url
from . import views 
urlpatterns = [
    url(r'^test$', views.TestView.as_view()),
    url(r'^CompleteRandomization$', views.CompleteRandomizationView.as_view()),
    url(r'^BlockRandomization$', views.BlockRandomizationView.as_view()),
    url(r'^StratifiedCompleteRandomization$', views.StratifiedCompleteRandomizationView.as_view()),
    url(r'^StratifiedBlockRandomization$', views.StratifiedBlockRandomizationView.as_view()),
    url(r'^MinimizationRandomization$', views.MinimizationRandomizationView.as_view()),
   ]