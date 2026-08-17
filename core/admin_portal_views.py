import csv
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from .models import Item, AuditLog, SystemSetting, SecurityAlert

def admin_required(view_func):
    """
    Decorator enforcing strict administrator / operations governance access.
    Non-staff and anonymous requests are blocked.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in with administrator credentials.")
            return redirect(f"{reverse('login')}?next={request.path}")
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, "Access restricted to system administrators and operations staff.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def get_client_ip(request):
    """Utility to extract client IP address for audited logs."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# ==============================================================================
# 1. Overview / Dashboard
# ==============================================================================
@admin_required
def admin_dashboard_view(request):
    """
    Central governance dashboard displaying security summaries,
    platform health metrics, active alerts, and recent audit timelines.
    """
    # User governance metrics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    disabled_users = User.objects.filter(is_active=False).count()
    staff_count = User.objects.filter(is_staff=True).count()
    admin_count = User.objects.filter(is_superuser=True).count()

    # Data lifecycle metrics
    total_items = Item.objects.count()
    active_items = Item.objects.filter(is_deleted=False).count()
    soft_deleted_items = Item.objects.filter(is_deleted=True).count()
    lost_items = Item.objects.filter(is_deleted=False, status=Item.STATUS_LOST).count()
    found_items = Item.objects.filter(is_deleted=False, status=Item.STATUS_FOUND).count()
    claimed_items = Item.objects.filter(is_deleted=False, status=Item.STATUS_CLAIMED).count()

    # Security & Audit data
    open_alerts = SecurityAlert.objects.filter(is_resolved=False)[:5]
    recent_audits = AuditLog.objects.select_related('actor')[:8]

    # Database connectivity check
    from django.db import connection
    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        db_ok = False

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'disabled_users': disabled_users,
        'staff_count': staff_count,
        'admin_count': admin_count,
        'total_items': total_items,
        'active_items': active_items,
        'soft_deleted_items': soft_deleted_items,
        'lost_items': lost_items,
        'found_items': found_items,
        'claimed_items': claimed_items,
        'open_alerts': open_alerts,
        'recent_audits': recent_audits,
        'db_ok': db_ok,
        'is_s3_enabled': getattr(settings, 'USE_S3', False),
    }
    return render(request, 'admin_portal/dashboard.html', context)


# ==============================================================================
# 2. User Governance & Management
# ==============================================================================
@admin_required
def admin_users_view(request):
    """
    Search, filter, and inspect user accounts across the institution.
    """
    users_qs = User.objects.all().order_by('-date_joined')

    # Search
    q = request.GET.get('q', '').strip()
    if q:
        users_qs = users_qs.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    # Role filter
    role = request.GET.get('role', '')
    if role == 'superuser':
        users_qs = users_qs.filter(is_superuser=True)
    elif role == 'staff':
        users_qs = users_qs.filter(is_staff=True, is_superuser=False)
    elif role == 'student':
        users_qs = users_qs.filter(is_staff=False, is_superuser=False)

    # Status filter
    status = request.GET.get('status', '')
    if status == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status == 'inactive':
        users_qs = users_qs.filter(is_active=False)

    paginator = Paginator(users_qs, 15)
    page = request.GET.get('page', 1)
    users = paginator.get_page(page)

    context = {
        'users': users,
        'query_q': q,
        'selected_role': role,
        'selected_status': status,
        'total_count': User.objects.count(),
        'active_count': User.objects.filter(is_active=True).count(),
        'inactive_count': User.objects.filter(is_active=False).count(),
        'staff_count': User.objects.filter(is_staff=True).count(),
    }
    return render(request, 'admin_portal/users.html', context)


@admin_required
def admin_user_detail_view(request, user_id):
    """
    Detailed profile for governance: permissions, reported items,
    status toggle, role elevation, password reset, and audit timeline.
    """
    target_user = get_object_or_404(User, pk=user_id)
    user_items = Item.objects.filter(user=target_user).order_by('-created_at')
    user_audits = AuditLog.objects.filter(
        Q(actor=target_user) | Q(target_model='User', target_id=str(target_user.id))
    ).order_by('-timestamp')[:10]

    context = {
        'target_user': target_user,
        'user_items': user_items,
        'user_audits': user_audits,
    }
    return render(request, 'admin_portal/user_detail.html', context)


