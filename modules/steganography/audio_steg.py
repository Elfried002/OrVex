#!/usr/bin/env python3
"""
Audio Steganography Module
- LSB in WAV files
- Echo Hiding
- Phase Coding
"""

import wave
import numpy as np
import struct
import math
from typing import Optional, List, Tuple

class AudioSteg:
    """Cache des payloads dans des fichiers audio WAV"""
    
    def __init__(self):
        self.marker = b"ORVEX_AUDIO"
        self.sample_width = 2  # 16-bit audio
        self.frame_rate = 44100  # CD quality
    
    # ========== LSB AUDIO ==========
    
    def lsb_embed(self, wav_path: str, payload: bytes, output_path: str) -> bool:
        """
        Cache un payload dans les LSB d'un fichier WAV
        """
        try:
            # Lire le WAV
            wav = wave.open(wav_path, 'rb')
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            wav.close()
            
            # Convertir en array numpy (int16)
            audio = np.frombuffer(frames, dtype=np.int16)
            
            # Préparer payload avec marqueur et taille
            payload_size = struct.pack('>I', len(payload))
            full_payload = self.marker + payload_size + payload
            payload_bits = self._bytes_to_bits(full_payload)
            
            # Vérifier capacité
            if len(payload_bits) > len(audio):
                raise ValueError(f"Payload trop grand: {len(payload_bits)} > {len(audio)}")
            
            # LSB encoding
            for i, bit in enumerate(payload_bits):
                audio[i] = (audio[i] & 0xFFFE) | bit
            
            # Sauvegarder
            output = wave.open(output_path, 'wb')
            output.setparams(params)
            output.writeframes(audio.tobytes())
            output.close()
            
            print(f"[✓] Payload caché dans {output_path}")
            return True
            
        except Exception as e:
            print(f"[!] LSB audio error: {e}")
            return False
    
    def lsb_extract(self, wav_path: str) -> Optional[bytes]:
        """
        Extrait un payload d'un fichier WAV
        """
        try:
            wav = wave.open(wav_path, 'rb')
            frames = wav.readframes(wav.getnframes())
            wav.close()
            
            audio = np.frombuffer(frames, dtype=np.int16)
            
            # Extraire LSB
            bits = []
            for sample in audio:
                bits.append(sample & 1)
            
            # Convertir en bytes
            data = self._bits_to_bytes(bits)
            
            # Chercher marqueur
            marker_pos = data.find(self.marker)
            if marker_pos == -1:
                return None
            
            pos = marker_pos + len(self.marker)
            size = struct.unpack('>I', data[pos:pos+4])[0]
            pos += 4
            
            return data[pos:pos+size]
            
        except Exception as e:
            print(f"[!] LSB extract error: {e}")
            return None
    
    # ========== ECHO HIDING ==========
    
    def echo_embed(self, wav_path: str, payload: bytes, output_path: str, 
                   delay_ms: float = 1.0, decay: float = 0.5) -> bool:
        """
        Cache des données en modifiant l'écho
        0 = bit 0, 1 = bit 1 avec délais différents
        """
        try:
            # Lire le WAV
            wav = wave.open(wav_path, 'rb')
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            wav.close()
            
            audio = np.frombuffer(frames, dtype=np.int16)
            audio_float = audio.astype(np.float32)
            
            # Paramètres d'écho
            sample_rate = params.framerate
            delay_samples_0 = int(delay_ms * sample_rate / 1000)
            delay_samples_1 = delay_samples_0 * 2  # Double délai pour bit 1
            
            # Préparer payload en bits
            payload_bits = self._bytes_to_bits(self.marker + struct.pack('>I', len(payload)) + payload)
            
            # Segmenter l'audio
            segment_size = 1000  # Samples par segment
            num_segments = len(audio_float) // segment_size
            
            for i, bit in enumerate(payload_bits):
                if i >= num_segments - 1:
                    break
                
                start = i * segment_size
                end = start + segment_size
                
                segment = audio_float[start:end].copy()
                
                # Choisir le délai selon le bit
                delay = delay_samples_0 if bit == 0 else delay_samples_1
                
                # Ajouter l'écho
                if start + delay < len(audio_float):
                    audio_float[start + delay:end + delay] += segment * decay
            
            # Convertir back to int16
            audio_float = np.clip(audio_float, -32768, 32767)
            audio_out = audio_float.astype(np.int16)
            
            # Sauvegarder
            output = wave.open(output_path, 'wb')
            output.setparams(params)
            output.writeframes(audio_out.tobytes())
            output.close()
            
            return True
            
        except Exception as e:
            print(f"[!] Echo hiding error: {e}")
            return False
    
    def echo_extract(self, wav_path: str, delay_ms: float = 1.0) -> Optional[bytes]:
        """
        Extrait les données cachées par écho
        """
        try:
            wav = wave.open(wav_path, 'rb')
            frames = wav.readframes(wav.getnframes())
            wav.close()
            
            audio = np.frombuffer(frames, dtype=np.int16)
            audio_float = audio.astype(np.float32)
            
            sample_rate = wav.getframerate()
            delay_samples_0 = int(delay_ms * sample_rate / 1000)
            delay_samples_1 = delay_samples_0 * 2
            
            # Calculer l'autocorrélation pour détecter les délais
            bits = []
            segment_size = 1000
            num_segments = len(audio_float) // segment_size
            
            for i in range(num_segments - 2):
                start = i * segment_size
                end = start + segment_size
                
                # Analyser les pics d'autocorrélation
                corr_0 = np.correlate(audio_float[start:end], 
                                       audio_float[start + delay_samples_0:end + delay_samples_0])
                corr_1 = np.correlate(audio_float[start:end], 
                                       audio_float[start + delay_samples_1:end + delay_samples_1])
                
                if len(corr_0) > 0 and len(corr_1) > 0:
                    bit = 0 if np.abs(corr_0[0]) > np.abs(corr_1[0]) else 1
                    bits.append(bit)
            
            # Convertir en bytes
            data = self._bits_to_bytes(bits)
            
            # Chercher marqueur
            marker_pos = data.find(self.marker)
            if marker_pos == -1:
                return None
            
            pos = marker_pos + len(self.marker)
            size = struct.unpack('>I', data[pos:pos+4])[0]
            pos += 4
            
            return data[pos:pos+size]
            
        except Exception as e:
            print(f"[!] Echo extract error: {e}")
            return None
    
    # ========== PHASE CODING ==========
    
    def phase_embed(self, wav_path: str, payload: bytes, output_path: str) -> bool:
        """
        Cache des données dans la phase du signal audio
        Technique plus robuste mais plus complexe
        """
        try:
            wav = wave.open(wav_path, 'rb')
            frames = wav.readframes(wav.getnframes())
            params = wav.getparams()
            wav.close()
            
            audio = np.frombuffer(frames, dtype=np.int16)
            
            # FFT
            fft = np.fft.fft(audio)
            magnitude = np.abs(fft)
            phase = np.angle(fft)
            
            # Préparer payload
            payload_bits = self._bytes_to_bits(self.marker + struct.pack('>I', len(payload)) + payload)
            
            # Modifier la phase (technique PSK-like)
            for i, bit in enumerate(payload_bits):
                if i < len(phase):
                    phase[i] = 0 if bit == 0 else math.pi
            
            # Inverse FFT
            fft_new = magnitude * np.exp(1j * phase)
            audio_new = np.fft.ifft(fft_new).real.astype(np.int16)
            
            # Sauvegarder
            output = wave.open(output_path, 'wb')
            output.setparams(params)
            output.writeframes(audio_new.tobytes())
            output.close()
            
            return True
            
        except Exception as e:
            print(f"[!] Phase coding error: {e}")
            return False
    
    # ========== UTILITAIRES ==========
    
    def _bytes_to_bits(self, data: bytes) -> List[int]:
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits
    
    def _bits_to_bytes(self, bits: List[int]) -> bytes:
        bytes_data = bytearray()
        for i in range(0, len(bits), 8):
            if i + 8 <= len(bits):
                byte = 0
                for j in range(8):
                    byte |= bits[i + j] << (7 - j)
                bytes_data.append(byte)
        return bytes(bytes_data)
    
    def create_test_wav(self, duration: float = 5.0, output: str = "test.wav"):
        """Crée un fichier WAV de test"""
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Créer un signal simple (sinus 440Hz)
        signal = np.sin(2 * np.pi * 440 * t) * 32767
        
        # Sauvegarder
        wav = wave.open(output, 'wb')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(signal.astype(np.int16).tobytes())
        wav.close()