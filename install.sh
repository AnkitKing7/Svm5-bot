#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                 SVM5-BOT - Complete Installation Script                       ║
# ║                         Made by Ankit-Dev with ❤️                             ║
# ║                 Version: 5.0.0 | Release Date: March 2025                    ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎨  COLOR DEFINITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

R='\033[0;31m'      # Red
G='\033[0;32m'      # Green
Y='\033[1;33m'      # Yellow
B='\033[0;34m'      # Blue
P='\033[0;35m'      # Purple
C='\033[0;36m'      # Cyan
W='\033[1;37m'      # White
NC='\033[0m'        # No Color
BOLD='\033[1m'
BLINK='\033[5m'
UNDERLINE='\033[4m'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📍  PATH CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🖥️  ASCII ART HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_header() {
    clear
    echo -e "${R}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${Y}║                                                                               ║${NC}"
    echo -e "${G}║        ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗    ║${NC}"
    echo -e "${C}║        ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝    ║${NC}"
    echo -e "${B}║        ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║       ║${NC}"
    echo -e "${P}║        ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║       ║${NC}"
    echo -e "${R}║        ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║       ║${NC}"
    echo -e "${Y}║        ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝       ║${NC}"
    echo -e "${W}║                                                                               ║${NC}"
    echo -e "${G}║                    🚀 Complete VPS Management Bot v5.0 🚀                    ║${NC}"
    echo -e "${C}║                        Made by ${BOLD}Ankit-Dev${NC}${C} with ❤️                         ║${NC}"
    echo -e "${P}║                     📅 Release Date: March 2025                              ║${NC}"
    echo -e "${R}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔐  LICENSE VERIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

check_license() {
    show_header
    echo -e "${Y}┌─────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${Y}│                    🔐 LICENSE ACTIVATION                         │${NC}"
    echo -e "${Y}├─────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${W}│  This software is licensed and requires a valid license key.    │${NC}"
    echo -e "${W}│  Please enter your license key to continue installation.        │${NC}"
    echo -e "${Y}└─────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Try to read from file if exists
    if [ -f "$INSTALL_DIR/license.key" ]; then
        STORED_KEY=$(cat "$INSTALL_DIR/license.key")
        echo -e "${G}📁 Found existing license key file.${NC}"
        read -p "🔑 Use stored key? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            KEY="$STORED_KEY"
        else
            read -sp "🔑 Enter License Key: " KEY
            echo ""
        fi
    else
        read -sp "🔑 Enter License Key: " KEY
        echo ""
    fi
    
    # License key verification
    # Valid keys: AnkitDev99$@, SVM5-PRO-2025, SVM5-ENTERPRISE
    if [[ "$KEY" == "AnkitDev99\$@" ]] || [[ "$KEY" == "SVM5-PRO-2025" ]] || [[ "$KEY" == "SVM5-ENTERPRISE" ]]; then
        echo -e "${G}✅ License Verified! Access Granted.${NC}"
        
        # Save license key
        sudo mkdir -p "$INSTALL_DIR"
        echo "$KEY" | sudo tee "$INSTALL_DIR/license.key" > /dev/null
        
        sleep 1
        return 0
    else
        echo -e "${R}❌ Invalid License Key! Access Denied.${NC}"
        echo -e "${Y}Debug: Entered key: $KEY${NC}"
        echo ""
        echo -e "${C}💡 To purchase a license, contact Ankit-Dev or send payment to:${NC}"
        echo -e "${W}   UPI: 9892642904@ybl${NC}"
        echo -e "${W}   Amount: ₹499 (One-time payment)${NC}"
        echo ""
        read -p "🔄 Press Enter to try again or 'q' to quit: " retry
        if [[ "$retry" == "q" ]]; then
            exit 1
        fi
        check_license
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📋  SYSTEM CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

check_system() {
    echo -e "${C}🔍 Checking system requirements...${NC}"
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        echo -e "${R}❌ This script must be run as root!${NC}"
        echo -e "${Y}   Please run: sudo bash install.sh${NC}"
        exit 1
    fi
    
    # Check OS
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    
    echo -e "${G}✅ Operating System: $OS $VER${NC}"
    
    # Check architecture
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]] || [[ "$ARCH" == "aarch64" ]]; then
        echo -e "${G}✅ Architecture: $ARCH${NC}"
    else
        echo -e "${R}❌ Unsupported architecture: $ARCH${NC}"
        exit 1
    fi
    
    # Check disk space
    AVAILABLE_SPACE=$(df / | awk 'NR==2 {print $4}')
    if [ $AVAILABLE_SPACE -lt 10485760 ]; then
        echo -e "${Y}⚠️  Low disk space: $(($AVAILABLE_SPACE/1024/1024))GB available${NC}"
        echo -e "${Y}   Recommended: At least 10GB free space${NC}"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo -e "${G}✅ Disk space: $(($AVAILABLE_SPACE/1024/1024))GB available${NC}"
    fi
    
    echo -e "${G}✅ System check passed!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📦  INSTALL DEPENDENCIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

install_dependencies() {
    echo -e "${C}📦 Installing system dependencies...${NC}"
    
    # Update package list
    echo -e "${Y}   → Updating package lists...${NC}"
    apt update -qq
    
    # Install essential packages
    echo -e "${Y}   → Installing essential tools...${NC}"
    apt install -y -qq \
        curl \
        wget \
        git \
        unzip \
        zip \
        tar \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        lxc \
        lxc-templates \
        lxc-utils \
        bridge-utils \
        uidmap \
        snapd \
        net-tools \
        htop \
        nginx \
        ufw \
        fail2ban \
        redis-server \
        sqlite3 \
        jq \
        screen \
        tmux \
        > /dev/null 2>&1
    
    # Install snap packages
    echo -e "${Y}   → Installing LXD via snap...${NC}"
    snap install lxd > /dev/null 2>&1
    
    # Add user to lxd group
    usermod -aG lxd $SUDO_USER 2>/dev/null || usermod -aG lxd $USER
    
    echo -e "${G}✅ Dependencies installed!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔧  CONFIGURE LXD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

configure_lxd() {
    echo -e "${C}🔧 Configuring LXD container system...${NC}"
    
    # Initialize LXD with default settings
    echo -e "${Y}   → Initializing LXD...${NC}"
    cat <<EOF | lxd init --preseed
config:
  core.https_address: "[::]:8443"
  core.trust_password: ""
networks:
- config:
    ipv4.address: 10.10.10.1/24
    ipv4.nat: "true"
    ipv6.address: none
  description: ""
  name: lxdbr0
  type: bridge
  project: default
storage_pools:
- config:
    size: 20GB
  description: ""
  name: default
  driver: dir
profiles:
- config: {}
  description: Default LXD profile
  devices:
    eth0:
      name: eth0
      network: lxdbr0
      type: nic
    root:
      path: /
      pool: default
      type: disk
  name: default
projects: []
cluster: null
EOF
    
    # Create storage pool if not exists
    if ! lxc storage list | grep -q "default"; then
        lxc storage create default dir > /dev/null 2>&1
    fi
    
    echo -e "${G}✅ LXD configured!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🐍  SETUP PYTHON ENVIRONMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

setup_python() {
    echo -e "${C}🐍 Setting up Python environment...${NC}"
    
    # Create installation directory
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Create virtual environment
    echo -e "${Y}   → Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    echo -e "${Y}   → Upgrading pip...${NC}"
    pip install --upgrade pip > /dev/null 2>&1
    
    # Install Python packages
    echo -e "${Y}   → Installing Python packages...${NC}"
    pip install \
        discord.py \
        aiohttp \
        python-dotenv \
        requests \
        psutil \
        > /dev/null 2>&1
    
    # Create requirements.txt
    cat > requirements.txt << EOF
discord.py>=2.3.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
requests>=2.31.0
psutil>=5.9.0
EOF
    
    echo -e "${G}✅ Python environment ready!${NC}"
    sleep 1
}