@admin_required
def admin_user_toggle_status_view(request, user_id):
    """
    Activate or deactivate a user account with mandatory reason capture.
    """
    target_user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Prevent self-deactivation of logged in superuser
        if target_user == request.user:
            messages.error(request, "Security protection: You cannot disable your own administrator account.")
            return redirect('admin_user_detail', user_id=target_user.id)

        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, "A mandatory reason is required for account status changes.")
            return redirect('admin_user_detail', user_id=target_user.id)

        new_status = not target_user.is_active
        target_user.is_active = new_status
        target_user.save()

        action_type = AuditLog.ACTION_USER_ACTIVATED if new_status else AuditLog.ACTION_USER_DEACTIVATED
        AuditLog.log_event(
            actor=request.user,
            action_type=action_type,
            target=target_user,
            target_repr=f"User: {target_user.username}",
            reason=reason,
            details={'is_active': new_status, 'changed_by': request.user.username},
            ip_address=get_client_ip(request)
        )

        status_text = "activated" if new_status else "disabled"
        messages.success(request, f"Account for '{target_user.username}' has been successfully {status_text}.")

    return redirect('admin_user_detail', user_id=target_user.id)


@admin_required
def admin_user_change_role_view(request, user_id):
    """
    Promote or demote user roles (Student, Staff Moderator, Superuser) with audit trail.
    """
    target_user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        if target_user == request.user and not request.user.is_superuser:
            messages.error(request, "Permission error: You cannot modify your own administrative role.")
            return redirect('admin_user_detail', user_id=target_user.id)

        new_role = request.POST.get('role', '')
        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, "A mandatory justification is required for role changes.")
            return redirect('admin_user_detail', user_id=target_user.id)

        old_role = "Administrator" if target_user.is_superuser else ("Staff Moderator" if target_user.is_staff else "Student")

        if new_role == 'superuser':
            target_user.is_superuser = True
            target_user.is_staff = True
        elif new_role == 'staff':
            target_user.is_superuser = False
            target_user.is_staff = True
        elif new_role == 'student':
            target_user.is_superuser = False
            target_user.is_staff = False
        target_user.save()

        action = AuditLog.ACTION_ROLE_PROMOTED if new_role in ('staff', 'superuser') else AuditLog.ACTION_ROLE_DEMOTED
        AuditLog.log_event(
            actor=request.user,
            action_type=action,
            target=target_user,
            target_repr=f"User: {target_user.username}",
            reason=reason,
            details={'old_role': old_role, 'new_role': new_role},
            ip_address=get_client_ip(request)
        )

        messages.success(request, f"Role for '{target_user.username}' updated from {old_role} to {new_role.capitalize()}.")

    return redirect('admin_user_detail', user_id=target_user.id)


@admin_required
def admin_user_reset_password_view(request, user_id):
    """
    Triggers administrative password reset with temporary credentials and audit record.
    """
    target_user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        reason = request.POST.get('reason', '').strip()

        if not new_password or len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect('admin_user_detail', user_id=target_user.id)
        if not reason:
            messages.error(request, "A justification reason is required for resetting user passwords.")
            return redirect('admin_user_detail', user_id=target_user.id)

        target_user.set_password(new_password)
        target_user.save()

        AuditLog.log_event(
            actor=request.user,
            action_type=AuditLog.ACTION_PASSWORD_RESET,
            target=target_user,
            target_repr=f"User: {target_user.username}",
            reason=reason,
            details={'reset_by': request.user.username},
            ip_address=get_client_ip(request)
        )

        messages.success(request, f"Password for '{target_user.username}' successfully reset.")

    return redirect('admin_user_detail', user_id=target_user.id)


