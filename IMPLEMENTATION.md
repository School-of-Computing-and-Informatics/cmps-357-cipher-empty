# PA2: Cipher Decryption Implementation

## Overview
This implementation provides a comprehensive cipher decryption program that processes multiple text files and attempts to decrypt them using three different classical ciphers.

## Features Implemented

### Ciphers Supported
1. **Caesar Cipher** (`caesar.py`)
   - Traditional substitution cipher with letter shifting
   - Tries all possible shifts (1-25)
   - Preserves case and non-alphabetic characters
   - Handles both uppercase and lowercase letters

2. **Vigenère Cipher** (`vigenere.py`)  
   - Polyalphabetic substitution cipher using keyword
   - Attempts common English words as keys
   - Includes short letter combinations
   - Uses keyword cycling for encryption/decryption

3. **Playfair Cipher** (`playfair.py`)
   - Digraph substitution cipher operating on letter pairs
   - Creates 5x5 key square (combines I/J)
   - Implements standard Playfair rules (row, column, rectangle)
   - Attempts various common keywords

### Scoring System (`scoring.py`)
The scoring system evaluates decryption quality using multiple criteria:

- **Letter Frequency Analysis (30%)**: Compares against English letter frequencies
- **Dictionary Word Matching (40%)**: Counts valid English words
- **Bigram Analysis (15%)**: Evaluates common letter pairs
- **Trigram Analysis (15%)**: Evaluates common three-letter sequences

Score range: 0.0 to 1.0 (higher is better)

### Main Program (`cipher_decoder.py`)
- Processes all `.txt` files in `INPUT/` directory
- Applies all three ciphers to each file
- Scores and ranks all decryption attempts
- Generates `output.md` with top 5 overall results
- Groups results by source file with detailed scoring

## Usage

1. Place encrypted text files in the `INPUT/` directory
2. Run the program:
   ```bash
   python3 cipher_decoder.py
   ```
3. Check `output.md` for results

## Sample Input Files
- `input1.txt`: Caesar cipher (shift 3) - "the quick brown fox..."
- `input2.txt`: Caesar cipher (shift 7) - "hello world this is..."  
- `input3.txt`: Caesar cipher (shift 5) - "cybersecurity is very..."
- `input4.txt`: Vigenère cipher (key "secret") - "this is a secret message..."

## Output Format
Results are organized by input file with:
- Cipher type used
- Numerical score (0-1 scale)
- Quality summary
- Complete decrypted text

## Technical Notes
- Alphabet handling varies by cipher type
- Caesar cipher works with standard a-z letters
- Vigenère cipher attempts common English keywords
- Playfair cipher uses traditional 5x5 grid approach
- Scoring emphasizes English text patterns and dictionary words