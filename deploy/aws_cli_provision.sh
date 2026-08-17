#!/bin/bash
# ==============================================================================
# CampusFind - Automated AWS CLI Infrastructure Provisioning Script
# Course: CSBC 252 - Introduction to Cloud Computing
# Provisions: VPC Security Groups, Amazon RDS PostgreSQL, Amazon S3, IAM, & EC2
# ==============================================================================

set -e

REGION="us-east-1"
DB_NAME="campusfind_db"
DB_USER="campusfind_admin"
DB_PASSWORD="CampusFindPass2026!"
BUCKET_NAME="campusfind-item-images-capstone-$((1000 + RANDOM % 9000))"
KEY_PAIR_NAME="campusfind-key"

echo "============================================================"
echo "🚀 CampusFind: Starting AWS CLI Infrastructure Provisioning"
echo "Region: $REGION"
echo "============================================================"

# 1. Check AWS CLI Authentication
echo -e "\n🔍 Step 1: Checking AWS CLI identity..."
CALLER_IDENTITY=$(aws sts get-caller-identity --output json)
echo "Authenticated as: $(echo $CALLER_IDENTITY | grep -o '"Arn": "[^"]*' | cut -d'"' -f4)"

# 2. Get Default VPC & Subnets
echo -e "\n🌐 Step 2: Fetching Default VPC and Subnets..."
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --region $REGION --query "Vpcs[0].VpcId" --output text)
echo "Default VPC ID: $VPC_ID"

SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --region $REGION --query "Subnets[*].SubnetId" --output text)
SUBNET_1=$(echo $SUBNET_IDS | awk '{print $1}')
SUBNET_2=$(echo $SUBNET_IDS | awk '{print $2}')
echo "Using Subnets: $SUBNET_1, $SUBNET_2"

# 3. Create Security Groups
echo -e "\n🔒 Step 3: Creating Security Groups..."

# EC2 Security Group
EC2_SG_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=CampusFind-EC2-SG" "Name=vpc-id,Values=$VPC_ID" --region $REGION --query "SecurityGroups[0].GroupId" --output text 2>/dev/null || echo "None")
if [ "$EC2_SG_ID" == "None" ] || [ -z "$EC2_SG_ID" ]; then
    EC2_SG_ID=$(aws ec2 create-security-group --group-name "CampusFind-EC2-SG" --description "Security Group for CampusFind EC2 Web Application" --vpc-id $VPC_ID --region $REGION --query "GroupId" --output text)
    echo "Created EC2 Security Group: $EC2_SG_ID"
    # Authorize HTTP, HTTPS, SSH
    aws ec2 authorize-security-group-ingress --group-id $EC2_SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0 --region $REGION
    aws ec2 authorize-security-group-ingress --group-id $EC2_SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0 --region $REGION
    aws ec2 authorize-security-group-ingress --group-id $EC2_SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $REGION
    echo "Authorized Ports 80, 443, 22 on $EC2_SG_ID"
else
    echo "Using existing EC2 Security Group: $EC2_SG_ID"
fi

# RDS Security Group
RDS_SG_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=CampusFind-RDS-SG" "Name=vpc-id,Values=$VPC_ID" --region $REGION --query "SecurityGroups[0].GroupId" --output text 2>/dev/null || echo "None")
if [ "$RDS_SG_ID" == "None" ] || [ -z "$RDS_SG_ID" ]; then
    RDS_SG_ID=$(aws ec2 create-security-group --group-name "CampusFind-RDS-SG" --description "Security Group for CampusFind RDS PostgreSQL Database" --vpc-id $VPC_ID --region $REGION --query "GroupId" --output text)
    echo "Created RDS Security Group: $RDS_SG_ID"
    # Authorize Port 5432 strictly from EC2 SG
    aws ec2 authorize-security-group-ingress --group-id $RDS_SG_ID --protocol tcp --port 5432 --source-group $EC2_SG_ID --region $REGION
    echo "Authorized Port 5432 strictly from EC2 SG ($EC2_SG_ID) on $RDS_SG_ID"
else
    echo "Using existing RDS Security Group: $RDS_SG_ID"
fi

# 4. Create Amazon S3 Bucket & IAM Access
echo -e "\n📦 Step 4: Creating Amazon S3 Bucket ($BUCKET_NAME)..."
if [ "$REGION" == "us-east-1" ]; then
    aws s3api create-bucket --bucket $BUCKET_NAME --region $REGION
else
    aws s3api create-bucket --bucket $BUCKET_NAME --region $REGION --create-bucket-configuration LocationConstraint=$REGION
fi
echo "Created S3 Bucket: $BUCKET_NAME"

