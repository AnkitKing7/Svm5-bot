# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                     SVM5-BOT - Complete VPS Management Bot                    ║
# ║                         Made by Ankit-Dev with ❤️                             ║
# ║                     Single File | No SSH | Direct LXC                         ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

import discord
from discord.ext import commands, tasks
from discord.ui import Modal, InputText, View, Button, Select
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
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
import aiohttp
import traceback

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ⚙️  CONFIGURATION - EDIT THESE BEFORE RUNNING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOT_TOKEN           = ""          # Discord Bot Token
BOT_PREFIX          = "."                             # Command prefix
BOT_NAME            = "SVM5-BOT"                      # Bot name
BOT_AUTHOR          = "Ankit-Dev"                      # Your name
MAIN_ADMIN_IDS      = [1405866008127864852]            # Your Discord ID(s)
VPS_USER_ROLE_ID    = ""                               # Auto-created if empty
DEFAULT_STORAGE_POOL = "default"                       # LXC storage pool

# Free VPS Plans based on invites
FREE_VPS_PLANS = {
    'invites': [
        {'name': '🥉 Bronze Plan', 'invites': 5, 'ram': 2, 'cpu': 1, 'disk': 20, 'emoji': '🥉'},
        {'name': '🥈 Silver Plan', 'invites': 10, 'ram': 4, 'cpu': 2, 'disk': 40, 'emoji': '🥈'},
        {'name': '🥇 Gold Plan', 'invites': 15, 'ram': 8, 'cpu': 4, 'disk': 80, 'emoji': '🥇'},
        {'name': '🏆 Platinum Plan', 'invites': 20, 'ram': 16, 'cpu': 8, 'disk': 160, 'emoji': '🏆'},
        {'name': '💎 Diamond Plan', 'invites': 25, 'ram': 32, 'cpu': 16, 'disk': 320, 'emoji': '💎'},
    ]
}

# OS Options for VPS Creation
OS_OPTIONS = [
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS"},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS"},
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS"},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable"},
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable"},
    {"label": "🎩 Fedora 39", "value": "images:fedora/39", "desc": "Fedora - Latest"},
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky - Enterprise Linux"},
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma - RHEL Compatible"},
]

# AI Configuration
AI_API_KEY          = "YOUR_GROQ_API_KEY"            # Get from console.groq.com
AI_MODEL            = "llama3-70b-8192"               # Groq model

# Thumbnail URL
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📝  LOGGING SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('svm5_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(BOT_NAME)

# Check if LXC is installed
if not shutil.which("lxc"):
    logger.error("❌ LXC command not found! Please install LXC first.")
    logger.error("   Ubuntu/Debian: sudo apt install lxc lxc-templates")
    logger.error("   Then run: sudo lxd init")
    sys.exit(1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🗄️  DATABASE SETUP (SQLite)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('svm5.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db()
    cur = conn.cursor()
    
    # Admins table
    cur.execute('''CREATE TABLE IF NOT EXISTS admins (
        user_id TEXT PRIMARY KEY
    )''')
    for admin_id in MAIN_ADMIN_IDS:
        cur.execute('INSERT OR IGNORE INTO admins (user_id) VALUES (?)', (str(admin_id),))
    
    # VPS table
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
        created_at TEXT NOT NULL,
        last_started TEXT,
        last_stopped TEXT,
        notes TEXT DEFAULT ''
    )''')
    
    # User stats table (invites/boosts)
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
        user_id TEXT PRIMARY KEY,
        invites INTEGER DEFAULT 0,
        boosts INTEGER DEFAULT 0,
        claimed_vps_count INTEGER DEFAULT 0,
        last_updated TEXT
    )''')
    
    # Settings table
    cur.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )''')
    
    # Transactions for IPv4 purchases
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        txn_ref TEXT UNIQUE NOT NULL,
        txn_id TEXT,
        amount INTEGER,
        status TEXT DEFAULT 'pending',
        created_at TEXT NOT NULL,
        verified_at TEXT
    )''')
    
    # IPv4 allocations
    cur.execute('''CREATE TABLE IF NOT EXISTS ipv4 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT NOT NULL,
        public_ip TEXT,
        private_ip TEXT,
        tunnel_url TEXT,
        assigned_at TEXT NOT NULL,
        UNIQUE(user_id, container_name)
    )''')
    
    # Port forwards
    cur.execute('''CREATE TABLE IF NOT EXISTS port_forwards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT NOT NULL,
        container_port INTEGER NOT NULL,
        host_port INTEGER UNIQUE NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    # Port allocations (quota)
    cur.execute('''CREATE TABLE IF NOT EXISTS port_allocations (
        user_id TEXT PRIMARY KEY,
        allocated_ports INTEGER DEFAULT 0
    )''')
    
    # Suspension logs
    cur.execute('''CREATE TABLE IF NOT EXISTS suspension_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        container_name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        action TEXT NOT NULL,
        reason TEXT,
        admin_id TEXT,
        created_at TEXT NOT NULL
    )''')
    
    # Backups/snapshots
    cur.execute('''CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT NOT NULL,
        snapshot_name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(container_name, snapshot_name)
    )''')
    
    # AI chat history
    cur.execute('''CREATE TABLE IF NOT EXISTS ai_history (
        user_id TEXT PRIMARY KEY,
        messages TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )''')
    
    # Initialize settings
    settings_init = [
        ('cpu_threshold', '90'),
        ('ram_threshold', '90'),
        ('maintenance_mode', 'false'),
        ('bot_version', '5.0.0'),
        ('bot_status', 'online'),
        ('bot_activity', 'watching'),
        ('bot_activity_name', f'{BOT_NAME} VPS Manager'),
        ('upcoming_purge', 'false'),
        ('upcoming_purge_time', ''),
    ]
    for key, value in settings_init:
        cur.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📊  DATABASE HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
    cur.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_user_vps(user_id: str) -> List[Dict]:
    """Get all VPS for a user"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM vps WHERE user_id = ? ORDER BY id', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_vps() -> List[Dict]:
    """Get all VPS from all users"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM vps ORDER BY user_id, id')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_vps(user_id: str, container_name: str, ram: int, cpu: int, disk: int, 
            os_version: str, plan_name: str = "Custom") -> Dict:
    """Add a new VPS to database"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT INTO vps 
                   (user_id, container_name, plan_name, ram, cpu, disk, os_version, status, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id, container_name, plan_name, ram, cpu, disk, os_version, 'running', now))
    vps_id = cur.lastrowid
    conn.commit()
    
    cur.execute('SELECT * FROM vps WHERE id = ?', (vps_id,))
    vps = dict(cur.fetchone())
    conn.close()
    return vps

def update_vps_status(container_name: str, status: str):
    """Update VPS status"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    if status == 'running':
        cur.execute('UPDATE vps SET status = ?, last_started = ? WHERE container_name = ?', 
                   (status, now, container_name))
    elif status == 'stopped':
        cur.execute('UPDATE vps SET status = ?, last_stopped = ? WHERE container_name = ?', 
                   (status, now, container_name))
    else:
        cur.execute('UPDATE vps SET status = ? WHERE container_name = ?', (status, container_name))
    conn.commit()
    conn.close()

def delete_vps(container_name: str) -> bool:
    """Delete VPS from database"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM vps WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM ipv4 WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM port_forwards WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM snapshots WHERE container_name = ?', (container_name,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted

def get_admins() -> List[str]:
    """Get all admin IDs"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM admins')
    rows = cur.fetchall()
    conn.close()
    return [row['user_id'] for row in rows]

def is_admin(user_id: str) -> bool:
    """Check if user is admin"""
    return user_id in get_admins() or user_id in [str(a) for a in MAIN_ADMIN_IDS]

def add_admin(user_id: str):
    """Add a new admin"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO admins (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def remove_admin(user_id: str):
    """Remove an admin"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_user_stats(user_id: str) -> Dict:
    """Get user statistics"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {'user_id': user_id, 'invites': 0, 'boosts': 0, 'claimed_vps_count': 0, 'last_updated': None}

def update_user_stats(user_id: str, invites: int = 0, boosts: int = 0, claimed_vps_count: int = 0):
    """Update user statistics"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''INSERT OR REPLACE INTO user_stats 
                   (user_id, invites, boosts, claimed_vps_count, last_updated) 
                   VALUES (?, 
                           COALESCE((SELECT invites FROM user_stats WHERE user_id = ?), 0) + ?, 
                           COALESCE((SELECT boosts FROM user_stats WHERE user_id = ?), 0) + ?,
                           COALESCE((SELECT claimed_vps_count FROM user_stats WHERE user_id = ?), 0) + ?,
                           ?)''',
                (user_id, user_id, invites, user_id, boosts, user_id, claimed_vps_count, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def add_transaction(user_id: str, txn_ref: str, amount: int) -> int:
    """Add a new transaction"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT INTO transactions (user_id, txn_ref, amount, created_at)
                   VALUES (?, ?, ?, ?)''', (user_id, txn_ref, amount, now))
    txn_id = cur.lastrowid
    conn.commit()
    conn.close()
    return txn_id

def verify_transaction(txn_ref: str, txn_id: str) -> bool:
    """Verify a transaction"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''UPDATE transactions SET status = 'verified', txn_id = ?, verified_at = ?
                   WHERE txn_ref = ? AND status = 'pending' ''', (txn_id, now, txn_ref))
    verified = cur.rowcount > 0
    conn.commit()
    conn.close()
    return verified

def get_pending_transactions() -> List[Dict]:
    """Get all pending transactions"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions WHERE status = "pending" ORDER BY created_at')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_ipv4(user_id: str, container_name: str, public_ip: str, private_ip: str, tunnel_url: str = ""):
    """Add IPv4 allocation"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT OR REPLACE INTO ipv4 (user_id, container_name, public_ip, private_ip, tunnel_url, assigned_at)
                   VALUES (?, ?, ?, ?, ?, ?)''', (user_id, container_name, public_ip, private_ip, tunnel_url, now))
    conn.commit()
    conn.close()

