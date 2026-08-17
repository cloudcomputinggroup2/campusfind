# Capstone Deliverable 4: Security & Testing Plan

## 1. Cloud & Application Security Plan

| Security Concern | Mitigation Strategy | Implementation Details |
| :--- | :--- | :--- |
| **Credential Management** | Zero hardcoded secrets | All database credentials, Django secret keys, and AWS access keys are loaded dynamically through `.env` using `python-dotenv`. |
| **Database Isolation** | Network isolation | Amazon RDS database resides in a private subnet with `CampusFind-RDS-SG`, which accepts inbound traffic on port 5432 **only** from the EC2 security group. |
| **Password Storage** | Cryptographic hashing | Utilizes Django's PBKDF2 algorithm with SHA-256 hash and unique per-user salt. |
| **Storage Security** | Least-privilege IAM policy | S3 credentials or EC2 instance profile only have `PutObject`, `GetObject`, `DeleteObject`, and `ListBucket` permissions scoped specifically to the item image bucket. |
| **File Upload Validation** | Size and MIME checking | Restricts uploaded files to valid image extensions (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`) and enforces a maximum file size of **5 MB**. |
| **Web Vulnerabilities** | Built-in framework defenses | Protection against SQL Injection (via ORM parameterization), Cross-Site Scripting (XSS auto-escaping in templates), and CSRF (via `CsrfViewMiddleware` and tokens on all POST requests). |
| **Production Hardening** | Debug mode off | `DEBUG=False` in production to prevent traceback leaks, with Whitenoise serving compressed assets. |

---

## 2. Functional Testing Plan & Test Cases

| Test ID | Test Scenario | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | User Registration | Submit registration form with valid campus credentials | User account is created and automatically authenticated | **PASS** |
| **TC-02** | User Login & Logout | Log in with registered credentials and log out | Successful session creation and destruction | **PASS** |
| **TC-03** | Create Lost Item Post | Fill in lost item form with title, category, campus location | Item is persisted and displayed on home and catalog pages | **PASS** |
| **TC-04** | Create Found Item Post | Fill in found item form with photo and contact info | Item is saved and image URL is correctly linked | **PASS** |
| **TC-05** | Image Upload Validation | Attempt to upload a non-image file or >5MB file | Form rejects upload with descriptive error message | **PASS** |
| **TC-06** | Catalog Search & Filter | Filter by keyword "MacBook", category, or status | Matching records returned with accurate count | **PASS** |
| **TC-07** | Ownership Edit Control | Attempt to edit another user's post as a normal student | Request redirected / forbidden; only owner or staff permitted | **PASS** |
| **TC-08** | Mark as Claimed/Resolved | Creator or moderator toggles status to "Claimed" | Item status changes to Claimed and resolution timestamp saved | **PASS** |
| **TC-09** | Cloud Health Check | Send HTTP GET request to `/health/` | Returns HTTP 200 with JSON payload `{"status": "healthy"}` | **PASS** |

---

## 3. Automated Test Suite Execution Output

Run tests with:
```bash
python manage.py test
```

### Execution Log:
```text
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 31.631s

OK
Destroying test database for alias 'default'...
```

---

## 4. Cloud Validation Proof Portfolio Checklist

When compiling the final presentation and report, capture screenshots of the following AWS console pages:

1. **Amazon EC2:** Instance state showing `CampusFind-WebServer` in `running` status with Public IPv4 address.
2. **Amazon RDS:** Database details showing `campusfind-db` in `Available` state with PostgreSQL/MySQL engine.
3. **Amazon S3:** Bucket contents view for `campusfind-item-images-capstone` displaying uploaded `.png`/`.jpg` item photos.
4. **AWS IAM:** IAM Policy `CampusFindS3ObjectAccess` attached to role/user.
5. **Security Groups:** Inbound rule table for `CampusFind-EC2-SG` (Port 80/443) and `CampusFind-RDS-SG` (Port 5432 from EC2).
6. **Amazon CloudWatch:** Dashboard showing EC2 `CPUUtilization` and network throughput metrics graphs.
7. **Working Web Application:** Browser screenshot showing public URL, homepage statistics, item listings, and printable notice.
