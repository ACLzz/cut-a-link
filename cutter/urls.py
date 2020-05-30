from django.urls import path
from cutter.views import IndexView, app_redirect, extra

app_name = 'cutter'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:short>/', app_redirect, name='redirect'),
    path('<str:short>/extra/', extra, name='extra')
]
