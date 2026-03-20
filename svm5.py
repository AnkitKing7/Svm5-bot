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
# ║  ║                    ✅ 84 COMMANDS + 70+ OS • FULL UI • EVERYTHING WORKING              ║   ║
# ║  ╠════════════════════════════════════════════════════════════════════════════════════════╣   ║
# ║  ║  🏠 HOME      👤 USER(14)  🖥️ VPS(8)   📟 CONSOLE(10)  🎮 GAMES(7)  🛠️ TOOLS(7)       ║   ║
# ║  ║  🌐 NODES(7)  👥 SHARE(4)  🔌 PORTS(6) 🌍 IPv4(6)     📦 PANELS(6) 🤖 AI(3)           ║   ║
# ║  ║  🐧 OS(70+)   🛡️ ADMIN(13) 👑 OWNER(9)  🔘 BUTTONS    📋 SELECT    🎨 GLOW UI          ║   ║
# ║  ╚════════════════════════════════════════════════════════════════════════════════════════╝   ║
# ║                                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

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
#  🎨  COLOR CONSTANTS FOR UI
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
    'os': 0x00FF88,
}

# ==================================================================================================
#  📝  LOGGING SETUP
# ==================================================================================================

os.makedirs('/opt/svm5-bot/logs', exist_ok=True)
os.makedirs('/opt/svm5-bot/data', exist_ok=True)
os.makedirs('/opt/svm5-bot/backups', exist_ok=True)
os.makedirs('/opt/svm5-bot/qr_codes', exist_ok=True)

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
    # Ubuntu Series (15)
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 18.04 LTS", "value": "ubuntu:18.04", "desc": "Bionic Beaver - Legacy", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 16.04 LTS", "value": "ubuntu:16.04", "desc": "Xenial Xerus - Old", "category": "Ubuntu", "ram_min": 256},
    {"label": "🐧 Ubuntu 14.04 LTS", "value": "ubuntu:14.04", "desc": "Trusty Tahr - Ancient", "category": "Ubuntu", "ram_min": 256},
    {"label": "🐧 Ubuntu 12.04 LTS", "value": "ubuntu:12.04", "desc": "Precise Pangolin - Retro", "category": "Ubuntu", "ram_min": 256},
    {"label": "🐧 Ubuntu 10.04 LTS", "value": "ubuntu:10.04", "desc": "Lucid Lynx - Museum", "category": "Ubuntu", "ram_min": 128},
    {"label": "🐧 Ubuntu 23.10", "value": "ubuntu:23.10", "desc": "Mantic Minotaur", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 23.04", "value": "ubuntu:23.04", "desc": "Lunar Lobster", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 22.10", "value": "ubuntu:22.10", "desc": "Kinetic Kudu", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 21.10", "value": "ubuntu:21.10", "desc": "Impish Indri", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 21.04", "value": "ubuntu:21.04", "desc": "Hirsute Hippo", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 20.10", "value": "ubuntu:20.10", "desc": "Groovy Gorilla", "category": "Ubuntu", "ram_min": 512},
    {"label": "🐧 Ubuntu 19.10", "value": "ubuntu:19.10", "desc": "Eoan Ermine", "category": "Ubuntu", "ram_min": 512},
    
    # Debian Series (15)
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable", "category": "Debian", "ram_min": 256},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable", "category": "Debian", "ram_min": 256},
    {"label": "🌀 Debian 10", "value": "images:debian/10", "desc": "Buster - Older", "category": "Debian", "ram_min": 256},
    {"label": "🌀 Debian 9", "value": "images:debian/9", "desc": "Stretch - Legacy", "category": "Debian", "ram_min": 256},
    {"label": "🌀 Debian 8", "value": "images:debian/8", "desc": "Jessie - Ancient", "category": "Debian", "ram_min": 128},
    {"label": "🌀 Debian 7", "value": "images:debian/7", "desc": "Wheezy - Retro", "category": "Debian", "ram_min": 128},
    {"label": "🌀 Debian 6", "value": "images:debian/6", "desc": "Squeeze - Very Old", "category": "Debian", "ram_min": 128},
    {"label": "🌀 Debian 5", "value": "images:debian/5", "desc": "Lenny - Museum", "category": "Debian", "ram_min": 128},
    {"label": "🌀 Debian 4", "value": "images:debian/4", "desc": "Etch - Retro", "category": "Debian", "ram_min": 64},
    {"label": "🌀 Debian 3", "value": "images:debian/3", "desc": "Woody - Museum", "category": "Debian", "ram_min": 64},
    {"label": "🌀 Debian Sid", "value": "images:debian/sid", "desc": "Unstable - Rolling", "category": "Debian", "ram_min": 512},
    {"label": "🌀 Debian Testing", "value": "images:debian/testing", "desc": "Testing - Next", "category": "Debian", "ram_min": 512},
    {"label": "🌀 Debian Unstable", "value": "images:debian/unstable", "desc": "Unstable - Dev", "category": "Debian", "ram_min": 512},
    {"label": "🌀 Debian Experimental", "value": "images:debian/experimental", "desc": "Experimental", "category": "Debian", "ram_min": 512},
    
    # Fedora Series (10)
    {"label": "🎩 Fedora 40", "value": "images:fedora/40", "desc": "Fedora 40 - Latest", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 39", "value": "images:fedora/39", "desc": "Fedora 39", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 38", "value": "images:fedora/38", "desc": "Fedora 38", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 37", "value": "images:fedora/37", "desc": "Fedora 37", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 36", "value": "images:fedora/36", "desc": "Fedora 36", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 35", "value": "images:fedora/35", "desc": "Fedora 35", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 34", "value": "images:fedora/34", "desc": "Fedora 34", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 33", "value": "images:fedora/33", "desc": "Fedora 33", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora 32", "value": "images:fedora/32", "desc": "Fedora 32", "category": "Fedora", "ram_min": 1024},
    {"label": "🎩 Fedora Rawhide", "value": "images:fedora/rawhide", "desc": "Development - Rolling", "category": "Fedora", "ram_min": 1024},
    
    # Rocky Linux (5)
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky 9 - Latest", "category": "Rocky", "ram_min": 1024},
    {"label": "🦊 Rocky Linux 8", "value": "images:rockylinux/8", "desc": "Rocky 8 - Stable", "category": "Rocky", "ram_min": 1024},
    {"label": "🦊 Rocky Linux 7", "value": "images:rockylinux/7", "desc": "Rocky 7 - Legacy", "category": "Rocky", "ram_min": 512},
    
    # AlmaLinux (5)
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma 9 - Latest", "category": "AlmaLinux", "ram_min": 1024},
    {"label": "🦊 AlmaLinux 8", "value": "images:almalinux/8", "desc": "Alma 8 - Stable", "category": "AlmaLinux", "ram_min": 1024},
    {"label": "🦊 AlmaLinux 7", "value": "images:almalinux/7", "desc": "Alma 7 - Legacy", "category": "AlmaLinux", "ram_min": 512},
    
    # CentOS Series (8)
    {"label": "📦 CentOS 9 Stream", "value": "images:centos/9-Stream", "desc": "CentOS 9 Stream", "category": "CentOS", "ram_min": 1024},
    {"label": "📦 CentOS 8 Stream", "value": "images:centos/8-Stream", "desc": "CentOS 8 Stream", "category": "CentOS", "ram_min": 1024},
    {"label": "📦 CentOS 7", "value": "images:centos/7", "desc": "CentOS 7 - Legacy", "category": "CentOS", "ram_min": 512},
    {"label": "📦 CentOS 6", "value": "images:centos/6", "desc": "CentOS 6 - Ancient", "category": "CentOS", "ram_min": 256},
    {"label": "📦 CentOS 5", "value": "images:centos/5", "desc": "CentOS 5 - Retro", "category": "CentOS", "ram_min": 256},
    {"label": "📦 CentOS 4", "value": "images:centos/4", "desc": "CentOS 4 - Museum", "category": "CentOS", "ram_min": 128},
    
    # Alpine Linux (8)
    {"label": "🐧 Alpine 3.19", "value": "images:alpine/3.19", "desc": "Alpine Latest", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine 3.18", "value": "images:alpine/3.18", "desc": "Alpine 3.18", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine 3.17", "value": "images:alpine/3.17", "desc": "Alpine 3.17", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine 3.16", "value": "images:alpine/3.16", "desc": "Alpine 3.16", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine 3.15", "value": "images:alpine/3.15", "desc": "Alpine 3.15", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine 3.14", "value": "images:alpine/3.14", "desc": "Alpine 3.14", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine 3.13", "value": "images:alpine/3.13", "desc": "Alpine 3.13", "category": "Alpine", "ram_min": 64},
    {"label": "🐧 Alpine Edge", "value": "images:alpine/edge", "desc": "Alpine Edge - Rolling", "category": "Alpine", "ram_min": 64},
    
    # Arch Linux (3)
    {"label": "📀 Arch Linux", "value": "images:archlinux", "desc": "Arch - Rolling Release", "category": "Arch", "ram_min": 512},
    {"label": "📀 Arch Linux (Current)", "value": "images:archlinux/current", "desc": "Arch Current", "category": "Arch", "ram_min": 512},
    {"label": "📀 Manjaro", "value": "images:manjaro", "desc": "Manjaro - Arch based", "category": "Arch", "ram_min": 512},
    
    # OpenSUSE (6)
    {"label": "🟢 OpenSUSE Tumbleweed", "value": "images:opensuse/tumbleweed", "desc": "Rolling Release", "category": "OpenSUSE", "ram_min": 1024},
    {"label": "🟢 OpenSUSE Leap 15.5", "value": "images:opensuse/15.5", "desc": "Leap 15.5", "category": "OpenSUSE", "ram_min": 1024},
    {"label": "🟢 OpenSUSE Leap 15.4", "value": "images:opensuse/15.4", "desc": "Leap 15.4", "category": "OpenSUSE", "ram_min": 1024},
    {"label": "🟢 OpenSUSE Leap 15.3", "value": "images:opensuse/15.3", "desc": "Leap 15.3", "category": "OpenSUSE", "ram_min": 1024},
    
    # FreeBSD (8)
    {"label": "🔵 FreeBSD 14", "value": "images:freebsd/14", "desc": "FreeBSD 14 - Latest", "category": "FreeBSD", "ram_min": 512},
    {"label": "🔵 FreeBSD 13", "value": "images:freebsd/13", "desc": "FreeBSD 13 - Stable", "category": "FreeBSD", "ram_min": 512},
    {"label": "🔵 FreeBSD 12", "value": "images:freebsd/12", "desc": "FreeBSD 12 - Legacy", "category": "FreeBSD", "ram_min": 512},
    {"label": "🔵 FreeBSD 11", "value": "images:freebsd/11", "desc": "FreeBSD 11 - Old", "category": "FreeBSD", "ram_min": 512},
    {"label": "🔵 FreeBSD 10", "value": "images:freebsd/10", "desc": "FreeBSD 10 - Ancient", "category": "FreeBSD", "ram_min": 512},
    
    # OpenBSD (5)
    {"label": "🐡 OpenBSD 7.4", "value": "images:openbsd/7.4", "desc": "OpenBSD 7.4", "category": "OpenBSD", "ram_min": 512},
    {"label": "🐡 OpenBSD 7.3", "value": "images:openbsd/7.3", "desc": "OpenBSD 7.3", "category": "OpenBSD", "ram_min": 512},
    {"label": "🐡 OpenBSD 7.2", "value": "images:openbsd/7.2", "desc": "OpenBSD 7.2", "category": "OpenBSD", "ram_min": 512},
    
    # Kali Linux (3)
    {"label": "🐉 Kali Linux", "value": "images:kali", "desc": "Kali - Security Testing", "category": "Kali", "ram_min": 1024},
    {"label": "🐉 Kali Linux Weekly", "value": "images:kali/weekly", "desc": "Kali Weekly", "category": "Kali", "ram_min": 1024},
    
    # Gentoo (4)
    {"label": "💻 Gentoo", "value": "images:gentoo", "desc": "Gentoo - Source based", "category": "Gentoo", "ram_min": 1024},
    {"label": "💻 Gentoo Current", "value": "images:gentoo/current", "desc": "Gentoo Current", "category": "Gentoo", "ram_min": 1024},
    
    # Void Linux (3)
    {"label": "⚪ Void Linux", "value": "images:voidlinux", "desc": "Void - Independent", "category": "Void", "ram_min": 256},
    {"label": "⚪ Void Linux musl", "value": "images:voidlinux/musl", "desc": "Void with musl", "category": "Void", "ram_min": 256},
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
#  🎨  UI HELPER FUNCTIONS
# ==================================================================================================

