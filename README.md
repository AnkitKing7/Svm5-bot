# 🤖 SVM5-BOT - Complete Discord VPS Management Bot

<div align="center">
  <img src="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg" width="200">
  
  **Version 5.0.0** | Made by **Ankit-Dev** with ❤️
  
  [![Discord](https://img.shields.io/badge/Discord-SVM5--BOT-5865F2?logo=discord&logoColor=white)](https://discord.gg)
  [![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
  [![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)
  [![GitHub](https://img.shields.io/badge/GitHub-AnkitKing7-181717?logo=github)](https://github.com/AnkitKing7/Svm5-bot)
</div>

## 📋 **Table of Contents**
- [✨ Features](#-features)
- [🐛 Fixed Issues](#-fixed-issues)
- [💻 Requirements](#-requirements)
- [🚀 Quick Installation](#-quick-installation)
- [📥 Manual Installation](#-manual-installation)
- [⚙️ Configuration](#️-configuration)
- [📖 Commands](#-commands)
- [🌐 Node Management](#-node-management)
- [📦 Panel Installation](#-panel-installation)
- [🔌 Port Forwarding](#-port-forwarding)
- [🌍 IPv4 Management](#-ipv4-management)
- [🤖 AI Chat](#-ai-chat)
- [📟 Console Commands](#-console-commands)
- [🛡️ Admin Commands](#️-admin-commands)
- [👑 Main Admin Commands](#-main-admin-commands)
- [📁 File Structure](#-file-structure)
- [🚀 Running the Bot](#-running-the-bot)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🔐 License & Purchase](#-license--purchase)
- [📞 Support](#-support)

---

## ✨ **Features**

### 🖥️ **VPS Management (Direct LXC)**
- ✅ Create/Delete VPS containers automatically
- ✅ Start/Stop/Restart containers with interactive buttons
- ✅ Live statistics (CPU, RAM, Disk, Uptime, Processes)
- ✅ 30+ OS options (Ubuntu, Debian, Fedora, Rocky, Alma, CentOS, Alpine, Arch, FreeBSD, OpenSUSE)
- ✅ Resource limits per container
- ✅ View container logs
- ✅ SSH access via tmate (temporary SSH links)
- ✅ Reboot and shutdown commands

### 🌐 **Node Management (NEW)**
- ✅ Add/Remove multiple LXC nodes
- ✅ Monitor node health and resources
- ✅ Distributed container management
- ✅ Node statistics and health checks
- ✅ API key authentication for nodes
- ✅ Region-based node grouping

### 🔌 **Port Forwarding**
- ✅ Forward ports from container to host
- ✅ TCP/UDP protocol support
- ✅ Quota system per user
- ✅ List and manage active forwards
- ✅ Random port allocation (20000-50000)
- ✅ Protocol selection (tcp, udp, tcp+udp)

### 📦 **Panel Installation**
- ✅ Install Pterodactyl game panel
- ✅ Install Pufferpanel lightweight panel
- ✅ Automatic credential generation
- ✅ Cloudflared tunnel support for public URLs
- ✅ Panel information storage
- ✅ Automatic DM with credentials

### 💰 **Free VPS System**
- ✅ Earn VPS by inviting users
- ✅ Multiple plans (Bronze to Legendary)
- ✅ Automatic claim system
- ✅ Invite tracking
- ✅ Boost rewards
- ✅ 7 plans with increasing resources

### 🌍 **IPv4 Management**
- ✅ Purchase IPv4 via UPI
- ✅ Automatic payment verification
- ✅ Admin assignment with full network details
- ✅ MAC address, gateway, netmask tracking
- ✅ View your IPv4 addresses
- ✅ ₹50 per IPv4 (configurable)

### 🤖 **AI Assistant (FIXED)**
- ✅ Groq LLaMA 3.3 integration (updated working model)
- ✅ Chat history per user
- ✅ Server management help
- ✅ 24/7 availability
- ✅ Reset conversation option
- ✅ No more "model deprecated" errors

### 📟 **Console Commands**
- ✅ `.ss` - Take VPS screenshot/console output
- ✅ `.console` - Interactive console
- ✅ `.execute` - Run commands in VPS
- ✅ `.top` - Show process monitor
- ✅ `.df` - Show disk usage
- ✅ `.free` - Show memory usage
- ✅ `.netstat` - Show network connections

### 👤 **User Features**
- ✅ Account generator (username/email/password)
- ✅ View your generated accounts
- ✅ Check invite statistics
- ✅ Interactive help menu
- ✅ Bot info and uptime
- ✅ Server hardware info

### 🛡️ **Admin Features**
- ✅ Full admin panel
- ✅ User management
- ✅ Resource allocation
- ✅ Suspension system
- ✅ Purge protection
- ✅ Server statistics
- ✅ Add/Remove admins
- ✅ List all users and VPS
- ✅ Database backup/restore

### 👑 **Main Admin Features**
- ✅ Maintenance mode
- ✅ Purge all unprotected VPS
- ✅ Protect VPS from purge
- ✅ Set CPU/RAM/Disk thresholds
- ✅ View all users
- ✅ System information

### 🔒 **Security**
- ✅ License key verification
- ✅ Role-based access control
- ✅ Suspension system
- ✅ Audit logs
- ✅ Firewall configuration
- ✅ Fail2ban integration

---

## 🐛 **Fixed Issues**

| Issue | Status | Fix |
|-------|--------|-----|
| `.help` interaction failed | ✅ FIXED | Added proper defer pattern and view handling |
| AI model deprecated | ✅ FIXED | Updated to `llama-3.3-70b-versatile` |
| SSH generation timeout | ✅ FIXED | Increased wait time and added error handling |
| `.node` command missing | ✅ FIXED | Added complete node management system |
| Port forwarding quota | ✅ FIXED | Added quota tracking and validation |
| Panel installation errors | ✅ FIXED | Added cloudflared tunnel support |
| IPv4 details incomplete | ✅ FIXED | Added MAC, gateway, netmask, interface |
| Console commands not working | ✅ FIXED | Added `.ss`, `.console`, `.top`, `.df`, `.free`, `.netstat` |
| Database backup missing | ✅ FIXED | Added backup/restore commands |
| Error handling improved | ✅ FIXED | Added comprehensive error handling |

---

## 💻 **Requirements**

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **OS** | Ubuntu 20.04 | Ubuntu 22.04/24.04 |
| **RAM** | 2 GB | 4 GB+ |
| **CPU** | 2 cores | 4 cores+ |
| **Disk** | 20 GB | 50 GB+ |
| **Python** | 3.8 | 3.10+ |
| **LXC/LXD** | 5.0 | 5.21+ |

---

## 🚀 **Quick Installation**

### **One-Line Install (Recommended)**
```bash
curl -sSL https://raw.githubusercontent.com/AnkitKing7/Svm5-bot/main/install.sh | sudo bash
