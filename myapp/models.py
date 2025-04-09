from django.db import models
from django.contrib.auth.models import User
import re

# Extend the UserProfile with a role field (technician, repair, manager, viewer)
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('technician', 'Technician'),
        ('repair', 'Repair'),
        ('manager', 'Manager'),
        ('viewer', 'View-only'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='technician')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Machine(models.Model):
    STATUS_CHOICES = (
        ('OK', 'OK'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    image = models.ImageField(upload_to='machines/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    # Allows multiple users (technicians/repair personnel) to be assigned to a machine
    assigned_to = models.ManyToManyField(User, related_name='assigned_machines', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FaultCase(models.Model):
    FAULT_STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    # Links each fault case to a Machine; allows multiple fault cases per machine
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="fault_cases")
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reported_faults")
    status = models.CharField(max_length=20, choices=FAULT_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Fault #{self.pk} - {self.machine.name} ({self.get_status_display()})"


class FaultNote(models.Model):
    # Links each note to a FaultCase; allows multiple notes per case
    fault_case = models.ForeignKey(FaultCase, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    image = models.ImageField(upload_to='fault_notes/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="fault_notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for Fault #{self.fault_case.pk} by {self.created_by}"


class Warning(models.Model):
    # Each warning is linked to a Machine
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="warnings")
    warning_text = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="warnings_created")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Warning on {self.machine.name}: {self.warning_text}"


class Collection(models.Model):
    # A unique collection name validated by regex (letters, numbers, hyphens only)
    name = models.CharField(max_length=50, unique=True)
    machines = models.ManyToManyField(Machine, related_name="collections", blank=True)

    def clean(self):
        # Enforce allowed characters in collection names
        if not re.match(r'^[A-Za-z0-9\-]+$', self.name):
            from django.core.exceptions import ValidationError
            raise ValidationError("Collection names can only contain letters, numbers, and hyphens.")

    def __str__(self):
        return self.name
