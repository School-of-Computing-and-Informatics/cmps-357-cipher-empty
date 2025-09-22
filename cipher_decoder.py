#!/usr/bin/env python3
"""
PA2: Cipher Decryption Assignment
Main program for decrypting multiple text files using classical ciphers.

This program implements Caesar, Vigenère, and Playfair cipher decryption
with scoring mechanisms to find the best decryptions.
"""

import os
import glob
from typing import List, Tuple, Dict
from dataclasses import dataclass

from caesar import CaesarCipher
from vigenere import VigenereCipher
from playfair import PlayfairCipher
from scoring import TextScorer


@dataclass
class DecryptionResult:
    """Container for decryption results."""
    filename: str
    cipher_name: str
    decrypted_text: str
    score: float
    summary: str


class CipherDecoder:
    """Main class for cipher decryption operations."""
    
    def __init__(self):
        """Initialize the cipher decoder with available ciphers."""
        self.ciphers = {
            'Caesar': CaesarCipher(),
            'Vigenère': VigenereCipher(),
            'Playfair': PlayfairCipher()
        }
        self.scorer = TextScorer()
        self.valid_alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:;\'!? ')
    
    def process_input_files(self, input_dir: str = 'INPUT') -> List[DecryptionResult]:
        """Process all .txt files in the input directory."""
        results = []
        
        if not os.path.exists(input_dir):
            print(f"Warning: Input directory '{input_dir}' does not exist.")
            return results
        
        txt_files = glob.glob(os.path.join(input_dir, '*.txt'))
        
        if not txt_files:
            print(f"Warning: No .txt files found in '{input_dir}' directory.")
            return results
        
        for file_path in txt_files:
            filename = os.path.basename(file_path)
            print(f"Processing {filename}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    encrypted_text = f.read().strip()
                
                # Filter text to only include valid alphabet characters
                filtered_text = self._filter_text(encrypted_text)
                
                # Try each cipher on this file
                file_results = self._decrypt_with_all_ciphers(filename, filtered_text)
                results.extend(file_results)
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        
        return results
    
    def _filter_text(self, text: str) -> str:
        """Filter text to only include valid alphabet characters."""
        # Keep the text as-is for now, let individual ciphers handle their own alphabets
        return text.strip()
    
    def _decrypt_with_all_ciphers(self, filename: str, encrypted_text: str) -> List[DecryptionResult]:
        """Decrypt text with all available ciphers and return results."""
        results = []
        
        for cipher_name, cipher in self.ciphers.items():
            try:
                # Get all possible decryptions for this cipher
                decryptions = cipher.decrypt_all_possibilities(encrypted_text)
                
                # Score each decryption
                for decrypted_text in decryptions:
                    score = self.scorer.score_text(decrypted_text)
                    summary = self.scorer.get_summary(decrypted_text, score)
                    
                    result = DecryptionResult(
                        filename=filename,
                        cipher_name=cipher_name,
                        decrypted_text=decrypted_text,
                        score=score,
                        summary=summary
                    )
                    results.append(result)
                    
            except Exception as e:
                print(f"Error decrypting {filename} with {cipher_name}: {e}")
        
        return results
    
    def get_top_decryptions(self, results: List[DecryptionResult], top_n: int = 5) -> List[DecryptionResult]:
        """Get the top N decryptions based on score."""
        return sorted(results, key=lambda x: x.score, reverse=True)[:top_n]
    
    def generate_output_md(self, results: List[DecryptionResult], output_file: str = 'output.md'):
        """Generate the output markdown file with results grouped by input file."""
        # Group results by filename
        results_by_file = {}
        for result in results:
            if result.filename not in results_by_file:
                results_by_file[result.filename] = []
            results_by_file[result.filename].append(result)
        
        # Sort results within each file by score
        for filename in results_by_file:
            results_by_file[filename].sort(key=lambda x: x.score, reverse=True)
        
        # Generate markdown content
        with open(output_file, 'w', encoding='utf-8') as f:
            for filename in sorted(results_by_file.keys()):
                f.write(f"# {filename}\n\n")
                
                file_results = results_by_file[filename]
                for i, result in enumerate(file_results, 1):
                    f.write(f"## Decryption {i}: {result.cipher_name} Cipher\n")
                    f.write(f"- Cipher: {result.cipher_name}\n")
                    f.write(f"- Score: {result.score:.3f}\n")
                    f.write(f"- Summary: {result.summary}\n")
                    f.write("```\n")
                    f.write(result.decrypted_text)
                    f.write("\n```\n\n")
                
                f.write("\n")
        
        print(f"Output written to {output_file}")


def main():
    """Main function to run the cipher decoder."""
    print("PA2: Cipher Decryption Assignment")
    print("=" * 40)
    
    decoder = CipherDecoder()
    
    # Process input files
    all_results = decoder.process_input_files()
    
    if not all_results:
        print("No results to process. Please check your INPUT directory and files.")
        return
    
    # Get top 5 decryptions overall
    top_results = decoder.get_top_decryptions(all_results, top_n=5)
    
    # Generate output
    decoder.generate_output_md(top_results)
    
    print(f"\nProcessed {len(all_results)} total decryptions")
    print(f"Top 5 decryptions saved to output.md")


if __name__ == "__main__":
    main()