def get_user_ipv4(user_id: str) -> List[Dict]:
    """Get all IPv4 for a user"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ipv4 WHERE user_id = ?', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def remove_ipv4(user_id: str, container_name: str = None):
    """Remove IPv4 allocation"""
    conn = get_db()
    cur = conn.cursor()
    if container_name:
        cur.execute('DELETE FROM ipv4 WHERE user_id = ? AND container_name = ?', (user_id, container_name))
    else:
        cur.execute('DELETE FROM ipv4 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_port_allocation(user_id: str) -> int:
    """Get user's port quota"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT allocated_ports FROM port_allocations WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def set_port_allocation(user_id: str, amount: int):
    """Set user's port quota"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO port_allocations (user_id, allocated_ports) VALUES (?, ?)',
                (user_id, amount))
    conn.commit()
    conn.close()

def add_port_allocation(user_id: str, amount: int):
    """Add to user's port quota"""
    current = get_port_allocation(user_id)
    set_port_allocation(user_id, current + amount)

def get_user_port_forwards(user_id: str) -> List[Dict]:
    """Get all port forwards for a user"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM port_forwards WHERE user_id = ? ORDER BY created_at', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_port_forward(user_id: str, container_name: str, container_port: int, host_port: int) -> int:
    """Add a port forward"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT INTO port_forwards (user_id, container_name, container_port, host_port, created_at)
                   VALUES (?, ?, ?, ?, ?)''', (user_id, container_name, container_port, host_port, now))
    pf_id = cur.lastrowid
    conn.commit()
    conn.close()
    return pf_id

def remove_port_forward(pf_id: int) -> Tuple[bool, str, int]:
    """Remove a port forward"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, container_name, host_port FROM port_forwards WHERE id = ?', (pf_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "", 0
    user_id, container_name, host_port = row['user_id'], row['container_name'], row['host_port']
    cur.execute('DELETE FROM port_forwards WHERE id = ?', (pf_id,))
    conn.commit()
    conn.close()
    return True, container_name, host_port

def log_suspension(container_name: str, user_id: str, action: str, reason: str = "", admin_id: str = ""):
    """Log a suspension action"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT INTO suspension_logs (container_name, user_id, action, reason, admin_id, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''', (container_name, user_id, action, reason, admin_id, now))
    conn.commit()
    conn.close()

def add_snapshot(user_id: str, container_name: str, snapshot_name: str):
    """Add a snapshot record"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT OR REPLACE INTO snapshots (user_id, container_name, snapshot_name, created_at)
                   VALUES (?, ?, ?, ?)''', (user_id, container_name, snapshot_name, now))
    conn.commit()
    conn.close()

def get_snapshots(container_name: str = None) -> List[Dict]:
    """Get snapshots"""
    conn = get_db()
    cur = conn.cursor()
    if container_name:
        cur.execute('SELECT * FROM snapshots WHERE container_name = ? ORDER BY created_at DESC', (container_name,))
    else:
        cur.execute('SELECT * FROM snapshots ORDER BY created_at DESC LIMIT 50')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_ai_history(user_id: str, messages: List[Dict]):
    """Save AI chat history"""
    conn = get_db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute('''INSERT OR REPLACE INTO ai_history (user_id, messages, updated_at)
                   VALUES (?, ?, ?)''', (user_id, json.dumps(messages), now))
    conn.commit()
    conn.close()

def load_ai_history(user_id: str) -> List[Dict]:
    """Load AI chat history"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT messages FROM ai_history WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row['messages'])
    return []

def clear_ai_history(user_id: str):
    """Clear AI chat history"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM ai_history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎨  EMBED HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_embed(title: str, description: str = "", color: int = 0x5865F2) -> discord.Embed:
    """Create a styled embed"""
    embed = discord.Embed(
        title=f"✦ {BOT_NAME} - {title}",
        description=description,
        color=color
    )
    if THUMBNAIL_URL:
        embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(
        text=f"{BOT_NAME} • {BOT_AUTHOR} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        icon_url=THUMBNAIL_URL
    )
    return embed

def success_embed(title: str, description: str = "") -> discord.Embed:
    """Create a success embed"""
    return create_embed(title, description, 0x57F287)

def error_embed(title: str, description: str = "") -> discord.Embed:
    """Create an error embed"""
    return create_embed(title, description, 0xED4245)

def info_embed(title: str, description: str = "") -> discord.Embed:
    """Create an info embed"""
    return create_embed(title, description, 0x5865F2)

def warning_embed(title: str, description: str = "") -> discord.Embed:
    """Create a warning embed"""
    return create_embed(title, description, 0xFEE75C)

def no_vps_embed() -> discord.Embed:
    """Create a no VPS embed"""
    return info_embed(
        "No VPS Found",
        f"You don't have any VPS yet.\n\n"
        f"**To get a free VPS:**\n"
        f"• Use `{BOT_PREFIX}plans` to see available plans\n"
        f"• Use `{BOT_PREFIX}claim-free` to claim based on invites\n"
        f"• Contact an admin for custom VPS"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🛠️  LXC HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def run_lxc(command: str, timeout: int = 60) -> Tuple[str, str, int]:
    """Run an LXC command asynchronously"""
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
    """Get detailed container stats"""
    stats = {
        'status': 'unknown',
        'cpu': 'N/A',
        'memory': 'N/A',
        'disk': 'N/A',
        'uptime': 'N/A',
        'ipv4': []
    }
    
    # Get status
    stats['status'] = await get_container_status(container_name)
    
    if stats['status'] == 'running':
        # Get CPU usage
        out, _, _ = await exec_in_container(container_name, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        stats['cpu'] = f"{out}%" if out else "N/A"
        
        # Get memory usage
        out, _, _ = await exec_in_container(container_name, "free -m | awk '/^Mem:/{printf \"%d/%d MB (%.1f%%)\", $3, $2, $3/$2*100}'")
        stats['memory'] = out if out else "N/A"
        
        # Get disk usage
        out, _, _ = await exec_in_container(container_name, "df -h / | awk 'NR==2{printf \"%s/%s (%s)\", $3, $2, $5}'")
        stats['disk'] = out if out else "N/A"
        
        # Get uptime
        out, _, _ = await exec_in_container(container_name, "uptime -p | sed 's/up //'")
        stats['uptime'] = out if out else "N/A"
        
        # Get IPv4 addresses
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | grep -v '127.0.0.1'")
        if out:
            stats['ipv4'] = out.splitlines()
    
    return stats

async def apply_lxc_config(container_name: str):
    """Apply LXC configuration for better compatibility"""
    try:
        # Enable nesting and privileged mode
        await run_lxc(f"lxc config set {container_name} security.nesting true")
        await run_lxc(f"lxc config set {container_name} security.privileged true")
        
        # Add kernel modules
        await run_lxc(f"lxc config set {container_name} linux.kernel_modules overlay,br_netfilter,nf_nat,ip_tables")
        
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
        "sysctl -p /etc/sysctl.d/99-custom.conf || true",
        "apt-get update -qq",
        "apt-get install -y -qq curl wget sudo vim nano htop net-tools",
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
    
    for _ in range(100):
        port = random.randint(20000, 50000)
        if port not in used_ports:
            return port
    return None

async def create_port_forward(user_id: str, container_name: str, container_port: int) -> Optional[int]:
    """Create a port forward"""
    host_port = await get_available_host_port()
    if not host_port:
        return None
    
    try:
        # Add TCP proxy
        await run_lxc(f"lxc config device add {container_name} proxy-tcp-{host_port} proxy listen=tcp:0.0.0.0:{host_port} connect=tcp:127.0.0.1:{container_port}")
        # Add UDP proxy
        await run_lxc(f"lxc config device add {container_name} proxy-udp-{host_port} proxy listen=udp:0.0.0.0:{host_port} connect=udp:127.0.0.1:{container_port}")
        
        add_port_forward(user_id, container_name, container_port, host_port)
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🤖  BOT SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.start_time = datetime.utcnow()

# Global variables
MAINTENANCE_MODE = get_setting('maintenance_mode', 'false').lower() == 'true'
CPU_THRESHOLD = int(get_setting('cpu_threshold', 90))
RAM_THRESHOLD = int(get_setting('ram_threshold', 90))
UPCOMING_PURGE = get_setting('upcoming_purge', 'false').lower() == 'true'
UPCOMING_PURGE_TIME = get_setting('upcoming_purge_time', '')

# Active help menus
active_help_menus = {}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ✅  MAINTENANCE CHECK DECORATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def maintenance_check(ctx) -> bool:
    """Check if bot is in maintenance mode"""
    global MAINTENANCE_MODE
    
    if MAINTENANCE_MODE and not is_admin(str(ctx.author.id)):
        embed = warning_embed(
            "Maintenance Mode Active",
            "The bot is currently under maintenance. Only administrators can use commands."
        )
        await ctx.send(embed=embed)
        return False
    return True

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ✅  ON READY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.event
async def on_ready():
    """Bot ready event"""
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_PREFIX}help | {BOT_NAME}"
        )
    )
    logger.info(f"✅ Bot is ready: {bot.user} (ID: {bot.user.id})")
    
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
    
    print(f"""
