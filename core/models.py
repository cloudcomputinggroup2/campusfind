from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import json

class Item(models.Model):
    """
    Core Item model representing Lost and Found items posted by campus users.
    Maps directly to the Items table specified in the CampusFind Capstone specification.
    Includes soft-delete support for administrative data recovery and auditing.
    """
    
    # Status Choices
    STATUS_LOST = 'LOST'
    STATUS_FOUND = 'FOUND'
    STATUS_CLAIMED = 'CLAIMED'
    
    STATUS_CHOICES = [
        (STATUS_LOST, 'Lost Item'),
        (STATUS_FOUND, 'Found Item'),
        (STATUS_CLAIMED, 'Claimed / Reunited'),
    ]

    # Category Choices
    CAT_ELECTRONICS = 'ELECTRONICS'
    CAT_CARDS_ID = 'CARDS_ID'
    CAT_KEYS = 'KEYS'
    CAT_BAGS_WALLETS = 'BAGS_WALLETS'
    CAT_BOOKS_DOCS = 'BOOKS_DOCS'
    CAT_CLOTHING = 'CLOTHING'
    CAT_ACCESSORIES = 'ACCESSORIES'
    CAT_SPORTS_BOTTLES = 'SPORTS_BOTTLES'
    CAT_OTHER = 'OTHER'

    CATEGORY_CHOICES = [
        (CAT_ELECTRONICS, 'Electronics & Gadgets (Phones, Laptops, Earbuds, Chargers)'),
        (CAT_CARDS_ID, 'Student IDs, Bank Cards & Badges'),
        (CAT_KEYS, 'Keys & Keychains'),
        (CAT_BAGS_WALLETS, 'Bags, Backpacks & Wallets'),
        (CAT_BOOKS_DOCS, 'Books, Notebooks & Documents'),
        (CAT_CLOTHING, 'Clothing, Jackets & Hats'),
        (CAT_ACCESSORIES, 'Watches, Glasses & Jewelry'),
        (CAT_SPORTS_BOTTLES, 'Water Bottles & Sports Equipment'),
        (CAT_OTHER, 'Other Miscellaneous Items'),
    ]

    # Campus Preset Locations
    LOCATION_PRESETS = [
        "Central Library",
        "Science Complex / Block A-D",
        "Student Union Building (SUB / SRC)",
        "Campus Cafeteria & Dining Hall",
        "Sports Complex & Gymnasium",
        "Engineering Lecture Theatres (LT 1-4)",
        "Main Auditorium",
        "Hostel & Student Residence Halls",
        "Campus Shuttle Station / Main Gate",
        "Computer Labs / IT Center",
        "Administrative Building",
        "Other / Outdoor Campus Green",
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The campus user who reported this item"
    )
    title = models.CharField(
        max_length=200,
        help_text="Clear headline for the item (e.g., 'Blue Dell Laptop Bag', 'Student ID Card')"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=CAT_OTHER
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_LOST,
        db_index=True
    )
    location = models.CharField(
        max_length=200,
        help_text="Campus area, building, room number, or landmark where it was lost or found"
    )
    date_event = models.DateField(
        default=timezone.now,
        verbose_name="Date Lost/Found",
        help_text="Approximate date when the item was lost or found"
    )
    description = models.TextField(
        help_text="Detailed description including brand, color, distinguishing marks, stickers, or contents"
    )
    contact = models.CharField(
        max_length=255,
        help_text="Contact email, phone number, WhatsApp, or designated campus drop-off office"
    )
    image = models.ImageField(
        upload_to='item_images/%Y/%m/',
        blank=True,
        null=True,
        help_text="Photo of the item (stored securely on Amazon S3 in cloud deployment)"
    )
    
    # Verification & Resolution tracking
    is_verified_returned = models.BooleanField(
        default=False,
        help_text="Designates whether the item has been successfully returned to its rightful owner"
    )
    resolved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Timestamp when the item was marked as claimed/reunited"
    )

    # Soft-delete Lifecycle Tracking (Admin Governance)
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Soft-delete flag allowing recovery by administrators"
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Timestamp when the item was soft-deleted"
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='deleted_items',
        help_text="The user or administrator who deleted this item"
    )
    deletion_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Audited justification provided when item was deleted"
    )
    
    # Metadata timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Campus Item'
        verbose_name_plural = 'Campus Items'

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} ({self.get_category_display()})"

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    def is_owner(self, user):
        """Check if a given user is the creator of this post or a staff member."""
        if not user or not user.is_authenticated:
            return False
        return self.user == user or user.is_staff or user.is_superuser

    def mark_as_claimed(self):
        """Mark this item as resolved/claimed."""
        self.status = self.STATUS_CLAIMED
        self.is_verified_returned = True
        self.resolved_at = timezone.now()
        self.save()

    def reopen(self, new_status=STATUS_LOST):
        """Reopen an item from claimed status."""
        self.status = new_status
        self.is_verified_returned = False
        self.resolved_at = None
        self.save()

    def soft_delete(self, user=None, reason=""):
        """Soft-deletes the item with audit tracking."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.deletion_reason = reason
        self.save()

    def restore(self, user=None, reason=""):
        """Restores a soft-deleted item."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.deletion_reason = None
        self.save()

    @property
    def status_badge_class(self):
        if self.status == self.STATUS_LOST:
            return 'badge-lost'
        elif self.status == self.STATUS_FOUND:
            return 'badge-found'
        elif self.status == self.STATUS_CLAIMED:
            return 'badge-claimed'
        return 'badge-secondary'

    @property
    def status_color(self):
        if self.status == self.STATUS_LOST:
            return '#be123c'  # Rose 700
        elif self.status == self.STATUS_FOUND:
            return '#0369a1'  # Sky 700
        elif self.status == self.STATUS_CLAIMED:
            return '#15803d'  # Emerald 700
        return '#64748b'

    @property
    def category_icon(self):
        mapping = {
            self.CAT_ELECTRONICS: 'bi-laptop',
            self.CAT_CARDS_ID: 'bi-person-badge',
            self.CAT_KEYS: 'bi-key-fill',
            self.CAT_BAGS_WALLETS: 'bi-backpack',
            self.CAT_BOOKS_DOCS: 'bi-book-half',
            self.CAT_CLOTHING: 'bi-tag',
            self.CAT_ACCESSORIES: 'bi-watch',
            self.CAT_SPORTS_BOTTLES: 'bi-cup-straw',
            self.CAT_OTHER: 'bi-box-seam',
        }
        return mapping.get(self.category, 'bi-box-seam')


