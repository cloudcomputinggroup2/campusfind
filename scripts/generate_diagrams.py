"""
Generate high-resolution architecture and system design diagrams for CampusFind DOCX deliverables.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('diagrams', exist_ok=True)

def generate_aws_architecture():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 75)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Outer VPC Box
    vpc_box = patches.FancyBboxPatch((3, 3), 114, 69, boxstyle="round,pad=1,rounding_size=2",
                                     edgecolor='#2563EB', facecolor='#F8FAFC', linewidth=2, linestyle='--')
    ax.add_patch(vpc_box)
    ax.text(6, 68.5, 'Amazon Web Services (AWS Free Tier VPC - Region: us-east-1)', fontsize=12, fontweight='bold', color='#1E3A8A')

    # 1. Client Layer
    client_box = patches.FancyBboxPatch((6, 32), 18, 18, boxstyle="round,pad=0.8,rounding_size=1.5",
                                        edgecolor='#0284C7', facecolor='#E0F2FE', linewidth=1.5)
    ax.add_patch(client_box)
    ax.text(15, 43, 'Student / Faculty\nWeb Browsers', ha='center', va='center', fontsize=10, fontweight='bold', color='#0369A1')
    ax.text(15, 36, '(Desktop, Tablet, Mobile)', ha='center', va='center', fontsize=8, color='#075985')

    # Arrow: Client -> EC2
    ax.annotate('', xy=(34, 41), xytext=(24, 41),
                arrowprops=dict(facecolor='#0284C7', edgecolor='#0284C7', width=2, headwidth=8))
    ax.text(29, 43.5, 'HTTPS :443\nHTTP :80', ha='center', va='center', fontsize=8, fontweight='bold', color='#0284C7')

    # 2. Public Subnet / EC2
    ec2_outer = patches.FancyBboxPatch((34, 18), 38, 46, boxstyle="round,pad=0.8,rounding_size=1.5",
                                       edgecolor='#EA580C', facecolor='#FFF7ED', linewidth=1.8)
    ax.add_patch(ec2_outer)
    ax.text(53, 61, 'Amazon EC2 Instance (t2.micro / Ubuntu 24.04)', ha='center', va='center', fontsize=10, fontweight='bold', color='#C2410C')
    ax.text(53, 58, 'Security Group: CampusFind-EC2-SG (Ports: 22, 80, 443)', ha='center', va='center', fontsize=7.5, color='#9A3412')

    # Inside EC2: Nginx Box
    nginx_box = patches.FancyBboxPatch((37, 43), 32, 11, boxstyle="round,pad=0.5,rounding_size=1",
                                       edgecolor='#16A34A', facecolor='#DCFCE7', linewidth=1.2)
    ax.add_patch(nginx_box)
    ax.text(53, 49.5, 'Nginx Reverse Proxy & Web Server', ha='center', va='center', fontsize=9, fontweight='bold', color='#166534')
    ax.text(53, 45.5, 'SSL Termination • Static Caching • Gzip', ha='center', va='center', fontsize=7.5, color='#15803D')

    # Inside EC2: Gunicorn + Django
    django_box = patches.FancyBboxPatch((37, 22), 32, 16, boxstyle="round,pad=0.5,rounding_size=1",
                                        edgecolor='#059669', facecolor='#D1FAE5', linewidth=1.2)
    ax.add_patch(django_box)
    ax.text(53, 34, 'Gunicorn WSGI + Django 5.0 App', ha='center', va='center', fontsize=9, fontweight='bold', color='#065F46')
    ax.text(53, 29, 'Systemd Service • Auth & CRUD Logic\nHealth Check Endpoint (/health/)', ha='center', va='center', fontsize=7.5, color='#047857')

    # Arrow: Nginx -> Django
    ax.annotate('', xy=(53, 38), xytext=(53, 43),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', width=1.5, headwidth=6))
    ax.text(58.5, 40.5, 'WSGI Port 8000', ha='center', va='center', fontsize=7, color='#166534')

    # 3. Private Subnet / RDS
    rds_box = patches.FancyBboxPatch((82, 38), 32, 26, boxstyle="round,pad=0.8,rounding_size=1.5",
                                     edgecolor='#4338CA', facecolor='#EEF2FF', linewidth=1.8)
    ax.add_patch(rds_box)
    ax.text(98, 60.5, 'Amazon RDS Managed DB', ha='center', va='center', fontsize=10, fontweight='bold', color='#3730A3')
    ax.text(98, 56.5, '(PostgreSQL 15 / MySQL 8.0)', ha='center', va='center', fontsize=8.5, color='#4338CA')
    ax.text(98, 49, 'Private Subnet Group\nSG: CampusFind-RDS-SG\n(Accepts Port 5432 ONLY from EC2-SG)', ha='center', va='center', fontsize=7.5, color='#312E81')
    ax.text(98, 41, 'Stores: Users, Items, Audit Logs', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1E1B4B')

    # Arrow: EC2 Django -> RDS
    ax.annotate('', xy=(82, 48), xytext=(69, 32),
                arrowprops=dict(facecolor='#4338CA', edgecolor='#4338CA', width=2, headwidth=7))
    ax.text(77, 39, 'Port 5432\nSQL Queries', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#4338CA')

    # 4. Amazon S3 Bucket
    s3_box = patches.FancyBboxPatch((82, 10), 32, 22, boxstyle="round,pad=0.8,rounding_size=1.5",
                                    edgecolor='#0284C7', facecolor='#F0F9FF', linewidth=1.8)
    ax.add_patch(s3_box)
    ax.text(98, 28, 'Amazon S3 Bucket', ha='center', va='center', fontsize=10, fontweight='bold', color='#0369A1')
    ax.text(98, 24, 'campusfind-item-images-capstone', ha='center', va='center', fontsize=8, color='#0284C7')
    ax.text(98, 17, 'Decoupled Media Object Storage\nItem Photos • Boto3 / django-storages\nZero disk storage load on EC2', ha='center', va='center', fontsize=7.5, color='#075985')

    # Arrow: EC2 Django -> S3
    ax.annotate('', xy=(82, 19), xytext=(69, 25),
                arrowprops=dict(facecolor='#0284C7', edgecolor='#0284C7', width=2, headwidth=7))
    ax.text(76, 21, 'IAM / Boto3\nMedia Upload', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0284C7')

    # 5. Security & Governance & CloudWatch Badges
    iam_badge = patches.FancyBboxPatch((6, 7), 24, 18, boxstyle="round,pad=0.6,rounding_size=1",
                                       edgecolor='#7C3AED', facecolor='#F5F3FF', linewidth=1.3)
    ax.add_patch(iam_badge)
    ax.text(18, 21.5, 'AWS IAM Governance', ha='center', va='center', fontsize=9, fontweight='bold', color='#6D28D9')
    ax.text(18, 14.5, 'Least-Privilege Policy\ns3:PutObject, s3:GetObject\nZero hardcoded keys (.env)', ha='center', va='center', fontsize=7.5, color='#5B21B6')

    cw_badge = patches.FancyBboxPatch((37, 5), 32, 10, boxstyle="round,pad=0.5,rounding_size=1",
                                      edgecolor='#D97706', facecolor='#FEF3C7', linewidth=1.3)
    ax.add_patch(cw_badge)
    ax.text(53, 11.5, 'Amazon CloudWatch Telemetry', ha='center', va='center', fontsize=9, fontweight='bold', color='#B45309')
    ax.text(53, 7.5, 'EC2 CPU & Network Alarms • Health Endpoint Monitoring', ha='center', va='center', fontsize=7.5, color='#92400E')

    plt.tight_layout()
    plt.savefig('diagrams/aws_architecture.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved diagrams/aws_architecture.png")


def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(11, 8), dpi=300)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 85)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # System boundary
    sys_box = patches.FancyBboxPatch((28, 4), 54, 76, boxstyle="round,pad=1,rounding_size=2",
                                     edgecolor='#2563EB', facecolor='#F8FAFC', linewidth=2)
    ax.add_patch(sys_box)
    ax.text(55, 76, 'CampusFind System Boundary', ha='center', va='center', fontsize=12, fontweight='bold', color='#1E3A8A')

    # Actors
    # 1. Student / Campus User (Left)
    ax.scatter(12, 50, s=400, color='#0284C7', zorder=4)
    ax.text(12, 43, 'Student / Campus User\n(Authenticated)', ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # 2. Campus Moderator (Right Top)
    ax.scatter(96, 60, s=400, color='#16A34A', zorder=4)
    ax.text(96, 53, 'Campus Staff /\nModerator', ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # 3. System Administrator (Right Bottom)
    ax.scatter(96, 22, s=400, color='#DC2626', zorder=4)
    ax.text(96, 15, 'System Administrator\n(Operations / Governance)', ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')

    # Use Cases (Ovals in center)
    use_cases = [
        (55, 68, 'Register & Authenticate Account', '#DBEAFE', '#1D4ED8'),
        (55, 59, 'Search & Multi-Filter Catalog', '#DBEAFE', '#1D4ED8'),
        (55, 50, 'Post Lost / Found Item & S3 Upload', '#DBEAFE', '#1D4ED8'),
        (55, 41, 'Generate Printable Notice Flyer', '#DBEAFE', '#1D4ED8'),
        (55, 32, 'Manage Own Posts / Mark Claimed', '#DBEAFE', '#1D4ED8'),
        (55, 23, 'Review Listings & Frontline Triage', '#DCFCE7', '#15803D'),
        (55, 14, 'User Governance & Data Recovery (/ops/)', '#FEE2E2', '#B91C1C'),
    ]

    for (x, y, text, bg, border) in use_cases:
        oval = patches.FancyBboxPatch((x-22, y-3), 44, 6, boxstyle="round,pad=0.3,rounding_size=3",
                                     edgecolor=border, facecolor=bg, linewidth=1.5)
        ax.add_patch(oval)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

    # Association Lines - Student
    for target_y in [68, 59, 50, 41, 32]:
        ax.plot([14, 33], [50, target_y], color='#0284C7', linewidth=1.3, linestyle='-')

    # Association Lines - Moderator
    for target_y in [68, 59, 23]:
        ax.plot([94, 77], [60, target_y], color='#16A34A', linewidth=1.3, linestyle='-')

    # Association Lines - Admin
    for target_y in [68, 59, 14]:
        ax.plot([94, 77], [22, target_y], color='#DC2626', linewidth=1.3, linestyle='-')

    plt.tight_layout()
    plt.savefig('diagrams/use_case_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved diagrams/use_case_diagram.png")


def generate_database_erd():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 80)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(60, 76, 'CampusFind Relational Database Schema (3NF Normalization)', ha='center', va='center', fontsize=13, fontweight='bold', color='#1E3A8A')

    # Entity 1: auth_user
    user_box = patches.FancyBboxPatch((6, 38), 32, 32, boxstyle="round,pad=0.5,rounding_size=1",
                                      edgecolor='#2563EB', facecolor='#EFF6FF', linewidth=1.8)
    ax.add_patch(user_box)
    ax.text(22, 67, 'auth_user (Table)', ha='center', va='center', fontsize=10, fontweight='bold', color='#1E3A8A')
    user_fields = [
        "[PK] id : Integer",
        "• username : VarChar(150) UNIQUE",
        "• email : VarChar(254)",
        "• password : VarChar(128) [PBKDF2]",
        "• first_name : VarChar(150)",
        "• last_name : VarChar(150)",
        "• is_staff : Boolean (Moderator)",
        "• is_superuser : Boolean (Admin)",
        "• is_active : Boolean",
        "• date_joined : DateTime",
        "• last_login : DateTime"
    ]
    for idx, field in enumerate(user_fields):
        ax.text(8, 62 - (idx * 2.3), field, fontsize=7.5, color='#1E293B')

    # Entity 2: core_item
    item_box = patches.FancyBboxPatch((46, 18), 36, 52, boxstyle="round,pad=0.5,rounding_size=1",
                                      edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.8)
    ax.add_patch(item_box)
    ax.text(64, 67, 'core_item (Table)', ha='center', va='center', fontsize=10, fontweight='bold', color='#065F46')
    item_fields = [
        "[PK] id : BigAutoField",
        "[FK] user_id : ForeignKey -> auth_user.id",
        "• title : VarChar(200)",
        "• category : VarChar(50) [INDEXED]",
        "• status : VarChar(20) [INDEXED]",
        "• location : VarChar(200)",
        "• date_event : Date",
        "• description : TextField",
        "• contact : VarChar(255)",
        "• image : ImageField (S3 URL path)",
        "• is_verified_returned : Boolean",
        "• resolved_at : DateTime (Nullable)",
        "• is_deleted : Boolean (Soft-Delete)",
        "• deleted_at : DateTime (Nullable)",
        "[FK] deleted_by_id : FK -> auth_user.id",
        "• deletion_reason : TextField",
        "• created_at : DateTime [INDEXED]",
        "• updated_at : DateTime"
    ]
    for idx, field in enumerate(item_fields):
        ax.text(48, 62 - (idx * 2.4), field, fontsize=7.5, color='#0F172A')

    # Entity 3: core_auditlog
    audit_box = patches.FancyBboxPatch((88, 42), 28, 28, boxstyle="round,pad=0.5,rounding_size=1",
                                       edgecolor='#7C3AED', facecolor='#F5F3FF', linewidth=1.8)
    ax.add_patch(audit_box)
    ax.text(102, 67, 'core_auditlog (Table)', ha='center', va='center', fontsize=10, fontweight='bold', color='#5B21B6')
    audit_fields = [
        "[PK] id : BigAutoField",
        "[FK] actor_id : FK -> auth_user.id",
        "• action_type : VarChar(50)",
        "• target_model : VarChar(50)",
        "• target_id : Integer",
        "• details : JSON / TextField",
        "• ip_address : GenericIPAddress",
        "• created_at : DateTime"
    ]
    for idx, field in enumerate(audit_fields):
        ax.text(90, 62 - (idx * 2.4), field, fontsize=7.5, color='#1E293B')

    # Entity 4: core_securityalert
    sec_box = patches.FancyBboxPatch((88, 10), 28, 28, boxstyle="round,pad=0.5,rounding_size=1",
                                     edgecolor='#DC2626', facecolor='#FEF2F2', linewidth=1.8)
    ax.add_patch(sec_box)
    ax.text(102, 35, 'core_securityalert (Table)', ha='center', va='center', fontsize=10, fontweight='bold', color='#991B1B')
    sec_fields = [
        "[PK] id : BigAutoField",
        "• alert_type : VarChar(50)",
        "• severity : VarChar(20)",
        "• description : TextField",
        "• is_resolved : Boolean",
        "[FK] resolved_by_id : FK -> auth_user.id",
        "• resolved_at : DateTime",
        "• created_at : DateTime"
    ]
    for idx, field in enumerate(sec_fields):
        ax.text(90, 30 - (idx * 2.4), field, fontsize=7.5, color='#1E293B')

    # Relationship Arrows
    # User 1 -> Many Items
    ax.annotate('', xy=(46, 54), xytext=(38, 54),
                arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=2, headwidth=7))
    ax.text(42, 56.5, '1 : N', ha='center', va='center', fontsize=8, fontweight='bold', color='#2563EB')

    # User 1 -> Many Audit Logs
    ax.annotate('', xy=(88, 54), xytext=(82, 54),
                arrowprops=dict(facecolor='#7C3AED', edgecolor='#7C3AED', width=2, headwidth=7))
    ax.text(85, 56.5, '1 : N', ha='center', va='center', fontsize=8, fontweight='bold', color='#7C3AED')

    plt.tight_layout()
    plt.savefig('diagrams/database_erd.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved diagrams/database_erd.png")


def generate_ui_wireframe_flow():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 75)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    ax.text(60, 71, 'CampusFind User Interface & Navigation Workflow', ha='center', va='center', fontsize=13, fontweight='bold', color='#1E3A8A')

    # 1. Homepage
    home_box = patches.FancyBboxPatch((6, 40), 24, 24, boxstyle="round,pad=0.6,rounding_size=1",
                                      edgecolor='#2563EB', facecolor='#EFF6FF', linewidth=1.5)
    ax.add_patch(home_box)
    ax.text(18, 61, '1. Homepage (/)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E3A8A')
    ax.text(18, 51, '• Hero Search Bar\n• Live Status Metrics\n• Category Chips\n• Recent Lost/Found Cards', ha='center', va='center', fontsize=7.5, color='#1E293B')

    # 2. Browse Directory
    browse_box = patches.FancyBboxPatch((36, 40), 26, 24, boxstyle="round,pad=0.6,rounding_size=1",
                                        edgecolor='#0284C7', facecolor='#F0F9FF', linewidth=1.5)
    ax.add_patch(browse_box)
    ax.text(49, 61, '2. Browse Items (/items/)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0369A1')
    ax.text(49, 51, '• Keyword Search\n• Category & Status Filters\n• Grid vs Table View Toggle\n• Location & Date Filters', ha='center', va='center', fontsize=7.5, color='#0C4A6E')

    # 3. Item Detail & Notice
    detail_box = patches.FancyBboxPatch((68, 40), 24, 24, boxstyle="round,pad=0.6,rounding_size=1",
                                        edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.5)
    ax.add_patch(detail_box)
    ax.text(80, 61, '3. Item Detail & Flyer', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#065F46')
    ax.text(80, 51, '• Full Item Image Modal\n• Secure Contact Card\n• Campus Safety Guidance\n• Printable Notice Flyer\n  (With tear-off slips)', ha='center', va='center', fontsize=7.5, color='#064E3B')

    # 4. Report Form
    form_box = patches.FancyBboxPatch((6, 8), 24, 24, boxstyle="round,pad=0.6,rounding_size=1",
                                      edgecolor='#D97706', facecolor='#FFFBEB', linewidth=1.5)
    ax.add_patch(form_box)
    ax.text(18, 29, '4. Report Item Form', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#B45309')
    ax.text(18, 19, '• Category & Preset Locations\n• Image Upload (S3 Preview)\n• Date & Details\n• Contact Drop-off Office', ha='center', va='center', fontsize=7.5, color='#78350F')

    # 5. User / Moderator Hub
    my_posts_box = patches.FancyBboxPatch((36, 8), 26, 24, boxstyle="round,pad=0.6,rounding_size=1",
                                          edgecolor='#8B5CF6', facecolor='#F5F3FF', linewidth=1.5)
    ax.add_patch(my_posts_box)
    ax.text(49, 29, '5. My Posts & Moderation', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#6D28D9')
    ax.text(49, 19, '• Edit / Delete Own Posts\n• "Mark as Claimed" Toggle\n• Staff Moderation Queue\n• Verification Badges', ha='center', va='center', fontsize=7.5, color='#4C1D95')

    # 6. Dedicated Admin Portal
    admin_box = patches.FancyBboxPatch((68, 8), 46, 24, boxstyle="round,pad=0.6,rounding_size=1",
                                       edgecolor='#DC2626', facecolor='#FEF2F2', linewidth=1.5)
    ax.add_patch(admin_box)
    ax.text(91, 29, '6. Admin Operations Portal (/ops/)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#B91C1C')
    ax.text(91, 19, '• Security & Governance Dashboard • User Role Administration\n• Immutable Audit Log Viewer & CSV Export\n• Soft-Delete Recovery Queue & Permanent Purge\n• Cloud Telemetry & Health Monitoring (/health/)', ha='center', va='center', fontsize=7.5, color='#7F1D1D')

    # Workflow arrows
    ax.annotate('', xy=(36, 52), xytext=(30, 52),
                arrowprops=dict(facecolor='#0284C7', edgecolor='#0284C7', width=1.5, headwidth=6))
    ax.annotate('', xy=(68, 52), xytext=(62, 52),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=1.5, headwidth=6))
    ax.annotate('', xy=(18, 32), xytext=(18, 40),
                arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', width=1.5, headwidth=6))
    ax.annotate('', xy=(36, 20), xytext=(30, 20),
                arrowprops=dict(facecolor='#8B5CF6', edgecolor='#8B5CF6', width=1.5, headwidth=6))
    ax.annotate('', xy=(68, 20), xytext=(62, 20),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=1.5, headwidth=6))

    plt.tight_layout()
    plt.savefig('diagrams/ui_wireframe_flow.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved diagrams/ui_wireframe_flow.png")


if __name__ == '__main__':
    generate_aws_architecture()
    generate_use_case_diagram()
    generate_database_erd()
    generate_ui_wireframe_flow()
