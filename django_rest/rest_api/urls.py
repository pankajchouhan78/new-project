
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='userviewset')
router.register(r'users_model_viewset', UserModelViewsets, basename = "users_model_view") 

urlpatterns = [
    path('person/', person),
    path('update_person/<int:pk>', update_person),

    # user api
    path('users/', users),
    path('users/<int:pk>', users_pk),

    # apiview
    path('check_login', check_login.as_view()),
    path('login', LoginView.as_view()),
    path('users_apiview/',UserAPIView.as_view()),
    path('users_apiview/<int:pk>',UserAPIView.as_view()),

    # router
    path('viewsets/', include(router.urls)),

    # generics view
    path('user_list', UserList.as_view()),
    path('user_detail/<int:pk>', UserDetail.as_view()),
    
]