class AuditLog(models.Model):
    """
    Immutable audit log model tracking all security, permission changes,
    account governance, and high-impact data operations.
    """
    ACTION_USER_CREATED = 'USER_CREATED'
    ACTION_USER_ACTIVATED = 'USER_ACTIVATED'
    ACTION_USER_DEACTIVATED = 'USER_DEACTIVATED'
    ACTION_ROLE_PROMOTED = 'ROLE_PROMOTED'
    ACTION_ROLE_DEMOTED = 'ROLE_DEMOTED'
    ACTION_PASSWORD_RESET = 'PASSWORD_RESET'
    ACTION_ITEM_SOFT_DELETED = 'ITEM_SOFT_DELETED'
    ACTION_ITEM_HARD_DELETED = 'ITEM_HARD_DELETED'
    ACTION_ITEM_RESTORED = 'ITEM_RESTORED'
    ACTION_SETTING_CHANGED = 'SETTING_CHANGED'
    ACTION_ALERT_RESOLVED = 'ALERT_RESOLVED'
    ACTION_BULK_OPERATION = 'BULK_OPERATION'
    ACTION_ADMIN_LOGIN = 'ADMIN_LOGIN'

    ACTION_CHOICES = [
        (ACTION_USER_CREATED, 'User Created'),
        (ACTION_USER_ACTIVATED, 'User Account Activated'),
        (ACTION_USER_DEACTIVATED, 'User Account Deactivated'),
        (ACTION_ROLE_PROMOTED, 'Role / Permission Promoted'),
        (ACTION_ROLE_DEMOTED, 'Role / Permission Demoted'),
        (ACTION_PASSWORD_RESET, 'Password Reset Triggered'),
        (ACTION_ITEM_SOFT_DELETED, 'Item Soft Deleted'),
        (ACTION_ITEM_HARD_DELETED, 'Item Permanently Deleted'),
        (ACTION_ITEM_RESTORED, 'Item Restored'),
        (ACTION_SETTING_CHANGED, 'System Setting Modified'),
        (ACTION_ALERT_RESOLVED, 'Security Alert Resolved'),
        (ACTION_BULK_OPERATION, 'Bulk Data Operation'),
        (ACTION_ADMIN_LOGIN, 'Admin Portal Sign In'),
    ]

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_audit_logs',
        help_text="The administrator or system user who triggered this action"
    )
    action_type = models.CharField(
        max_length=60,
        choices=ACTION_CHOICES,
        db_index=True
    )
    target_model = models.CharField(
        max_length=60,
        blank=True,
        help_text="Model affected (e.g., User, Item, SystemSetting)"
    )
    target_id = models.CharField(
        max_length=60,
        blank=True,
        help_text="ID of target object"
    )
    target_repr = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable title/name of the target object"
    )
    reason = models.TextField(
        blank=True,
        help_text="Mandatory justification captured for high-risk operations"
    )
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Contextual metadata, old vs new values diff"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Client IP address"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        actor_name = self.actor.username if self.actor else 'System'
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {actor_name} -> {self.get_action_type_display()} ({self.target_repr})"

    @classmethod
    def log_event(cls, actor, action_type, target=None, target_repr="", reason="", details=None, ip_address=None):
        """Helper to create an immutable audit record."""
        target_model = ""
        target_id = ""
        if target:
            target_model = target.__class__.__name__
            target_id = str(getattr(target, 'pk', ''))
            if not target_repr:
                target_repr = str(target)

        return cls.objects.create(
            actor=actor if (actor and actor.is_authenticated) else None,
            action_type=action_type,
            target_model=target_model,
            target_id=target_id,
            target_repr=target_repr,
            reason=reason or "Operational governance action",
            details=details or {},
            ip_address=ip_address
        )


