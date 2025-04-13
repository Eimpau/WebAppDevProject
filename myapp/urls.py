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
    path("add_machine/", views.add_machine, name="add_machine"),
    # Delete Machine route: Processes deletion of a machine, expects a machine ID as parameter.
    path("delete_machine/<int:machine_id>/", views.delete_machine, name="delete_machine"),
    # Assign Technician route: For managers to assign a technician to a machine, identified by its ID.
    path("assign_technician/<int:machine_id>/", views.assign_technician, name="assign_technician"),
    # Assign Repair route: For managers to assign repair personnel to a machine.
    path("assign_repair/<int:machine_id>/", views.assign_repair, name="assign_repair"),
    path("create_fault/", views.create_fault, name="create_fault"),
    # Add Fault Note route: Enables users to add notes to a specific fault case, identified by its ID.
    path("add_fault_note/<int:fault_id>/", views.add_fault_note, name="add_fault_note"),
    path("create_warning/", views.create_warning, name="create_warning"),
    # Delete Warning route: Processes deletion of a warning by its ID.
    path("delete_warning/<int:warning_id>/", views.delete_warning, name="delete_warning"),
    # Mark Resolved route: Marks a fault case as resolved by its ID.
    path("mark_resolved/<int:fault_id>/", views.mark_resolved, name="mark_resolved"),
    path("export_report/", views.export_report, name="export_report"),
    # Delete User route: Enables a manager to delete a user account; identified by user ID.
    path("delete_user/<int:user_id>/", views.delete_user, name="delete_user"),

    # New API endpoint for recording warnings and faults (POST requests)
    path("api/record_warning_fault/", views.record_warning_fault, name="record_warning_fault"),
]
