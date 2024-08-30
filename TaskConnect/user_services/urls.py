from django.urls import path
from user_services.API import api

urlpatterns = [
    # path('', api.index),
    # path('search/', api.SearchAPiView.as_view()),
    path('create_role/', api.RoleCreateView.as_view()),
]