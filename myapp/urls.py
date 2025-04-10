from django.urls import path

from . import views

app_name = "myapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("guide/", views.guide, name="guide"),
    path("employee_login/", views.employee_login, name="employee_login"),
    path("employee_logout/", views.employee_logout, name="employee_logout"),
    path("machines/", views.machines, name="machines"),
    path("products/", views.products, name="products"),
    path("manager_dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("technician_dashboard/", views.technician_dashboard, name="technician_dashboard"),
    path("repair_dashboard/", views.repair_dashboard, name="repair_dashboard"),
    path("viewonly_dashboard/", views.viewonly_dashboard, name="viewonly_dashboard"),
]