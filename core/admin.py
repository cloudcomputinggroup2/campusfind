from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Item, AuditLog, SystemSetting, SecurityAlert

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Customized Admin interface for managing campus lost and found posts.
    Provides batch actions, filters, search, and intuitive status updates.
    """
    list_display = [
        'title',
        'status_badge',
        'category',
        'location',
        'user',
        'is_deleted',
        'is_verified_returned',
        'created_at',
    ]
    list_filter = [
        'status',
        'category',
        'is_deleted',
        'is_verified_returned',
        'date_event',
        'created_at',
    ]
    search_fields = [
        'title',
        'description',
        'location',
        'contact',
        'user__username',
        'user__email',
    ]
    list_editable = ['is_verified_returned']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at', 'deleted_at']
    ordering = ['-created_at']
    actions = ['mark_as_claimed_action', 'mark_as_lost_action', 'mark_as_found_action', 'soft_delete_action', 'restore_action']

    fieldsets = (
        ('Item Basic Information', {
            'fields': ('title', 'category', 'status', 'location', 'date_event', 'image')
        }),
        ('Detailed Descriptions & Contact', {
            'fields': ('description', 'contact', 'user')
        }),
        ('Resolution Status & Lifecycle', {
            'fields': ('is_verified_returned', 'resolved_at', 'created_at', 'updated_at')
        }),
        ('Soft-Delete & Recovery Lifecycle', {
            'fields': ('is_deleted', 'deleted_at', 'deleted_by', 'deletion_reason')
        }),
    )

    @admin.display(description='Status')
    def status_badge(self, obj):
        color = obj.status_color
        return format_html(
            '<span style="background-color: {}; color: #ffffff; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.action(description="Mark selected items as Claimed / Reunited")
    def mark_as_claimed_action(self, request, queryset):
        count = queryset.update(
            status=Item.STATUS_CLAIMED,
            is_verified_returned=True,
            resolved_at=timezone.now()
        )
        self.message_user(request, f"{count} item(s) marked as Claimed / Reunited.")

    @admin.action(description="Mark selected items as Lost")
    def mark_as_lost_action(self, request, queryset):
        count = queryset.update(
            status=Item.STATUS_LOST,
            is_verified_returned=False,
            resolved_at=None
        )
        self.message_user(request, f"{count} item(s) marked as Lost.")

    @admin.action(description="Mark selected items as Found")
    def mark_as_found_action(self, request, queryset):
        count = queryset.update(
            status=Item.STATUS_FOUND,
            is_verified_returned=False,
            resolved_at=None
        )
        self.message_user(request, f"{count} item(s) marked as Found.")

    @admin.action(description="Soft delete selected items")
    def soft_delete_action(self, request, queryset):
        count = queryset.update(
            is_deleted=True,
            deleted_at=timezone.now(),
            deleted_by=request.user,
            deletion_reason="Django Admin bulk soft-delete"
        )
        self.message_user(request, f"{count} item(s) soft-deleted.")

    @admin.action(description="Restore selected items")
    def restore_action(self, request, queryset):
        count = queryset.update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None,
            deletion_reason=None
        )
        self.message_user(request, f"{count} item(s) restored.")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'actor', 'action_type', 'target_repr', 'reason', 'ip_address']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['target_repr', 'reason', 'actor__username', 'ip_address']
    readonly_fields = ['timestamp', 'actor', 'action_type', 'target_model', 'target_id', 'target_repr', 'reason', 'details', 'ip_address']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'data_type', 'category', 'updated_at', 'last_modified_by']
    list_filter = ['category', 'data_type']
    search_fields = ['key', 'value', 'description']


@admin.register(SecurityAlert)
class SecurityAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'is_resolved', 'created_at', 'resolved_at', 'resolved_by']
    list_filter = ['severity', 'is_resolved', 'created_at']
    search_fields = ['title', 'message', 'resolution_note']
