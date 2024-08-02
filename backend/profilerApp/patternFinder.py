from collections import defaultdict
import re

class patternFinder:

    def __init__(self, data):
        self.data = data
    
    def tokenize_string(self, s):
        """
        Tokenize the string into patterns of numbers, letters, and special characters.

        """
        imp_spe_char = ['.', ',', '/', '@']
        pattern = re.compile(r'\d+|[a-zA-Z]+|[^a-zA-Z\d]+')
        tokens = pattern.findall(s)
        return ''.join([token if token in imp_spe_char else 
                    '1' * len(token) if token.isdigit() else
                    'A' * len(token) if token.isalpha() else
                    '&' * len(token)
                    for token in tokens])

    def find_patterns(self):
        """
        Find and return patterns in the given list of strings.
        """
        pattern_counts = defaultdict(int)
    
        for item in self.data:
            pattern = self.tokenize_string(item)
            pattern_counts[pattern] += 1
    
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    
        return sorted_patterns
