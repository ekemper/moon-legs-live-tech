# Piano Practice App frontend: build with Node, serve with nginx.
# Build from repo root: docker build -f frontend/Dockerfile .

# --- Build stage ---
FROM node:20-alpine AS builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# --- Serve stage ---
FROM nginx:alpine

# Substitute backend upstream at build time (compose service name)
ARG BACKEND_UPSTREAM=backend:8765
COPY frontend/nginx.conf /tmp/nginx.conf
RUN sed -e "s/BACKEND_UPSTREAM/${BACKEND_UPSTREAM}/g" /tmp/nginx.conf > /etc/nginx/conf.d/default.conf && rm /tmp/nginx.conf

# Remove default nginx static content and use our build
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
