"""
Caesar Cipher implementation for PA2.

The Caesar cipher is a substitution cipher where each letter is shifted
by a fixed number of positions in the alphabet.
"""

from typing import List


class CaesarCipher:
    """Caesar cipher decryption implementation."""
    
    def __init__(self):
        """Initialize the Caesar cipher."""
        # Use only letters for Caesar cipher (traditional)
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet_size = 26
    
    def decrypt_with_shift(self, text: str, shift: int) -> str:
        """Decrypt text using a specific shift value."""
        result = []
        
        for char in text:
            if char.islower() and char in self.alphabet:
                # Handle lowercase letters
                old_pos = self.alphabet.index(char)
                new_pos = (old_pos - shift) % self.alphabet_size
                result.append(self.alphabet[new_pos])
            elif char.isupper() and char.lower() in self.alphabet:
                # Handle uppercase letters
                old_pos = self.alphabet.index(char.lower())
                new_pos = (old_pos - shift) % self.alphabet_size
                result.append(self.alphabet[new_pos].upper())
            else:
                # Keep non-alphabetic characters as-is
                result.append(char)
        
        return ''.join(result)
    
    def decrypt_all_possibilities(self, text: str) -> List[str]:
        """
        Try all possible shifts and return all decryptions.
        
        For Caesar cipher, we try all possible shift values from 0 to alphabet_size-1.
        """
        decryptions = []
        
        for shift in range(1, self.alphabet_size):  # Skip shift=0 as it returns original text
            decrypted = self.decrypt_with_shift(text, shift)
            decryptions.append(decrypted)
        
        return decryptions
    
    def find_best_shift(self, text: str, scorer) -> tuple:
        """
        Find the best shift value based on scoring.
        Returns (best_shift, best_decryption, best_score).
        """
        best_shift = 0
        best_score = -1
        best_decryption = text
        
        for shift in range(1, self.alphabet_size):
            decrypted = self.decrypt_with_shift(text, shift)
            score = scorer.score_text(decrypted)
            
            if score > best_score:
                best_score = score
                best_shift = shift
                best_decryption = decrypted
        
        return best_shift, best_decryption, best_score