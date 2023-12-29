from typing import List
from random import suffle

class Words:
    def __init__(self, list_of_words: List[str]):
        self.list_of_words = list_of_words
        self.guessed = list()
    
    def pick_word(self):
        """Pick the first word (the list of words has been suffled previously)."""
        return self.list_of_words[0]

    def reset(self):
        self.list_of_words = suffle(self.list_of_words+self.guessed)
        self.guessed = list()

    def validate_current_word(self):
        self.guessed.append(self.list_of_words[0])
        self.list_of_words = self.list_of_words[1:]
    
    def pass_current_word(self):
        self.list_of_words = self.list_of_words[1:].append(self.list_of_words[0])
        
