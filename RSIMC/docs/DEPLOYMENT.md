# Deployment Guide

## Prerequisites

- Docker & Docker Compose (v20.10+)
- Minimum 4GB RAM, 20GB storage
- Ubuntu 20.04 LTS or similar Linux distribution
- Static IP address for the server
- SSL certificates (for production)

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/darsi-cs.git
cd darsi-cs
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
docker-compose exec backend python -m alembic upgrade head
```

### 5. Access Applications
- Kiosk UI: http://localhost:3000
- Admin Dashboard: http://localhost:3001
- API Docs: http://localhost:8000/docs
- API Redoc: http://localhost:8000/redoc

## Production Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
sudo mkdir -p /opt/darsi-cs
sudo chown -R $USER:$USER /opt/darsi-cs
```

### 2. SSL Certificate Setup

```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Certificate locations:
# - /etc/letsencrypt/live/your-domain.com/fullchain.pem
# - /etc/letsencrypt/live/your-domain.com/privkey.pem
```

### 3. Configure Production Environment

```bash
cd /opt/darsi-cs
cp .env.example .env
```

Edit `.env` with production values:
```
DEBUG=False
ENV=production
SECRET_KEY=<generate-strong-key>
DATABASE_URL=postgresql://username:password@db.host:5432/darsi_db
REDIS_URL=redis://redis.host:6379/0
ALLOWED_HOSTS=your-domain.com,*.your-domain.com
```

### 4. Deploy Application

```bash
# Copy application files
rsync -avz ./backend /opt/darsi-cs/
rsync -avz ./kiosk-ui /opt/darsi-cs/
rsync -avz ./admin-dashboard /opt/darsi-cs/
rsync -avz ./docker-compose.yml /opt/darsi-cs/
rsync -avz ./.env /opt/darsi-cs/

# Start containers
cd /opt/darsi-cs
docker-compose up -d

# Verify deployment
docker-compose ps
docker-compose logs -f backend
```

### 5. Nginx Configuration

Create `/etc/nginx/sites-available/darsi-cs`:

```nginx
upstream api {
    server localhost:8000;
}

upstream kiosk {
    server localhost:3000;
}

upstream admin {
    server localhost:3001;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API
    location /api/ {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Kiosk
    location / {
        proxy_pass http://kiosk;
        proxy_set_header Host $host;
    }

    # Admin
    location /admin/ {
        proxy_pass http://admin/;
        proxy_set_header Host $host;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    limit_req zone=api_limit burst=200;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/darsi-cs /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Database Backup Setup

```bash
# Create backup script
cat > /opt/darsi-cs/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/darsi-cs/backups"
mkdir -p $BACKUP_DIR
docker-compose exec -T postgres pg_dump -U darsi_user darsi_db | gzip > $BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).sql.gz
find $BACKUP_DIR -name "backup-*.sql.gz" -mtime +30 -delete
EOF

chmod +x /opt/darsi-cs/backup.sh

# Schedule daily backup
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/darsi-cs/backup.sh") | crontab -
```

### 7. Monitoring Setup

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Setup log rotation
sudo tee /etc/logrotate.d/darsi-cs << 'EOF'
/opt/darsi-cs/docker-compose.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
}
EOF
```

### 8. Firewall Configuration

```bash
# Open required ports
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Monitoring & Maintenance

### Health Checks

```bash
# Check API health
curl https://your-domain.com/api/health

# Check Docker containers
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Database Maintenance

```bash
# Connect to database
docker-compose exec postgres psql -U darsi_user -d darsi_db

# Common queries
SELECT COUNT(*) FROM patients;
SELECT COUNT(*) FROM sessions WHERE created_at > NOW() - INTERVAL '24 hours';
```

### Updates & Patches

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose build --no-cache

# Restart services
docker-compose down
docker-compose up -d
```

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs backend

# Check disk space
df -h

# Check ports
sudo netstat -tlnp | grep -E ':8000|:5432|:6379'
```

### Database Connection Issues
```bash
# Test connection
docker-compose exec postgres psql -U darsi_user -d darsi_db -c "SELECT 1"

# Check PostgreSQL logs
docker-compose logs postgres
```

### High Memory Usage
```bash
# Check container memory
docker stats

# Reduce cache size in Redis
docker-compose exec redis redis-cli CONFIG SET maxmemory 1gb
```

## Performance Optimization

- Enable gzip compression in Nginx
- Use CDN for static assets
- Implement caching headers
- Monitor database query performance
- Scale horizontally with load balancer