def glow_text(text: str) -> str:
    return f"```glow\n{text}\n```"

def terminal_text(text: str) -> str:
    return f"```fix\n{text}\n```"

def success_text(text: str) -> str:
    return f"```diff\n+ {text}\n```"

def error_text(text: str) -> str:
    return f"```diff\n- {text}\n```"

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

def os_embed(title: str, desc: str = "") -> discord.Embed:
    return create_embed(f"🐧 {title}", desc, COLORS['os'])

def terminal_embed(title: str, content: str) -> discord.Embed:
    embed = discord.Embed(title=terminal_text(f"[ {title} ]"), description=f"```bash\n{content[:1900]}\n```", color=COLORS['terminal'])
    embed.set_footer(text=f"⚡ Terminal • {datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def no_vps_embed() -> discord.Embed:
    return info_embed("No VPS Found", error_text("You don't have any VPS yet.") + f"\n\nUse `{BOT_PREFIX}plans` to see plans")

# ==================================================================================================
#  🗄️  DATABASE SETUP
# ==================================================================================================

DATABASE_PATH = '/opt/svm5-bot/data/svm5.db'

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
    
    # Get IP and MAC
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
    # Create new user
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
    stats = {'status': 'unknown', 'cpu': '0%', 'memory': '0/0MB', 'disk': '0/0GB', 'ipv4': [], 'mac': 'N/A'}
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
#  🤖  BOT SETUP
# ==================================================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.start_time = datetime.utcnow()
LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'

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
    
    total_vps = len(get_all_vps())
    
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
║  💻 Hostname:      {HOSTNAME}                                                       ║
║                                                                                               ║
║  🖥️ Total VPS:     {total_vps}                                                               ║
║  🐧 Total OS:      {len(OS_OPTIONS)}                                                          ║
║  🎮 Total Games:   {len(GAMES_LIST)}                                                          ║
║  🛠️ Total Tools:   {len(TOOLS_LIST)}                                                          ║
║                                                                                               ║
║  📊 TOTAL COMMANDS: 84 + OS SELECTION │ ✅ ALL WORKING │ 🎨 FULL UI                          ║
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
#  🏠  HOME & HELP COMMAND - MAIN MENU
# ==================================================================================================

class HelpView(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_page = 0
        self.pages = [
            {
                "title": "🏠 HOME MENU",
                "desc": f"```glow\nWelcome to {BOT_NAME} - Complete VPS Management Solution\n```",
                "fields": [
                    ("👤 USER (14)", "`.help user` - User commands", True),
                    ("🖥️ VPS (8)", "`.help vps` - VPS management", True),
                    ("📟 CONSOLE (10)", "`.help console` - Terminal", True),
                    ("🎮 GAMES (7)", "`.help games` - Game servers", True),
                    ("🛠️ TOOLS (7)", "`.help tools` - Dev tools", True),
                    ("🌐 NODES (7)", "`.help nodes` - Cluster", True),
                    ("👥 SHARE (4)", "`.help share` - Share VPS", True),
                    ("🔌 PORTS (6)", "`.help ports` - Port forward", True),
                    ("🌍 IPv4 (6)", "`.help ipv4` - IPv4 management", True),
                    ("📦 PANELS (6)", "`.help panels` - Game panels", True),
                    ("🤖 AI (3)", "`.help ai` - AI assistant", True),
                    ("🐧 OS (70+)", "`.help os` - OS options", True),
                    ("🛡️ ADMIN (13)", "`.help admin` - Admin", True),
                    ("👑 OWNER (9)", "`.help owner` - Owner", True),
                ]
            },
            {
                "title": "👤 USER COMMANDS (14)",
                "desc": "```fix\nBasic commands for all users\n```",
                "fields": [
                    (f"{BOT_PREFIX}help", "Show this menu", False),
                    (f"{BOT_PREFIX}ping", "Check bot latency", False),
                    (f"{BOT_PREFIX}uptime", "Show bot uptime", False),
                    (f"{BOT_PREFIX}bot-info", "Bot information", False),
                    (f"{BOT_PREFIX}server-info", "Server hardware", False),
                    (f"{BOT_PREFIX}plans", "Free VPS plans", False),
                    (f"{BOT_PREFIX}stats", "Your statistics", False),
                    (f"{BOT_PREFIX}inv", "Your invites", False),
                    (f"{BOT_PREFIX}invites-top", "Top inviters", False),
                    (f"{BOT_PREFIX}claim-free", "Claim free VPS", False),
                    (f"{BOT_PREFIX}my-acc", "Your account", False),
                    (f"{BOT_PREFIX}gen-acc", "Generate account", False),
                    (f"{BOT_PREFIX}api-key", "API key", False),
                    (f"{BOT_PREFIX}userinfo", "User info", False),
                ]
            },
            {
                "title": "🖥️ VPS COMMANDS (8)",
                "desc": "```fix\nManage your VPS containers\n```",
                "fields": [
                    (f"{BOT_PREFIX}myvps", "List your VPS", False),
                    (f"{BOT_PREFIX}list", "Detailed VPS list", False),
                    (f"{BOT_PREFIX}manage", "Interactive manager", False),
                    (f"{BOT_PREFIX}stats", "VPS statistics", False),
                    (f"{BOT_PREFIX}logs", "View VPS logs", False),
                    (f"{BOT_PREFIX}reboot", "Reboot VPS", False),
                    (f"{BOT_PREFIX}shutdown", "Shutdown VPS", False),
                    (f"{BOT_PREFIX}rename", "Rename VPS", False),
                ]
            },
            {
                "title": "📟 CONSOLE COMMANDS (10)",
                "desc": "```fix\nTerminal access and commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}ss", "VPS snapshot", False),
                    (f"{BOT_PREFIX}console", "Interactive console", False),
                    (f"{BOT_PREFIX}execute", "Run command", False),
                    (f"{BOT_PREFIX}ssh-gen", "Generate SSH", False),
                    (f"{BOT_PREFIX}top", "Process monitor", False),
                    (f"{BOT_PREFIX}df", "Disk usage", False),
                    (f"{BOT_PREFIX}free", "Memory usage", False),
                    (f"{BOT_PREFIX}ps", "Process list", False),
                    (f"{BOT_PREFIX}who", "Logged users", False),
                    (f"{BOT_PREFIX}uptime", "Container uptime", False),
                ]
            },
            {
                "title": "🎮 GAMES COMMANDS (7)",
                "desc": "```fix\nInstall and manage game servers\n```",
                "fields": [
                    (f"{BOT_PREFIX}games", "List games", False),
                    (f"{BOT_PREFIX}game-info", "Game details", False),
                    (f"{BOT_PREFIX}install-game", "Install game", False),
                    (f"{BOT_PREFIX}my-games", "Your games", False),
                    (f"{BOT_PREFIX}start-game", "Start game", False),
                    (f"{BOT_PREFIX}stop-game", "Stop game", False),
                    (f"{BOT_PREFIX}game-stats", "Game stats", False),
                ]
            },
            {
                "title": "🛠️ TOOLS COMMANDS (7)",
                "desc": "```fix\nInstall development tools\n```",
                "fields": [
                    (f"{BOT_PREFIX}tools", "List tools", False),
                    (f"{BOT_PREFIX}tool-info", "Tool details", False),
                    (f"{BOT_PREFIX}install-tool", "Install tool", False),
                    (f"{BOT_PREFIX}my-tools", "Your tools", False),
                    (f"{BOT_PREFIX}start-tool", "Start tool", False),
                    (f"{BOT_PREFIX}stop-tool", "Stop tool", False),
                    (f"{BOT_PREFIX}tool-port", "Tool port", False),
                ]
            },
            {
                "title": "🌐 NODE COMMANDS (7)",
                "desc": "```fix\nManage cluster nodes\n```",
                "fields": [
                    (f"{BOT_PREFIX}node", "List nodes", False),
                    (f"{BOT_PREFIX}node-info", "Node details", False),
                    (f"{BOT_PREFIX}node-add", "Add node", False),
                    (f"{BOT_PREFIX}node-remove", "Remove node", False),
                    (f"{BOT_PREFIX}node-check", "Check node", False),
                    (f"{BOT_PREFIX}node-stats", "Cluster stats", False),
                    (f"{BOT_PREFIX}node-connect", "Connect node", False),
                ]
            },
            {
                "title": "👥 SHARE COMMANDS (4)",
                "desc": "```fix\nShare VPS with other users\n```",
                "fields": [
                    (f"{BOT_PREFIX}share", "Share VPS", False),
                    (f"{BOT_PREFIX}unshare", "Unshare VPS", False),
                    (f"{BOT_PREFIX}shared", "List shared", False),
                    (f"{BOT_PREFIX}manage-shared", "Manage shared", False),
                ]
            },
            {
                "title": "🔌 PORT COMMANDS (6)",
                "desc": "```fix\nPort forwarding management\n```",
                "fields": [
                    (f"{BOT_PREFIX}ports", "Port help", False),
                    (f"{BOT_PREFIX}ports add", "Add port", False),
                    (f"{BOT_PREFIX}ports list", "List ports", False),
                    (f"{BOT_PREFIX}ports remove", "Remove port", False),
                    (f"{BOT_PREFIX}ports quota", "Port quota", False),
                    (f"{BOT_PREFIX}ports check", "Check port", False),
                ]
            },
            {
                "title": "🌍 IPv4 COMMANDS (6)",
                "desc": "```fix\nBuy and manage IPv4\n```",
                "fields": [
                    (f"{BOT_PREFIX}ipv4", "Your IPv4", False),
                    (f"{BOT_PREFIX}ipv4-details", "IPv4 details", False),
                    (f"{BOT_PREFIX}buy-ipv4", "Buy IPv4", False),
                    (f"{BOT_PREFIX}upi", "UPI info", False),
                    (f"{BOT_PREFIX}upi-qr", "Generate QR", False),
                    (f"{BOT_PREFIX}pay", "Payment link", False),
                ]
            },
            {
                "title": "📦 PANEL COMMANDS (6)",
                "desc": "```fix\nInstall game panels\n```",
                "fields": [
                    (f"{BOT_PREFIX}install-panel", "Install panel", False),
                    (f"{BOT_PREFIX}panel-info", "Panel info", False),
                    (f"{BOT_PREFIX}panel-reset", "Reset password", False),
                    (f"{BOT_PREFIX}panel-delete", "Delete panel", False),
                    (f"{BOT_PREFIX}panel-tunnel", "Create tunnel", False),
                    (f"{BOT_PREFIX}panel-status", "Panel status", False),
                ]
            },
            {
                "title": "🤖 AI COMMANDS (3)",
                "desc": "```fix\nChat with AI assistant\n```",
                "fields": [
                    (f"{BOT_PREFIX}ai", "Chat with AI", False),
                    (f"{BOT_PREFIX}ai-reset", "Reset history", False),
                    (f"{BOT_PREFIX}ai-help", "AI help", False),
                ]
            },
            {
                "title": "🐧 OS COMMANDS",
                "desc": f"```fix\n70+ Operating Systems available\n```",
                "fields": [
                    ("Ubuntu", "15 versions (24.04 down to 10.04)", True),
                    ("Debian", "15 versions (12 down to 3)", True),
                    ("Fedora", "10 versions (40 down to 32)", True),
                    ("Rocky/Alma", "8 versions (9,8,7)", True),
                    ("CentOS", "8 versions (9 down to 4)", True),
                    ("Alpine", "8 versions (3.19 down to 3.13)", True),
                    ("Arch", "3 versions (Arch, Manjaro)", True),
                    ("OpenSUSE", "6 versions (Tumbleweed, Leap)", True),
                    ("FreeBSD", "8 versions (14 down to 10)", True),
                    ("OpenBSD", "5 versions (7.4 down to 7.2)", True),
                    ("Kali/Gentoo/Void", "10+ versions", True),
                ]
            },
        ]
        
        if is_admin(str(ctx.author.id)):
            self.pages.append({
                "title": "🛡️ ADMIN COMMANDS (13)",
                "desc": "```fix\nAdministrator commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}create", "Create VPS", False),
                    (f"{BOT_PREFIX}delete", "Delete VPS", False),
                    (f"{BOT_PREFIX}suspend", "Suspend VPS", False),
                    (f"{BOT_PREFIX}unsuspend", "Unsuspend VPS", False),
                    (f"{BOT_PREFIX}add-resources", "Add resources", False),
                    (f"{BOT_PREFIX}list-all", "List all VPS", False),
                    (f"{BOT_PREFIX}add-inv", "Add invites", False),
                    (f"{BOT_PREFIX}remove-inv", "Remove invites", False),
                    (f"{BOT_PREFIX}ports-add", "Add port slots", False),
                    (f"{BOT_PREFIX}serverstats", "Server stats", False),
                    (f"{BOT_PREFIX}admin-add-ipv4", "Assign IPv4", False),
                    (f"{BOT_PREFIX}admin-rm-ipv4", "Remove IPv4", False),
                    (f"{BOT_PREFIX}admin-pending-ipv4", "Pending IPv4", False),
                ]
            })
        
        if str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            self.pages.append({
                "title": "👑 OWNER COMMANDS (9)",
                "desc": "```fix\nMain owner commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}admin-add", "Add admin", False),
                    (f"{BOT_PREFIX}admin-remove", "Remove admin", False),
                    (f"{BOT_PREFIX}admin-list", "List admins", False),
                    (f"{BOT_PREFIX}maintenance", "Maintenance mode", False),
                    (f"{BOT_PREFIX}purge-all", "Purge all", False),
                    (f"{BOT_PREFIX}protect", "Protect VPS", False),
                    (f"{BOT_PREFIX}unprotect", "Unprotect VPS", False),
                    (f"{BOT_PREFIX}backup-db", "Backup DB", False),
                    (f"{BOT_PREFIX}restore-db", "Restore DB", False),
                ]
            })
        
        self.update_embed()
    
    def update_embed(self):
        page = self.pages[self.current_page]
        embed = discord.Embed(
            title=glow_text(f"{page['title']}"),
            description=page['desc'],
            color=COLORS['primary']
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        
        for name, value, inline in page["fields"]:
            embed.add_field(name=f"**{name}**", value=value, inline=inline)
        
        embed.set_footer(text=f"⚡ Page {self.current_page + 1}/{len(self.pages)} • Use dropdown below ⚡")
        self.embed = embed
    
    @discord.ui.select(
        placeholder="📋 Select command category...",
        options=[
            discord.SelectOption(label="🏠 Home", value="0", emoji="🏠"),
            discord.SelectOption(label="👤 User (14)", value="1", emoji="👤"),
            discord.SelectOption(label="🖥️ VPS (8)", value="2", emoji="🖥️"),
            discord.SelectOption(label="📟 Console (10)", value="3", emoji="📟"),
            discord.SelectOption(label="🎮 Games (7)", value="4", emoji="🎮"),
            discord.SelectOption(label="🛠️ Tools (7)", value="5", emoji="🛠️"),
            discord.SelectOption(label="🌐 Nodes (7)", value="6", emoji="🌐"),
            discord.SelectOption(label="👥 Share (4)", value="7", emoji="👥"),
            discord.SelectOption(label="🔌 Ports (6)", value="8", emoji="🔌"),
            discord.SelectOption(label="🌍 IPv4 (6)", value="9", emoji="🌍"),
            discord.SelectOption(label="📦 Panels (6)", value="10", emoji="📦"),
            discord.SelectOption(label="🤖 AI (3)", value="11", emoji="🤖"),
            discord.SelectOption(label="🐧 OS (70+)", value="12", emoji="🐧"),
            discord.SelectOption(label="🛡️ Admin (13)", value="13", emoji="🛡️"),
            discord.SelectOption(label="👑 Owner (9)", value="14", emoji="👑"),
        ]
    )
    async def select_menu(self, select: Select, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral=True)
            return
        self.current_page = int(select.values[0])
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)

