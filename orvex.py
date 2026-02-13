#!/usr/bin/env python3
"""
OrVex Framework - Advanced Exploitation Tool
Version: 1.9.0
Command: sudo orvex (Linux) | python orvex.py (Windows Dev)

Author: 3lfr13d
GitHub: @Elfried002
"""

import os
import sys
import platform
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

# Version
__version__ = '1.9.0'
__author__ = '3lfr13d'
__description__ = 'Advanced Exploitation Framework with EDR Evasion & Steganography'

class OrVexCLI:
    """Interface en ligne de commande pour OrVex"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_linux = self.system == 'linux'
        self.is_macos = self.system == 'darwin'
        
    def check_root(self, args) -> bool:
        """
        Vérifie si l'utilisateur a les privilèges nécessaires
        """
        if args.no_root_check:
            print("[*] Root check disabled (development mode)")
            return True
        
        if self.is_windows:
            return self._check_windows_admin()
        else:
            return self._check_linux_root()
    
    def _check_windows_admin(self) -> bool:
        """Vérifie les privilèges administrateur sous Windows"""
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print("[!] Warning: Not running as Administrator")
                print("[!] Some features may not work correctly")
                print("[*] For development, use: --no-root-check")
                print("")
                return False
            print("[✓] Running with Administrator privileges")
            return True
        except Exception as e:
            print(f"[!] Cannot verify admin rights: {e}")
            return False
    
    def _check_linux_root(self) -> bool:
        """Vérifie les privilèges root sous Linux"""
        try:
            if os.geteuid() != 0:
                print("[!] This tool must be run as root on Linux!")
                print("[!] Please use: sudo orvex")
                print("")
                print("[*] For development on Windows, use: python orvex.py --no-root-check")
                print("[*] For production on Kali/Parrot, use: sudo orvex")
                return False
            print("[✓] Running as root")
            return True
        except Exception as e:
            print(f"[!] Root check failed: {e}")
            return False
    
    def setup_environment(self, debug: bool = False) -> bool:
        """
        Configure l'environnement d'exécution
        """
        # Ajouter le chemin du projet au PYTHONPATH
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        # Créer les dossiers nécessaires
        dirs = [
            Path.home() / '.orvex',
            Path.home() / '.orvex/output',
            Path.home() / '.orvex/logs',
            Path.home() / '.orvex/templates',
            Path.cwd() / 'output',
            Path.cwd() / 'output/listeners',
            Path.cwd() / 'output/payloads',
            Path.cwd() / 'output/stego',
        ]
        
        for d in dirs:
            d.mkdir(exist_ok=True, parents=True)
        
        if debug:
            print(f"[*] Project root: {project_root}")
            print(f"[*] Python path: {sys.path}")
            print(f"[*] Directories created")
        
        return True
    
    def run_interactive(self, debug: bool = False):
        """
        Lance le mode interactif (menu)
        """
        try:
            from core.menu import OrVexMenu
            from core.banner import OrVexUI
            
            # Afficher les infos système
            if debug:
                OrVexUI.get_system_info()
            
            # Lancer le menu
            menu = OrVexMenu()
            menu.run()
            
        except ImportError as e:
            print(f"[!] Import error: {e}")
            print("[*] Make sure you're running from the OrVex directory")
            print("[*] Structure should be:")
            print("    OrVex/")
            print("    ├── orvex.py")
            print("    ├── core/")
            print("    │   ├── menu.py")
            print("    │   ├── banner.py")
            print("    │   ├── config.py")
            print("    │   └── engine.py")
            print("    └── modules/")
            if debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def generate_payload(self, args) -> bool:
        """
        Génère un payload en ligne de commande
        """
        try:
            from core.engine import get_engine
            
            engine = get_engine()
            
            # Parser les options d'évasion
            evasion = []
            if args.evasion:
                evasion = [e.strip() for e in args.evasion.split(',')]
            
            # Générer le payload
            success, message = engine.generate_payload(
                platform=args.platform,
                arch=args.arch,
                payload_type=args.type,
                lhost=args.lhost,
                lport=args.lport,
                evasion=evasion,
                encryption=args.encrypt,
                output=args.output,
                format=args.format
            )
            
            if success:
                print(f"\n[✓] Payload generated: {message}")
                
                # Générer un listener automatiquement
                if args.listener:
                    listener = engine.generate_listener(
                        lhost=args.lhost,
                        lport=args.lport,
                        payload_type=f"{args.platform}/{args.arch}/{args.type}"
                    )
                    print(f"[✓] Listener created: {listener}")
                
                return True
            else:
                print(f"\n[✗] Failed: {message}")
                return False
                
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def steganography(self, args) -> bool:
        """
        Opérations de stéganographie
        """
        try:
            from core.engine import get_engine
            
            engine = get_engine()
            
            if args.stego_action == 'hide':
                success = engine.create_stego_payload(
                    technique=args.technique,
                    carrier_path=args.carrier,
                    payload_path=args.payload,
                    output_path=args.output,
                    plane=args.plane,
                    quality=args.quality,
                    delay=args.delay,
                    decay=args.decay
                )
            elif args.stego_action == 'extract':
                success = engine.extract_stego_payload(
                    technique=args.technique,
                    carrier_path=args.carrier,
                    output_path=args.output,
                    plane=args.plane
                )
            else:
                print(f"[!] Unknown action: {args.stego_action}")
                return False
            
            if success:
                print(f"[✓] Steganography operation completed")
                return True
            else:
                print(f"[✗] Steganography operation failed")
                return False
                
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def check_dependencies(self, args) -> bool:
        """
        Vérifie les dépendances
        """
        try:
            from tools.check_deps import DependencyChecker
            
            checker = DependencyChecker()
            
            if args.fix:
                checker.fix_issues()
            else:
                results = checker.run_full_check()
                
                # Afficher le résumé
                python_ok = all(results.get('python_packages', {}).values())
                system_ok = all(results.get('system_packages', {}).values())
                tools_ok = all(results.get('tools', {}).values())
                
                print("\n" + "="*50)
                print("DEPENDENCY CHECK SUMMARY")
                print("="*50)
                print(f"Python Version: {'✓' if results.get('python_version') else '✗'}")
                print(f"Python Packages: {'✓' if python_ok else '✗'}")
                print(f"System Packages: {'✓' if system_ok else '✗'}")
                print(f"External Tools: {'✓' if tools_ok else '✗'}")
                print(f"Internet: {'✓' if results.get('internet') else '✗'}")
                print("="*50)
                
                if python_ok and system_ok and tools_ok:
                    print("[✓] All dependencies satisfied!")
                    return True
                else:
                    print("[!] Some dependencies missing. Run with --fix to install")
                    return False
                    
        except ImportError as e:
            print(f"[!] Dependency checker not available: {e}")
            return False
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def configure(self, args) -> bool:
        """
        Configure OrVex
        """
        try:
            from core.config import get_config
            
            config = get_config()
            
            if args.show:
                import yaml
                print(yaml.dump(config.config, default_flow_style=False))
                return True
            
            if args.set:
                key, value = args.set.split('=', 1)
                config.set(key.strip(), value.strip())
                print(f"[✓] Set {key} = {value}")
                return True
            
            if args.reset:
                config.reset()
                print("[✓] Configuration reset to defaults")
                return True
            
            if args.profile:
                if args.create:
                    config.create_profile(args.profile, args.base)
                else:
                    config.switch_profile(args.profile)
                return True
            
            # Afficher les valeurs par défaut
            print(f"Default LHOST: {config.get('network.default_lhost')}")
            print(f"Default LPORT: {config.get('network.default_lport')}")
            print(f"Profiles: {', '.join(config.list_profiles())}")
            print(f"Current profile: {config.profile}")
            
            return True
            
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

def main():
    """Point d'entrée principal"""
    
    cli = OrVexCLI()
    
    # Créer le parser principal
    parser = argparse.ArgumentParser(
        description=__description__,
        usage="""orvex <command> [options]

Commands:
  interactive              Launch interactive menu (default)
  generate                  Generate payload
  stego                     Steganography operations
  check                     Check dependencies
  config                    Configure OrVex
  version                   Show version
  help                      Show this help

Examples:
  sudo orvex                Launch interactive menu
  orvex generate --platform windows --type reverse_tcp --lhost 192.168.1.100 --lport 4444
  orvex stego hide --technique image_lsb --carrier image.png --payload payload.bin
  orvex check --fix
  orvex config --show
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-root-check', action='store_true', help='Skip root check (development)')
    
    # Sous-commandes
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Commande: version
    parser_version = subparsers.add_parser('version', help='Show version')
    
    # Commande: interactive (par défaut)
    parser_interactive = subparsers.add_parser('interactive', help='Launch interactive menu')
    
    # Commande: generate
    parser_generate = subparsers.add_parser('generate', help='Generate payload')
    parser_generate.add_argument('--platform', required=True, choices=['windows', 'linux', 'macos', 'android'],
                                help='Target platform')
    parser_generate.add_argument('--arch', required=True, choices=['x64', 'x86', 'arm64', 'arm'],
                                help='Target architecture')
    parser_generate.add_argument('--type', required=True, 
                                choices=['reverse_tcp', 'bind_tcp', 'meterpreter', 'exec'],
                                help='Payload type')
    parser_generate.add_argument('--lhost', required=True, help='Listener host')
    parser_generate.add_argument('--lport', required=True, type=int, help='Listener port')
    parser_generate.add_argument('--evasion', help='Comma-separated evasion techniques (syscall,obfuscate,sandbox)')
    parser_generate.add_argument('--encrypt', choices=['XOR', 'AES256', 'RC4'], help='Encryption algorithm')
    parser_generate.add_argument('--format', default='exe', choices=['exe', 'dll', 'elf', 'raw', 'python', 'powershell'],
                                help='Output format')
    parser_generate.add_argument('--output', help='Output file path')
    parser_generate.add_argument('--listener', action='store_true', help='Generate listener file')
    
    # Commande: stego
    parser_stego = subparsers.add_parser('stego', help='Steganography operations')
    parser_stego.add_argument('action', choices=['hide', 'extract'], help='Action to perform')
    parser_stego.add_argument('--technique', required=True,
                             choices=['image_lsb', 'image_bitplane', 'image_dct', 
                                     'audio_lsb', 'audio_echo', 'text_zwc',
                                     'polyglot_png_zip', 'polyglot_jpg_exe'],
                             help='Steganography technique')
    parser_stego.add_argument('--carrier', required=True, help='Carrier file (image/audio/text)')
    parser_stego.add_argument('--payload', help='Payload file to hide (for hide action)')
    parser_stego.add_argument('--output', required=True, help='Output file')
    parser_stego.add_argument('--plane', type=int, default=0, help='Bit plane (for bitplane technique)')
    parser_stego.add_argument('--quality', type=int, default=85, help='JPEG quality (for DCT)')
    parser_stego.add_argument('--delay', type=float, default=1.0, help='Echo delay in ms')
    parser_stego.add_argument('--decay', type=float, default=0.5, help='Echo decay')
    
    # Commande: check
    parser_check = subparsers.add_parser('check', help='Check dependencies')
    parser_check.add_argument('--fix', action='store_true', help='Fix missing dependencies')
    parser_check.add_argument('--verbose', action='store_true', help='Verbose output')
    
    # Commande: config
    parser_config = subparsers.add_parser('config', help='Configure OrVex')
    parser_config.add_argument('--show', action='store_true', help='Show current configuration')
    parser_config.add_argument('--set', metavar='KEY=VALUE', help='Set configuration value')
    parser_config.add_argument('--reset', action='store_true', help='Reset configuration to defaults')
    parser_config.add_argument('--profile', help='Switch to profile')
    parser_config.add_argument('--create', action='store_true', help='Create new profile')
    parser_config.add_argument('--base', default='default', help='Base profile for creation')
    
    # Parser les arguments
    args = parser.parse_args()
    
    # Mode debug
    if args.debug:
        print(f"[*] Debug mode enabled")
        print(f"[*] Python: {sys.version}")
        print(f"[*] Platform: {platform.platform()}")
        print(f"[*] Arguments: {args}")
    
    # Version
    if args.command == 'version' or hasattr(args, 'version') and args.version:
        print(f"OrVex Framework v{__version__}")
        print(f"Author: {__author__}")
        print(f"Description: {__description__}")
        print(f"Platform: Cross-platform (Windows Dev / Linux Production)")
        sys.exit(0)
    
    # Vérifier root (sauf pour version et help)
    if args.command not in ['version', 'help']:
        if not cli.check_root(args):
            if not args.no_root_check:
                print("\n[!] Insufficient privileges. Use --no-root-check for development.")
                sys.exit(1)
    
    # Configurer l'environnement
    cli.setup_environment(args.debug)
    
    # Exécuter la commande
    try:
        if args.command == 'generate':
            success = cli.generate_payload(args)
            sys.exit(0 if success else 1)
            
        elif args.command == 'stego':
            success = cli.steganography(args)
            sys.exit(0 if success else 1)
            
        elif args.command == 'check':
            success = cli.check_dependencies(args)
            sys.exit(0 if success else 1)
            
        elif args.command == 'config':
            success = cli.configure(args)
            sys.exit(0 if success else 1)
            
        else:  # interactive (default)
            cli.run_interactive(args.debug)
            
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()