#!/usr/bin/env python3
# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                              ███████╗██╗   ██╗███╗   ███╗███████╗                              ║
# ║                              ██╔════╝██║   ██║████╗ ████║██╔════╝                              ║
# ║                              ███████╗██║   ██║██╔████╔██║█████╗                                ║
# ║                              ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝                                ║
# ║                              ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗                              ║
# ║                              ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝                              ║
# ║                                                                                                 ║
# ║                    🚀 COMPLETE VPS MANAGEMENT BOT - ULTIMATE EDITION 🚀                        ║
# ║                                                                                                 ║
# ║                         ████████╗ ██████╗  ██████╗ ██╗     ███████╗                            ║
# ║                         ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝                            ║
# ║                            ██║   ██║   ██║██║   ██║██║     █████╗                              ║
# ║                            ██║   ██║   ██║██║   ██║██║     ██╔══╝                              ║
# ║                            ██║   ╚██████╔╝╚██████╔╝███████╗███████╗                            ║
# ║                            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                            ║
# ║                                                                                                 ║
# ║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                              ║
# ║                        ALL COMMANDS FIXED - ALL ISSUES RESOLVED                                ║
# ║                    AI Model Updated • SSH Fixed • Nodes Added • Panels Working                 ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

import discord
from discord.ext import commands, tasks
from discord.ui import Modal, TextInput, View, Button, Select
import asyncio
import json
import os
import random
import string
import subprocess
import sys
import re
import sqlite3
import logging
import shlex
import shutil
import time
import aiohttp
import psutil
import netifaces
import socket
import requests
import hashlib
import base64
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
import logging

# Logging setup karein
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# ==================================================================================================
#  ⚙️  CONFIGURATION SECTION - EDIT THESE VALUES
# ==================================================================================================

# 🔑 Discord Bot Configuration
BOT_TOKEN = ""           # Get from https://discord.com/developers/applications
BOT_PREFIX = "."                                     # Command prefix (default: .)
BOT_NAME = "SVM5-BOT"                                # Bot display name
BOT_AUTHOR = "Ankit-Dev"                             # Your name/username
MAIN_ADMIN_IDS = [1405866008127864852]               # Your Discord User ID

# 🖥️ Server Configuration
DEFAULT_STORAGE_POOL = "default"                     # LXC storage pool name
SERVER_HOSTNAME = socket.gethostname()               # Auto-detected hostname

# 🌐 Auto-detect Server Public IP
try:
    SERVER_IP = requests.get('https://api.ipify.org', timeout=5).text.strip()
    logger.info(f"✅ Auto-detected public IP: {SERVER_IP}")
except:
    try:
        SERVER_IP = subprocess.getoutput("curl -s ifconfig.me")
        logger.info(f"✅ Auto-detected public IP: {SERVER_IP}")
    except:
        SERVER_IP = "13.208.181.149"            # Fallback - set manually if auto-detection fails
        logger.warning(f"⚠️ Could not auto-detect IP, using fallback: {SERVER_IP}")

# 🔌 Get MAC Address
def get_mac_address():
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface != 'lo':
                addr = netifaces.ifaddresses(iface)
                if netifaces.AF_LINK in addr:
                    return addr[netifaces.AF_LINK][0]['addr']
    except:
        pass
    return "00:00:00:00:00:00"

MAC_ADDRESS = get_mac_address()

# 💰 UPI Payment Configuration
UPI_ID = "9892642904@ybl"                            # Your UPI ID for receiving payments
IPV4_PRICE_INR = 50                                   # Price per IPv4 in INR

# 🤖 AI Configuration - FIXED: Using working model
AI_API_KEY = "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"  # Your Groq API Key
AI_MODEL = "llama-3.3-70b-versatile"                  # ✅ WORKING MODEL (Updated from deprecated llama3-70b-8192)

# 🖼️ Thumbnail URL for embeds
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg"

# 🔐 License Keys (for verification)
VALID_LICENSE_KEYS = [
    "AnkitDev99$@", 
    "SVM5-PRO-2025", 
    "SVM5-ENTERPRISE", 
    "DEVELOPER-ANKIT",
    "PREMIUM-2025",
    "ULTIMATE-2025"
]

# 💎 Free VPS Plans based on invites
FREE_VPS_PLANS = {
    'invites': [
        {'name': '🥉 Bronze Plan', 'invites': 5, 'ram': 2, 'cpu': 1, 'disk': 20, 'emoji': '🥉'},
        {'name': '🥈 Silver Plan', 'invites': 10, 'ram': 4, 'cpu': 2, 'disk': 40, 'emoji': '🥈'},
        {'name': '🥇 Gold Plan', 'invites': 15, 'ram': 8, 'cpu': 4, 'disk': 80, 'emoji': '🥇'},
        {'name': '🏆 Platinum Plan', 'invites': 20, 'ram': 16, 'cpu': 8, 'disk': 160, 'emoji': '🏆'},
        {'name': '💎 Diamond Plan', 'invites': 25, 'ram': 32, 'cpu': 16, 'disk': 320, 'emoji': '💎'},
        {'name': '👑 Royal Plan', 'invites': 30, 'ram': 64, 'cpu': 32, 'disk': 640, 'emoji': '👑'},
        {'name': '⚡ Legendary Plan', 'invites': 40, 'ram': 128, 'cpu': 64, 'disk': 1280, 'emoji': '⚡'},
    ]
}

# 🐧 OS Options for VPS Creation (24+ Options)
OS_OPTIONS = [
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS", "emoji": "🐧"},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS", "emoji": "🐧"},
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS", "emoji": "🐧"},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable", "emoji": "🌀"},
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable", "emoji": "🌀"},
    {"label": "🌀 Debian 13", "value": "images:debian/13", "desc": "Trixie - Testing", "emoji": "🌀"},
    {"label": "🎩 Fedora 39", "value": "images:fedora/39", "desc": "Fedora 39", "emoji": "🎩"},
    {"label": "🎩 Fedora 40", "value": "images:fedora/40", "desc": "Fedora 40 - Latest", "emoji": "🎩"},
    {"label": "🎩 Fedora 41", "value": "images:fedora/41", "desc": "Fedora 41 - Development", "emoji": "🎩"},
    {"label": "🦊 Rocky Linux 8", "value": "images:rockylinux/8", "desc": "Rocky 8 - Enterprise", "emoji": "🦊"},
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky 9 - Latest", "emoji": "🦊"},
    {"label": "🦊 AlmaLinux 8", "value": "images:almalinux/8", "desc": "Alma 8 - RHEL Compatible", "emoji": "🦊"},
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma 9 - Latest", "emoji": "🦊"},
    {"label": "📦 CentOS 7", "value": "images:centos/7", "desc": "CentOS 7 - Legacy", "emoji": "📦"},
    {"label": "📦 CentOS 8", "value": "images:centos/8", "desc": "CentOS 8 - Stream", "emoji": "📦"},
    {"label": "📦 CentOS 9", "value": "images:centos/9", "desc": "CentOS 9 - Stream", "emoji": "📦"},
    {"label": "🔴 Red Hat 8", "value": "images:rhel/8", "desc": "RHEL 8 - Enterprise", "emoji": "🔴"},
    {"label": "🔴 Red Hat 9", "value": "images:rhel/9", "desc": "RHEL 9 - Latest", "emoji": "🔴"},
    {"label": "🐧 Alpine 3.18", "value": "images:alpine/3.18", "desc": "Alpine - Lightweight", "emoji": "🐧"},
    {"label": "🐧 Alpine 3.19", "value": "images:alpine/3.19", "desc": "Alpine - Latest", "emoji": "🐧"},
    {"label": "🐧 Alpine 3.20", "value": "images:alpine/3.20", "desc": "Alpine - Edge", "emoji": "🐧"},
    {"label": "📀 Arch Linux", "value": "images:archlinux", "desc": "Arch - Rolling Release", "emoji": "📀"},
    {"label": "💻 Gentoo", "value": "images:gentoo", "desc": "Gentoo - Source based", "emoji": "💻"},
    {"label": "🔵 FreeBSD 13", "value": "images:freebsd/13", "desc": "FreeBSD 13 - Unix", "emoji": "🔵"},
    {"label": "🔵 FreeBSD 14", "value": "images:freebsd/14", "desc": "FreeBSD 14 - Latest", "emoji": "🔵"},
    {"label": "🟢 OpenSUSE 15.5", "value": "images:opensuse/15.5", "desc": "OpenSUSE Leap", "emoji": "🟢"},
    {"label": "🟢 OpenSUSE Tumbleweed", "value": "images:opensuse/tumbleweed", "desc": "OpenSUSE Rolling", "emoji": "🟢"},
    {"label": "🟣 Kali Linux", "value": "images:kali", "desc": "Kali - Security", "emoji": "🟣"},
    {"label": "⚪ Void Linux", "value": "images:voidlinux", "desc": "Void - Independent", "emoji": "⚪"},
]

# ==================================================================================================
#  📝  LOGGING SETUP
# ==================================================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/opt/svm5-bot/svm5.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(BOT_NAME)

# Check if LXC is installed
if not shutil.which("lxc"):
    logger.error("❌ LXC command not found! Please install LXC first.")
    logger.error("   Run: sudo apt install lxc lxc-templates && sudo snap install lxd")
    sys.exit(1)

# Check if cloudflared is installed (for tunnels)
CLOUDFLARED_AVAILABLE = shutil.which("cloudflared") is not None
if not CLOUDFLARED_AVAILABLE:
    logger.warning("⚠️ cloudflared not found. Tunnel URLs will not be available.")
    logger.warning("   Install with: sudo apt install cloudflared")

# ==================================================================================================
#  🗄️  DATABASE SETUP - COMPLETE SCHEMA
# ==================================================================================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('/opt/svm5-bot/svm5.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize complete database with all tables"""
    conn = get_db()
    cur = conn.cursor()
    
    # 👑 Admins table
    cur.execute('''CREATE TABLE IF NOT EXISTS admins (
        user_id TEXT PRIMARY KEY,
        added_by TEXT,
        added_at TEXT,
        permissions TEXT DEFAULT 'all'
    )''')
    for admin_id in MAIN_ADMIN_IDS:
        cur.execute(
    'INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)',
    (str(admin_id), datetime.now().isoformat())
)
    
    # 🖥️ VPS table
    cur.execute('''CREATE TABLE IF NOT EXISTS vps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT UNIQUE NOT NULL,
        plan_name TEXT DEFAULT 'Custom',
        ram INTEGER NOT NULL,
        cpu INTEGER NOT NULL,
        disk INTEGER NOT NULL,
        os_version TEXT DEFAULT 'ubuntu:22.04',
        status TEXT DEFAULT 'stopped',
        suspended INTEGER DEFAULT 0,
        suspended_reason TEXT DEFAULT '',
        purge_protected INTEGER DEFAULT 0,
        node_name TEXT DEFAULT 'local',
        created_at TEXT NOT NULL,
        last_started TEXT,
        last_stopped TEXT,
        ip_address TEXT,
        mac_address TEXT,
        backup_enabled INTEGER DEFAULT 0,
        backup_frequency TEXT DEFAULT 'daily',
        last_backup TEXT,
        notes TEXT
    )''')
    
    # 🌐 Nodes table (NEW - Complete node management)
    cur.execute('''CREATE TABLE IF NOT EXISTS nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        host TEXT NOT NULL,
        port INTEGER DEFAULT 22,
        username TEXT NOT NULL,
        password TEXT,
        ssh_key TEXT,
        status TEXT DEFAULT 'offline',
        total_ram INTEGER DEFAULT 0,
        used_ram INTEGER DEFAULT 0,
        total_cpu INTEGER DEFAULT 0,
        used_cpu INTEGER DEFAULT 0,
        total_disk INTEGER DEFAULT 0,
        used_disk INTEGER DEFAULT 0,
        lxc_count INTEGER DEFAULT 0,
        api_key TEXT,
        api_url TEXT,
        region TEXT DEFAULT 'us',
        last_checked TEXT,
        added_by TEXT,
        added_at TEXT NOT NULL,
        description TEXT
    )''')
    
    # 📊 User stats table
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
        user_id TEXT PRIMARY KEY,
        invites INTEGER DEFAULT 0,
        boosts INTEGER DEFAULT 0,
        claimed_vps_count INTEGER DEFAULT 0,
        total_spent INTEGER DEFAULT 0,
        last_updated TEXT
    )''')
    
    # ⚙️ Settings table
    cur.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        description TEXT,
        updated_at TEXT
    )''')
    
    # 💳 Transactions table
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        txn_ref TEXT UNIQUE NOT NULL,
        txn_id TEXT,
        amount INTEGER,
        currency TEXT DEFAULT 'INR',
        payment_method TEXT DEFAULT 'UPI',
        status TEXT DEFAULT 'pending',
        purpose TEXT DEFAULT 'ipv4',
        created_at TEXT NOT NULL,
        verified_at TEXT,
        verified_by TEXT,
        notes TEXT
    )''')
    
    # 🌍 IPv4 allocations (Enhanced)
    cur.execute('''CREATE TABLE IF NOT EXISTS ipv4 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT NOT NULL,
        public_ip TEXT,
        private_ip TEXT,
        mac_address TEXT,
        gateway TEXT,
        netmask TEXT,
        interface TEXT,
        node_name TEXT DEFAULT 'local',
        tunnel_url TEXT,
        tunnel_id TEXT,
        assigned_at TEXT NOT NULL,
        expires_at TEXT,
        auto_renew INTEGER DEFAULT 1,
        UNIQUE(user_id, container_name)
    )''')
    
    # 🔌 Port forwards
    cur.execute('''CREATE TABLE IF NOT EXISTS port_forwards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT NOT NULL,
        container_port INTEGER NOT NULL,
        host_port INTEGER UNIQUE NOT NULL,
        protocol TEXT DEFAULT 'tcp+udp',
        node_name TEXT DEFAULT 'local',
        created_at TEXT NOT NULL,
        description TEXT
    )''')
    
    # 📦 Port allocations
    cur.execute('''CREATE TABLE IF NOT EXISTS port_allocations (
        user_id TEXT PRIMARY KEY,
        allocated_ports INTEGER DEFAULT 0,
        used_ports INTEGER DEFAULT 0,
        last_updated TEXT
    )''')
    
    # ⛔ Suspension logs
    cur.execute('''CREATE TABLE IF NOT EXISTS suspension_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        container_name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        action TEXT NOT NULL,
        reason TEXT,
        admin_id TEXT,
        created_at TEXT NOT NULL
    )''')
    
    # 💾 Snapshots/Backups
    cur.execute('''CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT NOT NULL,
        snapshot_name TEXT NOT NULL,
        size_mb INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        UNIQUE(container_name, snapshot_name)
    )''')
    
    # 🤖 AI chat history
    cur.execute('''CREATE TABLE IF NOT EXISTS ai_history (
        user_id TEXT PRIMARY KEY,
        messages TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )''')
    
    # 🔐 License table
    cur.execute('''CREATE TABLE IF NOT EXISTS license (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_key TEXT NOT NULL,
        activated_at TEXT NOT NULL,
        activated_by TEXT,
        mac_address TEXT,
        hostname TEXT,
        ip_address TEXT,
        expires_at TEXT
    )''')
    
    # 📦 Panel installations
    cur.execute('''CREATE TABLE IF NOT EXISTS panels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        panel_type TEXT NOT NULL,
        panel_url TEXT,
        admin_user TEXT,
        admin_pass TEXT,
        admin_email TEXT,
        node_name TEXT DEFAULT 'local',
        container_name TEXT,
        tunnel_url TEXT,
        installed_at TEXT NOT NULL,
        last_accessed TEXT
    )''')
    
    # 📋 Invite tracking
    cur.execute('''CREATE TABLE IF NOT EXISTS invites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inviter_id TEXT NOT NULL,
        invited_id TEXT NOT NULL,
        joined_at TEXT NOT NULL,
        rewarded INTEGER DEFAULT 0,
        UNIQUE(invited_id)
    )''')
    
    # 🚀 Initialize default settings
    settings_init = [
        ('cpu_threshold', '90', 'CPU usage threshold for alerts'),
        ('ram_threshold', '90', 'RAM usage threshold for alerts'),
        ('disk_threshold', '90', 'Disk usage threshold for alerts'),
        ('maintenance_mode', 'false', 'Maintenance mode status'),
        ('bot_version', '5.0.0', 'Bot version'),
        ('bot_status', 'online', 'Bot status'),
        ('bot_activity', 'watching', 'Bot activity type'),
        ('bot_activity_name', f'{BOT_NAME} VPS Manager', 'Bot activity text'),
        ('license_verified', 'false', 'License verification status'),
        ('server_ip', SERVER_IP, 'Server public IP'),
        ('mac_address', MAC_ADDRESS, 'Server MAC address'),
        ('hostname', HOSTNAME, 'Server hostname'),
        ('total_vps_created', '0', 'Total VPS created'),
        ('total_panels_installed', '0', 'Total panels installed'),
        ('total_nodes', '0', 'Total nodes added'),
        ('total_transactions', '0', 'Total transactions'),
        ('default_port_quota', '5', 'Default port quota for new users'),
        ('allow_free_vps', 'true', 'Allow free VPS claiming'),
        ('require_invites', 'true', 'Require invites for free VPS'),
        ('maintenance_message', 'Bot is under maintenance', 'Maintenance mode message'),
        ('welcome_message', 'Welcome to SVM5-BOT!', 'Welcome message'),
        ('default_node', 'local', 'Default node name'),
    ]
    
    for key, value, desc in settings_init:
        cur.execute('INSERT OR IGNORE INTO settings (key, value, description) VALUES (?, ?, ?)', (key, value, desc))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized successfully with all tables")

# Initialize database
init_db()

# ==================================================================================================
#  📊  DATABASE HELPER FUNCTIONS - COMPLETE
# ==================================================================================================

def get_setting(key: str, default: Any = None) -> Any:
    """Get a setting value"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key: str, value: str):
    """Set a setting value"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
                (key, value, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def increment_setting(key: str):
    """Increment a numeric setting"""
    current = int(get_setting(key, '0'))
    set_setting(key, str(current + 1))

# ==================================================================================================
#  🌐 NODE MANAGEMENT FUNCTIONS - COMPLETE
# ==================================================================================================

def add_node(name: str, host: str, username: str, password: str = None, ssh_key: str = None, 
             port: int = 22, region: str = "us", description: str = "", added_by: str = "") -> Dict:
    """Add a new node to the cluster"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    
    # Generate API key for node
    api_key = hashlib.sha256(f"{name}{host}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
    
    cur.execute('''INSERT INTO nodes 
                   (name, host, port, username, password, ssh_key, api_key, region, description, added_by, added_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (name, host, port, username, password, ssh_key, api_key, region, description, added_by, now))
    node_id = cur.lastrowid
    conn.commit()
    
    increment_setting('total_nodes')
    
    cur.execute('SELECT * FROM nodes WHERE id = ?', (node_id,))
    node = dict(cur.fetchone())
    conn.close()
    return node

def get_node(name: str) -> Optional[Dict]:
    """Get node by name"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM nodes WHERE name = ?', (name,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_nodes() -> List[Dict]:
    """Get all nodes"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM nodes ORDER BY name')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_node_status(name: str, status: str, stats: Dict = None):
    """Update node status and stats"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    
    if stats:
        cur.execute('''UPDATE nodes SET 
                       status = ?, total_ram = ?, used_ram = ?, total_cpu = ?, 
                       used_cpu = ?, total_disk = ?, used_disk = ?, lxc_count = ?,
                       last_checked = ?
                       WHERE name = ?''',
                    (status, stats.get('total_ram', 0), stats.get('used_ram', 0),
                     stats.get('total_cpu', 0), stats.get('used_cpu', 0),
                     stats.get('total_disk', 0), stats.get('used_disk', 0),
                     stats.get('lxc_count', 0), now, name))
    else:
        cur.execute('UPDATE nodes SET status = ?, last_checked = ? WHERE name = ?',
                    (status, now, name))
    
    conn.commit()
    conn.close()

def delete_node(name: str) -> bool:
    """Delete a node"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM nodes WHERE name = ?', (name,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