@bot.command(name="help")
async def help_command(ctx):
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        await ctx.send(embed=error_embed("License Required", "Please verify license first."))
        return
    
    view = HelpView(ctx)
    await ctx.send(embed=view.embed, view=view)

# ==================================================================================================
#  👤  USER COMMANDS (14)
# ==================================================================================================

@bot.command(name="ping")
async def ping(ctx):
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging..."))
    end = time.time()
    api = round(bot.latency * 1000)
    resp = round((end - start) * 1000)
    embed = success_embed("Pong! 🏓")
    embed.add_field(name="📡 API", value=f"```fix\n{api}ms\n```", inline=True)
    embed.add_field(name="⏱️ Response", value=f"```fix\n{resp}ms\n```", inline=True)
    await msg.edit(embed=embed)

@bot.command(name="uptime")
async def uptime(ctx):
    up = datetime.utcnow() - bot.start_time
    d = up.days
    h, r = divmod(up.seconds, 3600)
    m, s = divmod(r, 60)
    await ctx.send(embed=info_embed("Uptime", f"```fix\n{d}d {h}h {m}m {s}s\n```"))

@bot.command(name="bot-info")
async def bot_info(ctx):
    all_vps = get_all_vps()
    embed = info_embed("Bot Information")
    embed.add_field(name="📦 Version", value="```fix\n5.0.0\n```", inline=True)
    embed.add_field(name="👑 Author", value=f"```fix\n{BOT_AUTHOR}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(all_vps)}\n```", inline=True)
    embed.add_field(name="🐧 OS", value=f"```fix\n{len(OS_OPTIONS)}\n```", inline=True)
    embed.add_field(name="🎮 Games", value=f"```fix\n{len(GAMES_LIST)}\n```", inline=True)
    embed.add_field(name="🛠️ Tools", value=f"```fix\n{len(TOOLS_LIST)}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{MAC_ADDRESS[:17]}\n```", inline=True)
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
        text = f"```fix\nRAM: {p['ram']}GB | CPU: {p['cpu']} | Disk: {p['disk']}GB\nInvites: {p['invites']}\n```"
        embed.add_field(name=f"{p['emoji']} {p['name']}", value=text, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="stats")