class SystemSetting(models.Model):
    """
    Non-code operational configuration key-value storage.
    Enables administrators to adjust platform policies with versioned audit logging.
    """
    TYPE_BOOL = 'bool'
    TYPE_INT = 'int'
    TYPE_STR = 'str'
    TYPE_TEXT = 'text'

    TYPE_CHOICES = [
        (TYPE_BOOL, 'Boolean (True/False)'),
        (TYPE_INT, 'Integer Number'),
        (TYPE_STR, 'Short Text'),
        (TYPE_TEXT, 'Long Text / Notice'),
    ]

    key = models.CharField(max_length=60, unique=True, db_index=True)
    value = models.TextField(help_text="Current configuration value")
    description = models.CharField(max_length=255, help_text="Operational purpose of this setting")
    data_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_STR)
    category = models.CharField(max_length=50, default='General')
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_settings'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'key']
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'

    def __str__(self):
        return f"{self.key}: {self.value}"

    def get_typed_value(self):
        """Converts string storage into typed representation."""
        if self.data_type == self.TYPE_BOOL:
            return self.value.strip().lower() in ('true', '1', 'yes', 'on')
        elif self.data_type == self.TYPE_INT:
            try:
                return int(self.value)
            except ValueError:
                return 0
        return self.value

    @classmethod
    def get_val(cls, key, default=None):
        """Quick lookup for a system setting."""
        try:
            setting = cls.objects.get(key=key)
            return setting.get_typed_value()
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_val(cls, key, val, user=None, reason=""):
        """Sets a system setting with audit logging."""
        setting, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': str(val), 'description': key, 'last_modified_by': user}
        )
        old_val = setting.value
        setting.value = str(val)
        setting.last_modified_by = user
        setting.save()

        # Write audit log
        AuditLog.log_event(
            actor=user,
            action_type=AuditLog.ACTION_SETTING_CHANGED,
            target=setting,
            target_repr=f"Setting: {key}",
            reason=reason or f"Updated {key} setting",
            details={'old_value': old_val, 'new_value': str(val)}
        )
        return setting


class SecurityAlert(models.Model):
    """
    Tracks security incidents, anomalies, account lockouts, and compliance alerts.
    """
    SEV_INFO = 'INFO'
    SEV_WARNING = 'WARNING'
    SEV_CRITICAL = 'CRITICAL'

    SEV_CHOICES = [
        (SEV_INFO, 'Information'),
        (SEV_WARNING, 'Warning'),
        (SEV_CRITICAL, 'Critical Alert'),
    ]

    severity = models.CharField(max_length=20, choices=SEV_CHOICES, default=SEV_INFO)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False, db_index=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_resolved', '-created_at']
        verbose_name = 'Security Alert'
        verbose_name_plural = 'Security Alerts'

    def __str__(self):
        return f"[{self.severity}] {self.title} ({'Resolved' if self.is_resolved else 'Active'})"

    def resolve(self, user, note=""):
        """Marks this alert resolved with audit log."""
        self.is_resolved = True
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolution_note = note
        self.save()

        AuditLog.log_event(
            actor=user,
            action_type=AuditLog.ACTION_ALERT_RESOLVED,
            target=self,
            target_repr=f"Alert: {self.title}",
            reason=note or "Resolved security alert",
            details={'severity': self.severity, 'resolution_note': note}
        )

    @classmethod
    def create_alert(cls, title, message, severity=SEV_INFO):
        """Creates a security alert record."""
        return cls.objects.create(
            title=title,
            message=message,
            severity=severity
        )
