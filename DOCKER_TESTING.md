# Docker Testing & Verification Guide

Complete guide to test and verify the Docker setup for PDF Converter.

## Prerequisites

- Docker installed and running
- Docker Compose installed
- Git (for cloning/pulling)
- curl (for testing)
- Web browser

## ✅ Pre-Flight Checks

### 1. Verify Docker Installation

```bash
# Check Docker version
docker --version
# Should output: Docker version X.X.X

# Check Docker Compose version
docker-compose --version
# Should output: Docker Compose version X.X.X

# Test Docker daemon
docker ps
# Should list containers without errors
```

### 2. Check Available Resources

```bash
# Check available disk space
docker system df

# Check available memory
docker system info | grep Memory

# Check Docker daemon status
docker info
```

### 3. Verify Project Files

```bash
# Verify required files exist
ls -la Dockerfile
ls -la docker-compose.yaml
ls -la requirements.txt
ls -la index.html
ls -la static/
```

## 🏗️ Building the Docker Image

### Build Image

```bash
# Standard build
docker build -t pdf-converter .

# Build with no cache (fresh build)
docker build --no-cache -t pdf-converter .

# Build with verbose output
docker build --progress=plain -t pdf-converter .

# Verify image was created
docker images | grep pdf-converter
```

### Build Checks

```bash
# Check image size
docker images --format "table {{.Repository}}\t{{.Size}}" | grep pdf-converter

# Inspect image details
docker inspect pdf-converter

# Check image layers
docker history pdf-converter
```

## 🚀 Running with Docker Compose

### Start Container

```bash
# Start and display logs
docker-compose up

# Start in background
docker-compose up -d

# Start with rebuild
docker-compose up --build -d

# Start specific service
docker-compose up pdf-converter
```

### Verify Container Status

```bash
# Check running containers
docker-compose ps

# Should show:
# NAME              STATUS             PORTS
# pdf-converter-app  Up (healthy)       0.0.0.0:8000->8000/tcp
```

### Check Health Status

```bash
# View health status
docker-compose ps

# Health check details
docker inspect pdf-converter-app --format='{{.State.Health.Status}}'

# Manual health check
docker-compose exec pdf-converter curl http://localhost:8000/health

# Continuous health monitoring
watch docker-compose ps
```

## 🌐 Testing Web Interface

### Access Application

```bash
# Web UI
curl http://localhost:8000/index.html

# API Health
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Root endpoint
curl http://localhost:8000/
# Should return API info
```

### Test in Browser

1. Open: `http://localhost:8000/index.html`
2. Should see:
   - PDF Converter heading
   - Two tabs (Convert & Merge)
   - Upload areas
   - Styled interface

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API Docs (Swagger)
curl http://localhost:8000/docs

# API Docs (ReDoc)
curl http://localhost:8000/redoc

# Root info
curl http://localhost:8000/
```

## 📁 Testing Volume Mounts

### Verify Volumes

```bash
# Check volume configuration
docker-compose config | grep -A 3 volumes

# List volumes
docker volume ls

# Inspect volume
docker volume inspect pdf-converter_converted
docker volume inspect pdf-converter_uploads

# Check volume contents
docker-compose exec pdf-converter ls -la /app/converted
docker-compose exec pdf-converter ls -la /app/uploads
```

### Test File Persistence

```bash
# Create a test file in container
docker-compose exec pdf-converter touch /app/converted/test.txt

# Check it exists in host
ls -la ./converted/test.txt

# Stop and restart
docker-compose down
docker-compose up -d

# Verify file persists
docker-compose exec pdf-converter ls -la /app/converted/test.txt

# Cleanup
rm ./converted/test.txt
```

## 🔍 Testing Container Functionality

### Access Container Shell

```bash
# Open bash shell
docker-compose exec pdf-converter bash

# Inside container, test:
python --version
pip list
which uvicorn
python -m uvicorn main:app --help
```

### Test Python Dependencies

```bash
# Check installed packages
docker-compose exec pdf-converter pip list

# Test FastAPI import
docker-compose exec pdf-converter python -c "import fastapi; print(fastapi.__version__)"

# Test PDF libraries
docker-compose exec pdf-converter python -c "import pdf2image; print('pdf2image OK')"
docker-compose exec pdf-converter python -c "import PyPDF2; print('PyPDF2 OK')"

# Test poppler
docker-compose exec pdf-converter which pdfimages
```

## 📊 Testing API Functionality

### Test Convert Endpoint (with Sample PDF)

```bash
# Create or use existing PDF
# Example with test file:
curl -X POST http://localhost:8000/api/convert-pdf-to-jpg \
  -F "file=@test.pdf" \
  -o converted.jpg

# Check response
file converted.jpg  # Should be JPEG image
```

### Test Merge Endpoint

```bash
# Merge two PDFs
curl -X POST http://localhost:8000/api/merge-pdfs \
  -F "files=@file1.pdf" \
  -F "files=@file2.pdf" \
  -o merged.pdf

# Check response
file merged.pdf  # Should be PDF
```

## 📈 Performance Testing

### Check Container Resource Usage

```bash
# Real-time stats
docker stats pdf-converter-app

# One-time check
docker stats --no-stream pdf-converter-app

# CPU and memory usage
docker-compose exec pdf-converter ps aux
```

### Check Network

```bash
# View network configuration
docker network ls
docker network inspect pdf-converter_pdf-converter-network

# Test network connectivity
docker-compose exec pdf-converter curl http://localhost:8000/health
```

### Test File Operations

```bash
# Check file permissions
docker-compose exec pdf-converter ls -la /app/converted
docker-compose exec pdf-converter ls -la /app/uploads