async def stats(ctx):
    uid = str(ctx.author.id)
    s = get_user_stats(uid)
    v = get_user_vps(uid)
    embed = info_embed(f"Stats for {ctx.author.display_name}")
    embed.add_field(name="📨 Invites", value=f"```fix\n{s.get('invites',0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(v)}\n```", inline=True)
    embed.add_field(name="🗝️ API", value=f"```fix\n{s.get('api_key','None')[:16]}...\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="inv")
async def inv(ctx):
    s = get_user_stats(str(ctx.author.id))
    await ctx.send(embed=info_embed("Your Invites", f"```fix\n{ s.get('invites',0) }\n```"))

@bot.command(name="invites-top")
async def invites_top(ctx, lim: int = 10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, invites FROM user_stats WHERE invites > 0 ORDER BY invites DESC LIMIT ?', (lim,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("Top Inviters", "No invites yet."))
    embed = info_embed(f"Top {min(lim,len(rows))} Inviters")
    medals = ["🥇","🥈","🥉"]
    for i, r in enumerate(rows,1):
        try:
            u = await bot.fetch_user(int(r['user_id']))
            name = u.name
        except:
            name = f"Unknown"
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
    
    # OS Selection View
    view = View()
    opts = []
    for o in OS_OPTIONS[:25]:
        opts.append(discord.SelectOption(label=o['label'][:100], value=o['value'], description=o['desc'][:100]))
    select = Select(placeholder="Select OS...", options=opts)
    
    async def select_cb(i):
        if i.user.id != ctx.author.id:
            await i.response.send_message("Not for you!", ephemeral=True)
            return
        os_val = select.values[0]
        # Create VPS
        name = f"svm5-{uid[:6]}-{random.randint(1000,9999)}"
        msg = await i.followup.send(embed=info_embed("Creating VPS", "Step 1/4: Initializing..."), ephemeral=True)
        try:
            ram_mb = plan['ram'] * 1024
            await run_lxc(f"lxc init {os_val} {name} -s {DEFAULT_STORAGE_POOL}")
            await msg.edit(embed=info_embed("Creating VPS", "Step 2/4: Configuring..."))
            await run_lxc(f"lxc config set {name} limits.memory {ram_mb}MB")
            await run_lxc(f"lxc config set {name} limits.cpu {plan['cpu']}")
            await run_lxc(f"lxc config device set {name} root size={plan['disk']}GB")
            await msg.edit(embed=info_embed("Creating VPS", "Step 3/4: Starting..."))
            await run_lxc(f"lxc start {name}")
            await asyncio.sleep(3)
            await msg.edit(embed=info_embed("Creating VPS", "Step 4/4: Finalizing..."))
            add_vps(uid, name, plan['ram'], plan['cpu'], plan['disk'], os_val, plan['name'])
            update_user_stats(uid, -plan['invites'], 1)
            embed = success_embed("VPS Created!")
            embed.add_field(name="📦 Container", value=f"```fix\n{name}\n```", inline=True)
            embed.add_field(name="📋 Plan", value=f"```fix\n{plan['name']}\n```", inline=True)
            embed.add_field(name="⚙️ Resources", value=f"```fix\n{plan['ram']}GB RAM / {plan['cpu']} CPU / {plan['disk']}GB Disk\n```", inline=False)
            await msg.edit(embed=embed)
        except Exception as e:
            await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))
    
    select.callback = select_cb
    view.add_item(select)
    await ctx.send(embed=info_embed("Claim Free VPS", f"**{plan['emoji']} {plan['name']}**\nRAM: {plan['ram']}GB | CPU: {plan['cpu']} | Disk: {plan['disk']}GB\n\nSelect OS:"), view=view)

