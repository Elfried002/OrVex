#!/usr/bin/env python3
"""
Polyglot Files Generator
- PNG + ZIP polyglot
- JPG + EXE polyglot
- PDF + EXE polyglot
- GIF + RAR polyglot
"""

import os
import struct
import zlib
import shutil
from typing import Optional, Tuple, List

class PolyglotGenerator:
    """
    Générateur de fichiers polyglottes
    Un fichier valide dans plusieurs formats
    """
    
    # ========== PNG + ZIP ==========
    
    @staticmethod
    def create_png_zip(png_file: str, zip_file: str, output_file: str) -> bool:
        """
        Crée un fichier valide à la fois PNG et ZIP
        Technique: Ajouter le ZIP après la fin du PNG
        """
        try:
            with open(png_file, 'rb') as f:
                png_data = f.read()
            
            with open(zip_file, 'rb') as f:
                zip_data = f.read()
            
            # Vérifier que c'est un PNG valide
            if not png_data.startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError("Fichier PNG invalide")
            
            # Chercher la fin du PNG (IEND chunk)
            iend_pos = png_data.rfind(b'IEND')
            if iend_pos == -1:
                raise ValueError("Chunk IEND non trouvé")
            
            # PNG se termine par IEND (12 bytes)
            png_end = iend_pos + 12
            
            # Créer le polyglotte: PNG + ZIP
            with open(output_file, 'wb') as f:
                f.write(png_data[:png_end])  # PNG complet
                f.write(zip_data)  # ZIP après
            
            print(f"[✓] PNG+ZIP polyglot créé: {output_file}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    @staticmethod
    def extract_zip_from_png(polyglot_file: str, output_zip: str) -> bool:
        """
        Extrait la partie ZIP d'un polyglotte PNG+ZIP
        """
        try:
            with open(polyglot_file, 'rb') as f:
                data = f.read()
            
            # Chercher la signature ZIP
            zip_signature = b'PK\x03\x04'
            zip_pos = data.find(zip_signature)
            
            if zip_pos == -1:
                raise ValueError("Signature ZIP non trouvée")
            
            with open(output_zip, 'wb') as f:
                f.write(data[zip_pos:])
            
            print(f"[✓] ZIP extrait: {output_zip}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    # ========== JPG + EXE ==========
    
    @staticmethod
    def create_jpg_exe(jpg_file: str, exe_file: str, output_file: str) -> bool:
        """
        Crée un fichier valide JPG et EXE
        Technique: Ajouter EXE après commentaire JPG
        """
        try:
            with open(jpg_file, 'rb') as f:
                jpg_data = f.read()
            
            with open(exe_file, 'rb') as f:
                exe_data = f.read()
            
            # Vérifier JPG
            if not jpg_data.startswith(b'\xff\xd8'):
                raise ValueError("JPG invalide")
            
            # Chercher la fin du JPG (FF D9)
            eoi_pos = jpg_data.rfind(b'\xff\xd9')
            if eoi_pos == -1:
                raise ValueError("Fin JPG non trouvée")
            
            # JPG peut avoir des commentaires avant EOI
            comment_pos = jpg_data.rfind(b'\xff\xfe', 0, eoi_pos)
            
            if comment_pos != -1:
                # Utiliser le commentaire existant
                base = jpg_data[:comment_pos + 4]  # Garder le commentaire
                rest = jpg_data[comment_pos + 4:eoi_pos + 2]
            else:
                # Ajouter un commentaire
                comment = b'\xff\xfe\x00\x08Comment'
                base = jpg_data[:eoi_pos]
                rest = b''
            
            # Créer le polyglotte
            with open(output_file, 'wb') as f:
                f.write(base)
                f.write(exe_data)  # EXE caché dans le commentaire
                f.write(rest)
                f.write(b'\xff\xd9')  # Fin JPG
            
            print(f"[✓] JPG+EXE polyglot créé: {output_file}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    @staticmethod
    def extract_exe_from_jpg(polyglot_file: str, output_exe: str) -> bool:
        """
        Extrait l'EXE d'un polyglotte JPG+EXE
        """
        try:
            with open(polyglot_file, 'rb') as f:
                data = f.read()
            
            # Chercher la signature MZ
            mz_pos = data.find(b'MZ')
            if mz_pos == -1 or mz_pos + 64 >= len(data):
                raise ValueError("EXE non trouvé")
            
            # Chercher la signature PE
            pe_pos = data.find(b'PE\x00\x00', mz_pos)
            if pe_pos == -1:
                raise ValueError("PE non trouvé")
            
            # Extraire l'EXE complet
            with open(output_exe, 'wb') as f:
                f.write(data[mz_pos:])
            
            print(f"[✓] EXE extrait: {output_exe}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    # ========== PDF + EXE ==========
    
    @staticmethod
    def create_pdf_exe(pdf_file: str, exe_file: str, output_file: str) -> bool:
        """
        Crée un fichier valide PDF et EXE
        Technique: Utiliser les commentaires PDF
        """
        try:
            with open(pdf_file, 'rb') as f:
                pdf_data = f.read()
            
            with open(exe_file, 'rb') as f:
                exe_data = f.read()
            
            # Vérifier PDF
            if not pdf_data.startswith(b'%PDF'):
                raise ValueError("PDF invalide")
            
            # Chercher la fin du PDF
            eof_pos = pdf_data.rfind(b'%%EOF')
            if eof_pos == -1:
                raise ValueError("EOF non trouvé")
            
            # PDF peut avoir des commentaires
            # Les commentaires commencent par %
            
            # Créer le polyglotte: PDF + EXE avant %%EOF
            with open(output_file, 'wb') as f:
                f.write(pdf_data[:eof_pos])  # PDF sans EOF
                f.write(b'\n%')  # Commentaire
                f.write(exe_data)  # EXE caché
                f.write(b'\n')
                f.write(pdf_data[eof_pos:])  # %%EOF
            
            print(f"[✓] PDF+EXE polyglot créé: {output_file}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    @staticmethod
    def extract_from_pdf(polyglot_file: str, output_file: str) -> bool:
        """
        Extrait les données cachées d'un PDF
        """
        try:
            with open(polyglot_file, 'rb') as f:
                data = f.read()
            
            # Chercher le début du payload (après un commentaire)
            comment_start = data.find(b'\n%')
            if comment_start == -1:
                raise ValueError("Payload non trouvé")
            
            # Chercher la fin du payload
            eof_pos = data.find(b'%%EOF', comment_start)
            if eof_pos == -1:
                eof_pos = len(data)
            
            # Extraire
            payload = data[comment_start + 2:eof_pos]
            
            with open(output_file, 'wb') as f:
                f.write(payload)
            
            print(f"[✓] Payload extrait: {output_file}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    # ========== GIF + RAR ==========
    
    @staticmethod
    def create_gif_rar(gif_file: str, rar_file: str, output_file: str) -> bool:
        """
        Crée un fichier valide GIF et RAR
        """
        try:
            with open(gif_file, 'rb') as f:
                gif_data = f.read()
            
            with open(rar_file, 'rb') as f:
                rar_data = f.read()
            
            # Vérifier GIF
            if not gif_data.startswith(b'GIF89a') and not gif_data.startswith(b'GIF87a'):
                raise ValueError("GIF invalide")
            
            # GIF se termine par 00 3B
            gif_end = gif_data.rfind(b'\x00\x3b')
            if gif_end == -1:
                raise ValueError("Fin GIF non trouvée")
            
            # Créer polyglotte
            with open(output_file, 'wb') as f:
                f.write(gif_data[:gif_end + 2])  # GIF complet
                f.write(rar_data)  # RAR après
            
            print(f"[✓] GIF+RAR polyglot créé: {output_file}")
            return True
            
        except Exception as e:
            print(f"[!] Erreur: {e}")
            return False
    
    # ========== UTILITAIRES ==========
    
    @staticmethod
    def identify(file_path: str) -> List[str]:
        """
        Identifie les formats valides d'un polyglotte
        """
        formats = []
        
        with open(file_path, 'rb') as f:
            data = f.read(1024)  # Lire début
            
            # PNG
            if data.startswith(b'\x89PNG\r\n\x1a\n'):
                formats.append('PNG')
            
            # JPG
            if data.startswith(b'\xff\xd8'):
                formats.append('JPG')
            
            # GIF
            if data.startswith(b'GIF89a') or data.startswith(b'GIF87a'):
                formats.append('GIF')
            
            # PDF
            if data.startswith(b'%PDF'):
                formats.append('PDF')
            
            # ZIP
            if data.startswith(b'PK\x03\x04'):
                formats.append('ZIP')
            
            # EXE (MZ)
            if data.startswith(b'MZ'):
                formats.append('EXE')
            
            # RAR
            if data.startswith(b'Rar!\x1a\x07'):
                formats.append('RAR')
        
        return formats
    
    @staticmethod
    def verify(file_path: str) -> dict:
        """
        Vérifie l'intégrité d'un polyglotte
        """
        results = {}
        formats = PolyglotGenerator.identify(file_path)
        
        for fmt in formats:
            try:
                if fmt == 'PNG':
                    from PIL import Image
                    Image.open(file_path).verify()
                    results[fmt] = True
                elif fmt == 'JPG':
                    from PIL import Image
                    Image.open(file_path).verify()
                    results[fmt] = True
                elif fmt == 'GIF':
                    from PIL import Image
                    Image.open(file_path).verify()
                    results[fmt] = True
                elif fmt == 'PDF':
                    # Vérification basique
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        if b'%%EOF' in data:
                            results[fmt] = True
                        else:
                            results[fmt] = False
                elif fmt == 'ZIP':
                    import zipfile
                    results[fmt] = zipfile.is_zipfile(file_path)
                elif fmt == 'EXE':
                    # Vérification basique
                    with open(file_path, 'rb') as f:
                        data = f.read(1024)
                        results[fmt] = data.find(b'PE\x00\x00') != -1
                elif fmt == 'RAR':
                    # Vérification basique
                    with open(file_path, 'rb') as f:
                        data = f.read(1024)
                        results[fmt] = data.startswith(b'Rar!\x1a\x07')
                else:
                    results[fmt] = False
            except:
                results[fmt] = False
        
        return results