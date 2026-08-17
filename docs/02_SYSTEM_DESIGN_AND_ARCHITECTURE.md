# Capstone Deliverable 2: System Design & Architecture Document

## 1. System Overview & Use Cases

CampusFind is structured around distinct user roles: **Student / General User**, **Campus Moderator / Staff**, and **System Administrator**.

```mermaid
flowchart LR
    subgraph Users [Campus Actors]
        U[Student / User]
        M[Staff / Moderator]
        A[System Administrator]
    end

    subgraph UC [Use Cases]
        UC1[Register Account & Log In]
        UC2[Post Lost Item]
        UC3[Post Found Item]
        UC4[Upload Photo to Amazon S3]
        UC5[Search & Filter Catalog]
        UC6[Edit / Delete Own Posts]
        UC7[Mark Post as Claimed / Reunited]
        UC8[Print Physical Notice Flyer]
        UC9[Moderate Posts via Admin / Dashboard]
    end

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
    U --> UC6
    U --> UC7
    U --> UC8

    M --> UC5
    M --> UC7
    M --> UC9

    A --> UC1
    A --> UC7
    A --> UC9
```

### Key Use Cases:
1. **User Account Management:** Students create accounts with university credentials, login securely with hashed passwords, and view their dashboard.
2. **Item Reporting:** Users submit details for items lost or found, with category tagging, location selection, and optional image upload.
3. **Multi-Attribute Search & Discovery:** Users search by keyword, category, status (`Lost`, `Found`, `Claimed`), and campus building.
4. **Ownership & Lifecycle Verification:** Posters or staff mark items as `Claimed / Reunited` once returned to the rightful owner.
5. **Physical Campus Notice Generation:** Users can generate printable flyers with tear-off contact slips for physical bulletin boards.

---

## 2. Database Design & Entity Relationship Diagram (ERD)

The relational schema is implemented via the Django ORM and hosted on **Amazon RDS**.

```mermaid
erDiagram
    AUTH_USER ||--o{ CORE_ITEM : "creates / reports"
    
    AUTH_USER {
        int id PK
        string username "Unique campus username"
        string email "Campus email address"
        string password "PBKDF2/Argon2 password hash"
        string first_name "First name"
        string last_name "Last name"
        boolean is_staff "Staff / Moderator flag"
        boolean is_superuser "Admin flag"
        datetime date_joined "Account creation timestamp"
    }

    CORE_ITEM {
        int id PK
        int user_id FK "References auth_user.id"
        string title "Headline for the item"
        string category "Electronics, ID, Keys, Bags, etc."
        string status "LOST, FOUND, or CLAIMED"
        string location "Campus building or preset area"
        date date_event "Date lost or found"
        text description "Detailed physical identifiers"
        string contact "Contact phone, email, or desk"
        string image "S3 path / Media URL"
        boolean is_verified_returned "Lifecycle resolution flag"
        datetime resolved_at "Resolution timestamp"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last modified timestamp"
    }
```

### Table Specifications:
1. **`auth_user` Table:**
   - `id` (Primary Key, Integer)
   - `username` (VARCHAR(150), Unique)
   - `email` (VARCHAR(254), Indexed)
   - `password` (VARCHAR(128), Django PBKDF2 SHA-256 Hash)
   - `is_staff` / `is_superuser` (BOOLEAN)
   - `date_joined` (DATETIME)
2. **`core_item` Table:**
   - `id` (Primary Key, Integer)
   - `user_id` (Foreign Key -> `auth_user.id`, CASCADE on delete)
   - `title` (VARCHAR(200))
   - `category` (VARCHAR(50))
   - `status` (VARCHAR(20), Indexed)
   - `location` (VARCHAR(200))
   - `date_event` (DATE)
   - `description` (TEXT)
   - `contact` (VARCHAR(255))
   - `image` (VARCHAR(100), Stores Amazon S3 file key)
   - `is_verified_returned` (BOOLEAN, default False)
   - `resolved_at` (DATETIME, Nullable)
   - `created_at` / `updated_at` (DATETIME)

---

## 3. AWS Cloud Architecture Diagram

```mermaid
flowchart TB
    subgraph Internet [Public Internet]
        UserBrowser[Student Web Browsers / Devices]
    end

    subgraph AWSCloud [Amazon Web Services - Free Tier Region: us-east-1]
        
        subgraph VPC [Custom / Default VPC]
            
            subgraph PublicSubnet [Public Subnet]
                SG_EC2[Security Group: EC2-SG\nInbound: Port 80, 443, 22]
                
                subgraph EC2Instance [Amazon EC2 Instance - Ubuntu 24.04]
                    NginxWeb[Nginx Reverse Proxy]
                    GunicornWSGI[Gunicorn WSGI Server]
                    DjangoApp[Django 5 Web Application]
                    StaticWhiteNoise[WhiteNoise Static Storage]
                    
                    NginxWeb -->|HTTP 8000| GunicornWSGI
                    GunicornWSGI --> DjangoApp
                end
                
                SG_EC2 --- EC2Instance
            end

            subgraph PrivateSubnet [Private DB Subnet]
                SG_RDS[Security Group: RDS-SG\nInbound: Port 5432 ONLY from EC2-SG]
                RDS[(Amazon RDS\nPostgreSQL / MySQL)]
                
                SG_RDS --- RDS
            end
        end

        subgraph StorageLayer [AWS Storage & Identity]
            S3Bucket[(Amazon S3 Bucket\ncampusfind-item-images)]
            IAMRole[IAM Least-Privilege Role / Keys\ns3:PutObject, s3:GetObject]
            CloudWatch[Amazon CloudWatch\nEC2 Metrics & Health Logs]
        end
    end

    UserBrowser -->|HTTP Port 80| NginxWeb
    DjangoApp -->|Read / Write SQL| RDS
    DjangoApp -->|boto3 Image Uploads| S3Bucket
    IAMRole -.->|Authorizes| DjangoApp
    EC2Instance -.->|CPU / Network Telemetry| CloudWatch
```

### AWS Cloud Architecture Component Matrix:

| Layer | Component | AWS Service | Purpose & Configuration |
| :--- | :--- | :--- | :--- |
| **Presentation** | Web UI & Static Files | Nginx + WhiteNoise | Serves compressed CSS, JS, and HTML templates over HTTP/HTTPS |
| **Application** | Web Framework | Amazon EC2 (Ubuntu 24.04) | Hosts Django core logic, authentication, CRUD, and pagination |
| **Database** | Relational Data | Amazon RDS (PostgreSQL/MySQL) | Stores `auth_user` accounts and `core_item` records |
| **Object Storage** | Media Assets | Amazon S3 | Secure bucket for uploaded photos of lost/found items |
| **Security** | IAM & Security Groups | AWS IAM + EC2/RDS SGs | Restricts RDS inbound access strictly to EC2 SG; least privilege S3 policy |
| **Monitoring** | Observability | Amazon CloudWatch | Captures EC2 CPU utilization, network I/O, and health check alerts |
