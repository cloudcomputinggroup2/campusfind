# Capstone Deliverable 6: Final Technical Report

# CampusFind: A Cloud-Based Campus Lost & Found System
**Course:** CSBC 252 - Introduction to Cloud Computing  
**Semester Group Project / Capstone Technical Report**  
**Date:** August 2026  

---

## 1. Executive Summary / Abstract
In large university environments, personal property loss represents a pervasive logistical challenge. Millions of items ranging from official student ID cards to laptops and textbooks are misplaced annually, often ending up lost permanently due to decentralized communication. 

**CampusFind** is a modern, cloud-architected lost and found platform engineered to streamline report submission, catalog discovery, item verification, and owner reconnection. Built using Python, Django 5, and Bootstrap 5, the system leverages Amazon Web Services (AWS) Free Tier resources—including Amazon EC2 for compute hosting, Amazon RDS for relational persistence, Amazon S3 for secure media asset storage, AWS IAM for least-privilege governance, and Amazon CloudWatch for telemetry monitoring. 

This report documents the end-to-end development lifecycle, database normalization, cloud deployment architecture, security hardening, and validation test results.

---

## 2. Problem Statement
Traditional methods for tracking lost property on campus (such as informal group chats, bulletin boards, and manual lost-and-found desk logs) suffer from several critical shortcomings:
1. **Lack of Centralized Indexing:** Students must check multiple campus locations or chat channels.
2. **Absence of Real-Time Search & Filtering:** Finding a specific item (e.g. by building, category, or date) is nearly impossible in chat streams.
3. **No Lifecycle Verification:** Records are rarely updated when items are returned, cluttering notice boards with obsolete inquiries.
4. **Security Vulnerabilities:** Contact details and personal identities are exposed indiscriminately across social media groups.

---

## 3. Project Objectives
- **Centralized Cloud Platform:** Build and deploy a high-availability web service accessible across all student and faculty devices.
- **Full CRUD Functionality:** Deliver intuitive workflows for creating, reading, updating, and deleting lost/found listings.
- **Decoupled Cloud Storage:** Isolate image uploads from compute storage by utilizing Amazon S3.
- **Relational Cloud Persistence:** Store structured user profiles and item records on Amazon RDS PostgreSQL.
- **Security & Least-Privilege Architecture:** Implement environment variables, cryptographic password hashing, and tailored AWS Security Groups.
- **Automated Quality Assurance:** Implement unit tests, health check endpoints, and CloudWatch metrics monitoring.

---

## 4. Scope and Limitations

### In Scope:
- User registration, authentication, and session handling.
- Lost and found item posting with multi-attribute tags (category, location, date, description, contact, image).
- Search and filtering engine (keyword, category, status, campus location, date).
- Item detail views with contact integration and printable notice flyer generation.
- Owner and moderator item lifecycle management (marking posts as Claimed / Reunited).
- Automated AWS deployment scripts for Ubuntu Linux EC2 instances.

### Out of Scope:
- Real-time peer-to-peer chat system (direct phone/email/desk contact used instead).
- Monetary reward payment processing.
- Native iOS/Android mobile applications (responsive mobile-web interface used).
- Complex machine learning image recognition (basic category indexing used).

---

## 5. System Requirements
- **Backend Environment:** Python 3.12+, Django 5.0+
- **Database Engine:** PostgreSQL 15+ / MySQL 8.0 (Amazon RDS) or SQLite (Local Dev)
- **Object Storage:** Amazon Simple Storage Service (Amazon S3) with `boto3` & `django-storages`
- **Web & WSGI Servers:** Nginx 1.24+ & Gunicorn 21+
- **Operating System:** Ubuntu Server 22.04 / 24.04 LTS (Amazon EC2)

---

## 6. System Design & Architecture

### 6.1 Database Schema (ERD)
The database structure is designed for Third Normal Form (3NF) compliance:
- **`auth_user`:** Stores authentication records, salted password hashes, and staff permissions.
- **`core_item`:** Contains item attributes, campus building designations, foreign key association to `auth_user`, S3 image URLs, and resolution timestamps.

