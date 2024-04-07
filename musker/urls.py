from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("check_meep/", check_meep, name="check_meep"),
    path("like_unlike/<int:pk>/", Like_unlike, name='like-unlike'),
    path("like_unlike2/<int:pk>/<int:pk2>/", Like_unlike2, name='like-unlike2'),
    path("meep_share/<int:pk>/", meep_share, name='meep-share'),
    path("send_meep_link/<int:pk>/", send_meep_link, name='send-meep-link'),
    path("share_meep_profile/<int:pk>/", share_meep_profile, name='share-meep-profile'),
    path("like_unlike3/<int:pk>/", like_unlike3, name='like-unlike3'),

]
