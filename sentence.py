#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-
import re

class Word:
    def __init__(self, word = '', tags = []):
        '''Initialize a word with a list of tags'''
        self.word = word
        self.tags = tags # list các từ loại (part of speech)

    def __repr__(self):
        '''Nice string representation'''
        return "{0}<{1}>".format(self.word, ','.join(self.tags))

class Sentence:
    def __init__(self, words = []):
        '''A sentence is a list of words'''
        self.words = words

    def __repr__(self):
        '''Nice string representation'''
        return "[{0}]".format(', '.join(str(w) for w in self.words))

    def __len__(self):
        '''Sentence's length'''
        return len(self.words)

    def __getitem__(self, index):
        '''Return a word of a given index'''
        if index >= 0 and index < len(self):
            return self.words[index]
        else:
            return None

    def add_word(self, word):
        '''Add word to sentence'''
        self.words.append(word)

    @staticmethod
    def from_string(text):
        res = Sentence()
        for token in text.split(' '):
            word, tags = token.split('<')
            tags = tags.replace('>','').split(',')
            res.words.append(Word(word, tags))
        return res