# ==============================================================================
# 3. Roles & Permissions Management
# ==============================================================================
@admin_required
def admin_roles_view(request):
    """
    Inspect the effective permissions matrix and role bundles.
    """
    roles_summary = [
        {
            'name': 'System Administrator',
            'code': 'superuser',
            'badge': 'bg-dark text-white',
            'count': User.objects.filter(is_superuser=True).count(),
            'description': 'Full governance, security configuration, data recovery, and immutable audit access.',
            'capabilities': [
                'Full User & Staff Account Management',
                'Hard-Delete & Data Restoration Approvals',
                'System Settings & Operational Policy Controls',
                'Security Alert Triage & Incident Resolution',
                'Immutable Audit Log & CSV Compliance Exports'
            ]
        },
        {
            'name': 'Staff Moderator',
            'code': 'staff',
            'badge': 'bg-primary-subtle text-primary border border-primary-subtle',
            'count': User.objects.filter(is_staff=True, is_superuser=False).count(),
            'description': 'Campus staff responsible for front-line verification, item resolution, and moderation.',
            'capabilities': [
                'Browse & Search Moderation Catalog',
                'Mark Any Item as Claimed / Reunited',
                'Edit or Soft-Delete Inappropriate Listings',
                'Review Submissions & Contact Details'
            ]
        },
        {
            'name': 'Student / General User',
            'code': 'student',
            'badge': 'bg-light text-secondary border',
            'count': User.objects.filter(is_staff=False, is_superuser=False).count(),
            'description': 'Standard campus community members reporting or recovering lost belongings.',
            'capabilities': [
                'Report Lost and Found Items',
                'Upload Item Photos (Stored in Amazon S3)',
                'Manage & Edit Own Listings',
                'Print Campus Physical Notice Flyers'
            ]
        }
    ]

    recent_role_audits = AuditLog.objects.filter(
        action_type__in=[AuditLog.ACTION_ROLE_PROMOTED, AuditLog.ACTION_ROLE_DEMOTED]
    ).select_related('actor')[:6]

    context = {
        'roles_summary': roles_summary,
        'recent_role_audits': recent_role_audits,
    }
    return render(request, 'admin_portal/roles.html', context)


# ==============================================================================
# 4. Audit Log Viewer & CSV Export
# ==============================================================================
@admin_required
def admin_audit_logs_view(request):
    """
    Filterable immutable audit trail with search, date filters, and metadata inspection.
    """
    logs_qs = AuditLog.objects.select_related('actor').all().order_by('-timestamp')

    # Action type filter
    action_type = request.GET.get('action', '')
    if action_type:
        logs_qs = logs_qs.filter(action_type=action_type)

    # Actor search
    actor_q = request.GET.get('actor', '').strip()
    if actor_q:
        logs_qs = logs_qs.filter(actor__username__icontains=actor_q)

    # Target search
    q = request.GET.get('q', '').strip()
    if q:
        logs_qs = logs_qs.filter(
            Q(target_repr__icontains=q) |
            Q(reason__icontains=q) |
            Q(target_model__icontains=q)
        )

    paginator = Paginator(logs_qs, 20)
    page = request.GET.get('page', 1)
    logs = paginator.get_page(page)

    context = {
        'logs': logs,
        'action_choices': AuditLog.ACTION_CHOICES,
        'selected_action': action_type,
        'actor_q': actor_q,
        'query_q': q,
        'total_logs': logs_qs.count(),
    }
    return render(request, 'admin_portal/audit_logs.html', context)


@admin_required
def admin_audit_export_csv_view(request):
    """
    Exports filtered audit logs into CSV format for administrative compliance and reporting.
    """
    response = HttpResponse(content_type='text/csv')
    timestamp_str = timezone.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="campusfind_audit_report_{timestamp_str}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Log ID', 'Timestamp (UTC)', 'Actor Username', 'Action Type', 'Target Model', 'Target ID', 'Target Representation', 'Reason', 'IP Address'])

    logs = AuditLog.objects.select_related('actor').all().order_by('-timestamp')[:500]
    for l in logs:
        writer.writerow([
            l.id,
            l.timestamp.isoformat(),
            l.actor.username if l.actor else 'System',
            l.get_action_type_display(),
            l.target_model,
            l.target_id,
            l.target_repr,
            l.reason,
            l.ip_address or ''
        ])

    return response


