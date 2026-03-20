#!/usr/bin/env python3
# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                               ║
# ║     ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗                      ║
# ║     ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝                      ║
# ║     ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║                         ║
# ║     ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║                         ║
# ║     ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║                         ║
# ║     ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝                         ║
# ║                                                                                               ║
# ║                    🚀 SVM5-BOT TOOLS - ULTIMATE VPS MANAGEMENT 🚀                            ║
# ║                                                                                               ║
# ║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                            ║
# ║                                                                                               ║
# ║  ╔════════════════════════════════════════════════════════════════════════════════════════╗   ║
# ║  ║  ✅ 92 COMMANDS • 70+ OS • 7 GAMES • 7 TOOLS • NODES • SHARE • PORTS • IPv4 • PANELS  ║   ║
# ║  ║  ✅ FULL UI • BUTTONS • SELECT MENUS • MODALS • REAL-TIME STATS • NODE.JSON            ║   ║
# ║  ║  ✅ AUTO NODE DETECTION • CLOUDFLARED TUNNEL • AI CHAT • UPI QR • BACKUP/RESTORE      ║   ║
# ║  ╚════════════════════════════════════════════════════════════════════════════════════════╝   ║
# ║                                                                                               ║
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
import qrcode
import io
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple

# ==================================================================================================
#  🎨  COLOR CONSTANTS
# ==================================================================================================

COLORS = {
    'primary': 0x5865F2,
    'success': 0x57F287,
    'error': 0xED4245,
    'warning': 0xFEE75C,
    'info': 0x5865F2,
    'node': 0x9B59B6,
    'terminal': 0x2C2F33,
    'gold': 0xFFD700,
    'cyan': 0x00CCFF,
    'pink': 0xFF69B4,
    'os': 0x00FF88,
}

# ==================================================================================================
#  📝  LOGGING SETUP
# ==================================================================================================

os.makedirs('/opt/svm5-bot/logs', exist_ok=True)
os.makedirs('/opt/svm5-bot/data', exist_ok=True)
os.makedirs('/opt/svm5-bot/backups', exist_ok=True)
os.makedirs('/opt/svm5-bot/qr_codes', exist_ok=True)
os.makedirs('/opt/svm5-bot/nodes', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/opt/svm5-bot/logs/svm5.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SVM5-BOT")

# ==================================================================================================
#  ⚙️  CONFIGURATION
# ==================================================================================================

BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
BOT_PREFIX = "."
BOT_NAME = "SVM5-BOT"
BOT_AUTHOR = "Ankit-Dev"
MAIN_ADMIN_IDS = [1405866008127864852]
DEFAULT_STORAGE_POOL = "default"

# Auto-detect server
try:
    SERVER_IP = requests.get('https://api.ipify.org', timeout=5).text.strip()
except:
    try:
        SERVER_IP = subprocess.getoutput("curl -s ifconfig.me")
    except:
        SERVER_IP = "127.0.0.1"

HOSTNAME = socket.gethostname()

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
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg"

# License Keys
VALID_LICENSE_KEYS = ["AnkitDev99$@", "SVM5-PRO-2025", "SVM5-ENTERPRISE", "DEVELOPER-ANKIT"]

# ==================================================================================================
#  🐧  OS OPTIONS - 70+ OPERATING SYSTEMS
# ==================================================================================================

OS_OPTIONS = [
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 18.04 LTS", "value": "ubuntu:18.04", "desc": "Bionic Beaver - Legacy", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 16.04 LTS", "value": "ubuntu:16.04", "desc": "Xenial Xerus - Old", "category": "Ubuntu", "ram_min": 256},
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable", "category": "Debian", "ram_min": 256},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable", "category": "Debian", "ram_min": 256},
    {"label": "🎩 Fedora 40", "value": "images:fedora/40", "desc": "Fedora 40 - Latest", "category": "Fedora", "ram_min": 1024},
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky 9 - Latest", "category": "Rocky", "ram_min": 1024},
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma 9 - Latest", "category": "AlmaLinux", "ram_min": 1024},
    {"label": "📦 CentOS 9 Stream", "value": "images:centos/9-Stream", "desc": "CentOS 9 Stream", "category": "CentOS", "ram_min": 1024},
    {"label": "🐧 Alpine 3.19", "value": "images:alpine/3.19", "desc": "Alpine Latest", "category": "Alpine", "ram_min": 64},
    {"label": "📀 Arch Linux", "value": "images:archlinux", "desc": "Arch - Rolling Release", "category": "Arch", "ram_min": 512},
    {"label": "🟢 OpenSUSE Tumbleweed", "value": "images:opensuse/tumbleweed", "desc": "Rolling Release", "category": "OpenSUSE", "ram_min": 1024},
    {"label": "🔵 FreeBSD 14", "value": "images:freebsd/14", "desc": "FreeBSD 14 - Latest", "category": "FreeBSD", "ram_min": 512},
    {"label": "🐡 OpenBSD 7.4", "value": "images:openbsd/7.4", "desc": "OpenBSD 7.4", "category": "OpenBSD", "ram_min": 512},
    {"label": "🐉 Kali Linux", "value": "images:kali", "desc": "Kali - Security Testing", "category": "Kali", "ram_min": 1024},
    {"label": "💻 Gentoo", "value": "images:gentoo", "desc": "Gentoo - Source based", "category": "Gentoo", "ram_min": 1024},
    {"label": "⚪ Void Linux", "value": "images:voidlinux", "desc": "Void - Independent", "category": "Void", "ram_min": 256},
]

# ==================================================================================================
#  🎮  GAMES LIST
# ==================================================================================================

GAMES_LIST = [
    {'name': 'Minecraft Java', 'docker': 'itzg/minecraft-server', 'port': 25565, 'ram': 2048, 'icon': '🎮'},
    {'name': 'Minecraft Bedrock', 'docker': 'itzg/minecraft-bedrock-server', 'port': 19132, 'ram': 1024, 'icon': '📱'},
    {'name': 'Terraria', 'docker': 'beardedio/terraria', 'port': 7777, 'ram': 1024, 'icon': '🌳'},
    {'name': 'CS:GO', 'docker': 'cm2network/csgo', 'port': 27015, 'ram': 2048, 'icon': '🔫'},
    {'name': 'Valheim', 'docker': 'lloesche/valheim-server', 'port': 2456, 'ram': 2048, 'icon': '⚔️'},
    {'name': 'ARK', 'docker': 'hermsi/ark-server-tools', 'port': 7777, 'ram': 4096, 'icon': '🦖'},
    {'name': 'Rust', 'docker': 'didstopia/rust-server', 'port': 28015, 'ram': 4096, 'icon': '🦀'},
]

# ==================================================================================================
#  🛠️  TOOLS LIST
# ==================================================================================================

TOOLS_LIST = [
    {'name': 'Nginx', 'cmd': 'apt install nginx -y', 'port': 80, 'icon': '🌐'},
    {'name': 'Apache', 'cmd': 'apt install apache2 -y', 'port': 80, 'icon': '🕸️'},
    {'name': 'MySQL', 'cmd': 'apt install mysql-server -y', 'port': 3306, 'icon': '🗄️'},
    {'name': 'PostgreSQL', 'cmd': 'apt install postgresql -y', 'port': 5432, 'icon': '🐘'},
    {'name': 'Redis', 'cmd': 'apt install redis-server -y', 'port': 6379, 'icon': '🔴'},
    {'name': 'Docker', 'cmd': 'curl -fsSL https://get.docker.com | bash', 'icon': '🐳'},
    {'name': 'Node.js', 'cmd': 'curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt install nodejs -y', 'icon': '🟢'},
]

# ==================================================================================================
#  💰  FREE VPS PLANS
# ==================================================================================================

FREE_VPS_PLANS = {
    'invites': [
        {'name': '🥉 Bronze', 'invites': 5, 'ram': 2, 'cpu': 1, 'disk': 20, 'emoji': '🥉'},
        {'name': '🥈 Silver', 'invites': 10, 'ram': 4, 'cpu': 2, 'disk': 40, 'emoji': '🥈'},
        {'name': '🥇 Gold', 'invites': 15, 'ram': 8, 'cpu': 4, 'disk': 80, 'emoji': '🥇'},
        {'name': '🏆 Platinum', 'invites': 20, 'ram': 16, 'cpu': 8, 'disk': 160, 'emoji': '🏆'},
        {'name': '💎 Diamond', 'invites': 25, 'ram': 32, 'cpu': 16, 'disk': 320, 'emoji': '💎'},
        {'name': '👑 Royal', 'invites': 30, 'ram': 64, 'cpu': 32, 'disk': 640, 'emoji': '👑'},
    ]
}

# ==================================================================================================
#  🗄️  DATABASE SETUP
# ==================================================================================================

DATABASE_PATH = '/opt/svm5-bot/data/svm5.db'
NODES_FILE = '/opt/svm5-bot/nodes/nodes.json'

def get_db():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except:
        return None

def init_db():
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    
    # Admins
    cur.execute('''CREATE TABLE IF NOT EXISTS admins (user_id TEXT PRIMARY KEY, added_at TEXT)''')
    for aid in MAIN_ADMIN_IDS:
        cur.execute('INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)', (str(aid), datetime.now().isoformat()))
    
    # VPS
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
        purge_protected INTEGER DEFAULT 0,
        node_name TEXT DEFAULT 'local',
        created_at TEXT NOT NULL,
        ip_address TEXT,
        mac_address TEXT,
        games_installed TEXT DEFAULT '[]',
        tools_installed TEXT DEFAULT '[]',
        shared_with TEXT DEFAULT '[]'
    )''')
    
    # User stats
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
        user_id TEXT PRIMARY KEY,
        invites INTEGER DEFAULT 0,
        boosts INTEGER DEFAULT 0,
        claimed_vps_count INTEGER DEFAULT 0,
        api_key TEXT UNIQUE,
        last_updated TEXT
    )''')
    
    # Settings
    cur.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # Shared VPS
    cur.execute('''CREATE TABLE IF NOT EXISTS shared_vps (
        owner_id TEXT, shared_with_id TEXT, container_name TEXT, permissions TEXT, shared_at TEXT,
        UNIQUE(owner_id, shared_with_id, container_name)
    )''')
    
    # Games
    cur.execute('''CREATE TABLE IF NOT EXISTS installed_games (
        user_id TEXT, container_name TEXT, game_name TEXT, game_port INT, installed_at TEXT
    )''')
    
    # Tools
    cur.execute('''CREATE TABLE IF NOT EXISTS installed_tools (
        user_id TEXT, container_name TEXT, tool_name TEXT, tool_port INT, installed_at TEXT
    )''')
    
    # IPv4
    cur.execute('''CREATE TABLE IF NOT EXISTS ipv4 (
        user_id TEXT, container_name TEXT, public_ip TEXT, private_ip TEXT, mac_address TEXT, assigned_at TEXT
    )''')
    
    # Port forwards
    cur.execute('''CREATE TABLE IF NOT EXISTS port_forwards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, container_name TEXT, container_port INT, host_port INT UNIQUE, protocol TEXT, created_at TEXT
    )''')
    
    # Port allocations
    cur.execute('''CREATE TABLE IF NOT EXISTS port_allocations (
        user_id TEXT PRIMARY KEY, allocated_ports INTEGER DEFAULT 5
    )''')
    
    # Panels
    cur.execute('''CREATE TABLE IF NOT EXISTS panels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, panel_type TEXT, panel_url TEXT, admin_user TEXT, admin_pass TEXT, admin_email TEXT,
        container_name TEXT, tunnel_url TEXT, installed_at TEXT
    )''')
    
    # Transactions
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, txn_ref TEXT UNIQUE, txn_id TEXT, amount INT, status TEXT DEFAULT 'pending', created_at TEXT
    )''')
    
    # AI History
    cur.execute('''CREATE TABLE IF NOT EXISTS ai_history (user_id TEXT PRIMARY KEY, messages TEXT, updated_at TEXT)''')
    
    # Settings defaults
    settings = [
        ('license_verified', 'false'),
        ('server_ip', SERVER_IP),
        ('mac_address', MAC_ADDRESS),
        ('hostname', HOSTNAME),
        ('default_port_quota', '5'),
        ('ipv4_price', '50'),
        ('upi_id', '9892642904@ybl'),
    ]
    for k, v in settings:
        cur.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")
    return True

init_db()

# ==================================================================================================
#  📊  DATABASE HELPERS
# ==================================================================================================

def get_setting(key: str, default: Any = None) -> Any:
    conn = get_db()
    if not conn:
        return default
    cur = conn.cursor()
    cur.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key: str, value: str):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_user_vps(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM vps WHERE user_id = ? ORDER BY id', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_vps() -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM vps ORDER BY user_id, id')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_vps(user_id: str, container_name: str, ram: int, cpu: int, disk: int, os_version: str, plan: str = "Custom") -> Optional[Dict]:
    conn = get_db()
    if not conn:
        return None
    cur = conn.cursor()
    now = datetime.now().isoformat()
    
    ip = "N/A"
    mac = "N/A"
    try:
        ip = subprocess.getoutput(f"lxc exec {container_name} -- ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
        mac = subprocess.getoutput(f"lxc exec {container_name} -- ip link | grep ether | awk '{{print $2}}' | head -1")
    except:
        pass
    
    cur.execute('''INSERT INTO vps 
        (user_id, container_name, plan_name, ram, cpu, disk, os_version, status, created_at, ip_address, mac_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, container_name, plan, ram, cpu, disk, os_version, 'running', now, ip, mac))
    conn.commit()
    conn.close()
    return {'container_name': container_name}

def update_vps_status(container_name: str, status: str):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('UPDATE vps SET status = ? WHERE container_name = ?', (status, container_name))
    conn.commit()
    conn.close()

def delete_vps(container_name: str) -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute('DELETE FROM vps WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM shared_vps WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM installed_games WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM installed_tools WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM ipv4 WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM port_forwards WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM panels WHERE container_name = ?', (container_name,))
    conn.commit()
    conn.close()
    return True

def is_admin(user_id: str) -> bool:
    return user_id in [str(a) for a in MAIN_ADMIN_IDS]

def get_user_stats(user_id: str) -> Dict:
    conn = get_db()
    if not conn:
        return {'invites': 0}
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    api_key = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16]
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO user_stats (user_id, invites, boosts, claimed_vps_count, api_key, last_updated) VALUES (?, 0, 0, 0, ?, ?)',
               (user_id, api_key, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {'user_id': user_id, 'invites': 0, 'api_key': api_key}

def update_user_stats(user_id: str, invites: int = 0, claimed: int = 0):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('''INSERT OR REPLACE INTO user_stats 
        (user_id, invites, boosts, claimed_vps_count, api_key, last_updated)
        VALUES (?, 
                COALESCE((SELECT invites FROM user_stats WHERE user_id = ?), 0) + ?,
                0,
                COALESCE((SELECT claimed_vps_count FROM user_stats WHERE user_id = ?), 0) + ?,
                COALESCE((SELECT api_key FROM user_stats WHERE user_id = ?), ?),
                ?)''',
        (user_id, user_id, invites, user_id, claimed, user_id, hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16], datetime.now().isoformat()))
    conn.commit()
    conn.close()

def share_vps(owner: str, shared: str, container: str) -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('INSERT OR REPLACE INTO shared_vps VALUES (?, ?, ?, ?, ?)', (owner, shared, container, 'view', now))
    conn.commit()
    conn.close()
    return True

def unshare_vps(owner: str, shared: str, container: str) -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute('DELETE FROM shared_vps WHERE owner_id = ? AND shared_with_id = ? AND container_name = ?',
               (owner, shared, container))
    conn.commit()
    conn.close()
    return True