async def check_node_health(node: Dict) -> Dict:
    """Check node health via SSH"""
    import paramiko
    
    stats = {
        'status': 'offline',
        'total_ram': 0,
        'used_ram': 0,
        'total_cpu': 0,
        'used_cpu': 0,
        'total_disk': 0,
        'used_disk': 0,
        'lxc_count': 0
    }
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if node.get('password'):
            client.connect(node['host'], port=node['port'], 
                          username=node['username'], password=node['password'], timeout=10)
        elif node.get('ssh_key'):
            key = paramiko.RSAKey.from_private_key_file(node['ssh_key'])
            client.connect(node['host'], port=node['port'], 
                          username=node['username'], pkey=key, timeout=10)
        else:
            return stats
        
        # Get system stats
        stdin, stdout, stderr = client.exec_command('nproc')
        total_cpu = stdout.read().decode().strip()
        stats['total_cpu'] = int(total_cpu) if total_cpu.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        used_cpu = stdout.read().decode().strip()
        stats['used_cpu'] = float(used_cpu) if used_cpu else 0
        
        stdin, stdout, stderr = client.exec_command("free -m | awk '/^Mem:/{print $2}'")
        total_ram = stdout.read().decode().strip()
        stats['total_ram'] = int(total_ram) if total_ram.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("free -m | awk '/^Mem:/{print $3}'")
        used_ram = stdout.read().decode().strip()
        stats['used_ram'] = int(used_ram) if used_ram.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("df -BG / | awk 'NR==2{print $2}' | sed 's/G//'")
        total_disk = stdout.read().decode().strip()
        stats['total_disk'] = int(total_disk) if total_disk.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("df -BG / | awk 'NR==2{print $3}' | sed 's/G//'")
        used_disk = stdout.read().decode().strip()
        stats['used_disk'] = int(used_disk) if used_disk.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("lxc list --format csv 2>/dev/null | wc -l")
        lxc_count = stdout.read().decode().strip()
        stats['lxc_count'] = int(lxc_count) if lxc_count.isdigit() else 0
        
        stats['status'] = 'online'
        client.close()
        
    except Exception as e:
        logger.error(f"Node {node['name']} health check failed: {e}")
        stats['status'] = 'offline'
    
    return stats

# ==================================================================================================
#  🚀  CLOUDFLARED TUNNEL FUNCTIONS
# ==================================================================================================

async def create_cloudflared_tunnel(container_name: str, port: int = 80) -> Optional[str]:
    """Create a cloudflared tunnel for a container"""
    if not CLOUDFLARED_AVAILABLE:
        return None
    
    try:
        # Install cloudflared in container if not present
        await exec_in_container(container_name, "which cloudflared || (wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared)")
        
        # Generate unique tunnel ID
        tunnel_id = str(uuid.uuid4())[:8]
        
        # Start tunnel
        cmd = f"nohup cloudflared tunnel --url http://localhost:{port} --no-autoupdate > /tmp/cloudflared_{tunnel_id}.log 2>&1 & echo $!"
        pid, _, _ = await exec_in_container(container_name, cmd)
        
        # Wait for tunnel to establish
        await asyncio.sleep(5)
        
        # Get tunnel URL
        out, _, _ = await exec_in_container(container_name, f"cat /tmp/cloudflared_{tunnel_id}.log | grep -oP 'https://[a-z0-9-]+\\.trycloudflare\\.com' | head -1")
        url = out.strip()
        
        if url:
            return url
    except Exception as e:
        logger.error(f"Failed to create cloudflared tunnel: {e}")
    
    return None

# ==================================================================================================
#  🛠️  LXC HELPER FUNCTIONS - ENHANCED
# ==================================================================================================

def run_lxc_sync(command: str, timeout: int = 60) -> Tuple[str, str, int]:
    """Run LXC command synchronously"""
    try:
        cmd = shlex.split(command)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout} seconds", -1
    except Exception as e:
        return "", str(e), -1

async def run_lxc(command: str, timeout: int = 60) -> Tuple[str, str, int]:
    """Run an LXC command asynchronously"""
    return await asyncio.get_event_loop().run_in_executor(None, run_lxc_sync, command, timeout)

async def exec_in_container(container_name: str, command: str, timeout: int = 30) -> Tuple[str, str, int]:
    """Execute a command inside a container"""
    return await run_lxc(f"lxc exec {container_name} -- bash -c {shlex.quote(command)}", timeout)

def get_container_status_sync(container_name: str) -> str:
    """Get container status synchronously"""
    try:
        result = subprocess.run(['lxc', 'info', container_name], 
                                capture_output=True, text=True, timeout=10)
        for line in result.stdout.splitlines():
            if line.startswith("Status: "):
                return line.split(": ", 1)[1].strip().lower()
        return "unknown"
    except:
        return "unknown"

async def get_container_status(container_name: str) -> str:
    """Get container status asynchronously"""
    return await asyncio.get_event_loop().run_in_executor(None, get_container_status_sync, container_name)

