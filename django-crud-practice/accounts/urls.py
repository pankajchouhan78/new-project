from django.urls import path

from . import api as Api
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout_user"),
    # api
    path("view_cources/", Api.view_cources, name="view_api"),
    path("course_create/", Api.create_course, name="course_create"),
]
