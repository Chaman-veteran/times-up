from typing import List
from random import shuffle

class EndOfWords(Exception):
    pass 

class Words:
    def __init__(self, list_of_words: List[str]):
        self.list_of_words = list_of_words
        self.guessed = list()

    def nb_remaining_words(self):
        return len(self.list_of_words)
    
    def pick_word(self):
        """Pick the first word (the list of words has been suffled previously)."""
        if len(self.list_of_words) > 0:
            return self.list_of_words[0]
        else:
            raise EndOfWords

    def reset(self):
        self.list_of_words = self.list_of_words+self.guessed
        self.guessed = list()
        shuffle(self.list_of_words)

    def validate_current_word(self):
        self.guessed.append(self.list_of_words[0])
        self.list_of_words = self.list_of_words[1:]
    
    def pass_current_word(self):
        self.list_of_words = self.list_of_words[1:] + [self.list_of_words[0]]
        