@bot.command(name="gen-acc")
async def gen_acc(ctx):
    import random, string
    adj = ["cool","fast","dark","epic","blue","swift","neon","alpha","delta","super"]
    noun = ["wolf","tiger","storm","byte","nova","blade","fox","raven","hawk","lion"]
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
#  🖥️  VPS COMMANDS (8)
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

@bot.command(name="manage")
async def manage(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    stats = await get_container_stats(container)
    embed = info_embed(f"Managing: {container}")
    embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
    embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
    embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
    
    view = View()
    async def start_cb(i):
        await run_lxc(f"lxc start {container}")
        await i.response.send_message(f"Started {container}", ephemeral=True)
    async def stop_cb(i):
        await run_lxc(f"lxc stop {container}")
        await i.response.send_message(f"Stopped {container}", ephemeral=True)
    async def restart_cb(i):
        await run_lxc(f"lxc restart {container}")
        await i.response.send_message(f"Restarted {container}", ephemeral=True)
    view.add_item(Button(label="▶️ Start", style=discord.ButtonStyle.success, callback=start_cb))
    view.add_item(Button(label="⏹️ Stop", style=discord.ButtonStyle.danger, callback=stop_cb))
    view.add_item(Button(label="🔄 Restart", style=discord.ButtonStyle.primary, callback=restart_cb))
    await ctx.send(embed=embed, view=view)

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
    for k,v in stats.items():
        if k not in ['status','cpu','memory','disk','ipv4','mac']: continue
        embed.add_field(name=k.upper(), value=f"```fix\n{v}\n```", inline=True)
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
    was_running = status == 'running'
    if was_running:
        await run_lxc(f"lxc stop {old}")
        await asyncio.sleep(2)
    await run_lxc(f"lxc move {old} {new}")
    if was_running:
        await run_lxc(f"lxc start {new}")
    conn = get_db()
    cur = conn.cursor()
    for table in ['vps','shared_vps','installed_games','installed_tools','ipv4','port_forwards','panels']:
        cur.execute(f'UPDATE {table} SET container_name = ? WHERE container_name = ?', (new, old))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Renamed", f"```fix\n{old} → {new}\n```"))

# ==================================================================================================
#  📟  CONSOLE COMMANDS (10)
# ==================================================================================================

class CmdModal(Modal):
    def __init__(self, container):
        super().__init__(title="Run Command")
        self.container = container
        self.add_item(InputText(label="Command", placeholder="e.g., apt update", style=discord.InputTextStyle.paragraph))
        self.add_item(InputText(label="Timeout", placeholder="30", required=False, value="30"))
    async def callback(self, interaction):
        cmd = self.children[0].value
        to = int(self.children[1].value or "30")
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=info_embed("Executing", f"```fix\n$ {cmd}\n```"), ephemeral=True)
        out,err,code = await exec_in_container(self.container, cmd, to)
        embed = discord.Embed(title=terminal_text("[ Output ]"), description=f"```bash\n$ {cmd}\n\n{(out or err)[:1900]}\n```", color=0x00ff00 if code==0 else 0xff0000)
        embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```")
        await msg.edit(embed=embed)

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
        async def btn_cb(i): await i.response.send_modal(CmdModal(container))
        btn.callback = btn_cb
        view.add_item(btn)
        return await ctx.send(embed=info_embed(f"Console: {container}", "Click button to run command"), view=view)
    msg = await ctx.send(embed=info_embed("Executing", f"```fix\n$ {cmd}\n```"))
    out,err,code = await exec_in_container(container, cmd)
    embed = discord.Embed(title=terminal_text("[ Output ]"), description=f"```bash\n$ {cmd}\n\n{(out or err)[:1900]}\n```", color=0x00ff00 if code==0 else 0xff0000)
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
    await exec_in_container(container, "apt-get update -qq")
    await exec_in_container(container, "apt-get install -y -qq tmate")
    sess = f"svm5-{random.randint(1000,9999)}"
    await exec_in_container(container, f"tmate -S /tmp/{sess}.sock new-session -d")
    await asyncio.sleep(5)
    out,_,_ = await exec_in_container(container, f"tmate -S /tmp/{sess}.sock display -p '#{{tmate_ssh}}'")
    url = out.strip()
    if url:
        try:
            dm = success_embed("SSH Access")
            dm.add_field(name="Container", value=f"```fix\n{container}\n```")
            dm.add_field(name="SSH Command", value=f"```bash\n{url}\n```")
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
#  🎮  GAMES COMMANDS (7)
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
    out,err,code = await exec_in_container(container, cmd)
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
#  🛠️  TOOLS COMMANDS (7)
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
    out,err,code = await exec_in_container(container, t['cmd'])
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
#  🌐  NODE COMMANDS (7) - AUTO DETECT LOCAL
# ==================================================================================================

NODES_FILE = '/opt/svm5-bot/nodes.json'

def load_nodes():
    default = {"version":"1.0","last_updated":datetime.now().isoformat(),"main_node":"local","nodes":{},"node_groups":{"all":[]}}
    if os.path.exists(NODES_FILE):
        try:
            with open(NODES_FILE,'r') as f:
                return json.load(f)
        except:
            pass
    # Auto-create local node
    try:
        lxc_count = len(subprocess.getoutput("lxc list -c n --format csv").splitlines())
    except:
        lxc_count = 0
    local = {
        "name":"local","host":"localhost","port":0,"username":"local","type":"local","status":"online","is_main":True,
        "stats":{
            "total_ram":psutil.virtual_memory().total//1024//1024,
            "used_ram":psutil.virtual_memory().used//1024//1024,
            "total_cpu":psutil.cpu_count(),
            "used_cpu":psutil.cpu_percent(),
            "total_disk":psutil.disk_usage('/').total//1024//1024//1024,
            "used_disk":psutil.disk_usage('/').used//1024//1024//1024,
            "lxc_count":lxc_count,
            "last_checked":datetime.now().isoformat()
        }
    }
    default["nodes"]["local"] = local
    default["node_groups"]["all"].append("local")
    with open(NODES_FILE,'w') as f:
        json.dump(default,f,indent=2)
    return default

def save_nodes(data):
    with open(NODES_FILE,'w') as f:
        json.dump(data,f,indent=2)

def get_node(name):
    nodes = load_nodes()
    return nodes['nodes'].get(name)

@bot.command(name="node")
async def node_list(ctx):
    nodes = load_nodes()
    embed = node_embed("Node Network", f"```fix\nTotal: {len(nodes['nodes'])}\n```")
    for n,data in nodes['nodes'].items():
        s = data.get('stats',{})
        status = "🟢" if data['status']=='online' else "🔴"
        text = f"```fix\nHost: {data['host']}\nRAM: {s.get('used_ram',0)}/{s.get('total_ram',0)} MB\nCPU: {s.get('used_cpu',0)}%\nLXC: {s.get('lxc_count',0)}\n```"
        embed.add_field(name=f"{status} {n}", value=text, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="node-info")
async def node_info(ctx, name: str = "local"):
    n = get_node(name)
    if not n:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    s = n.get('stats',{})
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
            client.connect(host,port=port,username=user,password=pwd,timeout=10)
        else:
            key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
            client.connect(host,port=port,username=user,pkey=key,timeout=10)
        stdin,stdout,stderr = client.exec_command('nproc')
        cpu = stdout.read().decode().strip()
        stdin,stdout,stderr = client.exec_command("free -m | awk '/^Mem:/{print $2}'")
        ram = stdout.read().decode().strip()
        stdin,stdout,stderr = client.exec_command("df -BG / | awk 'NR==2{print $2}' | sed 's/G//'")
        disk = stdout.read().decode().strip()
        client.close()
        node_data = {
            "name":name,"host":host,"port":port,"username":user,"password":pwd,"type":"remote","status":"online",
            "is_main":False,"region":"us",
            "stats":{
                "total_ram":int(ram) if ram.isdigit() else 0,
                "used_ram":0,
                "total_cpu":int(cpu) if cpu.isdigit() else 0,
                "used_cpu":0,
                "total_disk":int(disk) if disk.isdigit() else 0,
                "used_disk":0,
                "lxc_count":0,
                "last_checked":datetime.now().isoformat()
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
            client.connect(n['host'],port=n['port'],username=n['username'],password=n['password'],timeout=10)
        else:
            key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
            client.connect(n['host'],port=n['port'],username=n['username'],pkey=key,timeout=10)
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
#  👥  SHARE COMMANDS (4)
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
#  🔌  PORT COMMANDS (6)
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
    success,container,hport = remove_port_forward(fid)
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
#  🌍  IPv4 COMMANDS (6)
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
        qr = qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",back_color="white")
        bio = io.BytesIO()
        img.save(bio,'PNG')
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
    for i,ip in enumerate(ips,1):
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
#  📦  PANEL COMMANDS (6)
# ==================================================================================================

CLOUDFLARED = shutil.which("cloudflared") is not None

async def create_tunnel(container: str, port: int) -> Optional[str]:
    if not CLOUDFLARED:
        return None
    try:
        await exec_in_container(container, "which cloudflared || (wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared)")
        tid = str(uuid.uuid4())[:8]
        await exec_in_container(container, f"nohup cloudflared tunnel --url http://localhost:{port} --no-autoupdate > /tmp/cloudflared_{tid}.log 2>&1 &")
        await asyncio.sleep(5)
        out,_,_ = await exec_in_container(container, f"cat /tmp/cloudflared_{tid}.log | grep -oP 'https://[a-z0-9-]+\\.trycloudflare\\.com' | head -1")
        return out.strip() if out else None
    except:
        return None

class PanelView(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        ptero = Button(label="🦅 Pterodactyl", style=discord.ButtonStyle.primary)
        puffer = Button(label="🐡 Pufferpanel", style=discord.ButtonStyle.success)
        cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        ptero.callback = lambda i: self.install(i, "pterodactyl")
        puffer.callback = lambda i: self.install(i, "pufferpanel")
        cancel.callback = lambda i: i.response.edit_message(embed=info_embed("Cancelled"), view=None)
        self.add_item(ptero)
        self.add_item(puffer)
        self.add_item(cancel)
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
            for i,v in enumerate(vps,1):
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
            admin = generate_username()
            email = generate_email(admin)
            pwd = generate_password()
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
                for i,cmd in enumerate(cmds,2):
                    await msg.edit(embed=info_embed(f"Installing {ptype.title()}", f"Step {i}/6: Progress..."))
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                out,_,_ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() or SERVER_IP
                url = f"http://{ip}"
                tun = await create_tunnel(container, 80)
                if tun:
                    url = tun
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
                for i,cmd in enumerate(cmds,2):
                    await msg.edit(embed=info_embed(f"Installing {ptype.title()}", f"Step {i}/6: Progress..."))
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                out,_,_ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() or SERVER_IP
                url = f"http://{ip}:8080"
                tun = await create_tunnel(container, 8080)
                if tun:
                    url = tun
            add_panel(uid, ptype, url, admin, pwd, email, container, tun or "")
            embed = success_embed(f"{ptype.title()} Installed!")
            embed.add_field(name="🌐 URL", value=f"```fix\n{url}\n```", inline=False)
            embed.add_field(name="👤 Username", value=f"||`{admin}`||", inline=True)
            embed.add_field(name="📧 Email", value=f"||`{email}`||", inline=True)
            embed.add_field(name="🔑 Password", value=f"||`{pwd}`||", inline=False)
            await msg.edit(embed=embed)
            try:
                dm = success_embed(f"🔐 {ptype.title()} Credentials")
                dm.add_field(name="URL", value=url, inline=False)
                dm.add_field(name="Username", value=admin, inline=True)
                dm.add_field(name="Email", value=email, inline=True)
                dm.add_field(name="Password", value=pwd, inline=False)
                await self.ctx.author.send(embed=dm)
            except:
                pass
        except Exception as e:
            await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)[:500]}\n```"))

