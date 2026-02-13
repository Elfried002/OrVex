#!/usr/bin/env python3
"""
Configuration Manager for OrVex Framework v2.1.0
- YAML-based configuration
- Multi-profile support
- API keys management
"""

import os
import yaml
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from cryptography.fernet import Fernet
from colorama import Fore, Style

class OrVexConfig:
    """Gestionnaire de configuration principal"""
    
    DEFAULT_CONFIG = {
        'version': '2.1.0',
        'general': {
            'debug': False,
            'log_level': 'INFO',
            'workspace': '~/orvex/output',
            'temp_dir': '/tmp/orvex',
            'max_payload_size': 52428800,
            'concurrent_jobs': 4
        },
        'network': {
            'default_lhost': '192.168.1.100',
            'default_lport': 4444,
            'default_protocol': 'tcp',
            'timeout': 30,
        },
        'payloads': {
            'windows': {
                'x64': ['meterpreter', 'reverse_tcp', 'exec', 'bind_tcp'],
                'x86': ['meterpreter', 'reverse_tcp', 'exec', 'bind_tcp']
            },
            'linux': {
                'x64': ['reverse_tcp', 'bind_tcp', 'exec', 'meterpreter'],
                'x86': ['reverse_tcp', 'bind_tcp', 'exec', 'meterpreter']
            },
            'macos': {
                'x64': ['reverse_tcp', 'exec', 'meterpreter'],
                'arm64': ['reverse_tcp', 'exec']
            },
            'android': {
                'arm': ['meterpreter', 'reverse_tcp'],
                'arm64': ['meterpreter', 'reverse_tcp']
            }
        },
        'evasion': {
            'syscalls': {
                'enabled': True,
                'hells_gate': True,
                'halos_gate': False,
            },
            'process_hollowing': {
                'enabled': True,
                'target_processes': ['svchost.exe', 'explorer.exe'],
            },
            'sandbox_checks': {
                'enabled': True,
                'check_debugger': True,
                'check_vm': True,
            },
            'obfuscation_level': 2
        },
        'encryption': {
            'default': 'AES256',
            'algorithms': ['XOR', 'AES256', 'RC4'],
            'xor_key': '0xAA',
        },
        'steganography': {
            'image': {
                'lsb_bits': 1,
                'marker': 'ORVEX',
                'formats': ['png', 'jpg', 'bmp']
            },
            'audio': {
                'marker': 'ORVEX_AUDIO',
                'sample_width': 2,
                'frame_rate': 44100,
            },
            'text': {
                'marker': 'ORVEX',
            },
            'network': {
                'dns_domain': 'orvex.c2',
                'dns_server': '8.8.8.8',
            }
        },
        'api_keys': {
            'virustotal': '',
            'shodan': '',
            'hybrid_analysis': '',
        },
        'paths': {
            'msfvenom': '/usr/bin/msfvenom',
            'mingw': '/usr/bin/x86_64-w64-mingw32-gcc',
            'go': '/usr/bin/go',
            'apktool': '/usr/bin/apktool',
            'searchsploit': '/usr/bin/searchsploit',
            'upx': '/usr/bin/upx'
        }
    }
    
    def __init__(self, profile='default'):
        self.profile = profile
        self.config_dir = Path.home() / '.orvex'
        self.config_file = self.config_dir / f'config_{profile}.yaml'
        self.key_file = self.config_dir / 'key.key'
        self.cipher = None
        self.config = self.load()
        
    def _init_crypto(self):
        """Initialise le chiffrement"""
        try:
            if not self.key_file.exists():
                key = Fernet.generate_key()
                self.key_file.write_bytes(key)
                self.key_file.chmod(0o600)
            else:
                key = self.key_file.read_bytes()
            self.cipher = Fernet(key)
        except:
            self.cipher = None
    
    def _ensure_dirs(self):
        """Crée les dossiers nécessaires"""
        self.config_dir.mkdir(exist_ok=True, mode=0o700)
        (self.config_dir / 'output').mkdir(exist_ok=True)
        (self.config_dir / 'logs').mkdir(exist_ok=True)
    
    def load(self) -> Dict[str, Any]:
        """Charge la configuration"""
        self._ensure_dirs()
        self._init_crypto()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    return self._merge_config(self.DEFAULT_CONFIG, config)
            except:
                return self.DEFAULT_CONFIG.copy()
        else:
            self.save(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save(self, config: Dict[str, Any] = None):
        """Sauvegarde la configuration"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False)
            self.config_file.chmod(0o600)
            print(f"{Fore.GREEN}[✓] Configuration saved{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Error saving config: {e}{Style.RESET_ALL}")
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """Merge deux configurations"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except:
            return default
    
    def set(self, key: str, value: Any):
        """Définit une valeur"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Récupère une clé API"""
        encrypted = self.config.get('api_keys', {}).get(service, '')
        if encrypted and self.cipher:
            try:
                return self.cipher.decrypt(encrypted.encode()).decode()
            except:
                return encrypted
        return encrypted
    
    def set_api_key(self, service: str, key: str):
        """Sauvegarde une clé API"""
        if self.cipher:
            encrypted = self.cipher.encrypt(key.encode()).decode()
        else:
            encrypted = key
        
        if 'api_keys' not in self.config:
            self.config['api_keys'] = {}
        self.config['api_keys'][service] = encrypted
        self.save()
        print(f"{Fore.GREEN}[✓] API key saved{Style.RESET_ALL}")
    
    def reset(self):
        """Réinitialise la configuration"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
        print(f"{Fore.GREEN}[✓] Configuration reset{Style.RESET_ALL}")
    
    def list_profiles(self) -> list:
        """Liste les profils"""
        profiles = []
        for f in self.config_dir.glob('config_*.yaml'):
            profile = f.stem.replace('config_', '')
            profiles.append(profile)
        return profiles


global_config = OrVexConfig()

def get_config():
    return global_config