from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user_home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('uploadimage/', views.upload_image, name='upload_image'),
    path('logout/', views.log_out, name='logout')
]