# Create IAM Policy for S3
IAM_USER="campusfind-s3-app-user"
echo "Creating IAM User: $IAM_USER..."
aws iam create-user --user-name $IAM_USER 2>/dev/null || echo "User $IAM_USER already exists"

# Generate Policy JSON
cat <<EOF > /tmp/s3_policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CampusFindS3Access",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::$BUCKET_NAME",
                "arn:aws:s3:::$BUCKET_NAME/*"
            ]
        }
    ]
}
EOF

aws iam put-user-policy --user-name $IAM_USER --policy-name "CampusFindS3Policy" --policy-document file:///tmp/s3_policy.json
echo "Attached Least-Privilege S3 Policy to $IAM_USER"

# Create Access Keys
ACCESS_KEYS_JSON=$(aws iam create-access-key --user-name $IAM_USER --output json 2>/dev/null || echo "EXISTS")
if [ "$ACCESS_KEYS_JSON" != "EXISTS" ]; then
    AWS_KEY_ID=$(echo $ACCESS_KEYS_JSON | grep -o '"AccessKeyId": "[^"]*' | cut -d'"' -f4)
    AWS_SECRET_KEY=$(echo $ACCESS_KEYS_JSON | grep -o '"SecretAccessKey": "[^"]*' | cut -d'"' -f4)
    echo "Generated new IAM Access Keys for $IAM_USER"
else
    echo "⚠️ Note: IAM access keys already exist for $IAM_USER. Retrieve from your credentials or AWS Console."
    AWS_KEY_ID="<YOUR-IAM-ACCESS-KEY-ID>"
    AWS_SECRET_KEY="<YOUR-IAM-SECRET-ACCESS-KEY>"
fi

# 5. Create RDS DB Subnet Group and PostgreSQL Database
echo -e "\n🗄️ Step 5: Provisioning Amazon RDS PostgreSQL Database (db.t3.micro)..."
DB_SUBNET_GROUP="campusfind-db-subnet-group"
aws rds create-db-subnet-group \
    --db-subnet-group-name $DB_SUBNET_GROUP \
    --db-subnet-group-description "Subnet group for CampusFind RDS" \
    --subnet-ids $SUBNET_1 $SUBNET_2 \
    --region $REGION 2>/dev/null || echo "Subnet group $DB_SUBNET_GROUP already exists"

DB_INSTANCE_ID="campusfind-postgres-db"
echo "Creating RDS Instance ($DB_INSTANCE_ID)..."
aws rds create-db-instance \
    --db-instance-identifier $DB_INSTANCE_ID \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.7 \
    --master-username $DB_USER \
    --master-user-password $DB_PASSWORD \
    --allocated-storage 20 \
    --db-name $DB_NAME \
    --vpc-security-group-ids $RDS_SG_ID \
    --db-subnet-group-name $DB_SUBNET_GROUP \
    --no-publicly-accessible \
    --backup-retention-period 1 \
    --region $REGION 2>/dev/null || echo "RDS Instance $DB_INSTANCE_ID is already creating or exists"

echo "⏳ RDS database creation triggered. It takes ~5-8 minutes to become available."

# 6. Create EC2 Key Pair (if not exists)
echo -e "\n🔑 Step 6: Checking EC2 SSH Key Pair..."
if [ ! -f "$KEY_PAIR_NAME.pem" ]; then
    aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --query "KeyMaterial" --output text --region $REGION > $KEY_PAIR_NAME.pem 2>/dev/null || echo "Key pair $KEY_PAIR_NAME already exists in AWS"
    chmod 400 $KEY_PAIR_NAME.pem 2>/dev/null || true
    echo "Saved SSH key pair to: $(pwd)/$KEY_PAIR_NAME.pem"
fi

# 7. Summary & Ready-to-Use .env Configuration
echo -e "\n============================================================"
echo "🎉 AWS INFRASTRUCTURE PROVISIONING INITIALIZED!"
echo "============================================================"
echo "VPC ID:                 $VPC_ID"
echo "EC2 Security Group:     $EC2_SG_ID (Ports 80, 443, 22)"
echo "RDS Security Group:     $RDS_SG_ID (Port 5432 from EC2 SG)"
echo "S3 Bucket Name:         $BUCKET_NAME"
echo "IAM User:               $IAM_USER"
echo "RDS Instance ID:        $DB_INSTANCE_ID"
echo "============================================================"
echo "To check RDS status and get endpoint:"
echo "aws rds describe-db-instances --db-instance-identifier $DB_INSTANCE_ID --region $REGION --query 'DBInstances[0].Endpoint.Address' --output text"
echo "============================================================"
