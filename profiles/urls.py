from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from profiles.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/user/login'}, name="logout"),
    url(r'^profile/$', login_required(ProfileView.as_view()), name="profile"),
]
