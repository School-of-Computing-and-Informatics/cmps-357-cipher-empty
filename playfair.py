"""
Playfair Cipher implementation for PA2.

The Playfair cipher is a digraph substitution cipher that encrypts pairs of letters.
This implementation handles the standard alphabet and some extended characters.
"""

from typing import List, Tuple
import string


class PlayfairCipher:
    """
    Playfair cipher decryption implementation.
    
    Note: This is the third cipher choice as specified in the requirements.
    Playfair is a substitution cipher that operates on pairs of letters (digraphs).
    """
    
    def __init__(self):
        """Initialize the Playfair cipher."""
        # For simplicity, we'll work with just the standard alphabet
        # and treat I and J as the same letter (traditional Playfair)
        self.base_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.common_keys = [
            'keyword', 'secret', 'cipher', 'playfair', 'code', 'test', 'hello',
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
            'key', 'word', 'example', 'monarchy', 'charles'  # Classic Playfair examples
        ]
    
    def create_key_square(self, key: str) -> List[List[str]]:
        """
        Create a 5x5 key square for the Playfair cipher.
        Combines I and J into one position.
        """
        # Remove duplicates from key and convert to lowercase
        seen = set()
        key_chars = []
        for char in key.lower():
            if char in self.base_alphabet and char not in seen:
                if char == 'j':
                    char = 'i'  # Combine I and J
                if char not in seen:
                    seen.add(char)
                    key_chars.append(char)
        
        # Add remaining alphabet letters
        for char in self.base_alphabet:
            if char == 'j':
                continue  # Skip J since we're using I
            if char not in seen:
                key_chars.append(char)
        
        # Create 5x5 grid
        square = []
        for i in range(5):
            row = key_chars[i*5:(i+1)*5]
            square.append(row)
        
        return square
    
    def find_position(self, char: str, square: List[List[str]]) -> Tuple[int, int]:
        """Find the row and column position of a character in the key square."""
        char = char.lower()
        if char == 'j':
            char = 'i'
        
        for i, row in enumerate(square):
            if char in row:
                return i, row.index(char)
        return -1, -1  # Not found
    
    def decrypt_digraph(self, digraph: str, square: List[List[str]]) -> str:
        """Decrypt a pair of characters using the Playfair rules."""
        if len(digraph) != 2:
            return digraph
        
        char1, char2 = digraph[0].lower(), digraph[1].lower()
        
        # Handle non-alphabetic characters
        if char1 not in self.base_alphabet or char2 not in self.base_alphabet:
            return digraph
        
        row1, col1 = self.find_position(char1, square)
        row2, col2 = self.find_position(char2, square)
        
        if row1 == -1 or row2 == -1:
            return digraph
        
        # Apply Playfair decryption rules
        if row1 == row2:
            # Same row: move left
            new_col1 = (col1 - 1) % 5
            new_col2 = (col2 - 1) % 5
            result = square[row1][new_col1] + square[row2][new_col2]
        elif col1 == col2:
            # Same column: move up
            new_row1 = (row1 - 1) % 5
            new_row2 = (row2 - 1) % 5
            result = square[new_row1][col1] + square[new_row2][col2]
        else:
            # Rectangle: swap columns
            result = square[row1][col2] + square[row2][col1]
        
        # Preserve original case
        if digraph[0].isupper():
            result = result[0].upper() + result[1]
        if digraph[1].isupper():
            result = result[0] + result[1].upper()
        
        return result
    
    def decrypt_with_key(self, text: str, key: str) -> str:
        """Decrypt text using a specific key."""
        if not key:
            return text
        
        square = self.create_key_square(key)
        result = []
        
        # Process text in pairs
        i = 0
        while i < len(text):
            if i + 1 < len(text):
                digraph = text[i:i+2]
                # Only process alphabetic pairs for Playfair
                if digraph[0].isalpha() and digraph[1].isalpha():
                    decrypted = self.decrypt_digraph(digraph, square)
                    result.append(decrypted)
                    i += 2
                else:
                    result.append(text[i])
                    i += 1
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    def decrypt_all_possibilities(self, text: str) -> List[str]:
        """
        Try various keys and return decryptions.
        
        For Playfair cipher, we try common English words as keys.
        """
        decryptions = []
        tried_keys = set()
        
        # Try common keys
        for key in self.common_keys:
            if key not in tried_keys:
                tried_keys.add(key)
                try:
                    decrypted = self.decrypt_with_key(text, key)
                    decryptions.append(decrypted)
                except Exception:
                    continue  # Skip if decryption fails
        
        # Try some single words and short phrases
        additional_keys = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
            'password', 'admin', 'user', 'system', 'data',
            'information', 'message', 'text', 'document'
        ]
        
        for key in additional_keys:
            if key not in tried_keys:
                tried_keys.add(key)
                try:
                    decrypted = self.decrypt_with_key(text, key)
                    decryptions.append(decrypted)
                except Exception:
                    continue
        
        return decryptions
    
    def find_best_key(self, text: str, scorer) -> tuple:
        """
        Find the best key based on scoring.
        Returns (best_key, best_decryption, best_score).
        """
        best_key = ""
        best_score = -1
        best_decryption = text
        
        for key in self.common_keys:
            try:
                decrypted = self.decrypt_with_key(text, key)
                score = scorer.score_text(decrypted)
                
                if score > best_score:
                    best_score = score
                    best_key = key
                    best_decryption = decrypted
            except Exception:
                continue
        
        return best_key, best_decryption, best_score