╔════════════════════════════════════════════════════════════════╗
║                     {BOT_NAME} - ONLINE                          ║
║                         Made by {BOT_AUTHOR}                      ║
╠════════════════════════════════════════════════════════════════╣
║  Bot: {bot.user}                             ║
║  ID : {bot.user.id}                                        ║
║  Prefix: {BOT_PREFIX}                                           ║
║  Commands: 50+                                                 ║
╚════════════════════════════════════════════════════════════════╝
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ❌  ERROR HANDLER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_embed(
            "Missing Argument",
            f"Usage: `{BOT_PREFIX}{ctx.command.name} {ctx.command.signature}`\n"
            f"Use `{BOT_PREFIX}help` for more info."
        ))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=error_embed(
            "Invalid Argument",
            "Please check your input and try again."
        ))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=error_embed(
            "Access Denied",
            "You don't have permission to use this command."
        ))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=warning_embed(
            "Command on Cooldown",
            f"Please wait {error.retry_after:.1f} seconds before using this command again."
        ))
    else:
        logger.error(f"Error in {ctx.command}: {error}")
        await ctx.send(embed=error_embed(
            "Unexpected Error",
            f"```\n{str(error)[:1900]}\n```"
        ))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📖  HELP COMMAND (INTERACTIVE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class HelpView(View):
    """Interactive help menu"""
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_page = 0
        self.pages = [
            {
                "title": "📚 Welcome to SVM5-BOT Help",
                "description": f"**Prefix:** `{BOT_PREFIX}`\n**Version:** 5.0.0\n**Author:** {BOT_AUTHOR}\n\nSelect a category below to see commands.",
                "fields": [
                    ("👤 User Commands", "Basic commands for all users", True),
                    ("🖥️ VPS Management", "Control your VPS containers", True),
                    ("🔌 Port Forwarding", "Manage port forwards", True),
                    ("🤖 AI Chat", "Chat with AI assistant", True),
                    ("💰 Invite System", "Earn free VPS with invites", True),
                    ("🌐 IPv4 Management", "Buy and manage IPv4", True),
                ]
            },
            {
                "title": "👤 User Commands",
                "description": "Basic commands for all users",
                "fields": [
                    (f"{BOT_PREFIX}ping", "Check bot latency", False),
                    (f"{BOT_PREFIX}uptime", "Show bot uptime", False),
                    (f"{BOT_PREFIX}bot-info", "Detailed bot information", False),
                    (f"{BOT_PREFIX}plans", "View free VPS plans", False),
                    (f"{BOT_PREFIX}stats", "View your stats", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}claim-free", "Claim free VPS with invites", False),
                    (f"{BOT_PREFIX}my-acc", "View your generated account", False),
                    (f"{BOT_PREFIX}gen-acc", "Generate random account", False),
                ]
            },
            {
                "title": "🖥️ VPS Management",
                "description": "Control and manage your VPS containers",
                "fields": [
                    (f"{BOT_PREFIX}myvps", "List your VPS", False),
                    (f"{BOT_PREFIX}list", "Detailed VPS list", False),
                    (f"{BOT_PREFIX}manage", "Interactive VPS manager", False),
                    (f"{BOT_PREFIX}stats", "View VPS statistics", False),
                    (f"{BOT_PREFIX}logs", "View VPS logs", False),
                    (f"{BOT_PREFIX}share @user <num>", "Share VPS access", False),
                    (f"{BOT_PREFIX}unshare @user <num>", "Revoke VPS access", False),
                    (f"{BOT_PREFIX}shared", "List shared VPS", False),
                ]
            },
            {
                "title": "🔌 Port Forwarding",
                "description": "Manage port forwarding for your VPS",
                "fields": [
                    (f"{BOT_PREFIX}ports", "Port forwarding help", False),
                    (f"{BOT_PREFIX}ports add <num> <port>", "Add port forward", False),
                    (f"{BOT_PREFIX}ports list", "List your forwards", False),
                    (f"{BOT_PREFIX}ports remove <id>", "Remove port forward", False),
                ]
            },
            {
                "title": "🤖 AI Chat",
                "description": "Chat with AI assistant (powered by Groq LLaMA)",
                "fields": [
                    (f"{BOT_PREFIX}ai <message>", "Chat with AI", False),
                    (f"{BOT_PREFIX}ai-reset", "Reset chat history", False),
                ]
            },
            {
                "title": "💰 Invite System",
                "description": "Earn free VPS by inviting users",
                "fields": [
                    (f"{BOT_PREFIX}plans", "View plan requirements", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}stats", "View your stats", False),
                    (f"{BOT_PREFIX}claim-free", "Claim your VPS", False),
                ]
            },
            {
                "title": "🌐 IPv4 Management",
                "description": "Buy and manage IPv4 addresses",
                "fields": [
                    (f"{BOT_PREFIX}ipv4", "View your IPv4 list", False),
                    (f"{BOT_PREFIX}buy-ipv4", "Purchase IPv4 via UPI", False),
                ]
            },
        ]
        
        if is_admin(str(ctx.author.id)):
            self.pages.append({
                "title": "🛡️ Admin Commands",
                "description": "Commands for administrators",
                "fields": [
                    (f"{BOT_PREFIX}create <ram> <cpu> <disk> @user", "Create VPS", False),
                    (f"{BOT_PREFIX}delete <@user> <num> [reason]", "Delete VPS", False),
                    (f"{BOT_PREFIX}suspend <container> [reason]", "Suspend VPS", False),
                    (f"{BOT_PREFIX}unsuspend <container>", "Unsuspend VPS", False),
                    (f"{BOT_PREFIX}add-resources <container> [ram] [cpu] [disk]", "Add resources", False),
                    (f"{BOT_PREFIX}userinfo @user", "User information", False),
                    (f"{BOT_PREFIX}list-all", "List all VPS", False),
                    (f"{BOT_PREFIX}add-inv @user <amount>", "Add invites", False),
                    (f"{BOT_PREFIX}remove-inv @user <amount>", "Remove invites", False),
                    (f"{BOT_PREFIX}ports-add @user <amount>", "Add port slots", False),
                    (f"{BOT_PREFIX}serverstats", "Server statistics", False),
                ]
            })
        
        if str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            self.pages.append({
                "title": "👑 Main Admin Commands",
                "description": "Commands for main administrator only",
                "fields": [
                    (f"{BOT_PREFIX}admin-add @user", "Add admin", False),
                    (f"{BOT_PREFIX}admin-remove @user", "Remove admin", False),
                    (f"{BOT_PREFIX}admin-list", "List admins", False),
                    (f"{BOT_PREFIX}maintenance <on/off>", "Toggle maintenance", False),
                    (f"{BOT_PREFIX}set-threshold <cpu> <ram>", "Set thresholds", False),
                    (f"{BOT_PREFIX}purge-all", "Purge all unprotected VPS", False),
                    (f"{BOT_PREFIX}protect @user [num]", "Protect VPS from purge", False),
                    (f"{BOT_PREFIX}unprotect @user [num]", "Remove protection", False),
                ]
            })
        
        self.update_embed()
    
    def update_embed(self):
        """Update the embed for current page"""
        page = self.pages[self.current_page]
        self.embed = create_embed(page["title"], page["description"])
        for name, value, inline in page["fields"]:
            self.embed.add_field(name=name, value=value, inline=inline)
        self.embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)} • Use buttons to navigate")
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def prev_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        self.current_page = (self.current_page - 1) % len(self.pages)
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.danger)
    async def delete_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        await interaction.message.delete()

