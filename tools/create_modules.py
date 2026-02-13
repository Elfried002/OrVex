#!/usr/bin/env python3
"""
Création automatique de tous les dossiers/fichiers modules
Exécutez ce script pour initialiser la structure complète
"""

import os
from pathlib import Path

def create_file(path, content=""):
    """Crée un fichier avec contenu par défaut"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Créé: {path}")

def main():
    """Crée toute la structure des modules"""
    
    print("🚀 Création de la structure des modules OrVex...\n")
    
    # 1. modules/__init__.py
    create_file("modules/__init__.py", 
        '"""OrVex Modules Package"""\n\n__all__ = ["evasion", "payloads", "steganography"]\n')
    
    # 2. modules/evasion/
    create_file("modules/evasion/__init__.py",
        '"""OrVex Evasion Module"""\n\nfrom .syscalls import SyscallManager\n__all__ = ["SyscallManager"]\n')
    create_file("modules/evasion/process_hollowing.py", '# Process Hollowing implementation\n')
    create_file("modules/evasion/dll_sideloading.py", '# DLL Sideloading implementation\n')
    create_file("modules/evasion/sandbox_detection.py", '# Sandbox detection\n')
    create_file("modules/evasion/obfuscation.py", '# Code obfuscation\n')
    
    # 3. modules/payloads/
    create_file("modules/payloads/__init__.py",
        '"""OrVex Payloads Module"""\n\n__all__ = ["windows", "linux", "macos", "android"]\n')
    
    # Windows
    create_file("modules/payloads/windows/__init__.py",
        '"""Windows Payloads"""\n\nfrom .x64_payloads import WindowsX64Payloads\nfrom .x86_payloads import WindowsX86Payloads\n__all__ = ["WindowsX64Payloads", "WindowsX86Payloads"]\n')
    create_file("modules/payloads/windows/x64_payloads.py", '# Windows x64 payloads\n')
    create_file("modules/payloads/windows/x86_payloads.py", '# Windows x86 payloads\n')
    
    # Linux
    create_file("modules/payloads/linux/__init__.py", '"""Linux Payloads"""\n')
    create_file("modules/payloads/linux/elf_payloads.py", '# Linux ELF payloads\n')
    
    # macOS
    create_file("modules/payloads/macos/__init__.py", '"""macOS Payloads"""\n')
    create_file("modules/payloads/macos/macho_payloads.py", '# macOS Mach-O payloads\n')
    
    # Android
    create_file("modules/payloads/android/__init__.py", '"""Android Payloads"""\n')
    create_file("modules/payloads/android/apk_payloads.py", '# Android APK payloads\n')
    
    # 4. modules/steganography/
    create_file("modules/steganography/__init__.py",
        '"""OrVex Steganography Module"""\n\nfrom .image_steg import ImageSteganography\n__all__ = ["ImageSteganography"]\n')
    create_file("modules/steganography/audio_steg.py", '# Audio steganography (LSB, Echo, Phase)\n')
    create_file("modules/steganography/text_steg.py", '# Text steganography (Zero-width, Whitespace)\n')
    create_file("modules/steganography/network_steg.py", '# Network steganography (DNS, ICMP, HTTP)\n')
    create_file("modules/steganography/polyglot.py", '# Polyglot files (PNG+ZIP, JPG+EXE, PDF+EXE)\n')
    
    print("\n" + "="*50)
    print("🎯 STRUCTURE COMPLÈTE CRÉÉE !")
    print("="*50)
    print("\n📁 Votre dossier modules/ contient maintenant:")
    
    for root, dirs, files in os.walk("modules"):
        level = root.replace("modules", "").count(os.sep)
        indent = "  " * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        for file in files[:3]:  # Affiche max 3 fichiers par dossier
            print(f"{indent}  📄 {file}")
        if len(files) > 3:
            print(f"{indent}  ... et {len(files)-3} autres fichiers")
    
    print("\n✅ Vous pouvez maintenant commencer à remplir ces fichiers !")
    print("🚀 Prochaine étape: implémenter les fonctionnalités de stéganographie")

if __name__ == "__main__":
    main()