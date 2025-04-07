from django.urls import path

from . import views

app_name = "myapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("guide/", views.guide, name="guide"),
    path("employee_login/", views.employee_login, name="employee_login"),
    path("machines/", views.machines, name="machines"),
    path("products/", views.products, name="products"),
]