"""
admin.py

This module registers the models with the Django admin interface and customizes
the display of model data. Each registered model includes additional metadata such as
list display fields, search fields, and list filters to make it easier for administrators
to manage the data within the Factory Machinery Status & Repair Tracking System.
"""

from django.contrib import admin
from .models import UserProfile, Machine, FaultCase, FaultNote, Warning, Collection

##################################
# UserProfile Admin Registration #
##################################
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Configures the display of the UserProfile model in the admin panel.
    The list_display option shows the username (via the related User object)
    and the user role. It also enables searching by username and role.
    """
    list_display = ['user__username', 'role']
    search_fields = ['user__username', 'role']


##############################
# Machine Admin Registration #
##############################
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    """
    Configures the Machine model display in the admin panel.
    It shows key fields such as name, status, assigned personnel, associated collections,
    and the creation date. Additionally, it provides filters for status, creation date, and
    collections, along with a search option over the machine's name and description.
    """
    list_display = ['name', 'status', 'display_assigned_to', 'display_collections', 'created_at']
    list_filter = ['status', 'created_at', 'collections']
    search_fields = ['name', 'description']

    def display_assigned_to(self, obj):
        # Returns a comma-separated string of usernames assigned to the machine.
        return ", ".join([user.username for user in obj.assigned_to.all()])
    display_assigned_to.short_description = "Assigned To"

    def display_collections(self, obj):
        # Returns a comma-separated string of the collection names the machine belongs to.
        return ", ".join([collection.name for collection in obj.collections.all()])
    display_collections.short_description = "Collections"


################################
# FaultCase Admin Registration #
################################
@admin.register(FaultCase)
class FaultCaseAdmin(admin.ModelAdmin):
    """
    Configures the FaultCase model in the admin panel.
    It displays the fault case ID, associated machine, reporting user, fault status,
    and creation date. Filtering by status and creation date along with search functionality
    enhances data management.
    """
    list_display = ['pk', 'machine', 'reported_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['machine__name', 'reported_by__username']


################################
# FaultNote Admin Registration #
################################
@admin.register(FaultNote)
class FaultNoteAdmin(admin.ModelAdmin):
    """
    Sets up the FaultNote model in the admin interface.
    Displays the linked fault case, creator of the note, and the time it was created.
    Also includes filters and search functionality to ease note management.
    """
    list_display = ['fault_case', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['fault_case__machine__name', 'note']


##############################
# Warning Admin Registration #
##############################
@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    """
    Registers the Warning model with the admin interface.
    Displays the related machine, warning text, whether the warning is active, and
    the creation date, and allows filtering by active status and creation date. This
    helps quickly identify and manage warnings.
    """
    list_display = ['machine', 'warning_text', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['machine__name', 'warning_text']


#################################
# Collection Admin Registration #
#################################
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    Configures the Collection model in the admin panel.
    Displays the collection name and provides a search field to easily find specific collections.
    """
    list_display = ['name']
    search_fields = ['name']
