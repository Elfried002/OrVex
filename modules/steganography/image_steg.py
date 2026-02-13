#!/usr/bin/env python3
"""
Image Steganography Module
- LSB (Least Significant Bit)
- Bit Plane Slicing
- DCT (Discrete Cosine Transform) pour JPG
"""

import numpy as np
from PIL import Image
import struct
import os
from typing import Optional, Tuple, List

class ImageSteganography:
    """Cache et extrait des payloads dans des images"""
    
    def __init__(self):
        self.marker = b"ORVEX_PAYLOAD_START"
        self.marker_len = len(self.marker)
        self.lsb_bits = 1  # Nombre de bits LSB à utiliser
    
    # ========== LSB TECHNIQUES ==========
    
    def lsb_embed(self, image_path: str, payload: bytes, output_path: str) -> bool:
        """
        Cache un payload dans une image (LSB classique)
        """
        try:
            # Ouvrir l'image
            img = Image.open(image_path)
            
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            height, width, channels = img_array.shape
            
            # Préparer le payload avec marqueur et taille
            payload_size = struct.pack('>I', len(payload))
            full_payload = self.marker + payload_size + payload
            
            # Convertir en bits
            payload_bits = self._bytes_to_bits(full_payload)
            
            # Vérifier la capacité
            max_bytes = (height * width * channels) // 8
            if len(full_payload) > max_bytes:
                raise ValueError(f"Payload too large: {len(full_payload)} > {max_bytes}")
            
            # Cacher les bits dans LSB
            flat_array = img_array.flatten()
            
            for i, bit in enumerate(payload_bits):
                flat_array[i] = (flat_array[i] & 0xFE) | bit
            
            # Reconstruire l'image
            modified_array = flat_array.reshape(img_array.shape)
            modified_img = Image.fromarray(modified_array.astype('uint8'), 'RGB')
            
            # Sauvegarder
            modified_img.save(output_path, format='PNG')
            print(f"[✓] Payload caché: {len(payload)} bytes dans {output_path}")
            return True
            
        except Exception as e:
            print(f"[!] LSB embed error: {e}")
            return False
    
    def lsb_extract(self, image_path: str) -> Optional[bytes]:
        """
        Extrait un payload d'une image (LSB)
        """
        try:
            # Ouvrir l'image
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            flat_array = img_array.flatten()
            
            # Extraire les LSB
            bits = []
            for pixel in flat_array:
                bits.append(pixel & 1)
            
            # Convertir en bytes
            data = self._bits_to_bytes(bits)
            
            # Chercher le marqueur
            marker_pos = data.find(self.marker)
            if marker_pos == -1:
                print("[!] Marqueur non trouvé")
                return None
            
            # Extraire la taille et le payload
            pos = marker_pos + self.marker_len
            payload_size = struct.unpack('>I', data[pos:pos+4])[0]
            pos += 4
            
            payload = data[pos:pos+payload_size]
            print(f"[✓] Payload extrait: {len(payload)} bytes")
            return payload
            
        except Exception as e:
            print(f"[!] LSB extract error: {e}")
            return None
    
    # ========== BIT PLANE SLICING ==========
    
    def bit_plane_embed(self, image_path: str, payload: bytes, plane: int = 0, output_path: str = None) -> bool:
        """
        Cache dans un plan de bits spécifique (plus robuste)
        """
        try:
            img = Image.open(image_path).convert('L')  # Convertir en niveaux de gris
            img_array = np.array(img)
            
            # Préparer payload
            payload_bits = self._bytes_to_bits(self.marker + struct.pack('>I', len(payload)) + payload)
            
            # Vérifier capacité
            if len(payload_bits) > img_array.size:
                raise ValueError("Payload trop grand")
            
            # Cacher dans le plan de bits spécifié
            for i, bit in enumerate(payload_bits):
                row = i // img_array.shape[1]
                col = i % img_array.shape[1]
                
                # Effacer le bit du plan cible et le remplacer
                mask = 1 << plane
                img_array[row, col] = (img_array[row, col] & ~mask) | (bit << plane)
            
            # Sauvegarder
            if output_path is None:
                output_path = f"stego_plane{plane}.png"
            
            Image.fromarray(img_array).save(output_path)
            return True
            
        except Exception as e:
            print(f"[!] Bit plane error: {e}")
            return False
    
    def bit_plane_extract(self, image_path: str, plane: int = 0) -> Optional[bytes]:
        """
        Extrait depuis un plan de bits spécifique
        """
        try:
            img = Image.open(image_path).convert('L')
            img_array = np.array(img)
            
            # Extraire les bits du plan spécifié
            bits = []
            for pixel in img_array.flatten():
                bits.append((pixel >> plane) & 1)
            
            data = self._bits_to_bytes(bits)
            
            # Chercher marqueur
            marker_pos = data.find(self.marker)
            if marker_pos == -1:
                return None
            
            pos = marker_pos + self.marker_len
            size = struct.unpack('>I', data[pos:pos+4])[0]
            pos += 4
            
            return data[pos:pos+size]
            
        except Exception as e:
            print(f"[!] Bit plane extract error: {e}")
            return None
    
    # ========== DCT (JPG) STEGANOGRAPHY ==========
    
    def dct_embed(self, jpg_path: str, payload: bytes, output_path: str, quality: int = 75) -> bool:
        """
        Cache dans les coefficients DCT (format JPG)
        Nécessite le module jpeg_turbo ou opencv
        """
        try:
            import cv2
            
            # Lire l'image
            img = cv2.imread(jpg_path)
            if img is None:
                raise ValueError("Impossible de lire l'image")
            
            # Convertir en YCrCb pour traiter la luminance
            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            y, cr, cb = cv2.split(img_yuv)
            
            # Diviser en blocs 8x8 pour DCT
            blocks = []
            for i in range(0, y.shape[0], 8):
                for j in range(0, y.shape[1], 8):
                    block = y[i:i+8, j:j+8]
                    if block.shape == (8,8):
                        blocks.append(block)
            
            # Convertir les blocs en float pour DCT
            blocks_float = [block.astype(np.float32) for block in blocks]
            
            # Appliquer DCT
            dct_blocks = [cv2.dct(block) for block in blocks_float]
            
            # Préparer payload
            payload_bits = self._bytes_to_bits(self.marker + struct.pack('>I', len(payload)) + payload)
            
            # Cacher dans les coefficients DCT (technique classique)
            for i, bit in enumerate(payload_bits):
                if i >= len(dct_blocks):
                    break
                # Modifier le coefficient (1,1) de chaque bloc
                dct_blocks[i][1][1] = (dct_blocks[i][1][1] & 0xFE) | bit
            
            # Inverse DCT
            reconstructed = []
            for dct_block in dct_blocks:
                block = cv2.idct(dct_block)
                reconstructed.append(block.clip(0, 255).astype(np.uint8))
            
            # Reconstruire l'image
            idx = 0
            for i in range(0, y.shape[0], 8):
                for j in range(0, y.shape[1], 8):
                    if idx < len(reconstructed):
                        y[i:i+8, j:j+8] = reconstructed[idx]
                        idx += 1
            
            # Réassembler l'image
            img_yuv = cv2.merge([y, cr, cb])
            img_bgr = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            
            # Sauvegarder
            cv2.imwrite(output_path, img_bgr, [cv2.IMWRITE_JPEG_QUALITY, quality])
            return True
            
        except ImportError:
            print("[!] OpenCV non installé. Installez: pip install opencv-python")
            return False
        except Exception as e:
            print(f"[!] DCT embed error: {e}")
            return False
    
    # ========== UTILITAIRES ==========
    
    def _bytes_to_bits(self, data: bytes) -> List[int]:
        """Convertit bytes en liste de bits"""
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits
    
    def _bits_to_bytes(self, bits: List[int]) -> bytes:
        """Convertit liste de bits en bytes"""
        bytes_data = bytearray()
        for i in range(0, len(bits), 8):
            if i + 8 <= len(bits):
                byte = 0
                for j in range(8):
                    byte |= bits[i + j] << (7 - j)
                bytes_data.append(byte)
        return bytes(bytes_data)
    
    def calculate_capacity(self, image_path: str) -> int:
        """Calcule la capacité maximale de l'image"""
        img = Image.open(image_path)
        if img.mode == 'RGB':
            return (img.size[0] * img.size[1] * 3) // 8
        else:
            return (img.size[0] * img.size[1]) // 8
    
    def analyze_lsb(self, image_path: str) -> dict:
        """Analyse la distribution LSB pour détecter une stégano"""
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        
        flat = img_array.flatten()
        lsb_sum = sum(pixel & 1 for pixel in flat)
        lsb_ratio = lsb_sum / len(flat)
        
        return {
            'total_pixels': len(flat),
            'lsb_ones': lsb_sum,
            'lsb_zeros': len(flat) - lsb_sum,
            'lsb_ratio': lsb_ratio,
            'suspicious': abs(lsb_ratio - 0.5) < 0.1  # Proche de 50% = suspect
        }