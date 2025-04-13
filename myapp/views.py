"""
views.py

This module contains the view functions for the web application. It handles all
HTTP requests and renders the appropriate templates. The functions include static
page renders (e.g., home, about, guide), user authentication (login/logout), role-based
dashboard rendering (Manager, Technician, Repair, View-only), and functionality for
managing machines, fault cases, warnings, and user assignments.
"""

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, Value, IntegerField
import csv

from .models import UserProfile, Machine, FaultCase, FaultNote, Warning, Collection
from .forms import LoginForm, ManagerUserRegistrationForm

#####################
# Public Page Views #
#####################
def home(request):
    """
    Render the 'Index' that is the landing page for the application.
    """
    context = {}
    return render(request, "myapp/index.html", context)


def about(request):
    """
    Render the 'About' page that describes information about the company.
    """
    context = {}
    return render(request, "myapp/about.html", context)


def guide(request):
    """
    Render the 'Guide' page which provides user guidance and instructions.
    """
    context = {}
    return render(request, "myapp/guide.html", context)

def machines(request):
    """
    Render the 'Machines' page that lists all machines in the system.
    """
    context = {}
    return render(request, "myapp/machines.html", context)

def products(request):
    """
    Render the 'Products' page that showcases the products or services offered.
    """
    context = {}
    return render(request, "myapp/products.html", context)


