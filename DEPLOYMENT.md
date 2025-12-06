# Deployment Guide

This guide covers deploying the User Profile Microservice to production environments.

## Prerequisites

- Docker & Docker Compose
- MySQL 8.0+ database
- Python 3.12+ (for local deployment)
- Domain name (for production)
- SSL/TLS certificates

## Deployment Options

1. **Docker Compose** (Recommended for small-scale)
2. **Kubernetes** (Recommended for large-scale)
3. **Traditional Server** (Linux with systemd)
4. **Cloud Platforms** (AWS, GCP, Azure)

---

## Option 1: Docker Compose Deployment

### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y
```

### Step 2: Clone and Configure

```bash
# Clone repository
git clone <your-repo-url>
cd cc-mvp

# Create production environment file
cp .env.example .env
```

### Step 3: Configure Environment

Edit `.env` for production:

```env
# Django Settings
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=user_profile_db
DB_USER=django_user
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=3306

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Service Configuration
SERVICE_NAME=user-profile-service
SERVICE_VERSION=1.0.0
DJANGO_LOG_LEVEL=WARNING
```

### Step 4: Generate Secret Key

```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 5: Update Docker Compose for Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: user_profile_db
    restart: always
    environment:
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - backend

  web:
    build: .
    container_name: user_profile_service
    restart: always
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 60 config.wsgi:application"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./logs:/app/logs
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - backend
      - frontend

  nginx:
    image: nginx:alpine
    container_name: nginx_proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web
    networks:
      - frontend

volumes:
  mysql_data:
  static_volume:
  media_volume:

networks:
  frontend:
  backend:
```

### Step 6: Configure Nginx

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        client_max_body_size 10M;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        # Health check endpoint
        location /health/ {
            proxy_pass http://django;
            access_log off;
        }
    }
}
```

### Step 7: Deploy

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

---

## Option 2: Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Helm (optional)

### Step 1: Create Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: user-profile-service
```

```bash
kubectl apply -f namespace.yaml
```

### Step 2: Create ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: django-config
  namespace: user-profile-service
data:
  ALLOWED_HOSTS: "yourdomain.com,www.yourdomain.com"
  DB_ENGINE: "django.db.backends.mysql"
  DB_NAME: "user_profile_db"
  DB_HOST: "mysql-service"
  DB_PORT: "3306"
  DEBUG: "False"
```

### Step 3: Create Secrets

```bash
kubectl create secret generic django-secrets \
  --from-literal=SECRET_KEY='your-secret-key' \
  --from-literal=DB_PASSWORD='your-db-password' \
  --namespace=user-profile-service
```

### Step 4: Deploy MySQL

```yaml
# mysql-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: user-profile-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: DB_PASSWORD
        - name: MYSQL_DATABASE
          value: user_profile_db
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  namespace: user-profile-service
spec:
  selector:
    app: mysql
  ports:
  - port: 3306
    targetPort: 3306
```

### Step 5: Deploy Django Application

```yaml
# django-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-app
  namespace: user-profile-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: django-app
  template:
    metadata:
      labels:
        app: django-app
    spec:
      containers:
      - name: django
        image: your-registry/user-profile-service:latest
        envFrom:
        - configMapRef:
            name: django-config
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: SECRET_KEY
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: django-secrets
              key: DB_PASSWORD
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: django-service
  namespace: user-profile-service
spec:
  selector:
    app: django-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## Option 3: Traditional Server Deployment

### Step 1: Install Dependencies

```bash
# Install Python 3.12
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12 python3.12-venv python3.12-dev -y

# Install MySQL
sudo apt install mysql-server -y

# Install Nginx
sudo apt install nginx -y
```

### Step 2: Setup Application

```bash
# Create application user
sudo useradd -m -s /bin/bash django

# Clone repository
sudo -u django git clone <repo-url> /home/django/app
cd /home/django/app

# Create virtual environment
sudo -u django python3.12 -m venv venv
sudo -u django venv/bin/pip install -r requirements.txt

# Configure environment
sudo -u django cp .env.example .env
sudo -u django nano .env
```

### Step 3: Configure Systemd Service

Create `/etc/systemd/system/user-profile-service.service`:

```ini
[Unit]
Description=User Profile Microservice
After=network.target mysql.service

[Service]
Type=notify
User=django
Group=django
WorkingDirectory=/home/django/app
Environment="PATH=/home/django/app/venv/bin"
ExecStart=/home/django/app/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/user-profile-service.sock \
    --timeout 60 \
    --access-logfile /var/log/user-profile-service/access.log \
    --error-logfile /var/log/user-profile-service/error.log \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/user-profile-service
sudo chown django:django /var/log/user-profile-service

# Enable and start service
sudo systemctl enable user-profile-service
sudo systemctl start user-profile-service
sudo systemctl status user-profile-service
```

---

## Post-Deployment Tasks

### 1. Database Migrations

```bash
python manage.py migrate
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Setup Monitoring

- Configure health check monitoring
- Set up log aggregation (ELK, Datadog, etc.)
- Configure alerts for errors

### 5. Setup Backups

```bash
# MySQL backup script
#!/bin/bash
mysqldump -u root -p user_profile_db > backup_$(date +%Y%m%d).sql
```

---

## Maintenance

### Updating the Application

```bash
# Pull latest code
git pull

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart user-profile-service
```

### Database Backup

```bash
# Backup
docker-compose exec db mysqldump -u root -p user_profile_db > backup.sql

# Restore
docker-compose exec -T db mysql -u root -p user_profile_db < backup.sql
```

### Monitoring Logs

```bash
# Docker
docker-compose logs -f web

# Systemd
journalctl -u user-profile-service -f

# Application logs
tail -f logs/django.log
```

---

## Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY generated
- [ ] ALLOWED_HOSTS configured
- [ ] SSL/TLS certificates installed
- [ ] Database credentials secured
- [ ] Firewall configured
- [ ] CORS origins restricted
- [ ] Rate limiting enabled
- [ ] Regular security updates
- [ ] Backup strategy implemented
- [ ] Log monitoring configured
- [ ] Health checks enabled

---

## Troubleshooting

### Application won't start

1. Check logs: `docker-compose logs web`
2. Verify environment variables
3. Check database connectivity
4. Ensure migrations are run

### Database connection errors

1. Verify MySQL is running
2. Check credentials in .env
3. Ensure database exists
4. Check firewall rules

### 502 Bad Gateway

1. Check if application is running
2. Verify Nginx configuration
3. Check socket/port binding
4. Review application logs

---

## Performance Tuning

### Gunicorn Workers

Formula: `(2 x CPU cores) + 1`

```bash
gunicorn --workers 9 --bind 0.0.0.0:8000 config.wsgi:application
```

### MySQL Optimization

```sql
-- Add indexes
CREATE INDEX idx_email ON user_profiles(email);
CREATE INDEX idx_active ON user_profiles(is_active);

-- Optimize tables
OPTIMIZE TABLE user_profiles;
```

### Caching (Redis)

Add to `requirements.txt`:
```
redis==5.0.0
django-redis==5.4.0
```

Update `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## Support

For deployment issues, consult:
- Django documentation: https://docs.djangoproject.com/
- Docker documentation: https://docs.docker.com/
- Nginx documentation: https://nginx.org/en/docs/
