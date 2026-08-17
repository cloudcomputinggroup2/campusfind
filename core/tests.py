from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Item, AuditLog, SystemSetting, SecurityAlert
from .forms import ItemForm, UserRegistrationForm

class CampusFindModelTests(TestCase):
    """
    Test suite for Item model and user interactions.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@campus.edu',
            password='Password123!'
        )
        self.other_user = User.objects.create_user(
            username='otherstudent',
            email='other@campus.edu',
            password='Password123!'
        )
        self.admin_user = User.objects.create_superuser(
            username='testadmin',
            email='admin@campus.edu',
            password='Password123!'
        )
        self.item = Item.objects.create(
            user=self.user,
            title='Blue HP Laptop',
            category=Item.CAT_ELECTRONICS,
            status=Item.STATUS_LOST,
            location='Central Library',
            date_event=timezone.now().date(),
            description='Blue HP Pavilion with scratch on lid',
            contact='student@campus.edu'
        )

    def test_item_creation(self):
        """Verify item is created with correct defaults."""
        self.assertEqual(self.item.title, 'Blue HP Laptop')
        self.assertEqual(self.item.status, Item.STATUS_LOST)
        self.assertFalse(self.item.is_verified_returned)
        self.assertIn('Blue HP Laptop', str(self.item))

    def test_item_ownership_permission(self):
        """Verify only owner or staff have ownership permissions."""
        self.assertTrue(self.item.is_owner(self.user))
        self.assertTrue(self.item.is_owner(self.admin_user))
        self.assertFalse(self.item.is_owner(self.other_user))

    def test_item_claim_and_reopen(self):
        """Verify marking item claimed and reopening works properly."""
        self.item.mark_as_claimed()
        self.assertEqual(self.item.status, Item.STATUS_CLAIMED)
        self.assertTrue(self.item.is_verified_returned)
        self.assertIsNotNone(self.item.resolved_at)

        self.item.reopen(new_status=Item.STATUS_LOST)
        self.assertEqual(self.item.status, Item.STATUS_LOST)
        self.assertFalse(self.item.is_verified_returned)
        self.assertIsNone(self.item.resolved_at)

    def test_soft_delete_and_restore(self):
        """Verify soft deletion and restoration lifecycle."""
        self.item.soft_delete(user=self.admin_user, reason="Test deletion")
        self.assertTrue(self.item.is_deleted)
        self.assertIsNotNone(self.item.deleted_at)
        self.assertEqual(self.item.deleted_by, self.admin_user)

        self.item.restore(user=self.admin_user, reason="Test restore")
        self.assertFalse(self.item.is_deleted)
        self.assertIsNone(self.item.deleted_at)


class CampusFindViewsTests(TestCase):
    """
    Test suite for Views, CRUD endpoints, and search/filter queries.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student1',
            email='student1@campus.edu',
            password='Password123!'
        )
        self.user2 = User.objects.create_user(
            username='student2',
            email='student2@campus.edu',
            password='Password123!'
        )
        self.item_lost = Item.objects.create(
            user=self.user,
            title='Lost Student ID Card',
            category=Item.CAT_CARDS_ID,
            status=Item.STATUS_LOST,
            location='Cafeteria',
            description='Green campus ID card',
            contact='student1@campus.edu'
        )
        self.item_found = Item.objects.create(
            user=self.user,
            title='Found TI-84 Calculator',
            category=Item.CAT_ELECTRONICS,
            status=Item.STATUS_FOUND,
            location='Science Block Room 101',
            description='Black calculator',
            contact='student1@campus.edu'
        )

    def test_home_page_status_and_context(self):
        """Home page should return 200 and display recent items."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reunite with Your Belongings')
        self.assertContains(response, 'Lost Student ID Card')
        self.assertContains(response, 'Found TI-84 Calculator')

    def test_item_list_view_and_filtering(self):
        """Item list should support filtering by status and search terms."""
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lost Student ID Card')

        # Filter by status
        response_lost = self.client.get(reverse('item_list') + '?status=LOST')
        self.assertContains(response_lost, 'Lost Student ID Card')
        self.assertNotContains(response_lost, 'Found TI-84 Calculator')

        # Filter by search keyword
        response_search = self.client.get(reverse('item_list') + '?q=Calculator')
        self.assertContains(response_search, 'Found TI-84 Calculator')
        self.assertNotContains(response_search, 'Lost Student ID Card')

    def test_item_detail_view(self):
        """Item detail view should display item specifics."""
        response = self.client.get(reverse('item_detail', kwargs={'pk': self.item_lost.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lost Student ID Card')
        self.assertContains(response, 'Cafeteria')

    def test_item_create_view_requires_login(self):
        """Creating an item requires authentication."""
        # Unauthenticated request redirects to login
        response = self.client.get(reverse('item_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

        # Authenticated post succeeds
        self.client.login(username='student1', password='Password123!')
        post_data = {
            'title': 'New Found Keys',
            'category': Item.CAT_KEYS,
            'status': Item.STATUS_FOUND,
            'location': 'Library 1st floor',
            'date_event': timezone.now().date(),
            'description': 'Two brass keys on a ring',
            'contact': '+1 555 123 4567',
        }
        response_post = self.client.post(reverse('item_create'), post_data)
        self.assertEqual(response_post.status_code, 302)
        self.assertTrue(Item.objects.filter(title='New Found Keys').exists())

    def test_item_update_view_permission_check(self):
        """Only item owner can edit their post."""
        self.client.login(username='student2', password='Password123!')
        # Non-owner edit attempt should redirect
        response = self.client.get(reverse('item_update', kwargs={'pk': self.item_lost.pk}))
        self.assertEqual(response.status_code, 302)

        # Owner edit succeeds
        self.client.login(username='student1', password='Password123!')
        response_owner = self.client.get(reverse('item_update', kwargs={'pk': self.item_lost.pk}))
        self.assertEqual(response_owner.status_code, 200)

    def test_health_check_endpoint(self):
        """Cloud health check endpoint should return 200 OK and healthy JSON status."""
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'healthy')
        self.assertEqual(json_data['database'], 'ok')


class AdminPortalOperationsTests(TestCase):
    """
    Test suite specifically verifying the Admin Role & Governance Rebuild requirements.
    """
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin_boss',
            email='admin@campus.edu',
            password='AdminPassword123!'
        )
        self.student = User.objects.create_user(
            username='student_sam',
            email='sam@campus.edu',
            password='StudentPassword123!'
        )
        self.item = Item.objects.create(
            user=self.student,
            title='Lost Black Wallet',
            category=Item.CAT_BAGS_WALLETS,
            status=Item.STATUS_LOST,
            location='Library',
            description='Leather wallet',
            contact='sam@campus.edu'
        )

    def test_admin_portal_access_gate(self):
        """Unauthenticated and student users cannot access admin dashboard."""
        # Unauthenticated
        resp_anon = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp_anon.status_code, 302)

        # Student user
        self.client.login(username='student_sam', password='StudentPassword123!')
        resp_student = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp_student.status_code, 302)

        # Superadmin user
        self.client.login(username='admin_boss', password='AdminPassword123!')
        resp_admin = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp_admin.status_code, 200)
        self.assertContains(resp_admin, 'System Governance Dashboard')

    def test_user_governance_toggle_status_and_audit(self):
        """Admin can deactivate user account with mandatory reason and audit record."""
        self.client.login(username='admin_boss', password='AdminPassword123!')
        url = reverse('admin_user_toggle_status', kwargs={'user_id': self.student.id})
        
        post_data = {'reason': 'Account security lockout review'}
        resp = self.client.post(url, post_data)
        self.assertEqual(resp.status_code, 302)

        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)

        # AuditLog check
        self.assertTrue(AuditLog.objects.filter(
            action_type=AuditLog.ACTION_USER_DEACTIVATED,
            reason='Account security lockout review'
        ).exists())

    def test_admin_data_operations_restore_and_hard_delete(self):
        """Admin can soft-delete, restore, and permanently hard-delete records with audit logging."""
        self.client.login(username='admin_boss', password='AdminPassword123!')
        
        # Soft delete
        self.item.soft_delete(user=self.admin, reason="Initial soft delete")
        self.assertTrue(self.item.is_deleted)

        # Restore
        restore_url = reverse('admin_item_restore', kwargs={'pk': self.item.pk})
        self.client.post(restore_url, {'reason': 'Verified legitimate post'})
        self.item.refresh_from_db()
        self.assertFalse(self.item.is_deleted)

        # Hard delete
        hard_delete_url = reverse('admin_item_hard_delete', kwargs={'pk': self.item.pk})
        resp_hard = self.client.post(hard_delete_url, {'confirm_text': 'DELETE', 'reason': 'Permanent purge per request'})
        self.assertEqual(resp_hard.status_code, 302)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())
        self.assertTrue(AuditLog.objects.filter(action_type=AuditLog.ACTION_ITEM_HARD_DELETED).exists())

    def test_admin_audit_logs_csv_export(self):
        """Admin can download CSV report of all immutable audit logs."""
        self.client.login(username='admin_boss', password='AdminPassword123!')
        resp = self.client.get(reverse('admin_audit_export_csv'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')
        self.assertIn('campusfind_audit_report_', resp['Content-Disposition'])

    def test_system_settings_update_with_audit(self):
        """Admin can update operational settings with versioned audit logging."""
        self.client.login(username='admin_boss', password='AdminPassword123!')
        url = reverse('admin_system_settings')
        resp = self.client.post(url, {
            'CAMPUS_NAME': 'Engineering & Science University',
            'reason': 'Institutional rebranding update'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(SystemSetting.get_val('CAMPUS_NAME'), 'Engineering & Science University')
        self.assertTrue(AuditLog.objects.filter(action_type=AuditLog.ACTION_SETTING_CHANGED).exists())
