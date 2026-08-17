#!/bin/bash
# ==============================================================================
# CampusFind AWS EC2 Automated Provisioning Script
# Target OS: Ubuntu 22.04 / 24.04 LTS on AWS Free Tier (t2.micro / t3.micro)
# Course: CSBC 252 - Introduction to Cloud Computing
# ==============================================================================

set -e

echo "=========================================="
echo "Starting CampusFind EC2 Deployment Setup..."
echo "=========================================="

# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install essential build tools, Python, Nginx, and Git
sudo apt install -y python3 python3-pip python3-venv git nginx libpq-dev curl

# 3. Create project directory if not already inside repo
APP_DIR="/home/ubuntu/campusfind"
if [ ! -d "$APP_DIR" ]; then
    echo "Creating application directory at $APP_DIR..."
    mkdir -p "$APP_DIR"
fi

cd "$APP_DIR"

# 4. Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
echo "Installing project dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 6. Check .env file
if [ ! -f ".env" ]; then
    echo "Generating .env from .env.example..."
    cp .env.example .env
    echo "IMPORTANT: Edit .env to supply your Amazon RDS and S3 credentials!"
fi

# 7. Run database migrations & static files
echo "Running migrations and static collection..."
python manage.py migrate
python manage.py collectstatic --noinput

# 8. Seed sample data
echo "Seeding sample database records..."
python manage.py seed_data

# 9. Configure Gunicorn systemd service
echo "Configuring Gunicorn systemd service..."
sudo cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 10. Configure Nginx reverse proxy
echo "Configuring Nginx reverse proxy..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/campusfind
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/campusfind /etc/nginx/sites-enabled/campusfind
sudo nginx -t
sudo systemctl restart nginx

# 11. Configure UFW Firewall (Allow SSH, HTTP, HTTPS)
echo "Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

echo "================================================================="
echo "CampusFind deployment complete!"
echo "Public access available at: http://$(curl -s http://checkip.amazonaws.com)"
echo "Health check endpoint: http://$(curl -s http://checkip.amazonaws.com)/health/"
echo "Admin panel: http://$(curl -s http://checkip.amazonaws.com)/admin/"
echo "================================================================="
