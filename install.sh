#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                 SVM5-BOT - Installation Script (Commands Only)                ║
# ║                         Made by Ankit-Dev with ❤️                             ║
# ║              This script ONLY installs dependencies - No Bot Code             ║
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📍  PATH CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALL_DIR="/opt/svm5-bot"
LOG_FILE="/var/log/svm5-install.log"

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
    echo -e "${G}║              🚀 INSTALLATION SCRIPT - COMMANDS ONLY 🚀                        ║${NC}"
    echo -e "${C}║              This script ONLY installs dependencies                          ║${NC}"
    echo -e "${P}║              You must manually add your v5.py file                           ║${NC}"
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
    echo -e "${W}│  This software requires a valid license key to install.         │${NC}"
    echo -e "${W}│  Valid keys: Buy Now License Key        │${NC}"
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
    if [[ "$KEY" == "AnkitDev99\$@" ]] || [[ "$KEY" == "SVM5-PRO-2025" ]] || [[ "$KEY" == "SVM5-ENTERPRISE" ]] || [[ "$KEY" == "DEVELOPER-ANKIT" ]]; then
        echo -e "${G}✅ License Verified! Access Granted.${NC}"
        
        # Create install directory and save license
        mkdir -p "$INSTALL_DIR"
        echo "$KEY" > "$INSTALL_DIR/license.key"
        chmod 600 "$INSTALL_DIR/license.key"
        
        sleep 2
        return 0
    else
        echo -e "${R}❌ Invalid License Key! Access Denied.${NC}"
        echo -e "${Y}Debug: Entered key: $KEY${NC}"
        echo ""
        echo -e "${C}💡 To purchase a license, contact Ankit-Dev or send payment to:${NC}"
        echo -e "${W}   UPI: 9892642904@ybl${NC}"
        echo -e "${W}   Amount: ₹499 (One-time payment)${NC}"
        echo -e "${W}   Send screenshot to @Ankit-Dev on Discord${NC}"
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
    
    # Check disk space (need at least 5GB)
    AVAILABLE_SPACE=$(df / | awk 'NR==2 {print $4}')
    if [ $AVAILABLE_SPACE -lt 5242880 ]; then
        echo -e "${Y}⚠️  Low disk space: $(($AVAILABLE_SPACE/1024/1024))GB available${NC}"
        echo -e "${Y}   Recommended: At least 5GB free space${NC}"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo -e "${G}✅ Disk space: $(($AVAILABLE_SPACE/1024/1024))GB available${NC}"
    fi
    
    # Check memory (need at least 1GB)
    TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
    if [ $TOTAL_RAM -lt 1024 ]; then
        echo -e "${Y}⚠️  Low memory: ${TOTAL_RAM}MB${NC}"
        echo -e "${Y}   Recommended: At least 1GB RAM${NC}"
    else
        echo -e "${G}✅ Memory: ${TOTAL_RAM}MB${NC}"
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
        build-essential \
        > /dev/null 2>&1
    
    echo -e "${G}   ✅ Core packages installed${NC}"
    
    # Install snap packages
    echo -e "${Y}   → Installing LXD via snap...${NC}"
    snap install lxd > /dev/null 2>&1
    echo -e "${G}   ✅ LXD installed${NC}"
    
    # Add user to lxd group
    usermod -aG lxd $SUDO_USER 2>/dev/null || usermod -aG lxd $USER
    echo -e "${G}   ✅ User added to lxd group${NC}"
    
    echo -e "${G}✅ All dependencies installed successfully!${NC}"
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
    
    echo -e "${G}✅ LXD configured successfully!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🐍  INSTALL PYTHON PACKAGES (GLOBALLY)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

