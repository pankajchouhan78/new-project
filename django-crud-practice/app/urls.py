from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete_emp/<int:pk>", views.delete_employee, name="delete_emp"),
    path("update_emp/<int:pk>", views.update_employee, name="update_emp"),
]
