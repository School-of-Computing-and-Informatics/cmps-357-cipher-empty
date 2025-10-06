"""
Vigenère Cipher implementation for PA2.

The Vigenère cipher is a polyalphabetic substitution cipher that uses
a keyword to determine the shift for each character.
"""

from typing import List
import itertools


class VigenereCipher:
    """Vigenère cipher decryption implementation."""
    
    def __init__(self):
        """Initialize the Vigenère cipher."""
        # Use standard alphabet for consistency
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabet_size = 26
        # Common English words that might be used as keys
        self.common_keys = [
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use',
            'key', 'word', 'code', 'cipher', 'secret', 'password', 'test', 'hello', 'world',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
    
    def decrypt_with_key(self, text: str, key: str) -> str:
        """Decrypt text using a specific key."""
        if not key:
            return text
        
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                # Get the shift from the current key character
                key_char = key[key_index % len(key)].lower()
                shift = ord(key_char) - ord('a')
                
                if char.islower():
                    # Handle lowercase letters
                    old_pos = ord(char) - ord('a')
                    new_pos = (old_pos - shift) % self.alphabet_size
                    result.append(chr(ord('a') + new_pos))
                else:
                    # Handle uppercase letters
                    old_pos = ord(char.lower()) - ord('a')
                    new_pos = (old_pos - shift) % self.alphabet_size
                    result.append(chr(ord('a') + new_pos).upper())
                
                key_index += 1
            else:
                # Keep non-alphabetic characters as-is
                result.append(char)
        
        return ''.join(result)
    
    def decrypt_all_possibilities(self, text: str) -> List[str]:
        """
        Try various keys and return decryptions.
        
        For Vigenère cipher, we try:
        1. Common English words as keys
        2. Single characters as keys (reduces to Caesar)
        3. Short letter combinations
        """
        decryptions = []
        tried_keys = set()
        
        # Try common keys
        for key in self.common_keys:
            if key not in tried_keys:
                tried_keys.add(key)
                decrypted = self.decrypt_with_key(text, key)
                decryptions.append(decrypted)
        
        # Try some short combinations for key lengths 2-4
        for key_length in range(2, 5):
            # Generate some combinations - limit to avoid too many possibilities
            letter_combinations = []
            for combo in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=key_length):
                key = ''.join(combo)
                letter_combinations.append(key)
                if len(letter_combinations) >= 20:  # Limit to avoid explosion
                    break
            
            for key in letter_combinations:
                if key not in tried_keys:
                    tried_keys.add(key)
                    decrypted = self.decrypt_with_key(text, key)
                    decryptions.append(decrypted)
        
        return decryptions
    
    def find_key_length(self, text: str) -> List[int]:
        """
        Use Kasiski examination to find likely key lengths.
        This is a simplified version that looks for repeated sequences.
        """
        likely_lengths = []
        
        # Look for repeated trigrams and their distances
        trigrams = {}
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            if trigram.isalpha():  # Only consider alphabetic trigrams
                if trigram in trigrams:
                    distance = i - trigrams[trigram]
                    # Find factors of the distance
                    for length in range(2, min(distance + 1, 21)):  # Check up to length 20
                        if distance % length == 0:
                            likely_lengths.append(length)
                else:
                    trigrams[trigram] = i
        
        # Return most common lengths
        if likely_lengths:
            length_counts = {}
            for length in likely_lengths:
                length_counts[length] = length_counts.get(length, 0) + 1
            
            sorted_lengths = sorted(length_counts.items(), key=lambda x: x[1], reverse=True)
            return [length for length, count in sorted_lengths[:5]]
        
        return [2, 3, 4, 5, 6]  # Default lengths to try
    
    def find_best_key(self, text: str, scorer) -> tuple:
        """
        Find the best key based on scoring.
        Returns (best_key, best_decryption, best_score).
        """
        best_key = ""
        best_score = -1
        best_decryption = text
        
        for key in self.common_keys:
            decrypted = self.decrypt_with_key(text, key)
            score = scorer.score_text(decrypted)
            
            if score > best_score:
                best_score = score
                best_key = key
                best_decryption = decrypted
        
        return best_key, best_decryption, best_score