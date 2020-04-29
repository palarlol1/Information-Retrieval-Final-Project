# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:05:08 2020

@author: Richard Wang
"""
from data.dataPuller import book


class spammer:
    
    def __init__ (self, targets, key):
        self.tags = set()
        self.add_targets(targets)
        self.books = []
        self.key = key
        self.generate_books()
        
    def generate_books(self):
        titles = ["Spam1", "Spam2", "Spam3"]
        publicationDates = [2010, 2012, 2013]
        authors = ["Nimble Thimble", "Nimble Thimble", "Nimble Thimble"]
        for i in range(len(titles)):
            self.books.append(book())
            self.books[-1].title = str(self.key) + " __ " + titles[i]
            self.books[-1].tags = list(self.tags)
            self.books[-1].publicationYear = publicationDates[i]
            self.books[-1].author = authors[i]
            
    def add_targets(self, newTargets):
        for book in newTargets:
            for tag in book.tags:
                self.tags.add(tag)
    
    def get_books(self):
        return self.books
            