from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from myapp import views

urlpatterns = [
    path('myapp/', views.snippet_list),
    path('myapp/<int:pk>/', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)