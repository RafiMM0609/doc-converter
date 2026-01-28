# Docker Setup Guide for PDF Converter

Complete guide for running PDF Converter using Docker and Docker Compose.

## Prerequisites

- Docker installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- No need to install Python or poppler-utils locally!

## Quick Start with Docker

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and run the container
docker-compose up

# The application will be available at:
# http://localhost:8000/index.html
```

### Option 2: Using Docker Directly

```bash
# Build the image
docker build -t pdf-converter .

# Run the container
docker run -p 8000:8000 -v ./converted:/app/converted -v ./uploads:/app/uploads pdf-converter

# The application will be available at:
# http://localhost:8000/index.html
```

## Docker Compose Configuration

### Features

- **Service**: `pdf-converter`
- **Port**: 8000 (exposed)
- **Volumes**: 
  - `./converted` - Stores converted files temporarily
  - `./uploads` - Stores uploaded files temporarily
- **Environment Variables**: `PYTHONUNBUFFERED=1`, `PORT=8000`
- **Restart Policy**: `unless-stopped`
- **Health Check**: Automatic health monitoring
- **Network**: Isolated Docker network

### Start Container

```bash
docker-compose up
```

### Start in Background

```bash
docker-compose up -d
```

### View Logs

```bash
# Real-time logs
docker-compose logs -f

# Follow specific service logs
docker-compose logs -f pdf-converter
```

### Stop Container

```bash
docker-compose down
```

### Remove Everything (including volumes)

```bash
docker-compose down -v
```

## Docker Commands

### Building

```bash
# Build image
docker build -t pdf-converter .

# Build with no cache
docker build --no-cache -t pdf-converter .

# Build specific target
docker build -t pdf-converter:latest .
```

### Running

```bash
# Run interactive
docker run -it -p 8000:8000 pdf-converter

# Run in background
docker run -d -p 8000:8000 --name pdf-app pdf-converter

# Run with volume mounts
docker run -p 8000:8000 \
  -v $(pwd)/converted:/app/converted \
  -v $(pwd)/uploads:/app/uploads \
  pdf-converter
```

### Managing Containers

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop pdf-app

# Start container
docker start pdf-app

# Remove container
docker rm pdf-app

# View container logs
docker logs pdf-app

# Execute command in container
docker exec -it pdf-app bash
```

### Debugging

```bash
# Access container shell
docker-compose exec pdf-converter bash

# Check container status
docker-compose ps

# Health check status
docker-compose exec pdf-converter curl http://localhost:8000/health

# View environment variables
docker-compose exec pdf-converter env
```

## Environment Variables

Can be customized in `docker-compose.yaml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1      # Unbuffered Python output
  - PORT=8000               # Application port
  # Add more as needed:
  # - MAX_FILE_SIZE=10485760
  # - DPI=200
```

## Volume Mounts

The `docker-compose.yaml` includes:

```yaml
volumes:
  - ./converted:/app/converted    # Converted files
  - ./uploads:/app/uploads        # Uploaded files
```

These directories will be created automatically when containers start.

## Health Check

The container includes a health check:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

To check health status:

```bash
docker-compose ps
docker inspect pdf-app --format='{{.State.Health.Status}}'
```

## Network Configuration

The compose file sets up a dedicated Docker network:

```yaml
networks:
  pdf-converter-network:
    driver: bridge
```

This keeps the application isolated while allowing internal communication.

## Resource Limits (Optional)

To limit CPU and memory, uncomment in `docker-compose.yaml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

## Accessing the Application

### From Your Computer

- **Web UI**: http://localhost:8000/index.html
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### From Another Container

If running other Docker containers on the same network:

- Use `http://pdf-converter:8000` instead of `http://localhost:8000`

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Check image exists
docker images

# Rebuild image
docker-compose up --build
```

### Port Already in Use

```bash
# Use different port in docker-compose.yaml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Volume Permission Issues

```bash
# Create volumes first
mkdir -p converted uploads

# Run with user permissions
docker-compose exec pdf-converter chmod 777 /app/converted /app/uploads
```

### Health Check Failing

```bash
# Test directly
docker-compose exec pdf-converter curl http://localhost:8000/health

# Check container logs
docker-compose logs pdf-converter
```

## Production Deployment

### Recommended Setup

```yaml
# docker-compose.prod.yaml
services:
  pdf-converter:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - PORT=8000
    volumes:
      - /data/converted:/app/converted
      - /data/uploads:/app/uploads
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Deploy Production

```bash
docker-compose -f docker-compose.prod.yaml up -d
```

### Monitor Production

```bash
# Check status
docker-compose -f docker-compose.prod.yaml ps

# View logs
docker-compose -f docker-compose.prod.yaml logs -f

# Monitor resources
docker stats pdf-converter
```

## Docker Image Details

### Base Image
- **Image**: `python:3.11-slim`
- **Size**: ~150 MB
- **OS**: Debian Bullseye

### Installed Packages
- Python 3.11
- poppler-utils (PDF processing)
- All Python dependencies from `requirements.txt`

### Exposed Port
- **Port**: 8000
- **Protocol**: HTTP

### Working Directory
- **Path**: `/app`

### Health Check
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

## Best Practices

✅ **Use Docker Compose** for development and deployment
✅ **Mount volumes** for persistence
✅ **Use health checks** for monitoring
✅ **Set restart policy** for reliability
✅ **Use environment variables** for configuration
✅ **Monitor logs** for troubleshooting
✅ **Resource limits** for production
✅ **Named containers** for easy management

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t pdf-converter:${{ github.sha }} .
      - name: Push to registry
        run: docker push registry.example.com/pdf-converter:${{ github.sha }}
```

### GitLab CI Example

```yaml
docker-build:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t pdf-converter:$CI_COMMIT_SHA .
    - docker push registry.example.com/pdf-converter:$CI_COMMIT_SHA
```

## Kubernetes Deployment

### Simple Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pdf-converter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pdf-converter
  template:
    metadata:
      labels:
        app: pdf-converter
    spec:
      containers:
      - name: pdf-converter
        image: pdf-converter:latest
        ports:
        - containerPort: 8000
        healthCheck:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
```

## Maintenance

### Clean Up

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything
docker system prune -a
```

### Update Application

```bash
# Pull latest code
git pull

# Rebuild image
docker-compose up --build

# Apply changes
docker-compose up -d
```

### Backup Volumes

```bash
# Backup converted files
docker run --rm -v pdf-converter_converted:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/converted-backup.tar.gz /data

# Backup uploads
docker run --rm -v pdf-converter_uploads:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/uploads-backup.tar.gz /data
```

## Support

For issues with Docker setup:
1. Check Docker installation: `docker --version`
2. Check Docker Compose: `docker-compose --version`
3. View logs: `docker-compose logs`
4. Test health: `docker-compose exec pdf-converter curl http://localhost:8000/health`

---

**Docker setup is complete and ready for development or production use!**
