# Capstone Deliverable 5: Video Presentation Script & Slides Outline

**Course:** CSBC 252 - Introduction to Cloud Computing  
**Project:** CampusFind: A Cloud-Based Campus Lost & Found System  
**Estimated Duration:** 15 – 20 Minutes  

---

## Group Roles & Presentation Structure

| Section | Topic | Speaker Role | Allocated Time |
| :--- | :--- | :--- | :--- |
| **1** | Project Introduction & Problem Statement | **Team Lead / PM** | 0:00 – 2:30 (2.5 mins) |
| **2** | Live Demonstration of Web Application | **Frontend / Fullstack Dev** | 2:30 – 7:30 (5.0 mins) |
| **3** | AWS Cloud Architecture & Infrastructure | **Cloud Architect** | 7:30 – 10:30 (3.0 mins) |
| **4** | Database Schema & RDS Integration | **Database Lead** | 10:30 – 12:30 (2.0 mins) |
| **5** | Security, S3 Image Storage & IAM | **Storage & Security Lead** | 12:30 – 15:00 (2.5 mins) |
| **6** | Testing, Validation & Conclusion | **QA / Documentation Lead** | 15:00 – 18:00 (3.0 mins) |

---

## Detailed Speaker Script

### Section 1: Introduction & Problem Statement (0:00 – 2:30)
> **Speaker (Team Lead):**  
> "Hello Professor and fellow students. Welcome to our Capstone presentation for CSBC 252: Introduction to Cloud Computing. Our project is **CampusFind: A Cloud-Based Campus Lost & Found System**.
>
> On any university campus, students and faculty lose valuable personal items every single day—ranging from student IDs and dorm keys to expensive laptops and textbooks. Traditionally, recovery efforts rely on fragmented WhatsApp group chats, physical bulletin boards, or word of mouth. This creates immense friction: there is no search functionality, no verification mechanism, and no way to know if an item has already been recovered.
>
> To solve this, our group engineered **CampusFind**—a centralized, cloud-native web application built using Django, Bootstrap, and deployed on Amazon Web Services using Free Tier resources: Amazon EC2, Amazon RDS, Amazon S3, IAM, and CloudWatch. Today, we are going to walk you through our live platform, our cloud architecture, security design, and how each component operates."

---

### Section 2: Live Demonstration of CampusFind (2:30 – 7:30)
> **Speaker (Frontend / Fullstack Dev):**  
> "Thank you. Let us now look at the live deployed application.
>
> *(Screen Share: Browser open to homepage)*  
>
> 1. **Homepage & Metrics:** Here on the homepage, students are greeted with real-time statistics—showing total items reported, active lost items, found items waiting, and reunited items. We also have a live search bar and category chips.
> 2. **User Registration & Login:** Let us log in as student Alex. Password authentication is handled securely with salted password hashing.
> 3. **Reporting a Lost Item:** Clicking **'Report Item'** opens our form. Notice how we can select the category, campus building presets, date, description, contact information, and upload an image with instant client-side preview.
> 4. **Item Directory & Filtering:** On the **'Browse Items'** page, we can switch between a modern card grid and a table layout. We can filter in real time by category (such as Electronics or Student IDs) and status (Lost vs Found).
> 5. **Item Details & Physical Print Notice:** Clicking into an item opens the detailed card with contact links and campus recovery safety tips. For physical bulletin boards, we built a one-click **'Print Notice Flyer'** feature complete with tear-off contact slips.
> 6. **Owner Lifecycle & Claiming:** From **'My Posts'**, the owner can easily edit, delete, or click **'Mark as Claimed / Reunited'** once the item is back in safe hands."

---

### Section 3: AWS Cloud Architecture (7:30 – 10:30)
> **Speaker (Cloud Architect):**  
> "Now let us examine the AWS cloud infrastructure supporting CampusFind.
>
> *(Screen Share: AWS Architecture Diagram & EC2 Console)*  
>
> - **Compute (Amazon EC2):** Our application runs on an Ubuntu 24.04 EC2 instance (t2.micro). We configured **Nginx** as a high-performance reverse proxy that handles Gzip compression and static caching, forwarding dynamic requests to **Gunicorn** WSGI workers.
> - **Security Groups:** We enforce strict least-privilege networking. `CampusFind-EC2-SG` allows public HTTP on port 80 and HTTPS on port 443, while restricting SSH (port 22) exclusively to trusted IP addresses.
> - **Service Management:** The application runs as a resilient `systemd` daemon, ensuring automatic restart upon server reboot."

---

### Section 4: Database Schema & Amazon RDS (10:30 – 12:30)
> **Speaker (Database Lead):**  
> "Let's explore our data layer.
>
> *(Screen Share: ERD Diagram & RDS Console)*  
>
> - **Managed Relational Database:** We host our PostgreSQL database on **Amazon RDS**. The RDS instance is placed in a private subnet, with its security group (`CampusFind-RDS-SG`) configured to accept inbound traffic on port 5432 **only** from our EC2 security group.
> - **Data Normalization:** Our schema cleanly decouples `auth_user` accounts from `core_item` listings with cascading foreign keys, indexing frequently queried fields like `status` and `category` for low-latency queries."

---

### Section 5: Security, Amazon S3 & IAM (12:30 – 15:00)
> **Speaker (Storage & Security Lead):**  
> "Storage separation and security were core priorities for this project.
>
> *(Screen Share: S3 Bucket & IAM Policy JSON)*  
>
> - **Decoupled Object Storage (Amazon S3):** Uploaded item photos are not stored on local EC2 disk storage. Instead, they are uploaded directly to our dedicated S3 bucket (`campusfind-item-images-capstone`) using `boto3` and `django-storages`.
> - **Least-Privilege IAM Policy:** We authored a custom IAM policy granting only `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, and `s3:ListBucket` on the specific bucket ARN.
> - **Zero Hardcoded Secrets:** All credentials, database hosts, and secret keys are injected at runtime via `.env` environment variables."

---

### Section 6: Testing, CloudWatch & Conclusion (15:00 – 18:00)
> **Speaker (QA & Documentation Lead):**  
> "To ensure enterprise reliability, we implemented comprehensive automated and cloud testing.
>
> *(Screen Share: Terminal test output & CloudWatch Graphs)*  
>
> - **Automated Test Suite:** Running `python manage.py test` executes 9 automated unit and integration tests covering user authentication, CRUD operations, permission checks, search filtering, and health endpoints.
> - **CloudWatch & Health Monitoring:** We configured a `/health/` JSON endpoint that tests database connectivity. In Amazon CloudWatch, we monitor CPU utilization and network traffic.
> - **Challenges & Lessons:** During development, we resolved static file manifest handling for WhiteNoise and engineered graceful S3 fallback for offline development.
> - **Future Work:** Future milestones include email notifications for matching items and QR-code tag scanning.
>
> Thank you for your time. We are now open for questions!"