# ==============================================================================
# 5. Controlled Data Operations (Soft-Delete & Hard-Delete Lifecycle)
# ==============================================================================
@admin_required
def admin_data_operations_view(request):
    """
    Data operations center:
    - Queue of soft-deleted items for restoration or permanent hard deletion.
    - Bulk operational controls (e.g. archiving older records).
    """
    deleted_items = Item.objects.filter(is_deleted=True).order_by('-deleted_at')
    active_count = Item.objects.filter(is_deleted=False).count()
    soft_deleted_count = deleted_items.count()

    context = {
        'deleted_items': deleted_items,
        'active_count': active_count,
        'soft_deleted_count': soft_deleted_count,
    }
    return render(request, 'admin_portal/data_operations.html', context)


@admin_required
def admin_item_restore_view(request, pk):
    """
    Restores a soft-deleted item back to active campus directory.
    """
    item = get_object_or_404(Item, pk=pk, is_deleted=True)

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, "A mandatory reason is required to restore an item.")
            return redirect('admin_data_operations')

        item.restore(user=request.user, reason=reason)

        AuditLog.log_event(
            actor=request.user,
            action_type=AuditLog.ACTION_ITEM_RESTORED,
            target=item,
            target_repr=item.title,
            reason=reason,
            details={'restored_by': request.user.username},
            ip_address=get_client_ip(request)
        )

        messages.success(request, f"Item '{item.title}' has been successfully restored to the public catalog.")

    return redirect('admin_data_operations')


@admin_required
def admin_item_hard_delete_view(request, pk):
    """
    Permanently deletes a record from the database with 2-step confirmation and mandatory reason capture.
    """
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        confirm_text = request.POST.get('confirm_text', '').strip()
        reason = request.POST.get('reason', '').strip()

        if confirm_text != 'DELETE':
            messages.error(request, "Verification failed: You must type 'DELETE' to confirm permanent hard delete.")
            return redirect('admin_data_operations')

        if not reason:
            messages.error(request, "A mandatory reason is required for permanent data destruction.")
            return redirect('admin_data_operations')

        title = item.title
        item_id = item.id

        AuditLog.log_event(
            actor=request.user,
            action_type=AuditLog.ACTION_ITEM_HARD_DELETED,
            target=None,
            target_repr=f"Permanent Delete: {title} (ID #{item_id})",
            reason=reason,
            details={'deleted_by': request.user.username, 'item_title': title, 'item_id': item_id},
            ip_address=get_client_ip(request)
        )

        item.delete()
        messages.success(request, f"Item '{title}' (ID #{item_id}) has been permanently purged from the database.")

    return redirect('admin_data_operations')


