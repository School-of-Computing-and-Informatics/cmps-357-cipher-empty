# cmps-357-cipher-empty
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
   Use or implement publicly available decryption methods for the following ciphers:
   - Caesar cipher
   - Vigenère cipher
   - One additional substitution cipher of your choice (for example, Atbash or Monoalphabetic substitution).

3. **Evaluation**  
   - Determine the **10 best decryptions overall** across all input files and ciphers.  
   - Restrict the evaluation alphabet to:
     ```
     a..z A..Z 0..9 . : ; ' ! ? [space]
     ```

4. **Output Format**  
   - Save the 10 best decryptions in a single file named `output.md`.
   - The `output.md` file should be structured as follows:
     - Each **input file** should have a **top-level section** (e.g., `# input1.txt`).
     - Under each input file section, include up to the best decryptions for that file as **second-level sections** (e.g., `## Decryption 1: Caesar Cipher`).
     - For each decryption, include:
       - The cipher used
       - The score or a summary of how well the decryption matches the chosen heuristic (e.g., letter distribution, dictionary matches)
       - The decrypted text itself (in a code block or clearly separated)
   - Example structure:
     ```
     # input1.txt
     ## Decryption 1: Caesar Cipher
     - Cipher: Caesar
     - Score: 0.85 (high match to English letter frequency)
     - Summary: Most words are dictionary valid.
     ```
     ```
     Decrypted text here...
     ```
     ## Decryption 2: Vigenère Cipher
     - Cipher: Vigenère
     - Score: 0.65 (moderate match to English letter frequency)
     - Summary: Some words are valid, some are not.
     ```
     Decrypted text here...
     ```

     # input2.txt
     ... (repeat for remaining input files and decryptions)
     ```

## Expected Behavior
- The program scans all `.txt` files in `INPUT`.
- Each file is decrypted using the specified cipher techniques.
- Candidate decryptions are scored and ranked.
- The top 5 overall are included in `output.md`, grouped by their source input file.

## Output Format (Summary)
- All output is consolidated into a single `output.md` file.
- Organized by input file, with best decryptions as subsections.
- Each decryption includes the cipher used, a score or summary, and the full decrypted text.

## Notes
- Ensure your program handles both uppercase and lowercase letters, digits, and the given symbols consistently.
- Design your scoring mechanism to fairly evaluate likelihood of correctness (e.g., letter frequencies, dictionary matching, n-gram analysis).
- The additional substitution cipher you choose should be clearly documented in your code.

---- Source file name
- Cipher used
- Score/ranking

## Notes
- Ensure your program handles both uppercase and lowercase letters, digits, and the given symbols consistently.
- Design your scoring mechanism to fairly evaluate likelihood of correctness (e.g., letter frequencies, dictionary matching, n-gram analysis).
- The additional substitution cipher you choose should be clearly documented in your code.

---
