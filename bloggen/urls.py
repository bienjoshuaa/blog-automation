from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_blog, name='generate_blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
]