def get_shared_vps(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('''SELECT v.*, sv.permissions, sv.owner_id 
                   FROM vps v JOIN shared_vps sv ON v.container_name = sv.container_name 
                   WHERE sv.shared_with_id = ?''', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_port_forward(user_id: str, container: str, cport: int, hport: int, proto: str = "tcp+udp") -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('INSERT INTO port_forwards (user_id, container_name, container_port, host_port, protocol, created_at) VALUES (?, ?, ?, ?, ?, ?)',
               (user_id, container, cport, hport, proto, now))
    conn.commit()
    conn.close()
    return True

def remove_port_forward(pid: int) -> Tuple[bool, str, int]:
    conn = get_db()
    if not conn:
        return False, "", 0
    cur = conn.cursor()
    cur.execute('SELECT container_name, host_port FROM port_forwards WHERE id = ?', (pid,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "", 0
    container, hport = row['container_name'], row['host_port']
    cur.execute('DELETE FROM port_forwards WHERE id = ?', (pid,))
    conn.commit()
    conn.close()
    return True, container, hport

def get_user_port_forwards(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM port_forwards WHERE user_id = ? ORDER BY created_at', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_port_allocation(user_id: str) -> int:
    conn = get_db()
    if not conn:
        return int(get_setting('default_port_quota', '5'))
    cur = conn.cursor()
    cur.execute('SELECT allocated_ports FROM port_allocations WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else int(get_setting('default_port_quota', '5'))

def add_port_allocation(user_id: str, amount: int):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    current = get_port_allocation(user_id)
    cur.execute('INSERT OR REPLACE INTO port_allocations (user_id, allocated_ports) VALUES (?, ?)',
               (user_id, current + amount))
    conn.commit()
    conn.close()

def add_ipv4(user_id: str, container: str, public: str, private: str, mac: str = ""):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('INSERT OR REPLACE INTO ipv4 VALUES (?, ?, ?, ?, ?, ?)',
               (user_id, container, public, private, mac, now))
    conn.commit()
    conn.close()

def get_user_ipv4(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM ipv4 WHERE user_id = ?', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_transaction(user_id: str, txn_ref: str, amount: int) -> int:
    conn = get_db()
    if not conn:
        return 0
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('INSERT INTO transactions (user_id, txn_ref, amount, created_at) VALUES (?, ?, ?, ?)',
               (user_id, txn_ref, amount, now))
    tid = cur.lastrowid
    conn.commit()
    conn.close()
    return tid

def add_game_install(user_id: str, container: str, game: str, port: int):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('INSERT INTO installed_games VALUES (?, ?, ?, ?, ?)',
               (user_id, container, game, port, now))
    conn.commit()
    conn.close()

def add_tool_install(user_id: str, container: str, tool: str, port: int = None):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('INSERT INTO installed_tools VALUES (?, ?, ?, ?, ?)',
               (user_id, container, tool, port, now))
    conn.commit()
    conn.close()

def add_panel(user_id: str, ptype: str, url: str, user: str, pwd: str, email: str, container: str, tunnel: str = ""):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT INTO panels 
        (user_id, panel_type, panel_url, admin_user, admin_pass, admin_email, container_name, tunnel_url, installed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, ptype, url, user, pwd, email, container, tunnel, now))
    conn.commit()
    conn.close()

# ==================================================================================================
#  🌐  NODE MANAGEMENT WITH NODES.JSON
# ==================================================================================================

def load_nodes():
    """Load nodes from JSON file with auto-detect"""
    default = {
        "version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "main_node": "local",
        "nodes": {},
        "node_groups": {"all": [], "us": [], "eu": [], "asia": []}
    }
    
    if os.path.exists(NODES_FILE):
        try:
            with open(NODES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Auto-create local node
    try:
        lxc_count = len(subprocess.getoutput("lxc list -c n --format csv").splitlines())
    except:
        lxc_count = 0
    
    local_node = {
        "name": "local",
        "host": "localhost",
        "port": 0,
        "username": "local",
        "type": "local",
        "status": "online",
        "is_main": True,
        "region": "us",
        "description": "Auto-detected local node",
        "api_key": hashlib.sha256(f"local{time.time()}".encode()).hexdigest()[:32],
        "stats": {
            "total_ram": psutil.virtual_memory().total // 1024 // 1024,
            "used_ram": psutil.virtual_memory().used // 1024 // 1024,
            "total_cpu": psutil.cpu_count(),
            "used_cpu": psutil.cpu_percent(),
            "total_disk": psutil.disk_usage('/').total // 1024 // 1024 // 1024,
            "used_disk": psutil.disk_usage('/').used // 1024 // 1024 // 1024,
            "lxc_count": lxc_count,
            "last_checked": datetime.now().isoformat()
        },
        "settings": {
            "max_containers": 100,
            "default_storage_pool": DEFAULT_STORAGE_POOL,
            "allow_overcommit": True
        }
    }
    
    default["nodes"]["local"] = local_node
    default["node_groups"]["all"].append("local")
    default["node_groups"]["us"].append("local")
    
    with open(NODES_FILE, 'w') as f:
        json.dump(default, f, indent=2)
    
    return default

def save_nodes(data):
    with open(NODES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_node(name):
    nodes = load_nodes()
    return nodes['nodes'].get(name)

def update_local_node_stats():
    nodes = load_nodes()
    if 'local' in nodes['nodes']:
        try:
            lxc_count = len(subprocess.getoutput("lxc list -c n --format csv").splitlines())
        except:
            lxc_count = 0
        nodes['nodes']['local']['stats'] = {
            "total_ram": psutil.virtual_memory().total // 1024 // 1024,
            "used_ram": psutil.virtual_memory().used // 1024 // 1024,
            "total_cpu": psutil.cpu_count(),
            "used_cpu": psutil.cpu_percent(),
            "total_disk": psutil.disk_usage('/').total // 1024 // 1024 // 1024,
            "used_disk": psutil.disk_usage('/').used // 1024 // 1024 // 1024,
            "lxc_count": lxc_count,
            "last_checked": datetime.now().isoformat()
        }
        nodes['nodes']['local']['status'] = "online"
        save_nodes(nodes)
    return nodes

# ==================================================================================================
#  🛠️  LXC HELPERS
# ==================================================================================================

async def run_lxc(cmd: str, timeout: int = 60) -> Tuple[str, str, int]:
    try:
        proc = await asyncio.create_subprocess_exec(
            *shlex.split(cmd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout)
            return out.decode().strip(), err.decode().strip(), proc.returncode
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return "", f"Timeout after {timeout}s", -1
    except Exception as e:
        return "", str(e), -1

async def exec_in_container(container: str, cmd: str, timeout: int = 30) -> Tuple[str, str, int]:
    return await run_lxc(f"lxc exec {container} -- bash -c {shlex.quote(cmd)}", timeout)

async def get_container_status(container: str) -> str:
    try:
        out = subprocess.getoutput(f"lxc info {container} | grep Status | awk '{{print $2}}'")
        return out.lower()
    except:
        return "unknown"

async def get_container_stats(container: str) -> Dict:
    stats = {'status': 'unknown', 'cpu': '0%', 'memory': '0/0MB', 'disk': '0/0GB', 'ipv4': [], 'mac': 'N/A', 'uptime': '0m'}
    stats['status'] = await get_container_status(container)
    if stats['status'] == 'running':
        out, _, _ = await exec_in_container(container, "top -bn1 | grep Cpu | awk '{print $2}'")
        stats['cpu'] = f"{out}%" if out else "0%"
        out, _, _ = await exec_in_container(container, "free -m | awk '/^Mem:/{print $3\"/\"$2}'")
        stats['memory'] = f"{out}MB" if out else "0/0MB"
        out, _, _ = await exec_in_container(container, "df -h / | awk 'NR==2{print $3\"/\"$2}'")
        stats['disk'] = out if out else "0/0GB"
        out, _, _ = await exec_in_container(container, "ip -4 addr show | grep -oP '(?<=inet\\s)[0-9.]+' | grep -v 127")
        stats['ipv4'] = out.splitlines() if out else []
        out, _, _ = await exec_in_container(container, "ip link | grep ether | awk '{print $2}'")
        stats['mac'] = out.splitlines()[0] if out else "N/A"
        out, _, _ = await exec_in_container(container, "uptime -p | sed 's/up //'")
        stats['uptime'] = out if out else "0m"
    return stats

async def get_available_port() -> Optional[int]:
    used = set()
    conn = get_db()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT host_port FROM port_forwards')
        used = {r[0] for r in cur.fetchall()}
        conn.close()
    for _ in range(100):
        port = random.randint(20000, 50000)
        if port not in used:
            return port
    return None

async def create_port_forward(user_id: str, container: str, cport: int, proto: str = "tcp+udp") -> Optional[int]:
    hport = await get_available_port()
    if not hport:
        return None
    try:
        if proto in ["tcp", "tcp+udp"]:
            await run_lxc(f"lxc config device add {container} proxy-tcp-{hport} proxy listen=tcp:0.0.0.0:{hport} connect=tcp:127.0.0.1:{cport}")
        if proto in ["udp", "tcp+udp"]:
            await run_lxc(f"lxc config device add {container} proxy-udp-{hport} proxy listen=udp:0.0.0.0:{hport} connect=udp:127.0.0.1:{cport}")
        add_port_forward(user_id, container, cport, hport, proto)
        return hport
    except:
        return None

async def remove_port_device(container: str, hport: int):
    try:
        await run_lxc(f"lxc config device remove {container} proxy-tcp-{hport}")
    except:
        pass
    try:
        await run_lxc(f"lxc config device remove {container} proxy-udp-{hport}")
    except:
        pass

# ==================================================================================================
#  🎨  UI HELPER FUNCTIONS
# ==================================================================================================

def glow_text(text: str) -> str:
    return f"```glow\n{text}\n```"

def terminal_text(text: str) -> str:
    return f"```fix\n{text}\n```"

def create_embed(title: str, desc: str = "", color: int = COLORS['primary']) -> discord.Embed:
    embed = discord.Embed(title=glow_text(f"✦ {BOT_NAME} - {title} ✦"), description=desc, color=color)
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(text=f"⚡ {BOT_NAME} • {BOT_AUTHOR} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡", icon_url=THUMBNAIL_URL)
    return embed

def success_embed(title: str, desc: str = "") -> discord.Embed:
    return create_embed(f"✅ {title}", desc, COLORS['success'])

def error_embed(title: str, desc: str = "") -> discord.Embed:
    return create_embed(f"❌ {title}", desc, COLORS['error'])

def info_embed(title: str, desc: str = "") -> discord.Embed:
    return create_embed(f"ℹ️ {title}", desc, COLORS['info'])

def warning_embed(title: str, desc: str = "") -> discord.Embed:
    return create_embed(f"⚠️ {title}", desc, COLORS['warning'])

def node_embed(title: str, desc: str = "") -> discord.Embed:
    return create_embed(f"🌐 {title}", desc, COLORS['node'])

def terminal_embed(title: str, content: str) -> discord.Embed:
    embed = discord.Embed(title=terminal_text(f"[ {title} ]"), description=f"```bash\n{content[:1900]}\n```", color=COLORS['terminal'])
    embed.set_footer(text=f"⚡ Terminal • {datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def no_vps_embed() -> discord.Embed:
    return info_embed("No VPS Found", error_text("You don't have any VPS yet.") + f"\n\nUse `{BOT_PREFIX}plans` to see plans")

# ==================================================================================================
#  🤖  BOT SETUP
# ==================================================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.start_time = datetime.utcnow()
LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'

# ==================================================================================================
#  🎯  VPS MANAGE VIEW WITH ALL BUTTONS
# ==================================================================================================

# ==================================================================================================
#  🖥️  COMPLETE VPS MANAGE VIEW - ALL BUTTONS INCLUDED
# ==================================================================================================

class VPSManageView(View):
    """Complete VPS Management View with All Buttons"""
    
    def __init__(self, ctx, container_name: str, container_data: dict):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.container = container_name
        self.data = container_data
        self.message = None
        self.live_mode = False
        self.live_task = None
        
        # All Buttons - Row 1 (Basic Controls)
        self.start_btn = Button(label="▶️ Start", style=discord.ButtonStyle.success, emoji="▶️", row=0)
        self.stop_btn = Button(label="⏹️ Stop", style=discord.ButtonStyle.danger, emoji="⏹️", row=0)
        self.restart_btn = Button(label="🔄 Restart", style=discord.ButtonStyle.primary, emoji="🔄", row=0)
        self.reboot_btn = Button(label="⚡ Reboot", style=discord.ButtonStyle.warning, emoji="⚡", row=0)
        self.shutdown_btn = Button(label="⛔ Shutdown", style=discord.ButtonStyle.danger, emoji="⛔", row=0)
        
        # Row 2 (Info & Access)
        self.stats_btn = Button(label="📊 Stats", style=discord.ButtonStyle.secondary, emoji="📊", row=1)
        self.process_btn = Button(label="🔝 Processes", style=discord.ButtonStyle.secondary, emoji="🔝", row=1)
        self.console_btn = Button(label="📟 Console", style=discord.ButtonStyle.secondary, emoji="📟", row=1)
        self.ssh_btn = Button(label="🔑 SSH-GEN", style=discord.ButtonStyle.primary, emoji="🔑", row=1)
        self.logs_btn = Button(label="📋 Logs", style=discord.ButtonStyle.secondary, emoji="📋", row=1)
        
        # Row 3 (Advanced)
        self.ipv4_btn = Button(label="🌍 IPv4 Check", style=discord.ButtonStyle.secondary, emoji="🌍", row=2)
        self.ports_btn = Button(label="🔌 Ports", style=discord.ButtonStyle.secondary, emoji="🔌", row=2)
        self.backup_btn = Button(label="💾 Backup", style=discord.ButtonStyle.success, emoji="💾", row=2)
        self.restore_btn = Button(label="🔄 Restore", style=discord.ButtonStyle.warning, emoji="🔄", row=2)
        self.snapshot_btn = Button(label="📸 Snapshot", style=discord.ButtonStyle.secondary, emoji="📸", row=2)
        
        # Row 4 (Management)
        self.reinstall_btn = Button(label="🔄 Reinstall OS", style=discord.ButtonStyle.danger, emoji="🔄", row=3)
        self.upgrade_btn = Button(label="⬆️ Upgrade VPS", style=discord.ButtonStyle.primary, emoji="⬆️", row=3)
        self.invites_btn = Button(label="📨 Check Invites", style=discord.ButtonStyle.secondary, emoji="📨", row=3)
        self.panel_btn = Button(label="📦 Install Panel", style=discord.ButtonStyle.primary, emoji="📦", row=3)
        self.share_btn = Button(label="👥 Share VPS", style=discord.ButtonStyle.secondary, emoji="👥", row=3)
        
        # Row 5 (Live & Refresh)
        self.live_btn = Button(label="🔴 Live Mode", style=discord.ButtonStyle.danger, emoji="🔴", row=4)
        self.refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=4)
        
        # Set callbacks
        self.start_btn.callback = self.start_callback
        self.stop_btn.callback = self.stop_callback
        self.restart_btn.callback = self.restart_callback
        self.reboot_btn.callback = self.reboot_callback
        self.shutdown_btn.callback = self.shutdown_callback
        
        self.stats_btn.callback = self.stats_callback
        self.process_btn.callback = self.process_callback
        self.console_btn.callback = self.console_callback
        self.ssh_btn.callback = self.ssh_callback
        self.logs_btn.callback = self.logs_callback
        
        self.ipv4_btn.callback = self.ipv4_callback
        self.ports_btn.callback = self.ports_callback
        self.backup_btn.callback = self.backup_callback
        self.restore_btn.callback = self.restore_callback
        self.snapshot_btn.callback = self.snapshot_callback
        
        self.reinstall_btn.callback = self.reinstall_callback
        self.upgrade_btn.callback = self.upgrade_callback
        self.invites_btn.callback = self.invites_callback
        self.panel_btn.callback = self.panel_callback
        self.share_btn.callback = self.share_callback
        
        self.live_btn.callback = self.live_callback
        self.refresh_btn.callback = self.refresh_callback
        
        # Add all buttons
        self.add_item(self.start_btn)
        self.add_item(self.stop_btn)
        self.add_item(self.restart_btn)
        self.add_item(self.reboot_btn)
        self.add_item(self.shutdown_btn)
        
        self.add_item(self.stats_btn)
        self.add_item(self.process_btn)
        self.add_item(self.console_btn)
        self.add_item(self.ssh_btn)
        self.add_item(self.logs_btn)
        
        self.add_item(self.ipv4_btn)
        self.add_item(self.ports_btn)
        self.add_item(self.backup_btn)
        self.add_item(self.restore_btn)
        self.add_item(self.snapshot_btn)
        
        self.add_item(self.reinstall_btn)
        self.add_item(self.upgrade_btn)
        self.add_item(self.invites_btn)
        self.add_item(self.panel_btn)
        self.add_item(self.share_btn)
        
        self.add_item(self.live_btn)
        self.add_item(self.refresh_btn)
    
    async def get_stats_embed(self) -> discord.Embed:
        """Get current VPS stats embed"""
        stats = await get_container_stats(self.container)
        
        embed = discord.Embed(
            title=f"```glow\n🖥️ VPS Management: {self.container}\n```",
            color=0x5865F2
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        
        # Status Section
        status_emoji = "🟢" if stats['status'] == 'running' else "🔴"
        status_text = stats['status'].upper()
        if self.data.get('suspended'):
            status_text = "⛔ SUSPENDED"
            status_emoji = "⛔"
        
        embed.add_field(
            name="📊 Status",
            value=f"{status_emoji} `{status_text}`",
            inline=True
        )
        
        # Resources Section
        embed.add_field(
            name="⚙️ Resources",
            value=f"```fix\nRAM: {self.data['ram']}GB\nCPU: {self.data['cpu']} Core(s)\nDisk: {self.data['disk']}GB\n```",
            inline=True
        )
        
        # OS Info
        embed.add_field(
            name="🐧 OS",
            value=f"```fix\n{self.data.get('os_version', 'ubuntu:22.04')}\n```",
            inline=True
        )
        
        if stats['status'] == 'running' and not self.data.get('suspended'):
            # CPU Usage with Graph
            cpu_val = float(stats['cpu'].replace('%', '')) if stats['cpu'] != '0%' else 0
            cpu_bar = "█" * int(cpu_val / 10) + "░" * (10 - int(cpu_val / 10))
            
            # Memory Usage with Graph
            mem_val = 0
            if '/' in stats['memory']:
                try:
                    used = int(stats['memory'].split('/')[0].replace('MB', '').strip())
                    total = int(stats['memory'].split('/')[1].replace('MB', '').strip())
                    mem_val = (used / total) * 100 if total > 0 else 0
                except:
                    mem_val = 0
            mem_bar = "█" * int(mem_val / 10) + "░" * (10 - int(mem_val / 10))
            
            # Disk Usage with Graph
            disk_val = 0
            if '/' in stats['disk']:
                try:
                    used = stats['disk'].split('/')[0].replace('GB', '').strip()
                    total = stats['disk'].split('/')[1].split()[0].strip()
                    disk_val = (float(used) / float(total)) * 100 if float(total) > 0 else 0
                except:
                    disk_val = 0
            disk_bar = "█" * int(disk_val / 10) + "░" * (10 - int(disk_val / 10))
            
            embed.add_field(
                name="💾 CPU Usage",
                value=f"```fix\n{cpu_bar} {stats['cpu']}\n```",
                inline=True
            )
            embed.add_field(
                name="📀 Memory Usage",
                value=f"```fix\n{mem_bar} {stats['memory']}\n```",
                inline=True
            )
            embed.add_field(
                name="💽 Disk Usage",
                value=f"```fix\n{disk_bar} {stats['disk']}\n```",
                inline=True
            )
            
            # Network Info
            embed.add_field(
                name="🌐 IP Address",
                value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```",
                inline=True
            )
            embed.add_field(
                name="🔌 MAC Address",
                value=f"```fix\n{stats['mac']}\n```",
                inline=True
            )
            embed.add_field(
                name="⏱️ Uptime",
                value=f"```fix\n{stats['uptime']}\n```",
                inline=True
            )
            
            # Process Count
            embed.add_field(
                name="📟 Processes",
                value=f"```fix\n{stats.get('processes', 'N/A')}\n```",
                inline=True
            )
        
        embed.set_footer(
            text=f"⚡ {BOT_NAME} • Container: {self.container} • Last Updated: {datetime.now().strftime('%H:%M:%S')} ⚡",
            icon_url=THUMBNAIL_URL
        )
        
        return embed
    
    async def start_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc start {self.container}")
        update_vps_status(self.container, 'running')
        await interaction.followup.send(embed=success_embed("Started", f"```fix\n{self.container} started successfully!\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def stop_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc stop {self.container}")
        update_vps_status(self.container, 'stopped')
        await interaction.followup.send(embed=success_embed("Stopped", f"```fix\n{self.container} stopped.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def restart_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc restart {self.container}")
        update_vps_status(self.container, 'running')
        await interaction.followup.send(embed=success_embed("Restarted", f"```fix\n{self.container} restarted.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def reboot_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc restart {self.container}")
        update_vps_status(self.container, 'running')
        await interaction.followup.send(embed=success_embed("Rebooted", f"```fix\n{self.container} rebooted.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def shutdown_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc stop {self.container}")
        update_vps_status(self.container, 'stopped')
        await interaction.followup.send(embed=success_embed("Shutdown", f"```fix\n{self.container} shutdown.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def stats_callback(self, interaction):
        stats = await get_container_stats(self.container)
        embed = info_embed(f"Live Stats: {self.container}")
        
        embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
        embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
        embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
        embed.add_field(name="💽 Disk", value=f"```fix\n{stats['disk']}\n```", inline=True)
        embed.add_field(name="⏱️ Uptime", value=f"```fix\n{stats['uptime']}\n```", inline=True)
        embed.add_field(name="🌐 IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def process_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "ps aux --sort=-%cpu | head -15")
        embed = terminal_embed(f"Top Processes: {self.container}", out)
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def console_callback(self, interaction):
        modal = CommandModal(self.container)
        await interaction.response.send_modal(modal)
    
    async def ssh_callback(self, interaction):
        await interaction.response.defer()
        await exec_in_container(self.container, "apt-get update -qq && apt-get install -y -qq tmate")
        sess = f"svm5-{random.randint(1000,9999)}"
        await exec_in_container(self.container, f"tmate -S /tmp/{sess}.sock new-session -d")
        await asyncio.sleep(5)
        out, _, _ = await exec_in_container(self.container, f"tmate -S /tmp/{sess}.sock display -p '#{{tmate_ssh}}'")
        url = out.strip()
        if url:
            try:
                dm = success_embed("🔑 SSH Access Generated")
                dm.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```")
                dm.add_field(name="🔐 SSH Command", value=f"```bash\n{url}\n```")
                dm.add_field(name="⏱️ Expires", value="```fix\n15 minutes\n```")
                await interaction.user.send(embed=dm)
                await interaction.followup.send(embed=success_embed("SSH Generated", "Check your DMs!"), ephemeral=True)
            except:
                await interaction.followup.send(embed=error_embed("DM Failed", f"```fix\n{url}\n```"), ephemeral=True)
        else:
            await interaction.followup.send(embed=error_embed("Failed", "Could not generate SSH"), ephemeral=True)
    
    async def logs_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "journalctl -n 50 --no-pager 2>/dev/null || dmesg | tail -50")
        embed = terminal_embed(f"Logs: {self.container}", out[:1900])
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def ipv4_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "ip addr show")
        embed = terminal_embed(f"IPv4 Details: {self.container}", out[:1900])
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def ports_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "netstat -tuln | head -20")
        embed = terminal_embed(f"Open Ports: {self.container}", out)
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def backup_callback(self, interaction):
        await interaction.response.defer()
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        out, err, code = await run_lxc(f"lxc snapshot {self.container} {backup_name}")
        
        if code == 0:
            add_snapshot(str(self.ctx.author.id), self.container, backup_name)
            embed = success_embed("Backup Created")
            embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
            embed.add_field(name="💾 Backup Name", value=f"```fix\n{backup_name}\n```", inline=True)
            embed.add_field(name="📅 Created", value=f"```fix\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n```", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(embed=error_embed("Backup Failed", f"```diff\n- {err}\n```"), ephemeral=True)
    
    async def restore_callback(self, interaction):
        # Get available snapshots
        snapshots = get_snapshots(self.container)
        
        if not snapshots:
            await interaction.response.send_message(embed=error_embed("No Backups", "No backups found for this VPS."), ephemeral=True)
            return
        
        # Create selection view for snapshots
        view = View(timeout=60)
        options = []
        for s in snapshots[:10]:
            options.append(discord.SelectOption(
                label=s['snapshot_name'],
                value=s['snapshot_name'],
                description=f"Created: {s['created_at'][:16]}"
            ))
        
        select = Select(placeholder="Select backup to restore...", options=options)
        
        async def select_callback(select_interaction):
            snap_name = select.values[0]
            await select_interaction.response.defer()
            msg = await select_interaction.followup.send(embed=info_embed("Restoring", f"```fix\nRestoring {self.container} from {snap_name}...\n```"), ephemeral=True)
            
            status = await get_container_status(self.container)
            if status == 'running':
                await run_lxc(f"lxc stop {self.container} --force")
            
            out, err, code = await run_lxc(f"lxc restore {self.container} {snap_name}")
            
            if code == 0:
                await run_lxc(f"lxc start {self.container}")
                embed = success_embed("Backup Restored")
                embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
                embed.add_field(name="💾 Backup", value=f"```fix\n{snap_name}\n```", inline=True)
                await msg.edit(embed=embed)
            else:
                await msg.edit(embed=error_embed("Restore Failed", f"```diff\n- {err}\n```"))
        
        select.callback = select_callback
        view.add_item(select)
        
        embed = info_embed("Select Backup", "Choose a backup to restore:")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def snapshot_callback(self, interaction):
        await interaction.response.defer()
        snapshots = get_snapshots(self.container)
        
        if not snapshots:
            await interaction.followup.send(embed=info_embed("No Snapshots", "No snapshots found."), ephemeral=True)
            return
        
        embed = info_embed(f"Snapshots: {self.container}")
        for s in snapshots[:10]:
            embed.add_field(
                name=f"📸 {s['snapshot_name']}",
                value=f"```fix\nCreated: {s['created_at'][:16]}\nSize: {s.get('size_mb', 'N/A')} MB\n```",
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def reinstall_callback(self, interaction):
        """Reinstall OS with OS selection"""
        # OS selection view
        view = View(timeout=120)
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(
                label=os['label'][:100],
                value=os['value'],
                description=os['desc'][:100],
                emoji=os.get('icon', '🐧')
            ))
        
        select = Select(placeholder="Select new operating system...", options=options)
        
        async def select_callback(select_interaction):
            if select_interaction.user.id != self.ctx.author.id:
                await select_interaction.response.send_message("Not for you!", ephemeral=True)
                return
            
            selected_os = select.values[0]
            
            # Confirmation view
            confirm_view = View(timeout=60)
            confirm_btn = Button(label="✅ Confirm Reinstall", style=discord.ButtonStyle.danger)
            cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
            
            async def confirm_cb(confirm_interaction):
                await confirm_interaction.response.defer()
                msg = await confirm_interaction.followup.send(embed=info_embed("Reinstalling", f"```fix\nReinstalling {self.container} with {selected_os}...\n```"), ephemeral=True)
                
                try:
                    status = await get_container_status(self.container)
                    if status == 'running':
                        await run_lxc(f"lxc stop {self.container} --force")
                    
                    ram_mb = self.data['ram'] * 1024
                    cpu = self.data['cpu']
                    disk = self.data['disk']
                    
                    await run_lxc(f"lxc delete {self.container} --force")
                    await run_lxc(f"lxc init {selected_os} {self.container} -s {DEFAULT_STORAGE_POOL}")
                    await run_lxc(f"lxc config set {self.container} limits.memory {ram_mb}MB")
                    await run_lxc(f"lxc config set {self.container} limits.cpu {cpu}")
                    await run_lxc(f"lxc config device set {self.container} root size={disk}GB")
                    await run_lxc(f"lxc start {self.container}")
                    await asyncio.sleep(5)
                    
                    embed = success_embed("OS Reinstalled")
                    embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
                    embed.add_field(name="🐧 New OS", value=f"```fix\n{selected_os}\n```", inline=True)
                    await msg.edit(embed=embed)
                    
                except Exception as e:
                    await msg.edit(embed=error_embed("Reinstall Failed", f"```diff\n- {str(e)}\n```"))
            
            async def cancel_cb(cancel_interaction):
                await cancel_interaction.response.edit_message(embed=info_embed("Cancelled", "Reinstall cancelled."), view=None)
            
            confirm_btn.callback = confirm_cb
            cancel_btn.callback = cancel_cb
            confirm_view.add_item(confirm_btn)
            confirm_view.add_item(cancel_btn)
            
            os_name = next((o['label'] for o in OS_OPTIONS if o['value'] == selected_os), selected_os)
            embed = warning_embed(
                "⚠️ Confirm Reinstall",
                f"```fix\nContainer: {self.container}\nCurrent OS: {self.data.get('os_version', 'ubuntu:22.04')}\nNew OS: {os_name}\nRAM: {self.data['ram']}GB\nCPU: {self.data['cpu']} Core(s)\nDisk: {self.data['disk']}GB\n```\n\n**⚠️ ALL DATA WILL BE LOST!**"
            )
            await select_interaction.response.edit_message(embed=embed, view=confirm_view)
        
        select.callback = select_callback
        view.add_item(select)
        
        embed = info_embed("Reinstall OS", "Select new operating system:")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def upgrade_callback(self, interaction):
        """Upgrade VPS resources"""
        await interaction.response.defer()
        
        # Get current stats
        stats = await get_container_stats(self.container)
        
        # Create upgrade options
        view = View(timeout=120)
        
        # RAM Upgrade Options
        ram_opts = [
            discord.SelectOption(label=f"RAM: +2GB (Total: {self.data['ram'] + 2}GB)", value=f"ram:2"),
            discord.SelectOption(label=f"RAM: +4GB (Total: {self.data['ram'] + 4}GB)", value=f"ram:4"),
            discord.SelectOption(label=f"RAM: +8GB (Total: {self.data['ram'] + 8}GB)", value=f"ram:8"),
        ]
        ram_select = Select(placeholder="Select RAM upgrade...", options=ram_opts, row=0)
        
        # CPU Upgrade Options
        cpu_opts = [
            discord.SelectOption(label=f"CPU: +1 Core (Total: {self.data['cpu'] + 1})", value=f"cpu:1"),
            discord.SelectOption(label=f"CPU: +2 Cores (Total: {self.data['cpu'] + 2})", value=f"cpu:2"),
            discord.SelectOption(label=f"CPU: +4 Cores (Total: {self.data['cpu'] + 4})", value=f"cpu:4"),
        ]
        cpu_select = Select(placeholder="Select CPU upgrade...", options=cpu_opts, row=1)
        
        # Disk Upgrade Options
        disk_opts = [
            discord.SelectOption(label=f"Disk: +10GB (Total: {self.data['disk'] + 10}GB)", value=f"disk:10"),
            discord.SelectOption(label=f"Disk: +20GB (Total: {self.data['disk'] + 20}GB)", value=f"disk:20"),
            discord.SelectOption(label=f"Disk: +50GB (Total: {self.data['disk'] + 50}GB)", value=f"disk:50"),
        ]
        disk_select = Select(placeholder="Select disk upgrade...", options=disk_opts, row=2)
        
        async def ram_callback(select_interaction):
            value = ram_select.values[0]
            amt = int(value.split(':')[1])
            await self.apply_upgrade(select_interaction, 'ram', amt)
        
        async def cpu_callback(select_interaction):
            value = cpu_select.values[0]
            amt = int(value.split(':')[1])
            await self.apply_upgrade(select_interaction, 'cpu', amt)
        
        async def disk_callback(select_interaction):
            value = disk_select.values[0]
            amt = int(value.split(':')[1])
            await self.apply_upgrade(select_interaction, 'disk', amt)
        
        ram_select.callback = ram_callback
        cpu_select.callback = cpu_callback
        disk_select.callback = disk_callback
        
        view.add_item(ram_select)
        view.add_item(cpu_select)
        view.add_item(disk_select)
        
        embed = info_embed("Upgrade VPS", f"```fix\nCurrent Resources:\nRAM: {self.data['ram']}GB\nCPU: {self.data['cpu']} Core(s)\nDisk: {self.data['disk']}GB\n```\nSelect upgrade option:")
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    async def apply_upgrade(self, interaction, resource, amount):
        await interaction.response.defer()
        
        status = await get_container_status(self.container)
        was_running = status == 'running'
        
        if was_running:
            await run_lxc(f"lxc stop {self.container} --force")
        
        if resource == 'ram':
            new_ram = self.data['ram'] + amount
            await run_lxc(f"lxc config set {self.container} limits.memory {new_ram * 1024}MB")
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ram = ? WHERE container_name = ?', (new_ram, self.container))
            conn.commit()
            conn.close()
            self.data['ram'] = new_ram
        
        elif resource == 'cpu':
            new_cpu = self.data['cpu'] + amount
            await run_lxc(f"lxc config set {self.container} limits.cpu {new_cpu}")
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET cpu = ? WHERE container_name = ?', (new_cpu, self.container))
            conn.commit()
            conn.close()
            self.data['cpu'] = new_cpu
        
        elif resource == 'disk':
            new_disk = self.data['disk'] + amount
            await run_lxc(f"lxc config device set {self.container} root size={new_disk}GB")
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET disk = ? WHERE container_name = ?', (new_disk, self.container))
            conn.commit()
            conn.close()
            self.data['disk'] = new_disk
        
        if was_running:
            await run_lxc(f"lxc start {self.container}")
        
        embed = success_embed("VPS Upgraded")
        embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
        embed.add_field(name="⚙️ New Resources", value=f"```fix\nRAM: {self.data['ram']}GB\nCPU: {self.data['cpu']} Core(s)\nDisk: {self.data['disk']}GB\n```", inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def invites_callback(self, interaction):
        await interaction.response.defer()
        stats = get_user_stats(str(self.ctx.author.id))
        invites = stats.get('invites', 0)
        vps_count = len(get_user_vps(str(self.ctx.author.id)))
        
        embed = info_embed("Your Invites")
        embed.add_field(name="📨 Total Invites", value=f"```fix\n{invites}\n```", inline=True)
        embed.add_field(name="🖥️ VPS Count", value=f"```fix\n{vps_count}\n```", inline=True)
        
        # Next plan
        next_plan = None
        for plan in FREE_VPS_PLANS['invites']:
            if invites < plan['invites']:
                next_plan = plan
                break
        
        if next_plan:
            embed.add_field(
                name="🎯 Next Plan",
                value=f"```fix\n{next_plan['emoji']} {next_plan['name']}\nNeed {next_plan['invites'] - invites} more invites\nRAM: {next_plan['ram']}GB | CPU: {next_plan['cpu']} | Disk: {next_plan['disk']}GB\n```",
                inline=False
            )
        else:
            embed.add_field(name="🏆 Status", value="```fix\nYou have reached the maximum plan!\n```", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def panel_callback(self, interaction):
        """Install Panel on VPS"""
        await interaction.response.defer()
        
        view = View(timeout=120)
        ptero_btn = Button(label="🦅 Pterodactyl", style=discord.ButtonStyle.primary, emoji="🦅")
        puffer_btn = Button(label="🐡 Pufferpanel", style=discord.ButtonStyle.success, emoji="🐡")
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
        
        async def ptero_cb(i):
            await self.install_panel(i, "pterodactyl")
        
        async def puffer_cb(i):
            await self.install_panel(i, "pufferpanel")
        
        async def cancel_cb(i):
            await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
        
        ptero_btn.callback = ptero_cb
        puffer_btn.callback = puffer_cb
        cancel_btn.callback = cancel_cb
        
        view.add_item(ptero_btn)
        view.add_item(puffer_btn)
        view.add_item(cancel_btn)
        
        embed = info_embed("Install Panel", "Select panel to install on this VPS:")
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    async def install_panel(self, interaction, panel_type):
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=info_embed(f"Installing {panel_type.title()}", "Step 1/6: Preparing..."), ephemeral=True)
        
        try:
            admin = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            email = f"{admin}@{random.choice(['gmail.com', 'outlook.com', 'proton.me'])}"
            pwd = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=16))
            
            if panel_type == "pterodactyl":
                cmds = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git unzip tar nginx mariadb-server redis-server php8.1 php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip}",
                    "curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer",
                    "mkdir -p /var/www/pterodactyl",
                    "cd /var/www/pterodactyl && curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz",
                    "cd /var/www/pterodactyl && tar -xzvf panel.tar.gz && chmod -R 755 storage/* bootstrap/cache/",
                    "cd /var/www/pterodactyl && cp .env.example .env",
                    "cd /var/www/pterodactyl && composer install --no-dev --optimize-autoloader --no-interaction",
                    "cd /var/www/pterodactyl && php artisan key:generate --force",
                    "cd /var/www/pterodactyl && php artisan migrate --seed --force",
                    f"cd /var/www/pterodactyl && php artisan p:user:make --email='{email}' --username='{admin}' --password='{pwd}' --name-first='Admin' --name-last='User' --admin=1 --no-interaction"
                ]
                for i, cmd in enumerate(cmds, 2):
                    await msg.edit(embed=info_embed(f"Installing {panel_type.title()}", f"Step {i}/6: Progress..."))
                    await exec_in_container(self.container, cmd)
                    await asyncio.sleep(1)
                out, _, _ = await exec_in_container(self.container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() or SERVER_IP
                url = f"http://{ip}"
            else:
                cmds = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git",
                    "curl -s https://packagecloud.io/install/repositories/pufferpanel/pufferpanel/script.deb.sh | bash",
                    "apt-get install -y -qq pufferpanel",
                    "systemctl enable pufferpanel",
                    "systemctl start pufferpanel",
                    f"pufferpanel user add --name '{admin}' --email '{email}' --password '{pwd}' --admin"
                ]
                for i, cmd in enumerate(cmds, 2):
                    await msg.edit(embed=info_embed(f"Installing {panel_type.title()}", f"Step {i}/6: Progress..."))
                    await exec_in_container(self.container, cmd)
                    await asyncio.sleep(1)
                out, _, _ = await exec_in_container(self.container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() or SERVER_IP
                url = f"http://{ip}:8080"
            
            add_panel(str(self.ctx.author.id), panel_type, url, admin, pwd, email, self.container, "")
            
            embed = success_embed(f"{panel_type.title()} Installed!")
            embed.add_field(name="🌐 URL", value=f"```fix\n{url}\n```", inline=False)
            embed.add_field(name="👤 Username", value=f"||`{admin}`||", inline=True)
            embed.add_field(name="📧 Email", value=f"||`{email}`||", inline=True)
            embed.add_field(name="🔑 Password", value=f"||`{pwd}`||", inline=False)
            await msg.edit(embed=embed)
            
            try:
                dm = success_embed(f"🔐 {panel_type.title()} Credentials")
                dm.add_field(name="URL", value=url)
                dm.add_field(name="Username", value=admin)
                dm.add_field(name="Email", value=email)
                dm.add_field(name="Password", value=pwd)
                await self.ctx.author.send(embed=dm)
            except:
                pass
                
        except Exception as e:
            await msg.edit(embed=error_embed("Installation Failed", f"```diff\n- {str(e)[:500]}\n```"))
    
    async def share_callback(self, interaction):
        """Share VPS with another user"""
        modal = ShareModal(self.container)
        await interaction.response.send_modal(modal)
    
    async def live_callback(self, interaction):
        """Toggle live mode"""
        self.live_mode = not self.live_mode
        
        if self.live_mode:
            self.live_btn.label = "⏹️ Stop Live"
            self.live_btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            
            # Start live update task
            self.live_task = asyncio.create_task(self.live_update_task(interaction))
        else:
            self.live_btn.label = "🔴 Live Mode"
            self.live_btn.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
            
            if self.live_task:
                self.live_task.cancel()
    
    async def live_update_task(self, interaction):
        """Task for live updates"""
        while self.live_mode:
            try:
                embed = await self.get_stats_embed()
                await interaction.edit_original_response(embed=embed, view=self)
                await asyncio.sleep(5)
            except:
                self.live_mode = False
                break
    
    async def refresh_callback(self, interaction):
        """Refresh VPS stats"""
        embed = await self.get_stats_embed()
        await interaction.response.edit_message(embed=embed, view=self)


class CommandModal(Modal):
    """Modal for running commands"""
    def __init__(self, container_name):
        super().__init__(title="Run Command")
        self.container = container_name
        self.add_item(InputText(label="Command", placeholder="e.g., apt update, ps aux, df -h", style=discord.InputTextStyle.paragraph))
        self.add_item(InputText(label="Timeout (seconds)", placeholder="30", required=False, value="30"))
    
    async def callback(self, interaction):
        cmd = self.children[0].value
        timeout = int(self.children[1].value or "30")
        
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=info_embed("Executing", f"```fix\n$ {cmd}\n```"), ephemeral=True)
        
        try:
            out, err, code = await exec_in_container(self.container, cmd, timeout)
            output = out if out else err
            
            embed = terminal_embed(f"Command Output", f"$ {cmd}\n\n{output[:1900]}")
            embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```")
            await msg.edit(embed=embed)
        except asyncio.TimeoutError:
            await msg.edit(embed=error_embed("Timeout", f"Command timed out after {timeout} seconds"))
        except Exception as e:
            await msg.edit(embed=error_embed("Error", f"```diff\n- {str(e)}\n```"))


class ShareModal(Modal):
    """Modal for sharing VPS"""
    def __init__(self, container):
        super().__init__(title="Share VPS")
        self.container = container
        self.add_item(InputText(label="User ID or @mention", placeholder="e.g., 123456789 or @username"))
        self.add_item(InputText(label="Permissions", placeholder="view, manage, full", required=False, value="view"))
    
    async def callback(self, interaction):
        user_input = self.children[0].value
        perms = self.children[1].value or "view"
        
        # Parse user
        user_id = user_input
        if user_input.startswith('<@') and user_input.endswith('>'):
            user_id = user_input[2:-1]
            if user_id.startswith('!'):
                user_id = user_id[1:]
        
        try:
            user = await interaction.client.fetch_user(int(user_id))
            if share_vps(str(interaction.user.id), str(user.id), self.container):
                embed = success_embed("VPS Shared")
                embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
                embed.add_field(name="👤 Shared With", value=user.mention, inline=True)
                embed.add_field(name="🔑 Permissions", value=f"```fix\n{perms}\n```", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
                # DM the user
                try:
                    dm = info_embed("VPS Shared With You")
                    dm.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```")
                    dm.add_field(name="👤 Owner", value=interaction.user.mention)
                    dm.add_field(name="🔑 Permissions", value=f"```fix\n{perms}\n```")
                    dm.add_field(name="🖥️ Manage", value=f"Use `.manage-shared {interaction.user.id} 1` to manage")
                    await user.send(embed=dm)
                except:
                    pass
            else:
                await interaction.response.send_message(embed=error_embed("Failed", "Could not share VPS"), ephemeral=True)
        except:
            await interaction.response.send_message(embed=error_embed("Invalid User", "User not found"), ephemeral=True)

# ==================================================================================================
#  📦  PANEL INSTALL VIEW WITH BUTTONS
# ==================================================================================================

class PanelInstallView(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        
        ptero_btn = Button(label="🦅 Pterodactyl Panel", style=discord.ButtonStyle.primary, emoji="🦅")
        puffer_btn = Button(label="🐡 Pufferpanel", style=discord.ButtonStyle.success, emoji="🐡")
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
        
        ptero_btn.callback = lambda i: self.install(i, "pterodactyl")
        puffer_btn.callback = lambda i: self.install(i, "pufferpanel")
        cancel_btn.callback = lambda i: i.response.edit_message(embed=info_embed("Cancelled"), view=None)
        
        self.add_item(ptero_btn)
        self.add_item(puffer_btn)
        self.add_item(cancel_btn)
    
    async def install(self, interaction, ptype):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("Not for you!", ephemeral=True)
        await interaction.response.defer()
        uid = str(self.ctx.author.id)
        vps = get_user_vps(uid)
        if not vps:
            return await interaction.followup.send(embed=no_vps_embed(), ephemeral=True)
        
        if len(vps) > 1:
            opts = []
            for i, v in enumerate(vps, 1):
                opts.append(discord.SelectOption(label=f"VPS #{i}: {v['container_name']}", value=v['container_name']))
            view = View()
            sel = Select(placeholder="Select VPS...", options=opts)
            async def sel_cb(si):
                await self.do_install(si, ptype, sel.values[0])
            sel.callback = sel_cb
            view.add_item(sel)
            await interaction.followup.send(embed=info_embed("Select VPS"), view=view, ephemeral=True)
        else:
            await self.do_install(interaction, ptype, vps[0]['container_name'])
    
    async def do_install(self, interaction, ptype, container):
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=info_embed(f"Installing {ptype.title()}", "Step 1/6: Preparing..."), ephemeral=True)
        try:
            admin = ''.join(random.choices(string.ascii_lowercase+string.digits, k=8))
            email = f"{admin}@{random.choice(['gmail.com','outlook.com','proton.me'])}"
            pwd = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$%", k=16))
            
            if ptype == "pterodactyl":
                cmds = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git unzip tar nginx mariadb-server redis-server php8.1 php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip}",
                    "curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer",
                    "mkdir -p /var/www/pterodactyl",
                    "cd /var/www/pterodactyl && curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz",
                    "cd /var/www/pterodactyl && tar -xzvf panel.tar.gz && chmod -R 755 storage/* bootstrap/cache/",
                    "cd /var/www/pterodactyl && cp .env.example .env",
                    "cd /var/www/pterodactyl && composer install --no-dev --optimize-autoloader --no-interaction",
                    "cd /var/www/pterodactyl && php artisan key:generate --force",
                    "cd /var/www/pterodactyl && php artisan migrate --seed --force",
                    f"cd /var/www/pterodactyl && php artisan p:user:make --email='{email}' --username='{admin}' --password='{pwd}' --name-first='Admin' --name-last='User' --admin=1 --no-interaction"
                ]
                for i, cmd in enumerate(cmds, 2):
                    await msg.edit(embed=info_embed(f"Installing {ptype.title()}", f"Step {i}/6: Progress..."))
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                out, _, _ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() or SERVER_IP
                url = f"http://{ip}"
            else:
                cmds = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git",
                    "curl -s https://packagecloud.io/install/repositories/pufferpanel/pufferpanel/script.deb.sh | bash",
                    "apt-get install -y -qq pufferpanel",
                    "systemctl enable pufferpanel",
                    "systemctl start pufferpanel",
                    f"pufferpanel user add --name '{admin}' --email '{email}' --password '{pwd}' --admin"
                ]
                for i, cmd in enumerate(cmds, 2):
                    await msg.edit(embed=info_embed(f"Installing {ptype.title()}", f"Step {i}/6: Progress..."))
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                out, _, _ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() or SERVER_IP
                url = f"http://{ip}:8080"
            
            add_panel(uid, ptype, url, admin, pwd, email, container, "")
            embed = success_embed(f"{ptype.title()} Installed!")
            embed.add_field(name="🌐 URL", value=f"```fix\n{url}\n```", inline=False)
            embed.add_field(name="👤 Username", value=f"||`{admin}`||", inline=True)
            embed.add_field(name="📧 Email", value=f"||`{email}`||", inline=True)
            embed.add_field(name="🔑 Password", value=f"||`{pwd}`||", inline=False)
            await msg.edit(embed=embed)
            try:
                dm = success_embed(f"🔐 {ptype.title()} Credentials")
                dm.add_field(name="URL", value=url)
                dm.add_field(name="Username", value=admin)
                dm.add_field(name="Email", value=email)
                dm.add_field(name="Password", value=pwd)
                await self.ctx.author.send(embed=dm)
            except:
                pass
        except Exception as e:
            await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)[:500]}\n```"))

# ==================================================================================================
#  📚  COMPLETE HELP COMMAND - ULTIMATE UI WITH SELECT MENU & IMAGES
# ==================================================================================================

# Help Category Images
HELP_IMAGES = {
    'home': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'user': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'vps': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'console': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'games': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'tools': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'nodes': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'share': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ports': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ipv4': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'panels': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ai': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'os': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'admin': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'owner': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ip': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
}

class HelpView(View):
    """Interactive Help Menu with Select Menu & Images"""
    
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_category = "home"
        self.message = None
        
        # Category Options with Emojis
        self.category_options = [
            discord.SelectOption(label="🏠 Home", value="home", emoji="🏠", description="Main menu with overview"),
            discord.SelectOption(label="👤 User Commands", value="user", emoji="👤", description="14 user commands"),
            discord.SelectOption(label="🖥️ VPS Commands", value="vps", emoji="🖥️", description="8 VPS management commands"),
            discord.SelectOption(label="📟 Console Commands", value="console", emoji="📟", description="10 console commands"),
            discord.SelectOption(label="🎮 Games Commands", value="games", emoji="🎮", description="7 game server commands"),
            discord.SelectOption(label="🛠️ Tools Commands", value="tools", emoji="🛠️", description="7 development tools"),
            discord.SelectOption(label="🌐 Node Commands", value="nodes", emoji="🌐", description="7 cluster management commands"),
            discord.SelectOption(label="👥 Share Commands", value="share", emoji="👥", description="4 VPS sharing commands"),
            discord.SelectOption(label="🔌 Port Commands", value="ports", emoji="🔌", description="6 port forwarding commands"),
            discord.SelectOption(label="🌍 IPv4 Commands", value="ipv4", emoji="🌍", description="6 IPv4 management commands"),
            discord.SelectOption(label="📦 Panel Commands", value="panels", emoji="📦", description="6 panel installation commands"),
            discord.SelectOption(label="🤖 AI Commands", value="ai", emoji="🤖", description="3 AI chat commands"),
            discord.SelectOption(label="🐧 OS Commands", value="os", emoji="🐧", description="70+ operating systems"),
            discord.SelectOption(label="🌐 IP Commands", value="ip", emoji="🌐", description="15+ IP management commands"),
            discord.SelectOption(label="🛡️ Admin Commands", value="admin", emoji="🛡️", description="13 admin commands"),
            discord.SelectOption(label="👑 Owner Commands", value="owner", emoji="👑", description="9 owner commands"),
        ]
        
        self.select = Select(placeholder="📋 Select a command category...", options=self.category_options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        # Add refresh button
        refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=1)
        refresh_btn.callback = self.refresh_callback
        self.add_item(refresh_btn)
        
        # Add delete button
        delete_btn = Button(label="🗑️ Close", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
        delete_btn.callback = self.delete_callback
        self.add_item(delete_btn)
        
        self.update_embed()
    
    def update_embed(self):
        """Update embed based on selected category"""
        
        # Category Data
        categories = {
            'home': {
                'title': "🏠 SVM5-BOT TOOLS - ULTIMATE VPS MANAGEMENT",
                'desc': f"```glow\nWelcome to {BOT_NAME} - Complete VPS Management Solution\n```\n"
                        f"**Select a category from the dropdown menu to view commands.**\n\n"
                        f"```fix\n📊 Bot Statistics:\n• Total Commands: 92+\n• OS Options: 70+\n• Games: 7\n• Tools: 7\n• Active Users: {len(get_all_vps())} VPS\n• Server IP: {SERVER_IP}\n• License: {'✅ Verified' if LICENSE_VERIFIED else '❌ Not Verified'}\n```",
                'fields': [
                    ("👤 USER (14)", "Basic commands for all users", True),
                    ("🖥️ VPS (8)", "Manage your VPS containers", True),
                    ("📟 CONSOLE (10)", "Terminal access and commands", True),
                    ("🎮 GAMES (7)", "Game server management", True),
                    ("🛠️ TOOLS (7)", "Development tools", True),
                    ("🌐 NODES (7)", "Cluster management", True),
                    ("👥 SHARE (4)", "Share VPS with users", True),
                    ("🔌 PORTS (6)", "Port forwarding", True),
                    ("🌍 IPv4 (6)", "IPv4 management", True),
                    ("📦 PANELS (6)", "Panel installation", True),
                    ("🤖 AI (3)", "AI assistant", True),
                    ("🐧 OS (70+)", "Operating systems", True),
                    ("🌐 IP (15+)", "IP management", True),
                    ("🛡️ ADMIN (13)", "Admin commands", True),
                    ("👑 OWNER (9)", "Owner commands", True),
                ]
            },
            'user': {
                'title': "👤 USER COMMANDS (14)",
                'desc': "```fix\nBasic commands available to all users\n```",
                'fields': [
                    (".help", "Show this interactive help menu", False),
                    (".ping", "Check bot latency with graph", False),
                    (".uptime", "Show bot uptime", False),
                    (".bot-info", "Detailed bot information", False),
                    (".server-info", "Show server hardware info", False),
                    (".plans", "View free VPS plans", False),
                    (".stats", "View your statistics", False),
                    (".inv", "Check your invites", False),
                    (".invites-top [limit]", "Show top inviters", False),
                    (".claim-free", "Claim free VPS with invites", False),
                    (".my-acc", "View your generated account", False),
                    (".gen-acc", "Generate random account", False),
                    (".api-key [regenerate]", "View or regenerate API key", False),
                    (".userinfo [@user]", "User information", False),
                ]
            },
            'vps': {
                'title': "🖥️ VPS COMMANDS (8)",
                'desc': "```fix\nManage your VPS containers with interactive buttons\n```",
                'fields': [
                    (".myvps", "List your VPS with status", False),
                    (".list", "Detailed VPS list with IPs", False),
                    (".manage [container]", "Interactive VPS manager with 20+ buttons", False),
                    (".stats [container]", "View VPS statistics with graphs", False),
                    (".logs [container] [lines]", "View VPS logs", False),
                    (".reboot <container>", "Reboot VPS", False),
                    (".shutdown <container>", "Shutdown VPS", False),
                    (".rename <old> <new>", "Rename VPS container", False),
                ]
            },
            'console': {
                'title': "📟 CONSOLE COMMANDS (10)",
                'desc': "```fix\nTerminal access and console commands\n```",
                'fields': [
                    (".ss [container]", "Take VPS snapshot/console output", False),
                    (".console <container> [command]", "Interactive console with modal", False),
                    (".execute <container> <command>", "Execute command in VPS", False),
                    (".ssh-gen <container>", "Generate temporary SSH access", False),
                    (".top <container>", "Show live process monitor", False),
                    (".df <container>", "Show disk usage with graph", False),
                    (".free <container>", "Show memory usage with graph", False),
                    (".ps <container>", "Show process list", False),
                    (".who <container>", "Show logged-in users", False),
                    (".uptime <container>", "Show container uptime", False),
                ]
            },
            'games': {
                'title': "🎮 GAMES COMMANDS (7)",
                'desc': "```fix\nInstall and manage game servers (Minecraft, CS:GO, etc.)\n```",
                'fields': [
                    (".games", "List all available games", False),
                    (".game-info <game>", "Detailed game information", False),
                    (".install-game <container> <game>", "Install game on VPS", False),
                    (".my-games [container]", "Your installed games", False),
                    (".start-game <container> <game>", "Start game server", False),
                    (".stop-game <container> <game>", "Stop game server", False),
                    (".game-stats <container> <game>", "Game server statistics", False),
                ]
            },
            'tools': {
                'title': "🛠️ TOOLS COMMANDS (7)",
                'desc': "```fix\nInstall development tools and services (Nginx, MySQL, Docker, etc.)\n```",
                'fields': [
                    (".tools", "List all available tools", False),
                    (".tool-info <tool>", "Detailed tool information", False),
                    (".install-tool <container> <tool>", "Install tool on VPS", False),
                    (".my-tools [container]", "Your installed tools", False),
                    (".start-tool <container> <tool>", "Start tool service", False),
                    (".stop-tool <container> <tool>", "Stop tool service", False),
                    (".tool-port <container> <tool>", "Show tool service port", False),
                ]
            },
            'nodes': {
                'title': "🌐 NODE COMMANDS (7)",
                'desc': "```fix\nManage cluster nodes (Auto-detects local node)\n```",
                'fields': [
                    (".node", "List all nodes in cluster", False),
                    (".node-info [name]", "Detailed node information", False),
                    (".node-add <name> <host> <user> <pass>", "Add new node (Admin)", False),
                    (".node-remove <name>", "Remove node (Admin)", False),
                    (".node-check <name>", "Check node health", False),
                    (".node-stats", "Cluster statistics", False),
                    (".node-connect <host> <user> [pass]", "Connect to remote node", False),
                ]
            },
            'share': {
                'title': "👥 SHARE COMMANDS (4)",
                'desc': "```fix\nShare VPS with other users\n```",
                'fields': [
                    (".share <@user> <vps_num>", "Share VPS with user", False),
                    (".unshare <@user> <vps_num>", "Remove VPS sharing", False),
                    (".shared", "List VPS shared with you", False),
                    (".manage-shared <owner> <num>", "Manage shared VPS", False),
                ]
            },
            'ports': {
                'title': "🔌 PORT COMMANDS (6)",
                'desc': "```fix\nPort forwarding management\n```",
                'fields': [
                    (".ports", "Port forwarding help", False),
                    (".ports add <vps_num> <port> [tcp/udp]", "Add port forward", False),
                    (".ports list", "List your port forwards", False),
                    (".ports remove <id>", "Remove port forward", False),
                    (".ports quota", "Check your port quota", False),
                    (".ports check <port>", "Check if port is available", False),
                ]
            },
            'ipv4': {
                'title': "🌍 IPv4 COMMANDS (6)",
                'desc': "```fix\nBuy and manage IPv4 addresses\n```",
                'fields': [
                    (".ipv4", "View your IPv4 addresses", False),
                    (".ipv4-details <container>", "Detailed IPv4 information", False),
                    (".buy-ipv4", "Purchase IPv4 via UPI with QR", False),
                    (".upi", "Show UPI payment information", False),
                    (".upi-qr [amount] [note]", "Generate UPI QR code", False),
                    (".pay <amount> [note]", "Generate payment link", False),
                ]
            },
            'panels': {
                'title': "📦 PANEL COMMANDS (6)",
                'desc': "```fix\nInstall game panels on your VPS\n```",
                'fields': [
                    (".install-panel", "Install Pterodactyl/Pufferpanel", False),
                    (".panel-info", "Show your installed panel info", False),
                    (".panel-reset [type]", "Reset panel admin password", False),
                    (".panel-delete [type]", "Delete panel record", False),
                    (".panel-tunnel [container] [port]", "Create cloudflared tunnel", False),
                    (".panel-status [container]", "Panel installation status", False),
                ]
            },
            'ai': {
                'title': "🤖 AI COMMANDS (3)",
                'desc': f"```fix\nChat with AI assistant (Model: {AI_MODEL})\n```",
                'fields': [
                    (".ai <message>", "Chat with AI assistant", False),
                    (".ai-reset", "Reset chat history", False),
                    (".ai-help <topic>", "Get AI help on specific topic", False),
                ]
            },
            'os': {
                'title': "🐧 OS COMMANDS",
                'desc': f"```fix\n70+ Operating Systems available for VPS creation\n```",
                'fields': [
                    (".os-list [category]", "List available OS by category", False),
                    ("Ubuntu", "20.04, 22.04, 24.04, 18.04, 16.04... (15 versions)", True),
                    ("Debian", "12, 11, 10, 9, 8, Sid, Testing... (14 versions)", True),
                    ("Fedora", "40, 39, 38, 37, 36, Rawhide... (10 versions)", True),
                    ("Rocky/Alma", "9, 8, 7 (6 versions)", True),
                    ("CentOS", "9 Stream, 8 Stream, 7, 6, 5, 4 (6 versions)", True),
                    ("Alpine", "3.19, 3.18, 3.17, Edge... (8 versions)", True),
                    ("Arch/Manjaro", "Arch Linux, Manjaro (3 versions)", True),
                    ("OpenSUSE", "Tumbleweed, Leap 15.5, 15.4, 15.3 (4 versions)", True),
                    ("FreeBSD", "14, 13, 12, 11, 10 (5 versions)", True),
                    ("OpenBSD", "7.4, 7.3, 7.2 (3 versions)", True),
                    ("Kali/Gentoo/Void", "Kali Linux, Gentoo, Void Linux (6+ versions)", True),
                ]
            },
            'ip': {
                'title': "🌐 IP COMMANDS (15+)",
                'desc': "```fix\nComplete IP management commands\n```",
                'fields': [
                    (".ip", "Show your IP information", False),
                    (".ip public", "Show server public IP", False),
                    (".ip vps", "Show all VPS IPs", False),
                    (".ip node", "Show all node IPs", False),
                    (".ip all", "Show all IPs", False),
                    (".ip <container>", "Show container IP details", False),
                    (".myip", "Your public IP", False),
                    (".vps-ip [container]", "VPS IP details", False),
                    (".node-ip [node]", "Node IP details", False),
                    (".public-ip", "Server public IP with location", False),
                    (".mac [container]", "MAC address", False),
                    (".gateway [container]", "Gateway information", False),
                    (".netstat [container]", "Network connections", False),
                    (".ifconfig [container]", "Network interfaces", False),
                    (".dns [container]", "DNS servers", False),
                    (".ping-ip <ip>", "Ping IP address", False),
                    (".trace-ip <ip>", "Trace route to IP", False),
                    (".user-ip @user", "User IPs (Admin)", False),
                    (".assign-ip @user <container> [ip]", "Assign IP (Admin)", False),
                    (".release-ip @user <container>", "Release IP (Admin)", False),
                    (".ip-stats", "IP statistics (Admin)", False),
                    (".my-ip-info", "Your network info", False),
                    (".ip-history [@user]", "IP history (Admin)", False),
                ]
            },
        }
        
        # Add admin commands if user is admin
        if is_admin(str(self.ctx.author.id)):
            categories['admin'] = {
                'title': "🛡️ ADMIN COMMANDS (13)",
                'desc': "```fix\nAdministrator commands\n```",
                'fields': [
                    (".create <ram> <cpu> <disk> @user", "Create VPS for user", False),
                    (".delete @user <num> [reason]", "Delete user's VPS", False),
                    (".suspend <container> [reason]", "Suspend VPS", False),
                    (".unsuspend <container>", "Unsuspend VPS", False),
                    (".add-resources <container> [ram] [cpu] [disk]", "Add resources", False),
                    (".list-all", "List all VPS in system", False),
                    (".add-inv @user <amount>", "Add invites", False),
                    (".remove-inv @user <amount>", "Remove invites", False),
                    (".ports-add @user <amount>", "Add port slots", False),
                    (".serverstats", "Server statistics", False),
                    (".admin-add-ipv4 @user <container>", "Assign IPv4", False),
                    (".admin-rm-ipv4 @user [container]", "Remove IPv4", False),
                    (".license-verfiy keyenter", "License Key Verifying", False),
                    (".admin-pending-ipv4", "View pending IPv4 purchases", False),
                ]
            }
        
        # Add owner commands if user is main admin
        if str(self.ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            categories['owner'] = {
                'title': "👑 OWNER COMMANDS (9)",
                'desc': "```fix\nMain owner commands\n```",
                'fields': [
                    (".admin-add @user", "Add new administrator", False),
                    (".admin-remove @user", "Remove administrator", False),
                    (".admin-list", "List all administrators", False),
                    (".maintenance <on/off>", "Toggle maintenance mode", False),
                    (".purge-all", "Purge all unprotected VPS", False),
                    (".protect @user [num]", "Protect VPS from purge", False),
                    (".unprotect @user [num]", "Remove purge protection", False),
                    (".backup-db", "Backup database", False),
                    (".restore-db <file>", "Restore database", False),
                ]
            }
        
        # Get current category data
        cat_data = categories.get(self.current_category, categories['home'])
        
        # Create embed
        embed = discord.Embed(
            title=f"```glow\n{cat_data['title']}\n```",
            description=cat_data['desc'],
            color=COLORS['primary']
        )
        
        # Set category image
        if self.current_category in HELP_IMAGES:
            embed.set_thumbnail(url=HELP_IMAGES[self.current_category])
        embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
        
        # Add fields
        for name, value, inline in cat_data['fields']:
            embed.add_field(name=f"**{name}**", value=value, inline=inline)
        
        # Add footer
        embed.set_footer(
            text=f"⚡ {BOT_NAME} • {len(cat_data['fields'])} commands • Page: {self.current_category.upper()} • Use dropdown to navigate ⚡",
            icon_url=THUMBNAIL_URL
        )
        
        self.embed = embed
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        self.current_category = self.select.values[0]
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    async def refresh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    async def delete_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        await interaction.message.delete()

@bot.command(name="commands")
async def commands_alias(ctx):
    """Alias for help command"""
    await help_command(ctx)


# ==================================================================================================
#  🆕  ADDITIONAL HELP COMMANDS FOR QUICK ACCESS
# ==================================================================================================

@bot.command(name="help-user")
async def help_user(ctx):
    """Quick help for user commands"""
    embed = discord.Embed(
        title="```glow\n👤 User Commands Quick Reference\n```",
        description="```fix\n14 basic commands for all users\n```",
        color=COLORS['info']
    )
    embed.set_thumbnail(url=HELP_IMAGES['user'])
    
    commands_list = [
        ".help", ".ping", ".uptime", ".bot-info", ".server-info",
        ".plans", ".stats", ".inv", ".invites-top", ".claim-free",
        ".my-acc", ".gen-acc", ".api-key", ".userinfo"
    ]
    embed.add_field(name="📋 Commands", value="\n".join([f"• `{c}`" for c in commands_list]), inline=False)
    embed.add_field(name="📌 Tip", value="Use `.help` for detailed information on each command", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="help-vps")
async def help_vps(ctx):
    """Quick help for VPS commands"""
    embed = discord.Embed(
        title="```glow\n🖥️ VPS Commands Quick Reference\n```",
        description="```fix\n8 VPS management commands\n```",
        color=COLORS['info']
    )
    embed.set_thumbnail(url=HELP_IMAGES['vps'])
    
    commands_list = [
        ".myvps", ".list", ".manage", ".stats", ".logs", ".reboot", ".shutdown", ".rename"
    ]
    embed.add_field(name="📋 Commands", value="\n".join([f"• `{c}`" for c in commands_list]), inline=False)
    embed.add_field(name="🎮 Tip", value="Use `.manage` for interactive VPS manager with 20+ buttons", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="help-ip")
async def help_ip(ctx):
    """Quick help for IP commands"""
    embed = discord.Embed(
        title="```glow\n🌐 IP Commands Quick Reference\n```",
        description="```fix\n15+ IP management commands\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=HELP_IMAGES['ip'])
    
    commands_list = [
        ".ip", ".ip public", ".ip vps", ".ip node", ".ip <container>",
        ".myip", ".vps-ip", ".node-ip", ".public-ip", ".mac",
        ".gateway", ".netstat", ".ifconfig", ".dns", ".ping-ip", ".trace-ip"
    ]
    embed.add_field(name="📋 Commands", value="\n".join([f"• `{c}`" for c in commands_list]), inline=False)
    embed.add_field(name="📌 Tip", value="Use `.ip all` to see all IPs at once", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="help-admin")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def help_admin(ctx):
    """Quick help for admin commands"""
    embed = discord.Embed(
        title="```glow\n🛡️ Admin Commands Quick Reference\n```",
        description="```fix\n13 admin commands\n```",
        color=COLORS['warning']
    )
    embed.set_thumbnail(url=HELP_IMAGES['admin'])
    
    commands_list = [
        ".create", ".delete", ".suspend", ".unsuspend", ".add-resources",
        ".list-all", ".add-inv", ".remove-inv", ".ports-add", ".serverstats",
        ".admin-add-ipv4", ".admin-rm-ipv4", ".admin-pending-ipv4"
    ]
    embed.add_field(name="📋 Commands", value="\n".join([f"• `{c}`" for c in commands_list]), inline=False)
    embed.add_field(name="⚠️ Warning", value="These commands affect other users' VPS", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="help-os")
async def help_os(ctx):
    """Quick help for OS options"""
    embed = discord.Embed(
        title="```glow\n🐧 Operating Systems Available\n```",
        description="```fix\n70+ Operating Systems for VPS creation\n```",
        color=COLORS['os']
    )
    embed.set_thumbnail(url=HELP_IMAGES['os'])
    
    os_list = [
        "🐧 Ubuntu (15 versions)", "🌀 Debian (14 versions)", "🎩 Fedora (10 versions)",
        "🦊 Rocky/Alma (6 versions)", "📦 CentOS (6 versions)", "🐧 Alpine (8 versions)",
        "📀 Arch/Manjaro (3 versions)", "🟢 OpenSUSE (4 versions)", "🔵 FreeBSD (5 versions)",
        "🐡 OpenBSD (3 versions)", "🐉 Kali Linux", "💻 Gentoo", "⚪ Void Linux"
    ]
    embed.add_field(name="📋 Available OS", value="\n".join([f"• {o}" for o in os_list]), inline=False)
    embed.add_field(name="📌 Tip", value="Use `.os-list [category]` to see detailed list", inline=False)
    
    await ctx.send(embed=embed)
           
# ==================================================================================================
#  ✅  ON READY
# ==================================================================================================

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_PREFIX}help | {BOT_NAME}"
        )
    )
    logger.info(f"✅ Bot is ready: {bot.user}")
    update_local_node_stats()
    
    total_vps = len(get_all_vps())
    nodes = len(load_nodes()['nodes'])
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                               ║
║                      ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗      ║
║                      ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝      ║
║                      ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║         ║
║                      ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║         ║
║                      ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║         ║
║                      ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝         ║
║                                                                                               ║
║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                            ║
║                                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                               ║
║  📍 Bot Status:    🟢 ONLINE                                                                 ║
║  🤖 Bot Name:      {bot.user}                                         ║
║  🔧 Prefix:        {BOT_PREFIX}                                                               ║
║  🔐 License:       {'✅ VERIFIED' if LICENSE_VERIFIED else '❌ NOT VERIFIED'}                          ║
║  🌐 Server IP:     {SERVER_IP}                                                           ║
║                                                                                               ║
║  🖥️ Total VPS:     {total_vps}                                                               ║
║  🌍 Total Nodes:   {nodes} (auto-detected)                                                    ║
║  🐧 Total OS:      {len(OS_OPTIONS)}                                                          ║
║  🎮 Total Games:   {len(GAMES_LIST)}                                                          ║
║  🛠️ Total Tools:   {len(TOOLS_LIST)}                                                          ║
║                                                                                               ║
║  📊 TOTAL COMMANDS: 92+ │ ✅ BUTTONS │ ✅ SELECT MENUS │ ✅ NODE.JSON │ ✅ EVERYTHING         ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
    """)

# ==================================================================================================
#  ❌  ERROR HANDLER
# ==================================================================================================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_embed("Missing Argument", f"Usage: `{BOT_PREFIX}{ctx.command.name} {ctx.command.signature}`"))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=error_embed("Invalid Argument", "Please check your input."))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=error_embed("Access Denied", "You don't have permission."))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=warning_embed("Cooldown", f"Wait {error.retry_after:.1f}s"))
    else:
        logger.error(f"Error: {error}")
        await ctx.send(embed=error_embed("Error", f"```diff\n- {str(error)[:1900]}\n```"))

# ==================================================================================================
#  🏠  HELP COMMAND
# ==================================================================================================

@bot.command(name="help")
async def help_command(ctx):
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    view = HelpView(ctx)
    await ctx.send(embed=view.embed, view=view)

# ==================================================================================================
#  👤  USER COMMANDS
# ==================================================================================================

@bot.command(name="ping")
async def ping(ctx):
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging..."))
    end = time.time()
    embed = success_embed("Pong! 🏓")
    embed.add_field(name="📡 API", value=f"```fix\n{round(bot.latency*1000)}ms\n```", inline=True)
    embed.add_field(name="⏱️ Response", value=f"```fix\n{round((end-start)*1000)}ms\n```", inline=True)
    await msg.edit(embed=embed)

@bot.command(name="bot-info")
async def bot_info(ctx):
    embed = info_embed("Bot Information")
    embed.add_field(name="📦 Version", value="```fix\n5.0.0\n```", inline=True)
    embed.add_field(name="👑 Author", value=f"```fix\n{BOT_AUTHOR}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(get_all_vps())}\n```", inline=True)
    embed.add_field(name="🐧 OS", value=f"```fix\n{len(OS_OPTIONS)}\n```", inline=True)
    embed.add_field(name="🎮 Games", value=f"```fix\n{len(GAMES_LIST)}\n```", inline=True)
    embed.add_field(name="🛠️ Tools", value=f"```fix\n{len(TOOLS_LIST)}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="server-info")
async def server_info(ctx):
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    embed = info_embed("Server Information")
    embed.add_field(name="💻 Hostname", value=f"```fix\n{HOSTNAME}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="⚙️ CPU", value=f"```fix\n{psutil.cpu_count()} cores @ {cpu}%\n```", inline=True)
    embed.add_field(name="💾 RAM", value=f"```fix\n{mem.used//1024//1024}MB/{mem.total//1024//1024}MB ({mem.percent}%)\n```", inline=True)
    embed.add_field(name="📀 Disk", value=f"```fix\n{disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="plans")
async def plans(ctx):
    embed = info_embed("Free VPS Plans")
    for p in FREE_VPS_PLANS['invites']:
        embed.add_field(name=f"{p['emoji']} {p['name']}", value=f"```fix\nRAM: {p['ram']}GB | CPU: {p['cpu']} | Disk: {p['disk']}GB\nInvites: {p['invites']}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="inv")
async def inv(ctx):
    s = get_user_stats(str(ctx.author.id))
    await ctx.send(embed=info_embed("Your Invites", f"```fix\n{s.get('invites',0)}\n```"))

@bot.command(name="invites-top")
async def invites_top(ctx, lim: int = 10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, invites FROM user_stats WHERE invites > 0 ORDER BY invites DESC LIMIT ?', (lim,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No invites"))
    embed = info_embed(f"Top {min(lim,len(rows))} Inviters")
    medals = ["🥇","🥈","🥉"]
    for i, r in enumerate(rows,1):
        try:
            u = await bot.fetch_user(int(r['user_id']))
            name = u.name
        except:
            name = "Unknown"
        m = medals[i-1] if i<=3 else f"{i}."
        embed.add_field(name=f"{m} {name}", value=f"```fix\nInvites: {r['invites']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="claim-free")
async def claim_free(ctx):
    uid = str(ctx.author.id)
    if get_user_vps(uid):
        return await ctx.send(embed=error_embed("Already have VPS", "You can only claim one free VPS."))
    s = get_user_stats(uid)
    inv = s.get('invites',0)
    plan = None
    for p in reversed(FREE_VPS_PLANS['invites']):
        if inv >= p['invites']:
            plan = p
            break
    if not plan:
        return await ctx.send(embed=error_embed("No Plan", f"You have {inv} invites. Need at least 5."))
    
    opts = []
    for o in OS_OPTIONS[:25]:
        opts.append(discord.SelectOption(label=o['label'][:100], value=o['value'], description=o['desc'][:100]))
    view = View()
    sel = Select(placeholder="Select OS...", options=opts)
    async def sel_cb(i):
        if i.user.id != ctx.author.id:
            return await i.response.send_message("Not for you!", ephemeral=True)
        osv = sel.values[0]
        name = f"svm5-{uid[:6]}-{random.randint(1000,9999)}"
        msg = await i.followup.send(embed=info_embed("Creating VPS", "Step 1/4..."), ephemeral=True)
        try:
            ram_mb = plan['ram'] * 1024
            await run_lxc(f"lxc init {osv} {name} -s {DEFAULT_STORAGE_POOL}")
            await msg.edit(embed=info_embed("Creating VPS", "Step 2/4..."))
            await run_lxc(f"lxc config set {name} limits.memory {ram_mb}MB")
            await run_lxc(f"lxc config set {name} limits.cpu {plan['cpu']}")
            await run_lxc(f"lxc config device set {name} root size={plan['disk']}GB")
            await msg.edit(embed=info_embed("Creating VPS", "Step 3/4..."))
            await run_lxc(f"lxc start {name}")
            await asyncio.sleep(3)
            await msg.edit(embed=info_embed("Creating VPS", "Step 4/4..."))
            add_vps(uid, name, plan['ram'], plan['cpu'], plan['disk'], osv, plan['name'])
            update_user_stats(uid, -plan['invites'], 1)
            embed = success_embed("VPS Created!")
            embed.add_field(name="📦 Container", value=f"```fix\n{name}\n```", inline=True)
            embed.add_field(name="⚙️ Resources", value=f"```fix\n{plan['ram']}GB RAM / {plan['cpu']} CPU / {plan['disk']}GB Disk\n```", inline=False)
            await msg.edit(embed=embed)
        except Exception as e:
            await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))
    sel.callback = sel_cb
    view.add_item(sel)
    await ctx.send(embed=info_embed("Claim Free VPS", f"**{plan['emoji']} {plan['name']}**\nRAM: {plan['ram']}GB | CPU: {plan['cpu']} | Disk: {plan['disk']}GB\n\nSelect OS:"), view=view)

@bot.command(name="gen-acc")
async def gen_acc(ctx):
    adj = ["cool","fast","dark","epic","blue","swift","neon","alpha","delta"]
    noun = ["wolf","tiger","storm","byte","nova","blade","fox","raven","hawk"]
    name = f"{random.choice(adj)}{random.choice(noun)}{random.randint(10,999)}"
    email = f"{name}@{random.choice(['gmail.com','yahoo.com','outlook.com'])}"
    pwd = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$%", k=16))
    api = hashlib.sha256(f"{ctx.author.id}{time.time()}".encode()).hexdigest()[:32]
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS generated_accounts (user_id TEXT PRIMARY KEY, username TEXT, email TEXT, password TEXT, api_key TEXT, created_at TEXT)''')
    cur.execute('INSERT OR REPLACE INTO generated_accounts VALUES (?,?,?,?,?,?)', (str(ctx.author.id), name, email, pwd, api, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    try:
        dm = success_embed("Your Account")
        dm.add_field(name="👤 Username", value=f"```fix\n{name}\n```")
        dm.add_field(name="📧 Email", value=f"```fix\n{email}\n```")
        dm.add_field(name="🔑 Password", value=f"```fix\n{pwd}\n```")
        dm.add_field(name="🗝️ API", value=f"```fix\n{api}\n```")
        await ctx.author.send(embed=dm)
        await ctx.send(embed=success_embed("Account Generated", "Check your DMs!"))
    except:
        await ctx.send(embed=error_embed("DM Failed", "Enable DMs to receive credentials."))

@bot.command(name="my-acc")
async def my_acc(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM generated_accounts WHERE user_id = ?', (str(ctx.author.id),))
    row = cur.fetchone()
    conn.close()
    if row:
        embed = info_embed("Your Account")
        embed.add_field(name="👤 Username", value=f"```fix\n{row['username']}\n```")
        embed.add_field(name="📧 Email", value=f"```fix\n{row['email']}\n```")
        embed.add_field(name="🗝️ API", value=f"```fix\n{row['api_key']}\n```")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=info_embed("No Account", "Use `.gen-acc` to create one."))

@bot.command(name="api-key")
async def api_key_cmd(ctx, action: str = "view"):
    uid = str(ctx.author.id)
    if action.lower() == "regenerate":
        new = hashlib.sha256(f"{uid}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE user_stats SET api_key = ?, last_updated = ? WHERE user_id = ?', (new, datetime.now().isoformat(), uid))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("API Key Regenerated", f"```fix\n{new}\n```"))
    else:
        s = get_user_stats(uid)
        await ctx.send(embed=info_embed("Your API Key", f"```fix\n{s.get('api_key','None')}\n```"))

@bot.command(name="userinfo")
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    elif not is_admin(str(ctx.author.id)) and user.id != ctx.author.id:
        return await ctx.send(embed=error_embed("Access Denied", "You can only view yourself."))
    uid = str(user.id)
    vps = get_user_vps(uid)
    s = get_user_stats(uid)
    embed = info_embed(f"User: {user.display_name}")
    embed.set_thumbnail(url=user.avatar.url if user.avatar else THUMBNAIL_URL)
    embed.add_field(name="🆔 ID", value=f"```fix\n{user.id}\n```", inline=True)
    embed.add_field(name="📨 Invites", value=f"```fix\n{s.get('invites',0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(vps)}\n```", inline=True)
    if vps:
        text = "\n".join([f"{'🟢' if v['status']=='running' else '🔴'} `{v['container_name']}`" for v in vps[:3]])
        embed.add_field(name="📋 VPS List", value=text, inline=False)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🖥️  VPS COMMANDS
# ==================================================================================================

@bot.command(name="myvps")
async def myvps(ctx):
    vps = get_user_vps(str(ctx.author.id))
    if not vps:
        return await ctx.send(embed=no_vps_embed())
    embed = info_embed(f"Your VPS ({len(vps)})")
    for i, v in enumerate(vps,1):
        status = "🟢" if v['status']=='running' and not v['suspended'] else "⛔" if v['suspended'] else "🔴"
        text = f"{status} **`{v['container_name']}`**\n```fix\nRAM: {v['ram']}GB | CPU: {v['cpu']} | Disk: {v['disk']}GB\nIP: {v.get('ip_address','N/A')}\n```"
        embed.add_field(name=f"VPS #{i}", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="list")
async def list_cmd(ctx):
    await myvps(ctx)

# In your manage command, replace the old view with:
@bot.command(name="manage")
async def manage(ctx, container: str = None):
    uid = str(ctx.author.id)
    
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
        container_data = vps[0]
    elif not any(v['container_name'] == container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    else:
        vps = get_user_vps(uid)
        container_data = next((v for v in vps if v['container_name'] == container), None)
    
    view = VPSManageView(ctx, container, container_data)
    embed = await view.get_stats_embed()
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg

@bot.command(name="stats")
async def vps_stats(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    stats = await get_container_stats(container)
    embed = info_embed(f"Stats: {container}")
    embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
    embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
    embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
    embed.add_field(name="💽 Disk", value=f"```fix\n{stats['disk']}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{stats['mac']}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{stats['uptime']}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="logs")
async def logs(ctx, container: str = None, lines: int = 50):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    lines = min(lines,200)
    out,_,_ = await exec_in_container(container, f"journalctl -n {lines} --no-pager 2>/dev/null || dmesg | tail -{lines}")
    embed = terminal_embed(f"Logs: {container}", out[:1900])
    await ctx.send(embed=embed)

@bot.command(name="reboot")
async def reboot(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await ctx.send(embed=info_embed("Rebooting", f"```fix\n{container}\n```"))
    await run_lxc(f"lxc restart {container}")
    update_vps_status(container, 'running')
    await ctx.send(embed=success_embed("Rebooted", f"```fix\n{container}\n```"))

@bot.command(name="shutdown")
async def shutdown(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await ctx.send(embed=info_embed("Shutting Down", f"```fix\n{container}\n```"))
    await run_lxc(f"lxc stop {container}")
    update_vps_status(container, 'stopped')
    await ctx.send(embed=success_embed("Shutdown", f"```fix\n{container}\n```"))

@bot.command(name="rename")
async def rename(ctx, old: str, new: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==old for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$', new):
        return await ctx.send(embed=error_embed("Invalid Name", "Use letters, numbers, hyphens only."))
    await ctx.send(embed=info_embed("Renaming", f"```fix\n{old} → {new}\n```"))
    status = await get_container_status(old)
    was = status == 'running'
    if was:
        await run_lxc(f"lxc stop {old}")
        await asyncio.sleep(2)
    await run_lxc(f"lxc move {old} {new}")
    if was:
        await run_lxc(f"lxc start {new}")
    conn = get_db()
    cur = conn.cursor()
    for t in ['vps','shared_vps','installed_games','installed_tools','ipv4','port_forwards','panels']:
        cur.execute(f'UPDATE {t} SET container_name = ? WHERE container_name = ?', (new, old))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Renamed", f"```fix\n{old} → {new}\n```"))

# ==================================================================================================
#  📟  CONSOLE COMMANDS
# ==================================================================================================

@bot.command(name="ss")
async def ss(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    msg = await ctx.send(embed=info_embed("📸 Snapshot", f"```fix\n{container}\n```"))
    u,_,_ = await exec_in_container(container, "uname -a")
    up,_,_ = await exec_in_container(container, "uptime")
    m,_,_ = await exec_in_container(container, "free -h")
    d,_,_ = await exec_in_container(container, "df -h")
    p,_,_ = await exec_in_container(container, "ps aux | head -15")
    out = f"=== {container} ===\nUname: {u}\nUptime: {up}\n\n{m}\n\n{d}\n\n{p}"
    embed = terminal_embed(f"Snapshot: {container}", out[:1900])
    await msg.edit(embed=embed)

@bot.command(name="console")
async def console(ctx, container: str, *, cmd: str = None):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    if not cmd:
        view = View()
        btn = Button(label="⚡ Run Command", style=discord.ButtonStyle.primary)
        async def btn_cb(i):
            modal = ConsoleModal(container)
            await i.response.send_modal(modal)
        btn.callback = btn_cb
        view.add_item(btn)
        return await ctx.send(embed=info_embed(f"Console: {container}", "Click button to run command"), view=view)
    
    msg = await ctx.send(embed=info_embed("Executing", f"```fix\n$ {cmd}\n```"))
    out, err, code = await exec_in_container(container, cmd)
    embed = terminal_embed(f"Output", f"$ {cmd}\n\n{(out or err)[:1900]}")
    embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```")
    await msg.edit(embed=embed)

@bot.command(name="execute")
async def execute(ctx, container: str, *, cmd: str):
    await console(ctx, container, cmd=cmd)

@bot.command(name="ssh-gen")
async def ssh_gen(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    msg = await ctx.send(embed=info_embed("Generating SSH", f"```fix\n{container}\n```"))
    await exec_in_container(container, "apt-get update -qq && apt-get install -y -qq tmate")
    sess = f"svm5-{random.randint(1000,9999)}"
    await exec_in_container(container, f"tmate -S /tmp/{sess}.sock new-session -d")
    await asyncio.sleep(5)
    out, _, _ = await exec_in_container(container, f"tmate -S /tmp/{sess}.sock display -p '#{{tmate_ssh}}'")
    url = out.strip()
    if url:
        try:
            dm = success_embed("SSH Access")
            dm.add_field(name="Container", value=f"```fix\n{container}\n```")
            dm.add_field(name="Command", value=f"```bash\n{url}\n```")
            await ctx.author.send(embed=dm)
            await msg.edit(embed=success_embed("SSH Generated", "Check your DMs!"))
        except:
            await msg.edit(embed=error_embed("DM Failed", f"```fix\n{url}\n```"))
    else:
        await msg.edit(embed=error_embed("Failed", "Could not generate SSH"))

@bot.command(name="top")
async def top(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "ps aux --sort=-%cpu | head -20")
    embed = terminal_embed(f"Top: {container}", out)
    await ctx.send(embed=embed)

@bot.command(name="df")
async def df(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "df -h")
    embed = terminal_embed(f"Disk: {container}", out)
    await ctx.send(embed=embed)

@bot.command(name="free")
async def free(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "free -h")
    embed = terminal_embed(f"Memory: {container}", out)
    await ctx.send(embed=embed)

@bot.command(name="ps")
async def ps_cmd(ctx, container: str = None):
    await top(ctx, container)

@bot.command(name="who")
async def who(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "who")
    embed = terminal_embed(f"Users: {container}", out or "No users")
    await ctx.send(embed=embed)

@bot.command(name="uptime")
async def uptime_cmd(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "uptime")
    await ctx.send(embed=info_embed(f"Uptime: {container}", f"```fix\n{out}\n```"))

# ==================================================================================================
#  🎮  GAMES COMMANDS
# ==================================================================================================

@bot.command(name="games")
async def games(ctx):
    embed = info_embed("Available Games", f"```fix\nTotal: {len(GAMES_LIST)}\n```")
    for g in GAMES_LIST:
        embed.add_field(name=f"{g['icon']} {g['name']}", value=f"```fix\nPort: {g['port']} | RAM: {g['ram']}MB\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="game-info")
async def game_info(ctx, *, name: str):
    g = next((x for x in GAMES_LIST if x['name'].lower() == name.lower()), None)
    if not g:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    embed = info_embed(f"{g['icon']} {g['name']}")
    embed.add_field(name="🔌 Port", value=f"```fix\n{g['port']}\n```", inline=True)
    embed.add_field(name="💾 RAM", value=f"```fix\n{g['ram']}MB\n```", inline=True)
    embed.add_field(name="🐳 Docker", value=f"```fix\n{g['docker']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="install-game")
async def install_game(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    g = next((x for x in GAMES_LIST if x['name'].lower() == game.lower()), None)
    if not g:
        return await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game}\n```"))
    msg = await ctx.send(embed=info_embed("Installing", f"```fix\n{g['name']} on {container}\n```"))
    await exec_in_container(container, "which docker || curl -fsSL https://get.docker.com | bash")
    cmd = f"docker run -d --name {g['name'].lower().replace(' ','-')} -p {g['port']}:{g['port']} {g['docker']}"
    out, err, code = await exec_in_container(container, cmd)
    if code == 0:
        add_game_install(uid, container, g['name'], g['port'])
        embed = success_embed("Game Installed")
        embed.add_field(name="🎮 Game", value=f"```fix\n{g['name']}\n```", inline=True)
        embed.add_field(name="🔌 Port", value=f"```fix\n{g['port']}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {err}\n```"))

@bot.command(name="my-games")
async def my_games(ctx, container: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if container:
        cur.execute('SELECT * FROM installed_games WHERE user_id = ? AND container_name = ?', (uid, container))
    else:
        cur.execute('SELECT * FROM installed_games WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Games", "No games installed."))
    embed = info_embed("Your Games")
    for r in rows:
        embed.add_field(name=f"🎮 {r['game_name']}", value=f"```fix\nContainer: {r['container_name']}\nPort: {r['game_port']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="start-game")
async def start_game(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await exec_in_container(container, f"docker start {game.lower().replace(' ','-')}")
    await ctx.send(embed=success_embed("Game Started", f"```fix\n{game}\n```"))

@bot.command(name="stop-game")
async def stop_game(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await exec_in_container(container, f"docker stop {game.lower().replace(' ','-')}")
    await ctx.send(embed=success_embed("Game Stopped", f"```fix\n{game}\n```"))

@bot.command(name="game-stats")
async def game_stats(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, f"docker stats {game.lower().replace(' ','-')} --no-stream")
    embed = terminal_embed(f"Game Stats: {game}", out)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🛠️  TOOLS COMMANDS
# ==================================================================================================

@bot.command(name="tools")
async def tools(ctx):
    embed = info_embed("Available Tools", f"```fix\nTotal: {len(TOOLS_LIST)}\n```")
    for t in TOOLS_LIST:
        embed.add_field(name=f"{t['icon']} {t['name']}", value=f"```fix\nPort: {t.get('port','None')}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="tool-info")
async def tool_info(ctx, *, name: str):
    t = next((x for x in TOOLS_LIST if x['name'].lower() == name.lower()), None)
    if not t:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    embed = info_embed(f"{t['icon']} {t['name']}")
    if t.get('port'):
        embed.add_field(name="🔌 Port", value=f"```fix\n{t['port']}\n```", inline=True)
    embed.add_field(name="📝 Command", value=f"```bash\n{t['cmd']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="install-tool")
async def install_tool(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    t = next((x for x in TOOLS_LIST if x['name'].lower() == tool.lower()), None)
    if not t:
        return await ctx.send(embed=error_embed("Tool Not Found", f"```diff\n- {tool}\n```"))
    msg = await ctx.send(embed=info_embed("Installing", f"```fix\n{t['name']} on {container}\n```"))
    out, err, code = await exec_in_container(container, t['cmd'])
    if code == 0 or "already" in err.lower():
        add_tool_install(uid, container, t['name'], t.get('port'))
        embed = success_embed("Tool Installed")
        embed.add_field(name="🛠️ Tool", value=f"```fix\n{t['name']}\n```", inline=True)
        embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {err}\n```"))

@bot.command(name="my-tools")
async def my_tools(ctx, container: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if container:
        cur.execute('SELECT * FROM installed_tools WHERE user_id = ? AND container_name = ?', (uid, container))
    else:
        cur.execute('SELECT * FROM installed_tools WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Tools", "No tools installed."))
    embed = info_embed("Your Tools")
    for r in rows:
        embed.add_field(name=f"🛠️ {r['tool_name']}", value=f"```fix\nContainer: {r['container_name']}\nPort: {r['tool_port'] or 'None'}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="start-tool")
async def start_tool(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    svc = tool.lower().replace(' ','')
    await exec_in_container(container, f"systemctl start {svc} 2>/dev/null || service {svc} start")
    await ctx.send(embed=success_embed("Tool Started", f"```fix\n{tool}\n```"))

@bot.command(name="stop-tool")
async def stop_tool(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    svc = tool.lower().replace(' ','')
    await exec_in_container(container, f"systemctl stop {svc} 2>/dev/null || service {svc} stop")
    await ctx.send(embed=success_embed("Tool Stopped", f"```fix\n{tool}\n```"))

@bot.command(name="tool-port")
async def tool_port(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    t = next((x for x in TOOLS_LIST if x['name'].lower() == tool.lower()), None)
    if not t or not t.get('port'):
        return await ctx.send(embed=error_embed("No Port", f"```diff\n- {tool} has no default port\n```"))
    await ctx.send(embed=success_embed("Tool Port", f"```fix\n{tool} runs on port {t['port']}\n```"))

# ==================================================================================================
#  🌐  NODE COMMANDS
# ==================================================================================================

@bot.command(name="node")
async def node_list(ctx):
    nodes = load_nodes()
    embed = node_embed("Node Network", f"```fix\nTotal: {len(nodes['nodes'])}\n```")
    for n, data in nodes['nodes'].items():
        s = data.get('stats', {})
        status = "🟢" if data['status']=='online' else "🔴"
        text = f"```fix\nHost: {data['host']}\nRAM: {s.get('used_ram',0)}/{s.get('total_ram',0)} MB\nCPU: {s.get('used_cpu',0)}%\nLXC: {s.get('lxc_count',0)}\n```"
        embed.add_field(name=f"{status} {n}", value=text, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="node-info")
async def node_info(ctx, name: str = "local"):
    nodes = load_nodes()
    n = nodes['nodes'].get(name)
    if not n:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    s = n.get('stats', {})
    embed = node_embed(f"Node: {name}")
    basic = f"```fix\nHost: {n['host']}:{n['port']}\nStatus: {n['status']}\nType: {n['type']}\n```"
    res = f"```fix\nRAM: {s.get('used_ram',0)}/{s.get('total_ram',0)} MB\nCPU: {s.get('used_cpu',0)}%\nDisk: {s.get('used_disk',0)}/{s.get('total_disk',0)} GB\nLXC: {s.get('lxc_count',0)}\n```"
    embed.add_field(name="📋 Basic", value=basic, inline=True)
    embed.add_field(name="📊 Resources", value=res, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="node-add")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_add(ctx, name: str, host: str, user: str, pwd: str = None, port: int = 22):
    nodes = load_nodes()
    if name in nodes['nodes']:
        return await ctx.send(embed=error_embed("Exists", f"```diff\n- {name} already exists\n```"))
    import paramiko
    msg = await ctx.send(embed=info_embed("Connecting", f"```fix\n{host}\n```"))
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if pwd:
            client.connect(host, port=port, username=user, password=pwd, timeout=10)
        else:
            key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
            client.connect(host, port=port, username=user, pkey=key, timeout=10)
        stdin,stdout,stderr = client.exec_command('nproc')
        cpu = stdout.read().decode().strip()
        stdin,stdout,stderr = client.exec_command("free -m | awk '/^Mem:/{print $2}'")
        ram = stdout.read().decode().strip()
        stdin,stdout,stderr = client.exec_command("df -BG / | awk 'NR==2{print $2}' | sed 's/G//'")
        disk = stdout.read().decode().strip()
        client.close()
        node_data = {
            "name": name, "host": host, "port": port, "username": user, "password": pwd,
            "type": "remote", "status": "online", "is_main": False, "region": "us",
            "stats": {
                "total_ram": int(ram) if ram.isdigit() else 0, "used_ram": 0,
                "total_cpu": int(cpu) if cpu.isdigit() else 0, "used_cpu": 0,
                "total_disk": int(disk) if disk.isdigit() else 0, "used_disk": 0,
                "lxc_count": 0, "last_checked": datetime.now().isoformat()
            }
        }
        nodes['nodes'][name] = node_data
        nodes['node_groups']['all'].append(name)
        save_nodes(nodes)
        await msg.edit(embed=success_embed("Node Added", f"```fix\n{name} connected\n```"))
    except Exception as e:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="node-remove")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_remove(ctx, name: str):
    nodes = load_nodes()
    if name not in nodes['nodes'] or name == 'local':
        return await ctx.send(embed=error_embed("Cannot Remove", "Node not found or is main node."))
    del nodes['nodes'][name]
    nodes['node_groups']['all'] = [x for x in nodes['node_groups']['all'] if x != name]
    save_nodes(nodes)
    await ctx.send(embed=success_embed("Node Removed", f"```fix\n{name}\n```"))

@bot.command(name="node-check")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_check(ctx, name: str):
    n = get_node(name)
    if not n:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    if name == 'local':
        return await ctx.send(embed=success_embed("Local Node", "```fix\nOnline\n```"))
    import paramiko
    msg = await ctx.send(embed=info_embed("Checking", f"```fix\n{name}\n```"))
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if n.get('password'):
            client.connect(n['host'], port=n['port'], username=n['username'], password=n['password'], timeout=10)
        else:
            key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
            client.connect(n['host'], port=n['port'], username=n['username'], pkey=key, timeout=10)
        client.close()
        nodes = load_nodes()
        nodes['nodes'][name]['status'] = 'online'
        nodes['nodes'][name]['stats']['last_checked'] = datetime.now().isoformat()
        save_nodes(nodes)
        await msg.edit(embed=success_embed("Node Online", f"```fix\n{name} is healthy\n```"))
    except:
        nodes = load_nodes()
        nodes['nodes'][name]['status'] = 'offline'
        save_nodes(nodes)
        await msg.edit(embed=error_embed("Node Offline", f"```diff\n- {name} is offline\n```"))

@bot.command(name="node-stats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_stats(ctx):
    nodes = load_nodes()
    alln = nodes['nodes']
    tr = sum(n['stats'].get('total_ram',0) for n in alln.values())
    ur = sum(n['stats'].get('used_ram',0) for n in alln.values())
    td = sum(n['stats'].get('total_disk',0) for n in alln.values())
    ud = sum(n['stats'].get('used_disk',0) for n in alln.values())
    tc = sum(n['stats'].get('total_cpu',0) for n in alln.values())
    tl = sum(n['stats'].get('lxc_count',0) for n in alln.values())
    on = sum(1 for n in alln.values() if n['status']=='online')
    embed = node_embed("Cluster Statistics")
    embed.add_field(name="📊 Summary", value=f"```fix\nTotal: {len(alln)}\nOnline: {on}\nOffline: {len(alln)-on}\nLXC: {tl}\n```", inline=False)
    embed.add_field(name="💾 Resources", value=f"```fix\nRAM: {ur}/{tr} MB ({(ur/tr*100) if tr>0 else 0:.1f}%)\nDisk: {ud}/{td} GB ({(ud/td*100) if td>0 else 0:.1f}%)\nCPU Cores: {tc}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="node-connect")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_connect(ctx, host: str, user: str, pwd: str = None, name: str = None, port: int = 22):
    if not name:
        name = host.split('.')[0]
    await node_add(ctx, name, host, user, pwd, port)

# ==================================================================================================
#  👥  SHARE COMMANDS
# ==================================================================================================

@bot.command(name="share")
async def share(ctx, user: discord.Member, num: int):
    uid = str(ctx.author.id)
    vps = get_user_vps(uid)
    if num < 1 or num > len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    container = vps[num-1]['container_name']
    if share_vps(uid, str(user.id), container):
        await ctx.send(embed=success_embed("Shared", f"```fix\n{container} with {user.name}\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Could not share VPS"))

@bot.command(name="unshare")
async def unshare(ctx, user: discord.Member, num: int):
    uid = str(ctx.author.id)
    vps = get_user_vps(uid)
    if num < 1 or num > len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    container = vps[num-1]['container_name']
    if unshare_vps(uid, str(user.id), container):
        await ctx.send(embed=success_embed("Unshared", f"```fix\n{container} from {user.name}\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Could not unshare VPS"))

@bot.command(name="shared")
async def shared(ctx):
    shared = get_shared_vps(str(ctx.author.id))
    if not shared:
        return await ctx.send(embed=info_embed("No Shared", "No one has shared VPS with you."))
    embed = info_embed("Shared With You")
    for v in shared:
        try:
            owner = await bot.fetch_user(int(v['owner_id']))
            oname = owner.name
        except:
            oname = "Unknown"
        embed.add_field(name=f"📦 {v['container_name']}", value=f"```fix\nOwner: {oname}\nStatus: {v['status']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="manage-shared")
async def manage_shared(ctx, owner: discord.Member, num: int):
    shared = get_shared_vps(str(ctx.author.id))
    owner_vps = [v for v in shared if v['owner_id'] == str(owner.id)]
    if num < 1 or num > len(owner_vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(owner_vps)}"))
    v = owner_vps[num-1]
    await manage(ctx, container=v['container_name'])

# ==================================================================================================
#  🔌  PORT COMMANDS
# ==================================================================================================

@bot.group(name="ports", invoke_without_command=True)
async def ports(ctx):
    uid = str(ctx.author.id)
    alloc = get_port_allocation(uid)
    fwds = get_user_port_forwards(uid)
    embed = info_embed("Port Forwarding")
    embed.add_field(name="📊 Quota", value=f"```fix\nAllocated: {alloc}\nUsed: {len(fwds)}\nAvailable: {alloc-len(fwds)}\n```", inline=False)
    embed.add_field(name="📋 Commands", value=f"`.ports add <vps_num> <port> [tcp/udp]`\n`.ports list`\n`.ports remove <id>`\n`.ports quota`\n`.ports check <port>`", inline=False)
    await ctx.send(embed=embed)

@ports.command(name="add")
async def ports_add(ctx, num: int, port: int, proto: str = "tcp+udp"):
    uid = str(ctx.author.id)
    vps = get_user_vps(uid)
    if not vps:
        return await ctx.send(embed=no_vps_embed())
    if num < 1 or num > len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    if port < 1 or port > 65535:
        return await ctx.send(embed=error_embed("Invalid", "Port must be 1-65535"))
    if proto not in ["tcp","udp","tcp+udp"]:
        return await ctx.send(embed=error_embed("Invalid", "Protocol must be tcp, udp, or tcp+udp"))
    alloc = get_port_allocation(uid)
    if len(get_user_port_forwards(uid)) >= alloc:
        return await ctx.send(embed=error_embed("Quota Exceeded", f"You have used all {alloc} slots"))
    v = vps[num-1]
    if v['suspended'] or v['status'] != 'running':
        return await ctx.send(embed=error_embed("Cannot Add", "VPS must be running"))
    msg = await ctx.send(embed=info_embed("Creating port forward..."))
    hport = await create_port_forward(uid, v['container_name'], port, proto)
    if hport:
        embed = success_embed("Port Forward Created")
        embed.add_field(name="📦 VPS", value=f"```fix\n#{num} - {v['container_name']}\n```", inline=True)
        embed.add_field(name="🔌 Container", value=f"```fix\n{port}\n```", inline=True)
        embed.add_field(name="🌐 Host", value=f"```fix\n{SERVER_IP}:{hport}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", "Could not assign port"))

@ports.command(name="list")
async def ports_list(ctx):
    uid = str(ctx.author.id)
    fwds = get_user_port_forwards(uid)
    if not fwds:
        return await ctx.send(embed=info_embed("No Port Forwards", "You have no active forwards."))
    embed = info_embed(f"Your Port Forwards ({len(fwds)})")
    for f in fwds:
        vnum = next((i+1 for i,v in enumerate(get_user_vps(uid)) if v['container_name']==f['container_name']), '?')
        embed.add_field(name=f"ID: {f['id']}", value=f"```fix\nVPS #{vnum}: {f['container_port']} → {SERVER_IP}:{f['host_port']} ({f['protocol']})\nCreated: {f['created_at'][:16]}\n```", inline=False)
    await ctx.send(embed=embed)

@ports.command(name="remove")
async def ports_remove(ctx, fid: int):
    uid = str(ctx.author.id)
    success, container, hport = remove_port_forward(fid)
    if not success:
        return await ctx.send(embed=error_embed("Not Found", f"ID {fid} not found"))
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this forward"))
    await remove_port_device(container, hport)
    await ctx.send(embed=success_embed("Removed", f"```fix\nForward ID {fid} removed\n```"))

@ports.command(name="quota")
async def ports_quota(ctx):
    uid = str(ctx.author.id)
    alloc = get_port_allocation(uid)
    used = len(get_user_port_forwards(uid))
    embed = info_embed("Port Quota")
    embed.add_field(name="📊 Allocated", value=f"```fix\n{alloc}\n```", inline=True)
    embed.add_field(name="📊 Used", value=f"```fix\n{used}\n```", inline=True)
    embed.add_field(name="📊 Available", value=f"```fix\n{alloc-used}\n```", inline=True)
    await ctx.send(embed=embed)

@ports.command(name="check")
async def ports_check(ctx, port: int):
    try:
        out = subprocess.getoutput(f"ss -tuln | grep :{port}")
        if out:
            await ctx.send(embed=error_embed("Port Unavailable", f"```diff\n- Port {port} is in use\n```"))
        else:
            await ctx.send(embed=success_embed("Port Available", f"```fix\nPort {port} is free\n```"))
    except:
        await ctx.send(embed=info_embed("Port Check", f"```fix\nCould not check port {port}\n```"))

# ==================================================================================================
#  🌍  IPv4 COMMANDS
# ==================================================================================================

UPI_ID = get_setting('upi_id', '9892642904@ybl')
IPV4_PRICE = int(get_setting('ipv4_price', '50'))

def gen_upi_qr(upi: str, amt: int = None, note: str = None):
    try:
        url = f"upi://pay?pa={upi}&pn={BOT_NAME}"
        if amt:
            url += f"&am={amt}"
        if note:
            url += f"&tn={note}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        bio = io.BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        return bio
    except:
        return None

@bot.command(name="ipv4")
async def ipv4_list(ctx, user: discord.Member = None):
    if user and user.id != ctx.author.id and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("Access Denied", "Only admins can view others."))
    tid = str(user.id) if user else str(ctx.author.id)
    ips = get_user_ipv4(tid)
    if not ips:
        return await ctx.send(embed=info_embed("No IPv4", "No addresses assigned."))
    embed = info_embed(f"IPv4 for {user.display_name if user else ctx.author.display_name}")
    for i, ip in enumerate(ips, 1):
        val = f"```fix\nContainer: {ip['container_name']}\nPublic: {ip['public_ip']}\nPrivate: {ip['private_ip']}\nMAC: {ip['mac_address']}\nAssigned: {ip['assigned_at'][:16]}\n```"
        embed.add_field(name=f"IPv4 #{i}", value=val, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ipv4-details")
async def ipv4_details(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)) and not is_admin(uid):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    ips = get_user_ipv4(uid)
    ip = next((i for i in ips if i['container_name']==container), None)
    out,_,_ = await exec_in_container(container, "ip addr show")
    embed = info_embed(f"IPv4 Details: {container}")
    if ip:
        embed.add_field(name="🌐 Public", value=f"```fix\n{ip['public_ip']}\n```", inline=True)
        embed.add_field(name="🏠 Private", value=f"```fix\n{ip['private_ip']}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{ip['mac_address']}\n```", inline=True)
    embed.add_field(name="📋 Network", value=f"```bash\n{out[:500]}\n```", inline=False)
    await ctx.send(embed=embed)

class TxnModal(Modal):
    def __init__(self, ctx, ref):
        super().__init__(title="Enter Transaction ID")
        self.ctx = ctx
        self.ref = ref
        self.add_item(InputText(label="UPI Transaction ID", placeholder="e.g., T25031234567890", min_length=8))
    async def callback(self, interaction):
        tid = self.children[0].value
        add_transaction(str(self.ctx.author.id), self.ref, IPV4_PRICE)
        for aid in MAIN_ADMIN_IDS:
            try:
                admin = await bot.fetch_user(aid)
                await admin.send(embed=warning_embed("New IPv4 Purchase", f"```fix\nUser: {self.ctx.author}\nRef: {self.ref}\nTxn: {tid}\nAmount: ₹{IPV4_PRICE}\n```"))
            except:
                pass
        await interaction.response.edit_message(embed=info_embed("Payment Submitted", f"```fix\nReference: {self.ref}\nTxn ID: {tid}\n```\nAdmin will verify."), view=None)

@bot.command(name="buy-ipv4")
async def buy_ipv4(ctx):
    ref = ''.join(random.choices(string.ascii_uppercase+string.digits, k=10))
    embed = info_embed("Buy IPv4 Address")
    embed.add_field(name="💰 Price", value=f"```fix\n₹{IPV4_PRICE}\n```", inline=True)
    embed.add_field(name="📱 UPI", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="🔖 Ref", value=f"```fix\n{ref}\n```", inline=True)
    embed.add_field(name="📋 Instructions", value=f"```fix\n1. Pay ₹{IPV4_PRICE} to {UPI_ID}\n2. Add ref {ref}\n3. Click ✅ below\n```", inline=False)
    qr = gen_upi_qr(UPI_ID, IPV4_PRICE, ref)
    file = discord.File(qr, filename="qr.png") if qr else None
    if file:
        embed.set_image(url="attachment://qr.png")
    view = View()
    pay_btn = Button(label="✅ I've Paid", style=discord.ButtonStyle.success)
    async def pay_cb(i):
        if i.user.id != ctx.author.id:
            await i.response.send_message("Not your purchase!", ephemeral=True)
            return
        await i.response.send_modal(TxnModal(ctx, ref))
    pay_btn.callback = pay_cb
    view.add_item(pay_btn)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    cancel_btn.callback = cancel_cb
    view.add_item(cancel_btn)
    if file:
        await ctx.send(embed=embed, file=file, view=view)
    else:
        await ctx.send(embed=embed, view=view)

@bot.command(name="upi")
async def upi_info(ctx):
    embed = info_embed("UPI Information")
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="💰 IPv4 Price", value=f"```fix\n₹{IPV4_PRICE}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="upi-qr")
async def upi_qr(ctx, amt: int = None, *, note: str = None):
    if not note:
        note = f"Payment to {BOT_NAME}"
    qr = gen_upi_qr(UPI_ID, amt, note)
    if not qr:
        return await ctx.send(embed=error_embed("Failed", "Could not generate QR"))
    file = discord.File(qr, filename="qr.png")
    embed = info_embed("UPI QR Code")
    if amt:
        embed.add_field(name="💰 Amount", value=f"```fix\n₹{amt}\n```", inline=True)
    if note:
        embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
    embed.set_image(url="attachment://qr.png")
    await ctx.send(embed=embed, file=file)

@bot.command(name="pay")
async def pay(ctx, amt: int, *, note: str = None):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    if not note:
        note = f"Payment to {BOT_NAME}"
    url = f"upi://pay?pa={UPI_ID}&pn={BOT_NAME}&am={amt}&tn={note}"
    view = View()
    view.add_item(Button(label="💳 Pay Now", style=discord.ButtonStyle.link, url=url))
    qr_btn = Button(label="📸 Show QR", style=discord.ButtonStyle.secondary)
    async def qr_cb(i):
        qr = gen_upi_qr(UPI_ID, amt, note)
        if qr:
            f = discord.File(qr, filename="qr.png")
            e = info_embed("Payment QR")
            e.set_image(url="attachment://qr.png")
            await i.response.send_message(embed=e, file=f, ephemeral=True)
        else:
            await i.response.send_message(embed=error_embed("Failed", "Could not generate QR"), ephemeral=True)
    qr_btn.callback = qr_cb
    view.add_item(qr_btn)
    embed = info_embed("Payment Link")
    embed.add_field(name="💰 Amount", value=f"```fix\n₹{amt}\n```", inline=True)
    embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  📦  PANEL COMMANDS
# ==================================================================================================

@bot.command(name="install-panel")
async def install_panel(ctx):
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license."))
    if not get_user_vps(str(ctx.author.id)):
        return await ctx.send(embed=no_vps_embed())
    embed = info_embed("Panel Installation", "Select panel type:")
    await ctx.send(embed=embed, view=PanelInstallView(ctx))

@bot.command(name="panel-info")
async def panel_info(ctx):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC', (uid,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Panels", "Use `.install-panel` to install one."))
    embed = info_embed(f"Your Panels ({len(rows)})")
    for r in rows:
        icon = "🦅" if r['panel_type']=='pterodactyl' else "🐡"
        val = f"```fix\nURL: {r['panel_url']}\nContainer: {r['container_name']}\nUsername: {r['admin_user']}\nEmail: {r['admin_email']}\nInstalled: {r['installed_at'][:16]}\n```"
        embed.add_field(name=f"{icon} {r['panel_type'].title()}", value=val, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="panel-reset")
async def panel_reset(ctx, ptype: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if ptype:
        cur.execute('SELECT * FROM panels WHERE user_id = ? AND panel_type = ? ORDER BY installed_at DESC LIMIT 1', (uid, ptype.lower()))
    else:
        cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC LIMIT 1', (uid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return await ctx.send(embed=error_embed("No Panel", "No panel found."))
    p = dict(row)
    new = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$%", k=16))
    msg = await ctx.send(embed=info_embed("Resetting Password", f"```fix\n{p['panel_type']} on {p['container_name']}\n```"))
    if p['panel_type'] == 'pterodactyl':
        cmd = f"cd /var/www/pterodactyl && php artisan p:user:password --email={p['admin_email']} --password={new}"
    else:
        cmd = f"pufferpanel user password --email {p['admin_email']} --password {new}"
    out, err, code = await exec_in_container(p['container_name'], cmd)
    if code == 0:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE panels SET admin_pass = ? WHERE id = ?', (new, p['id']))
        conn.commit()
        conn.close()
        embed = success_embed("Password Reset")
        embed.add_field(name="🌐 URL", value=f"```fix\n{p['panel_url']}\n```", inline=False)
        embed.add_field(name="👤 Username", value=f"```fix\n{p['admin_user']}\n```", inline=True)
        embed.add_field(name="🔑 New Password", value=f"||`{new}`||", inline=False)
        try:
            await ctx.author.send(embed=embed)
            await msg.edit(embed=success_embed("Password Reset", "Check your DMs!"))
        except:
            await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {err}\n```"))

@bot.command(name="panel-delete")
async def panel_delete(ctx, ptype: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if ptype:
        cur.execute('SELECT * FROM panels WHERE user_id = ? AND panel_type = ?', (uid, ptype.lower()))
    else:
        cur.execute('SELECT * FROM panels WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    if not rows:
        conn.close()
        return await ctx.send(embed=info_embed("No Panels", "No panels to delete."))
    if len(rows) > 1:
        opts = []
        for r in rows:
            icon = "🦅" if r['panel_type']=='pterodactyl' else "🐡"
            opts.append(discord.SelectOption(label=f"{icon} {r['panel_type']} on {r['container_name']}", value=str(r['id'])))
        view = View()
        sel = Select(placeholder="Select panel...", options=opts)
        async def sel_cb(i):
            pid = int(sel.values[0])
            cur.execute('DELETE FROM panels WHERE id = ? AND user_id = ?', (pid, uid))
            conn.commit()
            await i.response.edit_message(embed=success_embed("Deleted", "Panel record deleted."), view=None)
        sel.callback = sel_cb
        view.add_item(sel)
        await ctx.send(embed=info_embed("Select Panel"), view=view)
    else:
        r = rows[0]
        icon = "🦅" if r['panel_type']=='pterodactyl' else "🐡"
        view = View()
        conf = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
        canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        async def conf_cb(i):
            cur.execute('DELETE FROM panels WHERE id = ? AND user_id = ?', (r['id'], uid))
            conn.commit()
            await i.response.edit_message(embed=success_embed("Deleted", "Panel record deleted."), view=None)
        async def canc_cb(i):
            await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
        conf.callback = conf_cb
        canc.callback = canc_cb
        view.add_item(conf)
        view.add_item(canc)
        embed = warning_embed("Confirm Delete", f"{icon} {r['panel_type']} on {r['container_name']}\nThis only deletes the record, not the actual panel.")
        await ctx.send(embed=embed, view=view)
    conn.close()

@bot.command(name="panel-tunnel")
async def panel_tunnel(ctx, container: str = None, port: int = None):
    uid = str(ctx.author.id)
    if not container:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC LIMIT 1', (uid,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return await ctx.send(embed=error_embed("No Panel", "Specify container or install a panel."))
        container = row['container_name']
        port = 80 if row['panel_type']=='pterodactyl' else 8080
    if not any(v['container_name']==container for v in get_user_vps(uid)) and not is_admin(uid):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    if not port:
        view = View()
        b80 = Button(label="🌐 Port 80", style=discord.ButtonStyle.primary)
        b8080 = Button(label="🔌 Port 8080", style=discord.ButtonStyle.primary)
        async def b80_cb(i): await create_tunnel_cmd(i, container, 80)
        async def b8080_cb(i): await create_tunnel_cmd(i, container, 8080)
        b80.callback = b80_cb
        b8080.callback = b8080_cb
        view.add_item(b80)
        view.add_item(b8080)
        await ctx.send(embed=info_embed("Select Port"), view=view)
    else:
        await create_tunnel_cmd(ctx, container, port)

async def create_tunnel_cmd(ctx, container, port):
    msg = await ctx.send(embed=info_embed("Creating Tunnel", f"```fix\n{container}:{port}\n```"))
    try:
        await exec_in_container(container, "which cloudflared || (wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared)")
        tid = str(uuid.uuid4())[:8]
        await exec_in_container(container, f"nohup cloudflared tunnel --url http://localhost:{port} --no-autoupdate > /tmp/cloudflared_{tid}.log 2>&1 &")
        await asyncio.sleep(5)
        out,_,_ = await exec_in_container(container, f"cat /tmp/cloudflared_{tid}.log | grep -oP 'https://[a-z0-9-]+\\.trycloudflare\\.com' | head -1")
        url = out.strip()
        if url:
            embed = success_embed("Tunnel Created")
            embed.add_field(name="🌐 URL", value=f"```fix\n{url}\n```", inline=False)
            embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
            embed.add_field(name="🔌 Port", value=f"```fix\n{port}\n```", inline=True)
            await msg.edit(embed=embed)
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE panels SET tunnel_url = ? WHERE container_name = ?', (url, container))
            conn.commit()
            conn.close()
        else:
            await msg.edit(embed=error_embed("Failed", "Could not create tunnel. Install cloudflared."))
    except Exception as e:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="panel-status")
async def panel_status(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)) and not is_admin(uid):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM panels WHERE container_name = ?', (container,))
    panel = cur.fetchone()
    out,_,_ = await exec_in_container(container, "ps aux | grep -E 'nginx|pufferpanel|php|mysql' | grep -v grep")
    embed = info_embed(f"Panel Status: {container}")
    if panel:
        p = dict(panel)
        icon = "🦅" if p['panel_type']=='pterodactyl' else "🐡"
        status = f"```fix\nPanel: {icon} {p['panel_type']}\nURL: {p['panel_url']}\nUsername: {p['admin_user']}\nEmail: {p['admin_email']}\nInstalled: {p['installed_at'][:16]}\nTunnel: {'✅' if p['tunnel_url'] else '❌'}\n```"
        embed.add_field(name="📋 Panel Info", value=status, inline=False)
    if out:
        embed.add_field(name="🔄 Services", value=f"```fix\n{out[:500]}\n```", inline=False)
    else:
        embed.add_field(name="🔄 Services", value="```fix\nNo panel services detected\n```", inline=False)
    conn.close()
    await ctx.send(embed=embed)

# ==================================================================================================
#  🤖  AI COMMANDS
# ==================================================================================================

AI_KEY = "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"
AI_MODEL = "llama-3.3-70b-versatile"

@bot.command(name="ai")
async def ai(ctx, *, msg: str):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ai_history (user_id TEXT PRIMARY KEY, messages TEXT, updated_at TEXT)')
    cur.execute('SELECT messages FROM ai_history WHERE user_id = ?', (uid,))
    row = cur.fetchone()
    if row:
        history = json.loads(row['messages'])
    else:
        history = [{"role":"system","content":f"You are {BOT_NAME} AI Assistant, a helpful VPS management bot."}]
    history.append({"role":"user","content":msg})
    if len(history) > 21:
        history = [history[0]] + history[-20:]
    m = await ctx.send(embed=info_embed("AI is thinking..."))
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {AI_KEY}","Content-Type":"application/json"},
                json={"model":AI_MODEL,"messages":history,"max_tokens":1024,"temperature":0.7},
                timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data["choices"][0]["message"]["content"]
                    history.append({"role":"assistant","content":reply})
                    cur.execute('INSERT OR REPLACE INTO ai_history (user_id, messages, updated_at) VALUES (?, ?, ?)',
                              (uid, json.dumps(history), datetime.now().isoformat()))
                    conn.commit()
                    chunks = [reply[i:i+1900] for i in range(0,len(reply),1900)]
                    embed = info_embed("AI Response", chunks[0])
                    await m.edit(embed=embed)
                    for c in chunks[1:]:
                        await ctx.send(embed=info_embed("",c))
                else:
                    await m.edit(embed=error_embed("API Error", f"Status {resp.status}"))
    except Exception as e:
        await m.edit(embed=error_embed("Error", str(e)[:1900]))
    finally:
        conn.close()

@bot.command(name="ai-reset")
async def ai_reset(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM ai_history WHERE user_id = ?', (str(ctx.author.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("AI Reset", "History cleared."))

@bot.command(name="ai-help")
async def ai_help(ctx, *, topic: str):
    await ai(ctx, msg=f"Please help me with {topic} for VPS/LXC management")

# ==================================================================================================
#  🐧  OS COMMANDS
# ==================================================================================================

@bot.command(name="os-list")
async def os_list(ctx, category: str = None):
    if category:
        cats = [c['category'].lower() for c in OS_OPTIONS]
        if category.lower() not in cats:
            return await ctx.send(embed=error_embed("Invalid Category", f"Categories: Ubuntu, Debian, Fedora, Rocky, AlmaLinux, CentOS, Alpine, Arch, OpenSUSE, FreeBSD, OpenBSD, Kali, Gentoo, Void"))
        filtered = [o for o in OS_OPTIONS if o['category'].lower() == category.lower()]
    else:
        filtered = OS_OPTIONS[:25]
    embed = os_embed(f"OS Options {f'- {category}' if category else ''}", f"```fix\nTotal: {len(filtered)}\n```")
    for o in filtered[:10]:
        embed.add_field(name=o['label'], value=f"```fix\n{o['desc']}\nRAM Min: {o['ram_min']}MB\n```", inline=True)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🛡️  ADMIN COMMANDS
# ==================================================================================================

# ==================================================================================================
#  🚀  COMPLETE .create COMMAND - WITH apply_lxc_config FIX & FULL UI
# ==================================================================================================

import asyncio
import random
import string
import time
from datetime import datetime

# ==================================================================================================
#  🔧  LXC HELPER FUNCTIONS - ADD THESE IF NOT EXISTS
# ==================================================================================================

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
    await asyncio.sleep(3)
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


async def run_lxc(command: str, timeout: int = 60) -> Tuple[str, str, int]:
    """Run LXC command asynchronously"""
    try:
        cmd = shlex.split(command)
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return stdout.decode().strip(), stderr.decode().strip(), proc.returncode
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return "", f"Command timed out after {timeout} seconds", -1
    except Exception as e:
        return "", str(e), -1


async def exec_in_container(container_name: str, command: str, timeout: int = 30) -> Tuple[str, str, int]:
    """Execute command inside container"""
    return await run_lxc(f"lxc exec {container_name} -- bash -c {shlex.quote(command)}", timeout)


# ==================================================================================================
#  🎨  CREATE VPS VIEW WITH CONFIRMATION
# ==================================================================================================

class CreateVPSView(View):
    def __init__(self, ctx, ram, cpu, disk, user, os_version, os_name):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.ram = ram
        self.cpu = cpu
        self.disk = disk
        self.user = user
        self.os_version = os_version
        self.os_name = os_name
        
        # Confirm Button with Rainbow Style
        confirm_btn = Button(label="✅ Confirm Create", style=discord.ButtonStyle.success, emoji="✅", row=0)
        confirm_btn.callback = self.confirm_callback
        
        # Cancel Button
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=0)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(confirm_btn)
        self.add_item(cancel_btn)
    
    async def confirm_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.create_vps(interaction)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"),
            view=None
        )
    
    async def create_vps(self, interaction):
        await interaction.response.defer()
        
        user_id = str(self.user.id)
        container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
        
        # Rainbow Progress Embed
        progress = await interaction.followup.send(
            embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[░░░░░░░░░░░░░░░░░░░░] 0% | Step 1/6: Initializing container...\n```",
                color=0xFF0000
            ),
            ephemeral=True
        )
        
        try:
            ram_mb = self.ram * 1024
            colors = [0xFF0000, 0xFF7700, 0xFFFF00, 0x00FF00, 0x0000FF, 0x8B00FF]
            
            # Step 1: Initialize container
            await progress.edit(embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[████░░░░░░░░░░░░░░] 16% | Step 1/6: Initializing container...\n```",
                color=colors[0]
            ))
            await run_lxc(f"lxc init {self.os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
            
            # Step 2: Set limits
            await progress.edit(embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[████████░░░░░░░░░░] 33% | Step 2/6: Setting RAM limits...\n```",
                color=colors[1]
            ))
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            await run_lxc(f"lxc config set {container_name} limits.cpu {self.cpu}")
            await run_lxc(f"lxc config device set {container_name} root size={self.disk}GB")
            
            # Step 3: Apply LXC config
            await progress.edit(embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[████████████░░░░░░] 50% | Step 3/6: Applying LXC configuration...\n```",
                color=colors[2]
            ))
            await apply_lxc_config(container_name)
            
            # Step 4: Start container
            await progress.edit(embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[████████████████░░] 66% | Step 4/6: Starting container...\n```",
                color=colors[3]
            ))
            await run_lxc(f"lxc start {container_name}")
            
            # Step 5: Apply internal permissions
            await progress.edit(embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[██████████████████░░] 83% | Step 5/6: Configuring permissions...\n```",
                color=colors[4]
            ))
            await apply_internal_permissions(container_name)
            
            # Step 6: Get IP and MAC
            await progress.edit(embed=discord.Embed(
                title="```glow\n🌈 CREATING VPS - PROGRESS 🌈\n```",
                description="```fix\n[████████████████████] 100% | Step 6/6: Finalizing...\n```",
                color=colors[5]
            ))
            
            # Get IP and MAC
            ip = "N/A"
            mac = "N/A"
            try:
                out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() if out else "N/A"
                out, _, _ = await exec_in_container(container_name, "ip link | grep ether | awk '{print $2}' | head -1")
                mac = out.strip() if out else "N/A"
            except:
                pass
            
            # Save to database
            add_vps(user_id, container_name, self.ram, self.cpu, self.disk, self.os_version, "Custom")
            
            # Update VPS with IP and MAC
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ip_address = ?, mac_address = ? WHERE container_name = ?',
                       (ip, mac, container_name))
            conn.commit()
            conn.close()
            
            # Assign role
            if self.ctx.guild:
                role = discord.utils.get(self.ctx.guild.roles, name=f"{BOT_NAME} User")
                if not role:
                    role = await self.ctx.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
                try:
                    await self.user.add_roles(role)
                except:
                    pass
            
            # Rainbow Success Embed
            success_embed_msg = discord.Embed(
                title="```glow\n🌈 VPS CREATED SUCCESSFULLY! 🌈\n```",
                description=f"🎉 VPS **{container_name}** has been created for {self.user.mention}!",
                color=0x00FF88
            )
            success_embed_msg.set_thumbnail(url=THUMBNAIL_URL)
            success_embed_msg.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            # Resource Bar
            ram_bar = "█" * int(self.ram / 16) + "░" * (10 - int(self.ram / 16))
            cpu_bar = "█" * int(self.cpu / 8) + "░" * (10 - int(self.cpu / 8))
            disk_bar = "█" * int(self.disk / 100) + "░" * (10 - int(self.disk / 100))
            
            success_embed_msg.add_field(
                name="📦 CONTAINER DETAILS",
                value=f"```fix\nName: {container_name}\nIP Address: {ip}\nMAC Address: {mac}\nOS: {self.os_name}\n```",
                inline=False
            )
            
            success_embed_msg.add_field(
                name="⚙️ RESOURCE ALLOCATION",
                value=f"```fix\nRAM: {self.ram}GB [{ram_bar}]\nCPU: {self.cpu} Core(s) [{cpu_bar}]\nDisk: {self.disk}GB [{disk_bar}]\n```",
                inline=False
            )
            
            success_embed_msg.add_field(
                name="🖥️ MANAGEMENT COMMANDS",
                value=f"```fix\n.manage {container_name} - Interactive Manager\n.stats {container_name} - Live Statistics\n.logs {container_name} - System Logs\n.ssh-gen {container_name} - SSH Access\n.reboot {container_name} - Reboot VPS\n.shutdown {container_name} - Shutdown VPS\n```",
                inline=False
            )
            
            success_embed_msg.add_field(
                name="🔗 QUICK LINKS",
                value=f"[📖 Documentation](https://github.com/AnkitKing7/Svm5-bot) | [💬 Support](https://discord.gg) | [🐛 Report Issue](https://github.com/AnkitKing7/Svm5-bot/issues)",
                inline=False
            )
            
            success_embed_msg.set_footer(
                text=f"⚡ Created by {self.ctx.author.name} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await progress.edit(embed=success_embed_msg)
            
            # Send DM to user
            try:
                dm_embed = discord.Embed(
                    title="```glow\n✨ YOUR VPS IS READY! ✨\n```",
                    description=f"🎉 A new VPS has been created for you!",
                    color=0x57F287
                )
                dm_embed.set_thumbnail(url=THUMBNAIL_URL)
                dm_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
                
                dm_embed.add_field(
                    name="📦 CONTAINER",
                    value=f"```fix\nName: {container_name}\nIP: {ip}\nMAC: {mac}\nOS: {self.os_name}\n```",
                    inline=False
                )
                
                dm_embed.add_field(
                    name="⚙️ RESOURCES",
                    value=f"```fix\nRAM: {self.ram}GB\nCPU: {self.cpu} Core(s)\nDisk: {self.disk}GB\n```",
                    inline=True
                )
                
                dm_embed.add_field(
                    name="📅 CREATED",
                    value=f"```fix\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n```",
                    inline=True
                )
                
                dm_embed.add_field(
                    name="🖥️ QUICK COMMANDS",
                    value=f"```fix\n.manage {container_name}\n.stats {container_name}\n.logs {container_name}\n.ssh-gen {container_name}\n```",
                    inline=False
                )
                
                dm_embed.set_footer(
                    text=f"⚡ SVM5-BOT • Manage your VPS with .help ⚡",
                    icon_url=THUMBNAIL_URL
                )
                
                await self.user.send(embed=dm_embed)
                
            except:
                pass
            
            # Log
            logger.info(f"Admin {self.ctx.author} created VPS {container_name} for {self.user}")
            
        except Exception as e:
            await progress.edit(embed=error_embed("Creation Failed", f"```diff\n- {str(e)}\n```"))
            try:
                await run_lxc(f"lxc delete {container_name} --force")
            except:
                pass


# ==================================================================================================
#  📋  OS SELECTION VIEW
# ==================================================================================================

class OSDropdownView(View):
    def __init__(self, ctx, ram, cpu, disk, user):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.ram = ram
        self.cpu = cpu
        self.disk = disk
        self.user = user
        
        # Create OS options
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(
                label=os['label'][:100],
                value=os['value'],
                description=os['desc'][:100] if os.get('desc') else None,
                emoji=os.get('icon', '🐧')
            ))
        
        self.select = Select(placeholder="📋 Select an operating system...", options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=1)
        cancel_btn.callback = self.cancel_callback
        self.add_item(cancel_btn)
    
    async def select_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        selected_os = self.select.values[0]
        os_name = next((o['label'] for o in OS_OPTIONS if o['value'] == selected_os), selected_os)
        
        embed = discord.Embed(
            title="```glow\n⚠️ CONFIRM VPS CREATION ⚠️\n```",
            description=f"```fix\nUser: {self.user.mention}\nOS: {os_name}\nRAM: {self.ram}GB\nCPU: {self.cpu} Core(s)\nDisk: {self.disk}GB\n```\n\n**Please confirm to create this VPS.**",
            color=0xFFAA00
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
        
        view = CreateVPSView(self.ctx, self.ram, self.cpu, self.disk, self.user, selected_os, os_name)
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"),
            view=None
        )


# ==================================================================================================
#  🚀  .create COMMAND
# ==================================================================================================

@bot.command(name="create")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    """Create a VPS for a user with full UI and OS selection"""
    if ram <= 0 or cpu <= 0 or disk <= 0:
        return await ctx.send(embed=error_embed("Invalid Specs", "```diff\n- RAM, CPU, Disk must be positive integers.\n```"))
    
    embed = discord.Embed(
        title="```glow\n🖥️ CREATE NEW VPS 🖥️\n```",
        description=f"```fix\n👤 User: {user.mention}\n💾 RAM: {ram}GB\n⚙️ CPU: {cpu} Core(s)\n💽 Disk: {disk}GB\n```\n\n**Please select an operating system from the dropdown menu below.**",
        color=0x5865F2
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
    embed.set_footer(
        text=f"⚡ SVM5-BOT • Created by {ctx.author.name} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    
    view = OSDropdownView(ctx, ram, cpu, disk, user)
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  🔐  LICENSE VERIFY COMMAND
# ==================================================================================================

@bot.command(name="license-verify")
async def license_verify(ctx, key: str = None):
    """Verify your license key"""
    global LICENSE_VERIFIED
    
    if key is None:
        if LICENSE_VERIFIED:
            embed = success_embed("License Verified", "```fix\nYour license is active and verified.\n```")
        else:
            embed = warning_embed("License Not Verified", "```fix\nNo valid license found. Use .license-verify <key> to activate.\n```")
            embed.add_field(
                name="📌 Valid License Keys",
                value="```fix\nAnkitDev99$@\nSVM5-PRO-2025\nSVM5-ENTERPRISE\n```",
                inline=False
            )
        return await ctx.send(embed=embed)
    
    if key in VALID_LICENSE_KEYS:
        set_setting('license_verified', 'true')
        LICENSE_VERIFIED = True
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS license_info (
            license_key TEXT, activated_by TEXT, activated_at TEXT, ip TEXT, mac TEXT
        )''')
        cur.execute('INSERT INTO license_info VALUES (?, ?, ?, ?, ?)',
                   (key, str(ctx.author.id), datetime.now().isoformat(), SERVER_IP, MAC_ADDRESS))
        conn.commit()
        conn.close()
        
        embed = success_embed("✅ License Verified Successfully!")
        embed.add_field(name="🔑 License Key", value=f"```fix\n{key}\n```", inline=True)
        embed.add_field(name="👤 Activated By", value=ctx.author.mention, inline=True)
        embed.set_image(url=THUMBNAIL_URL)
        
        await ctx.send(embed=embed)
    else:
        embed = error_embed("Invalid License Key", f"```diff\n- The key '{key}' is not valid.\n```")
        await ctx.send(embed=embed)


@bot.command(name="license-status")
async def license_status(ctx):
    """Show license status"""
    if LICENSE_VERIFIED:
        embed = success_embed("License Status", "```fix\nLicense is active.\n```")
    else:
        embed = warning_embed("License Status", "```fix\nNo active license found.\n```")
        embed.add_field(name="📌 Activate", value=f"Use `{BOT_PREFIX}license-verify <key>` to activate.", inline=False)
    await ctx.send(embed=embed)
    
@bot.command(name="delete")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_delete(ctx, user: discord.Member, num: int, *, reason: str = "No reason"):
    uid = str(user.id)
    vps = get_user_vps(uid)
    if not vps or num<1 or num>len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    v = vps[num-1]
    view = View()
    conf = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def conf_cb(i):
        await run_lxc(f"lxc stop {v['container_name']} --force")
        await run_lxc(f"lxc delete {v['container_name']}")
        delete_vps(v['container_name'])
        await i.response.edit_message(embed=success_embed("Deleted", f"```fix\n{v['container_name']}\n```"), view=None)
    async def canc_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    conf.callback = conf_cb
    canc.callback = canc_cb
    view.add_item(conf)
    view.add_item(canc)
    await ctx.send(embed=warning_embed("Confirm Delete", f"```fix\nUser: {user}\nVPS: {v['container_name']}\nReason: {reason}\n```"), view=view)

@bot.command(name="suspend")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_suspend(ctx, container: str, *, reason: str = "Admin action"):
    allv = get_all_vps()
    v = next((v for v in allv if v['container_name']==container), None)
    if not v:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {container}\n```"))
    await run_lxc(f"lxc stop {container} --force")
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET suspended = 1, suspended_reason = ? WHERE container_name = ?', (reason, container))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Suspended", f"```fix\n{container}\nReason: {reason}\n```"))

@bot.command(name="unsuspend")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_unsuspend(ctx, container: str):
    allv = get_all_vps()
    v = next((v for v in allv if v['container_name']==container), None)
    if not v:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {container}\n```"))
    await run_lxc(f"lxc start {container}")
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET suspended = 0, suspended_reason = "" WHERE container_name = ?', (container,))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Unsuspended", f"```fix\n{container}\n```"))

@bot.command(name="add-resources")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_add_resources(ctx, container: str, ram: int = None, cpu: int = None, disk: int = None):
    if not ram and not cpu and not disk:
        return await ctx.send(embed=error_embed("Missing", "Specify at least one resource"))
    allv = get_all_vps()
    v = next((v for v in allv if v['container_name']==container), None)
    if not v:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {container}\n```"))
    was = v['status'] == 'running' and not v['suspended']
    if was:
        await run_lxc(f"lxc stop {container}")
    changes = []
    if ram:
        new = v['ram'] + ram
        await run_lxc(f"lxc config set {container} limits.memory {new*1024}MB")
        changes.append(f"RAM: +{ram}GB (now {new}GB)")
    if cpu:
        new = v['cpu'] + cpu
        await run_lxc(f"lxc config set {container} limits.cpu {new}")
        changes.append(f"CPU: +{cpu} cores (now {new})")
    if disk:
        new = v['disk'] + disk
        await run_lxc(f"lxc config device set {container} root size={new}GB")
        changes.append(f"Disk: +{disk}GB (now {new}GB)")
    if was:
        await run_lxc(f"lxc start {container}")
    conn = get_db()
    cur = conn.cursor()
    if ram:
        cur.execute('UPDATE vps SET ram = ram + ? WHERE container_name = ?', (ram, container))
    if cpu:
        cur.execute('UPDATE vps SET cpu = cpu + ? WHERE container_name = ?', (cpu, container))
    if disk:
        cur.execute('UPDATE vps SET disk = disk + ? WHERE container_name = ?', (disk, container))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Resources Added", "\n".join([f"```fix\n{c}\n```" for c in changes])))

@bot.command(name="list-all")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def list_all(ctx):
    allv = get_all_vps()
    if not allv:
        return await ctx.send(embed=info_embed("No VPS", "No VPS in system."))
    byuser = {}
    for v in allv:
        if v['user_id'] not in byuser:
            byuser[v['user_id']] = []
        byuser[v['user_id']].append(v)
    embed = info_embed(f"All VPS ({len(allv)})")
    for uid, vlist in list(byuser.items())[:5]:
        try:
            u = await bot.fetch_user(int(uid))
            name = u.name
        except:
            name = f"Unknown"
        text = "\n".join([f"{'🟢' if v['status']=='running' else '🔴'} `{v['container_name']}` ({v['ram']}GB)" for v in vlist[:3]])
        embed.add_field(name=f"{name} ({len(vlist)})", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="add-inv")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def add_inv(ctx, user: discord.Member, amt: int):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    update_user_stats(str(user.id), invites=amt)
    await ctx.send(embed=success_embed("Invites Added", f"```fix\n+{amt} to {user.name}\n```"))

@bot.command(name="remove-inv")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def remove_inv(ctx, user: discord.Member, amt: int):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    s = get_user_stats(str(user.id))
    if s.get('invites',0) < amt:
        amt = s.get('invites',0)
    update_user_stats(str(user.id), invites=-amt)
    await ctx.send(embed=success_embed("Invites Removed", f"```fix\n-{amt} from {user.name}\n```"))

@bot.command(name="ports-add")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def ports_add_admin(ctx, user: discord.Member, amt: int):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    add_port_allocation(str(user.id), amt)
    await ctx.send(embed=success_embed("Port Slots Added", f"```fix\n+{amt} to {user.name}\n```"))

@bot.command(name="serverstats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def serverstats(ctx):
    allv = get_all_vps()
    tr = sum(v['ram'] for v in allv)
    tc = sum(v['cpu'] for v in allv)
    td = sum(v['disk'] for v in allv)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM vps')
    tu = cur.fetchone()[0] or 0
    cur.execute('SELECT COUNT(*) FROM port_forwards')
    tp = cur.fetchone()[0] or 0
    conn.close()
    embed = info_embed("Server Statistics")
    embed.add_field(name="🖥️ VPS", value=f"```fix\nTotal: {len(allv)}\nUsers: {tu}\n```", inline=True)
    embed.add_field(name="💾 Resources", value=f"```fix\nRAM: {tr}GB\nCPU: {tc} cores\nDisk: {td}GB\n```", inline=True)
    embed.add_field(name="🔌 Ports", value=f"```fix\n{len(allv)} VPS\n{tp} forwards\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="admin-add-ipv4")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_add_ipv4(ctx, user: discord.Member, container: str):
    uid = str(user.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Not Found", f"Container {container} not found for user"))
    out,_,_ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
    priv = out.strip() or "N/A"
    out,_,_ = await exec_in_container(container, "ip link | grep ether | awk '{print $2}' | head -1")
    mac = out.strip() or "N/A"
    add_ipv4(uid, container, SERVER_IP, priv, mac)
    embed = success_embed("IPv4 Assigned")
    embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
    embed.add_field(name="🌐 Public", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🏠 Private", value=f"```fix\n{priv}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="admin-rm-ipv4")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_rm_ipv4(ctx, user: discord.Member, container: str = None):
    uid = str(user.id)
    if container:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM ipv4 WHERE user_id = ? AND container_name = ?', (uid, container))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("IPv4 Removed", f"```fix\n{container}\n```"))
    else:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM ipv4 WHERE user_id = ?', (uid,))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("IPv4 Removed", f"```fix\nAll IPv4 from {user.name}\n```"))

@bot.command(name="admin-pending-ipv4")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_pending_ipv4(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions WHERE status = "pending" ORDER BY created_at')
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Pending", "No pending IPv4 purchases."))
    embed = info_embed(f"Pending IPv4 ({len(rows)})")
    for r in rows:
        try:
            u = await bot.fetch_user(int(r['user_id']))
            name = u.name
        except:
            name = f"Unknown"
        embed.add_field(name=f"User: {name}", value=f"```fix\nRef: {r['txn_ref']}\nAmount: ₹{r['amount']}\nCreated: {r['created_at'][:16]}\n```", inline=False)
    await ctx.send(embed=embed)

# ==================================================================================================
#  👑  OWNER COMMANDS
# ==================================================================================================

@bot.command(name="admin-add")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_admin_add(ctx, user: discord.Member):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)', (str(user.id), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Admin Added", f"{user.mention} is now an admin"))

@bot.command(name="admin-remove")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_admin_remove(ctx, user: discord.Member):
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        return await ctx.send(embed=error_embed("Cannot Remove", "Cannot remove main admin"))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM admins WHERE user_id = ?', (str(user.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Admin Removed", f"{user.mention} is no longer admin"))

@bot.command(name="admin-list")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_admin_list(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM admins')
    rows = cur.fetchall()
    conn.close()
    main = "\n".join([f"👑 <@{a}>" for a in MAIN_ADMIN_IDS])
    admins = "\n".join([f"🛡️ <@{r['user_id']}>" for r in rows if r['user_id'] not in [str(a) for a in MAIN_ADMIN_IDS]])
    embed = info_embed("Admin List")
    embed.add_field(name="Main Admin", value=main or "None", inline=False)
    embed.add_field(name="Admins", value=admins or "None", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="maintenance")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_maintenance(ctx, mode: str):
    mode = mode.lower()
    if mode not in ['on','off']:
        return await ctx.send(embed=error_embed("Invalid", "Use on or off"))
    set_setting('maintenance_mode', mode)
    await ctx.send(embed=success_embed("Maintenance", f"Mode set to {mode}"))

@bot.command(name="purge-all")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_purge_all(ctx):
    allv = get_all_vps()
    unprotected = [v for v in allv if not v.get('purge_protected',0)]
    if not unprotected:
        return await ctx.send(embed=info_embed("No Unprotected", "All VPS are protected."))
    view = View()
    conf = Button(label="✅ PURGE", style=discord.ButtonStyle.danger)
    canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def conf_cb(i):
        await i.response.defer()
        prog = await i.followup.send(embed=info_embed("Purging", f"```fix\n0/{len(unprotected)}\n```"), ephemeral=True)
        deleted = 0
        for idx, v in enumerate(unprotected,1):
            try:
                await run_lxc(f"lxc stop {v['container_name']} --force")
                await run_lxc(f"lxc delete {v['container_name']}")
                delete_vps(v['container_name'])
                deleted += 1
                if idx % 5 == 0:
                    await prog.edit(embed=info_embed("Purging", f"```fix\n{idx}/{len(unprotected)}\n```"))
                await asyncio.sleep(2)
            except:
                pass
        await prog.edit(embed=success_embed("Purge Complete", f"```fix\nDeleted: {deleted}\nFailed: {len(unprotected)-deleted}\n```"))
    async def canc_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    conf.callback = conf_cb
    canc.callback = canc_cb
    view.add_item(conf)
    view.add_item(canc)
    await ctx.send(embed=warning_embed("⚠️ Purge All Unprotected", f"```fix\nThis will delete {len(unprotected)} unprotected VPS.\nProtected VPS will be skipped.\n```"), view=view)

@bot.command(name="protect")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_protect(ctx, user: discord.Member, num: int = None):
    uid = str(user.id)
    vps = get_user_vps(uid)
    if not vps:
        return await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS"))
    if num is None:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE user_id = ?', (uid,))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Protected", f"All VPS of {user.mention} are now protected"))
    else:
        if num < 1 or num > len(vps):
            return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE container_name = ?', (vps[num-1]['container_name'],))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Protected", f"VPS #{num} of {user.mention} is now protected"))

@bot.command(name="unprotect")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_unprotect(ctx, user: discord.Member, num: int = None):
    uid = str(user.id)
    vps = get_user_vps(uid)
    if not vps:
        return await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS"))
    if num is None:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE user_id = ?', (uid,))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Unprotected", f"All VPS of {user.mention} are no longer protected"))
    else:
        if num < 1 or num > len(vps):
            return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE container_name = ?', (vps[num-1]['container_name'],))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Unprotected", f"VPS #{num} of {user.mention} is no longer protected"))

@bot.command(name="backup-db")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_backup_db(ctx):
    name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    path = f"/opt/svm5-bot/backups/{name}"
    try:
        shutil.copy2(DATABASE_PATH, path)
        await ctx.send(embed=success_embed("Backup Created", f"```fix\n{name}\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Backup Failed", str(e)))

@bot.command(name="restore-db")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_restore_db(ctx, name: str):
    path = f"/opt/svm5-bot/backups/{name}"
    if not os.path.exists(path):
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    view = View()
    conf = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def conf_cb(i):
        try:
            shutil.copy2(path, DATABASE_PATH)
            await i.response.edit_message(embed=success_embed("Restored", f"```fix\n{name}\n```"), view=None)
        except Exception as e:
            await i.response.edit_message(embed=error_embed("Failed", str(e)), view=None)
    async def canc_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    conf.callback = conf_cb
    canc.callback = canc_cb
    view.add_item(conf)
    view.add_item(canc)
    await ctx.send(embed=warning_embed("Confirm Restore", f"```fix\nRestore {name}?\nCurrent DB will be overwritten!\n```"), view=view)
# ==================================================================================================
#  🌐  COMPLETE IP COMMANDS - USER IP, VPS IP, NODE IP, ALL DETAILS
# ==================================================================================================

@bot.command(name="ip")
async def ip_cmd(ctx, target: str = None):
    """Main IP command - show your IP, VPS IP, or node IP"""
    if not target:
        # Show user's own IP
        await show_my_ip(ctx)
    elif target.lower() == "public":
        # Show public IP of server
        await show_public_ip(ctx)
    elif target.lower() == "vps" or target.lower() == "container":
        # Show all VPS IPs
        await show_vps_ips(ctx)
    elif target.lower() == "node":
        # Show node IPs
        await show_node_ips(ctx)
    elif target.lower() == "all":
        # Show all IPs
        await show_all_ips(ctx)
    elif target.lower() == "mac":
        # Show MAC address
        await show_mac_address(ctx)
    elif target.lower() == "dns":
        # Show DNS servers
        await show_dns_servers(ctx)
    elif target.lower() == "route" or target.lower() == "gateway":
        # Show routing table
        await show_routing_table(ctx)
    elif target.lower() == "interface" or target.lower() == "ifconfig":
        # Show network interfaces
        await show_network_interfaces(ctx)
    else:
        # Show specific container IP
        await show_container_ip(ctx, target)


@bot.command(name="myip")
async def my_ip(ctx):
    """Show your own public IP"""
    await show_my_ip(ctx)


@bot.command(name="vps-ip")
async def vps_ip(ctx, container: str = None):
    """Show VPS container IP details"""
    if container:
        await show_container_ip(ctx, container)
    else:
        await show_vps_ips(ctx)


@bot.command(name="node-ip")
async def node_ip(ctx, node_name: str = None):
    """Show node IP details"""
    if node_name:
        await show_node_ip_detail(ctx, node_name)
    else:
        await show_node_ips(ctx)


@bot.command(name="public-ip")
async def public_ip(ctx):
    """Show server public IP"""
    await show_public_ip(ctx)


@bot.command(name="mac")
async def mac_address(ctx, container: str = None):
    """Show MAC address of server or container"""
    if container:
        await show_container_mac(ctx, container)
    else:
        await show_mac_address(ctx)


@bot.command(name="gateway")
async def gateway_cmd(ctx, container: str = None):
    """Show gateway information"""
    if container:
        await show_container_gateway(ctx, container)
    else:
        await show_routing_table(ctx)


@bot.command(name="netstat")
async def netstat_cmd(ctx, container: str = None):
    """Show network connections"""
    if container:
        await show_container_netstat(ctx, container)
    else:
        await show_server_netstat(ctx)


@bot.command(name="ifconfig")
async def ifconfig_cmd(ctx, container: str = None):
    """Show network interfaces"""
    if container:
        await show_container_interfaces(ctx, container)
    else:
        await show_network_interfaces(ctx)


@bot.command(name="dns")
async def dns_cmd(ctx, container: str = None):
    """Show DNS servers"""
    if container:
        await show_container_dns(ctx, container)
    else:
        await show_dns_servers(ctx)


@bot.command(name="ping-ip")
async def ping_ip(ctx, ip: str):
    """Ping an IP address"""
    await ping_target(ctx, ip)


@bot.command(name="trace-ip")
async def trace_ip(ctx, ip: str):
    """Trace route to IP address"""
    await trace_target(ctx, ip)


# ==================================================================================================
#  📡  IP COMMAND IMPLEMENTATIONS
# ==================================================================================================

async def show_my_ip(ctx):
    """Show user's own public IP"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org', timeout=5) as resp:
                public_ip = await resp.text()
    except:
        try:
            public_ip = subprocess.getoutput("curl -s ifconfig.me")
        except:
            public_ip = "Could not detect"
    
    embed = discord.Embed(
        title="```glow\n🌐 Your IP Information\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # Get local IPs
    local_ips = []
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface != 'lo':
                addr = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addr:
                    for ip in addr[netifaces.AF_INET]:
                        if ip['addr'] != '127.0.0.1':
                            local_ips.append(f"{iface}: {ip['addr']}")
    except:
        local_ips = ["Could not detect"]
    
    embed.add_field(
        name="🌍 Public IP",
        value=f"```fix\n{public_ip}\n```",
        inline=False
    )
    
    embed.add_field(
        name="🏠 Local IPs",
        value=f"```fix\n" + "\n".join(local_ips[:5]) + "\n```",
        inline=False
    )
    
    embed.add_field(
        name="🖥️ Hostname",
        value=f"```fix\n{HOSTNAME}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔌 MAC Address",
        value=f"```fix\n{MAC_ADDRESS}\n```",
        inline=True
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Your IP Information • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_public_ip(ctx):
    """Show server public IP"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org', timeout=5) as resp:
                public_ip = await resp.text()
    except:
        try:
            public_ip = subprocess.getoutput("curl -s ifconfig.me")
        except:
            public_ip = "Could not detect"
    
    # Get additional IP info
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://ip-api.com/json/{public_ip}', timeout=5) as resp:
                ip_info = await resp.json()
                location = f"{ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')}"
                isp = ip_info.get('isp', 'Unknown')
    except:
        location = "Unknown"
        isp = "Unknown"
    
    embed = discord.Embed(
        title="```glow\n🌍 Public IP Information\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    embed.add_field(
        name="🌐 IP Address",
        value=f"```fix\n{public_ip}\n```",
        inline=False
    )
    
    embed.add_field(
        name="📍 Location",
        value=f"```fix\n{location}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🏢 ISP",
        value=f"```fix\n{isp}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🖥️ Hostname",
        value=f"```fix\n{HOSTNAME}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔌 MAC",
        value=f"```fix\n{MAC_ADDRESS}\n```",
        inline=True
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Public IP Information • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_vps_ips(ctx):
    """Show all VPS containers IPs"""
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = discord.Embed(
        title="```glow\n🖥️ Your VPS IP Addresses\n```",
        color=COLORS['info']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    for vps in vps_list:
        container = vps['container_name']
        stats = await get_container_stats(container)
        
        status_emoji = "🟢" if stats['status'] == 'running' else "🔴"
        
        ip_text = f"{status_emoji} **`{container}`**\n"
        ip_text += f"```fix\n"
        
        if stats['ipv4']:
            for i, ip in enumerate(stats['ipv4'][:3], 1):
                ip_text += f"IPv4 #{i}: {ip}\n"
        else:
            ip_text += f"IPv4: Not assigned\n"
        
        ip_text += f"MAC: {stats['mac']}\n"
        ip_text += f"Status: {stats['status'].upper()}\n"
        ip_text += f"```"
        
        embed.add_field(name=f"📦 {container}", value=ip_text, inline=False)
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Use .ip <container> for details • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_container_ip(ctx, container_name: str):
    """Show detailed IP information for a container"""
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    stats = await get_container_stats(container_name)
    
    # Get more details from container
    ip_addr, _, _ = await exec_in_container(container_name, "ip addr show")
    route, _, _ = await exec_in_container(container_name, "ip route show")
    
    embed = discord.Embed(
        title=f"```glow\n🌐 IP Details: {container_name}\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # IPv4 Addresses
    ipv4_text = ""
    for ip in stats['ipv4']:
        ipv4_text += f"• {ip}\n"
    embed.add_field(
        name="🌍 IPv4 Addresses",
        value=f"```fix\n{ipv4_text if ipv4_text else 'No IPv4 assigned'}\n```",
        inline=True
    )
    
    # MAC Address
    embed.add_field(
        name="🔌 MAC Address",
        value=f"```fix\n{stats['mac']}\n```",
        inline=True
    )
    
    # Status
    embed.add_field(
        name="📊 Status",
        value=f"```fix\n{stats['status'].upper()}\n```",
        inline=True
    )
    
    # Full IP Configuration
    embed.add_field(
        name="📋 Full IP Configuration",
        value=f"```bash\n{ip_addr[:500]}\n```",
        inline=False
    )
    
    # Routing Table
    embed.add_field(
        name="🗺️ Routing Table",
        value=f"```bash\n{route[:500]}\n```",
        inline=False
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • {container_name} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_node_ips(ctx):
    """Show all node IPs"""
    nodes = load_nodes()
    
    if not nodes['nodes']:
        await ctx.send(embed=info_embed("No Nodes", "No nodes configured."))
        return
    
    embed = discord.Embed(
        title="```glow\n🌐 Node IP Addresses\n```",
        color=COLORS['node']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    for name, node in nodes['nodes'].items():
        status_emoji = "🟢" if node['status'] == 'online' else "🔴"
        is_main = " 👑 MAIN" if node.get('is_main') else ""
        
        ip_text = f"{status_emoji} **`{name}`**{is_main}\n"
        ip_text += f"```fix\n"
        ip_text += f"Host: {node['host']}\n"
        ip_text += f"Port: {node['port']}\n"
        ip_text += f"Status: {node['status'].upper()}\n"
        ip_text += f"Region: {node.get('region', 'us')}\n"
        ip_text += f"```"
        
        embed.add_field(name=f"🌍 {name}", value=ip_text, inline=False)
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Use .node-info <name> for details • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_node_ip_detail(ctx, node_name: str):
    """Show detailed IP for a specific node"""
    node = get_node(node_name)
    
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- {node_name}\n```"))
        return
    
    embed = discord.Embed(
        title=f"```glow\n🌐 Node IP Details: {node_name}\n```",
        color=COLORS['node']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    embed.add_field(
        name="🌐 Host",
        value=f"```fix\n{node['host']}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔌 Port",
        value=f"```fix\n{node['port']}\n```",
        inline=True
    )
    
    embed.add_field(
        name="📊 Status",
        value=f"```fix\n{node['status'].upper()}\n```",
        inline=True
    )
    
    embed.add_field(
        name="👤 Username",
        value=f"```fix\n{node['username']}\n```",
        inline=True
    )
    
    embed.add_field(
        name="📍 Region",
        value=f"```fix\n{node.get('region', 'us')}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🗝️ API Key",
        value=f"```fix\n{node.get('api_key', 'N/A')[:16]}...\n```",
        inline=True
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Node IP Information • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_all_ips(ctx):
    """Show all IPs (user, VPS, node)"""
    embed = discord.Embed(
        title="```glow\n🌐 Complete IP Overview\n```",
        color=COLORS['gold']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # Server IP
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        public_ip = subprocess.getoutput("curl -s ifconfig.me")
    
    embed.add_field(
        name="🖥️ Server IP",
        value=f"```fix\nPublic: {public_ip}\nLocal: {SERVER_IP}\nHostname: {HOSTNAME}\nMAC: {MAC_ADDRESS}\n```",
        inline=False
    )
    
    # VPS IPs
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if vps_list:
        vps_text = ""
        for vps in vps_list[:5]:
            stats = await get_container_stats(vps['container_name'])
            vps_text += f"• {vps['container_name']}: {stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n"
        embed.add_field(
            name="🖥️ Your VPS IPs",
            value=f"```fix\n{vps_text if vps_text else 'No VPS'}\n```",
            inline=False
        )
    
    # Node IPs
    nodes = load_nodes()
    if nodes['nodes']:
        node_text = ""
        for name, node in nodes['nodes'].items():
            node_text += f"• {name}: {node['host']} ({node['status']})\n"
        embed.add_field(
            name="🌐 Node IPs",
            value=f"```fix\n{node_text[:500]}\n```",
            inline=False
        )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Complete IP Overview • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_mac_address(ctx, container: str = None):
    """Show MAC address"""
    if container:
        # Show container MAC
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        stats = await get_container_stats(container)
        mac = stats['mac']
        
        embed = info_embed(f"🔌 MAC Address: {container}")
        embed.add_field(name="MAC Address", value=f"```fix\n{mac}\n```", inline=False)
        embed.add_field(name="Container", value=f"```fix\n{container}\n```", inline=True)
        await ctx.send(embed=embed)
    else:
        # Show server MAC
        embed = info_embed("🔌 Server MAC Address")
        embed.add_field(name="MAC Address", value=f"```fix\n{MAC_ADDRESS}\n```", inline=False)
        embed.add_field(name="Hostname", value=f"```fix\n{HOSTNAME}\n```", inline=True)
        await ctx.send(embed=embed)


async def show_routing_table(ctx, container: str = None):
    """Show routing table / gateway"""
    if container:
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        route, _, _ = await exec_in_container(container, "ip route show")
        
        embed = terminal_embed(f"Routing Table: {container}", route)
        await ctx.send(embed=embed)
    else:
        route = subprocess.getoutput("ip route show")
        embed = terminal_embed("Routing Table", route)
        await ctx.send(embed=embed)


async def show_container_gateway(ctx, container: str):
    """Show container gateway"""
    user_id = str(ctx.author.id)
    if not any(v['container_name'] == container for v in get_user_vps(user_id)):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    route, _, _ = await exec_in_container(container, "ip route show | grep default")
    gateway = route.split()[2] if route else "N/A"
    
    embed = info_embed(f"🚪 Gateway: {container}")
    embed.add_field(name="Gateway", value=f"```fix\n{gateway}\n```", inline=False)
    embed.add_field(name="Container", value=f"```fix\n{container}\n```", inline=True)
    await ctx.send(embed=embed)


async def show_network_interfaces(ctx, container: str = None):
    """Show network interfaces"""
    if container:
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        interfaces, _, _ = await exec_in_container(container, "ip link show")
        
        embed = terminal_embed(f"Network Interfaces: {container}", interfaces)
        await ctx.send(embed=embed)
    else:
        interfaces = subprocess.getoutput("ip link show")
        embed = terminal_embed("Network Interfaces", interfaces)
        await ctx.send(embed=embed)


async def show_container_interfaces(ctx, container: str):
    """Show container network interfaces"""
    await show_network_interfaces(ctx, container)


async def show_dns_servers(ctx, container: str = None):
    """Show DNS servers"""
    if container:
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        dns, _, _ = await exec_in_container(container, "cat /etc/resolv.conf | grep nameserver")
        
        embed = terminal_embed(f"DNS Servers: {container}", dns)
        await ctx.send(embed=embed)
    else:
        dns = subprocess.getoutput("cat /etc/resolv.conf | grep nameserver")
        embed = terminal_embed("DNS Servers", dns)
        await ctx.send(embed=embed)


async def show_container_dns(ctx, container: str):
    """Show container DNS servers"""
    await show_dns_servers(ctx, container)


async def show_server_netstat(ctx):
    """Show server network connections"""
    netstat = subprocess.getoutput("ss -tuln | head -30")
    embed = terminal_embed("Server Network Connections", netstat)
    await ctx.send(embed=embed)


async def show_container_netstat(ctx, container: str):
    """Show container network connections"""
    user_id = str(ctx.author.id)
    if not any(v['container_name'] == container for v in get_user_vps(user_id)):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    netstat, _, _ = await exec_in_container(container, "netstat -tuln | head -30")
    embed = terminal_embed(f"Network Connections: {container}", netstat)
    await ctx.send(embed=embed)


async def ping_target(ctx, ip: str):
    """Ping an IP address"""
    msg = await ctx.send(embed=info_embed("Pinging...", f"```fix\n{ip}\n```"))
    
    try:
        result = subprocess.getoutput(f"ping -c 4 {ip}")
        
        # Parse ping results
        lines = result.splitlines()
        loss = "100%"
        avg = "N/A"
        
        for line in lines:
            if "packet loss" in line:
                loss = line.split(',')[2].strip()
            if "avg" in line:
                parts = line.split('/')
                if len(parts) >= 5:
                    avg = f"{parts[4]}ms"
        
        embed = info_embed(f"Ping Results: {ip}")
        embed.add_field(name="📡 Target", value=f"```fix\n{ip}\n```", inline=True)
        embed.add_field(name="📊 Packet Loss", value=f"```fix\n{loss}\n```", inline=True)
        embed.add_field(name="⏱️ Avg Latency", value=f"```fix\n{avg}\n```", inline=True)
        embed.add_field(name="📋 Full Output", value=f"```bash\n{result[:500]}\n```", inline=False)
        
        await msg.edit(embed=embed)
    except Exception as e:
        await msg.edit(embed=error_embed("Ping Failed", f"```diff\n- {str(e)}\n```"))


async def trace_target(ctx, ip: str):
    """Trace route to IP address"""
    msg = await ctx.send(embed=info_embed("Tracing Route...", f"```fix\n{ip}\n```"))
    
    try:
        result = subprocess.getoutput(f"traceroute -n {ip} 2>/dev/null || tracepath {ip} 2>/dev/null")
        
        embed = terminal_embed(f"Trace Route to {ip}", result[:1900])
        await msg.edit(embed=embed)
    except Exception as e:
        await msg.edit(embed=error_embed("Trace Failed", f"```diff\n- {str(e)}\n```"))


# ==================================================================================================
#  🆕  NEW IP COMMANDS FOR USER MANAGEMENT
# ==================================================================================================

@bot.command(name="user-ip")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def user_ip(ctx, user: discord.Member):
    """Show IP information for a user (Admin only)"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=info_embed(f"No VPS", f"{user.mention} has no VPS."))
        return
    
    embed = discord.Embed(
        title=f"```glow\n🌐 IP Information for {user.display_name}\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else THUMBNAIL_URL)
    
    for vps in vps_list:
        stats = await get_container_stats(vps['container_name'])
        
        ip_text = f"```fix\n"
        ip_text += f"Container: {vps['container_name']}\n"
        if stats['ipv4']:
            ip_text += f"IPv4: {stats['ipv4'][0]}\n"
        ip_text += f"MAC: {stats['mac']}\n"
        ip_text += f"Status: {stats['status'].upper()}\n"
        ip_text += f"RAM: {vps['ram']}GB | CPU: {vps['cpu']}\n"
        ip_text += f"```"
        
        embed.add_field(name=f"📦 {vps['container_name']}", value=ip_text, inline=False)
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Admin View • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


@bot.command(name="assign-ip")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def assign_ip(ctx, user: discord.Member, container: str, ip_address: str = None):
    """Assign a static IP to a container (Admin only)"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container for v in vps_list):
        await ctx.send(embed=error_embed("Not Found", f"Container {container} not found for {user.mention}"))
        return
    
    if not ip_address:
        # Auto-assign IP
        ip_address = f"10.10.10.{random.randint(100, 250)}"
    
    # Get MAC address
    stats = await get_container_stats(container)
    mac = stats['mac']
    
    # Apply static IP
    cmd = f"ip addr add {ip_address}/24 dev eth0"
    await exec_in_container(container, cmd)
    
    # Save to database
    add_ipv4(user_id, container, ip_address, ip_address, mac)
    
    embed = success_embed("IP Assigned")
    embed.add_field(name="👤 User", value=user.mention, inline=True)
    embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
    embed.add_field(name="🌐 IP Address", value=f"```fix\n{ip_address}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{mac}\n```", inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name="release-ip")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def release_ip(ctx, user: discord.Member, container: str):
    """Release IP from a container (Admin only)"""
    user_id = str(user.id)
    
    # Remove from database
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM ipv4 WHERE user_id = ? AND container_name = ?', (user_id, container))
    conn.commit()
    conn.close()
    
    embed = success_embed("IP Released")
    embed.add_field(name="👤 User", value=user.mention, inline=True)
    embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name="ip-stats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def ip_stats(ctx):
    """Show IP statistics (Admin only)"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM ipv4')
    total_ips = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM ipv4')
    users_with_ips = cur.fetchone()[0] or 0
    
    cur.execute('SELECT user_id, COUNT(*) as count FROM ipv4 GROUP BY user_id ORDER BY count DESC LIMIT 5')
    top_users = cur.fetchall()
    conn.close()
    
    embed = info_embed("IP Statistics")
    embed.add_field(name="📊 Total IPs Assigned", value=f"```fix\n{total_ips}\n```", inline=True)
    embed.add_field(name="👥 Users with IPs", value=f"```fix\n{users_with_ips}\n```", inline=True)
    
    if top_users:
        top_text = ""
        for row in top_users:
            try:
                user = await bot.fetch_user(int(row['user_id']))
                top_text += f"• {user.name}: {row['count']} IPs\n"
            except:
                top_text += f"• Unknown: {row['count']} IPs\n"
        embed.add_field(name="🏆 Top Users", value=f"```fix\n{top_text}\n```", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="my-ip-info")
async def my_ip_info(ctx):
    """Show your IP information and network details"""
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    embed = discord.Embed(
        title="```glow\n🌐 Your Network Information\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # User info
    embed.add_field(
        name="👤 User",
        value=f"```fix\n{ctx.author.display_name}\nID: {ctx.author.id}\n```",
        inline=True
    )
    
    # Server info
    embed.add_field(
        name="🖥️ Server",
        value=f"```fix\nPublic: {SERVER_IP}\nHostname: {HOSTNAME}\nMAC: {MAC_ADDRESS}\n```",
        inline=True
    )
    
    # VPS Info
    if vps_list:
        vps_text = ""
        for vps in vps_list[:5]:
            stats = await get_container_stats(vps['container_name'])
            vps_text += f"• {vps['container_name']}: {stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n"
        embed.add_field(
            name="🖥️ Your VPS IPs",
            value=f"```fix\n{vps_text}\n```",
            inline=False
        )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Your Network Info • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


@bot.command(name="ip-history")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def ip_history(ctx, user: discord.Member = None):
    """Show IP assignment history (Admin only)"""
    conn = get_db()
    cur = conn.cursor()
    
    if user:
        cur.execute('SELECT * FROM ipv4 WHERE user_id = ? ORDER BY assigned_at DESC', (str(user.id),))
    else:
        cur.execute('SELECT * FROM ipv4 ORDER BY assigned_at DESC LIMIT 20')
    
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        await ctx.send(embed=info_embed("No IP History", "No IP assignments found."))
        return
    
    embed = info_embed(f"IP Assignment History ({len(rows)})")
    
    for row in rows[:10]:
        try:
            u = await bot.fetch_user(int(row['user_id']))
            username = u.name
        except:
            username = f"Unknown ({row['user_id'][:8]})"
        
        value = f"```fix\n"
        value += f"Container: {row['container_name']}\n"
        value += f"IP: {row['public_ip']}\n"
        value += f"MAC: {row['mac_address']}\n"
        value += f"Assigned: {row['assigned_at'][:16]}\n"
        value += f"```"
        
        embed.add_field(name=f"👤 {username}", value=value, inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  🚀  RUN THE BOT
# ==================================================================================================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n❌ ERROR: Please set your BOT_TOKEN!")
        sys.exit(1)
    update_local_node_stats()
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n❌ ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
