#!/usr/bin/env python3
"""
OrVex Dependency Checker
- Vérifie toutes les dépendances système
- Vérifie les packages Python
- Vérifie les permissions
- Installation automatique
"""

import os
import sys
import subprocess
import importlib
import shutil
import platform
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from colorama import init, Fore, Style

init(autoreset=True)

class DependencyChecker:
    """Vérificateur de dépendances pour OrVex"""
    
    def __init__(self):
        self.os_type = platform.system().lower()
        self.distro = self._detect_linux_distro()
        
        self.python_packages = {
            'colorama': 'colorama>=0.4.6',
            'yaml': 'pyyaml>=6.0',
            'requests': 'requests>=2.31.0',
            'PIL': 'Pillow>=10.0.0',
            'numpy': 'numpy>=1.24.0',
            'Crypto': 'pycryptodome>=3.19.0',
            'jinja2': 'Jinja2>=3.1.0',
            'cryptography': 'cryptography>=41.0.0'
        }
        
        self.system_packages = {
            'linux': {
                'kali': [
                    'metasploit-framework',
                    'mingw-w64',
                    'golang',
                    'xterm',
                    'apktool',
                    'zipalign',
                    'default-jdk',
                    'searchsploit',
                    'backdoor-factory',
                    'python3-pip',
                    'python3-venv',
                    'gcc',
                    'make'
                ],
                'ubuntu': [
                    'metasploit-framework',
                    'mingw-w64',
                    'golang',
                    'xterm',
                    'apktool',
                    'zipalign',
                    'default-jdk',
                    'exploitdb',
                    'python3-pip',
                    'python3-venv',
                    'gcc',
                    'make'
                ],
                'parrot': [
                    'metasploit-framework',
                    'mingw-w64',
                    'golang',
                    'xterm',
                    'apktool',
                    'zipalign',
                    'default-jdk',
                    'exploitdb',
                    'python3-pip',
                    'python3-venv',
                    'gcc',
                    'make'
                ],
                'generic': [
                    'metasploit-framework',
                    'mingw-w64',
                    'golang',
                    'xterm',
                    'python3-pip',
                    'python3-venv',
                    'gcc',
                    'make'
                ]
            },
            'windows': [
                'mingw-w64',
                'golang',
                'git',
                'python3'
            ],
            'darwin': [
                'metasploit',
                'mingw-w64',
                'go',
                'python3'
            ]
        }
    
    def _detect_linux_distro(self) -> str:
        """Détecte la distribution Linux"""
        if self.os_type != 'linux':
            return 'generic'
        
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'kali' in content:
                    return 'kali'
                elif 'ubuntu' in content:
                    return 'ubuntu'
                elif 'parrot' in content:
                    return 'parrot'
                elif 'debian' in content:
                    return 'debian'
                else:
                    return 'generic'
        except:
            return 'generic'
    
    def check_python_version(self) -> bool:
        """Vérifie la version de Python"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Python Environment Check{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        version = sys.version_info
        print(f"Version: {sys.version.split()[0]}")
        
        if version.major >= 3 and version.minor >= 8:
            print(f"{Fore.GREEN}✓ Python {version.major}.{version.minor}.{version.micro} OK{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}✗ Python 3.8+ required (found {version.major}.{version.minor}){Style.RESET_ALL}")
            return False
    
    def check_python_packages(self) -> Dict[str, bool]:
        """Vérifie les packages Python"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Python Packages Check{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        results = {}
        
        for module, package in self.python_packages.items():
            try:
                importlib.import_module(module)
                print(f"{Fore.GREEN}✓ {package.split('>=')[0]:<20} INSTALLED{Style.RESET_ALL}")
                results[package] = True
            except ImportError:
                print(f"{Fore.RED}✗ {package.split('>=')[0]:<20} MISSING{Style.RESET_ALL}")
                results[package] = False
        
        return results
    
    def check_system_packages(self) -> Dict[str, bool]:
        """Vérifie les packages système"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    System Packages Check ({self.distro}){Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        results = {}
        
        if self.os_type == 'linux':
            packages = self.system_packages['linux'].get(
                self.distro, 
                self.system_packages['linux']['generic']
            )
            
            for package in packages:
                # Vérifier avec dpkg
                result = subprocess.run(
                    ['dpkg', '-l', package],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0 and 'ii' in result.stdout:
                    print(f"{Fore.GREEN}✓ {package:<30} INSTALLED{Style.RESET_ALL}")
                    results[package] = True
                else:
                    print(f"{Fore.RED}✗ {package:<30} MISSING{Style.RESET_ALL}")
                    results[package] = False
        
        elif self.os_type == 'windows':
            for package in self.system_packages['windows']:
                # Vérifier avec where
                result = subprocess.run(
                    ['where', package],
                    capture_output=True,
                    shell=True
                )
                
                if result.returncode == 0:
                    print(f"{Fore.GREEN}✓ {package:<20} INSTALLED{Style.RESET_ALL}")
                    results[package] = True
                else:
                    print(f"{Fore.RED}✗ {package:<20} MISSING{Style.RESET_ALL}")
                    results[package] = False
        
        return results
    
    def check_tools(self) -> Dict[str, bool]:
        """Vérifie les outils spécifiques"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Essential Tools Check{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        tools = {
            'msfvenom': 'msfvenom',
            'mingw': 'x86_64-w64-mingw32-gcc',
            'go': 'go',
            'apktool': 'apktool',
            'xterm': 'xterm',
            'gcc': 'gcc',
            'make': 'make'
        }
        
        results = {}
        
        for name, cmd in tools.items():
            path = shutil.which(cmd)
            if path:
                print(f"{Fore.GREEN}✓ {name:<10} {path}{Style.RESET_ALL}")
                results[name] = True
            else:
                print(f"{Fore.RED}✗ {name:<10} NOT FOUND{Style.RESET_ALL}")
                results[name] = False
        
        return results
    
    def check_permissions(self) -> bool:
        """Vérifie les permissions"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Permissions Check{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        # Vérifier root
        if self.os_type == 'linux' or self.os_type == 'darwin':
            if os.geteuid() == 0:
                print(f"{Fore.GREEN}✓ Running as root{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠ Not running as root (some features may fail){Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.YELLOW}⚠ Permission check not applicable on Windows{Style.RESET_ALL}")
            return True
    
    def check_internet(self) -> bool:
        """Vérifie la connexion internet"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Internet Connection Check{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        try:
            subprocess.run(
                ['ping', '-c', '1', '8.8.8.8'],
                capture_output=True,
                timeout=2
            )
            print(f"{Fore.GREEN}✓ Internet: CONNECTED{Style.RESET_ALL}")
            return True
        except:
            print(f"{Fore.RED}✗ Internet: OFFLINE{Style.RESET_ALL}")
            return False
    
    def install_python_packages(self, packages: List[str] = None) -> bool:
        """Installe les packages Python manquants"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Installing Python Packages{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        if packages is None:
            packages = [pkg for module, pkg in self.python_packages.items()]
        
        try:
            subprocess.check_call([
                sys.executable, 
                '-m', 
                'pip', 
                'install', 
                '--upgrade',
                'pip'
            ])
            
            subprocess.check_call([
                sys.executable, 
                '-m', 
                'pip', 
                'install'
            ] + packages)
            
            print(f"{Fore.GREEN}✓ Python packages installed successfully{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Installation failed: {e}{Style.RESET_ALL}")
            return False
    
    def install_system_packages(self) -> bool:
        """Installe les packages système manquants"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Installing System Packages{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        if self.os_type != 'linux':
            print(f"{Fore.YELLOW}⚠ Automatic installation only supported on Linux{Style.RESET_ALL}")
            return False
        
        packages = self.system_packages['linux'].get(
            self.distro,
            self.system_packages['linux']['generic']
        )
        
        try:
            if self.distro in ['kali', 'ubuntu', 'parrot', 'debian']:
                subprocess.check_call(['apt-get', 'update'])
                subprocess.check_call([
                    'apt-get', 'install', '-y'
                ] + packages)
            
            print(f"{Fore.GREEN}✓ System packages installed successfully{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Installation failed: {e}{Style.RESET_ALL}")
            return False
    
    def run_full_check(self) -> Dict[str, any]:
        """Exécute une vérification complète"""
        results = {
            'python_version': False,
            'python_packages': {},
            'system_packages': {},
            'tools': {},
            'permissions': False,
            'internet': False
        }
        
        results['python_version'] = self.check_python_version()
        results['python_packages'] = self.check_python_packages()
        results['system_packages'] = self.check_system_packages()
        results['tools'] = self.check_tools()
        results['permissions'] = self.check_permissions()
        results['internet'] = self.check_internet()
        
        return results
    
    def fix_issues(self):
        """Tente de corriger automatiquement les problèmes"""
        print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    Auto-Fix Mode{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        
        # 1. Installer les packages Python manquants
        self.install_python_packages()
        
        # 2. Installer les packages système (si root)
        if os.geteuid() == 0:
            self.install_system_packages()
        else:
            print(f"{Fore.YELLOW}⚠ Run as root to install system packages{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✓ Auto-fix completed. Run check again.{Style.RESET_ALL}")


def main():
    """Point d'entrée principal"""
    print(f"{Fore.CYAN}")
    print("  ██████╗ ██████╗ ██╗   ██╗███████╗██╗  ██╗")
    print(" ██╔══██╗██╔══██╗██║   ██║██╔════╝╚██╗██╔╝")
    print(" ██████╔╝██████╔╝██║   ██║█████╗   ╚███╔╝ ")
    print(" ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══╝   ██╔██╗ ")
    print(" ██║  ██║██║  ██║ ╚████╔╝ ███████╗██╔╝ ██╗")
    print(" ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝")
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    Dependency Checker v1.9.0{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    For Kali Linux & Parrot OS{Style.RESET_ALL}\n")
    
    checker = DependencyChecker()
    
    # Mode auto-fix
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        checker.fix_issues()
        sys.exit(0)
    
    # Mode verbose
    verbose = len(sys.argv) > 1 and sys.argv[1] == '--verbose'
    
    # Exécuter la vérification
    results = checker.run_full_check()
    
    # Résumé
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Summary{Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
    
    python_ok = all(results['python_packages'].values())
    system_ok = all(results['system_packages'].values())
    tools_ok = all(results['tools'].values())
    
    if results['python_version'] and python_ok and system_ok and tools_ok:
        print(f"{Fore.GREEN}✓ All checks passed! OrVex is ready to use.{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"{Fore.YELLOW}⚠ Some checks failed. Run with --fix to attempt automatic repair.{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()