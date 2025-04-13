"""
models.py

This module defines the data models for the Factory Machinery Status & Repair Tracking System.
It contains definitions for Users (extended by a UserProfile), Machines, Fault Cases (for tracking
machine failures), Fault Notes (for adding comments and images to fault cases), Warnings (for
machine alerts) and Collections (groupings of machines). Each model has been commented to explain
its purpose and design decisions.
"""

from django.db import models
from django.contrib.auth.models import User
import re

#####################
# UserProfile Model #
#####################
class UserProfile(models.Model):
    """
    Extends the Django built-in User model by adding a 'role' field to define the type
    of user in the system (Manager, Technician, Repair, View-only).
    """
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
        ('View-only', 'View-only'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='technician')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


#################
# Machine Model #
#################
class Machine(models.Model):
    """
    Represents a piece of machinery in the factory. Each machine has a name, a description,
    a status (OK, Warning, Fault), an optional image and a record of users (technicians or repair
    personnel) assigned to it.
    """
    STATUS_CHOICES = (
        ('OK', 'OK'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    image = models.ImageField(upload_to='machines/', blank=True, null=True)

    assigned_to = models.ManyToManyField(User, related_name='assigned_machines', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


###################
# FaultCase Model #
###################
class FaultCase(models.Model):
    """
    Captures a fault reported for a machine. Contains information about the machine, who reported
    the fault, the title/description and the current status of the fault (open or resolved).
    Each fault case is linked to the relevant machine to track its history.
    """
    FAULT_STATUS_CHOICES = (
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    )
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="fault_cases")
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reported_faults")
    status = models.CharField(max_length=20, choices=FAULT_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Fault #{self.pk} - {self.machine.name} ({self.get_status_display()})"


###################
# FaultNote Model #
###################
class FaultNote(models.Model):
    """
    Represents a note associated with a fault case. A note may include text and an optional image,
    and it tracks who created the note and when it was added. This allows detailed logging for
    each fault incident.
    """
    fault_case = models.ForeignKey(FaultCase, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    image = models.ImageField(upload_to='fault_notes/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="fault_notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for Fault #{self.fault_case.pk} by {self.created_by}"


#################
# Warning Model #
#################
class Warning(models.Model):
    """
    Represents a warning signal associated with a machine. Warnings are free-text alerts that can
    be set by technicians. This model tracks the machine, the warning text, the user who created the
    warning, whether it is active, and when it was created.
    """
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="warnings")
    warning_text = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="warnings_created")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Warning on {self.machine.name}: {self.warning_text}"


#################
# Collection Model #
####################
class Collection(models.Model):
    """
    Allows you to group machines into collections (for example, by physical location or type).
    Each collection has a unique name and can contain multiple machines. The name is validated by a
    regular expression to only include letters, numbers, and hyphens.
    """
    name = models.CharField(max_length=50, unique=True)
    machines = models.ManyToManyField(Machine, related_name="collections", blank=True)

    def clean(self):
        if not re.match(r'^[A-Za-z0-9\-]+$', self.name):
            from django.core.exceptions import ValidationError
            raise ValidationError("Collection names can only contain letters, numbers, and hyphens.")

    def __str__(self):
        return self.name
