#!/usr/bin/env python3
"""
OrVex Banner - Style Metasploit v3 (ASCII only)
Version: 2.1.0
"""

import os
import sys
import platform
import subprocess
import socket
import shutil
import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

class OrVexUI:
    """Interface utilisateur style Metasploit v3 - ASCII only"""
    
    # ========== BANNIÈRE STYLE METASPLOIT V3 ==========
    BANNER = f"""
{Fore.RED}
                 ______
                / ____/___  ______ ___  ___  ____
               / /   / __ \\/ ___/ __ \\/ _ \\/ __ \\
              / /___/ /_/ (__  ) /_/ /  __/ / / /
              \\____/\\____/____/ .___/\\___/_/ /_/
                              /_/
{Style.RESET_ALL}
{Fore.CYAN}
       =[ OrVex v2.1.0 ]
+ -- --=[ 35 modules | 4 platforms | 8 stego techniques ]=--
+ -- --=[ https://github.com/Elfried002/OrVex ]=--

{Fore.GREEN}
               --=[ Advanced Exploitation Framework ]=--
{Style.RESET_ALL}
"""

    # ========== WARNING MESSAGE ==========
    WARNING = f"""
{Fore.RED}================================================================================
            ⚠️ WARNING ! WARNING ! WARNING ! WARNING ! WARNING ! ⚠️
================================================================================

  * Upload your payloads to:
    {Fore.CYAN}https://www.nodistribute.com{Fore.RED}

  * {Fore.YELLOW}DO NOT upload to:{Fore.RED}
    {Fore.CYAN}https://www.virustotal.com{Fore.RED}
    {Fore.CYAN}https://www.hybrid-analysis.com{Fore.RED}

  * Legitimate services only:
    {Fore.CYAN}https://antiscan.me{Fore.RED}

================================================================================{Style.RESET_ALL}
"""

    # ========== MENU PRINCIPAL ==========
    MENU = f"""
{Fore.CYAN}================================================================================
{Fore.WHITE}                                 MAIN MENU
{Fore.CYAN}================================================================================{Style.RESET_ALL}

{Fore.RED}   💣 PAYLOAD GENERATION{Style.RESET_ALL}
{Fore.GREEN}   [01]{Fore.WHITE} Create Backdoor with msfvenom
{Fore.GREEN}   [02]{Fore.WHITE} Create FUD 100% Backdoor
{Fore.GREEN}   [03]{Fore.WHITE} Direct Syscalls (Hell's Gate)
{Fore.GREEN}   [04]{Fore.WHITE} Backdoor Factory
{Fore.GREEN}   [05]{Fore.WHITE} Backdooring Original APK
{Fore.GREEN}   [06]{Fore.WHITE} Create Debian Package (Trodebi)
{Fore.GREEN}   [07]{Fore.WHITE} Create Backdoor For Office

{Fore.RED}   🖼️  STEGANOGRAPHY – IMAGE{Style.RESET_ALL}
{Fore.GREEN}   [08]{Fore.WHITE} LSB Hide in PNG
{Fore.GREEN}   [09]{Fore.WHITE} LSB Extract from PNG
{Fore.GREEN}   [10]{Fore.WHITE} Bit Plane Hide
{Fore.GREEN}   [11]{Fore.WHITE} Bit Plane Extract
{Fore.GREEN}   [12]{Fore.WHITE} DCT Hide (JPG)

{Fore.RED}   🔊 STEGANOGRAPHY – AUDIO{Style.RESET_ALL}
{Fore.GREEN}   [13]{Fore.WHITE} Audio LSB Hide
{Fore.GREEN}   [14]{Fore.WHITE} Audio LSB Extract
{Fore.GREEN}   [15]{Fore.WHITE} Echo Hiding Hide
{Fore.GREEN}   [16]{Fore.WHITE} Echo Hiding Extract

{Fore.RED}   📝 STEGANOGRAPHY – TEXT{Style.RESET_ALL}
{Fore.GREEN}   [17]{Fore.WHITE} Zero-Width Characters Hide
{Fore.GREEN}   [18]{Fore.WHITE} Zero-Width Characters Extract
{Fore.GREEN}   [19]{Fore.WHITE} Whitespace Encoding

{Fore.RED}   🌐 STEGANOGRAPHY – NETWORK{Style.RESET_ALL}
{Fore.GREEN}   [20]{Fore.WHITE} DNS Covert Channel Send
{Fore.GREEN}   [21]{Fore.WHITE} DNS Covert Server
{Fore.GREEN}   [22]{Fore.WHITE} ICMP Covert Channel

{Fore.RED}   🧬 POLYGLOT FILES{Style.RESET_ALL}
{Fore.GREEN}   [23]{Fore.WHITE} PNG+ZIP Polyglot
{Fore.GREEN}   [24]{Fore.WHITE} JPG+EXE Polyglot
{Fore.GREEN}   [25]{Fore.WHITE} PDF+EXE Polyglot

{Fore.RED}   🛠️  TOOLS & UTILITIES{Style.RESET_ALL}
{Fore.GREEN}   [26]{Fore.WHITE} Load/Create auto listeners
{Fore.GREEN}   [27]{Fore.WHITE} Jump to msfconsole
{Fore.GREEN}   [28]{Fore.WHITE} Searchsploit
{Fore.GREEN}   [29]{Fore.WHITE} File Pumper
{Fore.GREEN}   [30]{Fore.WHITE} Configure Default Settings
{Fore.GREEN}   [31]{Fore.WHITE} Cleanup
{Fore.GREEN}   [32]{Fore.WHITE} Help
{Fore.GREEN}   [33]{Fore.WHITE} Credits
{Fore.GREEN}   [34]{Fore.WHITE} Exit

{Fore.CYAN}================================================================================{Style.RESET_ALL}
"""

    # ========== CREDITS ==========
    CREDITS = f"""
{Fore.CYAN}================================================================================
{Fore.WHITE}                                   CREDITS
{Fore.CYAN}================================================================================{Style.RESET_ALL}

{Fore.RED}                 ______
                / ____/___  ______ ___  ___  ____
               / /   / __ \\/ ___/ __ \\/ _ \\/ __ \\
              / /___/ /_/ (__  ) /_/ /  __/ / / /
              \\____/\\____/____/ .___/\\___/_/ /_/
                              /_/
{Style.RESET_ALL}

{Fore.WHITE}  Version  : 2.1.0
  Author    : 3lfr13d (Elfried)
  GitHub    : @Elfried002
  Based on  : TheFatRat by Screetsec

{Fore.RED}  Special Thanks:{Style.RESET_ALL}
    * Screetsec (TheFatRat)
    * Dracos Linux Community
    * Offensive Security
    * All contributors

{Fore.CYAN}  "The quieter you become, the more you are able to hear."
{Fore.WHITE}                        - Kali Linux

{Fore.CYAN}  Site Web : https://elfried-yobouet.siteviral.com

{Fore.CYAN}================================================================================{Style.RESET_ALL}
"""

    @staticmethod
    def clear_screen():
        """Nettoie l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def press_enter():
        """Attend que l'utilisateur appuie sur Entrée"""
        input(f"\n{Fore.YELLOW}➡️  Press Enter to continue...{Style.RESET_ALL}")
    
    @staticmethod
    def show_banner():
        """Affiche la bannière"""
        OrVexUI.clear_screen()
        print(OrVexUI.BANNER)
    
    @staticmethod
    def show_warning():
        """Affiche l'avertissement"""
        OrVexUI.clear_screen()
        print(OrVexUI.BANNER)
        print(OrVexUI.WARNING)
        OrVexUI.press_enter()
    
    @staticmethod
    def show_menu():
        """Affiche le menu principal"""
        OrVexUI.clear_screen()
        print(OrVexUI.BANNER)
        print(OrVexUI.MENU)
    
    @staticmethod
    def show_credits():
        """Affiche les crédits"""
        OrVexUI.clear_screen()
        print(OrVexUI.CREDITS)
        OrVexUI.press_enter()
    
    @staticmethod
    def get_terminal_size():
        """Retourne la taille du terminal"""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80
    
    @staticmethod
    def print_centered(text, color=Fore.WHITE):
        """Affiche un texte centré"""
        width = OrVexUI.get_terminal_size()
        print(color + text.center(width) + Style.RESET_ALL)
    
    @staticmethod
    def get_system_info():
        """Affiche les informations système"""
        width = OrVexUI.get_terminal_size()
        
        print(f"\n{Fore.CYAN}{'=' * width}{Style.RESET_ALL}")
        OrVexUI.print_centered("SYSTEM INFORMATION", Fore.WHITE)
        print(f"{Fore.CYAN}{'=' * width}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}  OS        : {platform.system()} {platform.release()}")
        print(f"{Fore.WHITE}  Hostname  : {platform.node()}")
        print(f"{Fore.WHITE}  Arch      : {platform.machine()}")
        print(f"{Fore.WHITE}  Python    : {sys.version.split()[0]}")
        
        # Vérifier root
        try:
            if os.geteuid() == 0:
                print(f"{Fore.WHITE}  Privileges: {Fore.GREEN}ROOT")
            else:
                print(f"{Fore.WHITE}  Privileges: {Fore.YELLOW}User")
        except:
            print(f"{Fore.WHITE}  Privileges: {Fore.YELLOW}Windows Mode")
        
        # Vérifier connexion internet
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            print(f"{Fore.WHITE}  Internet  : {Fore.GREEN}Connected")
        except:
            print(f"{Fore.WHITE}  Internet  : {Fore.RED}Offline")
        
        print(f"\n{Fore.CYAN}{'=' * width}{Style.RESET_ALL}")
        return True
    
    @staticmethod
    def print_success(msg):
        """Affiche un message de succès"""
        print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(msg):
        """Affiche un message d'erreur"""
        print(f"{Fore.RED}[-] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(msg):
        """Affiche un message d'information"""
        print(f"{Fore.CYAN}[*] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(msg):
        """Affiche un avertissement"""
        print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def progress_bar(current, total, bar_length=40):
        """Affiche une barre de progression"""
        percent = float(current) * 100 / total
        arrow = '#' * int(percent/100 * bar_length)
        spaces = ' ' * (bar_length - len(arrow))
        print(f"\r{Fore.CYAN}[{arrow}{spaces}] {percent:.1f}%{Style.RESET_ALL}", end='')