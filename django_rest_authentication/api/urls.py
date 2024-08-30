from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.index),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('booklist/',views.BookViewLIst.as_view()),
    path('book/',views.BookView.as_view()),
    path('user/',views.UserView.as_view()),


]