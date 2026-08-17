from django.urls import path
from . import views
from . import admin_portal_views

urlpatterns = [
    # Public & Student Portal
    path('', views.home_view, name='home'),
    path('items/', views.item_list_view, name='item_list'),
    path('items/new/', views.item_create_view, name='item_create'),
    path('items/<int:pk>/', views.item_detail_view, name='item_detail'),
    path('items/<int:pk>/edit/', views.item_update_view, name='item_update'),
    path('items/<int:pk>/delete/', views.item_delete_view, name='item_delete'),
    path('items/<int:pk>/toggle-status/', views.item_toggle_status_view, name='item_toggle_status'),
    path('items/<int:pk>/print/', views.print_notice_view, name='print_notice'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    
    # Campus Moderator Hub (Front-line verification)
    path('moderator/', views.moderator_dashboard_view, name='moderator_dashboard'),
    
    # Dedicated Admin Operations Portal (System Governance & Security Rebuild)
    path('ops/', admin_portal_views.admin_dashboard_view, name='admin_dashboard'),
    path('ops/users/', admin_portal_views.admin_users_view, name='admin_users'),
    path('ops/users/<int:user_id>/', admin_portal_views.admin_user_detail_view, name='admin_user_detail'),
    path('ops/users/<int:user_id>/toggle-status/', admin_portal_views.admin_user_toggle_status_view, name='admin_user_toggle_status'),
    path('ops/users/<int:user_id>/change-role/', admin_portal_views.admin_user_change_role_view, name='admin_user_change_role'),
    path('ops/users/<int:user_id>/reset-password/', admin_portal_views.admin_user_reset_password_view, name='admin_user_reset_password'),
    path('ops/roles/', admin_portal_views.admin_roles_view, name='admin_roles'),
    path('ops/audit-logs/', admin_portal_views.admin_audit_logs_view, name='admin_audit_logs'),
    path('ops/audit-logs/export-csv/', admin_portal_views.admin_audit_export_csv_view, name='admin_audit_export_csv'),
    path('ops/data-operations/', admin_portal_views.admin_data_operations_view, name='admin_data_operations'),
    path('ops/data-operations/restore/<int:pk>/', admin_portal_views.admin_item_restore_view, name='admin_item_restore'),
    path('ops/data-operations/hard-delete/<int:pk>/', admin_portal_views.admin_item_hard_delete_view, name='admin_item_hard_delete'),
    path('ops/data-operations/bulk/', admin_portal_views.admin_bulk_operation_view, name='admin_bulk_operation'),
    path('ops/settings/', admin_portal_views.admin_system_settings_view, name='admin_system_settings'),
    path('ops/security/', admin_portal_views.admin_security_alerts_view, name='admin_security_alerts'),
    path('ops/security/resolve/<int:pk>/', admin_portal_views.admin_security_alert_resolve_view, name='admin_security_alert_resolve'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # AWS Cloud Telemetry
    path('health/', views.health_check_view, name='health_check'),
]