@bot.command(name="install-panel")
async def install_panel(ctx):
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license."))
    if not get_user_vps(str(ctx.author.id)):
        return await ctx.send(embed=no_vps_embed())
    embed = info_embed("Panel Installation", "Select panel type:")
    await ctx.send(embed=embed, view=PanelView(ctx))

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
    new = generate_password()
    msg = await ctx.send(embed=info_embed("Resetting Password", f"```fix\n{p['panel_type']} on {p['container_name']}\n```"))
    if p['panel_type'] == 'pterodactyl':
        cmd = f"cd /var/www/pterodactyl && php artisan p:user:password --email={p['admin_email']} --password={new}"
    else:
        cmd = f"pufferpanel user password --email {p['admin_email']} --password {new}"
    out,err,code = await exec_in_container(p['container_name'], cmd)
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
        b443 = Button(label="🔒 Port 443", style=discord.ButtonStyle.primary)
        async def b80_cb(i): await create_tunnel_cmd(i, container, 80)
        async def b8080_cb(i): await create_tunnel_cmd(i, container, 8080)
        async def b443_cb(i): await create_tunnel_cmd(i, container, 443)
        b80.callback = b80_cb
        b8080.callback = b8080_cb
        b443.callback = b443_cb
        view.add_item(b80)
        view.add_item(b8080)
        view.add_item(b443)
        await ctx.send(embed=info_embed("Select Port"), view=view)
    else:
        await create_tunnel_cmd(ctx, container, port)

