#!/bin/bash
#
# OrVex Framework Installer v2.1.0
# For Kali Linux and Parrot OS only
# Style: Metasploit v3 - ASCII only
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Version
VERSION="2.1.0"

# Installation directory
INSTALL_DIR="/opt/orvex"
VENV_DIR="$INSTALL_DIR/venv"

# Fonction d'affichage du banner style Metasploit v3
print_banner() {
    echo -e "${RED}"
    echo "                 ______"
    echo "                / ____/___  ______ ___  ___  ____"
    echo "               / /   / __ \\/ ___/ __ \\/ _ \\/ __ \\"
    echo "              / /___/ /_/ (__  ) /_/ /  __/ / / /"
    echo "              \\____/\\____/____/ .___/\\___/_/ /_/"
    echo "                              /_/"
    echo -e "${NC}"
    echo -e "${CYAN}       =[ OrVex v$VERSION ]=${NC}"
    echo -e "${CYAN}+ -- --=[ 35 modules | 4 platforms | 8 stego techniques ]=--${NC}"
    echo -e "${CYAN}+ -- --=[ https://github.com/Elfried002/OrVex ]=--${NC}"
    echo ""
    echo -e "${GREEN}       --=[ Advanced Exploitation Framework ]=--${NC}"
    echo ""
}

# Fonction de vérification root
check_root() {
    if [ "$EUID" -ne 0 ]; then 
        echo -e "${RED}[-] This script must be run as root!${NC}"
        echo -e "${YELLOW}[*] Please run: sudo ./setup.sh${NC}"
        exit 1
    fi
    echo -e "${GREEN}[+] Running as root${NC}"
}

# Fonction de détection OS (Kali/Parrot uniquement)
detect_os() {
    echo -e "\n${BLUE}[*] Detecting operating system...${NC}"
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        echo -e "${GREEN}[+] Detected: $OS $VER${NC}"
        
        # Vérifier compatibilité (Kali ou Parrot uniquement)
        if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Parrot"* ]]; then
            echo -e "${GREEN}[+] Compatible distribution: $OS${NC}"
        else
            echo -e "${RED}[-] This installer is for Kali Linux and Parrot OS only!${NC}"
            echo -e "${YELLOW}[!] Detected: $OS${NC}"
            echo -e "${YELLOW}[!] Please use the manual installation method for other distributions.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}[-] Cannot detect OS${NC}"
        exit 1
    fi
}

# Fonction d'installation des dépendances système
install_system_deps() {
    echo -e "\n${BLUE}[*] Installing system dependencies...${NC}"
    
    # Mise à jour des dépôts
    echo -e "${YELLOW}[*] Updating package lists...${NC}"
    apt-get update -qq
    
    # Liste des paquets nécessaires (optimisée pour Kali/Parrot)
    PACKAGES=(
        # Python et outils de base
        python3
        python3-pip
        python3-venv
        python3-dev
        python3-setuptools
        python3-full
        
        # Compilation et développement
        build-essential
        gcc
        g++
        make
        cmake
        
        # Cross-compilation Windows
        mingw-w64
        mingw-w64-tools
        
        # Go pour macOS
        golang
        
        # Metasploit
        metasploit-framework
        
        # Android
        apktool
        zipalign
        default-jdk
        default-jre
        
        # Outils d'exploitation
        backdoor-factory
        exploitdb
        
        # Stéganographie et multimédia
        imagemagick
        ffmpeg
        libavcodec-extra
        sox
        libsox-fmt-all
        
        # Réseau
        dnsutils
        net-tools
        tcpdump
        nmap
        wireshark-common
        
        # Utilitaires
        xterm
        upx-ucl
        git
        wget
        curl
        unzip
        zip
        
        # Documentation
        man-db
        manpages-dev
    )
    
    # Installation
    echo -e "${YELLOW}[*] Installing packages (this may take a while)...${NC}"
    for pkg in "${PACKAGES[@]}"; do
        echo -ne "  Installing $pkg... \r"
        apt-get install -y "$pkg" &>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}[+] $pkg installed${NC}"
        else
            echo -e "  ${YELLOW}[!] $pkg failed (optional)${NC}"
        fi
    done
    
    echo -e "${GREEN}[+] System dependencies installed${NC}"
}

