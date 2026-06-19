# Qdrant Docker Compose Setup
This setup provides a Qdrant vector database deployment with persistent storage, health checks, resource limits, and security best practices.

## Features
- Persistent storage with volumes
- Health checks for monitoring
- Resource limits (CPU & memory)
- Both HTTP and gRPC API endpoints
- Automatic restart policy
- Security with API keys (configurable)
- Snapshot support for backups

## Quick Start

### 1. Initial Setup
```bash
# Create necessary directories
mkdir -p qdrant_storage qdrant_snapshots

# Set proper permissions
chmod -R 755 qdrant_storage qdrant_snapshots

# Copy environment template (optional)
cp .env.example .env
```

### 2. Configure (Production)
For production, edit the `docker-compose.yml` and uncomment the API key lines:

```yaml
# Security (uncomment and configure for production)
- QDRANT__SERVICE__API_KEY=your-secure-api-key-here
- QDRANT__SERVICE__READ_ONLY_API_KEY=your-read-only-key-here
```

**Generate secure API keys:**
```bash
# Generate random API keys
openssl rand -base64 32
openssl rand -base64 32
```

### 3. Start Qdrant
```bash
# Start in detached mode
docker-compose up -d

# Check logs
docker-compose logs -f qdrant

# Check status
docker-compose ps
```

### 4. Verify Installation
```bash
# Check health
curl http://localhost:6333/healthz

# Get cluster info
curl http://localhost:6333/cluster

# List collections (if API key is set, add header)
curl http://localhost:6333/collections

# With API key:
curl -H "api-key: your-api-key-here" http://localhost:6333/collections
```

## API Endpoints
- **HTTP API**: `http://localhost:6333`
- **gRPC API**: `localhost:6334`
- **Web UI**: `http://localhost:6333/dashboard`

## Resource Configuration
Current defaults (adjust in `docker-compose.yml`):
- **CPU Limit**: 4 cores
- **Memory Limit**: 8GB
- **CPU Reservation**: 2 cores
- **Memory Reservation**: 4GB

### Adjusting Resources
Edit the `deploy.resources` section based on your workload:
```yaml
deploy:
  resources:
    limits:
      cpus: '8'      # Increase for larger workloads
      memory: 16G
    reservations:
      cpus: '4'
      memory: 8G
```

## Storage & Backups

### Persistent Storage
Data is stored in:
- `./qdrant_storage` - Main database files
- `./qdrant_snapshots` - Snapshot backups

### Creating Snapshots
```bash
# Create a snapshot via API
curl -X POST "http://localhost:6333/collections/{collection_name}/snapshots"

# List snapshots
curl "http://localhost:6333/collections/{collection_name}/snapshots"

# Snapshots are stored in ./qdrant_snapshots
```

### Backup Strategy
```bash
# Stop Qdrant (optional, for consistent backup)
docker-compose stop

# Backup storage directory
tar -czf qdrant_backup_$(date +%Y%m%d_%H%M%S).tar.gz qdrant_storage qdrant_snapshots

# Restart Qdrant
docker-compose start
```

## Security Best Practices
1. **Enable API Keys** (strongly recommended for production)
2. **Use HTTPS** with a reverse proxy (nginx/traefik)
3. **Restrict Network Access** using firewall rules
4. **Regular Backups** of storage volumes
5. **Monitor Resource Usage** and adjust limits
6. **Keep Updated** to latest stable version

### Example Nginx Reverse Proxy Config
```nginx
server {
    listen 443 ssl http2;
    server_name qdrant.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:6333;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Cluster Setup (Multi-Node)
For production clustering, enable cluster mode:
```yaml
environment:
  - QDRANT__CLUSTER__ENABLED=true
  - QDRANT__CLUSTER__P2P__PORT=6335
  - QDRANT__CLUSTER__CONSENSUS__TICK_PERIOD_MS=100
```

Refer to [Qdrant Clustering Documentation](https://qdrant.tech/documentation/guides/distributed_deployment/) for details.

## Useful Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# View logs
docker-compose logs -f qdrant

# Remove everything (WARNING: deletes data if volumes not persistent)
docker-compose down

# Remove with volumes (WARNING: deletes all data)
docker-compose down -v

# Execute commands in container
docker-compose exec qdrant sh
```

## Performance Tuning

### For High-Throughput Scenarios
```yaml
environment:
  - QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS=8
  - QDRANT__STORAGE__OPTIMIZERS__MEMMAP_THRESHOLD_KB=100000
  - QDRANT__STORAGE__WAL__WAL_CAPACITY_MB=128
```

### For Memory-Constrained Environments
```yaml
environment:
  - QDRANT__STORAGE__OPTIMIZERS__MEMMAP_THRESHOLD_KB=20000
  - QDRANT__STORAGE__PERFORMANCE__MAX_OPTIMIZATION_THREADS=1
deploy:
  resources:
    limits:
      memory: 2G
```
