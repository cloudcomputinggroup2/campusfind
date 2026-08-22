# 📑 CampusFind: Capstone Presentation Slides & Speaker Guide

**Course:** CSBC 252 - Introduction to Cloud Computing  
**Project:** CampusFind: A Cloud-Based Campus Lost & Found System  
**Presentation Target Duration:** 15 – 20 Minutes  
**Slide Deck Deliverable:** [`presentation.html`](file:///home/hackura/campusfind/presentation.html) (Interactive browser presentation deck with presenter controls and timer)

---

## 🧭 Group Speaking Roles & Timing Matrix

| Slide # | Slide Title | Speaker Role | Allocated Time | Cumulative Time |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Title Slide: CampusFind Cloud Architecture | **1. Team Lead / PM** | 0:00 – 0:30 | 0:30 |
| **2** | Executive Summary & Campus Vision | **1. Team Lead / PM** | 0:30 – 1:15 | 1:15 |
| **3** | Problem Statement: Traditional Friction | **1. Team Lead / PM** | 1:15 – 2:00 | 2:00 |
| **4** | Project Objectives & Scope Control | **1. Team Lead / PM** | 2:00 – 2:30 | 2:30 |
| **5** | Capstone Team Roles & Deliverables | **1. Team Lead / PM** | 2:30 – 3:00 | 3:00 |
| **6** | System Use Cases & Campus Personas | **2. Frontend UI Lead** | 3:00 – 4:00 | 4:00 |
| **7** | UI/UX Design System & Features | **2. Frontend UI Lead** | 4:00 – 5:00 | 5:00 |
| **8** | Live Demonstration Walkthrough Flow | **2. Frontend UI Lead** | 5:00 – 7:30 | 7:30 |
| **9** | Admin Operations Portal (`/ops/`) | **3. Backend Developer** | 7:30 – 8:30 | 8:30 |
| **10** | AWS Multi-Tier Cloud Architecture | **4. Cloud Architect** | 8:30 – 9:30 | 9:30 |
| **11** | Compute Tier: EC2, Nginx & Gunicorn | **4. Cloud Architect** | 9:30 – 10:45 | 10:45 |
| **12** | Database Tier: Amazon RDS PostgreSQL (3NF) | **5. Database Lead** | 10:45 – 12:30 | 12:30 |
| **13** | Decoupled Media Storage with Amazon S3 | **6. Storage & Security** | 12:30 – 13:45 | 13:45 |
| **14** | Security Governance, IAM Least-Privilege | **6. Storage & Security** | 13:45 – 15:00 | 15:00 |
| **15** | Automated Testing & QA Results (9/9) | **7. QA & Docs Lead** | 15:00 – 16:00 | 16:00 |
| **16** | CloudWatch Telemetry & `/health/` Check | **7. QA & Docs Lead** | 16:00 – 16:45 | 16:45 |
| **17** | Engineering Challenges & Solutions | **7. QA & Docs Lead** | 16:45 – 17:30 | 17:30 |
| **18** | System Roadmap & Future Enhancements | **7. QA & Docs Lead** | 17:30 – 18:00 | 18:00 |
| **19** | Project Summary & Capstone Achievements | **1. Team Lead / All** | 18:00 – 18:30 | 18:30 |
| **20** | Q&A, Live Demo & Discussion | **All Team Members** | 18:30 – 20:00 | 20:00 |

---

## 🖥️ Slide-by-Slide Content & Verbatim Speaker Scripts

---

### Slide 1: Title Slide (CampusFind)
- **Visuals:** Project Logo, Subtitle, Cloud Badges, Course Identifier (CSBC 252), Team Role Tags.
- **Speaker:** 1. Team Lead / Project Manager
- **Time:** 0:00 – 0:30

> **🎙️ Speaker Script:**  
> "Hello Professor and fellow classmates. Welcome to our Capstone presentation for **CSBC 252: Introduction to Cloud Computing**.  
> 
> Our team is proud to present **CampusFind: A Cloud-Based Campus Lost & Found System**.  
> 
> CampusFind is an enterprise-grade, cloud-native web application built using Python 3.12, Django 5.0, Bootstrap 5.3, and deployed 100% on **Amazon Web Services (AWS) Free Tier** resources. Over the next 18 minutes, our team will guide you through our problem space, live platform demo, multi-tier cloud architecture, database normalization, security posture, and testing results."

---

### Slide 2: Executive Summary & Vision
- **Visuals:** 3 Grid Cards: The Campus Problem, The Solution, AWS Cloud Strategy.
- **Speaker:** 1. Team Lead / Project Manager
- **Time:** 0:30 – 1:15

> **🎙️ Speaker Script:**  
> "To understand the motivation behind CampusFind: across any university campus, thousands of valuable personal items—such as student IDs, dorm keys, laptops, chargers, and textbooks—are misplaced each semester.  
> 
> Recovery efforts today are plagued by disorganized communication channels. Inquiries get lost in noisy chat groups, and physical lost-and-found desks lack real-time synchronization.  
> 
> CampusFind bridges this gap by providing a central cloud repository with instant search filters, image verification, and status tracking—leveraging Amazon EC2, Amazon RDS, Amazon S3, IAM, and CloudWatch."

---

### Slide 3: Problem Statement: Traditional Friction vs Cloud Paradigm
- **Visuals:** 2 Side-by-Side Cards: Traditional Methods (Failures) vs CampusFind Cloud Paradigm (Solutions).
- **Speaker:** 1. Team Lead / Project Manager
- **Time:** 1:15 – 2:00

> **🎙️ Speaker Script:**  
> "Looking closer at the current campus landscape, we identified four critical points of friction:  
> 1. **Scattered Channels:** Reports are fragmented across WhatsApp, Reddit, campus bulletin boards, and front desks.  
> 2. **Zero Search & Indexing:** A student looking for a specific calculator or dorm key has no way to filter by campus building, date, or category.  
> 3. **Obsolete Records:** Group chats and notice boards are never cleaned up once an item is returned.  
> 4. **Privacy Risks:** Students broadcast their personal phone numbers and identities indiscriminately.  
> 
> CampusFind replaces this chaos with a unified, searchable single source of truth featuring verified item resolution and secure role governance."

---

### Slide 4: Project Objectives & Scope Boundaries
- **Visuals:** Technical Objectives Card + Scope Boundary Card (In Scope vs Out of Scope).
- **Speaker:** 1. Team Lead / Project Manager
- **Time:** 2:00 – 2:30

> **🎙️ Speaker Script:**  
> "To ensure delivery of a robust system within our 3-day sprint timeline, we established strict scope boundaries:  
> 
> - **In Scope:** Full CRUD operations, dual card/table views, S3 decoupled image storage, Amazon RDS PostgreSQL persistence, printable notice flyers, staff moderation, and our dedicated `/ops/` admin operations portal.  
> - **Intentionally Out of Scope:** Real-time peer-to-peer chat (we use direct phone/email contact links to prevent spam and protect privacy) and payment/bounty gateways.  
> 
> I will now hand over to our Frontend UI Lead to walk you through our user experience and live platform demonstration."

---

### Slide 5: Capstone Team Roles & Deliverables
- **Visuals:** Structured Table mapping each team member to their technical domain, key file deliverables, and speaking slot.
- **Speaker:** 1. Team Lead / Project Manager (Transition to Frontend Lead)
- **Time:** 2:30 – 3:00

> **🎙️ Speaker Script:**  
> "Here is our group's workload distribution. Every member took full ownership of a specialized domain—from UI templates and backend CRUD logic, to EC2 provisioning, RDS database design, S3 storage security, and automated QA testing."

---

### Slide 6: System Use Cases & Campus Personas
- **Visuals:** 3 Personas Cards: Student / General User, Campus Staff / Moderator, System Administrator (`/ops/`).
- **Speaker:** 2. Frontend UI Lead
- **Time:** 3:00 – 4:00

> **🎙️ Speaker Script:**  
> "Thank you. Let's look at how our users interact with CampusFind. We designed the platform around three distinct user personas:  
> 
> 1. **Students & General Users:** Can register, submit lost or found item reports with photos, search the campus directory, print physical notice flyers, and manage their own listings.  
> 2. **Campus Staff & Moderators:** Access a dedicated Moderation Dashboard to review listings, resolve items handed into security desks, and flag spam.  
> 3. **System Administrators:** Operate our new `/ops/` portal for staff role assignment, user lockouts, audit trail compliance, and safe data lifecycle management."

---

### Slide 7: UI/UX Design System & Features
- **Visuals:** Interactive UI Components Card + Physical Bulletin Notice Flyer Card.
- **Speaker:** 2. Frontend UI Lead
- **Time:** 4:00 – 5:00

> **🎙️ Speaker Script:**  
> "For the frontend, we built a modern, responsive design system using Bootstrap 5.3 and custom CSS tokens:  
> 
> - **Real-Time Metrics:** Dynamic hero counters calculate active lost, found, and reunited items on every page load.  
> - **Dual View Layout:** Users can toggle between a visual Card Grid for photo browsing and a compact Table Directory for fast scanning.  
> - **Client-Side JS Validation (`main.js`):** Users get instant photo previews and file size checking before uploading.  
> - **Physical Notice Flyer:** A standout feature is our one-click printable notice generator (`print_notice.html`) formatted with tear-off contact slips for physical campus bulletin boards."

---

### Slide 8: Live Demonstration Walkthrough Flow
- **Visuals:** 3 Walkthrough Step Cards: 1. Discovery & Search, 2. Posting & Validation, 3. Flyer & Resolution.
- **Speaker:** 2. Frontend UI Lead
- **Time:** 5:00 – 7:30

> **🎙️ Speaker Script (Live Screen Share):**  
> "Let us now jump into the live deployed web application!  
> 
> *(Screen Share: Browser open to homepage)*  
> 
> 1. **Homepage:** Notice our live hero statistics and category chips. Let's search for 'MacBook'—notice how results filter instantly across campus buildings.  
> 2. **Posting a Report:** Let's log in as `student_alex`. We click 'Report Item', select category 'Electronics', pick 'Science & Tech Complex', add description, and select a photo. Notice the instant client-side image preview!  
> 3. **Printable Flyer:** Clicking into our new post, we click 'Print Notice Flyer'—here is the print-ready notice complete with tear-off contact slips.  
> 4. **Item Resolution:** Finally, navigating to 'My Posts', Alex can click 'Mark as Claimed/Reunited' once recovered, immediately updating the status badge to Reunited.  
> 
> Now, our Backend Developer will explain our administrative governance portal."

---

### Slide 9: Admin Operations Portal (`/ops/`) & Governance
- **Visuals:** 2 Cards: Security & Role Management + Audit Logging & Data Safety.
- **Speaker:** 3. Backend Developer
- **Time:** 7:30 – 8:30

> **🎙️ Speaker Script:**  
> "Beyond the student interface, we engineered an operations portal located at `/ops/` strictly for system administrators:  
> 
> - **User & Role Governance:** Admins can promote students to staff moderators, deactivate compromised accounts, or trigger password reset workflows.  
> - **Two-Phase Data Safety:** Destructive actions utilize a soft-delete queue first; permanent hard-deletes require explicit reason logging.  
> - **Immutable Audit Trail:** All administrative actions, role modifications, and login attempts are recorded with actors, timestamps, and IP metadata for academic compliance.  
> 
> I now pass the presentation to our Cloud Architect to explore our AWS infrastructure."

---

### Slide 10: AWS Multi-Tier Cloud Architecture
- **Visuals:** Embedded AWS Architecture Diagram + Key Architectural Highlights Card.
- **Speaker:** 4. Cloud Architect
- **Time:** 8:30 – 9:30

> **🎙️ Speaker Script:**  
> "Thank you. Let us examine the AWS cloud architecture supporting CampusFind.  
> 
> We architected a multi-tier, decoupled topology inside a custom Amazon VPC in the `us-east-1` region:  
> 
> 1. **Public Web Subnet:** Contains our Amazon EC2 instance hosting Nginx and Gunicorn.  
> 2. **Private DB Subnet:** Isolates our Amazon RDS PostgreSQL database from direct public internet exposure.  
> 3. **Decoupled S3 Layer:** Handles all uploaded media assets independently of EC2 disk storage.  
> 4. **Security & Observability:** Enforces IAM least-privilege policies and streams metrics to Amazon CloudWatch."

---

### Slide 11: Compute & Web Server Layer (EC2, Nginx, Gunicorn)
- **Visuals:** Server Configuration Card + EC2 Security Group Rule Table (Ports 80, 443, 22).
- **Speaker:** 4. Cloud Architect
- **Time:** 9:30 – 10:45

> **🎙️ Speaker Script:**  
> "On our Amazon EC2 instance (Ubuntu 24.04 LTS, `t2.micro`):  
> 
> - **Nginx 1.24** acts as our reverse proxy, terminating HTTP/HTTPS, serving static assets with WhiteNoise compression, and handling request buffering.  
> - **Gunicorn 21** manages Python WSGI worker processes on port 8000 and is configured as a `systemd` daemon with automatic reboot recovery.  
> - **Security Group (`CampusFind-EC2-SG`):** Allows public HTTP (80) and HTTPS (443), while administrative SSH (22) is strictly whitelisted to trusted administrative IPs.  
> 
> Now, our Database Lead will present our data persistence tier."

---

### Slide 12: Database Tier & RDS PostgreSQL (3NF Schema)
- **Visuals:** Embedded Database ERD Diagram + RDS Architecture & Normalization Card.
- **Speaker:** 5. Database Lead
- **Time:** 10:45 – 12:30

> **🎙️ Speaker Script:**  
> "Thanks! Let's examine our relational database layer.  
> 
> - **Managed Relational Persistence:** We utilize Amazon RDS PostgreSQL 16 on a `db.t3.micro` instance with automated storage and daily backups.  
> - **Network Isolation:** Our RDS security group (`CampusFind-RDS-SG`) accepts port 5432 connections **only from the EC2 security group**. It is completely inaccessible from the public internet.  
> - **Third Normal Form (3NF) Schema:** Our database cleanly separates `auth_user` accounts from `core_item` records via foreign keys with cascading integrity.  
> - **Performance Indexing:** We placed B-tree indexes on high-frequency query columns including `status`, `category`, and `created_at` for sub-10ms response times.  
> - **Data Seeding:** Our automated script `seed_data.py` populates realistic sample listings across campus buildings.  
> 
> Over to our Storage & Security Lead."

---

### Slide 13: Decoupled Media Storage with Amazon S3
- **Visuals:** Amazon S3 Integration Card + Upload Validation Pipeline Card.
- **Speaker:** 6. Storage & Security Lead
- **Time:** 12:30 – 13:45

> **🎙️ Speaker Script:**  
> "A core cloud design principle in CampusFind is decoupling ephemeral compute from persistent media storage:  
> 
> - **Amazon S3 Object Storage:** Item photos are uploaded directly to our dedicated S3 bucket (`campusfind-item-images-capstone`) using `django-storages` and `boto3`.  
> - **Stateless Compute:** Because images live on S3, our EC2 instance is completely stateless. It can be rebooted, scaled, or replaced with zero risk of user data loss.  
> - **Offline Resilience:** If `USE_S3=False` in `.env`, the system automatically switches to local disk storage, allowing full offline local development.  
> - **Validation Pipeline:** File uploads are validated both client-side and server-side with a strict 5MB limit and MIME image type whitelist."

---

### Slide 14: Security Governance & IAM Least-Privilege
- **Visuals:** Application Security Defenses Card + IAM Policy JSON Snippet.
- **Speaker:** 6. Storage & Security Lead
- **Time:** 13:45 – 15:00

> **🎙️ Speaker Script:**  
> "Security was designed into every layer of CampusFind:  
> 
> - **Zero Hardcoded Secrets:** All database credentials, Django secret keys, and AWS access tokens are loaded dynamically at runtime via `.env`.  
> - **Password Hashing:** Stored using Django's PBKDF2 SHA-256 algorithm with unique per-user cryptographic salts.  
> - **Injection & XSS Protection:** Parameterized ORM queries prevent SQL injection, while automatic template escaping prevents XSS.  
> - **Least-Privilege IAM Policy:** Our custom IAM policy restricts S3 access strictly to `PutObject`, `GetObject`, `DeleteObject`, and `ListBucket` exclusively on our bucket ARN.  
> 
> I now hand over to our QA & Documentation Lead."

---

### Slide 15: Automated Testing & QA Results
- **Visuals:** Comprehensive Test Table listing TC-01 through TC-09 with 100% PASS badges.
- **Speaker:** 7. QA & Documentation Lead
- **Time:** 15:00 – 16:00

> **🎙️ Speaker Script:**  
> "To verify enterprise stability, we developed a comprehensive automated test suite in Django.  
> 
> Running `python manage.py test` executes 9 automated test cases covering user registration, session authentication, item CRUD creation, file size validation, catalog filtering, ownership authorization checks, and our health endpoint.  
> 
> All 9 tests execute in under 32 seconds with a **100% pass rate and zero regressions**."

---

### Slide 16: CloudWatch Telemetry & Health Monitoring
- **Visuals:** Dedicated `/health/` Endpoint JSON Card + CloudWatch Telemetry Metrics Card.
- **Speaker:** 7. QA & Documentation Lead
- **Time:** 16:00 – 16:45

> **🎙️ Speaker Script:**  
> "For operational visibility:  
> 
> - **Health Check Probing:** We implemented a dedicated `/health/` JSON endpoint that performs a live database ping. It returns HTTP 200 with component status for AWS Route 53 or load balancer health checks.  
> - **Amazon CloudWatch:** We track real-time EC2 `CPUUtilization` (averaging under 3%), `NetworkIn`/`NetworkOut` traffic volumes, and hypervisor health checks."

---

### Slide 17: Engineering Challenges & Technical Solutions
- **Visuals:** 3 Cards: WhiteNoise Test Manifest, Offline Local Development, RDS Subnet Isolation.
- **Speaker:** 7. QA & Documentation Lead
- **Time:** 16:45 – 17:30

> **🎙️ Speaker Script:**  
> "During development, we overcame three key technical hurdles:  
> 1. **WhiteNoise Manifest in Testing:** Strict static manifest hashing caused test failures without pre-collected static files; we resolved this by using `CompressedStaticFilesStorage`.  
> 2. **Decoupled Local vs Cloud Storage:** We engineered conditional backend loading in `settings.py` so team members could test locally without active AWS credentials.  
> 3. **RDS Network Security:** We verified that PostgreSQL traffic was strictly confined between the EC2 and RDS security groups with zero public exposure."

---

### Slide 18: System Roadmap & Future Enhancements
- **Visuals:** 3 Vision Cards: AI Keyword Matching Engine, QR Code Asset Stickers, Multi-AZ High Availability.
- **Speaker:** 7. QA & Documentation Lead
- **Time:** 17:30 – 18:00

> **🎙️ Speaker Script:**  
> "Looking ahead, our roadmap includes:  
> - **Automated Email Matching:** Background Celery/SQS tasks to match newly found items with reported lost items and notify owners.  
> - **QR Code Asset Stickers:** Generatable QR stickers students can print and affix to laptops for 1-tap lost reporting.  
> - **Multi-AZ High Availability:** Adding an Application Load Balancer across multiple EC2 instances in different Availability Zones."

---

### Slide 19: Project Summary & Capstone Achievements
- **Visuals:** 4 Highlight Cards: AWS Free Tier, Decoupled Design, Hardened Security, Verified QA.
- **Speaker:** 1. Team Lead / Project Manager (with Group)
- **Time:** 18:00 – 18:30

> **🎙️ Speaker Script:**  
> "In summary, CampusFind demonstrates that a production-grade, highly available, and secure cloud solution can be engineered entirely within AWS Free Tier constraints. Our system decouples compute, database, and storage while enforcing enterprise role governance and automated QA."

---

### Slide 20: Q&A, Live Demo & Discussion
- **Visuals:** Congratulations / Q&A Prompt, Deliverable Checklist, GitHub Link.
- **Speaker:** All Team Members
- **Time:** 18:30 – 20:00

> **🎙️ Speaker Script:**  
> "Thank you very much for your time and attention. Our live deployment, code repository, and automated tests are open for inspection.  
> 
> We are now ready to answer any questions!"

---

## 🎯 Anticipated Q&A Defense Questions & Model Answers

### Question 1: "Why did you store uploaded images in Amazon S3 instead of saving them on the EC2 instance?"
- **Answer:**  
  *"Saving media on an EC2 instance creates stateful compute instances. If the instance crashes, needs scaling, or is replaced, all uploaded user photos would be permanently lost. By offloading media to Amazon S3, our EC2 compute layer remains stateless, durable, and easily scalable. Furthermore, S3 delivers built-in 99.999999999% (11 9's) data durability."*

### Question 2: "How is your Amazon RDS database protected from unauthorized internet access?"
- **Answer:**  
  *"We deployed our RDS PostgreSQL instance with 'Public Access: No' in a private DB subnet. Its security group, `CampusFind-RDS-SG`, contains a single inbound rule allowing TCP port 5432 strictly from the source security group `CampusFind-EC2-SG`. This means even if someone knows the RDS endpoint, only our EC2 web server can establish a connection."*

### Question 3: "How does your system prevent SQL Injection and Cross-Site Scripting (XSS)?"
- **Answer:**  
  *"Django's ORM parameterizes all database queries by default, ensuring user inputs are treated strictly as literal values rather than executable SQL. For XSS, Django templates automatically escape all HTML variables unless explicitly marked safe. In addition, all state-changing POST forms enforce CSRF tokens via `CsrfViewMiddleware`."*

### Question 4: "What happens if AWS credentials or S3 buckets are not configured in local development?"
- **Answer:**  
  *"We implemented conditional storage switching in `campusfind/settings.py`. When `USE_S3=False` in `.env`, Django falls back immediately to local file storage under `MEDIA_ROOT`. This ensures zero-configuration offline execution and seamless automated testing without needing live AWS credentials."*

---

## 🚀 How to Present or Export the Slide Deck

1. **Launch the Presentation:**  
   Open [`presentation.html`](file:///home/hackura/campusfind/presentation.html) in Google Chrome, Mozilla Firefox, or Microsoft Edge.
2. **Keyboard Shortcuts:**
   - <kbd>Space</kbd> or <kbd>→</kbd>: Next Slide
   - <kbd>←</kbd> or <kbd>Backspace</kbd>: Previous Slide
   - <kbd>N</kbd>: Toggle Presenter Notes Drawer (shows exact speaking scripts)
   - <kbd>O</kbd> or <kbd>Esc</kbd>: Toggle Slide Overview Grid
   - <kbd>F</kbd>: Toggle Fullscreen Mode
   - <kbd>T</kbd>: Start / Pause 20-minute Presentation Timer
   - <kbd>P</kbd> or <kbd>Ctrl+P</kbd>: Export / Print All Slides to PDF
