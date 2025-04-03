from django.urls import path

from . import views

app_name = "myapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("guide/", views.guide, name="guide"),
    path("login/", views.login, name="login"),
    path("machineDescription/", views.machineDescription, name="machineDescription"),
    path("products/", views.products, name="products"),


]