# Fonction d'installation des dépendances Python (avec venv pour Kali)
install_python_deps() {
    echo -e "\n${BLUE}[*] Installing Python dependencies in virtual environment...${NC}"
    
    # Créer le dossier d'installation
    mkdir -p $INSTALL_DIR
    
    # Copier les fichiers nécessaires
    echo -e "${YELLOW}[*] Copying files to $INSTALL_DIR...${NC}"
    cp -r . $INSTALL_DIR/ 2>/dev/null
    
    # Créer l'environnement virtuel
    echo -e "${YELLOW}[*] Creating Python virtual environment...${NC}"
    cd $INSTALL_DIR
    python3 -m venv venv
    
    # Activer l'environnement virtuel
    source venv/bin/activate
    
    # Mise à jour de pip dans le venv
    echo -e "${YELLOW}[*] Upgrading pip...${NC}"
    pip install --upgrade pip
    
    # Installation des dépendances depuis requirements.txt
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}[*] Installing packages from requirements.txt...${NC}"
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[+] Python packages installed successfully in virtual environment${NC}"
        else
            echo -e "${RED}[-] Some packages failed to install${NC}"
            echo -e "${YELLOW}[*] Attempting to install critical packages individually...${NC}"
            
            # Installation individuelle des packages critiques
            pip install colorama pyyaml requests cryptography jinja2
            pip install pillow numpy pycryptodome
            pip install opencv-python scapy dnspython pydub
        fi
    else
        echo -e "${RED}[-] requirements.txt not found${NC}"
        exit 1
    fi
    
    # Vérification des imports critiques
    echo -e "\n${YELLOW}[*] Verifying Python imports...${NC}"
    python -c "
import sys
modules = ['colorama', 'yaml', 'requests', 'cryptography', 'jinja2', 
           'PIL', 'numpy', 'Crypto', 'cv2', 'scapy', 'dns', 'pydub']
missing = []
for m in modules:
    try:
        __import__(m)
        print(f'  [+] {m}')
    except ImportError:
        missing.append(m)
        print(f'  [-] {m}')
if missing:
    print(f'\\n[!] Missing: {missing}')
    sys.exit(1)
"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[+] All Python imports successful${NC}"
    else
        echo -e "${RED}[-] Some imports failed. You may need to install them manually:${NC}"
        echo -e "${YELLOW}    source $VENV_DIR/bin/activate && pip install [package]${NC}"
    fi
    
    # Désactiver l'environnement virtuel
    deactivate
}

