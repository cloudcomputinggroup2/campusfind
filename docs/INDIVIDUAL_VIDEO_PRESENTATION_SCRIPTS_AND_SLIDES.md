# 🎬 CampusFind: Individual Video Presentation Scripts & Slide Guide

**Course:** CSBC 252 - Introduction to Cloud Computing  
**Project:** CampusFind: A Cloud-Based Campus Lost & Found System  
**Format:** Individual Video Recordings by Role (Self-Contained Slides & Pictures)  
**Interactive Slide Decks:** Open [`individual_slides.html`](file:///home/hackura/campusfind/individual_slides.html) in your browser for role-specific slides, pictures, teleprompter scripts, and recording timers.

---

## 🧭 Overview & Recording Guidelines

Each team member is responsible for recording a dedicated **2 to 4-minute video segment** focusing strictly on their technical domain and deliverables. All slides include self-contained diagrams, code snippets, and pictures—**no live screen-switching or live browser previews required**.

### 🎥 General Recording Best Practices:
1. **Screen + Face Cam (Optional):** Use OBS Studio, Loom, Clipchamp, or Zoom to record your screen while presenting your slides.
2. **Resolution & Audio:** Record at **1080p (1920x1080)** in landscape mode. Speak at a steady, natural pace.
3. **Teleprompter Script:** Press <kbd>N</kbd> on any slide deck to display the word-for-word spoken script.
4. **Time Management:** Press <kbd>T</kbd> to track your speaking time.

---

## 📋 Role Directory & Quick Navigation

| # | Role | Speaker Name / Placeholder | Video Target Time | Core Topic | Direct Slide File |
| :- | :--- | :--- | :--- | :--- | :--- |
| **1** | [**Team Lead / Project Manager**](#-role-1-team-lead--project-manager) | Student 1 | 2.5 Minutes | Project Vision, Problem Statement, Objectives, Team Matrix | [📑 `slides_team_lead.html`](file:///home/hackura/campusfind/docs/slides_team_lead.html) |
| **2** | [**Frontend Developer / UI Lead**](#-role-2-frontend-developer--ui-lead) | Student 2 | 3.5 Minutes | UI Workflow Diagram, Screen Mockups, Printable Notice Flyer, Use Cases | [🎨 `slides_frontend_lead.html`](file:///home/hackura/campusfind/docs/slides_frontend_lead.html) |
| **3** | [**Backend Developer**](#-role-3-backend-developer) | Student 3 | 2.5 Minutes | Django Models, CRUD Architecture, Ownership Gating, `/ops/` Admin Portal | [⚙️ `slides_backend_dev.html`](file:///home/hackura/campusfind/docs/slides_backend_dev.html) |
| **4** | [**Cloud Architect / DevOps**](#-role-4-cloud-architect--devops-lead) | Student 4 | 3.0 Minutes | AWS Topology, EC2 Ubuntu Provisioning, Nginx, Gunicorn, Security Groups | [☁️ `slides_cloud_architect.html`](file:///home/hackura/campusfind/docs/slides_cloud_architect.html) |
| **5** | [**Database Lead**](#-role-5-database-lead) | Student 5 | 2.0 Minutes | 3NF ERD Normalization, Amazon RDS PostgreSQL, DB Subnets, Seed Script | [🗄️ `slides_database_lead.html`](file:///home/hackura/campusfind/docs/slides_database_lead.html) |
| **6** | [**Storage & Security Lead**](#-role-6-storage--security-lead) | Student 6 | 2.5 Minutes | Decoupled Amazon S3 Storage, IAM Least-Privilege, `.env`, Framework Hardening | [🔐 `slides_storage_security.html`](file:///home/hackura/campusfind/docs/slides_storage_security.html) |
| **7** | [**QA & Documentation Lead**](#-role-7-qa--documentation-lead) | Student 7 | 3.0 Minutes | Automated Tests (9/9), CloudWatch Telemetry, `/health/`, Challenges, Conclusion | [🧪 `slides_qa_docs.html`](file:///home/hackura/campusfind/docs/slides_qa_docs.html) |

---

## 👑 Role 1: Team Lead / Project Manager

- **Target Duration:** 2:00 – 2:30 Minutes
- **Key Deliverable Files:** [`docs/01_PROJECT_PROPOSAL.md`](file:///home/hackura/campusfind/docs/01_PROJECT_PROPOSAL.md), [`README.md`](file:///home/hackura/campusfind/README.md)
- **Slide Deck:** Launch [`docs/slides_team_lead.html`](file:///home/hackura/campusfind/docs/slides_team_lead.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 1.1 — Title & Introduction]**  
> *"Hello Professor and evaluators. My name is [Your Name], and I am the Team Lead and Project Manager for our CSBC 252 Capstone Project: **CampusFind: A Cloud-Based Campus Lost & Found System**.*  
> 
> *Our project is a production-grade, cloud-native web application built using Django, Bootstrap, and deployed on Amazon Web Services using Free Tier infrastructure: Amazon EC2, Amazon RDS PostgreSQL, Amazon S3, AWS IAM, and Amazon CloudWatch."*

> **[Slide 1.2 — Problem Statement & Campus Friction]**  
> *"On any university campus, students and faculty lose valuable personal items every single day—ranging from student IDs and dorm keys to expensive laptops and textbooks.  
> 
> Traditionally, recovery efforts rely on fragmented WhatsApp group chats, physical bulletin boards, or word of mouth. This creates immense friction: there is no central search, no category filtering, records are never updated when items are found, and personal phone numbers are broadcast publicly. CampusFind replaces this with a unified, searchable single source of truth."*

> **[Slide 1.3 — Project Objectives & Scope Control]**  
> *"To ensure delivery within our 3-day sprint timeline, we established strict scope boundaries.  
> 
> In scope: full CRUD operations, S3-backed image uploads, Amazon RDS PostgreSQL persistence, printable notice flyers, staff moderation, and our dedicated /ops/ admin operations portal.  
> 
> Intentionally out of scope: complex peer-to-peer chat (we use direct phone/email contact links to prevent spam and protect privacy) and monetary bounty gateways."*

> **[Slide 1.4 — Team Roles & Responsibilities]**  
> *"Our project was divided across 7 specialized engineering domains: Frontend, Backend, Cloud Architecture, Database, Storage & Security, and Quality Assurance. Each team member had dedicated ownership of specific files, AWS resources, and presentation segments. I will now hand over to our Frontend Lead to walk you through our user interface and visual workflows."*

> **[Slide 1.5 — High-Level AWS Solution Topology]**  
> *"In summary, CampusFind demonstrates a resilient, cloud-native architecture built within AWS Free Tier limits. I will now let our team members present their individual technical implementations. Thank you!"*

---

## 🎨 Role 2: Frontend Developer / UI Lead

- **Target Duration:** 3:00 – 4:00 Minutes
- **Key Deliverable Files:** [`templates/`](file:///home/hackura/campusfind/templates), [`static/css/styles.css`](file:///home/hackura/campusfind/static/css/styles.css), [`static/js/main.js`](file:///home/hackura/campusfind/static/js/main.js)
- **Slide Deck:** Launch [`docs/slides_frontend_lead.html`](file:///home/hackura/campusfind/docs/slides_frontend_lead.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 2.1 — Role Title & Overview]**  
> *"Hello, my name is [Your Name], and I served as the Frontend Developer and UI Lead for CampusFind.  
> 
> My responsibility was designing and implementing an intuitive, accessible, and fully responsive user interface using HTML5, Bootstrap 5.3, custom CSS design tokens, and lightweight vanilla JavaScript.  
> 
> Key frontend features include real-time hero metric counters, a dual-mode catalog (Card Grid vs Table Directory), client-side image upload previews with 5MB validation in `main.js`, and one-click contact copying."*

> **[Slide 2.2 — UI & Navigation Workflow Diagram]**  
> *(Show Slide with `diagrams/ui_wireframe_flow.png`)*  
> *"Here is our complete UI Navigation Workflow diagram.  
> 
> The user journey starts at the Homepage with live metrics and search bar, moves to the Browse Directory where users can filter by category or toggle Card vs Table views, leads to the Item Detail page with campus safety guidance and the Printable Notice Flyer, supports Item Reporting with client-side image preview, provides My Posts for ownership resolution, and connects administrators to the /ops/ portal."*

> **[Slide 2.3 — Core Application Screens & Dual View]**  
> *(Show Slide with UI Mockup Screens)*  
> *"Let's look at the core user interface screens shown here:  
> - **1. Homepage:** Features live metric counters calculating active lost, found, and reunited items on every page load, along with quick category chips.  
> - **2. Report Item Form:** Features campus building dropdowns and instant client-side photo previews in `main.js` with 5MB validation before network transmission.  
> - **3. Dual Catalog View:** Users can toggle with one click between a visual Card Grid for photo browsing and a dense Table View for rapid scanning."*

> **[Slide 2.4 — Printable Bulletin Notice Flyer with Tear-Off Slips]**  
> *(Show Slide with Print Notice Poster & Tear-off Slips)*  
> *"A standout feature I engineered is the **Printable Notice Flyer** shown here.  
> 
> Recognizing that many students still check physical notice boards across campus, this feature generates a high-contrast print-ready poster formatted with a large photo, description, and **8 vertical tear-off contact slips** along the bottom.  
> 
> Students walking past in the library or dining hall can simply tear off a slip to contact the owner or drop-off desk. Once an item is recovered, the poster navigates to 'My Posts' and clicks 'Mark as Claimed' to update the status badge to Reunited."*

> **[Slide 2.5 — System Use Cases & Personas]**  
> *(Show Slide with `diagrams/use_case_diagram.png`)*  
> *"Finally, here is our Use Case Diagram showing how our three campus user personas—Students, Staff Moderators, and System Administrators—interact with the platform. This structured design ensures a smooth, accessible experience across all university devices. Thank you!"*

---

## ⚙️ Role 3: Backend Developer

- **Target Duration:** 2:30 – 3:00 Minutes
- **Key Deliverable Files:** [`core/models.py`](file:///home/hackura/campusfind/core/models.py), [`core/views.py`](file:///home/hackura/campusfind/core/views.py), [`core/forms.py`](file:///home/hackura/campusfind/core/forms.py), [`templates/admin_portal/`](file:///home/hackura/campusfind/templates/admin_portal)
- **Slide Deck:** Launch [`docs/slides_backend_dev.html`](file:///home/hackura/campusfind/docs/slides_backend_dev.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 3.1 — Backend Role Title]**  
> *"Hello, my name is [Your Name], and I was the Backend Developer for CampusFind. My role was implementing the core application logic using Python 3.12 and Django 5.0—including data models, form validations, ownership-based access control, search query filtering, and our custom Administrative Operations Portal."*

> **[Slide 3.2 — Data Models & Ownership Authorization]**  
> *"The `Item` model in `core/models.py` encapsulates all post attributes: foreign key link to `auth_user`, category choices, building locations, lifecycle resolution flags, and S3 image keys.  
> - We implemented custom model methods like `mark_as_claimed()`, `is_owner()`, and `status_badge_class` to keep views clean.  
> - In `views.py`, we enforce strict ownership authorization: students can only edit, delete, or resolve their own listings. Unauthorized modification requests are blocked at the view layer.  
> - `ItemForm` strictly validates uploaded file extensions and enforces a 5MB size limit before processing."*

> **[Slide 3.3 — Admin Operations Portal (`/ops/`)]**  
> *"To ensure proper platform governance, we built a dedicated `/ops/` Admin Portal for staff administrators:  
> - **User & Role Governance:** Admins can search users, toggle account active status, promote or demote staff moderator roles, and review security alerts.  
> - **Two-Phase Data Safety:** We avoid accidental data loss by utilizing a soft-delete queue first; permanent hard-deletes require mandatory reason logging.  
> - **Immutable Audit Trail:** All administrative promotions, lockouts, and deletions are recorded in our audit log viewer with timestamps and actor details."*

---

## ☁️ Role 4: Cloud Architect / DevOps Lead

- **Target Duration:** 2:30 – 3:00 Minutes
- **Key Deliverable Files:** [`deploy/ec2_setup.sh`](file:///home/hackura/campusfind/deploy/ec2_setup.sh), [`deploy/nginx.conf`](file:///home/hackura/campusfind/deploy/nginx.conf), [`deploy/gunicorn.service`](file:///home/hackura/campusfind/deploy/gunicorn.service)
- **Slide Deck:** Launch [`docs/slides_cloud_architect.html`](file:///home/hackura/campusfind/docs/slides_cloud_architect.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 4.1 — Cloud Architect Role Title]**  
> *"Hello, my name is [Your Name], and I served as the Cloud Architect and DevOps Lead for CampusFind. My primary objective was designing, provisioning, and securing our multi-tier cloud infrastructure on Amazon Web Services, fully adhering to the AWS Free Tier specifications within the `us-east-1` region."*

> **[Slide 4.2 — AWS Multi-Tier VPC Architecture]**  
> *"Our architecture employs a decoupled, multi-tier topology inside a custom VPC in `us-east-1`:  
> - **Public Subnet:** Hosts our Amazon EC2 instance running Ubuntu Server 24.04 on a `t2.micro` instance.  
> - **Nginx 1.24:** Serves as our front-line reverse proxy on ports 80 and 443, handling SSL termination, static caching, Gzip compression, and proxying dynamic requests to Gunicorn on socket port 8000.  
> - **Private Subnet:** Isolates our Amazon RDS database, and S3 handles uploaded media independently."*

> **[Slide 4.3 — EC2, Nginx & Gunicorn Systemd Daemon]**  
> *"Here is our compute server configuration:  
> - Our automated deployment script `deploy/ec2_setup.sh` configured the entire server cleanly.  
> - Gunicorn is managed as a resilient `systemd` daemon (`gunicorn.service`), ensuring automatic restart on reboot or crash.  
> - Nginx handles static file caching and reverse proxying with Gzip compression on ports 80 and 443."*

> **[Slide 4.4 — EC2 Security Group (`CampusFind-EC2-SG`)]**  
> *"For perimeter security, we created `CampusFind-EC2-SG`: Inbound HTTP on port 80 and HTTPS on port 443 are open to the public, while administrative SSH on port 22 is strictly whitelisted to trusted administrative IPs. This provides strong perimeter isolation. Thank you!"*

---

## 🗄️ Role 5: Database Lead

- **Target Duration:** 2:00 – 2:30 Minutes
- **Key Deliverable Files:** [`core/management/commands/seed_data.py`](file:///home/hackura/campusfind/core/management/commands/seed_data.py), [`campusfind/settings.py`](file:///home/hackura/campusfind/campusfind/settings.py)
- **Slide Deck:** Launch [`docs/slides_database_lead.html`](file:///home/hackura/campusfind/docs/slides_database_lead.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 5.1 — Database Lead Role Title]**  
> *"Hello, my name is [Your Name], and I was the Database Lead for CampusFind. I was responsible for database schema normalization, provisioning our managed relational database on Amazon RDS, configuring private subnet networking, and maintaining data migration integrity."*

> **[Slide 5.2 — Entity Relationship Diagram (3NF ERD)]**  
> *"Our schema is strictly normalized to **Third Normal Form (3NF)**:  
> - The standard `auth_user` table manages account authentication, password hashes, and staff flags.  
> - The `core_item` table stores lost/found listings, connected to `auth_user` via a cascading foreign key.  
> - We placed B-tree indexes on high-frequency query columns including `status`, `category`, and `created_at` to ensure sub-millisecond filtering speed even across thousands of campus records.  
> - Our automated seeding script `seed_data.py` populates realistic sample items and user accounts."*

> **[Slide 5.3 — Amazon RDS & Private Subnet Isolation]**  
> *"For our cloud database, we provisioned PostgreSQL 16 on Amazon RDS (`db.t3.micro` Free Tier).  
> - It is deployed with **'Publicly Accessible: No'** inside a private DB subnet group.  
> - Its dedicated security group, `CampusFind-RDS-SG`, contains an inbound rule allowing TCP port 5432 **exclusively from `CampusFind-EC2-SG`**.  
> - This guarantees that no external actor on the internet can scan or connect directly to the database. Thank you!"*

---

## 🔐 Role 6: Storage & Security Lead

- **Target Duration:** 2:30 – 3:00 Minutes
- **Key Deliverable Files:** [`deploy/iam_policy.json`](file:///home/hackura/campusfind/deploy/iam_policy.json), [`.env.example`](file:///home/hackura/campusfind/deploy/.env.example)
- **Slide Deck:** Launch [`docs/slides_storage_security.html`](file:///home/hackura/campusfind/docs/slides_storage_security.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 6.1 — Storage & Security Role Title]**  
> *"Hello, my name is [Your Name], and I served as the Storage & Security Lead for CampusFind. My responsibility was architecting our decoupled media storage pipeline on Amazon S3 and implementing an end-to-end least-privilege security framework across cloud and application layers."*

> **[Slide 6.2 — Decoupled Amazon S3 Media Pipeline]**  
> *"In cloud architecture, compute should always remain stateless. Instead of storing uploaded images on the EC2 disk, CampusFind uploads all item photos directly to our dedicated Amazon S3 bucket: `campusfind-item-images-capstone`.  
> - We integrated `boto3` and `django-storages` with automatic local storage fallback when `USE_S3=False` for offline testing.  
> - We enforce strict upload validation: files are restricted to valid image MIME types and capped at a maximum of **5 MB**."*

> **[Slide 6.3 — IAM Least-Privilege & Secrets Governance]**  
> *"For cloud security, we strictly follow the Principle of Least Privilege:  
> - Our IAM policy grants only `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, and `s3:ListBucket` strictly scoped to our specific bucket ARN.  
> - **Zero Hardcoded Secrets:** No database passwords, secret keys, or AWS access tokens exist in source code. Everything is injected at runtime through environment variables via `.env`."*

> **[Slide 6.4 — Application Layer Threat Hardening]**  
> *"At the application layer: User passwords use Django's PBKDF2 algorithm with SHA-256 and unique per-user cryptographic salts. SQL injection is prevented through parameterized ORM queries. CSRF tokens protect all state-changing forms, and template escaping prevents XSS attacks. Thank you!"*

---

## 🧪 Role 7: QA & Documentation Lead

- **Target Duration:** 2:30 – 3:00 Minutes
- **Key Deliverable Files:** [`core/tests.py`](file:///home/hackura/campusfind/core/tests.py), [`docs/06_FINAL_TECHNICAL_REPORT.md`](file:///home/hackura/campusfind/docs/06_FINAL_TECHNICAL_REPORT.md)
- **Slide Deck:** Launch [`docs/slides_qa_docs.html`](file:///home/hackura/campusfind/docs/slides_qa_docs.html)

### 🎙️ Word-for-Word Spoken Script:

> **[Slide 7.1 — QA Role Title]**  
> *"Hello, my name is [Your Name], and I served as the QA, Testing & Documentation Lead for CampusFind. My role was implementing automated unit and integration tests, setting up synthetic health monitoring, analyzing Amazon CloudWatch telemetry, and compiling our final capstone technical documentation."*

> **[Slide 7.2 — Automated Testing & Validation Results]**  
> *"To ensure zero regressions, we built a comprehensive test suite in `core/tests.py`.  
> 
> When we run `python manage.py test`:  
> - 9 automated test cases execute covering user registration, session authentication, item CRUD creation, file size validation, search filtering, ownership permissions, and health checks.  
> - All 9 tests pass with a **100% success rate** in under 32 seconds."*

> **[Slide 7.3 — CloudWatch Telemetry & Health Monitoring]**  
> *"For uptime monitoring, we implemented a dedicated `/health/` JSON endpoint that verifies live database connectivity for load balancers. In Amazon CloudWatch, we monitored our EC2 instance: `CPUUtilization` consistently averages under 3% during standard operations, and `NetworkIn`/`NetworkOut` metrics verify normal web and image transfer traffic without bottlenecks."*

> **[Slide 7.4 — Challenges Overcome & Future Roadmap]**  
> *"During our sprint, we resolved key engineering challenges—including WhiteNoise static manifests during test execution and implementing conditional S3 storage backends for offline development. Future roadmap items include automated email keyword matching and printable QR code asset tags."*

> **[Slide 7.5 — Project Summary & Capstone Achievements]**  
> *"In conclusion, CampusFind successfully proves that a secure, scalable, and production-grade cloud solution can be built entirely within AWS Free Tier resources. All 4 DOCX deliverables, deployment scripts, and automated tests are verified and complete. Thank you very much for your time!"*