install_python_packages() {
    echo -e "${C}🐍 Installing Python packages globally...${NC}"
    
    # Upgrade pip
    echo -e "${Y}   → Upgrading pip...${NC}"
    pip3 install --upgrade pip > /dev/null 2>&1
    
    # Install Python packages globally
    echo -e "${Y}   → Installing discord.py and dependencies...${NC}"
    pip3 install \
        discord.py \
        aiohttp \
        python-dotenv \
        requests \
        psutil \
        > /dev/null 2>&1
    
    echo -e "${G}✅ Python packages installed globally!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔥  CONFIGURE FIREWALL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

configure_firewall() {
    echo -e "${C}🔥 Configuring firewall...${NC}"
    
    # Allow SSH
    ufw allow 22/tcp > /dev/null 2>&1
    echo -e "${Y}   → SSH port 22 allowed${NC}"
    
    # Allow port forwarding range
    ufw allow 20000:50000/tcp > /dev/null 2>&1
    ufw allow 20000:50000/udp > /dev/null 2>&1
    echo -e "${Y}   → Port range 20000-50000 allowed (TCP/UDP)${NC}"
    
    # Enable firewall if not enabled
    ufw --force enable > /dev/null 2>&1
    echo -e "${Y}   → Firewall enabled${NC}"
    
    echo -e "${G}✅ Firewall configured!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📁  CREATE DIRECTORY STRUCTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

create_directories() {
    echo -e "${C}📁 Creating directory structure...${NC}"
    
    # Create main directory
    mkdir -p "$INSTALL_DIR"
    echo -e "${Y}   → Created $INSTALL_DIR${NC}"
    
    # Create logs directory
    mkdir -p "$INSTALL_DIR/logs"
    echo -e "${Y}   → Created $INSTALL_DIR/logs${NC}"
    
    # Create database directory
    mkdir -p "$INSTALL_DIR/data"
    echo -e "${Y}   → Created $INSTALL_DIR/data${NC}"
    
    # Set permissions
    chmod 755 "$INSTALL_DIR"
    
    echo -e "${G}✅ Directory structure created!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📋  CREATE REQUIREMENTS FILE (Optional)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

create_requirements() {
    echo -e "${C}📋 Creating requirements.txt file (optional)...${NC}"
    
    cat > "$INSTALL_DIR/requirements.txt" << EOF
discord.py>=2.3.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
requests>=2.31.0
psutil>=5.9.0
EOF
    
    echo -e "${G}✅ requirements.txt created at $INSTALL_DIR/requirements.txt${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📋  SHOW COMPLETION MESSAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_completion() {
    echo -e "${G}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${G}║              ✅ INSTALLATION COMPLETE ✅                        ║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}║${NC}  📍 Installation Directory: $INSTALL_DIR                   ${G}║${NC}"
    echo -e "${G}║${NC}  📋 Requirements File: $INSTALL_DIR/requirements.txt       ${G}║${NC}"
    echo -e "${G}║${NC}  📊 Database Location: $INSTALL_DIR/data/                  ${G}║${NC}"
    echo -e "${G}║${NC}  📝 Logs Location: $INSTALL_DIR/logs/                      ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}              📋 NEXT STEPS                                  ${G}║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}║${NC}  1. Copy your v5.py file to:                                ${G}║${NC}"
    echo -e "${G}║${NC}     $INSTALL_DIR/v5.py                   ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}║${NC}  2. Make it executable:                                     ${G}║${NC}"
    echo -e "${G}║${NC}     chmod +x $INSTALL_DIR/v5.py          ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}║${NC}  3. Install Python packages (if not already):               ${G}║${NC}"
    echo -e "${G}║${NC}     pip3 install -r $INSTALL_DIR/requirements.txt           ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}║${NC}  4. Run the bot manually to test:                           ${G}║${NC}"
    echo -e "${G}║${NC}     python3 $INSTALL_DIR/v5.py                            ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}║${NC}  5. (Optional) Create systemd service for auto-start:       ${G}║${NC}"
    echo -e "${G}║${NC}     See documentation for service file                      ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}              🔐 LICENSE INFORMATION                         ${G}║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}  License Key: $(cat $INSTALL_DIR/license.key)                      ${G}║${NC}"
    echo -e "${G}║${NC}  Valid Keys: AnkitDev99\$@, SVM5-PRO-2025                    ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}              📞 SUPPORT                                     ${G}║${NC}"
    echo -e "${G}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║${NC}  Developer: Ankit-Dev                                       ${G}║${NC}"
    echo -e "${G}║${NC}  UPI: 9892642904@ybl                                        ${G}║${NC}"
    echo -e "${G}║${NC}  Discord: @Ankit-Dev                                        ${G}║${NC}"
    echo -e "${G}║${NC}  GitHub: https://github.com/AnkitKing7/Svm5-bot             ${G}║${NC}"
    echo -e "${G}║${NC}                                                              ${G}║${NC}"
    echo -e "${G}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${G}🎉 System dependencies installed successfully! 🎉${NC}"
    echo -e "${Y}📌 Remember to copy your v5.py file to: $INSTALL_DIR/svm5.py${NC}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎯  MAIN INSTALLATION FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

main() {
    show_header
    check_license
    check_system
    install_dependencies
    configure_lxd
    install_python_packages
    configure_firewall
    create_directories
    create_requirements
    show_completion
}

# Run main function
main