# Fonction de création des dossiers
create_directories() {
    echo -e "\n${BLUE}[*] Creating directory structure...${NC}"
    
    DIRS=(
        "$INSTALL_DIR"
        "$INSTALL_DIR/core"
        "$INSTALL_DIR/modules"
        "$INSTALL_DIR/tools"
        "$INSTALL_DIR/loaders"
        "$INSTALL_DIR/templates"
        "/var/lib/orvex"
        "/var/lib/orvex/output"
        "/var/lib/orvex/output/payloads"
        "/var/lib/orvex/output/listeners"
        "/var/lib/orvex/output/stego"
        "/var/lib/orvex/logs"
        "/var/lib/orvex/tmp"
        "/etc/orvex"
        "/etc/orvex/profiles"
    )
    
    for dir in "${DIRS[@]}"; do
        mkdir -p "$dir"
        echo -e "  ${GREEN}[+] Created: $dir${NC}"
    done
    
    # Dossier utilisateur
    for user_home in /home/*; do
        if [ -d "$user_home" ]; then
            mkdir -p "$user_home/.orvex"
            mkdir -p "$user_home/.orvex/output"
            mkdir -p "$user_home/.orvex/logs"
            echo -e "  ${GREEN}[+] Created: $user_home/.orvex${NC}"
            chown -R $(basename $user_home):$(basename $user_home) "$user_home/.orvex" 2>/dev/null
        fi
    done
    
    # Dossier root
    mkdir -p /root/.orvex
    mkdir -p /root/.orvex/output
    
    echo -e "${GREEN}[+] Directory structure created${NC}"
}

# Fonction de copie des fichiers
copy_files() {
    echo -e "\n${BLUE}[*] Copying OrVex files to $INSTALL_DIR...${NC}"
    
    # Les fichiers sont déjà copiés dans install_python_deps
    
    # Configuration par défaut
    if [ -f "core/config.yaml" ]; then
        cp core/config.yaml /etc/orvex/config.yaml
    else
        # Créer une config par défaut
        cat > /etc/orvex/config.yaml << 'EOF'
# OrVex Global Configuration
version: 2.1.0
general:
  debug: false
  log_level: INFO
  workspace: /var/lib/orvex/output
network:
  default_lhost: 192.168.1.100
  default_lport: 4444
paths:
  msfvenom: /usr/bin/msfvenom
  mingw: /usr/bin/x86_64-w64-mingw32-gcc
  go: /usr/bin/go
  apktool: /usr/bin/apktool
EOF
    fi
    echo -e "  ${GREEN}[+] Configuration copied to /etc/orvex/config.yaml${NC}"
    
    echo -e "${GREEN}[+] All files copied successfully${NC}"
}

# Fonction de création de la commande système
create_system_command() {
    echo -e "\n${BLUE}[*] Creating system command 'orvex'...${NC}"
    
    cat > /usr/local/bin/orvex << EOF
#!/bin/bash
# OrVex system command wrapper for Kali/Parrot

# Activer l'environnement virtuel
source $VENV_DIR/bin/activate

# Lancer OrVex
cd $INSTALL_DIR
python3 orvex.py "\$@"

# Désactiver l'environnement virtuel
deactivate 2>/dev/null
EOF
    
    chmod +x /usr/local/bin/orvex
    echo -e "${GREEN}[+] Command created: /usr/local/bin/orvex${NC}"
}

# Fonction de configuration des permissions
set_permissions() {
    echo -e "\n${BLUE}[*] Setting permissions...${NC}"
    
    # Exécutables
    chmod -R 755 $INSTALL_DIR
    chmod 755 /usr/local/bin/orvex
    
    # Dossiers de travail
    chmod -R 777 /var/lib/orvex/output
    chmod -R 777 /var/lib/orvex/tmp
    
    # Configuration
    chmod -R 644 /etc/orvex/*.yaml
    chmod 755 /etc/orvex
    chmod 755 /etc/orvex/profiles
    
    echo -e "${GREEN}[+] Permissions set${NC}"
}

# Fonction de création des alias shell
create_shell_aliases() {
    echo -e "\n${BLUE}[*] Creating shell aliases...${NC}"
    
    ALIAS_FILE="/etc/bash.bashrc"
    
    # Vérifier si les alias existent déjà
    if ! grep -q "# OrVex Framework Aliases" "$ALIAS_FILE"; then
        cat >> "$ALIAS_FILE" << 'EOF'

# OrVex Framework Aliases
alias orvex='sudo /usr/local/bin/orvex'
alias orvex-update='cd /opt/orvex && sudo git pull && sudo source venv/bin/activate && sudo pip install -r requirements.txt'
alias orvex-config='sudo nano /etc/orvex/config.yaml'
alias orvex-listeners='ls -la /var/lib/orvex/output/listeners/'
alias orvex-payloads='ls -la /var/lib/orvex/output/payloads/'
alias orvex-stego='ls -la /var/lib/orvex/output/stego/'
alias orvex-clean='sudo rm -rf /var/lib/orvex/output/* && sudo rm -rf /tmp/orvex/*'
alias orvex-logs='sudo tail -f /var/lib/orvex/logs/orvex.log'
EOF
        echo -e "${GREEN}[+] Aliases added to $ALIAS_FILE${NC}"
    else
        echo -e "${YELLOW}[*] Aliases already exist${NC}"
    fi
    
    # Aliases pour ZSH si présent
    if [ -f "/etc/zsh/zshrc" ]; then
        if ! grep -q "# OrVex Framework Aliases" "/etc/zsh/zshrc"; then
            cat >> "/etc/zsh/zshrc" << 'EOF'

# OrVex Framework Aliases
alias orvex='sudo /usr/local/bin/orvex'
alias orvex-update='cd /opt/orvex && sudo git pull && sudo source venv/bin/activate && sudo pip install -r requirements.txt'
alias orvex-config='sudo nano /etc/orvex/config.yaml'
alias orvex-listeners='ls -la /var/lib/orvex/output/listeners/'
alias orvex-payloads='ls -la /var/lib/orvex/output/payloads/'
alias orvex-stego='ls -la /var/lib/orvex/output/stego/'
alias orvex-clean='sudo rm -rf /var/lib/orvex/output/* && sudo rm -rf /tmp/orvex/*'
alias orvex-logs='sudo tail -f /var/lib/orvex/logs/orvex.log'
EOF
            echo -e "${GREEN}[+] Aliases added to /etc/zsh/zshrc${NC}"
        fi
    fi
}

# Fonction de vérification finale
verify_installation() {
    echo -e "\n${BLUE}[*] Verifying installation...${NC}"
    
    # Vérifier la commande
    if command -v orvex &>/dev/null; then
        echo -e "${GREEN}[+] Command 'orvex' is available${NC}"
    else
        echo -e "${RED}[-] Command 'orvex' not found${NC}"
        return 1
    fi
    
    # Vérifier l'environnement virtuel
    if [ -f "$VENV_DIR/bin/activate" ]; then
        echo -e "${GREEN}[+] Virtual environment found at $VENV_DIR${NC}"
    else
        echo -e "${RED}[-] Virtual environment not found${NC}"
    fi
    
    # Vérifier les outils externes
    echo -e "${YELLOW}[*] Checking external tools...${NC}"
    TOOLS=("msfvenom" "x86_64-w64-mingw32-gcc" "go" "apktool")
    for tool in "${TOOLS[@]}"; do
        if command -v "$tool" &>/dev/null; then
            echo -e "  ${GREEN}[+] $tool found${NC}"
        else
            echo -e "  ${YELLOW}[!] $tool not found (optional)${NC}"
        fi
    done
    
    return 0
}

# Fonction d'affichage du résumé
show_summary() {
    echo -e "\n${CYAN}════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}                    OrVex Framework Installation Complete${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}  Version      :${WHITE} $VERSION"
    echo -e "${GREEN}  Installation :${WHITE} $INSTALL_DIR"
    echo -e "${GREEN}  Virtual env  :${WHITE} $VENV_DIR"
    echo -e "${GREEN}  Configuration :${WHITE} /etc/orvex/config.yaml"
    echo -e "${GREEN}  Output       :${WHITE} /var/lib/orvex/output/"
    echo -e "${GREEN}  Logs         :${WHITE} /var/lib/orvex/logs/"
    echo ""
    echo -e "${YELLOW}  Quick Start:${NC}"
    echo -e "    ${GREEN}[+]${WHITE} sudo orvex              - Launch interactive menu"
    echo -e "    ${GREEN}[+]${WHITE} orvex --help            - Show command line options"
    echo -e "    ${GREEN}[+]${WHITE} orvex generate ...       - Generate payload"
    echo -e "    ${GREEN}[+]${WHITE} orvex stego ...          - Steganography operations"
    echo -e "    ${GREEN}[+]${WHITE} orvex check              - Check dependencies"
    echo ""
    echo -e "${CYAN}  Documentation:${WHITE} https://github.com/Elfried002/OrVex/wiki"
    echo ""
    echo -e "${PURPLE}  \"The quieter you become, the more you are able to hear.\"${NC}"
    echo -e "${WHITE}                         - Kali Linux${NC}"
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════════════${NC}"
}

# Fonction principale
main() {
    print_banner
    check_root
    detect_os
    
    echo -e "\n${YELLOW}[!] This will install OrVex Framework v$VERSION on your system${NC}"
    echo -e "${YELLOW}[!] Installation directory: $INSTALL_DIR${NC}"
    echo -e "${YELLOW}[!] The following will be installed:${NC}"
    echo "    - System dependencies (compilers, tools, libraries)"
    echo "    - Python virtual environment with all packages"
    echo "    - OrVex core files in $INSTALL_DIR"
    echo "    - System command 'orvex' in /usr/local/bin/"
    echo "    - Configuration in /etc/orvex/"
    echo "    - Working directories in /var/lib/orvex/"
    echo ""
    read -p "Continue? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}[-] Installation cancelled${NC}"
        exit 1
    fi
    
    # Installation
    install_system_deps
    install_python_deps
    create_directories
    copy_files
    create_system_command
    set_permissions
    create_shell_aliases
    
    # Vérification
    verify_installation
    
    # Résumé
    show_summary
    
    echo -e "\n${GREEN}[+] Installation completed successfully!${NC}"
    echo -e "${YELLOW}[*] You may need to restart your terminal or run 'source /etc/bash.bashrc'${NC}"
    echo -e "${YELLOW}[*] To start OrVex, simply type: sudo orvex${NC}"
}

# Exécution
main "$@"