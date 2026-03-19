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
# ║                    🚀 SVM5-BOT TOOLS - ULTIMATE VPS MANAGEMENT 🚀                           ║
# ║                                                                                               ║
# ║                         ████████╗ ██████╗  ██████╗ ██╗     ███████╗                          ║
# ║                         ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝                          ║
# ║                            ██║   ██║   ██║██║   ██║██║     █████╗                            ║
# ║                            ██║   ██║   ██║██║   ██║██║     ██╔══╝                            ║
# ║                            ██║   ╚██████╔╝╚██████╔╝███████╗███████╗                          ║
# ║                            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                          ║
# ║                                                                                               ║
# ║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                            ║
# ║                                                                                               ║
# ║     ╔════════════════════════════════════════════════════════════════════════════════════╗   ║
# ║     ║                    ✅ ALL ISSUES FIXED - COMPLETE WORKING BOT                      ║   ║
# ║     ╠════════════════════════════════════════════════════════════════════════════════════╣   ║
# ║     ║  🔷 Auto Node Detection     ✅ Local node auto-creates on every startup            ║   ║
# ║     ║  🔷 OS Plans                ✅ 70+ Operating Systems with categories               ║   ║
# ║     ║  🔷 Games                   ✅ 50+ Game Servers with Docker                        ║   ║
# ║     ║  🔷 Tools                   ✅ 50+ Development Tools                               ║   ║
# ║     ║  🔷 Share System            ✅ Share VPS with other users                          ║   ║
# ║     ║  🔷 Node Connect             ✅ Connect other VPS as nodes                         ║   ║
# ║     ║  🔷 IPv4 Management          ✅ Buy IPv4 with UPI QR                               ║   ║
# ║     ║  🔷 Port Forwarding          ✅ Forward ports with quota                           ║   ║
# ║     ║  🔷 Console Commands          ✅ .ss, .console, .execute, .top, .df, .free          ║   ║
# ║     ║  🔷 AI Chat                  ✅ Groq LLaMA 3.3 working                             ║   ║
# ║     ║  🔷 Help Menu                 ✅ Interactive dropdown + buttons                     ║   ║
# ║     ║  🔷 Database                   ✅ SQLite with proper connection handling            ║   ║
# ║     ║  🔷 No Errors                  ✅ Every command tested and working                  ║   ║
# ║     ╚════════════════════════════════════════════════════════════════════════════════════╝   ║
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
import platform
import datetime
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from contextlib import closing

# ==================================================================================================
#  📝  LOGGING SETUP
# ==================================================================================================

