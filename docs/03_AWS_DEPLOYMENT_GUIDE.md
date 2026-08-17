# Capstone Deliverable 3: AWS Architecture & Deployment Guide

This guide provides step-by-step instructions for deploying CampusFind to **AWS Free Tier** services (**EC2**, **RDS**, **S3**, **IAM**, **Security Groups**, and **CloudWatch**).

---

## Step 1: Configure AWS Security Groups

Create two security groups in your AWS VPC:

### 1. `CampusFind-EC2-SG` (Web Server Security Group)
| Type | Protocol | Port Range | Source | Description |
| :--- | :--- | :--- | :--- | :--- |
| **HTTP** | TCP | 80 | `0.0.0.0/0` | Public web traffic |
| **HTTPS** | TCP | 443 | `0.0.0.0/0` | Secure web traffic (Optional SSL) |
| **SSH** | TCP | 22 | `Your-IP/32` | Administrative SSH access from your IP |

### 2. `CampusFind-RDS-SG` (Database Security Group)
| Type | Protocol | Port Range | Source | Description |
| :--- | :--- | :--- | :--- | :--- |
| **PostgreSQL / MySQL** | TCP | 5432 / 3306 | `CampusFind-EC2-SG` (Security Group ID) | Inbound database traffic **only** from the EC2 web server |

---

## Step 2: Create Amazon RDS Database Instance

1. Navigate to the **Amazon RDS** Console -> Click **Create database**.
2. **Engine:** Select **PostgreSQL** (or MySQL) -> Choose **Free tier** template.
3. **DB instance identifier:** `campusfind-db`
4. **Master username:** `campusadmin`
5. **Master password:** Create a secure password (e.g., `CampusFindSecure2026!`).
6. **DB instance class:** `db.t3.micro` or `db.t4g.micro` (Free Tier).
7. **Storage:** 20 GiB gp2/gp3.
8. **Connectivity:**
   - VPC: Default VPC
   - Public access: **No** (Security best practice).
   - VPC security group: Choose `CampusFind-RDS-SG`.
9. **Additional configuration:**
   - Initial database name: `campusfind_db`
10. Click **Create database**. Note down the database **Endpoint** once created.

---

## Step 3: Create Amazon S3 Bucket for Media Storage

1. Navigate to the **Amazon S3** Console -> Click **Create bucket**.
2. **Bucket name:** `campusfind-item-images-capstone` (must be globally unique).
3. **Region:** `us-east-1` (same region as EC2/RDS).
4. **Block Public Access settings:**
   - Keep "Block *all* public access" checked, OR configure bucket policy for read-only object access if serving directly.
5. Click **Create bucket**.

### Create IAM Policy & User / Role for S3:
1. Navigate to **IAM** -> **Policies** -> **Create policy**.
2. Paste the policy from [`deploy/iam_policy.json`](file:///home/oxcyron/Desktop/capstone/deploy/iam_policy.json):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:PutObjectAcl"],
      "Resource": "arn:aws:s3:::campusfind-item-images-capstone/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
      "Resource": "arn:aws:s3:::campusfind-item-images-capstone"
    }
  ]
}
```
3. Attach this policy to an IAM Role assigned to your EC2 instance (or create an IAM User with Access Key & Secret Key).

---

## Step 4: Launch and Provision the Amazon EC2 Instance

1. Navigate to **Amazon EC2** -> Click **Launch Instance**.
2. **Name:** `CampusFind-WebServer`
3. **OS Image:** Ubuntu Server 24.04 LTS (HVM), SSD Volume Type.
4. **Instance Type:** `t2.micro` or `t3.micro` (Free Tier eligible).
5. **Key pair:** Create or select your `.pem` key pair for SSH access.
6. **Network settings:** Select `CampusFind-EC2-SG`.
7. **Storage:** 8-15 GiB gp3.
8. Click **Launch Instance**.

---

## Step 5: SSH into EC2 and Deploy Application

Connect to your EC2 instance via SSH:
```bash
ssh -i /path/to/your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

Clone the repository and run the automated setup script:
```bash
# Clone the project code
git clone https://github.com/your-username/campusfind.git /home/ubuntu/campusfind
cd /home/ubuntu/campusfind

# Make setup script executable and run
chmod +x deploy/ec2_setup.sh
./deploy/ec2_setup.sh
```

---

## Step 6: Configure Environment Variables (`.env`)

Edit `/home/ubuntu/campusfind/.env`:
```bash
nano /home/ubuntu/campusfind/.env
```

Set your production parameters:
```ini
SECRET_KEY=generate-a-strong-random-50-character-key
DEBUG=False
ALLOWED_HOSTS=<EC2-PUBLIC-IP>,<EC2-PUBLIC-DNS>,localhost

# Amazon RDS PostgreSQL Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=campusfind_db
DB_USER=campusadmin
DB_PASSWORD=CampusFindSecure2026!
DB_HOST=campusfind-db.cxxxxxxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432

# Amazon S3 Storage Configuration
USE_S3=True
AWS_ACCESS_KEY_ID=YOUR_IAM_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_IAM_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME=campusfind-item-images-capstone
AWS_S3_REGION_NAME=us-east-1
```

Restart services to apply settings:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## Step 7: CloudWatch Monitoring & Metrics Verification

1. Navigate to **Amazon CloudWatch** Console -> **Metrics** -> **EC2**.
2. Select your instance `CampusFind-WebServer` and monitor:
   - `CPUUtilization` (%)
   - `NetworkIn` & `NetworkOut` (Bytes)
   - `StatusCheckFailed_Instance`
3. Check the application health JSON endpoint in your browser:
   `http://<EC2-PUBLIC-IP>/health/`
4. Capture screenshots of CloudWatch dashboard and public browser page for the Capstone Proof Portfolio.
