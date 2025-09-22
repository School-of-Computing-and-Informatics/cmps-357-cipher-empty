"""
Text scoring module for PA2.

This module provides scoring mechanisms to evaluate the quality of decrypted text.
It uses letter frequency analysis and basic dictionary matching.
"""

import re
from collections import Counter
from typing import Dict


class TextScorer:
    """Text scoring class for evaluating decryption quality."""
    
    def __init__(self):
        """Initialize the text scorer with English language statistics."""
        # English letter frequencies (approximate percentages)
        self.english_freq = {
            'a': 8.12, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.02, 'f': 2.23,
            'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
            'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
            's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
            'y': 1.97, 'z': 0.07
        }
        
        # Common English words for dictionary matching
        self.common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'that', 'with',
            'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been',
            'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just',
            'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them',
            'well', 'were', 'what', 'year', 'work', 'world', 'about', 'after',
            'again', 'before', 'could', 'first', 'great', 'little', 'other',
            'right', 'should', 'these', 'think', 'where', 'would', 'because',
            'between', 'through', 'without', 'another', 'around', 'during',
            'important', 'information', 'system', 'government', 'company', 'number',
            'people', 'water', 'state', 'place', 'school', 'house', 'student',
            'group', 'country', 'problem', 'business', 'service', 'program',
            'question', 'different', 'social', 'small', 'large', 'public',
            'local', 'possible', 'available', 'national', 'economic', 'political'
        }
        
        # Common English bigrams and trigrams
        self.common_bigrams = {
            'th', 'he', 'in', 'er', 'an', 're', 'ed', 'nd', 'on', 'en',
            'at', 'ou', 'it', 'is', 'or', 'ti', 'hi', 'st', 'ar', 'te'
        }
        
        self.common_trigrams = {
            'the', 'and', 'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for',
            'ent', 'ion', 'ter', 'was', 'you', 'ith', 'ver', 'all', 'wit'
        }
    
    def score_text(self, text: str) -> float:
        """
        Score text based on multiple criteria.
        Returns a score between 0 and 1, where 1 is most English-like.
        """
        if not text:
            return 0.0
        
        # Normalize text for analysis
        normalized_text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        
        if not normalized_text:
            return 0.0
        
        # Calculate component scores
        freq_score = self._calculate_frequency_score(normalized_text)
        word_score = self._calculate_word_score(normalized_text)
        bigram_score = self._calculate_bigram_score(normalized_text)
        trigram_score = self._calculate_trigram_score(normalized_text)
        
        # Weighted combination of scores
        total_score = (
            freq_score * 0.3 +      # Letter frequency: 30%
            word_score * 0.4 +      # Dictionary words: 40%
            bigram_score * 0.15 +   # Bigrams: 15%
            trigram_score * 0.15    # Trigrams: 15%
        )
        
        return min(total_score, 1.0)
    
    def _calculate_frequency_score(self, text: str) -> float:
        """Calculate score based on letter frequency analysis."""
        # Count letter frequencies
        letter_counts = Counter(c for c in text if c.isalpha())
        total_letters = sum(letter_counts.values())
        
        if total_letters == 0:
            return 0.0
        
        # Calculate chi-squared statistic
        chi_squared = 0.0
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            observed = letter_counts.get(letter, 0)
            expected = (self.english_freq[letter] / 100.0) * total_letters
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        # Convert chi-squared to a score (lower chi-squared = higher score)
        # Use empirical scaling - typical chi-squared values for random text are much higher
        score = max(0, 1 - (chi_squared / 1000.0))
        return min(score, 1.0)
    
    def _calculate_word_score(self, text: str) -> float:
        """Calculate score based on dictionary word matching."""
        words = text.split()
        if not words:
            return 0.0
        
        valid_words = sum(1 for word in words if word.lower() in self.common_words)
        return valid_words / len(words)
    
    def _calculate_bigram_score(self, text: str) -> float:
        """Calculate score based on common English bigrams."""
        text_clean = ''.join(c for c in text if c.isalpha())
        if len(text_clean) < 2:
            return 0.0
        
        bigrams = [text_clean[i:i+2] for i in range(len(text_clean) - 1)]
        if not bigrams:
            return 0.0
        
        common_bigrams = sum(1 for bigram in bigrams if bigram in self.common_bigrams)
        return common_bigrams / len(bigrams)
    
    def _calculate_trigram_score(self, text: str) -> float:
        """Calculate score based on common English trigrams."""
        text_clean = ''.join(c for c in text if c.isalpha())
        if len(text_clean) < 3:
            return 0.0
        
        trigrams = [text_clean[i:i+3] for i in range(len(text_clean) - 2)]
        if not trigrams:
            return 0.0
        
        common_trigrams = sum(1 for trigram in trigrams if trigram in self.common_trigrams)
        return common_trigrams / len(trigrams)
    
    def get_summary(self, text: str, score: float) -> str:
        """Generate a human-readable summary of the text quality."""
        if score >= 0.8:
            return "Excellent match to English text patterns"
        elif score >= 0.6:
            return "Good match to English text patterns"
        elif score >= 0.4:
            return "Moderate match to English text patterns"
        elif score >= 0.2:
            return "Poor match to English text patterns"
        else:
            return "Very poor match to English text patterns"
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Provide detailed analysis of text quality.
        Returns a dictionary with individual component scores.
        """
        normalized_text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        
        return {
            'frequency_score': self._calculate_frequency_score(normalized_text),
            'word_score': self._calculate_word_score(normalized_text),
            'bigram_score': self._calculate_bigram_score(normalized_text),
            'trigram_score': self._calculate_trigram_score(normalized_text),
            'overall_score': self.score_text(text)
        }