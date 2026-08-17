# 07 - Admin Role And Requirements (Rebuild Plan)

## Purpose
This document defines the responsibilities, authority boundaries, and minimum feature requirements for the new Admin interface that will be rebuilt from scratch.

This is an operations role, not a student role and not a moderator role.

## Role Definition
The Admin is responsible for system governance, platform integrity, and high-risk actions that affect security, permissions, and data lifecycle.

The Admin should not be used for routine moderation tasks that already belong to moderators.

## Primary Responsibilities
1. User and Staff Governance
- Create, disable, or reactivate staff accounts.
- Assign and revoke elevated roles and permissions.
- Enforce least-privilege access.

2. Security and Compliance
- Monitor suspicious activity and access anomalies.
- Review authentication and permission change logs.
- Trigger account lockout or forced password reset workflows.

3. Data Integrity and Recovery
- Handle irreversible operations (hard delete, data restore approvals).
- Verify backup status and recovery readiness.
- Approve high-impact bulk changes.

4. Platform Configuration
- Manage system-wide configuration flags and operational settings.
- Manage storage and media policy controls (retention, cleanup windows).
- Manage integration-level settings (if any external service is attached later).

5. Audit and Oversight
- Review activity timelines for critical actions.
- Export reports for governance and academic documentation.
- Maintain traceability of who changed what and when.

## What Admin Must Not Do
- Must not replace moderator workflows for daily item handling.
- Must not perform actions outside audited paths.
- Must not bypass approval controls for destructive operations.

## Required Admin Capabilities (MVP)
1. Authentication and Access Control
- Admin-only login gate.
- Role-based authorization checks per page and action.
- Session timeout and secure logout.

2. Dashboard
- Security summary: failed logins, locked users, recent role changes.
- Data summary: total users, total items, unresolved items, recent critical actions.
- Alert panel for anomalies and unresolved escalations.

3. User Management
- Search/filter users.
- Activate/deactivate account.
- Promote/demote staff role.
- Force password reset token trigger.

4. Permission Management
- View effective permissions per account.
- Assign/revoke permission bundles.
- Change history for permission updates.

5. Audit Log Viewer
- Filter by actor, action type, target object, date range.
- Immutable view for critical logs.
- CSV export for reporting.

6. Controlled Data Actions
- Bulk operations with preview and confirmation step.
- Soft-delete first, hard-delete only with second confirmation.
- Explicit reason capture for destructive actions.

7. System Settings (Scoped)
- Manage non-code operational settings only.
- Versioned change records (old value, new value, actor, timestamp).

## Security Requirements
1. Enforce CSRF protection and secure cookie/session settings.
2. Enforce server-side permission checks on every action.
3. Use explicit confirmation prompts for high-risk actions.
4. Log all critical events: auth, permission changes, destructive operations.
5. Block anonymous and non-admin access to all admin endpoints.

## UX Requirements
1. High-contrast, accessible color system (WCAG-aware).
2. Clear distinction between safe and destructive actions.
3. Keyboard-accessible controls and visible focus states.
4. Consistent layout and spacing across list, detail, and action pages.
5. Mobile-safe layout for quick oversight actions.

## Suggested Information Architecture
1. Overview
2. Users
3. Roles and Permissions
4. Audit Logs
5. Data Operations
6. System Settings
7. Security Alerts

## Success Criteria
The Admin rebuild is considered complete when:
1. All admin-only endpoints are protected and audited.
2. High-risk actions require explicit confirmation and reason capture.
3. Admin can manage users, roles, permissions, and logs without using legacy admin pages.
4. Moderator workflows remain independent and unchanged.
5. Accessibility and contrast checks pass on key screens.

## Implementation Notes
- Build the new Admin as dedicated application pages under a new route namespace.
- Keep moderator routes and templates untouched.
- Migrate capabilities in phases: read-only first, then controlled write actions.