# Check free disk space
docker-compose exec pdf-converter df -h

# Check memory
docker-compose exec pdf-converter free -h
```

## 🔐 Security Testing

### Check Running Processes

```bash
# View processes in container
docker-compose exec pdf-converter ps aux

# Check listening ports
docker-compose exec pdf-converter netstat -tuln
# Should show port 8000 listening
```

### Verify Environment Variables

```bash
# Check all env vars
docker-compose exec pdf-converter env

# Check specific var
docker-compose exec pdf-converter echo $PYTHONUNBUFFERED
docker-compose exec pdf-converter echo $PORT
```

### Test File Access

```bash
# Check file permissions
docker-compose exec pdf-converter ls -la /app
docker-compose exec pdf-converter ls -la /app/static
docker-compose exec pdf-converter ls -la /app/models
```

## 🔄 Lifecycle Testing

### Restart Tests

```bash
# Soft restart (stop and start)
docker-compose restart

# Hard restart (down and up)
docker-compose down && docker-compose up -d

# Verify service comes back up
docker-compose ps
curl http://localhost:8000/health
```

### Scale Testing (if using multiple replicas)

```bash
# Scale service (requires appropriate configuration)
docker-compose up -d --scale pdf-converter=2

# Check running instances
docker ps | grep pdf-converter
```

## 📋 Log Testing

### View Logs

```bash
# Real-time logs
docker-compose logs -f

# Last N lines
docker-compose logs --tail 50

# Follow specific service
docker-compose logs -f pdf-converter

# With timestamps
docker-compose logs -f --timestamps
```

### Check for Errors

```bash
# Search for errors
docker-compose logs | grep -i error

# Search for warnings
docker-compose logs | grep -i warning

# Get specific time range
docker-compose logs --since 10m
```

## 🧹 Cleanup & Reset

### Clean Up Containers

```bash
# Stop and remove containers
docker-compose down

# Stop and remove with volumes
docker-compose down -v

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything (BE CAREFUL!)
docker system prune -a --volumes
```

### Reset Environment

```bash
# Remove image
docker rmi pdf-converter

# Remove all related containers
docker rm pdf-converter-app

# Rebuild from scratch
docker build -t pdf-converter .
docker-compose up -d
```

## 📊 Comprehensive Test Checklist

### Docker Setup
- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] Project files present
- [ ] Requirements file accessible

### Build
- [ ] Image builds successfully
- [ ] No build errors
- [ ] Image size reasonable (~150MB)
- [ ] All dependencies installed

### Container
- [ ] Container starts successfully
- [ ] Container is healthy
- [ ] Container stays running
- [ ] Port 8000 is accessible

### Volumes
- [ ] Volumes created automatically
- [ ] Files persist after restart
- [ ] Directory permissions correct
- [ ] Both converted and uploads mounted

### Network
- [ ] Network created
- [ ] Container on network
- [ ] DNS resolution works
- [ ] Port forwarding works

### API
- [ ] Health endpoint responds
- [ ] Root endpoint works
- [ ] API Docs accessible (Swagger)
- [ ] ReDoc accessible

### UI
- [ ] Web UI loads
- [ ] Styling applies correctly
- [ ] JavaScript loads
- [ ] All tabs visible

### Features
- [ ] Convert endpoint works (test with PDF)
- [ ] Merge endpoint works (test with PDFs)
- [ ] File validation works
- [ ] Error handling works

### Performance
- [ ] Response time acceptable
- [ ] Memory usage reasonable
- [ ] CPU usage reasonable
- [ ] Disk I/O acceptable

### Reliability
- [ ] Container restarts properly
- [ ] Health checks work
- [ ] Logs are generated
- [ ] No memory leaks (after prolonged use)

## 🚨 Troubleshooting Tests

### If Container Won't Start

```bash
# Check logs
docker-compose logs

# Check for port conflicts
sudo lsof -i :8000

# Try different port
# Edit docker-compose.yaml and change ports

# Rebuild
docker-compose up --build
```

### If Volume Mounting Fails

```bash
# Check volume exists
docker volume ls

# Check permissions
ls -la ./converted
ls -la ./uploads

# Create if missing
mkdir -p ./converted ./uploads

# Fix permissions
chmod 755 ./converted ./uploads
```

### If Health Check Fails

```bash
# Check manually
docker-compose exec pdf-converter curl http://localhost:8000/health

# Check logs
docker-compose logs | grep health

# Increase health check timeout in compose file
```

### If API Doesn't Respond

```bash
# Check container is running
docker-compose ps

# Check logs for errors
docker-compose logs

# Test connectivity
docker-compose exec pdf-converter curl localhost:8000

# Verify port is exposed
docker port pdf-converter-app
```

## 📈 Automated Testing Script

Create `test-docker.sh`:

```bash
#!/bin/bash

echo "🧪 Running Docker tests..."

# Test 1: Image exists
echo "Test 1: Checking image..."
docker images | grep pdf-converter || echo "❌ Image not found"

# Test 2: Container runs
echo "Test 2: Starting container..."
docker-compose up -d

# Test 3: Health check
echo "Test 3: Health check..."
sleep 5
curl -f http://localhost:8000/health || echo "❌ Health check failed"

# Test 4: API endpoints
echo "Test 4: API endpoints..."
curl -f http://localhost:8000/ || echo "❌ Root endpoint failed"
curl -f http://localhost:8000/docs || echo "❌ Docs endpoint failed"

# Test 5: Cleanup
echo "Test 5: Cleanup..."
docker-compose down

echo "✅ All tests completed!"
```

Run tests:
```bash
chmod +x test-docker.sh
./test-docker.sh
```

---

**Docker configuration is ready for testing and deployment!**
