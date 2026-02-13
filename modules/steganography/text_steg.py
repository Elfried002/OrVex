#!/usr/bin/env python3
"""
Text Steganography Module
- Zero-Width Characters (ZWSP, ZWNJ, ZWJ, LRM, RLM)
- Whitespace Encoding
- Invisible Unicode characters
"""

import re
from typing import Optional, List, Tuple

class ZeroWidthSteg:
    """
    Cache des données dans des caractères invisibles
    ZWSP = \u200B (Zero Width Space)
    ZWNJ = \u200C (Zero Width Non-Joiner)
    ZWJ  = \u200D (Zero Width Joiner)
    LRM  = \u200E (Left-to-Right Mark)
    RLM  = \u200F (Right-to-Left Mark)
    """
    
    # Mapping 2 bits -> caractère invisible
    ZERO_WIDTH = {
        '00': '\u200B',  # Zero Width Space
        '01': '\u200C',  # Zero Width Non-Joiner
        '10': '\u200D',  # Zero Width Joiner
        '11': '\u200E',  # Left-to-Right Mark
    }
    
    # Mapping inverse
    REVERSE = {v: k for k, v in ZERO_WIDTH.items()}
    
    # Caractères invisibles supplémentaires
    EXTRA_INVISIBLE = [
        '\u200F',  # Right-to-Left Mark
        '\u202A',  # Left-to-Right Embedding
        '\u202B',  # Right-to-Left Embedding
        '\u202C',  # Pop Directional Formatting
        '\u202D',  # Left-to-Right Override
        '\u202E',  # Right-to-Left Override
        '\u2060',  # Word Joiner
        '\u2061',  # Function Application
        '\u2062',  # Invisible Times
        '\u2063',  # Invisible Separator
        '\u2064',  # Invisible Plus
        '\u2066',  # Left-to-Right Isolate
        '\u2067',  # Right-to-Left Isolate
        '\u2068',  # First Strong Isolate
        '\u2069',  # Pop Directional Isolate
        '\uFEFF',  # Zero Width No-Break Space
    ]
    
    def __init__(self, use_extra: bool = False):
        self.marker = "ORVEX"
        self.use_extra = use_extra
        
        if use_extra:
            # Utiliser plus de caractères (2 bits par caractère)
            self.mapping = {}
            for i, char in enumerate(self.EXTRA_INVISIBLE[:4]):
                bits = format(i, '02b')
                self.mapping[bits] = char
                self.REVERSE[char] = bits
        else:
            self.mapping = self.ZERO_WIDTH
    
    # ========== ENCODING ==========
    
    def encode(self, text: str, payload: str) -> str:
        """
        Cache un message dans le texte
        """
        # Convertir payload en binaire
        binary = ''.join(format(ord(c), '08b') for c in payload)
        
        # Ajouter marqueur et taille
        payload_len = format(len(payload), '016b')
        full_binary = self._text_to_bits(self.marker) + payload_len + binary
        
        # Grouper par 2 bits
        groups = [full_binary[i:i+2] for i in range(0, len(full_binary), 2)]
        
        # Convertir en caractères invisibles
        invisible = ''.join(self.mapping[g] for g in groups)
        
        # Insérer dans le texte
        # Option 1: Au milieu
        mid = len(text) // 2
        return text[:mid] + invisible + text[mid:]
    
    def encode_word_by_word(self, words: List[str], payload: str) -> str:
        """
        Cache en insérant entre les mots
        """
        binary = ''.join(format(ord(c), '08b') for c in payload)
        groups = [binary[i:i+2] for i in range(0, len(binary), 2)]
        
        result = []
        for i, word in enumerate(words):
            result.append(word)
            if i < len(groups):
                result.append(self.mapping[groups[i]])
        
        return ' '.join(result)
    
    def encode_at_punctuation(self, text: str, payload: str) -> str:
        """
        Cache après la ponctuation
        """
        binary = ''.join(format(ord(c), '08b') for c in payload)
        groups = [binary[i:i+2] for i in range(0, len(binary), 2)]
        
        result = text
        for group in groups:
            result = re.sub(r'([.!?])\s+', r'\1' + self.mapping[group] + ' ', result, count=1)
        
        return result
    
    # ========== DECODING ==========
    
    def decode(self, stego_text: str) -> Optional[str]:
        """
        Extrait le message caché
        """
        # Extraire tous les caractères invisibles
        invisible = ''
        for c in stego_text:
            if c in self.REVERSE:
                invisible += self.REVERSE[c]
        
        # Convertir en bits
        binary = ''.join(invisible)
        
        # Chercher marqueur
        marker_bits = self._text_to_bits(self.marker)
        marker_pos = binary.find(marker_bits)
        
        if marker_pos == -1:
            return None
        
        # Extraire taille et payload
        pos = marker_pos + len(marker_bits)
        payload_len = int(binary[pos:pos+16], 2)
        pos += 16
        
        # Extraire payload
        payload_bits = binary[pos:pos + (payload_len * 8)]
        
        # Convertir en texte
        return self._bits_to_text(payload_bits)
    
    def extract_all(self, stego_text: str) -> List[str]:
        """
        Extrait tous les messages possibles
        """
        messages = []
        
        # Essayer différents marqueurs
        for marker in ["ORVEX", "SECRET", "HIDDEN", "PAYLOAD"]:
            self.marker = marker
            msg = self.decode(stego_text)
            if msg:
                messages.append(msg)
        
        return messages
    
    # ========== ANALYSE ==========
    
    def detect(self, text: str) -> dict:
        """
        Détecte la présence de stéganographie
        """
        invisible_count = sum(1 for c in text if c in self.REVERSE)
        total_chars = len(text)
        
        return {
            'invisible_chars': invisible_count,
            'total_chars': total_chars,
            'ratio': invisible_count / total_chars if total_chars > 0 else 0,
            'suspicious': invisible_count > 0,
            'potential_capacity': invisible_count * 2 // 8  # bytes
        }
    
    # ========== UTILITAIRES ==========
    
    def _text_to_bits(self, text: str) -> str:
        """Convertit texte en binaire"""
        return ''.join(format(ord(c), '08b') for c in text)
    
    def _bits_to_text(self, bits: str) -> str:
        """Convertit binaire en texte"""
        chars = []
        for i in range(0, len(bits), 8):
            if i+8 <= len(bits):
                byte = int(bits[i:i+8], 2)
                chars.append(chr(byte))
        return ''.join(chars)


class WhitespaceSteg:
    """
    Cache dans les espaces et tabulations
    Space = 0, Tab = 1
    """
    
    def encode(self, text: str, payload: str) -> str:
        """
        Cache en utilisant espaces/tabs en fin de ligne
        """
        binary = ''.join(format(ord(c), '08b') for c in payload)
        
        lines = text.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            if i < len(binary):
                if binary[i] == '0':
                    result.append(' ')  # Space
                else:
                    result.append('\t')  # Tab
        
        return '\n'.join(result)
    
    def decode(self, text: str) -> Optional[str]:
        """
        Extrait le message
        """
        bits = ''
        for line in text.split('\n'):
            if line.endswith(' '):
                bits += '0'
            elif line.endswith('\t'):
                bits += '1'
        
        # Convertir en texte
        chars = []
        for i in range(0, len(bits), 8):
            if i+8 <= len(bits):
                chars.append(chr(int(bits[i:i+8], 2)))
        
        return ''.join(chars)