@admin_required
def admin_bulk_operation_view(request):
    """
    Handles audited bulk operations with preview and execution steps.
    """
    if request.method == 'POST':
        action = request.POST.get('bulk_action', '')
        reason = request.POST.get('reason', '').strip()

        if not reason:
            messages.error(request, "A mandatory justification reason is required for bulk actions.")
            return redirect('admin_data_operations')

        if action == 'archive_claimed':
            count = Item.objects.filter(is_deleted=False, status=Item.STATUS_CLAIMED).count()
            Item.objects.filter(is_deleted=False, status=Item.STATUS_CLAIMED).update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=request.user,
                deletion_reason=f"Bulk archive claimed items: {reason}"
            )
            AuditLog.log_event(
                actor=request.user,
                action_type=AuditLog.ACTION_BULK_OPERATION,
                target_repr="Bulk Archive Claimed Items",
                reason=reason,
                details={'action': action, 'records_affected': count},
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Successfully archived {count} claimed item(s).")

        elif action == 'restore_all':
            count = Item.objects.filter(is_deleted=True).count()
            Item.objects.filter(is_deleted=True).update(
                is_deleted=False,
                deleted_at=None,
                deleted_by=None,
                deletion_reason=None
            )
            AuditLog.log_event(
                actor=request.user,
                action_type=AuditLog.ACTION_BULK_OPERATION,
                target_repr="Bulk Restore All Soft-Deleted",
                reason=reason,
                details={'action': action, 'records_affected': count},
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Successfully restored {count} item(s).")

    return redirect('admin_data_operations')


# ==============================================================================
# 6. Scoped System Settings
# ==============================================================================
@admin_required
def admin_system_settings_view(request):
    """
    Manage non-code operational settings (broadcast alerts, upload limits, registration mode).
    """
    # Ensure default settings exist
    default_settings = [
        ('CAMPUS_NAME', 'Main Campus University', 'Institutional Name displayed across platform', 'str', 'General'),
        ('ALLOW_PUBLIC_REGISTRATION', 'True', 'Allow students to self-register accounts', 'bool', 'Access'),
        ('MAX_UPLOAD_MB', '5', 'Maximum image upload size in Megabytes', 'int', 'Storage'),
        ('CAMPUS_ALERT_BANNER_ACTIVE', 'False', 'Display sitewide alert banner at the top of all pages', 'bool', 'Alerts'),
        ('CAMPUS_ALERT_BANNER_TEXT', 'Notice: Campus Lost & Found Security Desk is open Mon-Fri 8am-5pm at SUB 102.', 'Message text for sitewide broadcast banner', 'text', 'Alerts'),
        ('AUTO_ARCHIVE_DAYS', '90', 'Number of days before inactive resolved posts are archived', 'int', 'Data Retention'),
    ]

    for key, val, desc, dtype, cat in default_settings:
        SystemSetting.objects.get_or_create(
            key=key,
            defaults={'value': val, 'description': desc, 'data_type': dtype, 'category': cat}
        )

    settings_list = SystemSetting.objects.all().order_by('category', 'key')

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, "A reason is required to update system settings.")
            return redirect('admin_system_settings')

        updated_count = 0
        for setting in settings_list:
            if setting.data_type == SystemSetting.TYPE_BOOL:
                new_val = 'True' if request.POST.get(setting.key) == 'on' else 'False'
            else:
                new_val = request.POST.get(setting.key, setting.value).strip()

            if new_val != setting.value:
                old_val = setting.value
                setting.value = new_val
                setting.last_modified_by = request.user
                setting.save()
                updated_count += 1

                AuditLog.log_event(
                    actor=request.user,
                    action_type=AuditLog.ACTION_SETTING_CHANGED,
                    target=setting,
                    target_repr=f"Setting: {setting.key}",
                    reason=reason,
                    details={'key': setting.key, 'old_val': old_val, 'new_val': new_val},
                    ip_address=get_client_ip(request)
                )

        messages.success(request, f"Successfully updated {updated_count} system setting(s).")
        return redirect('admin_system_settings')

    context = {
        'settings_list': settings_list,
    }
    return render(request, 'admin_portal/system_settings.html', context)


# ==============================================================================
# 7. Security Alerts & Anomaly Oversight
# ==============================================================================
@admin_required
def admin_security_alerts_view(request):
    """
    Security alert triage center.
    """
    alerts = SecurityAlert.objects.all().order_by('is_resolved', '-created_at')

    # Create demo alert if empty
    if not alerts.exists():
        SecurityAlert.create_alert(
            title="S3 Cloud Storage Policy Active",
            message="Amazon S3 media storage policy verified. All image uploads are directed to AWS S3 bucket.",
            severity=SecurityAlert.SEV_INFO
        )
        alerts = SecurityAlert.objects.all()

    context = {
        'alerts': alerts,
        'open_count': SecurityAlert.objects.filter(is_resolved=False).count(),
    }
    return render(request, 'admin_portal/security_alerts.html', context)


@admin_required
def admin_security_alert_resolve_view(request, pk):
    """
    Marks a security alert resolved with notes.
    """
    alert = get_object_or_404(SecurityAlert, pk=pk)

    if request.method == 'POST':
        note = request.POST.get('resolution_note', '').strip()
        alert.resolve(user=request.user, note=note)
        messages.success(request, f"Alert '{alert.title}' has been resolved.")

    return redirect('admin_security_alerts')
