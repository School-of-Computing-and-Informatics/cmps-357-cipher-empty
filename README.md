# cmps-357-cipher-empy
Instructions only repo for Fall 2025 PA2

# PA2: Cipher Decryption Assignment

## Overview
This assignment involves writing a program that attempts to decrypt multiple text files using different classical ciphers. You will analyze the results and save the top candidate decryptions.

## Requirements
1. **Input Directory**  
   - All input files will be located in a directory named `INPUT`.  
   - Files will have the extension `.txt`.  
   - Your program should process all `.txt` files in this directory.

2. **Decryption Methods**  
   Implement decryption attempts using the following ciphers:
   - Caesar cipher
   - Vigenère cipher
   - One additional substitution cipher of your choice (for example, Atbash or Monoalphabetic substitution).

3. **Evaluation**  
   - Determine the **10 best decryptions overall** across all input files and ciphers.  
   - Restrict the evaluation alphabet to:
     ```
     a..z A..Z 0..9 . : ; ' ! ? [space]
     ```

4. **Output Directory**  
   - Save the 10 best decryptions as separate files.  
   - Place these files in a directory named `out`.  
   - If the directory does not already exist, create it.

## Expected Behavior
- The program scans all `.txt` files in `INPUT`.
- Each file is decrypted using the specified cipher techniques.
- Candidate decryptions are scored and ranked.
- The top 10 are written to new files inside `out/`.

## Output Format
- Each of the 10 best decryptions should be saved in a separate file, e.g.: `out/input1-decrypt1.txt` `out/input1-decrypt2.txt` ... `out/input1-decrypt10.txt` ...

- Include metadata at the top of each output file, such as:
- Source file name
- Cipher used
- Score/ranking

## Notes
- Ensure your program handles both uppercase and lowercase letters, digits, and the given symbols consistently.
- Design your scoring mechanism to fairly evaluate likelihood of correctness (e.g., letter frequencies, dictionary matching, n-gram analysis).
- The additional substitution cipher you choose should be clearly documented in your code.

---