########################
# Authentication Views #
########################
def employee_login(request):
    """
    Handle user login functionality.
    - Processes POST request with login form data.
    - Validates credentials using Django's authentication.
    - On success, logs in the user and redirects them to the appropriate dashboard based on user role.
    - On failure, returns the login form with an error message.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect user based on their role using the extended UserProfile model.
                try:
                    role = user.userprofile.role
                except Exception:
                    role = None
                if role == "Manager":
                    return redirect("myapp:manager_dashboard")
                elif role == "Technician":
                    return redirect("myapp:technician_dashboard")
                elif role == "Repair":
                    return redirect("myapp:repair_dashboard")
                elif role == "View-only":
                    return redirect("myapp:viewonly_dashboard")
                else:
                    return redirect("myapp:home")
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, "myapp/login.html", context)


@login_required
def employee_logout(request):
    """
    Logs out the current user and redirects them to the homepage.
    """
    logout(request)
    return redirect("myapp:home")


#######################################
# Dashboard and Data Management Views #
#######################################
@login_required
def manager_dashboard(request):
    """
    Renders the Manager Dashboard.
    This view is accessible by Manager users as well as any superuser.
    It provides functionalities such as:
      - Creating new users via the ManagerUserRegistrationForm.
      - Viewing summary statistics for machine statuses.
      - Filtering machines by collections.
      - Ordering machines based on priority (Fault > Warning > OK).
      - Managing assignments (Technicians and Repair personnel).
    """
    # Allow superusers to bypass role restrictions.
    if not request.user.is_superuser and request.user.userprofile.role != "Manager":
        return HttpResponseForbidden("You are not authorized to view the Manager Dashboard.")
    
    if request.method == "POST":
        form = ManagerUserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user with an associated user profile.
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
    else:
        form = ManagerUserRegistrationForm()

    # Retrieve dynamic machine statistics and recent fault cases.
    active_machines = Machine.objects.filter(status="OK").count()
    warning_machines = Machine.objects.filter(status="Warning").count()
    faulty_machines = Machine.objects.filter(status="Fault").count()
    recent_fault_cases = FaultCase.objects.order_by("-created_at")[:5]
    collections = Collection.objects.all()

    collection_filter = request.GET.get("collection_filter")
    if collection_filter:
        machines = Machine.objects.filter(collections__pk=collection_filter).distinct()
    else:
        machines = Machine.objects.all()

    machines = machines.annotate(
        priority=Case(
            When(status="Fault", then=Value(1)),
            When(status="Warning", then=Value(2)),
            When(status="OK", then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by("priority", "created_at")

    technicians = User.objects.filter(userprofile__role="Technician")
    repair_personnel = User.objects.filter(userprofile__role="Repair")
    users = User.objects.filter(is_superuser=False).exclude(pk=request.user.pk).order_by("username")

    context = {
        'form': form,
        'active_machines': active_machines,
        'warning_machines': warning_machines,
        'faulty_machines': faulty_machines,
        'recent_fault_cases': recent_fault_cases,
        'collections': collections,
        'machines': machines,
        'technicians': technicians,
        'repair_personnel': repair_personnel,
        'users': users,
    }
    return render(request, "myapp/manager_dashboard.html", context)


@login_required
def technician_dashboard(request):
    """
    Renders the Technician Dashboard.
    This view is accessible by Manager or Technician users as well as superusers.
    It provides functionalities such as:
      - Orders machines based on a defined priority.
      - Displays machines assigned to the technician.
      - Shows all machines for broader context.
      - Lists open fault cases relevant to the technician.
    """
    if not request.user.is_superuser and request.user.userprofile.role not in ["Manager", "Technician"]:
        return HttpResponseForbidden("You are not authorized to view the Technician Dashboard.")

    priority_annotation = Case(
        When(status="Fault", then=Value(1)),
        When(status="Warning", then=Value(2)),
        When(status="OK", then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
    assigned_machines = request.user.assigned_machines.all() \
        .annotate(priority=priority_annotation) \
        .order_by("priority", "created_at")
    all_machines = Machine.objects.all() \
        .annotate(priority=priority_annotation) \
        .order_by("priority", "created_at")

    open_fault_cases = FaultCase.objects.filter(
        Q(machine__in=assigned_machines) | Q(reported_by=request.user),
        status="open"
    )
    
    context = {
        'assigned_machines': assigned_machines,
        'all_machines': all_machines,
        'open_fault_cases': open_fault_cases,
    }
    return render(request, "myapp/technician_dashboard.html", context)


@login_required
def repair_dashboard(request):
    """
    Renders the Repair Dashboard.
    This view is accessible by Manager, Technician, and Repair users as well as superusers.
    It provides functionalities such as:
      - Orders machines based on a defined priority.
      - Displays machines assigned to the Repair.
      - Shows all machines for broader context.
      - A list of repair cases that are open.
      - Active warnings on machines.
    """
    if not request.user.is_superuser and request.user.userprofile.role not in ["Manager", "Technician", "Repair"]:
        return HttpResponseForbidden("You are not authorized to view the Repair Dashboard.")
    
    priority_annotation = Case(
        When(status="Fault", then=Value(1)),
        When(status="Warning", then=Value(2)),
        When(status="OK", then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
    assigned_machines = request.user.assigned_machines.all() \
        .annotate(priority=priority_annotation) \
        .order_by("priority", "created_at")
    all_machines = Machine.objects.all() \
        .annotate(priority=priority_annotation) \
        .order_by("priority", "created_at")
        
    repair_cases = FaultCase.objects.filter(status__in=["open"])
    warnings = Warning.objects.filter(active=True)
    
    context = {
        'assigned_machines': assigned_machines,
        'all_machines': all_machines,
        'repair_cases': repair_cases,
        'warnings': warnings,
    }
    return render(request, "myapp/repair_dashboard.html", context)


@login_required
def viewonly_dashboard(request):
    """
    Renders the View-Only Dashboard.
    This view provides basic machine status information and summary statistics.
    It orders machines by priority and calculates counts for OK, Warning, and Fault statuses.
    """
    priority_annotation = Case(
        When(status="Fault", then=Value(1)),
        When(status="Warning", then=Value(2)),
        When(status="OK", then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
    machines = Machine.objects.all() \
        .annotate(priority=priority_annotation) \
        .order_by("priority", "created_at")
    
    ok_count = machines.filter(status="OK").count()
    warning_count = machines.filter(status="Warning").count()
    fault_count = machines.filter(status="Fault").count()
    
    context = {
        'machines': machines,
        'ok_count': ok_count,
        'warning_count': warning_count,
        'fault_count': fault_count,
    }
    return render(request, "myapp/viewonly_dashboard.html", context)


##########################################
# Machine Management and Reporting Views #
##########################################
@login_required
def add_machine(request):
    """
    Allows managers to add a new machine to the system.
    Processes both existing collection associations and new comma-separated collections.
    Also handles optional machine image uploads.
    """
    if request.method == "POST":
        machine_name = request.POST.get("name")
        # Retrieve selected existing collections and any new collections specified.
        collection_ids = request.POST.getlist("collections")
        new_collections = request.POST.get("new_collections", "").strip()
        machine_image = request.FILES.get("image")  # optional image

        # Create the machine with default description and OK status.
        machine = Machine.objects.create(
            name=machine_name,
            description="Default description",
            status="OK",
            image=machine_image
        )
        
        # Associate machine with selected existing collections.
        if collection_ids:
            for coll_id in collection_ids:
                try:
                    collection = Collection.objects.get(pk=coll_id)
                    collection.machines.add(machine)
                except Collection.DoesNotExist:
                    continue

        # Process and associate any new collections defined by the manager.
        if new_collections:
            new_list = [n.strip() for n in new_collections.split(",") if n.strip()]
            import re
            for new_coll in new_list:
                if re.match(r'^[A-Za-z0-9\-]+$', new_coll):
                    collection, created = Collection.objects.get_or_create(name=new_coll)
                    collection.machines.add(machine)

        return redirect("myapp:manager_dashboard")
    return redirect("myapp:manager_dashboard")


@login_required
def delete_machine(request, machine_id):
    """
    Handles deletion of a machine. Accessible via a POST request.
    After deletion, redirects back to the Manager Dashboard.
    """
    if request.method == "POST":
        machine = get_object_or_404(Machine, pk=machine_id)
        machine.delete()
    return redirect("myapp:manager_dashboard")


@login_required
def assign_technician(request, machine_id):
    """
    Assigns a technician to a machine.
    Before assigning, it clears any existing technician assignments (users with role "Technician")
    so that the machine can be re-assigned to a new technician.
    """
    if request.method == "POST":
        technician_id = request.POST.get("technician_id")
        machine = get_object_or_404(Machine, pk=machine_id)
        # Clear any existing technicians assigned to this machine
        current_technicians = machine.assigned_to.filter(userprofile__role="Technician")
        for tech in current_technicians:
            machine.assigned_to.remove(tech)
        try:
            technician = User.objects.get(pk=technician_id)
            if technician.userprofile.role == "Technician":
                machine.assigned_to.add(technician)
        except User.DoesNotExist:
            pass
    return redirect("myapp:manager_dashboard")


@login_required
def assign_repair(request, machine_id):
    """
    Assigns repair personnel to a machine.
    Before assigning, it clears any existing repair assignments (users with role "Repair")
    so that the machine can be re-assigned to new repair personnel.
    """
    if request.method == "POST":
        repair_id = request.POST.get("repair_id")
        machine = get_object_or_404(Machine, pk=machine_id)
        # Clear any existing repair personnel assigned to this machine
        current_repair = machine.assigned_to.filter(userprofile__role="Repair")
        for rep in current_repair:
            machine.assigned_to.remove(rep)
        try:
            repair_person = User.objects.get(pk=repair_id)
            if repair_person.userprofile.role == "Repair":
                machine.assigned_to.add(repair_person)
        except User.DoesNotExist:
            pass
    return redirect("myapp:manager_dashboard")


@login_required
def create_fault(request):
    """
    Allows a technician to create a new fault case for a machine.
    Once a fault is reported, the machine's status is updated to 'Fault'.
    """
    if request.method == "POST":
        machine_id = request.POST.get("machine")
        fault_title = request.POST.get("title", "")
        machine = get_object_or_404(Machine, pk=machine_id)
        fault = FaultCase.objects.create(
            machine=machine,
            reported_by=request.user,
            status="open",
            title=fault_title,
        )
        machine.status = "Fault"
        machine.save()
        return redirect("myapp:technician_dashboard")
    return redirect("myapp:technician_dashboard")


@login_required
def add_fault_note(request, fault_id):
    """
    Adds a note (with optional image) to an existing fault case.
    The view handles POST data and then redirects the user back to the appropriate dashboard.
    """
    if request.method == "POST":
        note_text = request.POST.get("note")
        image_file = request.FILES.get("image")
        if note_text or image_file:
            fault = get_object_or_404(FaultCase, pk=fault_id)
            FaultNote.objects.create(
                fault_case=fault,
                note=note_text,
                image=image_file,
                created_by=request.user
            )
        else:
            return redirect("myapp:technician_dashboard")
    return redirect("myapp:technician_dashboard")


@login_required
def create_warning(request):
    """
    Allows a technician to create a warning for a machine.
    Prevents duplicate active warnings (case-insensitive) from being created.
    Updates the machine's status to 'Warning'.
    """
    if request.method == "POST":
        machine_id = request.POST.get("machine")
        warning_text = request.POST.get("warning_text", "").strip()
        machine = get_object_or_404(Machine, pk=machine_id)
        if not Warning.objects.filter(
                machine=machine,
                warning_text__iexact=warning_text,
                active=True
            ).exists():
            Warning.objects.create(
                machine=machine,
                warning_text=warning_text,
                created_by=request.user,
                active=True
            )
        machine.status = "Warning"
        machine.save()
        return redirect("myapp:technician_dashboard")
    return redirect("myapp:technician_dashboard")


@login_required
def delete_warning(request, warning_id):
    """
    Deletes an active warning. Once deleted, checks if the machine has any remaining
    active warnings; if none exist, the machine status is reset to 'OK'.
    """
    if request.method == "POST":
        warning = get_object_or_404(Warning, pk=warning_id)
        machine = warning.machine
        warning.delete()
        if not Warning.objects.filter(machine=machine, active=True).exists():
            machine.status = "OK"
            machine.save()
        return redirect("myapp:repair_dashboard")
    return redirect("myapp:repair_dashboard")


@login_required
def mark_resolved(request, fault_id):
    """
    Marks a fault case as resolved and updates the machine status to 'OK'.
    This view is typically used by repair personnel once maintenance has been completed.
    """
    if request.method == "POST":
        fault = get_object_or_404(FaultCase, pk=fault_id)
        machine = fault.machine
        fault.status = "resolved"
        fault.save()
        machine.status = "OK"
        machine.save()
        return redirect("myapp:repair_dashboard")
    return redirect("myapp:repair_dashboard")


@login_required
def export_report(request):
    """
    Exports a CSV report of machines based on either a specific machine or collection filter.
    The CSV includes details such as machine name, status, description, associated collections,
    and assigned personnel.
    """
    collection_filter = request.GET.get("collection_filter")
    machine_id = request.GET.get("machine_id")
    
    if machine_id:
        qs = Machine.objects.filter(pk=machine_id)
    elif collection_filter:
        qs = Machine.objects.filter(collections__pk=collection_filter).distinct()
    else:
        qs = Machine.objects.all()
    
    qs = qs.annotate(
        priority=Case(
            When(status="Fault", then=Value(1)),
            When(status="Warning", then=Value(2)),
            When(status="OK", then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by("priority", "created_at")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="machines_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Name", "Status", "Description", "Collections", "Assigned Personnel"])
    
    for machine in qs:
        collections = ", ".join([col.name for col in machine.collections.all()])
        assigned = ", ".join([user.username for user in machine.assigned_to.all()])
        writer.writerow([machine.name, machine.status, machine.description, collections, assigned])
    
    return response


@login_required
def delete_user(request, user_id):
    """
    Allows a Manager to delete a user account (excluding self-deletion or deletion of superusers).
    This operation is only processed via a POST request.
    """
    if request.method == "POST":
        if request.user.userprofile.role != "Manager":
            return HttpResponseForbidden("You are not authorized to delete users.")
        user_to_delete = get_object_or_404(User, pk=user_id)
        if user_to_delete == request.user or user_to_delete.is_superuser:
            return HttpResponseForbidden("You cannot delete this user.")
        user_to_delete.delete()
        return redirect("myapp:manager_dashboard")
    return HttpResponseForbidden("Only POST requests are allowed.")
