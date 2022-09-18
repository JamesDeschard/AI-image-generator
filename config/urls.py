from django.urls import path, re_path

from main.views import Home

urlpatterns = [
    path('', Home.as_view()),
    re_path(r'^(?P<prompt_params>[\w\s]+)$', Home.as_view()),
]