### 6.2 AWS Cloud Architecture
The system employs a multi-tier cloud architecture within an Amazon VPC:
1. **Public Web Layer:** Amazon EC2 instance hosting Nginx and Gunicorn. Inbound traffic is governed by `CampusFind-EC2-SG` (Ports 80, 443, 22).
2. **Private Database Layer:** Amazon RDS PostgreSQL instance. Inbound traffic is strictly restricted by `CampusFind-RDS-SG` (Port 5432) to requests originating from `CampusFind-EC2-SG`.
3. **Storage & IAM Layer:** Amazon S3 bucket for item photographs governed by a least-privilege IAM policy.
4. **Monitoring Layer:** Amazon CloudWatch tracking EC2 CPU utilization, network traffic, and `/health/` JSON status.

---

## 7. Implementation Details

### 7.1 Backend Modules (`core` app):
- **`models.py`:** Defines the `Item` model with custom methods (`mark_as_claimed`, `is_owner`, `status_badge_class`).
- **`forms.py`:** Implements `ItemForm` with image format checking and 5MB size limit validation, plus `UserRegistrationForm`.
- **`views.py`:** Handles item catalog browsing, multi-parameter filtering, CRUD actions, ownership authorization, printable flyer generation, and cloud health monitoring.
- **`context_processors.py`:** Dynamically feeds live campus metrics and category definitions to all presentation templates.

### 7.2 Frontend Experience:
- **Responsive Design System:** Built with Bootstrap 5.3 and custom CSS tokens (`styles.css`).
- **Dynamic Interaction:** Pure JavaScript (`main.js`) powers instant client-side photo previews, one-click clipboard copying, and alert dismissals.
- **Campus Notice Flyer:** Print-optimized view (`print_notice.html`) formatted with tear-off contact slips for physical boards.

---

## 8. Security Configuration & Governance
- **Zero Secrets in Code:** Stored in `.env` and loaded at runtime via `python-dotenv`.
- **Password Security:** Salted PBKDF2 SHA-256 password hashing.
- **Injection Protection:** Django ORM parameterized queries prevent SQL injection.
- **Cross-Site Defenses:** Built-in CSRF token protection on all state-altering forms and XSS output escaping.
- **S3 IAM Scoping:** S3 bucket permissions limited exclusively to object creation, retrieval, and listing on the designated bucket ARN.

---

## 9. Testing & Validation Results

| Test Suite | Total Tests | Passed | Failed |
| :--- | :--- | :--- | :--- |
| Model Creation & Ownership Logic | 3 | 3 | 0 |
| Views, Search & Filtering | 2 | 2 | 0 |
| Authentication & CRUD Permissions | 2 | 2 | 0 |
| S3 Storage Integration & Health Check | 2 | 2 | 0 |
| **Total Automated Suite** | **9** | **9** | **0** |

All tests completed successfully with zero regression.

---

## 10. Challenges Encountered & Solutions
1. **WhiteNoise Static Manifest during Testing:**  
   *Challenge:* Enforcing hashed static manifests caused `ValueError` during automated test runs without prior static collection.  
   *Solution:* Configured `whitenoise.storage.CompressedStaticFilesStorage` to maintain high compression while eliminating manifest strictness during test iterations.
2. **Decoupled Local & S3 Storage:**  
   *Challenge:* Ensuring team members could develop offline without live AWS credentials.  
   *Solution:* Implemented conditional storage backend switching based on the `USE_S3` environment variable in `settings.py`.

---

## 11. Future Enhancements
- **Automated Matching Engine:** Email notification system alerting users when a newly posted found item closely matches a reported lost item's keywords and category.
- **QR Code Tags:** Generatable QR code stickers that students can affix to laptops and water bottles for instant reporting when found.
- **Multi-AZ High Availability:** Adding an Application Load Balancer (ALB) across multiple EC2 instances in different Availability Zones for increased fault tolerance.

---

## 12. Conclusion
The **CampusFind** Capstone Project successfully fulfills all academic and functional requirements outlined in the CSBC 252 curriculum. By coupling an intuitive Django web application with AWS cloud services (EC2, RDS, S3, IAM, CloudWatch), the system delivers a production-grade, secure, and resilient solution for campus lost and found management.