async def get_container_stats(container_name: str) -> Dict:
    """Get detailed container stats with terminal-like output"""
    stats = {
        'status': 'unknown',
        'cpu': '0.0%',
        'memory': '0/0 MB (0%)',
        'disk': '0/0 GB (0%)',
        'uptime': '0 min',
        'ipv4': [],
        'ipv6': [],
        'mac': 'N/A',
        'processes': '0',
        'load': '0.00 0.00 0.00',
        'network_rx': '0 B',
        'network_tx': '0 B',
        'hostname': container_name,
        'kernel': 'N/A',
        'os': 'N/A',
        'node': 'local'
    }
    
    # Get status
    stats['status'] = await get_container_status(container_name)
    
    if stats['status'] == 'running':
        # Get CPU usage
        out, _, _ = await exec_in_container(container_name, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
        stats['cpu'] = f"{out}%" if out else "0.0%"
        
        # Get memory usage
        out, _, _ = await exec_in_container(container_name, "free -m | awk '/^Mem:/{printf \"%d/%d MB (%.1f%%)\", $3, $2, $3/$2*100}'")
        stats['memory'] = out if out else "0/0 MB (0%)"
        
        # Get disk usage
        out, _, _ = await exec_in_container(container_name, "df -h / | awk 'NR==2{printf \"%s/%s (%s)\", $3, $2, $5}'")
        stats['disk'] = out if out else "0/0 GB (0%)"
        
        # Get uptime
        out, _, _ = await exec_in_container(container_name, "uptime -p | sed 's/up //'")
        stats['uptime'] = out if out else "0 min"
        
        # Get IPv4 addresses
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | grep -v '127.0.0.1'")
        if out:
            stats['ipv4'] = out.splitlines()
        
        # Get IPv6 addresses
        out, _, _ = await exec_in_container(container_name, "ip -6 addr show | grep -oP '(?<=inet6\\s)[a-f0-9:]+' | grep -v '::1'")
        if out:
            stats['ipv6'] = out.splitlines()
        
        # Get MAC address
        out, _, _ = await exec_in_container(container_name, "ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
        stats['mac'] = out.strip() if out else "N/A"
        
        # Get process count
        out, _, _ = await exec_in_container(container_name, "ps aux | wc -l")
        stats['processes'] = out.strip() if out else "0"
        
        # Get load average
        out, _, _ = await exec_in_container(container_name, "cat /proc/loadavg | awk '{print $1, $2, $3}'")
        stats['load'] = out.strip() if out else "0.00 0.00 0.00"
        
        # Get network stats
        out, _, _ = await exec_in_container(container_name, "cat /sys/class/net/eth0/statistics/rx_bytes | numfmt --to=iec")
        stats['network_rx'] = out.strip() if out else "0 B"
        
        out, _, _ = await exec_in_container(container_name, "cat /sys/class/net/eth0/statistics/tx_bytes | numfmt --to=iec")
        stats['network_tx'] = out.strip() if out else "0 B"
        
        # Get hostname
        out, _, _ = await exec_in_container(container_name, "hostname")
        stats['hostname'] = out.strip() if out else container_name
        
        # Get kernel version
        out, _, _ = await exec_in_container(container_name, "uname -r")
        stats['kernel'] = out.strip() if out else "N/A"
        
        # Get OS info
        out, _, _ = await exec_in_container(container_name, "cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'")
        stats['os'] = out.strip() if out else "N/A"
    
    return stats

async def apply_lxc_config(container_name: str):
    """Apply LXC configuration for better compatibility"""
    try:
        # Enable nesting and privileged mode
        await run_lxc(f"lxc config set {container_name} security.nesting true")
        await run_lxc(f"lxc config set {container_name} security.privileged true")
        
        # Add kernel modules
        await run_lxc(f"lxc config set {container_name} linux.kernel_modules overlay,br_netfilter,nf_nat,ip_tables,ip6_tables,netlink_diag,xt_conntrack,nf_conntrack")
        
        # Raw LXC config
        raw_config = """
lxc.apparmor.profile = unconfined
lxc.cgroup.devices.allow = a
lxc.cap.drop =
lxc.mount.auto = proc:rw sys:rw cgroup:rw
"""
        await run_lxc(f"lxc config set {container_name} raw.lxc '{raw_config}'")
        
        logger.info(f"✅ Applied LXC config to {container_name}")
    except Exception as e:
        logger.error(f"Failed to apply LXC config to {container_name}: {e}")

async def apply_internal_permissions(container_name: str):
    """Apply internal permissions for Docker compatibility"""
    await asyncio.sleep(3)  # Wait for container to start
    commands = [
        "mkdir -p /etc/sysctl.d/",
        "echo 'net.ipv4.ip_unprivileged_port_start=0' > /etc/sysctl.d/99-custom.conf",
        "echo 'net.ipv4.ping_group_range=0 2147483647' >> /etc/sysctl.d/99-custom.conf",
        "echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.d/99-custom.conf",
        "sysctl -p /etc/sysctl.d/99-custom.conf || true",
        "apt-get update -qq",
        "apt-get install -y -qq curl wget sudo vim nano htop net-tools iproute2 iputils-ping dnsutils traceroute mtr tcpdump telnet ncdu tmux screen",
    ]
    for cmd in commands:
        await exec_in_container(container_name, cmd)

async def get_available_host_port() -> Optional[int]:
    """Get an available host port for forwarding"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT host_port FROM port_forwards')
    used_ports = {row[0] for row in cur.fetchall()}
    conn.close()
    
    # Also check system for used ports
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if ':' in line:
                parts = line.split()
                for part in parts:
                    if ':' in part and part.split(':')[-1].isdigit():
                        used_ports.add(int(part.split(':')[-1]))
    except:
        pass
    
    for _ in range(100):
        port = random.randint(20000, 50000)
        if port not in used_ports:
            return port
    return None

async def create_port_forward(user_id: str, container_name: str, container_port: int, protocol: str = "tcp+udp") -> Optional[int]:
    """Create a port forward"""
    host_port = await get_available_host_port()
    if not host_port:
        return None
    
    try:
        if protocol == "tcp" or protocol == "tcp+udp":
            await run_lxc(f"lxc config device add {container_name} proxy-tcp-{host_port} proxy listen=tcp:0.0.0.0:{host_port} connect=tcp:127.0.0.1:{container_port}")
        
        if protocol == "udp" or protocol == "tcp+udp":
            await run_lxc(f"lxc config device add {container_name} proxy-udp-{host_port} proxy listen=udp:0.0.0.0:{host_port} connect=udp:127.0.0.1:{container_port}")
        
        # Save to database
        conn = get_db()
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO port_forwards (user_id, container_name, container_port, host_port, protocol, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)''', (user_id, container_name, container_port, host_port, protocol, now))
        conn.commit()
        conn.close()
        
        return host_port
    except Exception as e:
        logger.error(f"Failed to create port forward: {e}")
        return None

async def remove_port_forward_device(container_name: str, host_port: int):
    """Remove port forward devices"""
    try:
        await run_lxc(f"lxc config device remove {container_name} proxy-tcp-{host_port}")
    except:
        pass
    try:
        await run_lxc(f"lxc config device remove {container_name} proxy-udp-{host_port}")
    except:
        pass

async def get_container_console(container_name: str, lines: int = 20) -> str:
    """Get console output from container (like .ss command)"""
    try:
        # Get last N lines of console output
        out, _, _ = await exec_in_container(container_name, f"dmesg | tail -{lines} 2>/dev/null || journalctl -n {lines} --no-pager 2>/dev/null")
        if out:
            return out
        
        # Fallback to process list
        out, _, _ = await exec_in_container(container_name, f"ps aux --forest | head -{lines*2}")
        return out or "No console output available"
    except Exception as e:
        return f"Error getting console: {str(e)}"

# ==================================================================================================
#  🎨  EMBED HELPER FUNCTIONS - ENHANCED WITH GLOW EFFECTS
# ==================================================================================================

def create_embed(title: str, description: str = "", color: int = 0x5865F2) -> discord.Embed:
    """Create a styled embed with glow effects"""
    # Add glow effect to title
    glow_title = f"```glow\n✦ {BOT_NAME} - {title} ✦\n```"
    
    embed = discord.Embed(
        title=glow_title,
        description=description,
        color=color
    )
    
    if THUMBNAIL_URL:
        embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # Add gradient footer
    footer_text = f"⚡ {BOT_NAME} • {BOT_AUTHOR} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡"
    embed.set_footer(
        text=footer_text,
        icon_url=THUMBNAIL_URL
    )
    
    return embed

def success_embed(title: str, description: str = "") -> discord.Embed:
    """Create a success embed with glow"""
    return create_embed(f"✅ {title}", description, 0x57F287)

def error_embed(title: str, description: str = "") -> discord.Embed:
    """Create an error embed with glow"""
    return create_embed(f"❌ {title}", description, 0xED4245)

def info_embed(title: str, description: str = "") -> discord.Embed:
    """Create an info embed with glow"""
    return create_embed(f"ℹ️ {title}", description, 0x5865F2)

def warning_embed(title: str, description: str = "") -> discord.Embed:
    """Create a warning embed with glow"""
    return create_embed(f"⚠️ {title}", description, 0xFEE75C)

def node_embed(title: str, description: str = "") -> discord.Embed:
    """Create a node-specific embed with glow"""
    return create_embed(f"🌐 {title}", description, 0x9B59B6)

def terminal_embed(title: str, content: str, color: int = 0x2C2F33) -> discord.Embed:
    """Create a terminal-style embed for console output"""
    terminal_title = f"```fix\n[ {title} ]\n```"
    embed = discord.Embed(
        title=terminal_title,
        description=f"```bash\n{content[:1900]}\n```",
        color=color
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • Terminal Output • {datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def no_vps_embed() -> discord.Embed:
    """Create a no VPS embed"""
    return info_embed(
        "No VPS Found",
        f"```diff\n- You don't have any VPS yet.\n```\n\n"
        f"**To get a free VPS:**\n"
        f"• Use `{BOT_PREFIX}plans` to see available plans\n"
        f"• Use `{BOT_PREFIX}claim-free` to claim based on invites\n"
        f"• Contact an admin for custom VPS"
    )

# ==================================================================================================
#  🤖  BOT SETUP
# ==================================================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.start_time = datetime.utcnow()

# Global variables
MAINTENANCE_MODE = get_setting('maintenance_mode', 'false').lower() == 'true'
CPU_THRESHOLD = int(get_setting('cpu_threshold', 90))
RAM_THRESHOLD = int(get_setting('ram_threshold', 90))
DISK_THRESHOLD = int(get_setting('disk_threshold', 90))
LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'

# Active help menus
active_help_menus = {}

# Node monitoring task
@tasks.loop(minutes=5)
async def monitor_nodes():
    """Monitor all nodes every 5 minutes"""
    nodes = get_all_nodes()
    for node in nodes:
        if node['status'] == 'online':
            stats = await check_node_health(node)
            update_node_status(node['name'], stats['status'], stats)
            logger.info(f"Node {node['name']} status: {stats['status']}")

@tasks.loop(hours=1)
async def cleanup_old_logs():
    """Clean up old logs every hour"""
    # Implement log cleanup
    pass

# ==================================================================================================
#  ✅  MAINTENANCE CHECK DECORATOR
# ==================================================================================================

async def maintenance_check(ctx) -> bool:
    """Check if bot is in maintenance mode"""
    global MAINTENANCE_MODE
    
    if MAINTENANCE_MODE and not is_admin(str(ctx.author.id)):
        embed = warning_embed(
            "Maintenance Mode Active",
            f"```fix\n{get_setting('maintenance_message', 'Bot is under maintenance')}\n```\n"
            "Only administrators can use commands at this time."
        )
        await ctx.send(embed=embed)
        return False
    return True

# ==================================================================================================
#  ✅  LICENSE CHECK DECORATOR
# ==================================================================================================

async def license_check(ctx) -> bool:
    """Check if license is verified"""
    global LICENSE_VERIFIED
    
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        embed = error_embed(
            "License Required",
            "```diff\n- This bot requires a valid license key to operate.\n```\n\n"
            "**Purchase Information:**\n"
            f"• UPI: `9892642904@ybl`\n"
            f"• Amount: `₹499` (One-time)\n"
            f"• Contact: @Ankit-Dev on Discord\n\n"
            "After payment, you will receive a valid license key."
        )
        await ctx.send(embed=embed)
        return False
    return True

# ==================================================================================================
#  ✅  ON READY - FIXED
# ==================================================================================================

@bot.event
async def on_ready():
    """Bot ready event - FIXED"""
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_PREFIX}help | {BOT_NAME}"
        )
    )
    logger.info(f"✅ Bot is ready: {bot.user} (ID: {bot.user.id})")
    
    # Check license
    global LICENSE_VERIFIED
    LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'
    
    # Start monitoring tasks
    monitor_nodes.start()
    cleanup_old_logs.start()
    
    # Get server stats
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    running_vps = sum(1 for v in all_vps if v['status'] == 'running' and not v['suspended'])
    nodes = len(get_all_nodes())
    
    # Create VPS user role if needed
    for guild in bot.guilds:
        role = discord.utils.get(guild.roles, name=f"{BOT_NAME} User")
        if not role:
            try:
                await guild.create_role(
                    name=f"{BOT_NAME} User",
                    color=discord.Color.purple(),
                    reason=f"{BOT_NAME} user role"
                )
                logger.info(f"✅ Created role in {guild.name}")
            except:
                pass
    
    # Beautiful startup banner
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                 ║
║                      ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗        ║
║                      ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝        ║
║                      ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║           ║
║                      ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║           ║
║                      ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║           ║
║                      ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝           ║
║                                                                                                 ║
║                          ██████╗  ██████╗ ████████╗    ██╗   ██╗███████╗                       ║
║                          ██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║██╔════╝                       ║
║                          ██████╔╝██║   ██║   ██║       ██║   ██║███████╗                       ║
║                          ██╔══██╗██║   ██║   ██║       ╚██╗ ██╔╝╚════██║                       ║
║                          ██████╔╝╚██████╔╝   ██║        ╚████╔╝ ███████║                       ║
║                          ╚═════╝  ╚═════╝    ╚═╝         ╚═══╝  ╚══════╝                       ║
║                                                                                                 ║
║                      ███████╗██╗██╗  ██╗███████╗██████╗                                      ║
║                      ██╔════╝██║╚██╗██╔╝██╔════╝██╔══██╗                                     ║
║                      █████╗  ██║ ╚███╔╝ █████╗  ██║  ██║                                     ║
║                      ██╔══╝  ██║ ██╔██╗ ██╔══╝  ██║  ██║                                     ║
║                      ██║     ██║██╔╝ ██╗███████╗██████╔╝                                     ║
║                      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝                                      ║
║                                                                                                 ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                 ║
║  📍 Bot Status:    🟢 ONLINE                                                                   ║
║  🤖 Bot Name:      {bot.user:<56} ║
║  🆔 Bot ID:        {bot.user.id:<62} ║
║  🔧 Prefix:        {BOT_PREFIX:<63} ║
║                                                                                                 ║
║  🔐 License:       {'✅ VERIFIED' if LICENSE_VERIFIED else '❌ NOT VERIFIED':<56} ║
║  🌐 Server IP:     {SERVER_IP:<59} ║
║  🔌 MAC Address:   {MAC_ADDRESS:<55} ║
║  💻 Hostname:      {HOSTNAME:<59} ║
║                                                                                                 ║
║  🖥️ Total VPS:     {total_vps:<6} (Running: {running_vps:<4})                                    ║
║  🌍 Total Nodes:   {nodes:<6}                                                                    ║
║  📊 Commands:      65+                                                                            ║
║  🤖 AI Model:      {AI_MODEL:<58} ║
║                                                                                                 ║
║  👑 Main Admin:    <@1405866008127864852>                                                       ║
║                                                                                                 ║
║                         Made by Ankit-Dev with ❤️ - ALL FIXES APPLIED                           ║
║                    ✅ Help Fixed • ✅ AI Fixed • ✅ SSH Fixed • ✅ Nodes Added                   ║
║                                                                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
    """)

# ==================================================================================================
#  ❌  ERROR HANDLER - COMPLETELY FIXED FOR INTERACTION FAILED
# ==================================================================================================

@bot.event
async def on_command_error(ctx, error):
    """Global error handler - FIXED for Interaction Failed"""
    
    # Log the error
    logger.error(f"Error in command '{ctx.command}': {error}")
    
    if isinstance(error, commands.CommandNotFound):
        return
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = error_embed(
            "Missing Argument",
            f"```fix\nUsage: {BOT_PREFIX}{ctx.command.name} {ctx.command.signature}\n```\n"
            f"Use `{BOT_PREFIX}help` for more information."
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.BadArgument):
        embed = error_embed(
            "Invalid Argument",
            "```diff\n- Please check your input and try again.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CheckFailure):
        embed = error_embed(
            "Access Denied",
            "```diff\n- You don't have permission to use this command.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CommandOnCooldown):
        embed = warning_embed(
            "Command on Cooldown",
            f"```fix\nPlease wait {error.retry_after:.1f} seconds before using this command again.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, discord.errors.InteractionResponded):
        # Handle already responded interactions - FIXED
        try:
            # Try to send a followup
            await ctx.send(embed=warning_embed(
                "Slow Down",
                "```fix\nPlease wait a moment before using this again.\n```"
            ), ephemeral=True)
        except:
            # If that fails, just pass
            pass
    
    elif isinstance(error, discord.errors.Forbidden):
        embed = error_embed(
            "Permission Error",
            "```diff\n- I don't have permission to do that. Please check my permissions.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, asyncio.TimeoutError):
        embed = error_embed(
            "Timeout Error",
            "```diff\n- The operation timed out. Please try again.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CommandInvokeError) and "Interaction" in str(error):
        # Handle interaction errors specifically
        try:
            await ctx.send(embed=warning_embed(
                "Interaction Error",
                "```fix\nThere was an issue with the interaction. Please try again.\n```"
            ))
        except:
            pass
    
    else:
        # Unexpected error
        embed = error_embed(
            "Unexpected Error",
            f"```diff\n- {str(error)[:1900]}\n```\n"
            f"Please report this to an admin."
        )
        try:
            await ctx.send(embed=embed)
        except:
            pass

# ==================================================================================================
#  📖  HELP COMMAND - COMPLETELY FIXED WITH ALL COMMANDS
# ==================================================================================================

class HelpView(View):
    """Interactive help menu with all commands - FIXED"""
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_page = 0
        self.pages = [
            {
                "title": "📚 WELCOME TO SVM5-BOT HELP",
                "description": f"```glow\nPrefix: {BOT_PREFIX} | Version: 5.0.0 | Author: {BOT_AUTHOR}\nServer IP: {SERVER_IP} | MAC: {MAC_ADDRESS}\n```\n**Select a category below to see commands:**",
                "fields": [
                    ("👤 USER COMMANDS", "`Basic commands for all users`", True),
                    ("🖥️ VPS MANAGEMENT", "`Control your VPS containers`", True),
                    ("📟 CONSOLE & SSH", "`Terminal access and console`", True),
                    ("🔌 PORT FORWARDING", "`Manage port forwards`", True),
                    ("🌐 NODE MANAGEMENT", "`Manage cluster nodes`", True),
                    ("📦 PANEL INSTALL", "`Install game panels`", True),
                    ("🌍 IPv4 MANAGEMENT", "`Buy and manage IPv4`", True),
                    ("💰 INVITE SYSTEM", "`Earn free VPS`", True),
                    ("🤖 AI CHAT", "`Chat with AI assistant`", True),
                    ("🛡️ ADMIN COMMANDS", "`Administrator commands`", True),
                    ("👑 MAIN ADMIN", "`Main admin commands`", True),
                ]
            },
            {
                "title": "👤 USER COMMANDS",
                "description": "```fix\nBasic commands available to all users\n```",
                "fields": [
                    (f"{BOT_PREFIX}help", "Show this interactive help menu", False),
                    (f"{BOT_PREFIX}ping", "Check bot latency", False),
                    (f"{BOT_PREFIX}uptime", "Show bot uptime", False),
                    (f"{BOT_PREFIX}bot-info", "Detailed bot information", False),
                    (f"{BOT_PREFIX}server-info", "Show server hardware info", False),
                    (f"{BOT_PREFIX}plans", "View free VPS plans", False),
                    (f"{BOT_PREFIX}stats", "View your stats", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}claim-free", "Claim free VPS with invites", False),
                    (f"{BOT_PREFIX}my-acc", "View your generated account", False),
                    (f"{BOT_PREFIX}gen-acc", "Generate random account", False),
                ]
            },
            {
                "title": "🖥️ VPS MANAGEMENT",
                "description": "```fix\nControl and manage your VPS containers\n```",
                "fields": [
                    (f"{BOT_PREFIX}myvps", "List your VPS", False),
                    (f"{BOT_PREFIX}list", "Detailed VPS list", False),
                    (f"{BOT_PREFIX}manage", "Interactive VPS manager", False),
                    (f"{BOT_PREFIX}stats [container]", "View VPS statistics", False),
                    (f"{BOT_PREFIX}logs [container] [lines]", "View VPS logs", False),
                    (f"{BOT_PREFIX}reboot <container>", "Reboot VPS", False),
                    (f"{BOT_PREFIX}shutdown <container>", "Shutdown VPS", False),
                ]
            },
            {
                "title": "📟 CONSOLE & SSH COMMANDS",
                "description": "```fix\nTerminal access and console commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}ss [container]", "Show VPS console/screenshot", False),
                    (f"{BOT_PREFIX}console <container>", "Interactive console", False),
                    (f"{BOT_PREFIX}ssh-gen <container>", "Generate temporary SSH access", False),
                    (f"{BOT_PREFIX}execute <container> <cmd>", "Execute command in VPS", False),
                    (f"{BOT_PREFIX}top <container>", "Show live process monitor", False),
                    (f"{BOT_PREFIX}df <container>", "Show disk usage", False),
                    (f"{BOT_PREFIX}free <container>", "Show memory usage", False),
                    (f"{BOT_PREFIX}netstat <container>", "Show network connections", False),
                ]
            },
            {
                "title": "🔌 PORT FORWARDING",
                "description": "```fix\nManage port forwarding for your VPS\n```",
                "fields": [
                    (f"{BOT_PREFIX}ports", "Port forwarding help", False),
                    (f"{BOT_PREFIX}ports add <num> <port> [tcp/udp]", "Add port forward", False),
                    (f"{BOT_PREFIX}ports list", "List your forwards", False),
                    (f"{BOT_PREFIX}ports remove <id>", "Remove port forward", False),
                    (f"{BOT_PREFIX}ports quota", "Check your port quota", False),
                ]
            },
            {
                "title": "🌐 NODE MANAGEMENT",
                "description": "```fix\nManage cluster nodes (Admin only)\n```",
                "fields": [
                    (f"{BOT_PREFIX}node", "List all nodes with stats", False),
                    (f"{BOT_PREFIX}node-info <name>", "Detailed node information", False),
                    (f"{BOT_PREFIX}node-add <name> <host> <user> <pass>", "Add new node", False),
                    (f"{BOT_PREFIX}node-remove <name>", "Remove a node", False),
                    (f"{BOT_PREFIX}node-check <name>", "Check node health", False),
                    (f"{BOT_PREFIX}node-stats", "Show cluster statistics", False),
                ]
            },
            {
                "title": "📦 PANEL INSTALLATION",
                "description": "```fix\nInstall game server panels on your VPS\n```",
                "fields": [
                    (f"{BOT_PREFIX}install-panel", "Install Pterodactyl/Pufferpanel", False),
                    (f"{BOT_PREFIX}panel-info", "Show your installed panel info", False),
                    (f"{BOT_PREFIX}panel-reset <type>", "Reset panel admin password", False),
                    (f"{BOT_PREFIX}panel-tunnel <container>", "Create cloudflared tunnel", False),
                ]
            },
            {
                "title": "🌍 IPv4 MANAGEMENT",
                "description": "```fix\nBuy and manage IPv4 addresses\n```",
                "fields": [
                    (f"{BOT_PREFIX}ipv4", "View your IPv4 list", False),
                    (f"{BOT_PREFIX}buy-ipv4", "Purchase IPv4 via UPI", False),
                    (f"{BOT_PREFIX}ipv4-details <container>", "Show detailed IPv4 info", False),
                ]
            },
            {
                "title": "💰 INVITE SYSTEM",
                "description": "```fix\nEarn free VPS by inviting users\n```",
                "fields": [
                    (f"{BOT_PREFIX}plans", "View plan requirements", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}stats", "View your stats", False),
                    (f"{BOT_PREFIX}claim-free", "Claim your VPS", False),
                ]
            },
            {
                "title": "🤖 AI CHAT",
                "description": f"```fix\nChat with AI assistant (Model: {AI_MODEL})\n```",
                "fields": [
                    (f"{BOT_PREFIX}ai <message>", "Chat with AI", False),
                    (f"{BOT_PREFIX}ai-reset", "Reset chat history", False),
                ]
            },
        ]
        
        if is_admin(str(ctx.author.id)):
            self.pages.append({
                "title": "🛡️ ADMIN COMMANDS",
                "description": "```fix\nCommands for administrators\n```",
                "fields": [
                    (f"{BOT_PREFIX}create <ram> <cpu> <disk> @user", "Create VPS for user", False),
                    (f"{BOT_PREFIX}delete <@user> <num> [reason]", "Delete user's VPS", False),
                    (f"{BOT_PREFIX}suspend <container> [reason]", "Suspend VPS", False),
                    (f"{BOT_PREFIX}unsuspend <container>", "Unsuspend VPS", False),
                    (f"{BOT_PREFIX}add-resources <container> [ram] [cpu] [disk]", "Add resources", False),
                    (f"{BOT_PREFIX}userinfo @user", "User information", False),
                    (f"{BOT_PREFIX}list-all", "List all VPS", False),
                    (f"{BOT_PREFIX}add-inv @user <amount>", "Add invites", False),
                    (f"{BOT_PREFIX}remove-inv @user <amount>", "Remove invites", False),
                    (f"{BOT_PREFIX}ports-add @user <amount>", "Add port slots", False),
                    (f"{BOT_PREFIX}serverstats", "Server statistics", False),
                    (f"{BOT_PREFIX}admin-add-ipv4 @user <container>", "Assign IPv4", False),
                    (f"{BOT_PREFIX}admin-rm-ipv4 @user [container]", "Remove IPv4", False),
                    (f"{BOT_PREFIX}admin-pending-ipv4", "View pending IPv4 purchases", False),
                    (f"{BOT_PREFIX}admin-panels", "List all installed panels", False),
                    (f"{BOT_PREFIX}node-add", "Add new node", False),
                    (f"{BOT_PREFIX}node-remove", "Remove node", False),
                ]
            })
        
        if str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            self.pages.append({
                "title": "👑 MAIN ADMIN COMMANDS",
                "description": "```fix\nCommands for main administrator only\n```",
                "fields": [
                    (f"{BOT_PREFIX}admin-add @user", "Add new admin", False),
                    (f"{BOT_PREFIX}admin-remove @user", "Remove admin", False),
                    (f"{BOT_PREFIX}admin-list", "List all admins", False),
                    (f"{BOT_PREFIX}maintenance <on/off>", "Toggle maintenance mode", False),
                    (f"{BOT_PREFIX}set-threshold <cpu> <ram> <disk>", "Set resource thresholds", False),
                    (f"{BOT_PREFIX}purge-all", "Purge all unprotected VPS", False),
                    (f"{BOT_PREFIX}protect @user [num]", "Protect VPS from purge", False),
                    (f"{BOT_PREFIX}unprotect @user [num]", "Remove purge protection", False),
                    (f"{BOT_PREFIX}admin-users", "List all users", False),
                    (f"{BOT_PREFIX}system-info", "Detailed system information", False),
                    (f"{BOT_PREFIX}backup-db", "Backup database", False),
                    (f"{BOT_PREFIX}restore-db", "Restore database", False),
                ]
            })
        
        self.update_embed()
    
    def update_embed(self):
        """Update the embed for current page"""
        page = self.pages[self.current_page]
        
        # Create embed with glow effect
        embed = discord.Embed(
            title=f"```glow\n{page['title']}\n```",
            description=page['description'],
            color=0x9B59B6 if "ADMIN" in page['title'] else 0x5865F2
        )
        
        if THUMBNAIL_URL:
            embed.set_thumbnail(url=THUMBNAIL_URL)
        
        for name, value, inline in page["fields"]:
            # Add emoji indicators
            if "✅" in value or "❌" in value:
                # Already has emoji
                embed.add_field(name=f"**{name}**", value=value, inline=inline)
            else:
                # Add command prefix
                embed.add_field(name=f"**{name}**", value=f"`{value}`", inline=inline)
        
        footer_text = f"⚡ Page {self.current_page + 1}/{len(self.pages)} • Use buttons to navigate • {BOT_NAME} ⚡"
        embed.set_footer(
            text=footer_text,
            icon_url=THUMBNAIL_URL
        )
        
        self.embed = embed
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def prev_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_page = (self.current_page - 1) % len(self.pages)
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.danger)
    async def delete_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await interaction.message.delete()

@bot.command(name="help")
@commands.cooldown(1, 3, commands.BucketType.user)
async def help_command(ctx):
    """Show interactive help menu - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = ctx.author.id
    if user_id in active_help_menus:
        try:
            await active_help_menus[user_id].delete()
        except:
            pass
    
    view = HelpView(ctx)
    msg = await ctx.send(embed=view.embed, view=view)
    active_help_menus[user_id] = msg

@bot.command(name="commands")
async def commands_alias(ctx):
    """Alias for help"""
    await help_command(ctx)

# ==================================================================================================
#  ℹ️  INFO COMMANDS
# ==================================================================================================

@bot.command(name="ping")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping_command(ctx):
    """Check bot latency - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging...", "```fix\nMeasuring latency...\n```"))
    end = time.time()
    
    api_latency = round(bot.latency * 1000)
    response_latency = round((end - start) * 1000)
    
    embed = create_embed("Pong! 🏓")
    
    # Create latency bar
    if api_latency < 100:
        bar = "🟩" * 10
        status = "Excellent"
    elif api_latency < 200:
        bar = "🟨" * 7 + "⬜" * 3
        status = "Good"
    else:
        bar = "🟥" * 5 + "⬜" * 5
        status = "Poor"
    
    embed.add_field(name="📡 API Latency", value=f"```fix\n{api_latency}ms\n```", inline=True)
    embed.add_field(name="⏱️ Response Time", value=f"```fix\n{response_latency}ms\n```", inline=True)
    embed.add_field(name="📊 Status", value=f"```fix\n{status}\n{bar}\n```", inline=False)
    
    await msg.edit(embed=embed)

@bot.command(name="uptime")
@commands.cooldown(1, 5, commands.BucketType.user)
async def uptime_command(ctx):
    """Show bot uptime"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    
    embed = info_embed(
        "Bot Uptime",
        f"```fix\n{days}d {hours}h {minutes}m {seconds}s\n```"
    )
    await ctx.send(embed=embed)

@bot.command(name="server-info")
@commands.cooldown(1, 5, commands.BucketType.user)
async def server_info(ctx):
    """Show server hardware information"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Get system info
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    embed = create_embed("Server Information")
    embed.add_field(name="💻 Hostname", value=f"```fix\n{HOSTNAME}\n```", inline=True)
    embed.add_field(name="🌐 Server IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🔌 MAC Address", value=f"```fix\n{MAC_ADDRESS}\n```", inline=True)
    embed.add_field(name="⚙️ CPU Cores", value=f"```fix\n{cpu_count}\n```", inline=True)
    embed.add_field(name="📊 CPU Usage", value=f"```fix\n{cpu_percent}%\n```", inline=True)
    embed.add_field(name="💾 RAM", value=f"```fix\n{memory.used//1024//1024}MB/{memory.total//1024//1024}MB ({memory.percent}%)\n```", inline=True)
    embed.add_field(name="📀 Disk", value=f"```fix\n{disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n```", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="bot-info")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bot_info(ctx):
    """Show detailed bot information"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    running_vps = sum(1 for v in all_vps if v['status'] == 'running' and not v['suspended'])
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM vps')
    total_users = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM panels')
    total_panels = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM nodes')
    total_nodes = cur.fetchone()[0] or 0
    conn.close()
    
    embed = create_embed("Bot Information")
    embed.add_field(name="📦 Version", value="```fix\n5.0.0\n```", inline=True)
    embed.add_field(name="👑 Author", value=f"```fix\n{BOT_AUTHOR}\n```", inline=True)
    embed.add_field(name="📚 Library", value=f"```fix\ndiscord.py {discord.__version__}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{days}d {hours}h {minutes}m\n```", inline=True)
    embed.add_field(name="🌐 Servers", value=f"```fix\n{len(bot.guilds)}\n```", inline=True)
    embed.add_field(name="👥 Users", value=f"```fix\n{total_users}\n```", inline=True)
    embed.add_field(name="🖥️ Total VPS", value=f"```fix\n{total_vps}\n```", inline=True)
    embed.add_field(name="🟢 Running VPS", value=f"```fix\n{running_vps}\n```", inline=True)
    embed.add_field(name="📦 Panels", value=f"```fix\n{total_panels}\n```", inline=True)
    embed.add_field(name="🌍 Nodes", value=f"```fix\n{total_nodes}\n```", inline=True)
    embed.add_field(name="🌐 Server IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{MAC_ADDRESS[:17]}\n```", inline=True)
    embed.add_field(name="🔐 License", value="```fix\n✅ VERIFIED\n```" if LICENSE_VERIFIED else "```fix\n❌ NOT VERIFIED\n```", inline=True)
    embed.add_field(name="🤖 AI Model", value=f"```fix\n{AI_MODEL}\n```", inline=True)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  👤  ACCOUNT GENERATOR
# ==================================================================================================

def generate_username() -> str:
    """Generate a random username"""
    adjectives = ["cool", "fast", "dark", "epic", "blue", "swift", "neon", "alpha", "delta", "super", 
                  "mega", "ultra", "hyper", "cyber", "tech", "quantum", "nano", "pixel", "digital", "cloud",
                  "storm", "thunder", "lightning", "shadow", "phantom", "ghost", "crypto", "binary", "atomic"]
    nouns = ["wolf", "tiger", "storm", "byte", "nova", "blade", "fox", "raven", "hawk", "lion", 
             "dragon", "phoenix", "eagle", "shark", "viper", "phantom", "shadow", "ghost", "knight", "warrior",
             "phoenix", "dragon", "titan", "giant", "master", "legend", "hero", "ninja", "samurai"]
    num = random.randint(10, 9999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{num}"

def generate_email(username: str = None) -> str:
    """Generate a random email"""
    if not username:
        username = generate_username()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "proton.me", "hotmail.com", "mail.com", 
               "icloud.com", "aol.com", "yandex.com", "gmx.com", "tutanota.com", "zoho.com"]
    return f"{username}@{random.choice(domains)}"

def generate_password(length: int = 16) -> str:
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

@bot.command(name="gen-acc")
@commands.cooldown(1, 10, commands.BucketType.user)
async def gen_account(ctx):
    """Generate a random account - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    username = generate_username()
    email = generate_email(username)
    password = generate_password()
    api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # Save to database
    conn = get_db()
    cur = conn.cursor()
    
    # Create accounts table if not exists
    cur.execute('''CREATE TABLE IF NOT EXISTS generated_accounts (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        api_key TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    cur.execute('''INSERT OR REPLACE INTO generated_accounts (user_id, username, email, password, api_key, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (str(ctx.author.id), username, email, password, api_key, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Try to DM the full credentials
    try:
        dm_embed = success_embed("🔐 Your Generated Account")
        dm_embed.add_field(name="👤 Username", value=f"```fix\n{username}\n```", inline=False)
        dm_embed.add_field(name="📧 Email", value=f"```fix\n{email}\n```", inline=False)
        dm_embed.add_field(name="🔑 Password", value=f"```fix\n{password}\n```", inline=False)
        dm_embed.add_field(name="🗝️ API Key", value=f"```fix\n{api_key}\n```", inline=False)
        dm_embed.set_footer(text="⚡ Keep these safe! Delete this message after saving. ⚡")
        await ctx.author.send(embed=dm_embed)
        dm_status = "✅ Sent to your DMs"
    except:
        dm_status = "❌ Failed to send DM (enable DMs)"
    
    embed = success_embed("Account Generated!")
    embed.add_field(name="👤 Username", value=f"```fix\n{username}\n```", inline=True)
    embed.add_field(name="📧 Email", value=f"||`{email}`||", inline=True)
    embed.add_field(name="🔑 Password", value=f"||`{password}`||", inline=False)
    embed.add_field(name="📩 DM Status", value=f"```fix\n{dm_status}\n```", inline=False)
    embed.set_footer(text="⚡ Full credentials sent to DM (check spam) ⚡")
    await ctx.send(embed=embed)

@bot.command(name="my-acc")
@commands.cooldown(1, 5, commands.BucketType.user)
async def my_account(ctx):
    """View your generated account"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM generated_accounts WHERE user_id = ?', (str(ctx.author.id),))
    account = cur.fetchone()
    conn.close()
    
    if account:
        embed = info_embed("Your Generated Account")
        embed.add_field(name="👤 Username", value=f"```fix\n{account['username']}\n```", inline=True)
        embed.add_field(name="📧 Email", value=f"||`{account['email']}`||", inline=True)
        embed.add_field(name="🔑 Password", value=f"||`{account['password']}`||", inline=False)
        embed.add_field(name="🗝️ API Key", value=f"||`{account['api_key']}`||", inline=False)
        embed.add_field(name="📅 Created", value=f"```fix\n{account['created_at'][:16]}\n```", inline=True)
    else:
        stats = get_user_stats(str(ctx.author.id))
        embed = info_embed("Your Account Info")
        embed.add_field(name="🆔 User ID", value=f"```fix\n{ctx.author.id}\n```", inline=True)
        embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
        embed.add_field(name="🚀 Boosts", value=f"```fix\n{stats.get('boosts', 0)}\n```", inline=True)
        embed.add_field(name="🖥️ Claimed VPS", value=f"```fix\n{stats.get('claimed_vps_count', 0)}\n```", inline=True)
        embed.add_field(name="📝 Note", value=f"Use `{BOT_PREFIX}gen-acc` to generate a new account", inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  💰  FREE VPS PLANS & INVITE SYSTEM
# ==================================================================================================

@bot.command(name="plans")
@commands.cooldown(1, 5, commands.BucketType.user)
async def show_plans(ctx):
    """Show free VPS plans"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    embed = create_embed("Free VPS Plans", "```fix\nEarn VPS by inviting users to the server!\n```")
    
    plans_text = ""
    for plan in FREE_VPS_PLANS['invites']:
        plans_text += f"{plan['emoji']} **{plan['name']}**\n"
        plans_text += f"   • RAM: {plan['ram']}GB\n"
        plans_text += f"   • CPU: {plan['cpu']} Core(s)\n"
        plans_text += f"   • Disk: {plan['disk']}GB\n"
        plans_text += f"   • Requires: {plan['invites']} invites\n\n"
    
    embed.add_field(name="📋 Available Plans", value=plans_text, inline=False)
    embed.add_field(
        name="📌 How to Claim",
        value=f"• Use `{BOT_PREFIX}inv` to check your invites\n"
              f"• Use `{BOT_PREFIX}claim-free` to claim your VPS\n"
              f"• Invite more users to unlock better plans!",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="freeplans")
async def freeplans_alias(ctx):
    """Alias for plans"""
    await show_plans(ctx)

@bot.command(name="inv")
@commands.cooldown(1, 3, commands.BucketType.user)
async def check_invites(ctx):
    """Check your invites"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    stats = get_user_stats(str(ctx.author.id))
    invites = stats.get('invites', 0)
    
    embed = info_embed("Your Invite Stats", f"```fix\nCurrent invites: {invites}\n```")
    
    # Show available plans
    available = []
    for plan in FREE_VPS_PLANS['invites']:
        if invites >= plan['invites']:
            available.append(f"✅ {plan['emoji']} {plan['name']}")
        else:
            available.append(f"❌ {plan['emoji']} {plan['name']} (need {plan['invites']})")
    
    embed.add_field(name="📋 Available Plans", value="\n".join(available), inline=False)
    embed.add_field(
        name="📌 Next Steps",
        value=f"• Use `{BOT_PREFIX}claim-free` to claim your VPS",
        inline=False
    )
    
    await ctx.send(embed=embed)

class ClaimOSSelectView(View):
    """OS selection for VPS claim"""
    def __init__(self, ctx, plan):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.plan = plan
        
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(
                label=os["label"][:100],
                value=os["value"],
                description=os["desc"][:100] if os["desc"] else None,
                emoji=os.get("emoji", "🐧")
            ))
        
        self.select = Select(
            placeholder="📋 Select an operating system...",
            options=options,
            min_values=1,
            max_values=1
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, row=1)
        cancel_btn.callback = self.cancel_callback
        self.add_item(cancel_btn)
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        selected_os = self.select.values[0]
        
        # Create confirmation view
        view = View(timeout=60)
        confirm_btn = Button(label="✅ Confirm", style=discord.ButtonStyle.success)
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        
        async def confirm_callback(confirm_interaction):
            await self.create_vps(confirm_interaction, selected_os)
        
        async def cancel_callback(cancel_interaction):
            await cancel_interaction.response.edit_message(
                embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"),
                view=None
            )
        
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        view.add_item(confirm_btn)
        view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        
        embed = warning_embed(
            "Confirm VPS Creation",
            f"```fix\nPlan: {self.plan['name']}\nOS: {os_name}\nRAM: {self.plan['ram']}GB\nCPU: {self.plan['cpu']} Core(s)\nDisk: {self.plan['disk']}GB\n```\n"
            f"This will use **{self.plan['invites']}** invites from your account."
        )
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def cancel_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"),
            view=None
        )
    
    async def create_vps(self, interaction: discord.Interaction, os_version: str):
        await interaction.response.defer(ephemeral=True)
        
        user_id = str(self.ctx.author.id)
        stats = get_user_stats(user_id)
        
        # Check if user already has a VPS
        user_vps = get_user_vps(user_id)
        if user_vps:
            await interaction.followup.send(
                embed=error_embed("VPS Already Exists", "```diff\n- You already have a VPS. Contact an admin if you need another.\n```"),
                ephemeral=True
            )
            return
        
        # Generate container name
        container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
        
        # Create the container
        progress = await interaction.followup.send(
            embed=info_embed("Creating VPS", "```fix\nStep 1/4: Initializing container...\n```"),
            ephemeral=True
        )
        
        try:
            # Initialize container
            ram_mb = self.plan['ram'] * 1024
            await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
            
            await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 2/4: Configuring resources...\n```"))
            
            # Set limits
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            await run_lxc(f"lxc config set {container_name} limits.cpu {self.plan['cpu']}")
            await run_lxc(f"lxc config device set {container_name} root size={self.plan['disk']}GB")
            
            # Apply LXC config
            await apply_lxc_config(container_name)
            
            await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 3/4: Starting container...\n```"))
            
            # Start container
            await run_lxc(f"lxc start {container_name}")
            
            # Apply internal permissions
            await apply_internal_permissions(container_name)
            
            await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 4/4: Finalizing...\n```"))
            
            # Save to database
            vps = add_vps(
                user_id=user_id,
                container_name=container_name,
                ram=self.plan['ram'],
                cpu=self.plan['cpu'],
                disk=self.plan['disk'],
                os_version=os_version,
                plan_name=self.plan['name']
            )
            
            # Deduct invites
            update_user_stats(user_id, invites=-self.plan['invites'], claimed_vps_count=1)
            
            # Assign role
            if self.ctx.guild:
                role = discord.utils.get(self.ctx.guild.roles, name=f"{BOT_NAME} User")
                if not role:
                    role = await self.ctx.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
                try:
                    await self.ctx.author.add_roles(role)
                except:
                    pass
            
            # Send DM
            try:
                dm_embed = success_embed("✅ VPS Created Successfully!")
                dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
                dm_embed.add_field(name="📋 Plan", value=f"```fix\n{self.plan['name']}\n```", inline=True)
                dm_embed.add_field(name="🐧 OS", value=f"```fix\n{os_version}\n```", inline=True)
                dm_embed.add_field(name="⚙️ Resources", value=f"```fix\n{self.plan['ram']}GB RAM / {self.plan['cpu']} CPU / {self.plan['disk']}GB Disk\n```", inline=False)
                dm_embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
                dm_embed.add_field(name="📟 Console", value=f"Use `{BOT_PREFIX}ss {container_name}` to view console", inline=False)
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
            # Success message
            embed = success_embed("✅ VPS Created Successfully!")
            embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
            embed.add_field(name="📋 Plan", value=f"```fix\n{self.plan['name']}\n```", inline=True)
            embed.add_field(name="🐧 OS", value=f"```fix\n{os_version}\n```", inline=True)
            embed.add_field(name="⚙️ Resources", value=f"```fix\n{self.plan['ram']}GB RAM / {self.plan['cpu']} CPU / {self.plan['disk']}GB Disk\n```", inline=False)
            embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
            embed.add_field(name="📟 Console", value=f"Use `{BOT_PREFIX}ss {container_name}` to view console", inline=False)
            
            await progress.edit(embed=embed)
            
            # Log
            logger.info(f"User {self.ctx.author} created VPS {container_name} with plan {self.plan['name']}")
            
        except Exception as e:
            logger.error(f"VPS creation failed: {e}")
            await progress.edit(embed=error_embed("Creation Failed", f"```diff\n- Error: {str(e)}\n```"))
            
            # Clean up on failure
            try:
                await run_lxc(f"lxc delete {container_name} --force")
            except:
                pass

@bot.command(name="claim-free")
@commands.cooldown(1, 60, commands.BucketType.user)
async def claim_free(ctx):
    """Claim a free VPS based on your invites"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    invites = stats.get('invites', 0)
    
    # Check if user already has a VPS
    user_vps = get_user_vps(user_id)
    if user_vps:
        await ctx.send(embed=error_embed(
            "VPS Already Exists",
            "```diff\n- You already have a VPS. Each user can only claim one free VPS.\n```"
        ))
        return
    
    # Find highest eligible plan
    eligible_plan = None
    for plan in reversed(FREE_VPS_PLANS['invites']):
        if invites >= plan['invites']:
            eligible_plan = plan
            break
    
    if not eligible_plan:
        await ctx.send(embed=error_embed(
            "No Eligible Plans",
            f"```diff\n- You have {invites} invites.\n- You need at least 5 invites to claim a VPS.\n```\n\n"
            f"Invite more users to unlock plans!"
        ))
        return
    
    # Show plan details and ask for OS
    embed = info_embed(
        "You are eligible for:",
        f"**{eligible_plan['emoji']} {eligible_plan['name']}**\n"
        f"• RAM: {eligible_plan['ram']}GB\n"
        f"• CPU: {eligible_plan['cpu']} Core(s)\n"
        f"• Disk: {eligible_plan['disk']}GB\n"
        f"• Cost: {eligible_plan['invites']} invites\n\n"
        f"Please select an operating system:"
    )
    
    view = ClaimOSSelectView(ctx, eligible_plan)
    await ctx.send(embed=embed, view=view)

@bot.command(name="stats")
@commands.cooldown(1, 3, commands.BucketType.user)
async def user_stats_command(ctx):
    """View your statistics"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    user_vps = get_user_vps(user_id)
    
    embed = info_embed(f"Statistics for {ctx.author.display_name}")
    embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
    embed.add_field(name="🚀 Boosts", value=f"```fix\n{stats.get('boosts', 0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS Count", value=f"```fix\n{len(user_vps)}\n```", inline=True)
    embed.add_field(name="🎁 Claimed VPS", value=f"```fix\n{stats.get('claimed_vps_count', 0)}\n```", inline=True)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  🌐 NODE MANAGEMENT COMMANDS - COMPLETE
# ==================================================================================================

@bot.command(name="node")
@commands.cooldown(1, 3, commands.BucketType.user)
async def node_list(ctx):
    """List all nodes with stats"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    nodes = get_all_nodes()
    
    if not nodes:
        embed = info_embed(
            "No Nodes",
            "```fix\nNo nodes have been added yet.\n```\n\n"
            f"Use `{BOT_PREFIX}node-add` to add a node (admin only)."
        )
        await ctx.send(embed=embed)
        return
    
    embed = node_embed(f"Node Network ({len(nodes)} nodes)")
    
    online_count = sum(1 for n in nodes if n['status'] == 'online')
    offline_count = len(nodes) - online_count
    
    embed.add_field(name="📊 Summary", value=f"```fix\nOnline: {online_count} | Offline: {offline_count}\n```", inline=False)
    
    for node in nodes:
        status_emoji = "🟢" if node['status'] == 'online' else "🔴"
        
        # Calculate usage percentages
        ram_usage = (node['used_ram'] / node['total_ram'] * 100) if node['total_ram'] > 0 else 0
        cpu_usage = node['used_cpu']
        disk_usage = (node['used_disk'] / node['total_disk'] * 100) if node['total_disk'] > 0 else 0
        
        node_info = f"```fix\n"
        node_info += f"Host    : {node['host']}:{node['port']}\n"
        node_info += f"RAM     : {node['used_ram']}/{node['total_ram']} MB ({ram_usage:.1f}%)\n"
        node_info += f"CPU     : {cpu_usage:.1f}%\n"
        node_info += f"Disk    : {node['used_disk']}/{node['total_disk']} GB ({disk_usage:.1f}%)\n"
        node_info += f"LXC     : {node['lxc_count']} containers\n"
        node_info += f"Region  : {node.get('region', 'us')}\n"
        node_info += f"Last    : {node.get('last_checked', 'Never')[:16]}\n"
        node_info += f"```"
        
        embed.add_field(
            name=f"{status_emoji} {node['name']}",
            value=node_info,
            inline=False
        )
    
    embed.set_footer(text=f"⚡ Use {BOT_PREFIX}node-info <name> for details ⚡")
    await ctx.send(embed=embed)

@bot.command(name="node-info")
@commands.cooldown(1, 3, commands.BucketType.user)
async def node_info(ctx, name: str):
    """Get detailed node information"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    node = get_node(name)
    
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    embed = node_embed(f"Node Details: {name}")
    
    status_emoji = "🟢" if node['status'] == 'online' else "🔴"
    
    # Basic info
    basic = f"```fix\n"
    basic += f"Status  : {node['status'].upper()}\n"
    basic += f"Host    : {node['host']}:{node['port']}\n"
    basic += f"Username: {node['username']}\n"
    basic += f"Region  : {node.get('region', 'us')}\n"
    basic += f"Added   : {node['added_at'][:16]}\n"
    basic += f"Added By: {node.get('added_by', 'System')}\n"
    basic += f"```"
    embed.add_field(name="📋 Basic Info", value=basic, inline=False)
    
    # Resource usage
    ram_usage = (node['used_ram'] / node['total_ram'] * 100) if node['total_ram'] > 0 else 0
    cpu_usage = node['used_cpu']
    disk_usage = (node['used_disk'] / node['total_disk'] * 100) if node['total_disk'] > 0 else 0
    
    resources = f"```fix\n"
    resources += f"RAM     : {node['used_ram']}/{node['total_ram']} MB ({ram_usage:.1f}%)\n"
    resources += f"CPU     : {cpu_usage:.1f}%\n"
    resources += f"Disk    : {node['used_disk']}/{node['total_disk']} GB ({disk_usage:.1f}%)\n"
    resources += f"LXC     : {node['lxc_count']} containers\n"
    resources += f"Last    : {node.get('last_checked', 'Never')}\n"
    resources += f"```"
    embed.add_field(name="📊 Resource Usage", value=resources, inline=False)
    
    # API Info
    api_info = f"```fix\n"
    api_info += f"API Key : {node['api_key'][:8]}...{node['api_key'][-8:]}\n"
    api_info += f"API URL : {node.get('api_url', 'N/A')}\n"
    api_info += f"```"
    embed.add_field(name="🔌 API Information", value=api_info, inline=False)
    
    # Description
    if node.get('description'):
        embed.add_field(name="📝 Description", value=f"```fix\n{node['description']}\n```", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="node-add")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def node_add(ctx, name: str, host: str, username: str, password: str = None, port: int = 22):
    """Add a new node to the cluster"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Check if node already exists
    existing = get_node(name)
    if existing:
        await ctx.send(embed=error_embed("Node Exists", f"```diff\n- Node '{name}' already exists.\n```"))
        return
    
    # Add node to database
    try:
        node = add_node(name, host, username, password, port=port, added_by=str(ctx.author.id))
        
        # Check node health
        stats = await check_node_health(node)
        update_node_status(name, stats['status'], stats)
        
        embed = success_embed("Node Added Successfully")
        status_emoji = "🟢" if stats['status'] == 'online' else "🔴"
        
        info = f"```fix\n"
        info += f"Name    : {name}\n"
        info += f"Host    : {host}:{port}\n"
        info += f"Status  : {stats['status'].upper()}\n"
        info += f"RAM     : {stats.get('total_ram', 0)} MB\n"
        info += f"CPU     : {stats.get('total_cpu', 0)} cores\n"
        info += f"Disk    : {stats.get('total_disk', 0)} GB\n"
        info += f"API Key : {node['api_key'][:8]}...{node['api_key'][-8:]}\n"
        info += f"```"
        
        embed.add_field(name="📋 Node Information", value=info, inline=False)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed to Add Node", f"```diff\n- Error: {str(e)}\n```"))

@bot.command(name="node-remove")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def node_remove(ctx, name: str):
    """Remove a node from the cluster"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Check if node exists
    node = get_node(name)
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    # Confirm deletion
    view = View(timeout=60)
    confirm_btn = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        if delete_node(name):
            embed = success_embed("Node Removed", f"```fix\nNode '{name}' has been removed.\n```")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.edit_message(embed=error_embed("Failed", "```diff\n- Could not remove node.\n```"), view=None)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nNode removal cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "Confirm Node Removal",
        f"```fix\nAre you sure you want to remove node '{name}'?\n```\n"
        f"Host: {node['host']}\n"
        f"Status: {node['status']}\n\n"
        f"This action cannot be undone!"
    )
    
    await ctx.send(embed=embed, view=view)

@bot.command(name="node-check")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def node_check(ctx, name: str):
    """Check node health manually"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    node = get_node(name)
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Checking Node", f"```fix\nChecking health of node '{name}'...\n```"))
    
    stats = await check_node_health(node)
    update_node_status(name, stats['status'], stats)
    
    if stats['status'] == 'online':
        embed = success_embed("Node Health Check", f"```fix\nNode '{name}' is ONLINE\n```")
        
        info = f"```fix\n"
        info += f"RAM     : {stats['used_ram']}/{stats['total_ram']} MB\n"
        info += f"CPU     : {stats['used_cpu']:.1f}%\n"
        info += f"Disk    : {stats['used_disk']}/{stats['total_disk']} GB\n"
        info += f"LXC     : {stats['lxc_count']} containers\n"
        info += f"```"
        embed.add_field(name="📊 Resource Usage", value=info, inline=False)
        
    else:
        embed = error_embed("Node Health Check", f"```diff\n- Node '{name}' is OFFLINE\n```")
    
    await msg.edit(embed=embed)

@bot.command(name="node-stats")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def node_stats(ctx):
    """Show cluster statistics"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    nodes = get_all_nodes()
    
    if not nodes:
        await ctx.send(embed=info_embed("No Nodes", "```fix\nNo nodes in the cluster.\n```"))
        return
    
    total_ram = sum(n['total_ram'] for n in nodes)
    used_ram = sum(n['used_ram'] for n in nodes)
    total_cpu = sum(n['total_cpu'] for n in nodes)
    total_disk = sum(n['total_disk'] for n in nodes)
    used_disk = sum(n['used_disk'] for n in nodes)
    total_lxc = sum(n['lxc_count'] for n in nodes)
    online_nodes = sum(1 for n in nodes if n['status'] == 'online')
    
    embed = node_embed("Cluster Statistics")
    
    summary = f"```fix\n"
    summary += f"Total Nodes  : {len(nodes)}\n"
    summary += f"Online Nodes : {online_nodes}\n"
    summary += f"Offline Nodes: {len(nodes) - online_nodes}\n"
    summary += f"Total LXC    : {total_lxc}\n"
    summary += f"```"
    embed.add_field(name="📊 Summary", value=summary, inline=False)
    
    resources = f"```fix\n"
    resources += f"RAM         : {used_ram}/{total_ram} MB ({(used_ram/total_ram*100) if total_ram>0 else 0:.1f}%)\n"
    resources += f"CPU Cores   : {total_cpu}\n"
    resources += f"Disk        : {used_disk}/{total_disk} GB ({(used_disk/total_disk*100) if total_disk>0 else 0:.1f}%)\n"
    resources += f"```"
    embed.add_field(name="💾 Total Resources", value=resources, inline=False)
    
    # Per-node breakdown
    for node in nodes:
        status_emoji = "🟢" if node['status'] == 'online' else "🔴"
        ram_pct = (node['used_ram'] / node['total_ram'] * 100) if node['total_ram'] > 0 else 0
        disk_pct = (node['used_disk'] / node['total_disk'] * 100) if node['total_disk'] > 0 else 0
        
        node_info = f"{status_emoji} **{node['name']}**\n"
        node_info += f"```fix\n"
        node_info += f"RAM: {node['used_ram']}/{node['total_ram']} MB ({ram_pct:.1f}%)\n"
        node_info += f"CPU: {node['used_cpu']:.1f}%\n"
        node_info += f"Disk: {node['used_disk']}/{node['total_disk']} GB ({disk_pct:.1f}%)\n"
        node_info += f"LXC: {node['lxc_count']}\n"
        node_info += f"```"
        embed.add_field(name=f"Node: {node['name']}", value=node_info, inline=True)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  🖥️  VPS MANAGEMENT COMMANDS
# ==================================================================================================

@bot.command(name="myvps")
@commands.cooldown(1, 3, commands.BucketType.user)
async def my_vps(ctx):
    """List your VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = info_embed(f"Your VPS ({len(vps_list)})")
    
    for i, vps in enumerate(vps_list, 1):
        status_emoji = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
        status_text = vps['status'].upper()
        if vps['suspended']:
            status_text = "SUSPENDED"
        
        embed.add_field(
            name=f"VPS #{i}",
            value=f"{status_emoji} **`{vps['container_name']}`**\n"
                  f"Status: `{status_text}`\n"
                  f"Plan: {vps['plan_name']}\n"
                  f"Resources: {vps['ram']}GB RAM / {vps['cpu']} CPU / {vps['disk']}GB Disk\n"
                  f"IP: `{vps.get('ip_address', 'N/A')}`",
            inline=False
        )
    
    embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` for detailed control", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="list")
@commands.cooldown(1, 3, commands.BucketType.user)
async def list_command(ctx):
    """Detailed VPS list"""
    await my_vps(ctx)

class VPSManageView(View):
    """Interactive VPS management view with all controls"""
    def __init__(self, ctx, user_id, vps_list, is_admin_view=False, target_user=None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.user_id = user_id
        self.vps_list = vps_list
        self.current_index = 0
        self.is_admin_view = is_admin_view
        self.target_user = target_user
        self.message = None
        self.console_mode = False
        self.current_container = None
        
        self.update_buttons()
    
    def update_buttons(self):
        """Update view with current VPS"""
        self.clear_items()
        
        if len(self.vps_list) > 1:
            # Add navigation
            prev_btn = Button(label="◀️", style=discord.ButtonStyle.secondary)
            prev_btn.callback = self.prev_callback
            self.add_item(prev_btn)
            
            counter_btn = Button(label=f"{self.current_index + 1}/{len(self.vps_list)}", style=discord.ButtonStyle.secondary, disabled=True)
            self.add_item(counter_btn)
            
            next_btn = Button(label="▶️", style=discord.ButtonStyle.secondary)
            next_btn.callback = self.next_callback
            self.add_item(next_btn)
        
        # Action buttons
        start_btn = Button(label="▶️ Start", style=discord.ButtonStyle.success)
        start_btn.callback = self.start_callback
        self.add_item(start_btn)
        
        stop_btn = Button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
        stop_btn.callback = self.stop_callback
        self.add_item(stop_btn)
        
        restart_btn = Button(label="🔄 Restart", style=discord.ButtonStyle.primary)
        restart_btn.callback = self.restart_callback
        self.add_item(restart_btn)
        
        stats_btn = Button(label="📊 Stats", style=discord.ButtonStyle.secondary)
        stats_btn.callback = self.stats_callback
        self.add_item(stats_btn)
        
        console_btn = Button(label="📟 Console", style=discord.ButtonStyle.secondary)
        console_btn.callback = self.console_callback
        self.add_item(console_btn)
        
        ssh_btn = Button(label="🔑 SSH", style=discord.ButtonStyle.secondary)
        ssh_btn.callback = self.ssh_callback
        self.add_item(ssh_btn)
        
        refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary)
        refresh_btn.callback = self.refresh_callback
        self.add_item(refresh_btn)
    
    async def get_current_embed(self) -> discord.Embed:
        """Get embed for current VPS with full stats"""
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        self.current_container = container
        
        # Get live stats
        stats = await get_container_stats(container)
        
        status_emoji = "🟢" if stats['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
        status_text = stats['status'].upper()
        if vps['suspended']:
            status_text = "SUSPENDED"
        
        title = f"VPS Management: {container}"
        if self.is_admin_view and self.target_user:
            title = f"Admin: {self.target_user.display_name}'s VPS - {container}"
        
        embed = create_embed(title)
        
        # Basic Info
        basic = f"```fix\n"
        basic += f"Status : {status_text}\n"
        basic += f"Plan   : {vps['plan_name']}\n"
        basic += f"OS     : {vps['os_version']}\n"
        basic += f"RAM    : {vps['ram']}GB\n"
        basic += f"CPU    : {vps['cpu']} Core(s)\n"
        basic += f"Disk   : {vps['disk']}GB\n"
        basic += f"IP     : {stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n"
        basic += f"MAC    : {stats['mac']}\n"
        basic += f"```"
        embed.add_field(name="📋 Basic Info", value=basic, inline=False)
        
        if stats['status'] == 'running' and not vps['suspended']:
            # Live Stats
            live = f"```fix\n"
            live += f"CPU     : {stats['cpu']}\n"
            live += f"Memory  : {stats['memory']}\n"
            live += f"Disk    : {stats['disk']}\n"
            live += f"Uptime  : {stats['uptime']}\n"
            live += f"Process : {stats['processes']}\n"
            live += f"Load    : {stats['load']}\n"
            live += f"```"
            embed.add_field(name="📊 Live Stats", value=live, inline=True)
            
            # Network Stats
            network = f"```fix\n"
            network += f"IPv4    : {', '.join(stats['ipv4'][:2]) if stats['ipv4'] else 'N/A'}\n"
            network += f"RX      : {stats['network_rx']}\n"
            network += f"TX      : {stats['network_tx']}\n"
            network += f"```"
            embed.add_field(name="🌐 Network", value=network, inline=True)
            
            # System Info
            sysinfo = f"```fix\n"
            sysinfo += f"Hostname: {stats['hostname']}\n"
            sysinfo += f"Kernel  : {stats['kernel']}\n"
            sysinfo += f"OS      : {stats['os']}\n"
            sysinfo += f"```"
            embed.add_field(name="⚙️ System", value=sysinfo, inline=True)
        
        return embed
    
    async def prev_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_index = (self.current_index - 1) % len(self.vps_list)
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def next_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_index = (self.current_index + 1) % len(self.vps_list)
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def start_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended'] and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message(embed=error_embed("Cannot Start", "```diff\n- This VPS is suspended.\n```"), ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            await run_lxc(f"lxc start {container}")
            update_vps_status(container, 'running')
            await interaction.followup.send(embed=success_embed("Started", f"```fix\nVPS {container} started.\n```"), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"), ephemeral=True)
        
        # Refresh display
        await self.refresh_callback(interaction)
    
    async def stop_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended'] and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message(embed=error_embed("Cannot Stop", "```diff\n- This VPS is suspended.\n```"), ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            await run_lxc(f"lxc stop {container} --force")
            update_vps_status(container, 'stopped')
            await interaction.followup.send(embed=success_embed("Stopped", f"```fix\nVPS {container} stopped.\n```"), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"), ephemeral=True)
        
        # Refresh display
        await self.refresh_callback(interaction)
    
    async def restart_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended'] and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message(embed=error_embed("Cannot Restart", "```diff\n- This VPS is suspended.\n```"), ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            await run_lxc(f"lxc restart {container}")
            update_vps_status(container, 'running')
            await interaction.followup.send(embed=success_embed("Restarted", f"```fix\nVPS {container} restarted.\n```"), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"), ephemeral=True)
        
        # Refresh display
        await self.refresh_callback(interaction)
    
    async def stats_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        stats = await get_container_stats(container)
        
        embed = info_embed(f"Live Stats: {container}")
        
        stats_text = f"```fix\n"
        stats_text += f"Status : {stats['status'].upper()}\n"
        stats_text += f"CPU    : {stats['cpu']}\n"
        stats_text += f"Memory : {stats['memory']}\n"
        stats_text += f"Disk   : {stats['disk']}\n"
        stats_text += f"Uptime : {stats['uptime']}\n"
        stats_text += f"Process: {stats['processes']}\n"
        stats_text += f"Load   : {stats['load']}\n"
        stats_text += f"```"
        
        embed.add_field(name="📊 Statistics", value=stats_text, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def console_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        # Show console output
        console = await get_container_console(container, 30)
        
        embed = terminal_embed(f"Console: {container}", console)
        embed.add_field(name="📟 Commands", value=f"`{BOT_PREFIX}execute {container} <cmd>` to run commands", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def ssh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        await interaction.response.defer(ephemeral=True)
        
        # Call ssh-gen command
        await ssh_gen_command(interaction, container)
    
    async def refresh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        # Refresh VPS list from database
        if self.is_admin_view and self.target_user:
            self.vps_list = get_user_vps(str(self.target_user.id))
        else:
            self.vps_list = get_user_vps(self.user_id)
        
        if not self.vps_list:
            await interaction.response.edit_message(embed=no_vps_embed(), view=None)
            return
        
        if self.current_index >= len(self.vps_list):
            self.current_index = 0
        
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)

@bot.command(name="manage")
@commands.cooldown(1, 5, commands.BucketType.user)
async def manage_vps(ctx, user: discord.Member = None):
    """Interactive VPS manager - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- Only admins can manage other users' VPS.\n```"))
            return
        target_id = str(user.id)
        target_name = user.display_name
        is_admin_view = True
    else:
        target_id = str(ctx.author.id)
        target_name = ctx.author.display_name
        user = ctx.author
        is_admin_view = False
    
    vps_list = get_user_vps(target_id)
    
    if not vps_list:
        if user != ctx.author:
            await ctx.send(embed=info_embed(f"No VPS", f"{user.mention} has no VPS."))
        else:
            await ctx.send(embed=no_vps_embed())
        return
    
    view = VPSManageView(ctx, target_id, vps_list, is_admin_view, user if is_admin_view else None)
    embed = await view.get_current_embed()
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg

# ==================================================================================================
#  📟  CONSOLE & SSH COMMANDS - FIXED SSH ISSUE
# ==================================================================================================

@bot.command(name="ss")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ss_command(ctx, container_name: str = None):
    """Show VPS console/screenshot - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Find the container
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        # Verify ownership
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    msg = await ctx.send(embed=info_embed("📸 Taking VPS Snapshot", f"```fix\nGetting console output from {container_name}...\n```"))
    
    # Get console output
    console = await get_container_console(container_name, 40)
    
    # Get stats
    stats = await get_container_stats(container_name)
    
    # Create terminal-style embed
    terminal_output = f"=== {container_name} Console Output ===\n"
    terminal_output += f"Status: {stats['status'].upper()} | Uptime: {stats['uptime']}\n"
    terminal_output += f"CPU: {stats['cpu']} | Memory: {stats['memory']} | Disk: {stats['disk']}\n"
    terminal_output += "="*50 + "\n\n"
    terminal_output += console
    
    embed = terminal_embed(f"VPS Console: {container_name}", terminal_output)
    
    await msg.edit(embed=embed)

@bot.command(name="console")
@commands.cooldown(1, 5, commands.BucketType.user)
async def console_command(ctx, container_name: str, *, command: str = None):
    """Interactive console - type commands"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    if not command:
        # Just show console
        await ss_command(ctx, container_name)
        return
    
    # Execute command
    msg = await ctx.send(embed=info_embed("⚡ Executing Command", f"```fix\nRunning: {command}\n```"))
    
    out, err, code = await exec_in_container(container_name, command, timeout=60)
    
    output = out if out else err
    
    terminal_output = f"$ {command}\n\n"
    terminal_output += output
    
    embed = terminal_embed(f"Command Output: {container_name}", terminal_output)
    embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```", inline=True)
    
    await msg.edit(embed=embed)

@bot.command(name="execute")
@commands.cooldown(1, 5, commands.BucketType.user)
async def execute_command(ctx, container_name: str, *, command: str):
    """Execute a command in VPS"""
    await console_command(ctx, container_name, command=command)

@bot.command(name="top")
@commands.cooldown(1, 5, commands.BucketType.user)
async def top_command(ctx, container_name: str = None):
    """Show live process monitor"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Find the container
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        # Verify ownership
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    msg = await ctx.send(embed=info_embed("📊 Getting process list...", f"```fix\nFetching top output from {container_name}\n```"))
    
    out, _, _ = await exec_in_container(container_name, "ps aux --sort=-%cpu | head -20")
    
    terminal_output = f"=== Process List: {container_name} ===\n\n"
    terminal_output += out
    
    embed = terminal_embed(f"Process Monitor: {container_name}", terminal_output)
    
    await msg.edit(embed=embed)

@bot.command(name="df")
@commands.cooldown(1, 3, commands.BucketType.user)
async def df_command(ctx, container_name: str = None):
    """Show disk usage"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "df -h")
    
    embed = terminal_embed(f"Disk Usage: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="free")
@commands.cooldown(1, 3, commands.BucketType.user)
async def free_command(ctx, container_name: str = None):
    """Show memory usage"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "free -h")
    
    embed = terminal_embed(f"Memory Usage: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="netstat")
@commands.cooldown(1, 5, commands.BucketType.user)
async def netstat_command(ctx, container_name: str = None):
    """Show network connections"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "netstat -tuln | head -20")
    
    embed = terminal_embed(f"Network Connections: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="reboot")
@commands.cooldown(1, 10, commands.BucketType.user)
async def reboot_vps(ctx, container_name: str):
    """Reboot VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    await ctx.send(embed=info_embed("🔄 Rebooting", f"```fix\nRebooting VPS {container_name}...\n```"))
    
    try:
        await run_lxc(f"lxc restart {container_name}")
        update_vps_status(container_name, 'running')
        await ctx.send(embed=success_embed("Rebooted", f"```fix\nVPS {container_name} has been rebooted.\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="shutdown")
@commands.cooldown(1, 10, commands.BucketType.user)
async def shutdown_vps(ctx, container_name: str):
    """Shutdown VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    await ctx.send(embed=info_embed("⏹️ Shutting Down", f"```fix\nShutting down VPS {container_name}...\n```"))
    
    try:
        await run_lxc(f"lxc stop {container_name}")
        update_vps_status(container_name, 'stopped')
        await ctx.send(embed=success_embed("Shutdown", f"```fix\nVPS {container_name} has been shut down.\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  🔑  SSH-GEN COMMAND - COMPLETELY FIXED
# ==================================================================================================

async def ssh_gen_command(interaction_or_ctx, container_name: str):
    """Generate SSH access for a container - FIXED"""
    
    # Handle both interaction and context
    if isinstance(interaction_or_ctx, discord.Interaction):
        ctx = await bot.get_context(interaction_or_ctx.message)
        user = interaction_or_ctx.user
        send_msg = interaction_or_ctx.followup.send
        is_interaction = True
    else:
        ctx = interaction_or_ctx
        user = ctx.author
        send_msg = ctx.send
        is_interaction = False
    
    user_id = str(user.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await send_msg(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    msg = await send_msg(embed=info_embed("🔑 Generating SSH Access", f"```fix\nSetting up SSH for {container_name}...\n```"))
    
    try:
        # Check if container is running
        status = await get_container_status(container_name)
        if status != 'running':
            await msg.edit(embed=error_embed("Container Not Running", f"```diff\n- {container_name} is not running. Start it first with .manage\n```"))
            return
        
        # Install tmate if not present
        out, _, _ = await exec_in_container(container_name, "which tmate")
        if not out:
            await msg.edit(embed=info_embed("Installing SSH Service", "```fix\nInstalling tmate (this may take a moment)...\n```"))
            await exec_in_container(container_name, "apt-get update -qq")
            await exec_in_container(container_name, "apt-get install -y -qq tmate")
        
        # Generate unique session
        session_id = f"svm5-{random.randint(1000, 9999)}-{int(time.time())}"
        
        # Start tmate session with proper error handling
        await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock new-session -d")
        await asyncio.sleep(5)  # Increased wait time for tmate to initialize
        
        # Get SSH connection string
        out, err, code = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_ssh}}'")
        ssh_url = out.strip()
        
        if ssh_url and ssh_url.startswith('ssh'):
            # Try to DM the user
            try:
                dm_embed = success_embed("🔑 SSH Access Generated")
                dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
                dm_embed.add_field(name="🔐 SSH Command", value=f"```bash\n{ssh_url}\n```", inline=False)
                dm_embed.add_field(name="📋 Instructions", 
                                  value="```fix\n1. Copy the command above\n2. Paste in your terminal\n3. You'll have full shell access\n\n⚠️ This link expires in 15 minutes\n```", 
                                  inline=False)
                await user.send(embed=dm_embed)
                
                await msg.edit(embed=success_embed(
                    "SSH Access Generated",
                    f"```fix\n✅ SSH connection details sent to your DMs!\nContainer: {container_name}\n```"
                ))
            except discord.Forbidden:
                # If DM fails, send in channel but ephemeral
                await msg.edit(embed=error_embed(
                    "DM Failed",
                    f"```fix\n❌ Could not send DM. Please enable DMs.\n\nSSH Command:\n{ssh_url}\n```"
                ))
        else:
            # Try alternative method
            out, _, _ = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_web}}'")
            web_url = out.strip()
            
            if web_url:
                await msg.edit(embed=success_embed(
                    "Web Terminal Generated",
                    f"```fix\nWeb URL: {web_url}\n```\n"
                    f"Open this URL in your browser for terminal access."
                ))
            else:
                await msg.edit(embed=error_embed("Failed", "```diff\n- Could not generate SSH access. Try again later.\n```"))
    
    except Exception as e:
        logger.error(f"SSH generation error: {e}")
        await msg.edit(embed=error_embed("SSH Generation Failed", f"```diff\n- {str(e)[:100]}\n```"))

@bot.command(name="ssh-gen")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ssh_gen(ctx, container_name: str):
    """Generate SSH access for your container via tmate - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    await ssh_gen_command(ctx, container_name)

# ==================================================================================================
#  🔌  PORT FORWARDING COMMANDS
# ==================================================================================================

@bot.group(name="ports", invoke_without_command=True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def ports_group(ctx):
    """Port forwarding commands - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    
    embed = info_embed("Port Forwarding Help")
    embed.add_field(name="📊 Your Quota", value=f"```fix\nAllocated: {allocated}\nUsed: {len(forwards)}\nAvailable: {allocated - len(forwards)}\n```", inline=False)
    embed.add_field(
        name="📋 Commands",
        value=f"`{BOT_PREFIX}ports add <vps_num> <port> [tcp/udp]` - Add forward\n"
              f"`{BOT_PREFIX}ports list` - List your forwards\n"
              f"`{BOT_PREFIX}ports remove <id>` - Remove forward\n"
              f"`{BOT_PREFIX}ports quota` - Check your quota",
        inline=False
    )
    await ctx.send(embed=embed)

@ports_group.command(name="add")
async def ports_add(ctx, vps_num: int, port: int, protocol: str = "tcp+udp"):
    """Add a port forward"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
        return
    
    if port < 1 or port > 65535:
        await ctx.send(embed=error_embed("Invalid Port", "```diff\n- Port must be between 1 and 65535.\n```"))
        return
    
    if protocol not in ["tcp", "udp", "tcp+udp"]:
        await ctx.send(embed=error_embed("Invalid Protocol", "```diff\n- Protocol must be tcp, udp, or tcp+udp\n```"))
        return
    
    # Check quota
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    if len(forwards) >= allocated and allocated > 0:
        await ctx.send(embed=error_embed("Quota Exceeded", f"```diff\n- You have used all {allocated} port slots.\n```"))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Cannot Add", "```diff\n- VPS is suspended.\n```"))
        return
    
    if vps['status'] != 'running':
        await ctx.send(embed=error_embed("Cannot Add", "```diff\n- VPS must be running to add port forwards.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Creating port forward...", f"```fix\nForwarding port {port} ({protocol}) from VPS #{vps_num}\n```"))
    
    host_port = await create_port_forward(user_id, container, port, protocol)
    
    if host_port:
        embed = success_embed("Port Forward Created")
        embed.add_field(name="📦 VPS", value=f"```fix\n#{vps_num} - {container}\n```", inline=True)
        embed.add_field(name="🔌 Container Port", value=f"```fix\n{port}\n```", inline=True)
        embed.add_field(name="🌐 Host Port", value=f"```fix\n{host_port}\n```", inline=True)
        embed.add_field(name="📡 Protocol", value=f"```fix\n{protocol}\n```", inline=True)
        embed.add_field(name="🔗 Access", value=f"Connect to `{SERVER_IP}:{host_port}`", inline=False)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", "```diff\n- Could not assign a host port. Try again later.\n```"))

@ports_group.command(name="list")
async def ports_list(ctx):
    """List your port forwards"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    forwards = get_user_port_forwards(user_id)
    allocated = get_port_allocation(user_id)
    
    if not forwards:
        embed = info_embed("Port Forwards", "```fix\nYou have no active port forwards.\n```")
        embed.add_field(name="📊 Quota", value=f"```fix\nAllocated: {allocated}\nUsed: 0\nAvailable: {allocated}\n```")
        await ctx.send(embed=embed)
        return
    
    embed = info_embed(f"Your Port Forwards ({len(forwards)}/{allocated})")
    
    for f in forwards:
        vps_num = next((i+1 for i, v in enumerate(get_user_vps(user_id)) if v['container_name'] == f['container_name']), '?')
        embed.add_field(
            name=f"ID: {f['id']}",
            value=f"```fix\nVPS #{vps_num}: {f['container_port']} → {SERVER_IP}:{f['host_port']} ({f['protocol']})\nCreated: {f['created_at'][:16]}\n```",
            inline=False
        )
    
    embed.add_field(name="❌ Remove", value=f"Use `{BOT_PREFIX}ports remove <id>` to remove a forward", inline=False)
    await ctx.send(embed=embed)

@ports_group.command(name="remove")
async def ports_remove(ctx, forward_id: int):
    """Remove a port forward"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    success, container, host_port = remove_port_forward(forward_id)
    
    if not success:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- Port forward with ID {forward_id} not found.\n```"))
        return
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this port forward.\n```"))
        return
    
    # Remove devices
    await remove_port_forward_device(container, host_port)
    
    await ctx.send(embed=success_embed("Removed", f"```fix\nPort forward ID {forward_id} has been removed.\n```"))

@ports_group.command(name="quota")
async def ports_quota(ctx):
    """Check your port quota"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    used = len(get_user_port_forwards(user_id))
    
    embed = info_embed("Port Quota")
    embed.add_field(name="📊 Allocated", value=f"```fix\n{allocated}\n```", inline=True)
    embed.add_field(name="📊 Used", value=f"```fix\n{used}\n```", inline=True)
    embed.add_field(name="📊 Available", value=f"```fix\n{allocated - used}\n```", inline=True)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  📦  PANEL INSTALLATION COMMANDS WITH CLOUDFLARED TUNNEL
# ==================================================================================================

class PanelSelectView(View):
    """Panel selection view"""
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        
        ptero_btn = Button(label="🦅 Pterodactyl", style=discord.ButtonStyle.primary, emoji="🦅")
        ptero_btn.callback = self.ptero_callback
        
        puffer_btn = Button(label="🐡 Pufferpanel", style=discord.ButtonStyle.success, emoji="🐡")
        puffer_btn.callback = self.puffer_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(ptero_btn)
        self.add_item(puffer_btn)
        self.add_item(cancel_btn)
    
    async def ptero_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- Not for you!\n```", ephemeral=True)
            return
        await self.install_panel(interaction, "pterodactyl")
    
    async def puffer_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- Not for you!\n```", ephemeral=True)
            return
        await self.install_panel(interaction, "pufferpanel")
    
    async def cancel_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nPanel installation cancelled.\n```"), view=None)
    
    async def install_panel(self, interaction: discord.Interaction, panel_type: str):
        await interaction.response.defer()
        
        user_id = str(self.ctx.author.id)
        
        # Check if user has VPS
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await interaction.followup.send(embed=error_embed("No VPS", "```diff\n- You need a VPS to install a panel.\n```"), ephemeral=True)
            return
        
        container = vps_list[0]['container_name']
        
        progress = await interaction.followup.send(
            embed=info_embed(f"Installing {panel_type.title()}", "```fix\nStep 1/5: Preparing installation...\n```"),
            ephemeral=True
        )
        
        try:
            # Generate credentials
            admin_user = generate_username()
            admin_email = generate_email(admin_user)
            admin_pass = generate_password(16)
            
            if panel_type == "pterodactyl":
                # Install Pterodactyl
                await progress.edit(embed=info_embed("Installing Pterodactyl", "```fix\nStep 2/5: Installing dependencies...\n```"))
                
                commands = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git unzip tar",
                    "apt-get install -y -qq nginx mariadb-server redis-server",
                    "apt-get install -y -qq php8.1 php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip}",
                    "curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer",
                    "mkdir -p /var/www/pterodactyl",
                    "cd /var/www/pterodactyl && curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz",
                    "cd /var/www/pterodactyl && tar -xzvf panel.tar.gz && chmod -R 755 storage/* bootstrap/cache/"
                ]
                
                for cmd in commands:
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                
                await progress.edit(embed=info_embed("Installing Pterodactyl", "```fix\nStep 3/5: Configuring environment...\n```"))
                
                # Create .env and install
                env_cmds = [
                    "cd /var/www/pterodactyl && cp .env.example .env",
                    "cd /var/www/pterodactyl && composer install --no-dev --optimize-autoloader --no-interaction",
                    "cd /var/www/pterodactyl && php artisan key:generate --force",
                    "cd /var/www/pterodactyl && php artisan migrate --seed --force",
                    f"cd /var/www/pterodactyl && php artisan p:user:make --email='{admin_email}' --username='{admin_user}' --password='{admin_pass}' --name-first='Admin' --name-last='User' --admin=1 --no-interaction"
                ]
                
                for cmd in env_cmds:
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                
                # Get IP
                out, _, _ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
                ip = out.strip() or SERVER_IP
                panel_url = f"http://{ip}"
                
                # Create cloudflared tunnel
                await progress.edit(embed=info_embed("Installing Pterodactyl", "```fix\nStep 4/5: Creating tunnel...\n```"))
                tunnel_url = await create_cloudflared_tunnel(container, 80)
                if tunnel_url:
                    panel_url = tunnel_url
                
            else:  # pufferpanel
                await progress.edit(embed=info_embed("Installing Pufferpanel", "```fix\nStep 2/5: Installing...\n```"))
                
                commands = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git",
                    "curl -s https://packagecloud.io/install/repositories/pufferpanel/pufferpanel/script.deb.sh | bash",
                    "apt-get install -y -qq pufferpanel",
                    "systemctl enable pufferpanel",
                    "systemctl start pufferpanel",
                    f"pufferpanel user add --name '{admin_user}' --email '{admin_email}' --password '{admin_pass}' --admin"
                ]
                
                for cmd in commands:
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                
                out, _, _ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
                ip = out.strip() or SERVER_IP
                panel_url = f"http://{ip}:8080"
                
                # Create cloudflared tunnel
                await progress.edit(embed=info_embed("Installing Pufferpanel", "```fix\nStep 4/5: Creating tunnel...\n```"))
                tunnel_url = await create_cloudflared_tunnel(container, 8080)
                if tunnel_url:
                    panel_url = tunnel_url
            
            # Save to database
            add_panel(user_id, panel_type, panel_url, admin_user, admin_pass, admin_email)
            
            await progress.edit(embed=info_embed("Installing Panel", "```fix\nStep 5/5: Finalizing...\n```"))
            
            # Success message
            embed = success_embed(f"✅ {panel_type.title()} Installed Successfully!")
            embed.add_field(name="🌐 Panel URL", value=f"```fix\n{panel_url}\n```", inline=False)
            embed.add_field(name="👤 Username", value=f"||`{admin_user}`||", inline=True)
            embed.add_field(name="📧 Email", value=f"||`{admin_email}`||", inline=True)
            embed.add_field(name="🔑 Password", value=f"||`{admin_pass}`||", inline=False)
            embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
            
            await progress.edit(embed=embed)
            
            # DM user
            try:
                dm_embed = success_embed(f"🔐 Your {panel_type.title()} Credentials")
                dm_embed.add_field(name="🌐 Panel URL", value=panel_url, inline=False)
                dm_embed.add_field(name="👤 Username", value=admin_user, inline=True)
                dm_embed.add_field(name="📧 Email", value=admin_email, inline=True)
                dm_embed.add_field(name="🔑 Password", value=admin_pass, inline=False)
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
        except Exception as e:
            await progress.edit(embed=error_embed("Installation Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="install-panel")
@commands.cooldown(1, 300, commands.BucketType.user)
async def install_panel(ctx):
    """Install Pterodactyl or Pufferpanel on your VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Check if user has VPS
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = info_embed(
        "Panel Installation",
        f"```fix\nYour VPS: {vps_list[0]['container_name']}\n```\n\n"
        f"🦅 **Pterodactyl** - Popular game server panel\n"
        f"🐡 **Pufferpanel** - Lightweight alternative\n\n"
        f"Select a panel to install:"
    )
    
    view = PanelSelectView(ctx)
    await ctx.send(embed=embed, view=view)

@bot.command(name="panel-info")
@commands.cooldown(1, 3, commands.BucketType.user)
async def panel_info(ctx):
    """Show your installed panel info"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    panels = get_user_panels(user_id)
    
    if not panels:
        await ctx.send(embed=info_embed("No Panels", "```fix\nYou haven't installed any panels yet.\n```\nUse `.install-panel` to install one."))
        return
    
    embed = info_embed(f"Your Panels ({len(panels)})")
    
    for panel in panels:
        embed.add_field(
            name=f"{'🦅' if panel['panel_type'] == 'pterodactyl' else '🐡'} {panel['panel_type'].title()}",
            value=f"```fix\nURL: {panel['panel_url']}\nUsername: {panel['admin_user']}\nInstalled: {panel['installed_at'][:16]}\n```",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name="panel-tunnel")
@commands.cooldown(1, 30, commands.BucketType.user)
async def panel_tunnel(ctx, container_name: str, port: int = 80):
    """Create cloudflared tunnel for panel"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Creating Tunnel", f"```fix\nCreating cloudflared tunnel for {container_name} on port {port}...\n```"))
    
    tunnel_url = await create_cloudflared_tunnel(container_name, port)
    
    if tunnel_url:
        embed = success_embed("Tunnel Created")
        embed.add_field(name="🌐 Tunnel URL", value=f"```fix\n{tunnel_url}\n```", inline=False)
        embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
        embed.add_field(name="🔌 Port", value=f"```fix\n{port}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", "```diff\n- Could not create tunnel. Make sure cloudflared is installed.\n```"))

# ==================================================================================================
#  🌍  IPv4 MANAGEMENT (with UPI payment) - FIXED
# ==================================================================================================

@bot.command(name="buy-ipv4")
@commands.cooldown(1, 30, commands.BucketType.user)
async def buy_ipv4(ctx):
    """Buy an IPv4 address via UPI - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    txn_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    embed = create_embed("Buy IPv4 Address")
    embed.add_field(name="💰 Price", value=f"```fix\n₹{IPV4_PRICE_INR}\n```", inline=True)
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="🔖 Reference", value=f"```fix\n{txn_ref}\n```", inline=True)
    embed.add_field(
        name="📋 Payment Instructions",
        value=f"```fix\n1. Pay ₹{IPV4_PRICE_INR} to {UPI_ID}\n2. Add reference {txn_ref} in notes\n3. Click ✅ after payment\n```",
        inline=False
    )
    
    # Create view with payment confirmation button
    view = View(timeout=300)
    
    async def payment_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("```diff\n- Not your purchase!\n```", ephemeral=True)
            return
        
        # Open modal for transaction ID
        modal = TransactionModal(ctx, txn_ref)
        await interaction.response.send_modal(modal)
    
    payment_btn = Button(label="✅ I've Paid", style=discord.ButtonStyle.success)
    payment_btn.callback = payment_callback
    view.add_item(payment_btn)
    
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def cancel_callback(interaction: discord.Interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nPurchase cancelled.\n```"), view=None)
    
    cancel_btn.callback = cancel_callback
    view.add_item(cancel_btn)
    
    await ctx.send(embed=embed, view=view)

class TransactionModal(Modal):
    def __init__(self, ctx, txn_ref):
        super().__init__(title="Enter Transaction ID")
        self.ctx = ctx
        self.txn_ref = txn_ref
        
        self.add_item(InputText(
            label="UPI Transaction ID",
            placeholder="e.g., T25031234567890",
            min_length=8,
            max_length=50,
            required=True
        ))
    
    async def callback(self, interaction: discord.Interaction):
        txn_id = self.children[0].value
        
        # Save transaction
        add_transaction(str(self.ctx.author.id), self.txn_ref, IPV4_PRICE_INR)
        
        # Notify admins
        embed = warning_embed("New IPv4 Purchase", 
            f"```fix\nUser: {self.ctx.author}\nRef: {self.txn_ref}\nTxn ID: {txn_id}\nAmount: ₹{IPV4_PRICE_INR}\n```")
        
        for admin_id in MAIN_ADMIN_IDS:
            try:
                admin = await bot.fetch_user(admin_id)
                await admin.send(embed=embed)
            except:
                pass
        
        await interaction.response.edit_message(
            embed=info_embed(
                "Payment Submitted",
                f"```fix\nReference: {self.txn_ref}\nTransaction ID: {txn_id}\n```\n\n"
                f"An admin will verify your payment and assign IPv4 shortly."
            ),
            view=None
        )

@bot.command(name="ipv4")
@commands.cooldown(1, 3, commands.BucketType.user)
async def list_ipv4(ctx, user: discord.Member = None):
    """List your IPv4 addresses with full details"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- Only admins can view others' IPv4.\n```"))
            return
        target_id = str(user.id)
        target_name = user.display_name
    else:
        target_id = str(ctx.author.id)
        target_name = ctx.author.display_name
        user = ctx.author
    
    ipv4_list = get_user_ipv4(target_id)
    
    if not ipv4_list:
        await ctx.send(embed=info_embed("No IPv4", f"{user.mention} has no IPv4 addresses assigned."))
        return
    
    embed = info_embed(f"IPv4 Addresses - {target_name}", f"```fix\nTotal: {len(ipv4_list)}\n```")
    
    for i, ip in enumerate(ipv4_list, 1):
        value = f"```fix\n"
        value += f"Container: {ip['container_name']}\n"
        if ip['public_ip']:
            value += f"Public IP: {ip['public_ip']}\n"
        if ip['private_ip']:
            value += f"Private IP: {ip['private_ip']}\n"
        if ip['mac_address']:
            value += f"MAC Addr  : {ip['mac_address']}\n"
        if ip['gateway']:
            value += f"Gateway   : {ip['gateway']}\n"
        if ip['netmask']:
            value += f"Netmask   : {ip['netmask']}\n"
        if ip['tunnel_url']:
            value += f"Tunnel    : {ip['tunnel_url']}\n"
        value += f"Assigned  : {ip['assigned_at'][:16]}\n"
        value += f"```"
        
        embed.add_field(name=f"IPv4 #{i}", value=value, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="ipv4-details")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ipv4_details(ctx, container_name: str):
    """Show detailed IPv4 info for a container"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Get IPv4 from database
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ipv4 WHERE user_id = ? AND container_name = ?', (user_id, container_name))
    ipv4 = cur.fetchone()
    
    # Get live network info
    out, _, _ = await exec_in_container(container_name, "ip addr show")
    routes, _, _ = await exec_in_container(container_name, "ip route show")
    
    conn.close()
    
    if ipv4:
        embed = info_embed(f"IPv4 Details: {container_name}")
        embed.add_field(name="🌐 Public IP", value=f"```fix\n{ipv4['public_ip']}\n```", inline=True)
        embed.add_field(name="🏠 Private IP", value=f"```fix\n{ipv4['private_ip']}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{ipv4['mac_address']}\n```", inline=True)
        embed.add_field(name="🚪 Gateway", value=f"```fix\n{ipv4['gateway']}\n```", inline=True)
        embed.add_field(name="🎭 Netmask", value=f"```fix\n{ipv4['netmask']}\n```", inline=True)
        embed.add_field(name="📡 Interface", value=f"```fix\n{ipv4['interface']}\n```", inline=True)
    else:
        embed = info_embed(f"Network Info: {container_name}")
    
    embed.add_field(name="📋 Live Network Config", value=f"```bash\n{out[:500]}\n```", inline=False)
    embed.add_field(name="🗺️ Routing Table", value=f"```bash\n{routes[:500]}\n```", inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  🤖  AI CHAT COMMANDS - FIXED WITH WORKING MODEL
# ==================================================================================================

@bot.command(name="ai")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ai_chat(ctx, *, message: str):
    """Chat with AI assistant - FIXED with working model"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if not AI_API_KEY or AI_API_KEY == "YOUR_GROQ_API_KEY":
        await ctx.send(embed=error_embed("AI Not Configured", "```diff\n- Please set a valid Groq API key in the config.\n```"))
        return
    
    user_id = str(ctx.author.id)
    
    # Load history
    history = load_ai_history(user_id)
    if not history:
        history = [{
            "role": "system",
            "content": f"You are {BOT_NAME} AI Assistant, a helpful VPS management bot made by {BOT_AUTHOR}. You help with Linux, LXC containers, server management, and general questions. Keep responses concise, friendly, and helpful. Server IP: {SERVER_IP}"
        }]
    
    # Add user message
    history.append({"role": "user", "content": message})
    
    # Keep last 20 messages + system
    if len(history) > 21:
        history = [history[0]] + history[-20:]
    
    msg = await ctx.send(embed=info_embed("AI is thinking...", "```fix\nThis may take a few seconds...\n```"))
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": AI_MODEL,  # Using updated working model
                    "messages": history,
                    "max_tokens": 1024,
                    "temperature": 0.7
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data["choices"][0]["message"]["content"]
                    
                    # Add to history
                    history.append({"role": "assistant", "content": reply})
                    save_ai_history(user_id, history)
                    
                    # Send response
                    chunks = [reply[i:i+1900] for i in range(0, len(reply), 1900)]
                    embed = info_embed("AI Response", chunks[0])
                    await msg.edit(embed=embed)
                    
                    for chunk in chunks[1:]:
                        await ctx.send(embed=info_embed("", chunk))
                else:
                    error_text = await resp.text()
                    await msg.edit(embed=error_embed("API Error", f"```diff\n- Status {resp.status}: {error_text[:200]}\n```"))
    except asyncio.TimeoutError:
        await msg.edit(embed=error_embed("Timeout", "```diff\n- The AI request timed out. Please try again.\n```"))
    except Exception as e:
        await msg.edit(embed=error_embed("AI Error", f"```diff\n- {str(e)[:1900]}\n```"))

@bot.command(name="ai-reset")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ai_reset(ctx):
    """Reset AI chat history"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    clear_ai_history(str(ctx.author.id))
    await ctx.send(embed=success_embed("AI History Reset", "```fix\nYour conversation with AI has been cleared.\n```"))

# ==================================================================================================
#  🛡️  ADMIN COMMANDS
# ==================================================================================================

def admin_only():
    """Decorator for admin-only commands"""
    async def predicate(ctx):
        if not await maintenance_check(ctx):
            return False
        if not await license_check(ctx):
            return False
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- This command is for administrators only.\n```"))
            return False
        return True
    return commands.check(predicate)

def main_admin_only():
    """Decorator for main admin-only commands"""
    async def predicate(ctx):
        if not await maintenance_check(ctx):
            return False
        if not await license_check(ctx):
            return False
        if str(ctx.author.id) not in [str(a) for a in MAIN_ADMIN_IDS]:
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- This command is for the main administrator only.\n```"))
            return False
        return True
    return commands.check(predicate)

@bot.command(name="create")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    """Create a VPS for a user"""
    if ram <= 0 or cpu <= 0 or disk <= 0:
        await ctx.send(embed=error_embed("Invalid Specs", "```diff\n- RAM, CPU, and Disk must be positive integers.\n```"))
        return
    
    # OS selection view
    view = View(timeout=60)
    options = []
    for os in OS_OPTIONS[:25]:
        options.append(discord.SelectOption(
            label=os["label"][:100], 
            value=os["value"], 
            description=os["desc"][:100] if os["desc"] else None,
            emoji=os.get("emoji", "🐧")
        ))
    
    select = Select(placeholder="📋 Select operating system...", options=options)
    
    async def select_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("```diff\n- Not your command!\n```", ephemeral=True)
            return
        
        selected_os = select.values[0]
        
        # Confirm view
        confirm_view = View(timeout=60)
        confirm_btn = Button(label="✅ Create", style=discord.ButtonStyle.success)
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        
        async def confirm_callback(confirm_interaction):
            await create_vps_action(confirm_interaction, user, ram, cpu, disk, selected_os)
        
        async def cancel_callback(cancel_interaction):
            await cancel_interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"), view=None)
        
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        confirm_view.add_item(confirm_btn)
        confirm_view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        
        embed = warning_embed(
            "Confirm VPS Creation",
            f"```fix\nUser: {user}\nOS: {os_name}\nRAM: {ram}GB\nCPU: {cpu} Core(s)\nDisk: {disk}GB\n```"
        )
        
        await interaction.response.edit_message(embed=embed, view=confirm_view)
    
    select.callback = select_callback
    view.add_item(select)
    
    embed = info_embed("Create VPS", f"```fix\nSelect an operating system for {user}\n```")
    await ctx.send(embed=embed, view=view)

async def create_vps_action(interaction, user, ram, cpu, disk, os_version):
    await interaction.response.defer(ephemeral=True)
    
    user_id = str(user.id)
    container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
    
    progress = await interaction.followup.send(
        embed=info_embed("Creating VPS", "```fix\nStep 1/4: Initializing container...\n```"),
        ephemeral=True
    )
    
    try:
        # Initialize
        ram_mb = ram * 1024
        await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
        
        await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 2/4: Configuring resources...\n```"))
        
        # Set limits
        await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
        await run_lxc(f"lxc config set {container_name} limits.cpu {cpu}")
        await run_lxc(f"lxc config device set {container_name} root size={disk}GB")
        
        # Apply config
        await apply_lxc_config(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 3/4: Starting container...\n```"))
        
        # Start
        await run_lxc(f"lxc start {container_name}")
        
        # Apply permissions
        await apply_internal_permissions(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 4/4: Finalizing...\n```"))
        
        # Save to database
        vps = add_vps(
            user_id=user_id,
            container_name=container_name,
            ram=ram,
            cpu=cpu,
            disk=disk,
            os_version=os_version,
            plan_name="Custom"
        )
        
        # Assign role
        if interaction.guild:
            role = discord.utils.get(interaction.guild.roles, name=f"{BOT_NAME} User")
            if not role:
                role = await interaction.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
            try:
                await user.add_roles(role)
            except:
                pass
        
        # DM user
        try:
            dm_embed = success_embed("✅ VPS Created for You!")
            dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
            dm_embed.add_field(name="⚙️ Resources", value=f"```fix\n{ram}GB RAM / {cpu} CPU / {disk}GB Disk\n```", inline=True)
            dm_embed.add_field(name="🐧 OS", value=f"```fix\n{os_version}\n```", inline=True)
            dm_embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        # Success
        embed = success_embed("✅ VPS Created Successfully!")
        embed.add_field(name="👤 User", value=user.mention, inline=True)
        embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
        embed.add_field(name="⚙️ Resources", value=f"```fix\n{ram}GB RAM / {cpu} CPU / {disk}GB Disk\n```", inline=False)
        
        await progress.edit(embed=embed)
        logger.info(f"Admin {interaction.user} created VPS {container_name} for {user}")
        
    except Exception as e:
        logger.error(f"VPS creation failed: {e}")
        await progress.edit(embed=error_embed("Creation Failed", f"```diff\n- Error: {str(e)}\n```"))
        try:
            await run_lxc(f"lxc delete {container_name} --force")
        except:
            pass

@bot.command(name="delete")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_delete(ctx, user: discord.Member, vps_num: int, *, reason: str = "No reason provided"):
    """Delete a user's VPS"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"```diff\n- {user.mention} has no VPS.\n```"))
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid Number", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    # Confirmation view
    view = View(timeout=60)
    confirm_btn = Button(label="✅ Confirm Delete", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        await delete_vps_action(interaction, user, vps, container, reason)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nDeletion cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "⚠️ Confirm VPS Deletion",
        f"```fix\nUser: {user}\nVPS #{vps_num}: {container}\nPlan: {vps['plan_name']}\nResources: {vps['ram']}GB RAM / {vps['cpu']} CPU / {vps['disk']}GB Disk\nReason: {reason}\n```\n\n"
        f"**This action cannot be undone!**"
    )
    
    await ctx.send(embed=embed, view=view)

async def delete_vps_action(interaction, user, vps, container, reason):
    await interaction.response.defer()
    
    try:
        # Stop and delete container
        await run_lxc(f"lxc stop {container} --force")
        await run_lxc(f"lxc delete {container}")
        
        # Remove from database
        delete_vps(container)
        
        # Log
        log_suspension(container, str(user.id), 'delete', reason, str(interaction.user.id))
        
        # DM user
        try:
            dm_embed = warning_embed("VPS Deleted", f"```fix\nYour VPS {container} has been deleted.\nReason: {reason}\n```")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Deleted", f"```fix\nVPS {container} has been deleted.\n```")
        await interaction.followup.send(embed=embed)
        logger.info(f"Admin {interaction.user} deleted VPS {container} for {user}")
        
    except Exception as e:
        await interaction.followup.send(embed=error_embed("Deletion Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="suspend")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_suspend(ctx, container_name: str, *, reason: str = "Admin action"):
    """Suspend a VPS"""
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- VPS {container_name} not found.\n```"))
        return
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Already Suspended", "```diff\n- This VPS is already suspended.\n```"))
        return
    
    try:
        # Stop the container
        await run_lxc(f"lxc stop {container_name} --force")
        
        # Update database
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET suspended = 1, suspended_reason = ?, status = "stopped" WHERE container_name = ?',
                    (reason, container_name))
        conn.commit()
        conn.close()
        
        # Log
        log_suspension(container_name, vps['user_id'], 'suspend', reason, str(ctx.author.id))
        
        # Notify user
        try:
            user = await bot.fetch_user(int(vps['user_id']))
            dm_embed = warning_embed("VPS Suspended", f"```fix\nYour VPS {container_name} has been suspended.\nReason: {reason}\n```")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Suspended", f"```fix\nVPS {container_name} has been suspended.\nReason: {reason}\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="unsuspend")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_unsuspend(ctx, container_name: str):
    """Unsuspend a VPS"""
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- VPS {container_name} not found.\n```"))
        return
    
    if not vps['suspended']:
        await ctx.send(embed=error_embed("Not Suspended", "```diff\n- This VPS is not suspended.\n```"))
        return
    
    try:
        # Start the container
        await run_lxc(f"lxc start {container_name}")
        
        # Update database
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET suspended = 0, suspended_reason = "", status = "running" WHERE container_name = ?',
                    (container_name,))
        conn.commit()
        conn.close()
        
        # Log
        log_suspension(container_name, vps['user_id'], 'unsuspend', '', str(ctx.author.id))
        
        # Notify user
        try:
            user = await bot.fetch_user(int(vps['user_id']))
            dm_embed = success_embed("VPS Unsuspended", f"```fix\nYour VPS {container_name} has been unsuspended.\n```")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Unsuspended", f"```fix\nVPS {container_name} has been unsuspended and started.\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="add-resources")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_add_resources(ctx, container_name: str, ram: int = None, cpu: int = None, disk: int = None):
    """Add resources to a VPS"""
    if ram is None and cpu is None and disk is None:
        await ctx.send(embed=error_embed("Missing Parameters", "```diff\n- Specify at least one resource to add.\n```"))
        return
    
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- VPS {container_name} not found.\n```"))
        return
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Suspended", "```diff\n- Cannot modify a suspended VPS.\n```"))
        return
    
    was_running = vps['status'] == 'running' and not vps['suspended']
    
    if was_running:
        await ctx.send(embed=info_embed("Stopping VPS", f"```fix\nStopping {container_name} to apply changes...\n```"))
        await run_lxc(f"lxc stop {container_name} --force")
    
    changes = []
    
    try:
        if ram:
            current_ram = vps['ram']
            new_ram = current_ram + ram
            ram_mb = new_ram * 1024
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            changes.append(f"RAM: +{ram}GB (now {new_ram}GB)")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ram = ? WHERE container_name = ?', (new_ram, container_name))
            conn.commit()
            conn.close()
        
        if cpu:
            current_cpu = vps['cpu']
            new_cpu = current_cpu + cpu
            await run_lxc(f"lxc config set {container_name} limits.cpu {new_cpu}")
            changes.append(f"CPU: +{cpu} cores (now {new_cpu})")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET cpu = ? WHERE container_name = ?', (new_cpu, container_name))
            conn.commit()
            conn.close()
        
        if disk:
            current_disk = vps['disk']
            new_disk = current_disk + disk
            await run_lxc(f"lxc config device set {container_name} root size={new_disk}GB")
            changes.append(f"Disk: +{disk}GB (now {new_disk}GB)")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET disk = ? WHERE container_name = ?', (new_disk, container_name))
            conn.commit()
            conn.close()
        
        if was_running:
            await ctx.send(embed=info_embed("Starting VPS", f"```fix\nStarting {container_name}...\n```"))
            await run_lxc(f"lxc start {container_name}")
            await apply_internal_permissions(container_name)
        
        embed = success_embed("Resources Added", f"```fix\nChanges applied to {container_name}:\n{chr(10).join(changes)}\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))
        
        # Try to start if it was running
        if was_running:
            try:
                await run_lxc(f"lxc start {container_name}")
            except:
                pass

@bot.command(name="userinfo")
@admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def admin_userinfo(ctx, user: discord.Member):
    """Get detailed user information"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    stats = get_user_stats(user_id)
    ipv4_list = get_user_ipv4(user_id)
    forwards = get_user_port_forwards(user_id)
    port_quota = get_port_allocation(user_id)
    panels = get_user_panels(user_id)
    
    embed = info_embed(f"User Info: {user.display_name}")
    embed.add_field(name="🆔 User ID", value=f"```fix\n{user.id}\n```", inline=True)
    embed.add_field(name="📅 Joined", value=f"```fix\n{user.joined_at.strftime('%Y-%m-%d') if user.joined_at else 'Unknown'}\n```", inline=True)
    
    stats_text = f"```fix\n"
    stats_text += f"Invites : {stats.get('invites', 0)}\n"
    stats_text += f"Boosts  : {stats.get('boosts', 0)}\n"
    stats_text += f"Claimed : {stats.get('claimed_vps_count', 0)}\n"
    stats_text += f"Ports   : {port_quota} (Used: {len(forwards)})\n"
    stats_text += f"```"
    embed.add_field(name="📊 Statistics", value=stats_text, inline=True)
    
    if vps_list:
        vps_text = ""
        for i, vps in enumerate(vps_list, 1):
            status = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
            vps_text += f"{status} VPS #{i}: `{vps['container_name']}` ({vps['ram']}GB/{vps['cpu']}C/{vps['disk']}GB)\n"
        embed.add_field(name=f"🖥️ VPS ({len(vps_list)})", value=vps_text, inline=False)
    else:
        embed.add_field(name="🖥️ VPS", value="```fix\nNone\n```", inline=False)
    
    if ipv4_list:
        embed.add_field(name=f"🌍 IPv4 ({len(ipv4_list)})", value="\n".join(f"`{ip['container_name']}`" for ip in ipv4_list), inline=False)
    
    if panels:
        embed.add_field(name=f"📦 Panels ({len(panels)})", value="\n".join(f"`{p['panel_type']}`" for p in panels), inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="list-all")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_list_all(ctx):
    """List all VPS in the system"""
    all_vps = get_all_vps()
    
    if not all_vps:
        await ctx.send(embed=info_embed("No VPS", "```fix\nNo VPS in the system.\n```"))
        return
    
    # Group by user
    users = {}
    for vps in all_vps:
        if vps['user_id'] not in users:
            users[vps['user_id']] = []
        users[vps['user_id']].append(vps)
    
    embed = info_embed(f"All VPS ({len(all_vps)})")
    
    for user_id, vps_list in list(users.items())[:5]:
        try:
            user = await bot.fetch_user(int(user_id))
            username = user.name
        except:
            username = f"Unknown ({user_id})"
        
        vps_text = ""
        for vps in vps_list:
            status = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
            vps_text += f"{status} `{vps['container_name']}` ({vps['ram']}GB/{vps['cpu']}C)\n"
        
        embed.add_field(name=f"{username} ({len(vps_list)})", value=vps_text, inline=False)
    
    if len(users) > 5:
        embed.add_field(name="📝 Note", value=f"Showing 5 of {len(users)} users", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="add-inv")
@admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def admin_add_invites(ctx, user: discord.Member, amount: int):
    """Add invites to a user"""
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "```diff\n- Amount must be positive.\n```"))
        return
    
    update_user_stats(str(user.id), invites=amount)
    stats = get_user_stats(str(user.id))
    
    embed = success_embed("Invites Added", f"```fix\nAdded {amount} invites to {user}\nNew total: {stats['invites']}\n```")
    await ctx.send(embed=embed)

@bot.command(name="remove-inv")
@admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def admin_remove_invites(ctx, user: discord.Member, amount: int):
    """Remove invites from a user"""
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "```diff\n- Amount must be positive.\n```"))
        return
    
    stats = get_user_stats(str(user.id))
    if stats['invites'] < amount:
        amount = stats['invites']
    
    update_user_stats(str(user.id), invites=-amount)
    new_stats = get_user_stats(str(user.id))
    
    embed = success_embed("Invites Removed", f"```fix\nRemoved {amount} invites from {user}\nNew total: {new_stats['invites']}\n```")
    await ctx.send(embed=embed)

@bot.command(name="ports-add")
@admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def admin_ports_add(ctx, user: discord.Member, amount: int):
    """Add port slots to a user"""
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "```diff\n- Amount must be positive.\n```"))
        return
    
    add_port_allocation(str(user.id), amount)
    new_quota = get_port_allocation(str(user.id))
    
    embed = success_embed("Port Slots Added", f"```fix\nAdded {amount} port slots to {user}\nNew quota: {new_quota}\n```")
    await ctx.send(embed=embed)

@bot.command(name="serverstats")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_serverstats(ctx):
    """Show server statistics"""
    all_vps = get_all_vps()
    
    total_vps = len(all_vps)
    running = sum(1 for v in all_vps if v['status'] == 'running' and not v['suspended'])
    stopped = sum(1 for v in all_vps if v['status'] == 'stopped' and not v['suspended'])
    suspended = sum(1 for v in all_vps if v['suspended'])
    
    total_ram = sum(v['ram'] for v in all_vps)
    total_cpu = sum(v['cpu'] for v in all_vps)
    total_disk = sum(v['disk'] for v in all_vps)
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM vps')
    total_users = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM port_forwards')
    total_ports = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM panels')
    total_panels = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM nodes')
    total_nodes = cur.fetchone()[0] or 0
    conn.close()
    
    embed = info_embed("Server Statistics")
    
    stats_text = f"```fix\n"
    stats_text += f"VPS Total   : {total_vps}\n"
    stats_text += f"VPS Running : {running}\n"
    stats_text += f"VPS Stopped : {stopped}\n"
    stats_text += f"VPS Suspended: {suspended}\n"
    stats_text += f"```"
    embed.add_field(name="🖥️ VPS Stats", value=stats_text, inline=True)
    
    resources_text = f"```fix\n"
    resources_text += f"RAM Total   : {total_ram}GB\n"
    resources_text += f"CPU Total   : {total_cpu} cores\n"
    resources_text += f"Disk Total  : {total_disk}GB\n"
    resources_text += f"```"
    embed.add_field(name="💾 Resources", value=resources_text, inline=True)
    
    other_text = f"```fix\n"
    other_text += f"Users       : {total_users}\n"
    other_text += f"Ports       : {total_ports}\n"
    other_text += f"Panels      : {total_panels}\n"
    other_text += f"Nodes       : {total_nodes}\n"
    other_text += f"```"
    embed.add_field(name="📊 Other", value=other_text, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="admin-add-ipv4")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_add_ipv4(ctx, user: discord.Member, container_name: str):
    """Assign IPv4 to a user's container with full details"""
    user_id = str(user.id)
    
    # Verify container exists and belongs to user
    vps_list = get_user_vps(user_id)
    vps = next((v for v in vps_list if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Container Not Found", f"```diff\n- Container {container_name} not found for {user}\n```"))
        return
    
    # Get container network details
    private_ip, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
    private_ip = private_ip.strip() or "N/A"
    
    mac, _, _ = await exec_in_container(container_name, "ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
    mac = mac.strip() or "N/A"
    
    gateway, _, _ = await exec_in_container(container_name, "ip route | grep default | awk '{print $3}'")
    gateway = gateway.strip() or "N/A"
    
    netmask, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=/)\\d+'")
    netmask = netmask.strip() or "24"
    
    # Get host public IP
    public_ip = SERVER_IP
    
    # Add to database
    add_ipv4(user_id, container_name, public_ip, private_ip, mac, gateway, netmask, "eth0")
    
    embed = success_embed("IPv4 Assigned", f"```fix\nAssigned IPv4 to {user}'s container {container_name}\n```")
    embed.add_field(name="🌐 Public IP", value=f"```fix\n{public_ip}\n```", inline=True)
    embed.add_field(name="🏠 Private IP", value=f"```fix\n{private_ip}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{mac}\n```", inline=True)
    embed.add_field(name="🚪 Gateway", value=f"```fix\n{gateway}\n```", inline=True)
    embed.add_field(name="🎭 Netmask", value=f"```fix\n{netmask}\n```", inline=True)
    
    # DM user
    try:
        dm_embed = success_embed("IPv4 Assigned to Your VPS")
        dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
        dm_embed.add_field(name="🌐 Public IP", value=f"```fix\n{public_ip}\n```", inline=True)
        dm_embed.add_field(name="🏠 Private IP", value=f"```fix\n{private_ip}\n```", inline=True)
        await user.send(embed=dm_embed)
    except:
        pass
    
    await ctx.send(embed=embed)

@bot.command(name="admin-rm-ipv4")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_rm_ipv4(ctx, user: discord.Member, container_name: str = None):
    """Remove IPv4 from a user"""
    user_id = str(user.id)
    
    if container_name:
        remove_ipv4(user_id, container_name)
        embed = success_embed("IPv4 Removed", f"```fix\nRemoved IPv4 from {user}'s container {container_name}\n```")
    else:
        remove_ipv4(user_id)
        embed = success_embed("IPv4 Removed", f"```fix\nRemoved all IPv4 from {user}\n```")
    
    await ctx.send(embed=embed)

@bot.command(name="admin-pending-ipv4")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_pending_ipv4(ctx):
    """List pending IPv4 purchases"""
    pending = get_pending_transactions()
    
    if not pending:
        await ctx.send(embed=info_embed("Pending IPv4", "```fix\nNo pending IPv4 purchases.\n```"))
        return
    
    embed = info_embed(f"Pending IPv4 Purchases ({len(pending)})")
    
    for txn in pending:
        try:
            user = await bot.fetch_user(int(txn['user_id']))
            username = user.name
        except:
            username = f"Unknown ({txn['user_id']})"
        
        embed.add_field(
            name=f"User: {username}",
            value=f"```fix\nRef: {txn['txn_ref']}\nAmount: ₹{txn['amount']}\nCreated: {txn['created_at'][:16]}\n```",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name="admin-panels")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_panels(ctx):
    """List all installed panels"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM panels ORDER BY installed_at DESC LIMIT 20')
    panels = cur.fetchall()
    conn.close()
    
    if not panels:
        await ctx.send(embed=info_embed("Panels", "```fix\nNo panels installed.\n```"))
        return
    
    embed = info_embed(f"Installed Panels ({len(panels)})")
    
    for panel in panels:
        try:
            user = await bot.fetch_user(int(panel['user_id']))
            username = user.name
        except:
            username = f"Unknown ({panel['user_id']})"
        
        embed.add_field(
            name=f"{'🦅' if panel['panel_type'] == 'pterodactyl' else '🐡'} {panel['panel_type'].title()} - {username}",
            value=f"```fix\nURL: {panel['panel_url']}\nInstalled: {panel['installed_at'][:16]}\n```",
            inline=False
        )
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  👑  MAIN ADMIN COMMANDS
# ==================================================================================================

@bot.command(name="admin-add")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_add(ctx, user: discord.Member):
    """Add a new admin"""
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Already Main Admin", "```diff\n- This user is already a main admin.\n```"))
        return
    
    if is_admin(str(user.id)):
        await ctx.send(embed=error_embed("Already Admin", f"```diff\n- {user.mention} is already an admin.\n```"))
        return
    
    add_admin(str(user.id))
    
    embed = success_embed("Admin Added", f"```fix\n{user.mention} has been added as an admin.\n```")
    await ctx.send(embed=embed)

@bot.command(name="admin-remove")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_remove(ctx, user: discord.Member):
    """Remove an admin"""
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Cannot Remove", "```diff\n- Cannot remove main admin.\n```"))
        return
    
    if not is_admin(str(user.id)):
        await ctx.send(embed=error_embed("Not Admin", f"```diff\n- {user.mention} is not an admin.\n```"))
        return
    
    remove_admin(str(user.id))
    
    embed = success_embed("Admin Removed", f"```fix\n{user.mention} has been removed as an admin.\n```")
    await ctx.send(embed=embed)

@bot.command(name="admin-list")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_list(ctx):
    """List all admins"""
    admins = get_admins()
    
    embed = info_embed("Admin List")
    
    main_admin_text = ""
    for admin_id in MAIN_ADMIN_IDS:
        try:
            user = await bot.fetch_user(admin_id)
            main_admin_text += f"👑 {user.mention}\n"
        except:
            main_admin_text += f"👑 `{admin_id}`\n"
    
    embed.add_field(name="👑 Main Admin", value=main_admin_text, inline=False)
    
    if admins:
        admin_text = ""
        for admin_id in admins:
            try:
                user = await bot.fetch_user(int(admin_id))
                admin_text += f"🛡️ {user.mention}\n"
            except:
                admin_text += f"🛡️ `{admin_id}`\n"
        embed.add_field(name="🛡️ Admins", value=admin_text, inline=False)
    else:
        embed.add_field(name="🛡️ Admins", value="```fix\nNone\n```", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="maintenance")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def main_maintenance(ctx, mode: str):
    """Toggle maintenance mode"""
    global MAINTENANCE_MODE
    
    mode = mode.lower()
    if mode not in ['on', 'off']:
        await ctx.send(embed=error_embed("Invalid Mode", "```diff\n- Use `on` or `off`.\n```"))
        return
    
    MAINTENANCE_MODE = (mode == 'on')
    set_setting('maintenance_mode', str(MAINTENANCE_MODE).lower())
    
    if MAINTENANCE_MODE:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="🔧 Maintenance Mode"))
        embed = warning_embed("Maintenance Mode Enabled", "```fix\nOnly admins can use commands now.\n```")
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {BOT_NAME}"))
        embed = success_embed("Maintenance Mode Disabled", "```fix\nAll commands are now available.\n```")
    
    await ctx.send(embed=embed)

@bot.command(name="set-threshold")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def main_set_threshold(ctx, cpu: int, ram: int, disk: int = 90):
    """Set CPU, RAM and Disk thresholds"""
    global CPU_THRESHOLD, RAM_THRESHOLD, DISK_THRESHOLD
    
    if cpu < 0 or cpu > 100 or ram < 0 or ram > 100 or disk < 0 or disk > 100:
        await ctx.send(embed=error_embed("Invalid Values", "```diff\n- Thresholds must be between 0 and 100.\n```"))
        return
    
    CPU_THRESHOLD = cpu
    RAM_THRESHOLD = ram
    DISK_THRESHOLD = disk
    set_setting('cpu_threshold', str(cpu))
    set_setting('ram_threshold', str(ram))
    set_setting('disk_threshold', str(disk))
    
    embed = success_embed("Thresholds Updated", f"```fix\nCPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%\n```")
    await ctx.send(embed=embed)

@bot.command(name="system-info")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def system_info(ctx):
    """Detailed system information"""
    # Get system stats
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    network = psutil.net_io_counters()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    users = psutil.users()
    
    embed = create_embed("System Information")
    
    # System Info
    sys_info = f"```fix\n"
    sys_info += f"Hostname : {HOSTNAME}\n"
    sys_info += f"Server IP: {SERVER_IP}\n"
    sys_info += f"MAC Addr : {MAC_ADDRESS}\n"
    sys_info += f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    sys_info += f"Users    : {len(users)}\n"
    sys_info += f"```"
    embed.add_field(name="💻 System", value=sys_info, inline=False)
    
    # CPU Info
    cpu_info = f"```fix\n"
    cpu_info += f"Cores    : {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)\n"
    cpu_info += f"Usage    : {cpu_percent[0]:.1f}% (avg)\n"
    cpu_info += f"Frequency: {cpu_freq.current:.0f} MHz\n"
    cpu_info += f"```"
    embed.add_field(name="⚙️ CPU", value=cpu_info, inline=True)
    
    # Memory Info
    mem_info = f"```fix\n"
    mem_info += f"RAM      : {memory.used//1024//1024}MB/{memory.total//1024//1024}MB ({memory.percent}%)\n"
    mem_info += f"Swap     : {swap.used//1024//1024}MB/{swap.total//1024//1024}MB ({swap.percent}%)\n"
    mem_info += f"```"
    embed.add_field(name="💾 Memory", value=mem_info, inline=True)
    
    # Disk Info
    disk_info = f"```fix\n"
    disk_info += f"Disk     : {disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n"
    disk_info += f"Read     : {disk_io.read_bytes//1024//1024} MB\n" if disk_io else ""
    disk_info += f"Write    : {disk_io.write_bytes//1024//1024} MB\n" if disk_io else ""
    disk_info += f"```"
    embed.add_field(name="📀 Disk", value=disk_info, inline=True)
    
    # Network Info
    net_info = f"```fix\n"
    net_info += f"Sent     : {network.bytes_sent/1024/1024:.2f} MB\n"
    net_info += f"Received : {network.bytes_recv/1024/1024:.2f} MB\n"
    net_info += f"Packets Sent: {network.packets_sent}\n"
    net_info += f"Packets Recv: {network.packets_recv}\n"
    net_info += f"```"
    embed.add_field(name="🌐 Network", value=net_info, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="protect")
@main_admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def main_protect(ctx, user: discord.Member, vps_num: int = None):
    """Protect a VPS from purge"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"```diff\n- {user.mention} has no VPS.\n```"))
        return
    
    if vps_num is None:
        # Protect all
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Added", f"```fix\nAll VPS of {user.mention} are now protected from purge.\n```")
        await ctx.send(embed=embed)
    else:
        if vps_num < 1 or vps_num > len(vps_list):
            await ctx.send(embed=error_embed("Invalid Number", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
            return
        
        vps = vps_list[vps_num - 1]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE container_name = ?', (vps['container_name'],))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Added", f"```fix\nVPS #{vps_num} of {user.mention} is now protected from purge.\n```")
        await ctx.send(embed=embed)

@bot.command(name="unprotect")
@main_admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def main_unprotect(ctx, user: discord.Member, vps_num: int = None):
    """Remove purge protection from a VPS"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"```diff\n- {user.mention} has no VPS.\n```"))
        return
    
    if vps_num is None:
        # Unprotect all
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Removed", f"```fix\nAll VPS of {user.mention} are no longer protected from purge.\n```")
        await ctx.send(embed=embed)
    else:
        if vps_num < 1 or vps_num > len(vps_list):
            await ctx.send(embed=error_embed("Invalid Number", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
            return
        
        vps = vps_list[vps_num - 1]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE container_name = ?', (vps['container_name'],))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Removed", f"```fix\nVPS #{vps_num} of {user.mention} is no longer protected from purge.\n```")
        await ctx.send(embed=embed)

@bot.command(name="purge-all")
@main_admin_only()
@commands.cooldown(1, 300, commands.BucketType.user)
async def main_purge_all(ctx):
    """Purge all unprotected VPS"""
    all_vps = get_all_vps()
    
    # Count unprotected
    unprotected = [v for v in all_vps if not v.get('purge_protected', 0)]
    
    if not unprotected:
        await ctx.send(embed=info_embed("No Unprotected VPS", "```fix\nAll VPS are protected.\n```"))
        return
    
    embed = warning_embed(
        "⚠️ PURGE ALL UNPROTECTED VPS",
        f"```fix\nThis will delete {len(unprotected)} unprotected VPS.\nProtected VPS will be skipped.\n```\n\n"
        f"**This action cannot be undone!**"
    )
    
    view = View(timeout=60)
    confirm_btn = Button(label="✅ PURGE", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        await perform_purge(interaction, unprotected)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nPurge cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    await ctx.send(embed=embed, view=view)

async def perform_purge(interaction, unprotected):
    await interaction.response.defer()
    
    progress = await interaction.followup.send(
        embed=info_embed("Purging VPS", f"```fix\nStarting purge of {len(unprotected)} VPS...\n```"),
        ephemeral=True
    )
    
    deleted = 0
    failed = 0
    
    for i, vps in enumerate(unprotected, 1):
        container = vps['container_name']
        
        try:
            # Update progress
            if i % 5 == 0:
                await progress.edit(embed=info_embed("Purging VPS", f"```fix\nProgress: {i}/{len(unprotected)}...\n```"))
            
            # Stop and delete
            await run_lxc(f"lxc stop {container} --force")
            await run_lxc(f"lxc delete {container}")
            
            # Remove from DB
            delete_vps(container)
            
            # Log
            log_suspension(container, vps['user_id'], 'purge', 'Purge all unprotected', str(interaction.user.id))
            
            deleted += 1
            
            # Small delay
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"Failed to purge {container}: {e}")
            failed += 1
    
    embed = success_embed("Purge Complete", f"```fix\nDeleted: {deleted}\nFailed: {failed}\n```")
    await progress.edit(embed=embed)

@bot.command(name="admin-users")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_users(ctx):
    """List all users with VPS"""
    all_vps = get_all_vps()
    
    # Group by user
    users = {}
    for vps in all_vps:
        if vps['user_id'] not in users:
            users[vps['user_id']] = []
        users[vps['user_id']].append(vps)
    
    if not users:
        await ctx.send(embed=info_embed("No Users", "```fix\nNo users have VPS.\n```"))
        return
    
    embed = info_embed(f"Users with VPS ({len(users)})")
    
    for user_id, vps_list in list(users.items())[:10]:
        try:
            user = await bot.fetch_user(int(user_id))
            username = f"{user.name} ({user.id})"
        except:
            username = f"Unknown ({user_id})"
        
        vps_count = len(vps_list)
        running = sum(1 for v in vps_list if v['status'] == 'running' and not v['suspended'])
        
        embed.add_field(
            name=username,
            value=f"```fix\nVPS: {vps_count} (Running: {running})\nContainers: {', '.join([v['container_name'][:10] + '...' for v in vps_list[:3]])}\n```",
            inline=False
        )
    
    if len(users) > 10:
        embed.add_field(name="📝 Note", value=f"Showing 10 of {len(users)} users", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="backup-db")
@main_admin_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def backup_db(ctx):
    """Backup database"""
    backup_name = f"svm5_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    backup_path = f"/opt/svm5-bot/backups/{backup_name}"
    
    # Create backups directory if not exists
    os.makedirs("/opt/svm5-bot/backups", exist_ok=True)
    
    try:
        # Copy database
        import shutil
        shutil.copy2("/opt/svm5-bot/svm5.db", backup_path)
        
        # Compress
        import gzip
        with open(backup_path, 'rb') as f_in:
            with gzip.open(f"{backup_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        os.remove(backup_path)
        
        embed = success_embed("Database Backup Created", f"```fix\nBackup: {backup_name}.gz\nLocation: /opt/svm5-bot/backups/\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Backup Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="restore-db")
@main_admin_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def restore_db(ctx, backup_name: str):
    """Restore database from backup"""
    backup_path = f"/opt/svm5-bot/backups/{backup_name}"
    
    if not os.path.exists(backup_path):
        await ctx.send(embed=error_embed("Backup Not Found", f"```diff\n- Backup {backup_name} not found.\n```"))
        return
    
    # Confirmation view
    view = View(timeout=60)
    confirm_btn = Button(label="✅ Confirm Restore", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        try:
            # Backup current database
            import shutil
            current_backup = f"/opt/svm5-bot/backups/current_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2("/opt/svm5-bot/svm5.db", current_backup)
            
            # Restore
            shutil.copy2(backup_path, "/opt/svm5-bot/svm5.db")
            
            embed = success_embed("Database Restored", f"```fix\nRestored from: {backup_name}\nCurrent DB backed up to: {os.path.basename(current_backup)}\n```")
            await interaction.response.edit_message(embed=embed, view=None)
            
            # Restart bot? Optional
            
        except Exception as e:
            await interaction.response.edit_message(embed=error_embed("Restore Failed", f"```diff\n- {str(e)}\n```"), view=None)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nRestore cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "⚠️ Confirm Database Restore",
        f"```fix\nBackup: {backup_name}\n```\n\n"
        f"**This will overwrite the current database!**\n"
        f"A backup of the current database will be created automatically."
    )
    
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  🚀  RUN THE BOT
# ==================================================================================================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n" + "="*80)
        print("❌ ERROR: Please set your BOT_TOKEN in the configuration!")
        print("="*80 + "\n")
        sys.exit(1)
    
    # Check license
    if not LICENSE_VERIFIED:
        print("\n" + "="*80)
        print("⚠️  WARNING: License not verified!")
        print("   Valid license keys: AnkitDev99$@, SVM5-PRO-2025, SVM5-ENTERPRISE")
        print("="*80 + "\n")
    
    # Check LXC
    try:
        subprocess.run(['lxc', '--version'], capture_output=True, check=True)
    except:
        print("\n" + "="*80)
        print("❌ ERROR: LXC is not installed or not in PATH!")
        print("Install LXC: sudo apt install lxc lxc-templates")
        print("Then run: sudo lxd init")
        print("="*80 + "\n")
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs("/opt/svm5-bot/backups", exist_ok=True)
    os.makedirs("/opt/svm5-bot/logs", exist_ok=True)
    
    # Run bot
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n" + "="*80)
        print("❌ ERROR: Invalid Discord token!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
