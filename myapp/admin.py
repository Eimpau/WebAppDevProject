from django.contrib import admin
from .models import UserProfile, Machine, FaultCase, FaultNote, Warning, Collection

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    search_fields = ['user__username', 'role']

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'display_assigned_to', 'display_collections', 'created_at']
    list_filter = ['status', 'created_at', 'collections']
    search_fields = ['name', 'description']

    def display_assigned_to(self, obj):
        return ", ".join([user.username for user in obj.assigned_to.all()])
    display_assigned_to.short_description = "Assigned To"

    def display_collections(self, obj):
        return ", ".join([collection.name for collection in obj.collections.all()])
    display_collections.short_description = "Collections"

@admin.register(FaultCase)
class FaultCaseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'machine', 'reported_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['machine__name', 'reported_by__username']

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