@bot.command(name="help")
@commands.cooldown(1, 3, commands.BucketType.user)
async def help_command(ctx):
    """Show interactive help menu"""
    if not await maintenance_check(ctx):
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ℹ️  INFO COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name="ping")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping_command(ctx):
    """Check bot latency"""
    if not await maintenance_check(ctx):
        return
    
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging...", "Measuring latency..."))
    end = time.time()
    
    api_latency = round(bot.latency * 1000)
    response_latency = round((end - start) * 1000)
    
    embed = create_embed("Pong! 🏓")
    embed.add_field(name="API Latency", value=f"`{api_latency}ms`", inline=True)
    embed.add_field(name="Response Time", value=f"`{response_latency}ms`", inline=True)
    
    if api_latency < 100:
        status = "🟢 Excellent"
    elif api_latency < 200:
        status = "🟡 Good"
    else:
        status = "🔴 Poor"
    embed.add_field(name="Status", value=status, inline=True)
    
    await msg.edit(embed=embed)

@bot.command(name="uptime")
@commands.cooldown(1, 5, commands.BucketType.user)
async def uptime_command(ctx):
    """Show bot uptime"""
    if not await maintenance_check(ctx):
        return
    
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    
    embed = info_embed(
        "Bot Uptime",
        f"**{days}d {hours}h {minutes}m {seconds}s**"
    )
    await ctx.send(embed=embed)

@bot.command(name="bot-info")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bot_info(ctx):
    """Show detailed bot information"""
    if not await maintenance_check(ctx):
        return
    
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    running_vps = sum(1 for v in all_vps if v['status'] == 'running')
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM vps')
    total_users = cur.fetchone()[0] or 0
    conn.close()
    
    embed = create_embed("Bot Information")
    embed.add_field(name="Version", value="`5.0.0`", inline=True)
    embed.add_field(name="Author", value=f"`{BOT_AUTHOR}`", inline=True)
    embed.add_field(name="Library", value=f"`discord.py {discord.__version__}`", inline=True)
    embed.add_field(name="Uptime", value=f"`{days}d {hours}h {minutes}m`", inline=True)
    embed.add_field(name="Servers", value=f"`{len(bot.guilds)}`", inline=True)
    embed.add_field(name="Users", value=f"`{total_users}`", inline=True)
    embed.add_field(name="Total VPS", value=f"`{total_vps}`", inline=True)
    embed.add_field(name="Running VPS", value=f"`{running_vps}`", inline=True)
    embed.add_field(name="Database", value="`SQLite 3`", inline=True)
    
    await ctx.send(embed=embed)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  👤  ACCOUNT GENERATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_username() -> str:
    """Generate a random username"""
    adjectives = ["cool", "fast", "dark", "epic", "blue", "swift", "neon", "alpha", "delta", "super"]
    nouns = ["wolf", "tiger", "storm", "byte", "nova", "blade", "fox", "raven", "hawk", "lion"]
    num = random.randint(10, 999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{num}"

def generate_email(username: str = None) -> str:
    """Generate a random email"""
    if not username:
        username = generate_username()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "proton.me", "hotmail.com"]
    return f"{username}@{random.choice(domains)}"

def generate_password(length: int = 16) -> str:
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

