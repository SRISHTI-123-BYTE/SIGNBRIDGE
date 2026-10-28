# SignBridge Production Deployment Guide

SignBridge is engineered with a **unified production architecture**: a single-port FastAPI ASGI server natively serves both the REST/WebSocket machine learning backend and the compiled React 18 Single Page Application (SPA).

---

## Architecture Overview

```
                      +-----------------------------+
                      |   Client Web Browser        |
                      |   (Camera, WASM, WebGL)     |
                      +--------------+--------------+
                                     |
               HTTPS (Port 443) / HTTP (Port 8000)
               WSS / WS Full-Duplex Stream
                                     v
                      +-----------------------------+
                      |    FastAPI ASGI Engine      |
                      |    (Uvicorn 0.0.0.0:8000)   |
                      +--------------+--------------+
                                     |
     +-------------------------------+-------------------------------+
     |                               |                               |
     v                               v                               v
[Static SPA Handler]       [REST API Endpoints]            [WebSocket Stream]
- / (React index.html)     - /api/health                   - /ws/live-sign
- /assets/*.js             - /api/vocabulary               - 107-Pt Normalization
- /assets/*.css            - /api/sign-languages           - ST-GCN ONNX Engine
- SPA Fallback Route       - /api/scenarios/simulate       - CTC Token Decoder
                                                           - Multilingual NLP
```

---

## 1. Quick Local Production Run (Windows / macOS / Linux)

### Windows One-Click:
Simply double-click:
```bat
start_production.bat
```
*(Or run `start.bat` and select Option `[1]`)*.

This script:
1. Checks for the compiled frontend distribution (`frontend/dist/index.html`).
2. Automatically compiles the React assets via `npm run build` if not already present.
3. Launches the unified FastAPI server on `http://localhost:8000`.
4. Automatically opens your browser.

### Manual Command Line:
```bash
# 1. Build frontend distribution
cd frontend
npm install
npm run build
cd ..

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Launch unified server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir backend
```

Open **`http://localhost:8000`** in your browser.

---

## 2. Docker Container Deployment

SignBridge includes a **multi-stage production Dockerfile** that builds the frontend with Node 18, sets up the Python 3.10 inference environment, copies ONNX neural weights, and exposes a production container with automated health checks.

### Single-Command Launch:
```bash
docker compose up --build -d
```

### Or using Docker CLI:
```bash
# Build Docker image
docker build -t signbridge:latest .

# Run container
docker run -d -p 8000:8000 --name signbridge_app signbridge:latest
```

### Verify Container Status:
```bash
docker ps --filter "name=signbridge_app"
curl http://localhost:8000/api/health
```

---

## 3. Free Cloud Deployment (1-Click)

### Option A: Render.com (Recommended — 100% Free Tier, Native WebSockets)
1. Push your repository to **GitHub** or **GitLab**.
2. Go to [dashboard.render.com](https://dashboard.render.com) and click **New + > Blueprint**.
3. Select your repository. Render automatically reads the included [`render.yaml`](file:///c:/Users/srish/.gemini/antigravity/scratch/signbridge/render.yaml):
   - **Environment**: Python 3.10
   - **Build Command**: `cd frontend && npm install && npm run build && cd .. && pip install -r backend/requirements.txt`
   - **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT --app-dir backend`
   - **Region**: Oregon (or Frankfurt)
   - **Plan**: Free
4. Click **Apply**. Your app is live at `https://signbridge.onrender.com` in under 3 minutes with free automatic HTTPS and WSS certificates.

---

### Option B: Railway.app
1. Create a new project on [Railway.app](https://railway.app).
2. Connect your GitHub repository.
3. Railway detects the root [`Dockerfile`](file:///c:/Users/srish/.gemini/antigravity/scratch/signbridge/Dockerfile) and automatically executes the multi-stage build.
4. Set the domain in Railway Settings -> **Generate Domain**.
5. Live immediately with auto-restarts and WebSockets.

---

### Option C: Koyeb / Fly.io / Heroku
The included [`Procfile`](file:///c:/Users/srish/.gemini/antigravity/scratch/signbridge/Procfile) contains standard ASGI deployment declarations:
```procfile
web: python -m uvicorn main:app --host 0.0.0.0 --port $PORT --app-dir backend
```
Deploy by linking the repo or via CLI:
```bash
fly launch
# or
koyeb app init signbridge --git github.com/username/signbridge --git-branch main
```

---

## 4. Linux VPS Production Deployment (Ubuntu / Debian / AWS EC2 / DigitalOcean)

### A. Systemd Background Service
Create `/etc/systemd/system/signbridge.service`:
```ini
[Unit]
Description=SignBridge Edge AI Web Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/signbridge
Environment="PATH=/home/ubuntu/signbridge/venv/bin"
Environment="FRONTEND_DIST_DIR=/home/ubuntu/signbridge/frontend/dist"
ExecStart=/home/ubuntu/signbridge/venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000 --app-dir backend --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable signbridge
sudo systemctl start signbridge
sudo systemctl status signbridge
```

### B. Nginx Reverse Proxy with WebSocket Upgrade
Create `/etc/nginx/sites-available/signbridge`:
```nginx
server {
    listen 80;
    server_name signbridge.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket timeouts for persistent streaming
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
```

Enable and issue Let's Encrypt SSL:
```bash
sudo ln -s /etc/nginx/sites-available/signbridge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d signbridge.yourdomain.com
```

---

## 5. Automated Verification Test Suite

Verify that your deployment is operating with 100% integrity across all tiers:
```bash
python verify_deployment.py
```

### Verification Checklist:
- [x] **SPA Entrypoint (GET /)**: HTTP 200, React root DOM element loaded.
- [x] **Static Asset Bundling (/assets)**: CSS stylesheet & JavaScript application chunks loaded.
- [x] **SPA Client Routing**: Deep client routes (e.g., `/scenarios`, `/recorder`) properly fall back to `index.html`.
- [x] **REST API (/api/health)**: Online status, 52 model classes, edge-ready confirmation.
- [x] **Multi-Dialect Metadata (/api/sign-languages)**: ISLRTC national standard & 6 regional zonal chapters returned.
- [x] **Full-Duplex WebSocket Handshake (/ws/live-sign)**: Real-time 107-point landmark transmission & frame telemetry acknowledgment.