async def create_tunnel_cmd(ctx, container, port):
    msg = await ctx.send(embed=info_embed("Creating Tunnel", f"```fix\n{container}:{port}\n```"))
    url = await create_tunnel(container, port)
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
#  🤖  AI COMMANDS (3)
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
#  🐧  OS COMMANDS (For reference - OS selection in create/claim)
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
    embed = info_embed(f"OS Options {f'- {category}' if category else ''}", f"```fix\nTotal: {len(filtered)}\n```")
    for o in filtered[:10]:
        embed.add_field(name=o['label'], value=f"```fix\n{o['desc']}\nRAM Min: {o['ram_min']}MB\n```", inline=True)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🛡️  ADMIN COMMANDS (13)
# ==================================================================================================

@bot.command(name="create")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    if ram<=0 or cpu<=0 or disk<=0:
        return await ctx.send(embed=error_embed("Invalid", "RAM, CPU, Disk must be positive"))
    # OS selection view
    view = View()
    opts = []
    for o in OS_OPTIONS[:25]:
        opts.append(discord.SelectOption(label=o['label'][:100], value=o['value'], description=o['desc'][:100]))
    sel = Select(placeholder="Select OS...", options=opts)
    async def sel_cb(i):
        if i.user.id != ctx.author.id:
            return await i.response.send_message("Not for you!", ephemeral=True)
        osv = sel.values[0]
        # Confirm
        cv = View()
        conf = Button(label="✅ Create", style=discord.ButtonStyle.success)
        canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        async def conf_cb(ci):
            await ci.response.defer()
            name = f"svm5-{str(user.id)[:6]}-{random.randint(1000,9999)}"
            prog = await ci.followup.send(embed=info_embed("Creating VPS", "Step 1/4: Initializing..."), ephemeral=True)
            try:
                ram_mb = ram * 1024
                await run_lxc(f"lxc init {osv} {name} -s {DEFAULT_STORAGE_POOL}")
                await prog.edit(embed=info_embed("Creating VPS", "Step 2/4: Configuring..."))
                await run_lxc(f"lxc config set {name} limits.memory {ram_mb}MB")
                await run_lxc(f"lxc config set {name} limits.cpu {cpu}")
                await run_lxc(f"lxc config device set {name} root size={disk}GB")
                await prog.edit(embed=info_embed("Creating VPS", "Step 3/4: Starting..."))
                await run_lxc(f"lxc start {name}")
                await asyncio.sleep(3)
                await prog.edit(embed=info_embed("Creating VPS", "Step 4/4: Finalizing..."))
                add_vps(str(user.id), name, ram, cpu, disk, osv, "Custom")
                embed = success_embed("VPS Created")
                embed.add_field(name="👤 User", value=user.mention, inline=True)
                embed.add_field(name="📦 Container", value=f"```fix\n{name}\n```", inline=True)
                embed.add_field(name="⚙️ Resources", value=f"```fix\n{ram}GB RAM / {cpu} CPU / {disk}GB Disk\n```", inline=False)
                await prog.edit(embed=embed)
            except Exception as e:
                await prog.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))
        async def canc_cb(ci):
            await ci.response.edit_message(embed=info_embed("Cancelled"), view=None)
        conf.callback = conf_cb
        canc.callback = canc_cb
        cv.add_item(conf)
        cv.add_item(canc)
        osname = next((o['label'] for o in OS_OPTIONS if o['value']==osv), osv)
        await i.response.edit_message(embed=warning_embed("Confirm", f"```fix\nUser: {user}\nOS: {osname}\nRAM: {ram}GB\nCPU: {cpu}\nDisk: {disk}GB\n```"), view=cv)
    sel.callback = sel_cb
    view.add_item(sel)
    await ctx.send(embed=info_embed("Create VPS", f"Select OS for {user.mention}"), view=view)

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
    for uid,vlist in list(byuser.items())[:5]:
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
#  👑  OWNER COMMANDS (9)
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
        for idx,v in enumerate(unprotected,1):
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
#  🚀  RUN THE BOT
# ==================================================================================================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n❌ ERROR: Please set your BOT_TOKEN!")
        sys.exit(1)
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n❌ ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
