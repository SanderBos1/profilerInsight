from collections import defaultdict
import re

import pandas as pd

class PatternFinder:
    """
    The PatternFinder class, finds patterns in a list of strings.
    
    Parameters:
        - N / A
        
    """
    def __init__(self):
        pass
    
    def tokenize_string(self, s):
        """
        Tokenize the string into patterns of numbers, letters, and special characters.

        """
        imp_spe_char = ['.', ',', '/', '@']

        returned_pattern = ""
        for token in s:
            if token in imp_spe_char:
                returned_pattern = returned_pattern + token
            elif token.isdigit():
                returned_pattern = returned_pattern + "1"
            elif token.isalpha():
                returned_pattern = returned_pattern + "A"
            else:
                returned_pattern = returned_pattern + "&"
        return returned_pattern

    def find_patterns(self, data:pd.Series) -> list:
        """
        Find and return patterns in the given list of strings.

        Args:
            - data (list): The list of strings to find patterns in.
        """
        pattern_counts = defaultdict(int)
    
        for item in data:
            pattern = self.tokenize_string(item)
            pattern_counts[pattern] += 1
    
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    
        return sorted_patterns
