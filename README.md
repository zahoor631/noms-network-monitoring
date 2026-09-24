# 🌐 NOMS — Network Operations & Monitoring System

A web-based Network Monitoring, IP Management, Topology Visualization & Incident Management Platform.

![Status](https://img.shields.io/badge/status-active-success)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Features

- 🔐 **Authentication** — JWT with role-based access (Admin, Engineer, NOC, Viewer)
- 🖥️ **Device Management** — CRUD for routers, switches, servers, firewalls, APs
- 📡 **Live Monitoring** — Real ICMP ping, response time, packet loss tracking
- 🌐 **IPAM** — Subnet management, IP auto-generation, subnet calculator
- 🗺️ **Topology** — Interactive network diagram with auto-discovery
- 🏢 **Organization** — Site and department-wise hierarchy
- 🔔 **Alerts** — Severity-based alerts (info, warning, critical)
- 🎫 **Tickets** — Incident management with priority, status, assignment
- 📊 **Reports** — Uptime analytics with CSV export
- 👥 **User Management** — 4 roles with permissions
- ⚙️ **Settings** — System info, health check, monitoring config
- 🖼️ **Photo Upload** — User avatars with admin management

## 🏗️ Tech Stack

**Backend:**
- Python 3.12 + FastAPI
- SQLAlchemy + MySQL/MariaDB
- JWT Authentication
- APScheduler (background tasks)
- Real ICMP ping monitoring

**Frontend:**
- Vue 3 (Composition API)
- Vite + Tailwind CSS
- Pinia + Vue Router
- Vue Flow (topology)
- Chart.js (analytics)

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- MySQL 8+ or MariaDB 10+
- XAMPP (for Windows, easy MySQL setup)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Database create karo
mysql -u root -e "CREATE DATABASE noms_db CHARACTER SET utf8mb4;"

# Admin user banao
python -m scripts.create_admin

# Server chalao
uvicorn app.main:app --reload --port 8000