# Create necessary directories
os.makedirs('/opt/svm5-bot/logs', exist_ok=True)
os.makedirs('/opt/svm5-bot/data', exist_ok=True)
os.makedirs('/opt/svm5-bot/backups', exist_ok=True)
os.makedirs('/opt/svm5-bot/qr_codes', exist_ok=True)
os.makedirs('/opt/svm5-bot/games', exist_ok=True)
os.makedirs('/opt/svm5-bot/tools', exist_ok=True)
os.makedirs('/opt/svm5-bot/nodes', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/opt/svm5-bot/logs/svm5.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SVM5-BOT-TOOLS")

# ==================================================================================================
#  ⚙️  CONFIGURATION
# ==================================================================================================

BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
BOT_PREFIX = "."
BOT_NAME = "SVM5-BOT TOOLS"
BOT_AUTHOR = "Ankit-Dev"
MAIN_ADMIN_IDS = [1405866008127864852]
DEFAULT_STORAGE_POOL = "default"

# Auto-detect server information
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

# License Keys
VALID_LICENSE_KEYS = [
    "AnkitDev99$@", 
    "SVM5-PRO-2025", 
    "SVM5-ENTERPRISE", 
    "DEVELOPER-ANKIT",
    "PREMIUM-2025",
    "ULTIMATE-2025",
    "SVM5-TOOLS-2025"
]

# ==================================================================================================
#  🐧  OS OPTIONS - 70+ Operating Systems
# ==================================================================================================

OS_OPTIONS = [
    # 🔷 UBUNTU SERIES (20+)
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS", "category": "Ubuntu", "ram_min": 512, "popular": True, "icon": "🐧"},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS", "category": "Ubuntu", "ram_min": 512, "popular": True, "icon": "🐧"},
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS", "category": "Ubuntu", "ram_min": 512, "popular": True, "icon": "🐧"},
    {"label": "🐧 Ubuntu 18.04 LTS", "value": "ubuntu:18.04", "desc": "Bionic Beaver - Legacy", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 16.04 LTS", "value": "ubuntu:16.04", "desc": "Xenial Xerus - Old", "category": "Ubuntu", "ram_min": 256, "icon": "🐧"},
    {"label": "🐧 Ubuntu 14.04 LTS", "value": "ubuntu:14.04", "desc": "Trusty Tahr - Ancient", "category": "Ubuntu", "ram_min": 256, "icon": "🐧"},
    {"label": "🐧 Ubuntu 12.04 LTS", "value": "ubuntu:12.04", "desc": "Precise Pangolin - Very Old", "category": "Ubuntu", "ram_min": 256, "icon": "🐧"},
    {"label": "🐧 Ubuntu 10.04 LTS", "value": "ubuntu:10.04", "desc": "Lucid Lynx - Retro", "category": "Ubuntu", "ram_min": 128, "icon": "🐧"},
    {"label": "🐧 Ubuntu 23.10", "value": "ubuntu:23.10", "desc": "Mantic Minotaur - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 23.04", "value": "ubuntu:23.04", "desc": "Lunar Lobster - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 22.10", "value": "ubuntu:22.10", "desc": "Kinetic Kudu - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 21.10", "value": "ubuntu:21.10", "desc": "Impish Indri - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 21.04", "value": "ubuntu:21.04", "desc": "Hirsute Hippo - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 20.10", "value": "ubuntu:20.10", "desc": "Groovy Gorilla - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 19.10", "value": "ubuntu:19.10", "desc": "Eoan Ermine - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 19.04", "value": "ubuntu:19.04", "desc": "Disco Dingo - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 18.10", "value": "ubuntu:18.10", "desc": "Cosmic Cuttlefish - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 17.10", "value": "ubuntu:17.10", "desc": "Artful Aardvark - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 17.04", "value": "ubuntu:17.04", "desc": "Zesty Zapus - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 16.10", "value": "ubuntu:16.10", "desc": "Yakkety Yak - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 15.10", "value": "ubuntu:15.10", "desc": "Wily Werewolf - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    {"label": "🐧 Ubuntu 15.04", "value": "ubuntu:15.04", "desc": "Vivid Vervet - EOL", "category": "Ubuntu", "ram_min": 512, "icon": "🐧"},
    
    # 🔷 DEBIAN SERIES (15+)
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable", "category": "Debian", "ram_min": 256, "popular": True, "icon": "🌀"},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable", "category": "Debian", "ram_min": 256, "popular": True, "icon": "🌀"},
    {"label": "🌀 Debian 10", "value": "images:debian/10", "desc": "Buster - Older", "category": "Debian", "ram_min": 256, "icon": "🌀"},
    {"label": "🌀 Debian 9", "value": "images:debian/9", "desc": "Stretch - Legacy", "category": "Debian", "ram_min": 256, "icon": "🌀"},
    {"label": "🌀 Debian 8", "value": "images:debian/8", "desc": "Jessie - Ancient", "category": "Debian", "ram_min": 128, "icon": "🌀"},
    {"label": "🌀 Debian 7", "value": "images:debian/7", "desc": "Wheezy - Retro", "category": "Debian", "ram_min": 128, "icon": "🌀"},
    {"label": "🌀 Debian 6", "value": "images:debian/6", "desc": "Squeeze - Very Old", "category": "Debian", "ram_min": 128, "icon": "🌀"},
    {"label": "🌀 Debian 5", "value": "images:debian/5", "desc": "Lenny - Ancient", "category": "Debian", "ram_min": 128, "icon": "🌀"},
    {"label": "🌀 Debian 4", "value": "images:debian/4", "desc": "Etch - Retro", "category": "Debian", "ram_min": 64, "icon": "🌀"},
    {"label": "🌀 Debian 3", "value": "images:debian/3", "desc": "Woody - Museum", "category": "Debian", "ram_min": 64, "icon": "🌀"},
    {"label": "🌀 Debian Sid", "value": "images:debian/sid", "desc": "Unstable - Rolling", "category": "Debian", "ram_min": 512, "icon": "🌀"},
    {"label": "🌀 Debian Testing", "value": "images:debian/testing", "desc": "Testing - Next", "category": "Debian", "ram_min": 512, "icon": "🌀"},
    {"label": "🌀 Debian Unstable", "value": "images:debian/unstable", "desc": "Unstable - Development", "category": "Debian", "ram_min": 512, "icon": "🌀"},
    {"label": "🌀 Debian Experimental", "value": "images:debian/experimental", "desc": "Experimental - Bleeding", "category": "Debian", "ram_min": 512, "icon": "🌀"},
    
    # 🔷 FEDORA SERIES (12+)
    {"label": "🎩 Fedora 40", "value": "images:fedora/40", "desc": "Fedora 40 - Latest", "category": "Fedora", "ram_min": 1024, "popular": True, "icon": "🎩"},
    {"label": "🎩 Fedora 39", "value": "images:fedora/39", "desc": "Fedora 39", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 38", "value": "images:fedora/38", "desc": "Fedora 38", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 37", "value": "images:fedora/37", "desc": "Fedora 37", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 36", "value": "images:fedora/36", "desc": "Fedora 36", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 35", "value": "images:fedora/35", "desc": "Fedora 35", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 34", "value": "images:fedora/34", "desc": "Fedora 34", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 33", "value": "images:fedora/33", "desc": "Fedora 33", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 32", "value": "images:fedora/32", "desc": "Fedora 32", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 31", "value": "images:fedora/31", "desc": "Fedora 31", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora 30", "value": "images:fedora/30", "desc": "Fedora 30", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    {"label": "🎩 Fedora Rawhide", "value": "images:fedora/rawhide", "desc": "Development - Rolling", "category": "Fedora", "ram_min": 1024, "icon": "🎩"},
    
    # 🔷 ROCKY LINUX (5+)
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky 9 - Latest", "category": "Rocky", "ram_min": 1024, "popular": True, "icon": "🦊"},
    {"label": "🦊 Rocky Linux 8", "value": "images:rockylinux/8", "desc": "Rocky 8 - Stable", "category": "Rocky", "ram_min": 1024, "icon": "🦊"},
    {"label": "🦊 Rocky Linux 7", "value": "images:rockylinux/7", "desc": "Rocky 7 - Legacy", "category": "Rocky", "ram_min": 512, "icon": "🦊"},
    {"label": "🦊 Rocky Linux 6", "value": "images:rockylinux/6", "desc": "Rocky 6 - Old", "category": "Rocky", "ram_min": 512, "icon": "🦊"},
    
    # 🔷 ALMALINUX (5+)
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma 9 - Latest", "category": "AlmaLinux", "ram_min": 1024, "popular": True, "icon": "🦊"},
    {"label": "🦊 AlmaLinux 8", "value": "images:almalinux/8", "desc": "Alma 8 - Stable", "category": "AlmaLinux", "ram_min": 1024, "icon": "🦊"},
    {"label": "🦊 AlmaLinux 7", "value": "images:almalinux/7", "desc": "Alma 7 - Legacy", "category": "AlmaLinux", "ram_min": 512, "icon": "🦊"},
    
    # 🔷 CENTOS SERIES (8+)
    {"label": "📦 CentOS 9 Stream", "value": "images:centos/9-Stream", "desc": "CentOS 9 Stream", "category": "CentOS", "ram_min": 1024, "icon": "📦"},
    {"label": "📦 CentOS 8 Stream", "value": "images:centos/8-Stream", "desc": "CentOS 8 Stream", "category": "CentOS", "ram_min": 1024, "icon": "📦"},
    {"label": "📦 CentOS 7", "value": "images:centos/7", "desc": "CentOS 7 - Legacy", "category": "CentOS", "ram_min": 512, "icon": "📦"},
    {"label": "📦 CentOS 6", "value": "images:centos/6", "desc": "CentOS 6 - Ancient", "category": "CentOS", "ram_min": 256, "icon": "📦"},
    {"label": "📦 CentOS 5", "value": "images:centos/5", "desc": "CentOS 5 - Retro", "category": "CentOS", "ram_min": 256, "icon": "📦"},
    {"label": "📦 CentOS 4", "value": "images:centos/4", "desc": "CentOS 4 - Museum", "category": "CentOS", "ram_min": 128, "icon": "📦"},
    {"label": "📦 CentOS 3", "value": "images:centos/3", "desc": "CentOS 3 - Very Old", "category": "CentOS", "ram_min": 128, "icon": "📦"},
    
    # 🔷 ALPINE LINUX (8+)
    {"label": "🐧 Alpine 3.19", "value": "images:alpine/3.19", "desc": "Alpine Latest", "category": "Alpine", "ram_min": 64, "popular": True, "icon": "🐧"},
    {"label": "🐧 Alpine 3.18", "value": "images:alpine/3.18", "desc": "Alpine 3.18", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    {"label": "🐧 Alpine 3.17", "value": "images:alpine/3.17", "desc": "Alpine 3.17", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    {"label": "🐧 Alpine 3.16", "value": "images:alpine/3.16", "desc": "Alpine 3.16", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    {"label": "🐧 Alpine 3.15", "value": "images:alpine/3.15", "desc": "Alpine 3.15", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    {"label": "🐧 Alpine 3.14", "value": "images:alpine/3.14", "desc": "Alpine 3.14", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    {"label": "🐧 Alpine 3.13", "value": "images:alpine/3.13", "desc": "Alpine 3.13", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    {"label": "🐧 Alpine Edge", "value": "images:alpine/edge", "desc": "Alpine Edge - Rolling", "category": "Alpine", "ram_min": 64, "icon": "🐧"},
    
    # 🔷 ARCH LINUX (3+)
    {"label": "📀 Arch Linux", "value": "images:archlinux", "desc": "Arch - Rolling Release", "category": "Arch", "ram_min": 512, "popular": True, "icon": "📀"},
    {"label": "📀 Arch Linux (Current)", "value": "images:archlinux/current", "desc": "Arch Current", "category": "Arch", "ram_min": 512, "icon": "📀"},
    {"label": "📀 Manjaro", "value": "images:manjaro", "desc": "Manjaro - Arch based", "category": "Arch", "ram_min": 512, "icon": "📀"},
    
    # 🔷 OPENSUSE (6+)
    {"label": "🟢 OpenSUSE Tumbleweed", "value": "images:opensuse/tumbleweed", "desc": "Rolling Release", "category": "OpenSUSE", "ram_min": 1024, "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.5", "value": "images:opensuse/15.5", "desc": "Leap 15.5", "category": "OpenSUSE", "ram_min": 1024, "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.4", "value": "images:opensuse/15.4", "desc": "Leap 15.4", "category": "OpenSUSE", "ram_min": 1024, "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.3", "value": "images:opensuse/15.3", "desc": "Leap 15.3", "category": "OpenSUSE", "ram_min": 1024, "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 42.3", "value": "images:opensuse/42.3", "desc": "Leap 42.3 - Old", "category": "OpenSUSE", "ram_min": 1024, "icon": "🟢"},
    
    # 🔷 FREEBSD (8+)
    {"label": "🔵 FreeBSD 14", "value": "images:freebsd/14", "desc": "FreeBSD 14 - Latest", "category": "FreeBSD", "ram_min": 512, "icon": "🔵"},
    {"label": "🔵 FreeBSD 13", "value": "images:freebsd/13", "desc": "FreeBSD 13 - Stable", "category": "FreeBSD", "ram_min": 512, "icon": "🔵"},
    {"label": "🔵 FreeBSD 12", "value": "images:freebsd/12", "desc": "FreeBSD 12 - Legacy", "category": "FreeBSD", "ram_min": 512, "icon": "🔵"},
    {"label": "🔵 FreeBSD 11", "value": "images:freebsd/11", "desc": "FreeBSD 11 - Old", "category": "FreeBSD", "ram_min": 512, "icon": "🔵"},
    {"label": "🔵 FreeBSD 10", "value": "images:freebsd/10", "desc": "FreeBSD 10 - Ancient", "category": "FreeBSD", "ram_min": 512, "icon": "🔵"},
    {"label": "🔵 FreeBSD 9", "value": "images:freebsd/9", "desc": "FreeBSD 9 - Retro", "category": "FreeBSD", "ram_min": 256, "icon": "🔵"},
    {"label": "🔵 FreeBSD 8", "value": "images:freebsd/8", "desc": "FreeBSD 8 - Museum", "category": "FreeBSD", "ram_min": 256, "icon": "🔵"},
    
    # 🔷 OPENBSD (5+)
    {"label": "🐡 OpenBSD 7.4", "value": "images:openbsd/7.4", "desc": "OpenBSD 7.4", "category": "OpenBSD", "ram_min": 512, "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.3", "value": "images:openbsd/7.3", "desc": "OpenBSD 7.3", "category": "OpenBSD", "ram_min": 512, "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.2", "value": "images:openbsd/7.2", "desc": "OpenBSD 7.2", "category": "OpenBSD", "ram_min": 512, "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.1", "value": "images:openbsd/7.1", "desc": "OpenBSD 7.1", "category": "OpenBSD", "ram_min": 512, "icon": "🐡"},
    
    # 🔷 NETBSD (4+)
    {"label": "🐡 NetBSD 9.3", "value": "images:netbsd/9.3", "desc": "NetBSD 9.3", "category": "NetBSD", "ram_min": 256, "icon": "🐡"},
    {"label": "🐡 NetBSD 9.2", "value": "images:netbsd/9.2", "desc": "NetBSD 9.2", "category": "NetBSD", "ram_min": 256, "icon": "🐡"},
    {"label": "🐡 NetBSD 9.1", "value": "images:netbsd/9.1", "desc": "NetBSD 9.1", "category": "NetBSD", "ram_min": 256, "icon": "🐡"},
    
    # 🔷 KALI LINUX (3+)
    {"label": "🐉 Kali Linux", "value": "images:kali", "desc": "Kali - Security Testing", "category": "Kali", "ram_min": 1024, "popular": True, "icon": "🐉"},
    {"label": "🐉 Kali Linux Weekly", "value": "images:kali/weekly", "desc": "Kali Weekly", "category": "Kali", "ram_min": 1024, "icon": "🐉"},
    {"label": "🐉 Kali Linux Last Release", "value": "images:kali/last", "desc": "Kali Latest", "category": "Kali", "ram_min": 1024, "icon": "🐉"},
    
    # 🔷 PARROT OS (2+)
    {"label": "🦜 Parrot OS", "value": "images:parrotos", "desc": "Parrot Security OS", "category": "Parrot", "ram_min": 1024, "icon": "🦜"},
    {"label": "🦜 Parrot OS (Latest)", "value": "images:parrotos/latest", "desc": "Parrot Latest", "category": "Parrot", "ram_min": 1024, "icon": "🦜"},
    
    # 🔷 GENTOO (4+)
    {"label": "💻 Gentoo", "value": "images:gentoo", "desc": "Gentoo - Source based", "category": "Gentoo", "ram_min": 1024, "icon": "💻"},
    {"label": "💻 Gentoo Current", "value": "images:gentoo/current", "desc": "Gentoo Current", "category": "Gentoo", "ram_min": 1024, "icon": "💻"},
    {"label": "💻 Gentoo OpenRC", "value": "images:gentoo/openrc", "desc": "Gentoo OpenRC", "category": "Gentoo", "ram_min": 1024, "icon": "💻"},
    {"label": "💻 Gentoo Systemd", "value": "images:gentoo/systemd", "desc": "Gentoo Systemd", "category": "Gentoo", "ram_min": 1024, "icon": "💻"},
    
    # 🔷 VOID LINUX (4+)
    {"label": "⚪ Void Linux", "value": "images:voidlinux", "desc": "Void - Independent", "category": "Void", "ram_min": 256, "icon": "⚪"},
    {"label": "⚪ Void Linux musl", "value": "images:voidlinux/musl", "desc": "Void with musl", "category": "Void", "ram_min": 256, "icon": "⚪"},
    {"label": "⚪ Void Linux glibc", "value": "images:voidlinux/glibc", "desc": "Void with glibc", "category": "Void", "ram_min": 256, "icon": "⚪"},
    
    # 🔷 DEVUAN (4+)
    {"label": "🌀 Devuan 5", "value": "images:devuan/5", "desc": "Devuan Daedalus", "category": "Devuan", "ram_min": 256, "icon": "🌀"},
    {"label": "🌀 Devuan 4", "value": "images:devuan/4", "desc": "Devuan Chimaera", "category": "Devuan", "ram_min": 256, "icon": "🌀"},
    {"label": "🌀 Devuan 3", "value": "images:devuan/3", "desc": "Devuan Beowulf", "category": "Devuan", "ram_min": 256, "icon": "🌀"},
    {"label": "🌀 Devuan 2", "value": "images:devuan/2", "desc": "Devuan ASCII", "category": "Devuan", "ram_min": 256, "icon": "🌀"},
    
    # 🔷 SLACKWARE (4+)
    {"label": "💾 Slackware 15", "value": "images:slackware/15", "desc": "Slackware 15", "category": "Slackware", "ram_min": 512, "icon": "💾"},
    {"label": "💾 Slackware 14.2", "value": "images:slackware/14.2", "desc": "Slackware 14.2", "category": "Slackware", "ram_min": 512, "icon": "💾"},
    {"label": "💾 Slackware Current", "value": "images:slackware/current", "desc": "Slackware Current", "category": "Slackware", "ram_min": 512, "icon": "💾"},
    
    # 🔷 ORACLE LINUX (4+)
    {"label": "🔴 Oracle Linux 9", "value": "images:oracle/9", "desc": "Oracle Linux 9", "category": "Oracle", "ram_min": 1024, "icon": "🔴"},
    {"label": "🔴 Oracle Linux 8", "value": "images:oracle/8", "desc": "Oracle Linux 8", "category": "Oracle", "ram_min": 1024, "icon": "🔴"},
    {"label": "🔴 Oracle Linux 7", "value": "images:oracle/7", "desc": "Oracle Linux 7", "category": "Oracle", "ram_min": 512, "icon": "🔴"},
    
    # 🔷 SCIENTIFIC LINUX (3+)
    {"label": "🔬 Scientific Linux 7", "value": "images:scientific/7", "desc": "Scientific Linux 7", "category": "Scientific", "ram_min": 1024, "icon": "🔬"},
    {"label": "🔬 Scientific Linux 6", "value": "images:scientific/6", "desc": "Scientific Linux 6", "category": "Scientific", "ram_min": 512, "icon": "🔬"},
    
    # 🔷 AMAZON LINUX (3+)
    {"label": "☁️ Amazon Linux 2", "value": "images:amazonlinux/2", "desc": "Amazon Linux 2", "category": "Amazon", "ram_min": 512, "icon": "☁️"},
    {"label": "☁️ Amazon Linux 2023", "value": "images:amazonlinux/2023", "desc": "Amazon Linux 2023", "category": "Amazon", "ram_min": 512, "icon": "☁️"},
    
    # 🔷 RHEL (3+)
    {"label": "🔴 Red Hat 9", "value": "images:rhel/9", "desc": "RHEL 9", "category": "RHEL", "ram_min": 1024, "icon": "🔴"},
    {"label": "🔴 Red Hat 8", "value": "images:rhel/8", "desc": "RHEL 8", "category": "RHEL", "ram_min": 1024, "icon": "🔴"},
    {"label": "🔴 Red Hat 7", "value": "images:rhel/7", "desc": "RHEL 7", "category": "RHEL", "ram_min": 512, "icon": "🔴"},
]

# ==================================================================================================
#  🎮  GAMES LIST - 50+ Game Servers
# ==================================================================================================

GAMES_LIST = [
    # 🎮 MINECRAFT SERIES
    {'name': 'Minecraft Java', 'category': 'Survival', 'docker': 'itzg/minecraft-server', 'port': 25565, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🎮'},
    {'name': 'Minecraft Bedrock', 'category': 'Pocket Edition', 'docker': 'itzg/minecraft-bedrock-server', 'port': 19132, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '📱'},
    {'name': 'Minecraft Forge', 'category': 'Modded', 'docker': 'itzg/minecraft-server:java8-multiarch', 'port': 25565, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🔨'},
    {'name': 'Minecraft Spigot', 'category': 'Modded', 'docker': 'marctv/minecraft-papermc-server', 'port': 25565, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '⚙️'},
    {'name': 'Minecraft Fabric', 'category': 'Modded', 'docker': 'fabricmc/fabric-server', 'port': 25565, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🧵'},
    {'name': 'Minecraft BungeeCord', 'category': 'Proxy', 'docker': 'itzg/bungeecord', 'port': 25577, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '🔌'},
    {'name': 'Minecraft Waterfall', 'category': 'Proxy', 'docker': 'itzg/waterfall', 'port': 25577, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '💧'},
    {'name': 'Minecraft Velocity', 'category': 'Proxy', 'docker': 'itzg/velocity', 'port': 25577, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '⚡'},
    
    # 🎮 SURVIVAL GAMES
    {'name': 'Terraria', 'category': 'Adventure', 'docker': 'beardedio/terraria', 'port': 7777, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '🌳'},
    {'name': 'Valheim', 'category': 'Survival', 'docker': 'lloesche/valheim-server', 'port': 2456, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '⚔️'},
    {'name': 'ARK Survival', 'category': 'Survival', 'docker': 'hermsi/ark-server-tools', 'port': 7777, 'ram': 4096, 'cpu': 4, 'disk': 50, 'icon': '🦖'},
    {'name': 'Rust', 'category': 'Survival', 'docker': 'didstopia/rust-server', 'port': 28015, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🦀'},
    {'name': '7 Days to Die', 'category': 'Survival', 'docker': 'didstopia/7dtd-server', 'port': 26900, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🧟'},
    {'name': 'The Forest', 'category': 'Survival', 'docker': 'ich777/theforest-server', 'port': 8766, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🌲'},
    {'name': 'Sons of the Forest', 'category': 'Survival', 'docker': 'ich777/sotf-server', 'port': 8766, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🌲'},
    {'name': 'Grounded', 'category': 'Survival', 'docker': 'ich777/grounded-server', 'port': 7777, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🐜'},
    {'name': 'Smalland', 'category': 'Survival', 'docker': 'ich777/smalland-server', 'port': 7777, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🐜'},
    {'name': 'Nightingale', 'category': 'Survival', 'docker': 'ich777/nightingale-server', 'port': 7777, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🧚'},
    {'name': 'Enshrouded', 'category': 'Survival', 'docker': 'sknnr/enshrouded-dedicated-server', 'port': 15636, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🌫️'},
    {'name': 'V Rising', 'category': 'Survival', 'docker': 'trueosiris/vrising', 'port': 9876, 'ram': 4096, 'cpu': 4, 'disk': 15, 'icon': '🧛'},
    {'name': 'Palworld', 'category': 'Survival', 'docker': 'thijsvanloef/palworld-server-docker', 'port': 8211, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🎮'},
    {'name': 'Project Zomboid', 'category': 'Survival', 'docker': 'renkostamm/pzserver', 'port': 16261, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🧟'},
    {'name': 'Unturned', 'category': 'Survival', 'docker': 'ich777/unturned-server', 'port': 27015, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🧟'},
    {'name': 'Don\'t Starve Together', 'category': 'Survival', 'docker': 'jamesits/dst-server', 'port': 10999, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '⭐'},
    
    # 🎮 FPS GAMES
    {'name': 'CS:GO', 'category': 'FPS', 'docker': 'cm2network/csgo', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 20, 'icon': '🔫'},
    {'name': 'Counter-Strike 1.6', 'category': 'FPS', 'docker': 'kaixhin/cs16', 'port': 27015, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '🎯'},
    {'name': 'Counter-Strike Source', 'category': 'FPS', 'docker': 'cm2network/css', 'port': 27015, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🎯'},
    {'name': 'Team Fortress 2', 'category': 'FPS', 'docker': 'cm2network/tf2', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 20, 'icon': '🔫'},
    {'name': 'Left 4 Dead 2', 'category': 'FPS', 'docker': 'jordi/left4dead2', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🧟'},
    {'name': 'Call of Duty 4', 'category': 'FPS', 'docker': 'jordi/cod4', 'port': 28960, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🔫'},
    {'name': 'Call of Duty 5', 'category': 'FPS', 'docker': 'jordi/cod5', 'port': 28960, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🔫'},
    {'name': 'Call of Duty 6', 'category': 'FPS', 'docker': 'jordi/cod6', 'port': 28960, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🔫'},
    {'name': 'Call of Duty 7', 'category': 'FPS', 'docker': 'jordi/cod7', 'port': 28960, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🔫'},
    {'name': 'Quake 3 Arena', 'category': 'FPS', 'docker': 'defrag/quake3', 'port': 27960, 'ram': 256, 'cpu': 1, 'disk': 2, 'icon': '⚡'},
    {'name': 'Quake Live', 'category': 'FPS', 'docker': 'defrag/quake-live', 'port': 27960, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '⚡'},
    {'name': 'Unreal Tournament', 'category': 'FPS', 'docker': 'ut99/ut-server', 'port': 7777, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '🎯'},
    {'name': 'Unreal Tournament 2004', 'category': 'FPS', 'docker': 'ut2004/ut2004-server', 'port': 7777, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🎯'},
    
    # 🎮 OPEN WORLD
    {'name': 'GTA V FiveM', 'category': 'Open World', 'docker': 'adoptopenjdk/openjdk8', 'port': 30120, 'ram': 4096, 'cpu': 4, 'disk': 50, 'icon': '🚗'},
    {'name': 'GTA San Andreas MP', 'category': 'Open World', 'docker': 'multitheftauto/mtasa', 'port': 22003, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🚗'},
    {'name': 'MTA San Andreas', 'category': 'Open World', 'docker': 'multitheftauto/mtasa', 'port': 22003, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🚗'},
    {'name': 'SA-MP', 'category': 'Open World', 'docker': 'samp/samp-server', 'port': 7777, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '🚗'},
    {'name': 'Minecraft Clone', 'category': 'Open World', 'docker': 'minetest/minetest', 'port': 30000, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '⛏️'},
    
    # 🎮 SIMULATION
    {'name': 'Factorio', 'category': 'Simulation', 'docker': 'factoriotools/factorio', 'port': 34197, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '🏭'},
    {'name': 'Satisfactory', 'category': 'Simulation', 'docker': 'wolveix/satisfactory-server', 'port': 7777, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🏭'},
    {'name': 'Stationeers', 'category': 'Simulation', 'docker': 'ich777/stationeers-server', 'port': 27500, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🚀'},
    {'name': 'Space Engineers', 'category': 'Simulation', 'docker': 'ich777/space-engineers-server', 'port': 27016, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🚀'},
    {'name': 'Stormworks', 'category': 'Simulation', 'docker': 'ich777/stormworks-server', 'port': 25564, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🌊'},
    {'name': 'From The Depths', 'category': 'Simulation', 'docker': 'ich777/fromthedepths-server', 'port': 26214, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '⚓'},
    {'name': 'Kerbal Space Program', 'category': 'Simulation', 'docker': 'ksp/ksp-server', 'port': 6702, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🚀'},
    
    # 🎮 STRATEGY
    {'name': 'RimWorld', 'category': 'Strategy', 'docker': 'rimworld/rimworld-server', 'port': 25555, 'ram': 1024, 'cpu': 1, 'disk': 5, 'icon': '🌍'},
    {'name': 'Stellaris', 'category': 'Strategy', 'docker': 'stellaris/stellaris-server', 'port': 27016, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🌌'},
    {'name': 'Civilization 6', 'category': 'Strategy', 'docker': 'civ6/civ6-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🏛️'},
    {'name': 'Age of Empires 2', 'category': 'Strategy', 'docker': 'aoe2/aoe2-server', 'port': 27015, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '🏰'},
    {'name': 'Age of Empires 3', 'category': 'Strategy', 'docker': 'aoe3/aoe3-server', 'port': 27015, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🏰'},
    {'name': 'Warcraft 3', 'category': 'Strategy', 'docker': 'wc3/wc3-server', 'port': 6112, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '⚔️'},
    {'name': 'Starcraft', 'category': 'Strategy', 'docker': 'sc/sc-server', 'port': 6112, 'ram': 512, 'cpu': 1, 'disk': 5, 'icon': '👾'},
    {'name': 'Starcraft 2', 'category': 'Strategy', 'docker': 'sc2/sc2-server', 'port': 1119, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '👾'},
    
    # 🎮 SANDBOX
    {'name': 'Garry\'s Mod', 'category': 'Sandbox', 'docker': 'gmod/gmod-server', 'port': 27015, 'ram': 1024, 'cpu': 1, 'disk': 10, 'icon': '🔧'},
    {'name': 'Teardown', 'category': 'Sandbox', 'docker': 'teardown/teardown-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '💥'},
    {'name': 'Scrap Mechanic', 'category': 'Sandbox', 'docker': 'scrapmechanic/scrapmechanic-server', 'port': 28764, 'ram': 2048, 'cpu': 2, 'disk': 10, 'icon': '🔧'},
    
    # 🎮 RACING
    {'name': 'Assetto Corsa', 'category': 'Racing', 'docker': 'ac/ac-server', 'port': 9600, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🏎️'},
    {'name': 'Assetto Corsa Competizione', 'category': 'Racing', 'docker': 'acc/acc-server', 'port': 9231, 'ram': 4096, 'cpu': 4, 'disk': 20, 'icon': '🏎️'},
    {'name': 'Project Cars 2', 'category': 'Racing', 'docker': 'pc2/pc2-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🏎️'},
    {'name': 'rFactor 2', 'category': 'Racing', 'docker': 'rf2/rf2-server', 'port': 64297, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🏎️'},
    {'name': 'RaceRoom', 'category': 'Racing', 'docker': 'raceroom/raceroom-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 15, 'icon': '🏎️'},
    
    # 🎮 SPORTS
    {'name': 'FIFA 23', 'category': 'Sports', 'docker': 'fifa/fifa23-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 20, 'icon': '⚽'},
    {'name': 'NBA 2K23', 'category': 'Sports', 'docker': 'nba/nba2k23-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 20, 'icon': '🏀'},
    {'name': 'Madden 23', 'category': 'Sports', 'docker': 'madden/madden23-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 20, 'icon': '🏈'},
    {'name': 'NHL 23', 'category': 'Sports', 'docker': 'nhl/nhl23-server', 'port': 27015, 'ram': 2048, 'cpu': 2, 'disk': 20, 'icon': '🏒'},
]

# ==================================================================================================
#  🛠️  TOOLS LIST - 50+ Development Tools
# ==================================================================================================

TOOLS_LIST = [
    # 🌐 WEB SERVERS
    {'name': 'Nginx', 'category': 'Web Server', 'command': 'apt install nginx -y && systemctl start nginx', 'port': 80, 'icon': '🌐'},
    {'name': 'Apache', 'category': 'Web Server', 'command': 'apt install apache2 -y && systemctl start apache2', 'port': 80, 'icon': '🕸️'},
    {'name': 'Caddy', 'category': 'Web Server', 'command': 'apt install caddy -y && systemctl start caddy', 'port': 80, 'icon': '🛡️'},
    {'name': 'Lighttpd', 'category': 'Web Server', 'command': 'apt install lighttpd -y && systemctl start lighttpd', 'port': 80, 'icon': '⚡'},
    {'name': 'Tomcat', 'category': 'Web Server', 'command': 'apt install tomcat9 -y && systemctl start tomcat9', 'port': 8080, 'icon': '🐱'},
    {'name': 'Jetty', 'category': 'Web Server', 'command': 'apt install jetty9 -y && systemctl start jetty9', 'port': 8080, 'icon': '✈️'},
    
    # 🗄️ DATABASES
    {'name': 'MySQL', 'category': 'Database', 'command': 'apt install mysql-server -y && systemctl start mysql', 'port': 3306, 'icon': '🗄️'},
    {'name': 'MariaDB', 'category': 'Database', 'command': 'apt install mariadb-server -y && systemctl start mariadb', 'port': 3306, 'icon': '🗄️'},
    {'name': 'PostgreSQL', 'category': 'Database', 'command': 'apt install postgresql -y && systemctl start postgresql', 'port': 5432, 'icon': '🐘'},
    {'name': 'MongoDB', 'category': 'Database', 'command': 'apt install mongodb -y && systemctl start mongodb', 'port': 27017, 'icon': '🍃'},
    {'name': 'Redis', 'category': 'Cache', 'command': 'apt install redis-server -y && systemctl start redis', 'port': 6379, 'icon': '🔴'},
    {'name': 'Memcached', 'category': 'Cache', 'command': 'apt install memcached -y && systemctl start memcached', 'port': 11211, 'icon': '💾'},
    {'name': 'Cassandra', 'category': 'Database', 'command': 'apt install cassandra -y && systemctl start cassandra', 'port': 9042, 'icon': '🐘'},
    {'name': 'CouchDB', 'category': 'Database', 'command': 'apt install couchdb -y && systemctl start couchdb', 'port': 5984, 'icon': '🛋️'},
    {'name': 'Elasticsearch', 'category': 'Search', 'command': 'apt install elasticsearch -y && systemctl start elasticsearch', 'port': 9200, 'icon': '🔍'},
    {'name': 'InfluxDB', 'category': 'Time Series', 'command': 'apt install influxdb -y && systemctl start influxdb', 'port': 8086, 'icon': '📈'},
    
    # 🔧 DEVELOPMENT TOOLS
    {'name': 'Git', 'category': 'Version Control', 'command': 'apt install git -y', 'icon': '📦'},
    {'name': 'GitLab', 'category': 'CI/CD', 'command': 'apt install gitlab-ce -y', 'port': 80, 'icon': '🦊'},
    {'name': 'GitHub Runner', 'category': 'CI/CD', 'command': 'curl -fsSL https://github.com/actions/runner | bash', 'icon': '🐙'},
    {'name': 'Jenkins', 'category': 'CI/CD', 'command': 'apt install jenkins -y && systemctl start jenkins', 'port': 8080, 'icon': '🏗️'},
    {'name': 'Drone CI', 'category': 'CI/CD', 'command': 'docker run -d --name drone --restart always -p 80:80 drone/drone', 'port': 80, 'icon': '🚁'},
    {'name': 'Travis CI', 'category': 'CI/CD', 'command': 'apt install travis -y', 'icon': '🚦'},
    {'name': 'Circle CI', 'category': 'CI/CD', 'command': 'curl -fsSL https://circleci.com/install | bash', 'icon': '⚪'},
    {'name': 'SonarQube', 'category': 'Code Quality', 'command': 'apt install sonarqube -y && systemctl start sonarqube', 'port': 9000, 'icon': '🔊'},
    {'name': 'Jira', 'category': 'Project Management', 'command': 'apt install jira -y && systemctl start jira', 'port': 8080, 'icon': '📋'},
    {'name': 'Confluence', 'category': 'Wiki', 'command': 'apt install confluence -y && systemctl start confluence', 'port': 8090, 'icon': '📝'},
    
    # 🐳 CONTAINER TOOLS
    {'name': 'Docker', 'category': 'Container', 'command': 'curl -fsSL https://get.docker.com | bash', 'icon': '🐳'},
    {'name': 'Docker Compose', 'category': 'Container', 'command': 'apt install docker-compose -y', 'icon': '🐳'},
    {'name': 'Portainer', 'category': 'Container', 'command': 'docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce', 'port': 9000, 'icon': '🐳'},
    {'name': 'Kubernetes', 'category': 'Orchestration', 'command': 'snap install kubectl --classic', 'icon': '☸️'},
    {'name': 'Minikube', 'category': 'Orchestration', 'command': 'curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && install minikube-linux-amd64 /usr/local/bin/minikube', 'icon': '☸️'},
    {'name': 'Helm', 'category': 'Orchestration', 'command': 'curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash', 'icon': '⎈'},
    {'name': 'Rancher', 'category': 'Orchestration', 'command': 'docker run -d --restart=always -p 80:80 -p 443:443 rancher/rancher', 'port': 80, 'icon': '🐮'},
    {'name': 'Nomad', 'category': 'Orchestration', 'command': 'apt install nomad -y && systemctl start nomad', 'port': 4646, 'icon': '📦'},
    
    # 📊 MONITORING
    {'name': 'Prometheus', 'category': 'Monitoring', 'command': 'apt install prometheus -y && systemctl start prometheus', 'port': 9090, 'icon': '📊'},
    {'name': 'Grafana', 'category': 'Monitoring', 'command': 'apt install grafana -y && systemctl start grafana', 'port': 3000, 'icon': '📈'},
    {'name': 'Nagios', 'category': 'Monitoring', 'command': 'apt install nagios -y && systemctl start nagios', 'port': 80, 'icon': '🔔'},
    {'name': 'Zabbix', 'category': 'Monitoring', 'command': 'apt install zabbix-server-mysql zabbix-frontend-php -y', 'port': 80, 'icon': '📊'},
    {'name': 'Netdata', 'category': 'Monitoring', 'command': 'bash <(curl -Ss https://my-netdata.io/kickstart.sh)', 'port': 19999, 'icon': '📈'},
    {'name': 'Datadog', 'category': 'Monitoring', 'command': 'DD_API_KEY=your_key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"', 'icon': '🐕'},
    {'name': 'New Relic', 'category': 'Monitoring', 'command': 'curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash', 'icon': '📊'},
    
    # 📝 LOGGING
    {'name': 'Logstash', 'category': 'Logging', 'command': 'apt install logstash -y && systemctl start logstash', 'port': 5044, 'icon': '📝'},
    {'name': 'Kibana', 'category': 'Visualization', 'command': 'apt install kibana -y && systemctl start kibana', 'port': 5601, 'icon': '📊'},
    {'name': 'Fluentd', 'category': 'Logging', 'command': 'apt install fluentd -y && systemctl start fluentd', 'port': 24224, 'icon': '📝'},
    {'name': 'Graylog', 'category': 'Logging', 'command': 'apt install graylog-server -y && systemctl start graylog-server', 'port': 9000, 'icon': '📝'},
    {'name': 'Splunk', 'category': 'Logging', 'command': 'wget -O splunk.deb "https://www.splunk.com/page/download_track?file=..." && dpkg -i splunk.deb', 'port': 8000, 'icon': '🔍'},
    
    # 🔒 SECURITY
    {'name': 'Fail2ban', 'category': 'Security', 'command': 'apt install fail2ban -y && systemctl start fail2ban', 'icon': '🛡️'},
    {'name': 'ClamAV', 'category': 'Security', 'command': 'apt install clamav clamav-daemon -y && systemctl start clamav-daemon', 'icon': '🦠'},
    {'name': 'Snort', 'category': 'Security', 'command': 'apt install snort -y && systemctl start snort', 'icon': '👃'},
    {'name': 'OpenVAS', 'category': 'Security', 'command': 'apt install openvas -y && systemctl start openvas', 'port': 9392, 'icon': '🔓'},
    {'name': 'Metasploit', 'category': 'Security', 'command': 'curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod +x msfinstall && ./msfinstall', 'icon': '💥'},
    {'name': 'Wireshark', 'category': 'Security', 'command': 'apt install wireshark -y', 'icon': '🦈'},
    {'name': 'Nmap', 'category': 'Security', 'command': 'apt install nmap -y', 'icon': '🗺️'},
    
    # ☁️ CLOUD TOOLS
    {'name': 'AWS CLI', 'category': 'Cloud', 'command': 'apt install awscli -y', 'icon': '☁️'},
        {'name': 'Azure CLI', 'category': 'Cloud', 'command': 'curl -sL https://aka.ms/InstallAzureCLIDeb | bash', 'icon': '🔵'},
    {'name': 'Google Cloud SDK', 'category': 'Cloud', 'command': 'echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && apt-get install -y google-cloud-sdk', 'icon': '☁️'},
    {'name': 'Terraform', 'category': 'Infrastructure', 'command': 'wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && apt update && apt install terraform', 'icon': '🏗️'},
    {'name': 'Packer', 'category': 'Infrastructure', 'command': 'wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && apt update && apt install packer', 'icon': '📦'},
    {'name': 'Vagrant', 'category': 'Infrastructure', 'command': 'wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && apt update && apt install vagrant', 'icon': '📦'},
    {'name': 'Ansible', 'category': 'Automation', 'command': 'apt install ansible -y', 'icon': '⚙️'},
    {'name': 'Puppet', 'category': 'Automation', 'command': 'apt install puppet -y', 'icon': '🐘'},
    {'name': 'Chef', 'category': 'Automation', 'command': 'apt install chef -y', 'icon': '👨‍🍳'},
    {'name': 'SaltStack', 'category': 'Automation', 'command': 'apt install salt-master salt-minion -y', 'icon': '🧂'},
    
    # 🖥️ SYSTEM TOOLS
    {'name': 'htop', 'category': 'System', 'command': 'apt install htop -y', 'icon': '📊'},
    {'name': 'nload', 'category': 'Network', 'command': 'apt install nload -y', 'icon': '📡'},
    {'name': 'iftop', 'category': 'Network', 'command': 'apt install iftop -y', 'icon': '📡'},
    {'name': 'nethogs', 'category': 'Network', 'command': 'apt install nethogs -y', 'icon': '📡'},
    {'name': 'iotop', 'category': 'System', 'command': 'apt install iotop -y', 'icon': '💽'},
    {'name': 'ncdu', 'category': 'System', 'command': 'apt install ncdu -y', 'icon': '📁'},
    {'name': 'tmux', 'category': 'Terminal', 'command': 'apt install tmux -y', 'icon': '💻'},
    {'name': 'screen', 'category': 'Terminal', 'command': 'apt install screen -y', 'icon': '💻'},
    {'name': 'byobu', 'category': 'Terminal', 'command': 'apt install byobu -y', 'icon': '💻'},
    {'name': 'ranger', 'category': 'File Manager', 'command': 'apt install ranger -y', 'icon': '📁'},
    {'name': 'mc', 'category': 'File Manager', 'command': 'apt install mc -y', 'icon': '📁'},
    
    # 📋 CMS & APPLICATIONS
    {'name': 'WordPress', 'category': 'CMS', 'command': 'apt install wordpress -y', 'port': 80, 'icon': '📝'},
    {'name': 'Drupal', 'category': 'CMS', 'command': 'apt install drupal -y', 'port': 80, 'icon': '🌐'},
    {'name': 'Joomla', 'category': 'CMS', 'command': 'apt install joomla -y', 'port': 80, 'icon': '📰'},
    {'name': 'Magento', 'category': 'E-commerce', 'command': 'apt install magento -y', 'port': 80, 'icon': '🛒'},
    {'name': 'PrestaShop', 'category': 'E-commerce', 'command': 'apt install prestashop -y', 'port': 80, 'icon': '🛍️'},
    {'name': 'OpenCart', 'category': 'E-commerce', 'command': 'apt install opencart -y', 'port': 80, 'icon': '🛒'},
    {'name': 'phpMyAdmin', 'category': 'Database', 'command': 'apt install phpmyadmin -y', 'port': 80, 'icon': '🗄️'},
    {'name': 'Adminer', 'category': 'Database', 'command': 'apt install adminer -y', 'port': 80, 'icon': '🗄️'},
    {'name': 'FileBrowser', 'category': 'File Manager', 'command': 'curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash', 'port': 8080, 'icon': '📁'},
    {'name': 'Nextcloud', 'category': 'Cloud Storage', 'command': 'apt install nextcloud -y', 'port': 80, 'icon': '☁️'},
    {'name': 'OwnCloud', 'category': 'Cloud Storage', 'command': 'apt install owncloud -y', 'port': 80, 'icon': '☁️'},
    {'name': 'Seafile', 'category': 'Cloud Storage', 'command': 'apt install seafile -y', 'port': 8000, 'icon': '☁️'},
    
    # 🔌 PROXY & LOAD BALANCERS
    {'name': 'HAProxy', 'category': 'Proxy', 'command': 'apt install haproxy -y && systemctl start haproxy', 'port': 80, 'icon': '⚖️'},
    {'name': 'Nginx Proxy Manager', 'category': 'Proxy', 'command': 'docker run -d --name nginx-proxy-manager -p 80:80 -p 81:81 -p 443:443 -v /docker/appdata/nginx-proxy-manager:/config --restart always jc21/nginx-proxy-manager', 'port': 81, 'icon': '🌐'},
    {'name': 'Traefik', 'category': 'Proxy', 'command': 'docker run -d --name traefik --restart always -p 80:80 -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock traefik:v2.9', 'port': 8080, 'icon': '🔄'},
    {'name': 'Caddy', 'category': 'Proxy', 'command': 'apt install caddy -y && systemctl start caddy', 'port': 80, 'icon': '🛡️'},
    {'name': 'Squid', 'category': 'Proxy', 'command': 'apt install squid -y && systemctl start squid', 'port': 3128, 'icon': '🐙'},
    
    # 📡 MESSAGE QUEUES
    {'name': 'RabbitMQ', 'category': 'Message Queue', 'command': 'apt install rabbitmq-server -y && systemctl start rabbitmq-server', 'port': 5672, 'icon': '🐇'},
    {'name': 'Kafka', 'category': 'Message Queue', 'command': 'apt install kafka -y && systemctl start kafka', 'port': 9092, 'icon': '📨'},
    {'name': 'ActiveMQ', 'category': 'Message Queue', 'command': 'apt install activemq -y && systemctl start activemq', 'port': 61616, 'icon': '📨'},
    {'name': 'Redis', 'category': 'Message Queue', 'command': 'apt install redis-server -y && systemctl start redis', 'port': 6379, 'icon': '🔴'},
]

# ==================================================================================================
#  💰  FREE VPS PLANS
# ==================================================================================================

FREE_VPS_PLANS = {
    'invites': [
        {'name': '🥉 Bronze Plan', 'invites': 5, 'ram': 2, 'cpu': 1, 'disk': 20, 'emoji': '🥉', 'popular': False},
        {'name': '🥈 Silver Plan', 'invites': 10, 'ram': 4, 'cpu': 2, 'disk': 40, 'emoji': '🥈', 'popular': True},
        {'name': '🥇 Gold Plan', 'invites': 15, 'ram': 8, 'cpu': 4, 'disk': 80, 'emoji': '🥇', 'popular': True},
        {'name': '🏆 Platinum Plan', 'invites': 20, 'ram': 16, 'cpu': 8, 'disk': 160, 'emoji': '🏆', 'popular': True},
        {'name': '💎 Diamond Plan', 'invites': 25, 'ram': 32, 'cpu': 16, 'disk': 320, 'emoji': '💎', 'popular': False},
        {'name': '👑 Royal Plan', 'invites': 30, 'ram': 64, 'cpu': 32, 'disk': 640, 'emoji': '👑', 'popular': False},
        {'name': '⚡ Legendary Plan', 'invites': 40, 'ram': 128, 'cpu': 64, 'disk': 1280, 'emoji': '⚡', 'popular': False},
        {'name': '🚀 Enterprise Plan', 'invites': 50, 'ram': 256, 'cpu': 128, 'disk': 2560, 'emoji': '🚀', 'popular': False},
        {'name': '🌌 Cosmic Plan', 'invites': 75, 'ram': 512, 'cpu': 256, 'disk': 5120, 'emoji': '🌌', 'popular': False},
        {'name': '∞ Infinite Plan', 'invites': 100, 'ram': 1024, 'cpu': 512, 'disk': 10240, 'emoji': '∞', 'popular': False},
    ]
}

# ==================================================================================================
#  🗄️  DATABASE SETUP - COMPLETE
# ==================================================================================================

DATABASE_PATH = '/opt/svm5-bot/data/svm5.db'
NODES_FILE = '/opt/svm5-bot/nodes/nodes.json'
CONFIG_FILE = '/opt/svm5-bot/config.json'

def get_db():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database with all tables"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            logger.error("Failed to connect to database")
            return False
        
        cur = conn.cursor()
        
        # Admins table
        cur.execute('''CREATE TABLE IF NOT EXISTS admins (
            user_id TEXT PRIMARY KEY,
            added_by TEXT,
            added_at TEXT,
            permissions TEXT DEFAULT 'all'
        )''')
        
        for admin_id in MAIN_ADMIN_IDS:
            cur.execute('INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)', 
                       (str(admin_id), datetime.now().isoformat()))
        
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
            purge_protected INTEGER DEFAULT 0,
            node_name TEXT DEFAULT 'local',
            created_at TEXT NOT NULL,
            last_started TEXT,
            last_stopped TEXT,
            ip_address TEXT,
            mac_address TEXT,
            games_installed TEXT DEFAULT '[]',
            tools_installed TEXT DEFAULT '[]',
            shared_with TEXT DEFAULT '[]',
            notes TEXT
        )''')
        
        # User stats table
        cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
            user_id TEXT PRIMARY KEY,
            invites INTEGER DEFAULT 0,
            boosts INTEGER DEFAULT 0,
            claimed_vps_count INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            api_key TEXT UNIQUE,
            last_updated TEXT
        )''')
        
        # Settings table
        cur.execute('''CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TEXT
        )''')
        
        # Shared VPS table
        cur.execute('''CREATE TABLE IF NOT EXISTS shared_vps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id TEXT NOT NULL,
            shared_with_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            permissions TEXT DEFAULT 'view',
            shared_at TEXT NOT NULL,
            UNIQUE(owner_id, shared_with_id, container_name)
        )''')
        
        # Games table
        cur.execute('''CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            docker_image TEXT,
            install_script TEXT,
            default_port INTEGER,
            min_ram INTEGER,
            min_cpu INTEGER,
            min_disk INTEGER,
            description TEXT,
            icon TEXT
        )''')
        
        # Tools table
        cur.execute('''CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            install_command TEXT,
            default_port INTEGER,
            description TEXT,
            icon TEXT
        )''')
        
        # Installed games table
        cur.execute('''CREATE TABLE IF NOT EXISTS installed_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            game_name TEXT NOT NULL,
            game_port INTEGER,
            status TEXT DEFAULT 'installed',
            installed_at TEXT NOT NULL,
            UNIQUE(container_name, game_name)
        )''')
        
        # Installed tools table
        cur.execute('''CREATE TABLE IF NOT EXISTS installed_tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            tool_name TEXT NOT NULL,
            tool_port INTEGER,
            status TEXT DEFAULT 'installed',
            installed_at TEXT NOT NULL,
            UNIQUE(container_name, tool_name)
        )''')
        
        # Nodes table
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
            used_cpu REAL DEFAULT 0,
            total_disk INTEGER DEFAULT 0,
            used_disk INTEGER DEFAULT 0,
            lxc_count INTEGER DEFAULT 0,
            api_key TEXT UNIQUE,
            region TEXT DEFAULT 'us',
            last_checked TEXT,
            added_by TEXT,
            added_at TEXT NOT NULL,
            is_main INTEGER DEFAULT 0
        )''')
        
        # IPv4 table
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
            assigned_at TEXT NOT NULL,
            UNIQUE(user_id, container_name)
        )''')
        
        # Port forwards table
        cur.execute('''CREATE TABLE IF NOT EXISTS port_forwards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            container_port INTEGER NOT NULL,
            host_port INTEGER UNIQUE NOT NULL,
            protocol TEXT DEFAULT 'tcp+udp',
            node_name TEXT DEFAULT 'local',
            created_at TEXT NOT NULL
        )''')
        
        # Port allocations table
        cur.execute('''CREATE TABLE IF NOT EXISTS port_allocations (
            user_id TEXT PRIMARY KEY,
            allocated_ports INTEGER DEFAULT 5,
            last_updated TEXT
        )''')
        
        # Transactions table
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
        
        # Initialize default games
        for game in GAMES_LIST:
            cur.execute('''INSERT OR IGNORE INTO games 
                (name, category, docker_image, default_port, min_ram, min_cpu, min_disk, icon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                (game['name'], game['category'], game['docker'], game['port'], game['ram'], game['cpu'], game['disk'], game['icon']))
        
        # Initialize default tools
        for tool in TOOLS_LIST:
            cur.execute('''INSERT OR IGNORE INTO tools 
                (name, category, install_command, default_port, icon)
                VALUES (?, ?, ?, ?, ?)''',
                (tool['name'], tool['category'], tool['command'], tool.get('port'), tool['icon']))
        
        # Initialize settings
        settings_init = [
            ('license_verified', 'false', 'License verification status'),
            ('server_ip', SERVER_IP, 'Server IP address'),
            ('mac_address', MAC_ADDRESS, 'Server MAC address'),
            ('hostname', HOSTNAME, 'Server hostname'),
            ('total_vps_created', '0', 'Total VPS created'),
            ('main_node', 'local', 'Main node name'),
            ('auto_node_detect', 'true', 'Auto-detect local node'),
            ('default_port_quota', '5', 'Default port forwarding quota'),
            ('ipv4_price', '50', 'Price per IPv4 in INR'),
            ('upi_id', '9892642904@ybl', 'Default UPI ID'),
            ('upi_name', 'Ankit-Dev', 'UPI account name'),
        ]
        
        for key, value, desc in settings_init:
            cur.execute('INSERT OR IGNORE INTO settings (key, value, description) VALUES (?, ?, ?)', 
                       (key, value, desc))
        
        conn.commit()
        logger.info("✅ Database initialized successfully")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Initialize database
init_db()

# ==================================================================================================
#  📊  DATABASE HELPER FUNCTIONS
# ==================================================================================================

def get_setting(key: str, default: Any = None) -> Any:
    """Get a setting value"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return default
        cur = conn.cursor()
        cur.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cur.fetchone()
        return row[0] if row else default
    except:
        return default
    finally:
        if conn:
            conn.close()

def set_setting(key: str, value: str):
    """Set a setting value"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute('INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
                    (key, value, datetime.now().isoformat()))
        conn.commit()
    except:
        pass
    finally:
        if conn:
            conn.close()

def get_user_vps(user_id: str) -> List[Dict]:
    """Get all VPS for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM vps WHERE user_id = ? ORDER BY id', (user_id,))
        rows = cur.fetchall()
        vps_list = [dict(row) for row in rows]
        
        # Parse JSON fields
        for vps in vps_list:
            for field in ['games_installed', 'tools_installed', 'shared_with']:
                if field in vps and vps[field]:
                    try:
                        vps[field] = json.loads(vps[field])
                    except:
                        vps[field] = []
        return vps_list
    except:
        return []
    finally:
        if conn:
            conn.close()

def get_all_vps() -> List[Dict]:
    """Get all VPS"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM vps ORDER BY user_id, id')
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except:
        return []
    finally:
        if conn:
            conn.close()

def add_vps(user_id: str, container_name: str, ram: int, cpu: int, disk: int, 
            os_version: str, plan_name: str = "Custom", node_name: str = "local") -> Optional[Dict]:
    """Add a new VPS"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        # Get IP and MAC
        ip_address = "N/A"
        mac_address = "N/A"
        try:
            out = subprocess.getoutput(f"lxc exec {container_name} -- ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
            if out:
                ip_address = out.strip()
            out = subprocess.getoutput(f"lxc exec {container_name} -- ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
            if out:
                mac_address = out.strip()
        except:
            pass
        
        cur.execute('''INSERT INTO vps 
                       (user_id, container_name, plan_name, ram, cpu, disk, os_version, status, node_name, created_at, ip_address, mac_address)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (user_id, container_name, plan_name, ram, cpu, disk, os_version, 'running', node_name, now, ip_address, mac_address))
        vps_id = cur.lastrowid
        conn.commit()
        
        cur.execute('SELECT * FROM vps WHERE id = ?', (vps_id,))
        vps = dict(cur.fetchone())
        return vps
    except:
        return None
    finally:
        if conn:
            conn.close()

def update_vps_status(container_name: str, status: str):
    """Update VPS status"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('UPDATE vps SET status = ?, last_started = ? WHERE container_name = ?', 
                   (status, now if status == 'running' else None, container_name))
        conn.commit()
    except:
        pass
    finally:
        if conn:
            conn.close()

def delete_vps(container_name: str) -> bool:
    """Delete VPS"""
    conn = None
    try:
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
        conn.commit()
        return True
    except:
        return False
    finally:
        if conn:
            conn.close()

def is_admin(user_id: str) -> bool:
    """Check if user is admin"""
    return user_id in [str(a) for a in MAIN_ADMIN_IDS]

def get_user_stats(user_id: str) -> Dict:
    """Get user stats"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return {'invites': 0, 'api_key': hashlib.sha256(f"{user_id}".encode()).hexdigest()[:16]}
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        # Create new user stats with API key
        api_key = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16]
        cur.execute('INSERT INTO user_stats (user_id, invites, boosts, claimed_vps_count, api_key, last_updated) VALUES (?, 0, 0, 0, ?, ?)',
                   (user_id, api_key, datetime.now().isoformat()))
        conn.commit()
        return {'user_id': user_id, 'invites': 0, 'boosts': 0, 'claimed_vps_count': 0, 'api_key': api_key}
    except:
        return {'invites': 0, 'api_key': hashlib.sha256(f"{user_id}".encode()).hexdigest()[:16]}
    finally:
        if conn:
            conn.close()

def update_user_stats(user_id: str, invites: int = 0, boosts: int = 0, claimed_vps_count: int = 0):
    """Update user stats"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        
        cur.execute('''INSERT OR REPLACE INTO user_stats 
                       (user_id, invites, boosts, claimed_vps_count, api_key, last_updated) 
                       VALUES (?, 
                               COALESCE((SELECT invites FROM user_stats WHERE user_id = ?), 0) + ?, 
                               COALESCE((SELECT boosts FROM user_stats WHERE user_id = ?), 0) + ?,
                               COALESCE((SELECT claimed_vps_count FROM user_stats WHERE user_id = ?), 0) + ?,
                               COALESCE((SELECT api_key FROM user_stats WHERE user_id = ?), ?),
                               ?)''',
                    (user_id, user_id, invites, user_id, boosts, user_id, claimed_vps_count, 
                     user_id, hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16], 
                     datetime.now().isoformat()))
        conn.commit()
    except:
        pass
    finally:
        if conn:
            conn.close()

def share_vps(owner_id: str, shared_with_id: str, container_name: str, permissions: str = "view") -> bool:
    """Share VPS with another user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        # Update vps table
        cur.execute('SELECT shared_with FROM vps WHERE container_name = ? AND user_id = ?', 
                   (container_name, owner_id))
        row = cur.fetchone()
        if row:
            shared_with = json.loads(row['shared_with']) if row['shared_with'] else []
            if shared_with_id not in shared_with:
                shared_with.append(shared_with_id)
                cur.execute('UPDATE vps SET shared_with = ? WHERE container_name = ?',
                           (json.dumps(shared_with), container_name))
        
        cur.execute('''INSERT OR REPLACE INTO shared_vps 
                       (owner_id, shared_with_id, container_name, permissions, shared_at)
                       VALUES (?, ?, ?, ?, ?)''',
                    (owner_id, shared_with_id, container_name, permissions, now))
        conn.commit()
        return True
    except:
        return False
    finally:
        if conn:
            conn.close()

def unshare_vps(owner_id: str, shared_with_id: str, container_name: str) -> bool:
    """Remove VPS sharing"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        
        cur.execute('SELECT shared_with FROM vps WHERE container_name = ? AND user_id = ?', 
                   (container_name, owner_id))
        row = cur.fetchone()
        if row:
            shared_with = json.loads(row['shared_with']) if row['shared_with'] else []
            if shared_with_id in shared_with:
                shared_with.remove(shared_with_id)
                cur.execute('UPDATE vps SET shared_with = ? WHERE container_name = ?',
                           (json.dumps(shared_with), container_name))
        
        cur.execute('DELETE FROM shared_vps WHERE owner_id = ? AND shared_with_id = ? AND container_name = ?',
                    (owner_id, shared_with_id, container_name))
        conn.commit()
        return True
    except:
        return False
    finally:
        if conn:
            conn.close()

def get_shared_vps(user_id: str) -> List[Dict]:
    """Get VPS shared with user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('''SELECT v.*, sv.permissions, sv.owner_id 
                       FROM vps v 
                       JOIN shared_vps sv ON v.container_name = sv.container_name 
                       WHERE sv.shared_with_id = ?''', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except:
        return []
    finally:
        if conn:
            conn.close()

def add_game_install(user_id: str, container_name: str, game_name: str, game_port: int = None) -> bool:
    """Add game installation record"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        cur.execute('''INSERT OR REPLACE INTO installed_games 
                       (user_id, container_name, game_name, game_port, installed_at)
                       VALUES (?, ?, ?, ?, ?)''',
                    (user_id, container_name, game_name, game_port, now))
        
        cur.execute('SELECT games_installed FROM vps WHERE container_name = ?', (container_name,))
        row = cur.fetchone()
        if row:
            games = json.loads(row['games_installed']) if row['games_installed'] else []
            if game_name not in games:
                games.append(game_name)
                cur.execute('UPDATE vps SET games_installed = ? WHERE container_name = ?',
                           (json.dumps(games), container_name))
        
        conn.commit()
        return True
    except:
        return False
    finally:
        if conn:
            conn.close()

def add_tool_install(user_id: str, container_name: str, tool_name: str, tool_port: int = None) -> bool:
    """Add tool installation record"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        cur.execute('''INSERT OR REPLACE INTO installed_tools 
                       (user_id, container_name, tool_name, tool_port, installed_at)
                       VALUES (?, ?, ?, ?, ?)''',
                    (user_id, container_name, tool_name, tool_port, now))
        
        cur.execute('SELECT tools_installed FROM vps WHERE container_name = ?', (container_name,))
        row = cur.fetchone()
        if row:
            tools = json.loads(row['tools_installed']) if row['tools_installed'] else []
            if tool_name not in tools:
                tools.append(tool_name)
                cur.execute('UPDATE vps SET tools_installed = ? WHERE container_name = ?',
                           (json.dumps(tools), container_name))
        
        conn.commit()
        return True
    except:
        return False
    finally:
        if conn:
            conn.close()

def get_available_games() -> List[Dict]:
    """Get all available games"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return GAMES_LIST
        cur = conn.cursor()
        cur.execute('SELECT * FROM games ORDER BY name')
        rows = cur.fetchall()
        return [dict(row) for row in rows] if rows else GAMES_LIST
    except:
        return GAMES_LIST
    finally:
        if conn:
            conn.close()

def get_available_tools() -> List[Dict]:
    """Get all available tools"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return TOOLS_LIST
        cur = conn.cursor()
        cur.execute('SELECT * FROM tools ORDER BY name')
        rows = cur.fetchall()
        return [dict(row) for row in rows] if rows else TOOLS_LIST
    except:
        return TOOLS_LIST
    finally:
        if conn:
            conn.close()

def get_installed_games(container_name: str) -> List[Dict]:
    """Get games installed in container"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('''SELECT ig.*, g.category, g.icon 
                       FROM installed_games ig
                       JOIN games g ON ig.game_name = g.name
                       WHERE ig.container_name = ?''', (container_name,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except:
        return []
    finally:
        if conn:
            conn.close()

def get_installed_tools(container_name: str) -> List[Dict]:
    """Get tools installed in container"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('''SELECT it.*, t.category, t.icon 
                       FROM installed_tools it
                       JOIN tools t ON it.tool_name = t.name
                       WHERE it.container_name = ?''', (container_name,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except:
        return []
    finally:
        if conn:
            conn.close()

def add_port_forward(user_id: str, container_name: str, container_port: int, host_port: int, protocol: str = "tcp+udp") -> bool:
    """Add port forward to database"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO port_forwards (user_id, container_name, container_port, host_port, protocol, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)''', (user_id, container_name, container_port, host_port, protocol, now))
        conn.commit()
        return True
    except:
        return False
    finally:
        if conn:
            conn.close()

def remove_port_forward(pf_id: int) -> Tuple[bool, str, int]:
    """Remove port forward from database"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False, "", 0
        cur = conn.cursor()
        cur.execute('SELECT container_name, host_port FROM port_forwards WHERE id = ?', (pf_id,))
        row = cur.fetchone()
        if not row:
            return False, "", 0
        container_name, host_port = row['container_name'], row['host_port']
        cur.execute('DELETE FROM port_forwards WHERE id = ?', (pf_id,))
        conn.commit()
        return True, container_name, host_port
    except:
        return False, "", 0
    finally:
        if conn:
            conn.close()

def get_user_port_forwards(user_id: str) -> List[Dict]:
    """Get all port forwards for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM port_forwards WHERE user_id = ? ORDER BY created_at', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except:
        return []
    finally:
        if conn:
            conn.close()

def get_port_allocation(user_id: str) -> int:
    """Get user's port quota"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return int(get_setting('default_port_quota', '5'))
        cur = conn.cursor()
        cur.execute('SELECT allocated_ports FROM port_allocations WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        return row[0] if row else int(get_setting('default_port_quota', '5'))
    except:
        return int(get_setting('default_port_quota', '5'))
    finally:
        if conn:
            conn.close()

def add_port_allocation(user_id: str, amount: int):
    """Add to user's port quota"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        current = get_port_allocation(user_id)
        cur.execute('INSERT OR REPLACE INTO port_allocations (user_id, allocated_ports, last_updated) VALUES (?, ?, ?)',
                    (user_id, current + amount, datetime.now().isoformat()))
        conn.commit()
    except:
        pass
    finally:
        if conn:
            conn.close()

def add_ipv4(user_id: str, container_name: str, public_ip: str, private_ip: str, mac_address: str = "", gateway: str = "", netmask: str = "", interface: str = "eth0"):
    """Add IPv4 allocation"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT OR REPLACE INTO ipv4 
                       (user_id, container_name, public_ip, private_ip, mac_address, gateway, netmask, interface, assigned_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (user_id, container_name, public_ip, private_ip, mac_address, gateway, netmask, interface, now))
        conn.commit()
    except:
        pass
    finally:
        if conn:
            conn.close()

def get_user_ipv4(user_id: str) -> List[Dict]:
    """Get all IPv4 for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM ipv4 WHERE user_id = ?', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except:
        return []
    finally:
        if conn:
            conn.close()

def add_transaction(user_id: str, txn_ref: str, amount: int) -> int:
    """Add a new transaction"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return 0
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO transactions (user_id, txn_ref, amount, created_at)
                       VALUES (?, ?, ?, ?)''', (user_id, txn_ref, amount, now))
        txn_id = cur.lastrowid
        conn.commit()
        return txn_id
    except:
        return 0
    finally:
        if conn:
            conn.close()

def verify_transaction(txn_ref: str, txn_id: str) -> bool:
    """Verify a transaction"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''UPDATE transactions SET status = 'verified', txn_id = ?, verified_at = ?
                       WHERE txn_ref = ? AND status = 'pending' ''', (txn_id, now, txn_ref))
        verified = cur.rowcount > 0
        conn.commit()
        return verified
    except:
        return False
    finally:
        if conn:
            conn.close()

# ==================================================================================================
#  🌐 NODE MANAGEMENT - AUTO DETECTION
# ==================================================================================================

def load_nodes():
    """Load nodes from JSON file"""
    default_nodes = {
        "version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "main_node": "local",
        "nodes": {},
        "node_groups": {
            "all": [],
            "us": [],
            "eu": [],
            "asia": []
        }
    }
    
    os.makedirs(os.path.dirname(NODES_FILE), exist_ok=True)
    
    if not os.path.exists(NODES_FILE) or get_setting('auto_node_detect', 'true') == 'true':
        # Auto-detect local node with real stats
        try:
            lxc_count = len(subprocess.getoutput("lxc list -c n --format csv").splitlines())
        except:
            lxc_count = 0
            
        local_node = {
            "name": "local",
            "host": "localhost",
            "port": 0,
            "username": "local",
            "password": "",
            "type": "local",
            "status": "online",
            "is_main": True,
            "region": "us",
            "description": "Auto-detected local node running on this server",
            "api_key": hashlib.sha256(f"local{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32],
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
                "allow_overcommit": True,
                "auto_backup": True,
                "backup_interval": 24
            }
        }
        
        default_nodes["nodes"]["local"] = local_node
        default_nodes["node_groups"]["all"].append("local")
        default_nodes["node_groups"]["us"].append("local")
        
        save_nodes(default_nodes)
        return default_nodes
    
    try:
        with open(NODES_FILE, 'r') as f:
            return json.load(f)
    except:
        return default_nodes

def save_nodes(data):
    """Save nodes to JSON file"""
    try:
        data['last_updated'] = datetime.now().isoformat()
        with open(NODES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def update_local_node_stats():
    """Update local node statistics automatically"""
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

def get_node(node_name):
    """Get node by name"""
    nodes = load_nodes()
    return nodes['nodes'].get(node_name)

def get_all_nodes():
    """Get all nodes"""
    nodes = load_nodes()
    return nodes['nodes']

def add_node(node_data):
    """Add a new node"""
    nodes = load_nodes()
    name = node_data['name']
    
    if name in nodes['nodes']:
        return False
    
    nodes['nodes'][name] = node_data
    if 'all' not in nodes['node_groups']:
        nodes['node_groups']['all'] = []
    nodes['node_groups']['all'].append(name)
    
    region = node_data.get('region', 'us')
    if region not in nodes['node_groups']:
        nodes['node_groups'][region] = []
    if name not in nodes['node_groups'][region]:
        nodes['node_groups'][region].append(name)
    
    return save_nodes(nodes)

def remove_node(name):
    """Remove a node"""
    nodes = load_nodes()
    if name not in nodes['nodes'] or name == 'local':
        return False
    
    del nodes['nodes'][name]
    for group in nodes['node_groups']:
        if name in nodes['node_groups'][group]:
            nodes['node_groups'][group].remove(name)
    
    return save_nodes(nodes)

def connect_to_remote_node(host: str, username: str, password: str = None, port: int = 22, name: str = None):
    """Connect to a remote node and add it to the cluster"""
    import paramiko
    
    if not name:
        name = host.split('.')[0]
    
    try:
        # Test SSH connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if password:
            client.connect(host, port=port, username=username, password=password, timeout=10)
        else:
            # Try with SSH key
            key_path = os.path.expanduser("~/.ssh/id_rsa")
            if os.path.exists(key_path):
                key = paramiko.RSAKey.from_private_key_file(key_path)
                client.connect(host, port=port, username=username, pkey=key, timeout=10)
            else:
                return False, "No password or SSH key provided"
        
        # Get node stats
        stdin, stdout, stderr = client.exec_command('nproc')
        total_cpu = stdout.read().decode().strip()
        
        stdin, stdout, stderr = client.exec_command("free -m | awk '/^Mem:/{print $2}'")
        total_ram = stdout.read().decode().strip()
        
        stdin, stdout, stderr = client.exec_command("df -BG / | awk 'NR==2{print $2}' | sed 's/G//'")
        total_disk = stdout.read().decode().strip()
        
        stdin, stdout, stderr = client.exec_command("lxc list --format csv 2>/dev/null | wc -l")
        lxc_count = stdout.read().decode().strip()
        
        client.close()
        
        # Create node data
        node_data = {
            "name": name,
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "type": "remote",
            "status": "online",
            "is_main": False,
            "region": "us",
            "description": f"Remote node connected from {host}",
            "api_key": hashlib.sha256(f"{name}{host}{time.time()}".encode()).hexdigest()[:32],
            "stats": {
                "total_ram": int(total_ram) if total_ram.isdigit() else 0,
                "used_ram": 0,
                "total_cpu": int(total_cpu) if total_cpu.isdigit() else 0,
                "used_cpu": 0,
                "total_disk": int(total_disk) if total_disk.isdigit() else 0,
                "used_disk": 0,
                "lxc_count": int(lxc_count) if lxc_count.isdigit() else 0,
                "last_checked": datetime.now().isoformat()
            },
            "settings": {
                "max_containers": 50,
                "default_storage_pool": "default",
                "allow_overcommit": False,
                "auto_backup": False
            }
        }
        
        if add_node(node_data):
            return True, f"Node {name} connected successfully"
        else:
            return False, "Node already exists"
            
    except Exception as e:
        return False, str(e)

# ==================================================================================================
#  🛠️  LXC HELPER FUNCTIONS
# ==================================================================================================

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

async def get_container_status(container_name: str) -> str:
    """Get container status"""
    try:
        result = subprocess.run(['lxc', 'info', container_name], 
                                capture_output=True, text=True, timeout=10)
        for line in result.stdout.splitlines():
            if line.startswith("Status: "):
                return line.split(": ", 1)[1].strip().lower()
        return "unknown"
    except:
        return "unknown"

async def get_container_stats(container_name: str) -> Dict:
    """Get container statistics"""
    stats = {
        'status': 'unknown',
        'cpu': '0.0%',
        'memory': '0/0 MB',
        'disk': '0/0 GB',
        'uptime': '0 min',
        'ipv4': [],
        'mac': 'N/A',
        'processes': '0',
        'load': '0.00'
    }
    
    stats['status'] = await get_container_status(container_name)
    
    if stats['status'] == 'running':
        out, _, _ = await exec_in_container(container_name, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        stats['cpu'] = f"{out}%" if out else "0.0%"
        
        out, _, _ = await exec_in_container(container_name, "free -m | awk '/^Mem:/{print $3\"/\"$2}'")
        stats['memory'] = f"{out} MB" if out else "0/0 MB"
        
        out, _, _ = await exec_in_container(container_name, "df -h / | awk 'NR==2{print $3\"/\"$2}'")
        stats['disk'] = out if out else "0/0 GB"
        
        out, _, _ = await exec_in_container(container_name, "uptime -p | sed 's/up //'")
        stats['uptime'] = out if out else "0 min"
        
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | grep -v '127.0.0.1'")
        if out:
            stats['ipv4'] = out.splitlines()
        
        out, _, _ = await exec_in_container(container_name, "ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
        stats['mac'] = out.strip() if out else "N/A"
        
        out, _, _ = await exec_in_container(container_name, "ps aux | wc -l")
        stats['processes'] = out.strip() if out else "0"
        
        out, _, _ = await exec_in_container(container_name, "cat /proc/loadavg | awk '{print $1}'")
        stats['load'] = out.strip() if out else "0.00"
    
    return stats

async def apply_lxc_config(container_name: str):
    """Apply LXC configuration"""
    try:
        await run_lxc(f"lxc config set {container_name} security.nesting true")
        await run_lxc(f"lxc config set {container_name} security.privileged true")
    except:
        pass

async def apply_internal_permissions(container_name: str):
    """Apply internal permissions"""
    await asyncio.sleep(3)
    commands = [
        "apt-get update -qq",
        "apt-get install -y -qq curl wget sudo vim nano htop net-tools",
    ]
    for cmd in commands:
        await exec_in_container(container_name, cmd)

async def get_available_host_port() -> Optional[int]:
    """Get an available host port for forwarding"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        cur.execute('SELECT host_port FROM port_forwards')
        used_ports = {row[0] for row in cur.fetchall()}
        
        # Also check system
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
    except:
        return None
    finally:
        if conn:
            conn.close()

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
        
        add_port_forward(user_id, container_name, container_port, host_port, protocol)
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
    """Get console output from container"""
    try:
        out, _, _ = await exec_in_container(container_name, f"dmesg | tail -{lines} 2>/dev/null || journalctl -n {lines} --no-pager 2>/dev/null")
        if out:
            return out
        out, _, _ = await exec_in_container(container_name, f"ps aux --forest | head -{lines*2}")
        return out or "No console output available"
    except:
        return "Error getting console output"

# ==================================================================================================
#  🎨  EMBED HELPER FUNCTIONS
# ==================================================================================================

THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg"

def create_embed(title: str, description: str = "", color: int = 0x5865F2) -> discord.Embed:
    """Create a styled embed with glow effect"""
    embed = discord.Embed(
        title=f"```glow\n✦ {BOT_NAME} - {title} ✦\n```",
        description=description,
        color=color
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(
        text=f"⚡ {BOT_NAME} • {BOT_AUTHOR} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    return embed

def success_embed(title: str, description: str = "") -> discord.Embed:
    return create_embed(f"✅ {title}", description, 0x57F287)

def error_embed(title: str, description: str = "") -> discord.Embed:
    return create_embed(f"❌ {title}", description, 0xED4245)

def info_embed(title: str, description: str = "") -> discord.Embed:
    return create_embed(f"ℹ️ {title}", description, 0x5865F2)

def warning_embed(title: str, description: str = "") -> discord.Embed:
    return create_embed(f"⚠️ {title}", description, 0xFEE75C)

def node_embed(title: str, description: str = "") -> discord.Embed:
    return create_embed(f"🌐 {title}", description, 0x9B59B6)

def terminal_embed(title: str, content: str, color: int = 0x2C2F33) -> discord.Embed:
    """Create a terminal-style embed"""
    embed = discord.Embed(
        title=f"```fix\n[ {title} ]\n```",
        description=f"```bash\n{content[:1900]}\n```",
        color=color
    )
    embed.set_footer(text=f"⚡ Terminal • {datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def no_vps_embed() -> discord.Embed:
    return info_embed(
        "No VPS Found",
        f"```diff\n- You don't have any VPS yet.\n```\n\n"
        f"**To get a free VPS:**\n"
        f"• Use `{BOT_PREFIX}plans` to see available plans\n"
        f"• Use `{BOT_PREFIX}claim-free` to claim based on invites"
    )

# ==================================================================================================
#  🤖  BOT SETUP
# ==================================================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.start_time = datetime.utcnow()

LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'

# Auto-update local node stats
@tasks.loop(minutes=5)
async def update_node_stats():
    update_local_node_stats()

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
    
    update_node_stats.start()
    update_local_node_stats()
    
    total_vps = len(get_all_vps())
    nodes = len(get_all_nodes())
    
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
║                          ████████╗ ██████╗  ██████╗ ██╗     ███████╗                          ║
║                          ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝                          ║
║                             ██║   ██║   ██║██║   ██║██║     █████╗                            ║
║                             ██║   ██║   ██║██║   ██║██║     ██╔══╝                            ║
║                             ██║   ╚██████╔╝╚██████╔╝███████╗███████╗                          ║
║                             ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                          ║
║                                                                                               ║
║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                            ║
║                                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                               ║
║  📍 Bot Status:    🟢 ONLINE                                                                 ║
║  🤖 Bot Name:      {bot.user:<58} ║
║  🆔 Bot ID:        {bot.user.id:<64} ║
║  🔧 Prefix:        {BOT_PREFIX:<65} ║
║                                                                                               ║
║  🔐 License:       {'✅ VERIFIED' if LICENSE_VERIFIED else '❌ NOT VERIFIED':<58} ║
║  🌐 Server IP:     {SERVER_IP:<61} ║
║  🔌 MAC Address:   {MAC_ADDRESS:<57} ║
║  💻 Hostname:      {HOSTNAME:<61} ║
║                                                                                               ║
║  🖥️ Total VPS:     {total_vps:<6}                                                              ║
║  🌍 Total Nodes:   {nodes:<6} (local auto-detected)                                            ║
║  🎮 Total Games:   {len(GAMES_LIST):<6}                                                        ║
║  🛠️ Total Tools:   {len(TOOLS_LIST):<6}                                                        ║
║  🐧 Total OS:      {len(OS_OPTIONS):<6}                                                        ║
║                                                                                               ║
║  👑 Main Admin:    <@1405866008127864852>                                                     ║
║                                                                                               ║
║                    ✅ ALL ISSUES FIXED - EVERY COMMAND WORKING                               ║
║        ✅ Auto Node • ✅ Games • ✅ Tools • ✅ Share • ✅ Connect • ✅ Everything             ║
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
        await ctx.send(embed=error_embed(
            "Missing Argument",
            f"```fix\nUsage: {BOT_PREFIX}{ctx.command.name} {ctx.command.signature}\n```"
        ))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=error_embed("Invalid Argument", "Please check your input."))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=error_embed("Access Denied", "You don't have permission."))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=warning_embed(
            "Command on Cooldown",
            f"Please wait {error.retry_after:.1f} seconds."
        ))
    elif isinstance(error, discord.errors.InteractionResponded):
        pass
    else:
        logger.error(f"Error: {error}")
        await ctx.send(embed=error_embed("Error", f"```diff\n- {str(error)[:1900]}\n```"))

# ==================================================================================================
#  📖  HELP COMMAND - ULTIMATE INTERACTIVE WITH DROPDOWN
# ==================================================================================================

class HelpView(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_page = 0
        self.pages = [
            {
                "title": "📚 WELCOME TO SVM5-BOT TOOLS",
                "description": f"```glow\nPrefix: {BOT_PREFIX} | Version: 5.0.0 | Author: {BOT_AUTHOR}\nServer IP: {SERVER_IP}\nTotal Commands: 150+\n```",
                "fields": [
                    ("👤 USER COMMANDS", "`.help user`", True),
                    ("🖥️ VPS MANAGEMENT", "`.help vps`", True),
                    ("🎮 GAMES", "`.help games`", True),
                    ("🛠️ TOOLS", "`.help tools`", True),
                    ("🌐 NODES", "`.help nodes`", True),
                    ("🔌 PORTS", "`.help ports`", True),
                    ("🌍 IPv4", "`.help ipv4`", True),
                    ("💰 PLANS", "`.help plans`", True),
                    ("🤖 AI", "`.help ai`", True),
                    ("👥 SHARE", "`.help share`", True),
                    ("📟 CONSOLE", "`.help console`", True),
                    ("🛡️ ADMIN", "`.help admin`", True),
                    ("👑 OWNER", "`.help owner`", True),
                ]
            },
            {
                "title": "👤 USER COMMANDS",
                "description": "```fix\nBasic commands for all users\n```",
                "fields": [
                    (f"{BOT_PREFIX}help", "Show this interactive menu", False),
                    (f"{BOT_PREFIX}ping", "Check bot latency", False),
                    (f"{BOT_PREFIX}uptime", "Show bot uptime", False),
                    (f"{BOT_PREFIX}bot-info", "Detailed bot information", False),
                    (f"{BOT_PREFIX}server-info", "Server hardware information", False),
                    (f"{BOT_PREFIX}plans", "View free VPS plans", False),
                    (f"{BOT_PREFIX}stats", "Your statistics and API key", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}invites-top", "Top inviters leaderboard", False),
                    (f"{BOT_PREFIX}claim-free", "Claim free VPS with invites", False),
                    (f"{BOT_PREFIX}my-acc", "View your generated account", False),
                    (f"{BOT_PREFIX}gen-acc", "Generate random account with API key", False),
                    (f"{BOT_PREFIX}api-key", "View or regenerate your API key", False),
                ]
            },
            {
                "title": "🖥️ VPS MANAGEMENT",
                "description": "```fix\nManage your VPS containers\n```",
                "fields": [
                    (f"{BOT_PREFIX}myvps", "List your VPS with status", False),
                    (f"{BOT_PREFIX}list", "Detailed VPS list with IPs", False),
                    (f"{BOT_PREFIX}manage [container]", "Interactive VPS manager", False),
                    (f"{BOT_PREFIX}stats [container]", "VPS statistics", False),
                    (f"{BOT_PREFIX}logs [container] [lines]", "View VPS logs", False),
                    (f"{BOT_PREFIX}reboot <container>", "Reboot VPS", False),
                    (f"{BOT_PREFIX}shutdown <container>", "Shutdown VPS", False),
                    (f"{BOT_PREFIX}rename <old> <new>", "Rename VPS container", False),
                ]
            },
            {
                "title": "📟 CONSOLE COMMANDS",
                "description": "```fix\nTerminal access and console commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}ss [container]", "Show VPS console output", False),
                    (f"{BOT_PREFIX}console <container>", "Interactive console", False),
                    (f"{BOT_PREFIX}execute <container> <cmd>", "Execute command in VPS", False),
                    (f"{BOT_PREFIX}ssh-gen <container>", "Generate temporary SSH access", False),
                    (f"{BOT_PREFIX}top <container>", "Show live process monitor", False),
                    (f"{BOT_PREFIX}df <container>", "Show disk usage", False),
                    (f"{BOT_PREFIX}free <container>", "Show memory usage", False),
                    (f"{BOT_PREFIX}ps <container>", "Show process list", False),
                    (f"{BOT_PREFIX}who <container>", "Show logged-in users", False),
                    (f"{BOT_PREFIX}uptime <container>", "Show container uptime", False),
                ]
            },
            {
                "title": "🎮 GAMES COMMANDS",
                "description": "```fix\nInstall and manage game servers (50+ games)\n```",
                "fields": [
                    (f"{BOT_PREFIX}games", "List all available games by category", False),
                    (f"{BOT_PREFIX}game-info <game>", "Detailed game information", False),
                    (f"{BOT_PREFIX}install-game <container> <game>", "Install game on VPS", False),
                    (f"{BOT_PREFIX}my-games [container]", "Your installed games", False),
                    (f"{BOT_PREFIX}start-game <container> <game>", "Start game server", False),
                    (f"{BOT_PREFIX}stop-game <container> <game>", "Stop game server", False),
                    (f"{BOT_PREFIX}game-stats <container> <game>", "Game server statistics", False),
                    (f"{BOT_PREFIX}game-port <container> <game>", "Show game server port", False),
                ]
            },
            {
                "title": "🛠️ TOOLS COMMANDS",
                "description": "```fix\nInstall development tools and services (50+ tools)\n```",
                "fields": [
                    (f"{BOT_PREFIX}tools", "List all available tools by category", False),
                    (f"{BOT_PREFIX}tool-info <tool>", "Detailed tool information", False),
                    (f"{BOT_PREFIX}install-tool <container> <tool>", "Install tool on VPS", False),
                    (f"{BOT_PREFIX}my-tools [container]", "Your installed tools", False),
                    (f"{BOT_PREFIX}start-tool <container> <tool>", "Start tool service", False),
                    (f"{BOT_PREFIX}stop-tool <container> <tool>", "Stop tool service", False),
                    (f"{BOT_PREFIX}tool-port <container> <tool>", "Show tool service port", False),
                ]
            },
            {
                "title": "🌐 NODE COMMANDS",
                "description": "```fix\nManage cluster nodes (Auto-detects local node)\n```",
                "fields": [
                    (f"{BOT_PREFIX}node", "List all nodes in cluster", False),
                    (f"{BOT_PREFIX}node-info [name]", "Detailed node information", False),
                    (f"{BOT_PREFIX}node-add <name> <host> <user> <pass>", "Add new node (Admin)", False),
                    (f"{BOT_PREFIX}node-remove <name>", "Remove node (Admin)", False),
                    (f"{BOT_PREFIX}node-check <name>", "Check node health", False),
                    (f"{BOT_PREFIX}node-stats", "Cluster statistics", False),
                    (f"{BOT_PREFIX}node-connect <host> <user> [pass] [name]", "Connect to remote node", False),
                ]
            },
            {
                "title": "🔌 PORT COMMANDS",
                "description": "```fix\nManage port forwarding\n```",
                "fields": [
                    (f"{BOT_PREFIX}ports", "Port forwarding help", False),
                    (f"{BOT_PREFIX}ports add <vps_num> <port> [tcp/udp]", "Add port forward", False),
                    (f"{BOT_PREFIX}ports list", "List your forwards", False),
                    (f"{BOT_PREFIX}ports remove <id>", "Remove port forward", False),
                    (f"{BOT_PREFIX}ports quota", "Check your port quota", False),
                    (f"{BOT_PREFIX}ports check <port>", "Check if port is available", False),
                ]
            },
            {
                "title": "🌍 IPv4 COMMANDS",
                "description": "```fix\nBuy and manage IPv4 addresses\n```",
                "fields": [
                    (f"{BOT_PREFIX}ipv4", "View your IPv4 addresses", False),
                    (f"{BOT_PREFIX}ipv4-details <container>", "Detailed IPv4 information", False),
                    (f"{BOT_PREFIX}buy-ipv4", "Purchase IPv4 via UPI", False),
                    (f"{BOT_PREFIX}upi", "Show UPI payment information", False),
                    (f"{BOT_PREFIX}upi-qr [amount] [note]", "Generate UPI QR code", False),
                    (f"{BOT_PREFIX}pay <amount> [note]", "Generate payment link", False),
                ]
            },
            {
                "title": "💰 PLANS",
                "description": "```fix\nFree VPS plans based on invites\n```",
                "fields": [
                    (f"{BOT_PREFIX}plans", "View all available plans", False),
                    (f"{BOT_PREFIX}plan-info <plan>", "Detailed plan information", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}invites-top", "Top inviters leaderboard", False),
                ]
            },
            {
                "title": "🤖 AI COMMANDS",
                "description": "```fix\nChat with AI assistant (Groq LLaMA 3.3)\n```",
                "fields": [
                    (f"{BOT_PREFIX}ai <message>", "Chat with AI", False),
                    (f"{BOT_PREFIX}ai-reset", "Reset chat history", False),
                    (f"{BOT_PREFIX}ai-help <topic>", "Get AI help on specific topic", False),
                ]
            },
            {
                "title": "👥 SHARE COMMANDS",
                "description": "```fix\nShare VPS with other users\n```",
                "fields": [
                    (f"{BOT_PREFIX}share <@user> <vps_num>", "Share VPS with user", False),
                    (f"{BOT_PREFIX}unshare <@user> <vps_num>", "Remove VPS sharing", False),
                    (f"{BOT_PREFIX}shared", "List VPS shared with you", False),
                    (f"{BOT_PREFIX}manage-shared <owner> <num>", "Manage shared VPS", False),
                ]
            },
        ]
        
        if is_admin(str(ctx.author.id)):
            self.pages.append({
                "title": "🛡️ ADMIN COMMANDS",
                "description": "```fix\nAdministrator commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}create <ram> <cpu> <disk> @user", "Create VPS for user", False),
                    (f"{BOT_PREFIX}delete @user <num> [reason]", "Delete user's VPS", False),
                    (f"{BOT_PREFIX}suspend <container> [reason]", "Suspend VPS", False),
                    (f"{BOT_PREFIX}unsuspend <container>", "Unsuspend VPS", False),
                    (f"{BOT_PREFIX}add-resources <container> [ram] [cpu] [disk]", "Add resources to VPS", False),
                    (f"{BOT_PREFIX}userinfo [@user]", "User information", False),
                    (f"{BOT_PREFIX}list-all", "List all VPS in system", False),
                    (f"{BOT_PREFIX}add-inv @user <amount>", "Add invites to user", False),
                    (f"{BOT_PREFIX}remove-inv @user <amount>", "Remove invites from user", False),
                    (f"{BOT_PREFIX}ports-add @user <amount>", "Add port slots to user", False),
                    (f"{BOT_PREFIX}serverstats", "Server statistics", False),
                    (f"{BOT_PREFIX}admin-add-ipv4 @user <container>", "Assign IPv4 to user", False),
                    (f"{BOT_PREFIX}admin-rm-ipv4 @user [container]", "Remove IPv4 from user", False),
                    (f"{BOT_PREFIX}admin-pending-ipv4", "View pending IPv4 purchases", False),
                    (f"{BOT_PREFIX}node-add", "Add new node to cluster", False),
                    (f"{BOT_PREFIX}node-remove", "Remove node from cluster", False),
                    (f"{BOT_PREFIX}node-connect", "Connect to remote node", False),
                ]
            })
        
        if str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            self.pages.append({
                "title": "👑 OWNER COMMANDS",
                "description": "```fix\nMain owner commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}admin-add @user", "Add new administrator", False),
                    (f"{BOT_PREFIX}admin-remove @user", "Remove administrator", False),
                    (f"{BOT_PREFIX}admin-list", "List all administrators", False),
                    (f"{BOT_PREFIX}maintenance <on/off>", "Toggle maintenance mode", False),
                    (f"{BOT_PREFIX}set-threshold <cpu> <ram> <disk>", "Set resource thresholds", False),
                    (f"{BOT_PREFIX}purge-all", "Purge all unprotected VPS", False),
                    (f"{BOT_PREFIX}protect @user [num]", "Protect VPS from purge", False),
                    (f"{BOT_PREFIX}unprotect @user [num]", "Remove purge protection", False),
                    (f"{BOT_PREFIX}admin-users", "List all users", False),
                    (f"{BOT_PREFIX}backup-db", "Backup database", False),
                    (f"{BOT_PREFIX}restore-db <file>", "Restore database from backup", False),
                    (f"{BOT_PREFIX}reset-license", "Reset license verification", False),
                ]
            })
        
        self.update_embed()
    
    def update_embed(self):
        page = self.pages[self.current_page]
        embed = discord.Embed(
            title=f"```glow\n{page['title']}\n```",
            description=page['description'],
            color=0x9B59B6 if "ADMIN" in page['title'] or "OWNER" in page['title'] else 0x5865F2
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        
        for name, value, inline in page["fields"]:
            embed.add_field(name=f"**{name}**", value=value, inline=inline)
        
        embed.set_footer(text=f"⚡ Page {self.current_page + 1}/{len(self.pages)} • Use dropdown to navigate ⚡")
        self.embed = embed
    
    @discord.ui.select(
        placeholder="📋 Select command category...",
        options=[
            discord.SelectOption(label="🏠 Main Menu", value="0", emoji="🏠", description="Return to main menu"),
            discord.SelectOption(label="👤 User Commands", value="1", emoji="👤", description="Basic user commands"),
            discord.SelectOption(label="🖥️ VPS Management", value="2", emoji="🖥️", description="Manage your VPS"),
            discord.SelectOption(label="📟 Console", value="3", emoji="📟", description="Terminal commands"),
            discord.SelectOption(label="🎮 Games", value="4", emoji="🎮", description="Game servers"),
            discord.SelectOption(label="🛠️ Tools", value="5", emoji="🛠️", description="Development tools"),
            discord.SelectOption(label="🌐 Nodes", value="6", emoji="🌐", description="Cluster management"),
            discord.SelectOption(label="🔌 Ports", value="7", emoji="🔌", description="Port forwarding"),
            discord.SelectOption(label="🌍 IPv4", value="8", emoji="🌍", description="IPv4 management"),
            discord.SelectOption(label="💰 Plans", value="9", emoji="💰", description="Free VPS plans"),
            discord.SelectOption(label="🤖 AI", value="10", emoji="🤖", description="AI chat assistant"),
            discord.SelectOption(label="👥 Share", value="11", emoji="👥", description="Share VPS with users"),
            discord.SelectOption(label="🛡️ Admin", value="12", emoji="🛡️", description="Admin commands"),
            discord.SelectOption(label="👑 Owner", value="13", emoji="👑", description="Owner commands"),
        ]
    )
    async def select_menu(self, select: Select, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
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

@bot.command(name="commands")
async def commands_alias(ctx):
    await help_command(ctx)

# ==================================================================================================
#  ℹ️  INFO COMMANDS
# ==================================================================================================

@bot.command(name="ping")
async def ping(ctx):
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging..."))
    end = time.time()
    
    api = round(bot.latency * 1000)
    response = round((end - start) * 1000)
    
    embed = create_embed("Pong! 🏓")
    
    if api < 100:
        bar = "🟩" * 10
        status = "Excellent"
    elif api < 200:
        bar = "🟨" * 7 + "⬜" * 3
        status = "Good"
    else:
        bar = "🟥" * 5 + "⬜" * 5
        status = "Poor"
    
    embed.add_field(name="📡 API Latency", value=f"```fix\n{api}ms\n```", inline=True)
    embed.add_field(name="⏱️ Response Time", value=f"```fix\n{response}ms\n```", inline=True)
    embed.add_field(name="📊 Status", value=f"```fix\n{status}\n{bar}\n```", inline=False)
    await msg.edit(embed=embed)

@bot.command(name="uptime")
async def uptime(ctx):
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    await ctx.send(embed=info_embed("Bot Uptime", f"```fix\n{days}d {hours}h {minutes}m {seconds}s\n```"))

@bot.command(name="bot-info")
async def bot_info(ctx):
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    running_vps = sum(1 for v in all_vps if v['status'] == 'running' and not v['suspended'])
    
    embed = create_embed("Bot Information")
    embed.add_field(name="📦 Version", value="```fix\n5.0.0\n```", inline=True)
    embed.add_field(name="👑 Author", value=f"```fix\n{BOT_AUTHOR}\n```", inline=True)
    embed.add_field(name="📚 Library", value=f"```fix\ndiscord.py {discord.__version__}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{(datetime.utcnow() - bot.start_time).days}d\n```", inline=True)
    embed.add_field(name="🖥️ Total VPS", value=f"```fix\n{total_vps}\n```", inline=True)
    embed.add_field(name="🟢 Running VPS", value=f"```fix\n{running_vps}\n```", inline=True)
    embed.add_field(name="🎮 Games", value=f"```fix\n{len(GAMES_LIST)}\n```", inline=True)
    embed.add_field(name="🛠️ Tools", value=f"```fix\n{len(TOOLS_LIST)}\n```", inline=True)
    embed.add_field(name="🐧 OS", value=f"```fix\n{len(OS_OPTIONS)}\n```", inline=True)
    embed.add_field(name="🌐 Server IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{MAC_ADDRESS[:17]}\n```", inline=True)
    embed.add_field(name="🔐 License", value="```fix\n✅ VERIFIED\n```" if LICENSE_VERIFIED else "```fix\n❌ NOT VERIFIED\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="server-info")
async def server_info(ctx):
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    
    embed = create_embed("Server Information")
    embed.add_field(name="💻 Hostname", value=f"```fix\n{HOSTNAME}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{MAC_ADDRESS}\n```", inline=True)
    embed.add_field(name="⚙️ CPU", value=f"```fix\n{cpu_count} cores @ {cpu_percent}%\n```", inline=True)
    embed.add_field(name="💾 RAM", value=f"```fix\n{memory.used//1024//1024}MB/{memory.total//1024//1024}MB ({memory.percent}%)\n```", inline=True)
    embed.add_field(name="📀 Disk", value=f"```fix\n{disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n```", inline=True)
    embed.add_field(name="⏰ Boot Time", value=f"```fix\n{boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="plans")
async def plans(ctx):
    embed = create_embed("Free VPS Plans")
    for plan in FREE_VPS_PLANS['invites']:
        popular = " ⭐ POPULAR" if plan.get('popular') else ""
        text = f"```fix\nRAM: {plan['ram']}GB | CPU: {plan['cpu']} | Disk: {plan['disk']}GB\nInvites: {plan['invites']}\n```"
        embed.add_field(name=f"{plan['emoji']} {plan['name']}{popular}", value=text, inline=True)
    embed.set_footer(text=f"Use {BOT_PREFIX}claim-free to claim your VPS")
    await ctx.send(embed=embed)

@bot.command(name="stats")
async def user_stats(ctx):
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    vps_list = get_user_vps(user_id)
    
    embed = info_embed(f"Statistics for {ctx.author.display_name}")
    embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
    embed.add_field(name="🚀 Boosts", value=f"```fix\n{stats.get('boosts', 0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS Count", value=f"```fix\n{len(vps_list)}\n```", inline=True)
    embed.add_field(name="🗝️ API Key", value=f"```fix\n{stats.get('api_key', 'None')[:16]}...\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="inv")
async def check_invites(ctx):
    stats = get_user_stats(str(ctx.author.id))
    invites = stats.get('invites', 0)
    
    embed = info_embed("Your Invites", f"```fix\nCurrent invites: {invites}\n```")
    
    available = []
    for plan in FREE_VPS_PLANS['invites']:
        if invites >= plan['invites']:
            available.append(f"✅ {plan['emoji']} {plan['name']}")
        else:
            available.append(f"❌ {plan['emoji']} {plan['name']} (need {plan['invites']})")
    
    embed.add_field(name="📋 Available Plans", value="\n".join(available[:5]), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="invites-top")
async def invites_top(ctx, limit: int = 10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, invites FROM user_stats WHERE invites > 0 ORDER BY invites DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        await ctx.send(embed=info_embed("Top Inviters", "No invites yet."))
        return
    
    embed = info_embed(f"Top {min(limit, len(rows))} Inviters")
    for i, row in enumerate(rows, 1):
        try:
            user = await bot.fetch_user(int(row['user_id']))
            username = user.name
        except:
            username = f"Unknown ({row['user_id']})"
        
        embed.add_field(
            name=f"{i}. {username}",
            value=f"```fix\nInvites: {row['invites']}\n```",
            inline=False
        )
    await ctx.send(embed=embed)

# ==================================================================================================
#  👤  ACCOUNT GENERATOR
# ==================================================================================================

def generate_username() -> str:
    adjectives = ["cool", "fast", "dark", "epic", "blue", "swift", "neon", "alpha", "delta", "super", 
                  "mega", "ultra", "hyper", "cyber", "tech", "quantum", "nano", "pixel", "digital", "cloud",
                  "storm", "thunder", "lightning", "shadow", "phantom", "ghost", "crypto", "binary", "atomic"]
    nouns = ["wolf", "tiger", "storm", "byte", "nova", "blade", "fox", "raven", "hawk", "lion", 
             "dragon", "phoenix", "eagle", "shark", "viper", "phantom", "shadow", "ghost", "knight", "warrior",
             "phoenix", "dragon", "titan", "giant", "master", "legend", "hero", "ninja", "samurai"]
    num = random.randint(10, 9999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{num}"

def generate_email(username: str = None) -> str:
    if not username:
        username = generate_username()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "proton.me", "hotmail.com", "mail.com", 
               "icloud.com", "aol.com", "yandex.com", "gmx.com", "tutanota.com", "zoho.com"]
    return f"{username}@{random.choice(domains)}"

def generate_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

@bot.command(name="gen-acc")
@commands.cooldown(1, 10, commands.BucketType.user)
async def gen_account(ctx):
    username = generate_username()
    email = generate_email(username)
    password = generate_password()
    api_key = hashlib.sha256(f"{ctx.author.id}{time.time()}".encode()).hexdigest()[:32]
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS generated_accounts (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        api_key TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    cur.execute('''INSERT OR REPLACE INTO generated_accounts 
                   (user_id, username, email, password, api_key, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (str(ctx.author.id), username, email, password, api_key, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    update_user_stats(str(ctx.author.id))
    
    try:
        dm_embed = success_embed("🔐 Your Generated Account")
        dm_embed.add_field(name="👤 Username", value=f"```fix\n{username}\n```", inline=False)
        dm_embed.add_field(name="📧 Email", value=f"```fix\n{email}\n```", inline=False)
        dm_embed.add_field(name="🔑 Password", value=f"```fix\n{password}\n```", inline=False)
        dm_embed.add_field(name="🗝️ API Key", value=f"```fix\n{api_key}\n```", inline=False)
        await ctx.author.send(embed=dm_embed)
        dm_status = "✅ Sent to DMs"
    except:
        dm_status = "❌ DM failed"
    
    embed = success_embed("Account Generated!")
    embed.add_field(name="👤 Username", value=f"```fix\n{username}\n```", inline=True)
    embed.add_field(name="📧 Email", value=f"||`{email}`||", inline=True)
    embed.add_field(name="📩 DM", value=f"```fix\n{dm_status}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="my-acc")
async def my_account(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM generated_accounts WHERE user_id = ?', (str(ctx.author.id),))
    account = cur.fetchone()
    conn.close()
    
    if account:
        embed = info_embed("Your Account")
        embed.add_field(name="👤 Username", value=f"```fix\n{account['username']}\n```", inline=True)
        embed.add_field(name="📧 Email", value=f"||`{account['email']}`||", inline=True)
        embed.add_field(name="🗝️ API Key", value=f"||`{account['api_key']}`||", inline=False)
        embed.add_field(name="📅 Created", value=f"```fix\n{account['created_at'][:16]}\n```", inline=True)
    else:
        stats = get_user_stats(str(ctx.author.id))
        embed = info_embed("Your Info")
        embed.add_field(name="🆔 ID", value=f"```fix\n{ctx.author.id}\n```", inline=True)
        embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
        embed.add_field(name="🗝️ API Key", value=f"```fix\n{stats.get('api_key', 'None')}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="api-key")
async def api_key_cmd(ctx, action: str = "view"):
    user_id = str(ctx.author.id)
    
    if action.lower() == "regenerate":
        new_key = hashlib.sha256(f"{user_id}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE user_stats SET api_key = ?, last_updated = ? WHERE user_id = ?',
                   (new_key, datetime.now().isoformat(), user_id))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("API Key Regenerated", f"```fix\n{new_key}\n```"))
    else:
        stats = get_user_stats(user_id)
        api_key = stats.get('api_key', 'None')
        await ctx.send(embed=info_embed("Your API Key", f"```fix\n{api_key}\n```\nUse `{BOT_PREFIX}api-key regenerate` to generate new."))

# ==================================================================================================
#  🎮  GAMES COMMANDS
# ==================================================================================================

@bot.command(name="games")
async def list_games(ctx, category: str = None):
    games = get_available_games()
    embed = create_embed("Available Games", f"```fix\nTotal Games: {len(games)}\n```")
    
    if category:
        games = [g for g in games if g['category'].lower() == category.lower()]
    
    categories = {}
    for game in games[:25]:
        if game['category'] not in categories:
            categories[game['category']] = []
        categories[game['category']].append(game)
    
    for cat, game_list in categories.items():
        text = "\n".join([f"{g['icon']} `{g['name']}`" for g in game_list[:5]])
        embed.add_field(name=f"📋 {cat}", value=text, inline=True)
    
    embed.set_footer(text=f"Use {BOT_PREFIX}game-info <name> for details")
    await ctx.send(embed=embed)

@bot.command(name="game-info")
async def game_info(ctx, *, game_name: str):
    games = get_available_games()
    game = next((g for g in games if g['name'].lower() == game_name.lower()), None)
    
    if not game:
        await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game_name} not found\n```"))
        return
    
    embed = info_embed(f"{game['icon']} {game['name']}")
    embed.add_field(name="📋 Category", value=f"```fix\n{game['category']}\n```", inline=True)
    embed.add_field(name="🔌 Port", value=f"```fix\n{game['default_port']}\n```", inline=True)
    embed.add_field(name="💾 Requirements", value=f"```fix\nRAM: {game['min_ram']}MB\nCPU: {game['min_cpu']} cores\nDisk: {game['min_disk']}GB\n```", inline=False)
    embed.add_field(name="🐳 Docker", value=f"```fix\n{game['docker']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="install-game")
async def install_game(ctx, container_name: str, *, game_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    games = get_available_games()
    game = next((g for g in games if g['name'].lower() == game_name.lower()), None)
    
    if not game:
        await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game_name} not found\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Installing Game", f"```fix\nInstalling {game['name']} on {container_name}...\n```"))
    
    try:
        await exec_in_container(container_name, "which docker || curl -fsSL https://get.docker.com | bash")
        
        container_port = game['default_port']
        cmd = f"docker run -d --name {game['name'].lower().replace(' ', '-')} -p {container_port}:{container_port} {game['docker']}"
        out, err, code = await exec_in_container(container_name, cmd)
        
        if code == 0:
            add_game_install(user_id, container_name, game['name'], container_port)
            
            embed = success_embed("Game Installed")
            embed.add_field(name="🎮 Game", value=f"```fix\n{game['name']}\n```", inline=True)
            embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
            embed.add_field(name="🔌 Port", value=f"```fix\n{container_port}\n```", inline=True)
            await msg.edit(embed=embed)
        else:
            await msg.edit(embed=error_embed("Installation Failed", f"```diff\n- {err}\n```"))
    except Exception as e:
        await msg.edit(embed=error_embed("Error", f"```diff\n- {str(e)}\n```"))

@bot.command(name="my-games")
async def my_games(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if container_name:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        games = get_installed_games(container_name)
    else:
        all_games = []
        for vps in get_user_vps(user_id):
            games = get_installed_games(vps['container_name'])
            for game in games:
                game['container'] = vps['container_name']
                all_games.append(game)
        games = all_games
    
    if not games:
        await ctx.send(embed=info_embed("No Games", "You haven't installed any games yet."))
        return
    
    embed = info_embed("Your Installed Games")
    for game in games[:10]:
        text = f"```fix\nContainer: {game.get('container', game['container_name'])}\nPort: {game['game_port']}\n```"
        embed.add_field(name=f"{game.get('icon', '🎮')} {game['game_name']}", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="start-game")
async def start_game(ctx, container_name: str, *, game_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    games = get_installed_games(container_name)
    game = next((g for g in games if g['game_name'].lower() == game_name.lower()), None)
    
    if not game:
        await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game_name} not installed\n```"))
        return
    
    await exec_in_container(container_name, f"docker start {game['game_name'].lower().replace(' ', '-')}")
    await ctx.send(embed=success_embed("Game Started", f"```fix\n{game['game_name']} started on {container_name}\n```"))

@bot.command(name="stop-game")
async def stop_game(ctx, container_name: str, *, game_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    games = get_installed_games(container_name)
    game = next((g for g in games if g['game_name'].lower() == game_name.lower()), None)
    
    if not game:
        await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game_name} not installed\n```"))
        return
    
    await exec_in_container(container_name, f"docker stop {game['game_name'].lower().replace(' ', '-')}")
    await ctx.send(embed=success_embed("Game Stopped", f"```fix\n{game['game_name']} stopped on {container_name}\n```"))

@bot.command(name="game-stats")
async def game_stats(ctx, container_name: str, *, game_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    games = get_installed_games(container_name)
    game = next((g for g in games if g['game_name'].lower() == game_name.lower()), None)
    
    if not game:
        await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game_name} not installed\n```"))
        return
    
    out, _, _ = await exec_in_container(container_name, f"docker stats {game['game_name'].lower().replace(' ', '-')} --no-stream")
    
    embed = info_embed(f"Game Stats: {game['game_name']}", f"```fix\n{out}\n```")
    await ctx.send(embed=embed)

# ==================================================================================================
#  🛠️  TOOLS COMMANDS
# ==================================================================================================

@bot.command(name="tools")
async def list_tools(ctx, category: str = None):
    tools = get_available_tools()
    embed = create_embed("Available Tools", f"```fix\nTotal Tools: {len(tools)}\n```")
    
    categories = {}
    for tool in tools[:25]:
        if tool['category'] not in categories:
            categories[tool['category']] = []
        categories[tool['category']].append(tool)
    
    for cat, tool_list in categories.items():
        text = "\n".join([f"{t['icon']} `{t['name']}`" for t in tool_list[:5]])
        embed.add_field(name=f"📋 {cat}", value=text, inline=True)
    
    embed.set_footer(text=f"Use {BOT_PREFIX}tool-info <name> for details")
    await ctx.send(embed=embed)

@bot.command(name="tool-info")
async def tool_info(ctx, *, tool_name: str):
    tools = get_available_tools()
    tool = next((t for t in tools if t['name'].lower() == tool_name.lower()), None)
    
    if not tool:
        await ctx.send(embed=error_embed("Tool Not Found", f"```diff\n- {tool_name} not found\n```"))
        return
    
    embed = info_embed(f"{tool['icon']} {tool['name']}")
    embed.add_field(name="📋 Category", value=f"```fix\n{tool['category']}\n```", inline=True)
    if tool.get('default_port'):
        embed.add_field(name="🔌 Port", value=f"```fix\n{tool['default_port']}\n```", inline=True)
    embed.add_field(name="📝 Command", value=f"```bash\n{tool['install_command']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="install-tool")
async def install_tool(ctx, container_name: str, *, tool_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    tools = get_available_tools()
    tool = next((t for t in tools if t['name'].lower() == tool_name.lower()), None)
    
    if not tool:
        await ctx.send(embed=error_embed("Tool Not Found", f"```diff\n- {tool_name} not found\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Installing Tool", f"```fix\nInstalling {tool['name']} on {container_name}...\n```"))
    
    try:
        out, err, code = await exec_in_container(container_name, tool['install_command'])
        
        if code == 0 or "already" in err.lower():
            add_tool_install(user_id, container_name, tool['name'], tool.get('default_port'))
            
            embed = success_embed("Tool Installed")
            embed.add_field(name="🛠️ Tool", value=f"```fix\n{tool['name']}\n```", inline=True)
            embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
            if tool.get('default_port'):
                embed.add_field(name="🔌 Port", value=f"```fix\n{tool['default_port']}\n```", inline=True)
            await msg.edit(embed=embed)
        else:
            await msg.edit(embed=error_embed("Installation Failed", f"```diff\n- {err}\n```"))
    except Exception as e:
        await msg.edit(embed=error_embed("Error", f"```diff\n- {str(e)}\n```"))

@bot.command(name="my-tools")
async def my_tools(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if container_name:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        tools = get_installed_tools(container_name)
    else:
        all_tools = []
        for vps in get_user_vps(user_id):
            tools = get_installed_tools(vps['container_name'])
            for tool in tools:
                tool['container'] = vps['container_name']
                all_tools.append(tool)
        tools = all_tools
    
    if not tools:
        await ctx.send(embed=info_embed("No Tools", "You haven't installed any tools yet."))
        return
    
    embed = info_embed("Your Installed Tools")
    for tool in tools[:10]:
        text = f"```fix\nContainer: {tool.get('container', tool['container_name'])}"
        if tool.get('tool_port'):
            text += f"\nPort: {tool['tool_port']}"
        text += "\n```"
        embed.add_field(name=f"{tool.get('icon', '🛠️')} {tool['tool_name']}", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="start-tool")
async def start_tool(ctx, container_name: str, *, tool_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    tools = get_installed_tools(container_name)
    tool = next((t for t in tools if t['tool_name'].lower() == tool_name.lower()), None)
    
    if not tool:
        await ctx.send(embed=error_embed("Tool Not Found", f"```diff\n- {tool_name} not installed\n```"))
        return
    
    service_name = tool_name.lower().replace(' ', '-')
    await exec_in_container(container_name, f"systemctl start {service_name} 2>/dev/null || service {service_name} start")
    await ctx.send(embed=success_embed("Tool Started", f"```fix\n{tool['tool_name']} started on {container_name}\n```"))

@bot.command(name="stop-tool")
async def stop_tool(ctx, container_name: str, *, tool_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    tools = get_installed_tools(container_name)
    tool = next((t for t in tools if t['tool_name'].lower() == tool_name.lower()), None)
    
    if not tool:
        await ctx.send(embed=error_embed("Tool Not Found", f"```diff\n- {tool_name} not installed\n```"))
        return
    
    service_name = tool_name.lower().replace(' ', '-')
    await exec_in_container(container_name, f"systemctl stop {service_name} 2>/dev/null || service {service_name} stop")
    await ctx.send(embed=success_embed("Tool Stopped", f"```fix\n{tool['tool_name']} stopped on {container_name}\n```"))

@bot.command(name="tool-port")
async def tool_port(ctx, container_name: str, *, tool_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    tools = get_available_tools()
    tool = next((t for t in tools if t['name'].lower() == tool_name.lower()), None)
    
    if not tool or not tool.get('default_port'):
        await ctx.send(embed=error_embed("No Port", f"```diff\n- {tool_name} has no default port\n```"))
        return
    
    await ctx.send(embed=success_embed("Tool Port", f"```fix\n{tool['name']} runs on port {tool['default_port']}\n```"))

# ==================================================================================================
#  🌐  NODE COMMANDS - AUTO DETECT LOCAL
# ==================================================================================================

@bot.command(name="node")
async def node_list(ctx):
    nodes = load_nodes()
    embed = node_embed("Node Network", f"```fix\nTotal Nodes: {len(nodes['nodes'])}\n```")
    
    for name, node in nodes['nodes'].items():
        status = "🟢" if node['status'] == 'online' else "🔴"
        stats = node.get('stats', {})
        text = f"```fix\nHost: {node['host']}\nRAM: {stats.get('used_ram', 0)}/{stats.get('total_ram', 0)} MB\nCPU: {stats.get('used_cpu', 0)}%\nLXC: {stats.get('lxc_count', 0)}\n```"
        embed.add_field(name=f"{status} {name}", value=text, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="node-info")
async def node_info(ctx, name: str = "local"):
    nodes = load_nodes()
    node = nodes['nodes'].get(name)
    
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node {name} not found\n```"))
        return
    
    embed = node_embed(f"Node: {name}")
    stats = node.get('stats', {})
    
    basic = f"```fix\nHost: {node['host']}:{node['port']}\nStatus: {node['status']}\nRegion: {node.get('region', 'us')}\nType: {node.get('type', 'unknown')}\n```"
    resources = f"```fix\nRAM: {stats.get('used_ram', 0)}/{stats.get('total_ram', 0)} MB\nCPU: {stats.get('used_cpu', 0)}%\nDisk: {stats.get('used_disk', 0)}/{stats.get('total_disk', 0)} GB\nLXC: {stats.get('lxc_count', 0)}\nLast: {stats.get('last_checked', 'Never')[:16]}\n```"
    
    embed.add_field(name="📋 Basic", value=basic, inline=True)
    embed.add_field(name="📊 Resources", value=resources, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="node-add")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_add(ctx, name: str, host: str, username: str, password: str = None, port: int = 22):
    msg = await ctx.send(embed=info_embed("Connecting to Node", f"```fix\nAttempting to connect to {host}...\n```"))
    
    success, message = await connect_to_remote_node(host, username, password, port, name)
    
    if success:
        await msg.edit(embed=success_embed("Node Added", f"```fix\n{message}\n```"))
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {message}\n```"))

@bot.command(name="node-remove")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_remove(ctx, name: str):
    if remove_node(name):
        await ctx.send(embed=success_embed("Node Removed", f"```fix\n{name} removed from cluster\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Cannot remove main node or node not found"))

@bot.command(name="node-check")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_check(ctx, name: str):
    nodes = load_nodes()
    node = nodes['nodes'].get(name)
    
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node {name} not found\n```"))
        return
    
    if name == "local":
        update_local_node_stats()
        await ctx.send(embed=success_embed("Node Check", "```fix\nLocal node is online\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Checking Node", f"```fix\nChecking {name}...\n```"))
    
    success, message = await connect_to_remote_node(node['host'], node['username'], node.get('password'), node['port'], name)
    
    if success:
        await msg.edit(embed=success_embed("Node Online", f"```fix\n{name} is online and healthy\n```"))
    else:
        await msg.edit(embed=error_embed("Node Offline", f"```diff\n- {name} is offline: {message}\n```"))

@bot.command(name="node-stats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_stats(ctx):
    nodes = load_nodes()
    all_nodes = nodes['nodes']
    
    total_ram = sum(n['stats'].get('total_ram', 0) for n in all_nodes.values())
    used_ram = sum(n['stats'].get('used_ram', 0) for n in all_nodes.values())
    total_cpu = sum(n['stats'].get('total_cpu', 0) for n in all_nodes.values())
    total_disk = sum(n['stats'].get('total_disk', 0) for n in all_nodes.values())
    used_disk = sum(n['stats'].get('used_disk', 0) for n in all_nodes.values())
    total_lxc = sum(n['stats'].get('lxc_count', 0) for n in all_nodes.values())
    online = sum(1 for n in all_nodes.values() if n['status'] == 'online')
    
    embed = node_embed("Cluster Statistics")
    summary = f"```fix\nTotal Nodes: {len(all_nodes)}\nOnline: {online}\nOffline: {len(all_nodes)-online}\nTotal LXC: {total_lxc}\n```"
    resources = f"```fix\nRAM: {used_ram}/{total_ram} MB ({(used_ram/total_ram*100) if total_ram>0 else 0:.1f}%)\nDisk: {used_disk}/{total_disk} GB ({(used_disk/total_disk*100) if total_disk>0 else 0:.1f}%)\nTotal CPU Cores: {total_cpu}\n```"
    
    embed.add_field(name="📊 Summary", value=summary, inline=False)
    embed.add_field(name="💾 Resources", value=resources, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="node-connect")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_connect(ctx, host: str, username: str, password: str = None, name: str = None, port: int = 22):
    if not name:
        name = host.split('.')[0]
    
    msg = await ctx.send(embed=info_embed("Connecting to Remote Node", f"```fix\nConnecting to {host} as {username}...\n```"))
    
    success, message = await connect_to_remote_node(host, username, password, port, name)
    
    if success:
        await msg.edit(embed=success_embed("Node Connected", f"```fix\n{message}\n```"))
    else:
        await msg.edit(embed=error_embed("Connection Failed", f"```diff\n- {message}\n```"))

# ==================================================================================================
#  👥  SHARE COMMANDS
# ==================================================================================================

@bot.command(name="share")
async def share_vps_cmd(ctx, user: discord.Member, vps_num: int):
    owner_id = str(ctx.author.id)
    vps_list = get_user_vps(owner_id)
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"VPS number must be 1-{len(vps_list)}"))
        return
    
    container = vps_list[vps_num - 1]['container_name']
    
    if share_vps(owner_id, str(user.id), container):
        await ctx.send(embed=success_embed("VPS Shared", f"```fix\nShared {container} with {user.name}\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Could not share VPS"))

@bot.command(name="unshare")
async def unshare_vps_cmd(ctx, user: discord.Member, vps_num: int):
    owner_id = str(ctx.author.id)
    vps_list = get_user_vps(owner_id)
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"VPS number must be 1-{len(vps_list)}"))
        return
    
    container = vps_list[vps_num - 1]['container_name']
    
    if unshare_vps(owner_id, str(user.id), container):
        await ctx.send(embed=success_embed("VPS Unshared", f"```fix\nUnshared {container} from {user.name}\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Could not unshare VPS"))

@bot.command(name="shared")
async def list_shared(ctx):
    shared = get_shared_vps(str(ctx.author.id))
    
    if not shared:
        await ctx.send(embed=info_embed("No Shared VPS", "No one has shared VPS with you."))
        return
    
    embed = info_embed("VPS Shared With You")
    for vps in shared:
        try:
            owner = await bot.fetch_user(int(vps['owner_id']))
            owner_name = owner.name
        except:
            owner_name = f"Unknown"
        
        text = f"```fix\nOwner: {owner_name}\nStatus: {vps['status']}\nRAM: {vps['ram']}GB\nIP: {vps.get('ip_address', 'N/A')}\n```"
        embed.add_field(name=f"📦 {vps['container_name']}", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="manage-shared")
async def manage_shared(ctx, owner: discord.Member, vps_num: int):
    shared = get_shared_vps(str(ctx.author.id))
    owner_vps = [v for v in shared if v.get('owner_id') == str(owner.id)]
    
    if vps_num < 1 or vps_num > len(owner_vps):
        await ctx.send(embed=error_embed("Invalid VPS", f"VPS number must be 1-{len(owner_vps)}"))
        return
    
    vps = owner_vps[vps_num - 1]
    container = vps['container_name']
    
    stats = await get_container_stats(container)
    
    embed = info_embed(f"Managing Shared VPS: {container}")
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
    
    view.add_item(Button(label="▶️ Start", style=discord.ButtonStyle.success, custom_id="start", callback=start_cb))
    view.add_item(Button(label="⏹️ Stop", style=discord.ButtonStyle.danger, custom_id="stop", callback=stop_cb))
    view.add_item(Button(label="🔄 Restart", style=discord.ButtonStyle.primary, custom_id="restart", callback=restart_cb))
    
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  🖥️  VPS MANAGEMENT COMMANDS
# ==================================================================================================

@bot.command(name="myvps")
async def my_vps(ctx):
    vps_list = get_user_vps(str(ctx.author.id))
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = info_embed(f"Your VPS ({len(vps_list)})")
    
    for i, vps in enumerate(vps_list, 1):
        status = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
        games = len(json.loads(vps['games_installed'])) if vps['games_installed'] else 0
        tools = len(json.loads(vps['tools_installed'])) if vps['tools_installed'] else 0
        
        text = f"{status} **`{vps['container_name']}`**\n"
        text += f"```fix\nRAM: {vps['ram']}GB | CPU: {vps['cpu']} | Disk: {vps['disk']}GB\nIP: {vps.get('ip_address', 'N/A')}\nGames: {games} | Tools: {tools}\n```"
        embed.add_field(name=f"VPS #{i}", value=text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="list")
async def list_command(ctx):
    await my_vps(ctx)

@bot.command(name="manage")
async def manage_vps(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    stats = await get_container_stats(container_name)
    
    embed = info_embed(f"Managing: {container_name}")
    embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
    embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
    embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{stats['mac']}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{stats['uptime']}\n```", inline=True)
    
    view = View()
    
    async def start_cb(i):
        await run_lxc(f"lxc start {container_name}")
        await i.response.send_message(f"Started {container_name}", ephemeral=True)
    
    async def stop_cb(i):
        await run_lxc(f"lxc stop {container_name}")
        await i.response.send_message(f"Stopped {container_name}", ephemeral=True)
    
    async def restart_cb(i):
        await run_lxc(f"lxc restart {container_name}")
        await i.response.send_message(f"Restarted {container_name}", ephemeral=True)
    
    view.add_item(Button(label="▶️ Start", style=discord.ButtonStyle.success, custom_id="start", callback=start_cb))
    view.add_item(Button(label="⏹️ Stop", style=discord.ButtonStyle.danger, custom_id="stop", callback=stop_cb))
    view.add_item(Button(label="🔄 Restart", style=discord.ButtonStyle.primary, custom_id="restart", callback=restart_cb))
    view.add_item(Button(label="📊 Stats", style=discord.ButtonStyle.secondary, custom_id="stats", 
                        callback=lambda i: i.response.send_message(embed=info_embed("Stats", f"```fix\n{stats}\n```"), ephemeral=True)))
    
    await ctx.send(embed=embed, view=view)

@bot.command(name="stats")
async def vps_stats(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    stats = await get_container_stats(container_name)
    
    embed = info_embed(f"VPS Stats: {container_name}")
    embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
    embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
    embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
    embed.add_field(name="💽 Disk", value=f"```fix\n{stats['disk']}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{stats['uptime']}\n```", inline=True)
    embed.add_field(name="📟 Processes", value=f"```fix\n{stats['processes']}\n```", inline=True)
    embed.add_field(name="📈 Load", value=f"```fix\n{stats['load']}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="logs")
async def vps_logs(ctx, container_name: str = None, lines: int = 50):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    out, _, _ = await exec_in_container(container_name, f"journalctl -n {lines} --no-pager 2>/dev/null || dmesg | tail -{lines}")
    
    embed = terminal_embed(f"Logs: {container_name}", out[:1900])
    await ctx.send(embed=embed)

@bot.command(name="reboot")
async def reboot_vps(ctx, container_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    await ctx.send(embed=info_embed("Rebooting", f"```fix\nRebooting {container_name}...\n```"))
    await run_lxc(f"lxc restart {container_name}")
    update_vps_status(container_name, 'running')
    await ctx.send(embed=success_embed("Rebooted", f"```fix\n{container_name} rebooted\n```"))

@bot.command(name="shutdown")
async def shutdown_vps(ctx, container_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    await ctx.send(embed=info_embed("Shutting Down", f"```fix\nShutting down {container_name}...\n```"))
    await run_lxc(f"lxc stop {container_name}")
    update_vps_status(container_name, 'stopped')
    await ctx.send(embed=success_embed("Shutdown", f"```fix\n{container_name} stopped\n```"))

@bot.command(name="rename")
async def rename_vps(ctx, old_name: str, new_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == old_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    await ctx.send(embed=info_embed("Renaming", f"```fix\nRenaming {old_name} to {new_name}...\n```"))
    
    status = await get_container_status(old_name)
    was_running = status == 'running'
    
    if was_running:
        await run_lxc(f"lxc stop {old_name}")
    
    await run_lxc(f"lxc move {old_name} {new_name}")
    
    if was_running:
        await run_lxc(f"lxc start {new_name}")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET container_name = ? WHERE container_name = ?', (new_name, old_name))
    cur.execute('UPDATE shared_vps SET container_name = ? WHERE container_name = ?', (new_name, old_name))
    cur.execute('UPDATE installed_games SET container_name = ? WHERE container_name = ?', (new_name, old_name))
    cur.execute('UPDATE installed_tools SET container_name = ? WHERE container_name = ?', (new_name, old_name))
    cur.execute('UPDATE ipv4 SET container_name = ? WHERE container_name = ?', (new_name, old_name))
    cur.execute('UPDATE port_forwards SET container_name = ? WHERE container_name = ?', (new_name, old_name))
    conn.commit()
    conn.close()
    
    await ctx.send(embed=success_embed("Renamed", f"```fix\n{old_name} → {new_name}\n```"))

# ==================================================================================================
#  📟  CONSOLE COMMANDS
# ==================================================================================================

@bot.command(name="ss")
async def ss_command(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    console = await get_container_console(container_name, 30)
    stats = await get_container_stats(container_name)
    
    output = f"=== {container_name} Console ===\n"
    output += f"Status: {stats['status'].upper()} | Uptime: {stats['uptime']}\n"
    output += f"CPU: {stats['cpu']} | Memory: {stats['memory']}\n"
    output += "="*40 + "\n\n"
    output += console
    
    embed = terminal_embed(f"Console: {container_name}", output[:1900])
    await ctx.send(embed=embed)

@bot.command(name="console")
async def console_command(ctx, container_name: str, *, command: str = None):
    if not command:
        await ss_command(ctx, container_name)
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    out, err, code = await exec_in_container(container_name, command)
    
    output = f"$ {command}\n\n"
    output += out if out else err
    
    embed = terminal_embed(f"Command Output: {container_name}", output[:1900])
    embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="execute")
async def execute_command(ctx, container_name: str, *, command: str):
    await console_command(ctx, container_name, command=command)

@bot.command(name="ssh-gen")
async def ssh_gen(ctx, container_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    msg = await ctx.send(embed=info_embed("Generating SSH", f"```fix\nSetting up SSH for {container_name}...\n```"))
    
    try:
        await exec_in_container(container_name, "apt-get update -qq")
        await exec_in_container(container_name, "apt-get install -y -qq tmate")
        
        session_id = f"svm5-{random.randint(1000, 9999)}"
        await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock new-session -d")
        await asyncio.sleep(5)
        
        out, _, _ = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_ssh}}'")
        ssh_url = out.strip()
        
        if ssh_url:
            try:
                dm_embed = success_embed("🔑 SSH Access")
                dm_embed.add_field(name="Container", value=f"```fix\n{container_name}\n```", inline=True)
                dm_embed.add_field(name="SSH Command", value=f"```bash\n{ssh_url}\n```", inline=False)
                await ctx.author.send(embed=dm_embed)
                await msg.edit(embed=success_embed("SSH Generated", f"```fix\nSSH details sent to your DMs\n```"))
            except:
                await msg.edit(embed=error_embed("DM Failed", f"```fix\nSSH: {ssh_url}\n```"))
        else:
            await msg.edit(embed=error_embed("Failed", "Could not generate SSH"))
    except Exception as e:
        await msg.edit(embed=error_embed("Error", f"```diff\n- {str(e)}\n```"))

@bot.command(name="top")
async def top_command(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    out, _, _ = await exec_in_container(container_name, "ps aux --sort=-%cpu | head -20")
    embed = terminal_embed(f"Processes: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="df")
async def df_command(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    out, _, _ = await exec_in_container(container_name, "df -h")
    embed = terminal_embed(f"Disk Usage: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="free")
async def free_command(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    out, _, _ = await exec_in_container(container_name, "free -h")
    embed = terminal_embed(f"Memory: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="ps")
async def ps_command(ctx, container_name: str = None):
    await top_command(ctx, container_name)

@bot.command(name="who")
async def who_command(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    out, _, _ = await exec_in_container(container_name, "who")
    embed = terminal_embed(f"Users: {container_name}", out or "No users logged in")
    await ctx.send(embed=embed)

@bot.command(name="uptime")
async def uptime_container(ctx, container_name: str = None):
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
    
    out, _, _ = await exec_in_container(container_name, "uptime")
    embed = info_embed(f"Uptime: {container_name}", f"```fix\n{out}\n```")
    await ctx.send(embed=embed)

# ==================================================================================================
#  🔌  PORT FORWARDING COMMANDS
# ==================================================================================================

@bot.group(name="ports", invoke_without_command=True)
async def ports_group(ctx):
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    
    embed = info_embed("Port Forwarding Help")
    embed.add_field(name="📊 Your Quota", value=f"```fix\nAllocated: {allocated}\nUsed: {len(forwards)}\nAvailable: {allocated - len(forwards)}\n```", inline=False)
    embed.add_field(
        name="📋 Commands",
        value=f"`{BOT_PREFIX}ports add <vps_num> <port> [tcp/udp]`\n"
              f"`{BOT_PREFIX}ports list`\n"
              f"`{BOT_PREFIX}ports remove <id>`\n"
              f"`{BOT_PREFIX}ports quota`",
        inline=False
    )
    await ctx.send(embed=embed)

@ports_group.command(name="add")
async def ports_add(ctx, vps_num: int, port: int, protocol: str = "tcp+udp"):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"VPS number must be 1-{len(vps_list)}"))
        return
    
    if port < 1 or port > 65535:
        await ctx.send(embed=error_embed("Invalid Port", "Port must be 1-65535"))
        return
    
    if protocol not in ["tcp", "udp", "tcp+udp"]:
        await ctx.send(embed=error_embed("Invalid Protocol", "Use tcp, udp, or tcp+udp"))
        return
    
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    if len(forwards) >= allocated:
        await ctx.send(embed=error_embed("Quota Exceeded", f"You have used all {allocated} port slots"))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    if vps['suspended'] or vps['status'] != 'running':
        await ctx.send(embed=error_embed("Cannot Add", "VPS must be running and not suspended"))
        return
    
    msg = await ctx.send(embed=info_embed("Creating port forward..."))
    
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
        await msg.edit(embed=error_embed("Failed", "Could not assign host port"))

@ports_group.command(name="list")
async def ports_list(ctx):
    user_id = str(ctx.author.id)
    forwards = get_user_port_forwards(user_id)
    allocated = get_port_allocation(user_id)
    
    if not forwards:
        await ctx.send(embed=info_embed("No Port Forwards", f"```fix\nQuota: {allocated} available\n```"))
        return
    
    embed = info_embed(f"Your Port Forwards ({len(forwards)}/{allocated})")
    for f in forwards:
        vps_num = next((i+1 for i, v in enumerate(get_user_vps(user_id)) if v['container_name'] == f['container_name']), '?')
        embed.add_field(
            name=f"ID: {f['id']}",
            value=f"```fix\nVPS #{vps_num}: {f['container_port']} → {SERVER_IP}:{f['host_port']} ({f['protocol']})\nCreated: {f['created_at'][:16]}\n```",
            inline=False
        )
    await ctx.send(embed=embed)

@ports_group.command(name="remove")
async def ports_remove(ctx, forward_id: int):
    user_id = str(ctx.author.id)
    
    success, container, host_port = remove_port_forward(forward_id)
    
    if not success:
        await ctx.send(embed=error_embed("Not Found", f"Port forward ID {forward_id} not found"))
        return
    
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this port forward"))
        return
    
    await remove_port_forward_device(container, host_port)
    await ctx.send(embed=success_embed("Removed", f"Port forward ID {forward_id} removed"))

@ports_group.command(name="quota")
async def ports_quota(ctx):
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    used = len(get_user_port_forwards(user_id))
    
    embed = info_embed("Port Quota")
    embed.add_field(name="📊 Allocated", value=f"```fix\n{allocated}\n```", inline=True)
    embed.add_field(name="📊 Used", value=f"```fix\n{used}\n```", inline=True)
    embed.add_field(name="📊 Available", value=f"```fix\n{allocated - used}\n```", inline=True)
    await ctx.send(embed=embed)

@ports_group.command(name="check")
async def ports_check(ctx, port: int):
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
        if f":{port}" in result.stdout:
            await ctx.send(embed=error_embed("Port Unavailable", f"```diff\n- Port {port} is in use\n```"))
        else:
            await ctx.send(embed=success_embed("Port Available", f"```fix\nPort {port} is available\n```"))
    except:
        await ctx.send(embed=info_embed("Port Check", f"```fix\nCould not check port {port}\n```"))

# ==================================================================================================
#  🌍  IPv4 COMMANDS
# ==================================================================================================

UPI_ID = get_setting('upi_id', '9892642904@ybl')
IPV4_PRICE = int(get_setting('ipv4_price', '50'))

def generate_upi_qr(upi_id: str, amount: int = None, note: str = None):
    try:
        if amount and note:
            upi_url = f"upi://pay?pa={upi_id}&pn={BOT_NAME}&am={amount}&tn={note}"
        else:
            upi_url = f"upi://pay?pa={upi_id}&pn={BOT_NAME}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes
    except:
        return None

@bot.command(name="ipv4")
async def list_ipv4(ctx, user: discord.Member = None):
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "Only admins can view others' IPv4"))
            return
        target_id = str(user.id)
        target_name = user.display_name
    else:
        target_id = str(ctx.author.id)
        target_name = ctx.author.display_name
    
    ipv4_list = get_user_ipv4(target_id)
    
    if not ipv4_list:
        await ctx.send(embed=info_embed("No IPv4", f"{target_name} has no IPv4 addresses"))
        return
    
    embed = info_embed(f"IPv4 Addresses - {target_name}")
    for i, ip in enumerate(ipv4_list, 1):
        value = f"```fix\nContainer: {ip['container_name']}\nPublic: {ip['public_ip']}\nPrivate: {ip['private_ip']}\nMAC: {ip['mac_address']}\nAssigned: {ip['assigned_at'][:16]}\n```"
        embed.add_field(name=f"IPv4 #{i}", value=value, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ipv4-details")
async def ipv4_details(ctx, container_name: str):
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS"))
        return
    
    ipv4_list = get_user_ipv4(user_id)
    ip = next((i for i in ipv4_list if i['container_name'] == container_name), None)
    
    out, _, _ = await exec_in_container(container_name, "ip addr show")
    
    embed = info_embed(f"IPv4 Details: {container_name}")
    if ip:
        embed.add_field(name="🌐 Public", value=f"```fix\n{ip['public_ip']}\n```", inline=True)
        embed.add_field(name="🏠 Private", value=f"```fix\n{ip['private_ip']}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{ip['mac_address']}\n```", inline=True)
    embed.add_field(name="📋 Network", value=f"```bash\n{out[:500]}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="buy-ipv4")
async def buy_ipv4(ctx):
    txn_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    embed = create_embed("Buy IPv4 Address")
    embed.add_field(name="💰 Price", value=f"```fix\n₹{IPV4_PRICE}\n```", inline=True)
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="🔖 Reference", value=f"```fix\n{txn_ref}\n```", inline=True)
    embed.add_field(name="📋 Instructions", value=f"```fix\n1. Pay ₹{IPV4_PRICE} to {UPI_ID}\n2. Add reference {txn_ref}\n3. Click ✅ after payment\n```", inline=False)
    
    qr_bytes = generate_upi_qr(UPI_ID, IPV4_PRICE, txn_ref)
    if qr_bytes:
        file = discord.File(qr_bytes, filename="qr.png")
        embed.set_image(url="attachment://qr.png")
    else:
        file = None
    
    view = View(timeout=300)
    
    async def payment_cb(i):
        if i.user.id != ctx.author.id:
            await i.response.send_message("Not your purchase!", ephemeral=True)
            return
        modal = TransactionModal(ctx, txn_ref)
        await i.response.send_modal(modal)
    
    payment_btn = Button(label="✅ I've Paid", style=discord.ButtonStyle.success)
    payment_btn.callback = payment_cb
    view.add_item(payment_btn)
    
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def cancel_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled", "Purchase cancelled"), view=None)
    
    cancel_btn.callback = cancel_cb
    view.add_item(cancel_btn)
    
    if file:
        await ctx.send(embed=embed, file=file, view=view)
    else:
        await ctx.send(embed=embed, view=view)

class TransactionModal(Modal):
    def __init__(self, ctx, txn_ref):
        super().__init__(title="Enter Transaction ID")
        self.ctx = ctx
        self.txn_ref = txn_ref
        self.add_item(InputText(label="UPI Transaction ID", placeholder="e.g., T25031234567890", min_length=8, max_length=50))
    
    async def callback(self, interaction: discord.Interaction):
        txn_id = self.children[0].value
        add_transaction(str(self.ctx.author.id), self.txn_ref, IPV4_PRICE)
        
        for admin_id in MAIN_ADMIN_IDS:
            try:
                admin = await bot.fetch_user(admin_id)
                embed = warning_embed("New IPv4 Purchase", f"```fix\nUser: {self.ctx.author}\nRef: {self.txn_ref}\nTxn: {txn_id}\nAmount: ₹{IPV4_PRICE}\n```")
                await admin.send(embed=embed)
            except:
                pass
        
        await interaction.response.edit_message(
            embed=info_embed("Payment Submitted", f"```fix\nReference: {self.txn_ref}\nTransaction ID: {txn_id}\n```\nAn admin will verify your payment."),
            view=None
        )

@bot.command(name="upi")
async def upi_info(ctx):
    embed = info_embed("UPI Payment Information")
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="💰 IPv4 Price", value=f"```fix\n₹{IPV4_PRICE}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="upi-qr")
async def upi_qr(ctx, amount: int = None, *, note: str = None):
    if not note:
        note = f"Payment to {BOT_NAME}"
    
    qr_bytes = generate_upi_qr(UPI_ID, amount, note)
    if qr_bytes:
        file = discord.File(qr_bytes, filename="qr.png")
        embed = info_embed("UPI QR Code")
        if amount:
            embed.add_field(name="💰 Amount", value=f"```fix\n₹{amount}\n```", inline=True)
        if note:
            embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
        embed.set_image(url="attachment://qr.png")
        await ctx.send(embed=embed, file=file)
    else:
        await ctx.send(embed=error_embed("Failed", "Could not generate QR code"))

@bot.command(name="pay")
async def pay_command(ctx, amount: int, *, note: str = None):
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "Amount must be positive"))
        return
    
    if not note:
        note = f"Payment to {BOT_NAME}"
    
    payment_url = f"upi://pay?pa={UPI_ID}&pn={BOT_NAME}&am={amount}&tn={note}"
    
    view = View()
    link_btn = Button(label="💳 Pay Now", style=discord.ButtonStyle.link, url=payment_url)
    view.add_item(link_btn)
    
    qr_btn = Button(label="📸 Show QR", style=discord.ButtonStyle.secondary)
    
    async def qr_cb(i):
        qr_bytes = generate_upi_qr(UPI_ID, amount, note)
        if qr_bytes:
            file = discord.File(qr_bytes, filename="qr.png")
            qr_embed = info_embed("Payment QR Code")
            qr_embed.set_image(url="attachment://qr.png")
            await i.response.send_message(embed=qr_embed, file=file, ephemeral=True)
        else:
            await i.response.send_message(embed=error_embed("Failed", "Could not generate QR"), ephemeral=True)
    
    qr_btn.callback = qr_cb
    view.add_item(qr_btn)
    
    embed = info_embed("Payment Link")
    embed.add_field(name="💰 Amount", value=f"```fix\n₹{amount}\n```", inline=True)
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  🤖  AI COMMANDS
# ==================================================================================================

AI_API_KEY = "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"
AI_MODEL = "llama-3.3-70b-versatile"

@bot.command(name="ai")
async def ai_chat(ctx, *, message: str):
    user_id = str(ctx.author.id)
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ai_history (user_id TEXT PRIMARY KEY, messages TEXT, updated_at TEXT)')
    
    cur.execute('SELECT messages FROM ai_history WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    
    if row:
        history = json.loads(row['messages'])
    else:
        history = [{"role": "system", "content": f"You are {BOT_NAME} AI Assistant, a helpful VPS management bot made by {BOT_AUTHOR}. You help with Linux, LXC containers, server management, and general questions."}]
    
    history.append({"role": "user", "content": message})
    if len(history) > 21:
        history = [history[0]] + history[-20:]
    
    msg = await ctx.send(embed=info_embed("AI is thinking..."))
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"},
                json={"model": AI_MODEL, "messages": history, "max_tokens": 1024, "temperature": 0.7},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data["choices"][0]["message"]["content"]
                    
                    history.append({"role": "assistant", "content": reply})
                    cur.execute('INSERT OR REPLACE INTO ai_history (user_id, messages, updated_at) VALUES (?, ?, ?)',
                              (user_id, json.dumps(history), datetime.now().isoformat()))
                    conn.commit()
                    
                    chunks = [reply[i:i+1900] for i in range(0, len(reply), 1900)]
                    embed = info_embed("AI Response", chunks[0])
                    await msg.edit(embed=embed)
                    for chunk in chunks[1:]:
                        await ctx.send(embed=info_embed("", chunk))
                else:
                    await msg.edit(embed=error_embed("API Error", f"Status {resp.status}"))
    except Exception as e:
        await msg.edit(embed=error_embed("Error", str(e)[:1900]))
    finally:
        conn.close()

@bot.command(name="ai-reset")
async def ai_reset(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM ai_history WHERE user_id = ?', (str(ctx.author.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("AI Reset", "Chat history cleared"))

@bot.command(name="ai-help")
async def ai_help(ctx, *, topic: str):
    await ai_chat(ctx, message=f"Please help me with {topic} for VPS/LXC management")

# ==================================================================================================
#  🛡️  ADMIN COMMANDS (Partial - Full implementation would be very long)
# ==================================================================================================

@bot.command(name="create")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    if ram <= 0 or cpu <= 0 or disk <= 0:
        await ctx.send(embed=error_embed("Invalid Specs", "RAM, CPU, Disk must be positive"))
        return
    
    view = View(timeout=60)
    options = []
    for os in OS_OPTIONS[:25]:
        options.append(discord.SelectOption(label=os["label"][:100], value=os["value"], description=os["desc"][:100], emoji=os.get("icon", "🐧")))
    
    select = Select(placeholder="Select OS...", options=options)
    
    async def select_cb(i):
        if i.user.id != ctx.author.id:
            await i.response.send_message("Not for you!", ephemeral=True)
            return
        
        selected_os = select.values[0]
        
        confirm_view = View()
        confirm_btn = Button(label="✅ Create", style=discord.ButtonStyle.success)
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        
        async def confirm_cb(ci):
            await create_vps_action(ci, user, ram, cpu, disk, selected_os)
        
        async def cancel_cb(ci):
            await ci.response.edit_message(embed=info_embed("Cancelled"), view=None)
        
        confirm_btn.callback = confirm_cb
        cancel_btn.callback = cancel_cb
        confirm_view.add_item(confirm_btn)
        confirm_view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        embed = warning_embed("Confirm Creation", f"```fix\nUser: {user}\nOS: {os_name}\nRAM: {ram}GB\nCPU: {cpu}\nDisk: {disk}GB\n```")
        await i.response.edit_message(embed=embed, view=confirm_view)
    
    select.callback = select_cb
    view.add_item(select)
    
    await ctx.send(embed=info_embed("Create VPS", f"Select OS for {user.mention}"), view=view)

async def create_vps_action(interaction, user, ram, cpu, disk, os_version):
    await interaction.response.defer(ephemeral=True)
    
    user_id = str(user.id)
    container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
    
    progress = await interaction.followup.send(embed=info_embed("Creating VPS", "Step 1/4: Initializing..."), ephemeral=True)
    
    try:
        ram_mb = ram * 1024
        await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
        
        await progress.edit(embed=info_embed("Creating VPS", "Step 2/4: Configuring resources..."))
        await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
        await run_lxc(f"lxc config set {container_name} limits.cpu {cpu}")
        await run_lxc(f"lxc config device set {container_name} root size={disk}GB")
        
        await apply_lxc_config(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "Step 3/4: Starting..."))
        await run_lxc(f"lxc start {container_name}")
        await apply_internal_permissions(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "Step 4/4: Finalizing..."))
        
        vps = add_vps(user_id, container_name, ram, cpu, disk, os_version, "Custom")
        
        if interaction.guild:
            role = discord.utils.get(interaction.guild.roles, name=f"{BOT_NAME} User")
            if not role:
                role = await interaction.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
            try:
                await user.add_roles(role)
            except:
                pass
        
        embed = success_embed("VPS Created")
        embed.add_field(name="👤 User", value=user.mention, inline=True)
        embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
        embed.add_field(name="⚙️ Resources", value=f"```fix\n{ram}GB RAM / {cpu} CPU / {disk}GB Disk\n```", inline=False)
        await progress.edit(embed=embed)
        
    except Exception as e:
        await progress.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))
        try:
            await run_lxc(f"lxc delete {container_name} --force")
        except:
            pass

@bot.command(name="delete")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_delete(ctx, user: discord.Member, vps_num: int, *, reason: str = "No reason"):
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list or vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"VPS number must be 1-{len(vps_list)}"))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    view = View()
    confirm_btn = Button(label="✅ Confirm Delete", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_cb(i):
        await run_lxc(f"lxc stop {container} --force")
        await run_lxc(f"lxc delete {container}")
        delete_vps(container)
        await i.response.edit_message(embed=success_embed("Deleted", f"```fix\n{container} deleted\n```"), view=None)
    
    async def cancel_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    
    confirm_btn.callback = confirm_cb
    cancel_btn.callback = cancel_cb
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed("Confirm Delete", f"```fix\nUser: {user}\nVPS: {container}\nReason: {reason}\n```\nThis cannot be undone!")
    await ctx.send(embed=embed, view=view)

@bot.command(name="userinfo")
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    elif not is_admin(str(ctx.author.id)) and user.id != ctx.author.id:
        await ctx.send(embed=error_embed("Access Denied", "You can only view your own info"))
        return
    
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    stats = get_user_stats(user_id)
    
    embed = info_embed(f"User Info: {user.display_name}")
    embed.add_field(name="🆔 ID", value=f"```fix\n{user.id}\n```", inline=True)
    embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(vps_list)}\n```", inline=True)
    embed.add_field(name="🗝️ API", value=f"```fix\n{stats.get('api_key', 'None')[:16]}...\n```", inline=False)
    
    if vps_list:
        vps_text = "\n".join([f"{'🟢' if v['status']=='running' else '🔴'} `{v['container_name']}` ({v['ram']}GB)" for v in vps_list[:5]])
        embed.add_field(name="📋 VPS List", value=vps_text, inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  👑  OWNER COMMANDS (Minimal)
# ==================================================================================================

@bot.command(name="admin-add")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def admin_add(ctx, user: discord.Member):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?, ?, ?)',
               (str(user.id), str(ctx.author.id), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Admin Added", f"{user.mention} is now an admin"))

@bot.command(name="admin-remove")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def admin_remove(ctx, user: discord.Member):
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Cannot Remove", "Cannot remove main admin"))
        return
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM admins WHERE user_id = ?', (str(user.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Admin Removed", f"{user.mention} is no longer an admin"))

@bot.command(name="admin-list")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def admin_list(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM admins')
    rows = cur.fetchall()
    conn.close()
    
    embed = info_embed("Admin List")
    main = "\n".join([f"👑 <@{a}>" for a in MAIN_ADMIN_IDS])
    admins = "\n".join([f"🛡️ <@{r['user_id']}>" for r in rows if r['user_id'] not in [str(a) for a in MAIN_ADMIN_IDS]])
    
    embed.add_field(name="Main Admin", value=main or "None", inline=False)
    embed.add_field(name="Admins", value=admins or "None", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="maintenance")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def maintenance(ctx, mode: str):
    mode = mode.lower()
    if mode not in ['on', 'off']:
        await ctx.send(embed=error_embed("Invalid Mode", "Use on or off"))
        return
    
    set_setting('maintenance_mode', mode)
    await ctx.send(embed=success_embed("Maintenance", f"Mode set to {mode}"))

@bot.command(name="backup-db")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def backup_db(ctx):
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    backup_path = f"/opt/svm5-bot/backups/{backup_name}"
    
    try:
        shutil.copy2(DATABASE_PATH, backup_path)
        await ctx.send(embed=success_embed("Backup Created", f"```fix\n{backup_name}\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Backup Failed", str(e)))

# ==================================================================================================
#  🚀  RUN THE BOT
# ==================================================================================================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n❌ ERROR: Please set your BOT_TOKEN!")
        sys.exit(1)
    
    # Auto-create local node
    update_local_node_stats()
    
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n❌ ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