@bot.command(name="gen-acc")
@commands.cooldown(1, 10, commands.BucketType.user)
async def gen_account(ctx):
    """Generate a random account"""
    if not await maintenance_check(ctx):
        return
    
    username = generate_username()
    email = generate_email(username)
    password = generate_password()
    api_key = ''.join(random.choices(string.hexdigits, k=32))
    
    # Save to database (we can store in user_stats or a separate table)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''INSERT OR REPLACE INTO user_stats (user_id, invites, boosts, claimed_vps_count, last_updated)
                   VALUES (?, 
                           COALESCE((SELECT invites FROM user_stats WHERE user_id = ?), 0),
                           COALESCE((SELECT boosts FROM user_stats WHERE user_id = ?), 0),
                           COALESCE((SELECT claimed_vps_count FROM user_stats WHERE user_id = ?), 0),
                           ?)''',
                (str(ctx.author.id), str(ctx.author.id), str(ctx.author.id), str(ctx.author.id), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Try to DM the full credentials
    try:
        dm_embed = success_embed("🔐 Your Generated Account")
        dm_embed.add_field(name="Username", value=f"`{username}`", inline=False)
        dm_embed.add_field(name="Email", value=f"`{email}`", inline=False)
        dm_embed.add_field(name="Password", value=f"`{password}`", inline=False)
        dm_embed.add_field(name="API Key", value=f"`{api_key}`", inline=False)
        dm_embed.set_footer(text="Keep these safe! Delete this message after saving.")
        await ctx.author.send(embed=dm_embed)
        dm_status = "✅ Sent to your DMs"
    except:
        dm_status = "❌ Failed to send DM (enable DMs)"
    
    embed = success_embed("Account Generated!")
    embed.add_field(name="Username", value=f"`{username}`", inline=True)
    embed.add_field(name="Email", value=f"||`{email}`||", inline=True)
    embed.add_field(name="Password", value=f"||`{password}`||", inline=False)
    embed.add_field(name="DM Status", value=dm_status, inline=False)
    embed.set_footer(text="Full credentials sent to DM (check spam)")
    await ctx.send(embed=embed)

@bot.command(name="my-acc")
@commands.cooldown(1, 5, commands.BucketType.user)
async def my_account(ctx):
    """View your generated account"""
    if not await maintenance_check(ctx):
        return
    
    # Since we don't store the full account, we can't retrieve it
    # We'll show stats instead
    stats = get_user_stats(str(ctx.author.id))
    
    embed = info_embed("Your Account Info")
    embed.add_field(name="User ID", value=f"`{ctx.author.id}`", inline=True)
    embed.add_field(name="Invites", value=f"`{stats.get('invites', 0)}`", inline=True)
    embed.add_field(name="Boosts", value=f"`{stats.get('boosts', 0)}`", inline=True)
    embed.add_field(name="Claimed VPS", value=f"`{stats.get('claimed_vps_count', 0)}`", inline=True)
    embed.add_field(name="Note", value="Use `.gen-acc` to generate a new account", inline=False)
    
    await ctx.send(embed=embed)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  💰  FREE VPS PLANS & INVITE SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name="plans")
@commands.cooldown(1, 5, commands.BucketType.user)
async def show_plans(ctx):
    """Show free VPS plans"""
    if not await maintenance_check(ctx):
        return
    
    embed = create_embed("Free VPS Plans", "Earn VPS by inviting users to the server!")
    
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
    if not await maintenance_check(ctx):
        return
    
    stats = get_user_stats(str(ctx.author.id))
    invites = stats.get('invites', 0)
    
    embed = info_embed("Your Invite Stats", f"Current invites: **{invites}**")
    
    # Show available plans
    available = []
    for plan in FREE_VPS_PLANS['invites']:
        if invites >= plan['invites']:
            available.append(f"✅ {plan['emoji']} {plan['name']}")
        else:
            available.append(f"❌ {plan['emoji']} {plan['name']} (need {plan['invites']})")
    
    embed.add_field(name="Available Plans", value="\n".join(available), inline=False)
    embed.add_field(
        name="Next Steps",
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
        for os in OS_OPTIONS:
            options.append(discord.SelectOption(
                label=os["label"],
                value=os["value"],
                description=os["desc"]
            ))
        
        self.select = Select(
            placeholder="Select an operating system...",
            options=options[:25],
            min_values=1,
            max_values=1
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
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
                embed=info_embed("Cancelled", "VPS creation cancelled."),
                view=None
            )
        
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        view.add_item(confirm_btn)
        view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        
        embed = warning_embed(
            "Confirm VPS Creation",
            f"**Plan:** {self.plan['name']}\n"
            f"**OS:** {os_name}\n"
            f"**RAM:** {self.plan['ram']}GB\n"
            f"**CPU:** {self.plan['cpu']} Core(s)\n"
            f"**Disk:** {self.plan['disk']}GB\n\n"
            f"This will use **{self.plan['invites']}** invites from your account."
        )
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def create_vps(self, interaction: discord.Interaction, os_version: str):
        await interaction.response.defer()
        
        user_id = str(self.ctx.author.id)
        stats = get_user_stats(user_id)
        
        # Check if user already has a VPS
        user_vps = get_user_vps(user_id)
        if user_vps:
            await interaction.followup.send(
                embed=error_embed("VPS Already Exists", "You already have a VPS. Contact an admin if you need another."),
                ephemeral=True
            )
            return
        
        # Generate container name
        container_name = f"svm5-{user_id[:8]}-{random.randint(1000, 9999)}"
        
        # Create the container
        progress = await interaction.followup.send(
            embed=info_embed("Creating VPS", "Step 1/4: Initializing container..."),
            ephemeral=True
        )
        
        try:
            # Initialize container
            ram_mb = self.plan['ram'] * 1024
            await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
            
            await progress.edit(embed=info_embed("Creating VPS", "Step 2/4: Configuring resources..."))
            
            # Set limits
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            await run_lxc(f"lxc config set {container_name} limits.cpu {self.plan['cpu']}")
            await run_lxc(f"lxc config device set {container_name} root size={self.plan['disk']}GB")
            
            # Apply LXC config
            await apply_lxc_config(container_name)
            
            await progress.edit(embed=info_embed("Creating VPS", "Step 3/4: Starting container..."))
            
            # Start container
            await run_lxc(f"lxc start {container_name}")
            
            # Apply internal permissions
            await apply_internal_permissions(container_name)
            
            await progress.edit(embed=info_embed("Creating VPS", "Step 4/4: Finalizing..."))
            
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
                dm_embed.add_field(name="Container", value=f"`{container_name}`", inline=True)
                dm_embed.add_field(name="Plan", value=self.plan['name'], inline=True)
                dm_embed.add_field(name="OS", value=os_version, inline=True)
                dm_embed.add_field(name="Resources", value=f"{self.plan['ram']}GB RAM / {self.plan['cpu']} CPU / {self.plan['disk']}GB Disk", inline=False)
                dm_embed.add_field(name="Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
            # Success message
            embed = success_embed("✅ VPS Created Successfully!")
            embed.add_field(name="Container", value=f"`{container_name}`", inline=True)
            embed.add_field(name="Plan", value=self.plan['name'], inline=True)
            embed.add_field(name="OS", value=os_version, inline=True)
            embed.add_field(name="Resources", value=f"{self.plan['ram']}GB RAM / {self.plan['cpu']} CPU / {self.plan['disk']}GB Disk", inline=False)
            embed.add_field(name="Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
            
            await progress.edit(embed=embed)
            
            # Log
            logger.info(f"User {self.ctx.author} created VPS {container_name} with plan {self.plan['name']}")
            
        except Exception as e:
            logger.error(f"VPS creation failed: {e}")
            await progress.edit(embed=error_embed("Creation Failed", f"Error: {str(e)}"))
            
            # Clean up on failure
            try:
                await run_lxc(f"lxc delete {container_name} --force")
            except:
                pass

@bot.command(name="claim-free")
@commands.cooldown(1, 60, commands.BucketType.user)
async def claim_free(ctx):
    """Claim a free VPS based on your invites"""
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    invites = stats.get('invites', 0)
    
    # Check if user already has a VPS
    user_vps = get_user_vps(user_id)
    if user_vps:
        await ctx.send(embed=error_embed(
            "VPS Already Exists",
            "You already have a VPS. Each user can only claim one free VPS."
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
            f"You have **{invites}** invites.\n"
            f"You need at least **5** invites to claim a VPS.\n\n"
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
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    user_vps = get_user_vps(user_id)
    
    embed = info_embed(f"Statistics for {ctx.author.display_name}")
    embed.add_field(name="Invites", value=f"`{stats.get('invites', 0)}`", inline=True)
    embed.add_field(name="Boosts", value=f"`{stats.get('boosts', 0)}`", inline=True)
    embed.add_field(name="VPS Count", value=f"`{len(user_vps)}`", inline=True)
    embed.add_field(name="Claimed VPS", value=f"`{stats.get('claimed_vps_count', 0)}`", inline=True)
    
    await ctx.send(embed=embed)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🖥️  VPS MANAGEMENT COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name="myvps")
@commands.cooldown(1, 3, commands.BucketType.user)
async def my_vps(ctx):
    """List your VPS"""
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = info_embed(f"Your VPS ({len(vps_list)})")
    
    for i, vps in enumerate(vps_list, 1):
        status_emoji = "🟢" if vps['status'] == 'running' else "🔴"
        status_text = vps['status'].upper()
        if vps['suspended']:
            status_text = "⛔ SUSPENDED"
        
        embed.add_field(
            name=f"VPS #{i}",
            value=f"{status_emoji} **`{vps['container_name']}`**\n"
                  f"Status: `{status_text}`\n"
                  f"Plan: {vps['plan_name']}\n"
                  f"Resources: {vps['ram']}GB RAM / {vps['cpu']} CPU / {vps['disk']}GB Disk",
            inline=False
        )
    
    embed.add_field(name="Management", value=f"Use `{BOT_PREFIX}manage` for detailed control", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="list")
@commands.cooldown(1, 3, commands.BucketType.user)
async def list_command(ctx):
    """Detailed VPS list"""
    await my_vps(ctx)

class VPSManageView(View):
    """Interactive VPS management view"""
    def __init__(self, ctx, user_id, vps_list):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.user_id = user_id
        self.vps_list = vps_list
        self.current_index = 0
        self.message = None
        
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
        
        refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary)
        refresh_btn.callback = self.refresh_callback
        self.add_item(refresh_btn)
    
    async def get_current_embed(self) -> discord.Embed:
        """Get embed for current VPS"""
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        # Get live stats
        stats = await get_container_stats(container)
        
        status_emoji = "🟢" if stats['status'] == 'running' else "🔴" if stats['status'] == 'stopped' else "🟡"
        status_text = stats['status'].upper()
        if vps['suspended']:
            status_text = "⛔ SUSPENDED"
        
        embed = create_embed(f"VPS Management: {container}")
        embed.add_field(name="Status", value=f"{status_emoji} `{status_text}`", inline=True)
        embed.add_field(name="Plan", value=vps['plan_name'], inline=True)
        embed.add_field(name="OS", value=vps['os_version'], inline=True)
        embed.add_field(name="Resources", value=f"RAM: {vps['ram']}GB\nCPU: {vps['cpu']} Core(s)\nDisk: {vps['disk']}GB", inline=True)
        
        if stats['status'] == 'running':
            embed.add_field(name="CPU Usage", value=f"`{stats['cpu']}`", inline=True)
            embed.add_field(name="Memory", value=f"`{stats['memory']}`", inline=True)
            embed.add_field(name="Disk", value=f"`{stats['disk']}`", inline=True)
            embed.add_field(name="Uptime", value=f"`{stats['uptime']}`", inline=True)
            if stats['ipv4']:
                embed.add_field(name="IP Addresses", value="\n".join(f"`{ip}`" for ip in stats['ipv4']), inline=False)
        
        return embed
    
    async def prev_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        self.current_index = (self.current_index - 1) % len(self.vps_list)
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def next_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        self.current_index = (self.current_index + 1) % len(self.vps_list)
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def start_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended']:
            await interaction.response.send_message(embed=error_embed("Cannot Start", "This VPS is suspended."), ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            await run_lxc(f"lxc start {container}")
            update_vps_status(container, 'running')
            await interaction.followup.send(embed=success_embed("Started", f"VPS `{container}` started."), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", str(e)), ephemeral=True)
        
        # Refresh display
        await self.refresh_callback(interaction)
    
    async def stop_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended']:
            await interaction.response.send_message(embed=error_embed("Cannot Stop", "This VPS is suspended."), ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            await run_lxc(f"lxc stop {container} --force")
            update_vps_status(container, 'stopped')
            await interaction.followup.send(embed=success_embed("Stopped", f"VPS `{container}` stopped."), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", str(e)), ephemeral=True)
        
        # Refresh display
        await self.refresh_callback(interaction)
    
    async def restart_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended']:
            await interaction.response.send_message(embed=error_embed("Cannot Restart", "This VPS is suspended."), ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            await run_lxc(f"lxc restart {container}")
            update_vps_status(container, 'running')
            await interaction.followup.send(embed=success_embed("Restarted", f"VPS `{container}` restarted."), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", str(e)), ephemeral=True)
        
        # Refresh display
        await self.refresh_callback(interaction)
    
    async def stats_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        stats = await get_container_stats(container)
        
        embed = info_embed(f"Live Stats: {container}")
        embed.add_field(name="Status", value=stats['status'].upper(), inline=True)
        embed.add_field(name="CPU", value=stats['cpu'], inline=True)
        embed.add_field(name="Memory", value=stats['memory'], inline=True)
        embed.add_field(name="Disk", value=stats['disk'], inline=True)
        embed.add_field(name="Uptime", value=stats['uptime'], inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def refresh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        # Refresh VPS list from database
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
    """Interactive VPS manager"""
    if not await maintenance_check(ctx):
        return
    
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "Only admins can manage other users' VPS."))
            return
        target_id = str(user.id)
        target_name = user.display_name
    else:
        target_id = str(ctx.author.id)
        target_name = ctx.author.display_name
        user = ctx.author
    
    vps_list = get_user_vps(target_id)
    
    if not vps_list:
        if user:
            await ctx.send(embed=info_embed(f"No VPS", f"{user.mention} has no VPS."))
        else:
            await ctx.send(embed=no_vps_embed())
        return
    
    view = VPSManageView(ctx, target_id, vps_list)
    embed = await view.get_current_embed()
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg

@bot.command(name="logs")
@commands.cooldown(1, 5, commands.BucketType.user)
async def view_logs(ctx, container_name: str = None, lines: int = 50):
    """View VPS logs"""
    if not await maintenance_check(ctx):
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
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    await ctx.send(embed=info_embed("Fetching logs...", f"Getting last {lines} lines from {container_name}"))
    
    try:
        out, err, code = await exec_in_container(container_name, f"journalctl -n {lines} --no-pager || dmesg | tail -{lines}")
        if out:
            if len(out) > 1900:
                out = out[:1900] + "...\n(truncated)"
            embed = info_embed(f"Logs: {container_name}", f"```\n{out}\n```")
        else:
            embed = info_embed(f"Logs: {container_name}", "No logs available.")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", str(e)))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔌  PORT FORWARDING COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.group(name="ports", invoke_without_command=True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def ports_group(ctx):
    """Port forwarding commands"""
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    
    embed = info_embed("Port Forwarding Help")
    embed.add_field(name="Your Quota", value=f"Allocated: `{allocated}`\nUsed: `{len(forwards)}`\nAvailable: `{allocated - len(forwards)}`", inline=False)
    embed.add_field(
        name="Commands",
        value=f"`{BOT_PREFIX}ports add <vps_num> <port>` - Add forward\n"
              f"`{BOT_PREFIX}ports list` - List your forwards\n"
              f"`{BOT_PREFIX}ports remove <id>` - Remove forward",
        inline=False
    )
    await ctx.send(embed=embed)

@ports_group.command(name="add")
async def ports_add(ctx, vps_num: int, port: int):
    """Add a port forward"""
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"VPS number must be between 1 and {len(vps_list)}."))
        return
    
    if port < 1 or port > 65535:
        await ctx.send(embed=error_embed("Invalid Port", "Port must be between 1 and 65535."))
        return
    
    # Check quota
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    if len(forwards) >= allocated:
        await ctx.send(embed=error_embed("Quota Exceeded", f"You have used all {allocated} port slots."))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Cannot Add", "VPS is suspended."))
        return
    
    if vps['status'] != 'running':
        await ctx.send(embed=error_embed("Cannot Add", "VPS must be running to add port forwards."))
        return
    
    await ctx.send(embed=info_embed("Creating port forward...", f"Forwarding port {port} from VPS #{vps_num}"))
    
    host_port = await create_port_forward(user_id, container, port)
    
    if host_port:
        embed = success_embed("Port Forward Created")
        embed.add_field(name="VPS", value=f"#{vps_num} - `{container}`", inline=True)
        embed.add_field(name="Container Port", value=f"`{port}`", inline=True)
        embed.add_field(name="Host Port", value=f"`{host_port}`", inline=True)
        embed.add_field(name="Access", value=f"Connect to your server IP on port `{host_port}`", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=error_embed("Failed", "Could not assign a host port. Try again later."))

@ports_group.command(name="list")
async def ports_list(ctx):
    """List your port forwards"""
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    forwards = get_user_port_forwards(user_id)
    allocated = get_port_allocation(user_id)
    
    if not forwards:
        embed = info_embed("Port Forwards", "You have no active port forwards.")
        embed.add_field(name="Quota", value=f"Allocated: {allocated}\nUsed: 0\nAvailable: {allocated}")
        await ctx.send(embed=embed)
        return
    
    embed = info_embed(f"Your Port Forwards ({len(forwards)}/{allocated})")
    
    for f in forwards:
        vps_num = next((i+1 for i, v in enumerate(get_user_vps(user_id)) if v['container_name'] == f['container_name']), '?')
        embed.add_field(
            name=f"ID: {f['id']}",
            value=f"VPS #{vps_num}: `{f['container_port']}` → `{f['host_port']}`\nCreated: {f['created_at'][:16]}",
            inline=False
        )
    
    embed.add_field(name="Remove", value=f"Use `{BOT_PREFIX}ports remove <id>` to remove a forward", inline=False)
    await ctx.send(embed=embed)

@ports_group.command(name="remove")
async def ports_remove(ctx, forward_id: int):
    """Remove a port forward"""
    if not await maintenance_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    success, container, host_port = remove_port_forward(forward_id)
    
    if not success:
        await ctx.send(embed=error_embed("Not Found", f"Port forward with ID {forward_id} not found."))
        return
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this port forward."))
        return
    
    # Remove devices
    await remove_port_forward_device(container, host_port)
    
    await ctx.send(embed=success_embed("Removed", f"Port forward ID {forward_id} has been removed."))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🌐  IPv4 MANAGEMENT (with UPI payment)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UPI_ID = "your-upi@paytm"  # Change this
IPV4_PRICE_INR = 50

@bot.command(name="buy-ipv4")
@commands.cooldown(1, 30, commands.BucketType.user)
async def buy_ipv4(ctx):
    """Buy an IPv4 address via UPI"""
    if not await maintenance_check(ctx):
        return
    
    txn_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    embed = create_embed("Buy IPv4 Address")
    embed.add_field(name="Price", value=f"`₹{IPV4_PRICE_INR}`", inline=True)
    embed.add_field(name="UPI ID", value=f"`{UPI_ID}`", inline=True)
    embed.add_field(name="Reference", value=f"`{txn_ref}`", inline=True)
    embed.add_field(
        name="Payment Instructions",
        value=f"1. Pay ₹{IPV4_PRICE_INR} to `{UPI_ID}`\n"
              f"2. Add reference `{txn_ref}` in notes\n"
              f"3. Click ✅ after payment and enter transaction ID",
        inline=False
    )
    
    # Create view with payment confirmation button
    view = View(timeout=300)
    
    async def payment_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("Not your purchase!", ephemeral=True)
            return
        
        # Open modal for transaction ID
        modal = TransactionModal(ctx, txn_ref)
        await interaction.response.send_modal(modal)
    
    payment_btn = Button(label="✅ I've Paid", style=discord.ButtonStyle.success)
    payment_btn.callback = payment_callback
    view.add_item(payment_btn)
    
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def cancel_callback(interaction: discord.Interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "Purchase cancelled."), view=None)
    
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
            placeholder="e.g. T25031234567890",
            min_length=8,
            max_length=50
        ))
    
    async def callback(self, interaction: discord.Interaction):
        txn_id = self.children[0].value
        
        # Save transaction
        add_transaction(str(self.ctx.author.id), self.txn_ref, IPV4_PRICE_INR)
        
        # Notify admins
        embed = warning_embed("New IPv4 Purchase", f"User: {self.ctx.author.mention}\nTxn Ref: `{self.txn_ref}`\nTxn ID: `{txn_id}`\nAmount: ₹{IPV4_PRICE_INR}")
        
        for admin_id in MAIN_ADMIN_IDS:
            try:
                admin = await bot.fetch_user(admin_id)
                await admin.send(embed=embed)
            except:
                pass
        
        await interaction.response.edit_message(
            embed=info_embed(
                "Payment Submitted",
                f"Your payment has been submitted for verification.\n"
                f"**Reference:** `{self.txn_ref}`\n"
                f"**Transaction ID:** `{txn_id}`\n\n"
                f"An admin will verify your payment and assign IPv4 shortly."
            ),
            view=None
        )

@bot.command(name="ipv4")
@commands.cooldown(1, 3, commands.BucketType.user)
async def list_ipv4(ctx, user: discord.Member = None):
    """List your IPv4 addresses"""
    if not await maintenance_check(ctx):
        return
    
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "Only admins can view others' IPv4."))
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
    
    embed = info_embed(f"IPv4 Addresses - {target_name}", f"Total: {len(ipv4_list)}")
    
    for i, ip in enumerate(ipv4_list, 1):
        value = f"Container: `{ip['container_name']}`\n"
        if ip['public_ip']:
            value += f"Public IP: `{ip['public_ip']}`\n"
        if ip['private_ip']:
            value += f"Private IP: `{ip['private_ip']}`\n"
        if ip['tunnel_url']:
            value += f"Tunnel: {ip['tunnel_url']}\n"
        value += f"Assigned: {ip['assigned_at'][:16]}"
        
        embed.add_field(name=f"IPv4 #{i}", value=value, inline=False)
    
    await ctx.send(embed=embed)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🤖  AI CHAT COMMANDS (Groq LLaMA)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name="ai")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ai_chat(ctx, *, message: str):
    """Chat with AI assistant"""
    if not await maintenance_check(ctx):
        return
    
    if not AI_API_KEY or AI_API_KEY == "YOUR_GROQ_API_KEY":
        await ctx.send(embed=error_embed("AI Not Configured", "Please set a valid Groq API key in the config."))
        return
    
    user_id = str(ctx.author.id)
    
    # Load history
    history = load_ai_history(user_id)
    if not history:
        history = [{
            "role": "system",
            "content": f"You are {BOT_NAME} AI Assistant, a helpful VPS management bot made by {BOT_AUTHOR}. You help with Linux, LXC containers, and server management. Keep responses concise and friendly."
        }]
    
    # Add user message
    history.append({"role": "user", "content": message})
    
    # Keep last 20 messages + system
    if len(history) > 21:
        history = [history[0]] + history[-20:]
    
    await ctx.send(embed=info_embed("AI is thinking...", "This may take a few seconds."))
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": AI_MODEL,
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
                    await ctx.send(embed=embed)
                    
                    for chunk in chunks[1:]:
                        await ctx.send(embed=info_embed("", chunk))
                else:
                    error_text = await resp.text()
                    await ctx.send(embed=error_embed("API Error", f"Status {resp.status}: {error_text[:200]}"))
    except Exception as e:
        await ctx.send(embed=error_embed("AI Error", str(e)[:1900]))

@bot.command(name="ai-reset")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ai_reset(ctx):
    """Reset AI chat history"""
    if not await maintenance_check(ctx):
        return
    
    clear_ai_history(str(ctx.author.id))
    await ctx.send(embed=success_embed("AI History Reset", "Your conversation with AI has been cleared."))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🛡️  ADMIN COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def admin_only():
    """Decorator for admin-only commands"""
    async def predicate(ctx):
        if not await maintenance_check(ctx):
            return False
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "This command is for administrators only."))
            return False
        return True
    return commands.check(predicate)

def main_admin_only():
    """Decorator for main admin-only commands"""
    async def predicate(ctx):
        if not await maintenance_check(ctx):
            return False
        if str(ctx.author.id) not in [str(a) for a in MAIN_ADMIN_IDS]:
            await ctx.send(embed=error_embed("Access Denied", "This command is for the main administrator only."))
            return False
        return True
    return commands.check(predicate)

@bot.command(name="create")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    """Create a VPS for a user"""
    if ram <= 0 or cpu <= 0 or disk <= 0:
        await ctx.send(embed=error_embed("Invalid Specs", "RAM, CPU, and Disk must be positive integers."))
        return
    
    # OS selection view
    view = View(timeout=60)
    options = []
    for os in OS_OPTIONS:
        options.append(discord.SelectOption(label=os["label"], value=os["value"], description=os["desc"]))
    
    select = Select(placeholder="Select operating system...", options=options[:25])
    
    async def select_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("Not your command!", ephemeral=True)
            return
        
        selected_os = select.values[0]
        
        # Confirm view
        confirm_view = View(timeout=60)
        confirm_btn = Button(label="✅ Create", style=discord.ButtonStyle.success)
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        
        async def confirm_callback(confirm_interaction):
            await create_vps_action(confirm_interaction, user, ram, cpu, disk, selected_os)
        
        async def cancel_callback(cancel_interaction):
            await cancel_interaction.response.edit_message(embed=info_embed("Cancelled", "VPS creation cancelled."), view=None)
        
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        confirm_view.add_item(confirm_btn)
        confirm_view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        
        embed = warning_embed(
            "Confirm VPS Creation",
            f"**User:** {user.mention}\n"
            f"**OS:** {os_name}\n"
            f"**RAM:** {ram}GB\n"
            f"**CPU:** {cpu} Core(s)\n"
            f"**Disk:** {disk}GB"
        )
        
        await interaction.response.edit_message(embed=embed, view=confirm_view)
    
    select.callback = select_callback
    view.add_item(select)
    
    embed = info_embed("Create VPS", f"Select an operating system for {user.mention}")
    await ctx.send(embed=embed, view=view)

async def create_vps_action(interaction, user, ram, cpu, disk, os_version):
    await interaction.response.defer()
    
    user_id = str(user.id)
    container_name = f"svm5-{user_id[:8]}-{random.randint(1000, 9999)}"
    
    progress = await interaction.followup.send(
        embed=info_embed("Creating VPS", "Step 1/4: Initializing container..."),
        ephemeral=True
    )
    
    try:
        # Initialize
        ram_mb = ram * 1024
        await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
        
        await progress.edit(embed=info_embed("Creating VPS", "Step 2/4: Configuring resources..."))
        
        # Set limits
        await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
        await run_lxc(f"lxc config set {container_name} limits.cpu {cpu}")
        await run_lxc(f"lxc config device set {container_name} root size={disk}GB")
        
        # Apply config
        await apply_lxc_config(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "Step 3/4: Starting container..."))
        
        # Start
        await run_lxc(f"lxc start {container_name}")
        
        # Apply permissions
        await apply_internal_permissions(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "Step 4/4: Finalizing..."))
        
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
            dm_embed.add_field(name="Container", value=f"`{container_name}`", inline=True)
            dm_embed.add_field(name="Resources", value=f"{ram}GB RAM / {cpu} CPU / {disk}GB Disk", inline=True)
            dm_embed.add_field(name="OS", value=os_version, inline=True)
            dm_embed.add_field(name="Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        # Success
        embed = success_embed("✅ VPS Created Successfully!")
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Container", value=f"`{container_name}`", inline=True)
        embed.add_field(name="Resources", value=f"{ram}GB RAM / {cpu} CPU / {disk}GB Disk", inline=False)
        
        await progress.edit(embed=embed)
        logger.info(f"Admin {interaction.user} created VPS {container_name} for {user}")
        
    except Exception as e:
        logger.error(f"VPS creation failed: {e}")
        await progress.edit(embed=error_embed("Creation Failed", f"Error: {str(e)}"))
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
        await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS."))
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid Number", f"VPS number must be between 1 and {len(vps_list)}."))
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
        await interaction.response.edit_message(embed=info_embed("Cancelled", "Deletion cancelled."), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "⚠️ Confirm VPS Deletion",
        f"**User:** {user.mention}\n"
        f"**VPS #{vps_num}:** `{container}`\n"
        f"**Plan:** {vps['plan_name']}\n"
        f"**Resources:** {vps['ram']}GB RAM / {vps['cpu']} CPU / {vps['disk']}GB Disk\n"
        f"**Reason:** {reason}\n\n"
        f"This action cannot be undone!"
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
            dm_embed = warning_embed("VPS Deleted", f"Your VPS `{container}` has been deleted by an admin.")
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Deleted", f"VPS `{container}` has been deleted.")
        await interaction.followup.send(embed=embed)
        logger.info(f"Admin {interaction.user} deleted VPS {container} for {user}")
        
    except Exception as e:
        await interaction.followup.send(embed=error_embed("Deletion Failed", str(e)))

@bot.command(name="suspend")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_suspend(ctx, container_name: str, *, reason: str = "Admin action"):
    """Suspend a VPS"""
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"VPS `{container_name}` not found."))
        return
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Already Suspended", "This VPS is already suspended."))
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
            dm_embed = warning_embed("VPS Suspended", f"Your VPS `{container_name}` has been suspended.")
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Suspended", f"VPS `{container_name}` has been suspended.\nReason: {reason}")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", str(e)))

@bot.command(name="unsuspend")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_unsuspend(ctx, container_name: str):
    """Unsuspend a VPS"""
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"VPS `{container_name}` not found."))
        return
    
    if not vps['suspended']:
        await ctx.send(embed=error_embed("Not Suspended", "This VPS is not suspended."))
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
            dm_embed = success_embed("VPS Unsuspended", f"Your VPS `{container_name}` has been unsuspended.")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Unsuspended", f"VPS `{container_name}` has been unsuspended and started.")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", str(e)))

@bot.command(name="add-resources")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_add_resources(ctx, container_name: str, ram: int = None, cpu: int = None, disk: int = None):
    """Add resources to a VPS"""
    if ram is None and cpu is None and disk is None:
        await ctx.send(embed=error_embed("Missing Parameters", "Specify at least one resource to add."))
        return
    
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"VPS `{container_name}` not found."))
        return
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Suspended", "Cannot modify a suspended VPS."))
        return
    
    was_running = vps['status'] == 'running'
    
    if was_running:
        await ctx.send(embed=info_embed("Stopping VPS", f"Stopping {container_name} to apply changes..."))
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
            await ctx.send(embed=info_embed("Starting VPS", f"Starting {container_name}..."))
            await run_lxc(f"lxc start {container_name}")
            await apply_internal_permissions(container_name)
        
        embed = success_embed("Resources Added", f"Changes applied to `{container_name}`:")
        embed.add_field(name="Changes", value="\n".join(changes), inline=False)
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", str(e)))
        
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
    
    embed = info_embed(f"User Info: {user.display_name}")
    embed.add_field(name="User ID", value=f"`{user.id}`", inline=True)
    embed.add_field(name="Joined", value=user.joined_at.strftime("%Y-%m-%d") if user.joined_at else "Unknown", inline=True)
    
    stats_text = f"Invites: `{stats.get('invites', 0)}`\n"
    stats_text += f"Boosts: `{stats.get('boosts', 0)}`\n"
    stats_text += f"Claimed VPS: `{stats.get('claimed_vps_count', 0)}`\n"
    stats_text += f"Port Quota: `{port_quota}` (Used: {len(forwards)})"
    embed.add_field(name="Statistics", value=stats_text, inline=True)
    
    if vps_list:
        vps_text = ""
        for i, vps in enumerate(vps_list, 1):
            status = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
            vps_text += f"{status} VPS #{i}: `{vps['container_name']}` ({vps['ram']}GB/{vps['cpu']}C/{vps['disk']}GB)\n"
        embed.add_field(name=f"VPS ({len(vps_list)})", value=vps_text, inline=False)
    else:
        embed.add_field(name="VPS", value="None", inline=False)
    
    if ipv4_list:
        embed.add_field(name=f"IPv4 ({len(ipv4_list)})", value="\n".join(f"`{ip['container_name']}`" for ip in ipv4_list), inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="list-all")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_list_all(ctx):
    """List all VPS in the system"""
    all_vps = get_all_vps()
    
    if not all_vps:
        await ctx.send(embed=info_embed("No VPS", "No VPS in the system."))
        return
    
    # Group by user
    users = {}
    for vps in all_vps:
        if vps['user_id'] not in users:
            users[vps['user_id']] = []
        users[vps['user_id']].append(vps)
    
    embed = info_embed(f"All VPS ({len(all_vps)})")
    
    for user_id, vps_list in list(users.items())[:5]:  # Limit to 5 users per embed
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
        embed.add_field(name="Note", value=f"Showing 5 of {len(users)} users", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="add-inv")
@admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def admin_add_invites(ctx, user: discord.Member, amount: int):
    """Add invites to a user"""
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "Amount must be positive."))
        return
    
    update_user_stats(str(user.id), invites=amount)
    stats = get_user_stats(str(user.id))
    
    embed = success_embed("Invites Added", f"Added **{amount}** invites to {user.mention}")
    embed.add_field(name="New Total", value=f"Invites: `{stats['invites']}`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="remove-inv")
@admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def admin_remove_invites(ctx, user: discord.Member, amount: int):
    """Remove invites from a user"""
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "Amount must be positive."))
        return
    
    stats = get_user_stats(str(user.id))
    if stats['invites'] < amount:
        amount = stats['invites']
    
    update_user_stats(str(user.id), invites=-amount)
    new_stats = get_user_stats(str(user.id))
    
    embed = success_embed("Invites Removed", f"Removed **{amount}** invites from {user.mention}")
    embed.add_field(name="New Total", value=f"Invites: `{new_stats['invites']}`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ports-add")
@admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def admin_ports_add(ctx, user: discord.Member, amount: int):
    """Add port slots to a user"""
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "Amount must be positive."))
        return
    
    add_port_allocation(str(user.id), amount)
    new_quota = get_port_allocation(str(user.id))
    
    embed = success_embed("Port Slots Added", f"Added **{amount}** port slots to {user.mention}")
    embed.add_field(name="New Quota", value=f"Total: `{new_quota}`", inline=False)
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
    conn.close()
    
    embed = info_embed("Server Statistics")
    embed.add_field(name="VPS Stats", value=f"Total: {total_vps}\nRunning: {running}\nStopped: {stopped}\nSuspended: {suspended}", inline=True)
    embed.add_field(name="Resources", value=f"RAM: {total_ram}GB\nCPU: {total_cpu} cores\nDisk: {total_disk}GB", inline=True)
    embed.add_field(name="Other", value=f"Users: {total_users}\nPort Forwards: {total_ports}", inline=True)
    
    await ctx.send(embed=embed)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  👑  MAIN ADMIN COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.command(name="admin-add")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_add(ctx, user: discord.Member):
    """Add a new admin"""
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Already Main Admin", "This user is already a main admin."))
        return
    
    if is_admin(str(user.id)):
        await ctx.send(embed=error_embed("Already Admin", f"{user.mention} is already an admin."))
        return
    
    add_admin(str(user.id))
    
    embed = success_embed("Admin Added", f"{user.mention} has been added as an admin.")
    await ctx.send(embed=embed)

@bot.command(name="admin-remove")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_remove(ctx, user: discord.Member):
    """Remove an admin"""
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Cannot Remove", "Cannot remove main admin."))
        return
    
    if not is_admin(str(user.id)):
        await ctx.send(embed=error_embed("Not Admin", f"{user.mention} is not an admin."))
        return
    
    remove_admin(str(user.id))
    
    embed = success_embed("Admin Removed", f"{user.mention} has been removed as an admin.")
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
    
    embed.add_field(name="Main Admin", value=main_admin_text, inline=False)
    
    if admins:
        admin_text = ""
        for admin_id in admins:
            try:
                user = await bot.fetch_user(int(admin_id))
                admin_text += f"🛡️ {user.mention}\n"
            except:
                admin_text += f"🛡️ `{admin_id}`\n"
        embed.add_field(name="Admins", value=admin_text, inline=False)
    else:
        embed.add_field(name="Admins", value="None", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="maintenance")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def main_maintenance(ctx, mode: str):
    """Toggle maintenance mode"""
    global MAINTENANCE_MODE
    
    mode = mode.lower()
    if mode not in ['on', 'off']:
        await ctx.send(embed=error_embed("Invalid Mode", "Use `on` or `off`."))
        return
    
    MAINTENANCE_MODE = (mode == 'on')
    set_setting('maintenance_mode', str(MAINTENANCE_MODE).lower())
    
    if MAINTENANCE_MODE:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="🔧 Maintenance Mode"))
        embed = warning_embed("Maintenance Mode Enabled", "Only admins can use commands now.")
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {BOT_NAME}"))
        embed = success_embed("Maintenance Mode Disabled", "All commands are now available.")
    
    await ctx.send(embed=embed)

@bot.command(name="set-threshold")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def main_set_threshold(ctx, cpu: int, ram: int):
    """Set CPU and RAM thresholds"""
    global CPU_THRESHOLD, RAM_THRESHOLD
    
    if cpu < 0 or cpu > 100 or ram < 0 or ram > 100:
        await ctx.send(embed=error_embed("Invalid Values", "Thresholds must be between 0 and 100."))
        return
    
    CPU_THRESHOLD = cpu
    RAM_THRESHOLD = ram
    set_setting('cpu_threshold', str(cpu))
    set_setting('ram_threshold', str(ram))
    
    embed = success_embed("Thresholds Updated", f"CPU: {cpu}%\nRAM: {ram}%")
    await ctx.send(embed=embed)

@bot.command(name="protect")
@main_admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def main_protect(ctx, user: discord.Member, vps_num: int = None):
    """Protect a VPS from purge"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS."))
        return
    
    if vps_num is None:
        # Protect all
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Added", f"All VPS of {user.mention} are now protected from purge.")
        await ctx.send(embed=embed)
    else:
        if vps_num < 1 or vps_num > len(vps_list):
            await ctx.send(embed=error_embed("Invalid Number", f"VPS number must be between 1 and {len(vps_list)}."))
            return
        
        vps = vps_list[vps_num - 1]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE container_name = ?', (vps['container_name'],))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Added", f"VPS #{vps_num} of {user.mention} is now protected from purge.")
        await ctx.send(embed=embed)

@bot.command(name="unprotect")
@main_admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def main_unprotect(ctx, user: discord.Member, vps_num: int = None):
    """Remove purge protection from a VPS"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS."))
        return
    
    if vps_num is None:
        # Unprotect all
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Removed", f"All VPS of {user.mention} are no longer protected from purge.")
        await ctx.send(embed=embed)
    else:
        if vps_num < 1 or vps_num > len(vps_list):
            await ctx.send(embed=error_embed("Invalid Number", f"VPS number must be between 1 and {len(vps_list)}."))
            return
        
        vps = vps_list[vps_num - 1]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE container_name = ?', (vps['container_name'],))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Removed", f"VPS #{vps_num} of {user.mention} is no longer protected from purge.")
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
        await ctx.send(embed=info_embed("No Unprotected VPS", "All VPS are protected."))
        return
    
    embed = warning_embed(
        "⚠️ PURGE ALL UNPROTECTED VPS",
        f"This will delete **{len(unprotected)}** unprotected VPS.\n"
        f"Protected VPS will be skipped.\n\n"
        f"**This action cannot be undone!**"
    )
    
    view = View(timeout=60)
    confirm_btn = Button(label="✅ PURGE", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        await perform_purge(interaction, unprotected)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "Purge cancelled."), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    await ctx.send(embed=embed, view=view)

async def perform_purge(interaction, unprotected):
    await interaction.response.defer()
    
    progress = await interaction.followup.send(
        embed=info_embed("Purging VPS", f"Starting purge of {len(unprotected)} VPS..."),
        ephemeral=True
    )
    
    deleted = 0
    failed = 0
    
    for i, vps in enumerate(unprotected, 1):
        container = vps['container_name']
        
        try:
            # Update progress
            if i % 5 == 0:
                await progress.edit(embed=info_embed("Purging VPS", f"Progress: {i}/{len(unprotected)}..."))
            
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
    
    embed = success_embed("Purge Complete", f"Deleted: {deleted}\nFailed: {failed}")
    await progress.edit(embed=embed)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🚀  RUN THE BOT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "="*50)
        print("❌ ERROR: Please set your BOT_TOKEN in the configuration!")
        print("="*50 + "\n")
        sys.exit(1)
    
    # Check LXC
    try:
        subprocess.run(['lxc', '--version'], capture_output=True, check=True)
    except:
        print("\n" + "="*50)
        print("❌ ERROR: LXC is not installed or not in PATH!")
        print("Install LXC: sudo apt install lxc lxc-templates")
        print("Then run: sudo lxd init")
        print("="*50 + "\n")
        sys.exit(1)
    
    # Run bot
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n" + "="*50)
        print("❌ ERROR: Invalid Discord token!")
        print("="*50 + "\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
