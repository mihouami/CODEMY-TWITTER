from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("check_meep/", check_meep, name="check_meep"),
    path("like_unlike/<int:pk>/", Like_unlike, name='like-unlike'),
    path("like_unlike2/<int:pk>/<int:pk2>/", Like_unlike2, name='like-unlike2')
]
