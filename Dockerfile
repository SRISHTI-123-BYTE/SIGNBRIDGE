# ========================================================
# SignBridge Multi-Stage Production Dockerfile
# Stage 1: Build Frontend (Vite + React 18 + Tailwind CSS)
# Stage 2: Lightweight Python 3.10 Edge Inference Runtime
# ========================================================

# --- Stage 1: Frontend Build ---
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Install package dependencies
COPY frontend/package*.json ./
RUN npm ci --silent || npm install --silent

# Copy source code and build production distribution
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Python Backend & Static SPA Hosting ---
FROM python:3.10-slim AS production

# Security & optimization environment flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    FRONTEND_DIST_DIR=/app/frontend/dist

WORKDIR /app

# Install minimal OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code and trained neural models
COPY backend/ ./backend/

# Copy compiled frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose production port
EXPOSE 8000

# Health check to ensure service readiness
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Launch FastAPI with Uvicorn ASGI server
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "backend"]
