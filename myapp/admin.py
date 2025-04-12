from django.contrib import admin
from .models import UserProfile, Machine, FaultCase, FaultNote, Warning, Collection

@admin.register(UserProfile) # Register the UserProfile model with the admin site
class UserProfileAdmin(admin.ModelAdmin): # Admin interface for UserProfile
    list_display = ['user', 'role'] # Display these fields in the list view
    search_fields = ['user__username', 'role']  # Enable search by username and role

# Register the Machine model with the admin interface
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'display_assigned_to', 'display_collections', 'created_at'] # Display these fields in the machine list view
    list_filter = ['status', 'created_at', 'collections'] # Add filters for status, created date, and collections
    search_fields = ['name', 'description']  # Enable search by name and description

    def display_assigned_to(self, obj): # Custom method to show assigned users as a comma-separated list
        return ", ".join([user.username for user in obj.assigned_to.all()])
    display_assigned_to.short_description = "Assigned To" # Label for admin column

    def display_collections(self, obj): # Custom method to show related collections as a comma-separated list
        return ", ".join([collection.name for collection in obj.collections.all()])
    display_collections.short_description = "Collections" # Label for admin column

@admin.register(FaultCase) # Register the FaultCase model with the admin interface
class FaultCaseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'machine', 'reported_by', 'status', 'created_at'] # Display these fields in the fault case list view
    list_filter = ['status', 'created_at']  #Add filters for status and creation date
    search_fields = ['machine__name', 'reported_by__username'] # Enable search by machine name and reporter username

# Rest of code similar to above
@admin.register(FaultNote) 
class FaultNoteAdmin(admin.ModelAdmin):
    list_display = ['fault_case', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['fault_case__machine__name', 'note']

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ['machine', 'warning_text', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['machine__name', 'warning_text']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
