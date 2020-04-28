# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:37:11 2020

@author: Richard Wang
"""
from collections import defaultdict
from data.dataPuller import pull_book_list, pull_tag_list
import math

'''
Simple content based recommendation System
'''

numResults = 100

class TFIDF:
    def __init__(self, bookList):
        self.invertedIndex = defaultdict(set)
        self.dfTracker = defaultdict(int)
        self.numDocs = 0
        self.add_books(bookList)
    
    #Puts new books into the Inverted Index
    def add_books(self, books):
        for book in books:
            self.numDocs += 1
            for tag in book.tags:
                self.invertedIndex[tag].add(book.title)
                self.dfTracker[tag] += 1       
                
    def recommend(self, likedBooks):
        tagWeights = defaultdict(int) #Counts the number of times a term appears - we can use this to weight tags
        bookWeights = defaultdict(int) #Map docs to the number of tags they satisfy
        tagsToCheck = set()
        ignoreBooks = set()
        for book in likedBooks:
            ignoreBooks.add(book) #Keep track of the books the user has liked
            for tag in book.tags:
                tagWeights[tag] += 1
                tagsToCheck.add(tag)
        
        for tag in tagsToCheck:
            for book in self.invertedIndex[tag]:
                tfidf = 1 * math.log((1 + self.numDocs) / (1 + self.dfTracker[tag])) + 1
                '''
                Because we are using tags, our tf will always be set at 1. As a meaningful substitute,
                we will be using the number of times one tag appears in the list of liked books.For example
                if there are 2 books of the fantasy genre, we will multiply the value by 2.
                '''
                bookWeights[book] += (tagWeights[tag] * tfidf)
        
        for toDelete in ignoreBooks:
            del bookWeights[toDelete.title] #Remove already liked books
        
        ranking = list(bookWeights.keys())
        ranking.sort(key = lambda a : bookWeights[a], reverse = True)
        
        return ranking[:min(numResults, len(ranking) - 1)]
    

class nearestNeighbor:
    def __init__(self, bookList):
        self.tagRef = {} #gives an index to each tag we find
        self.bookData = {} #We're going to store the individual vectors of the books here
        #Using one hot encoding
        tagsList = pull_tag_list()
        for i in range(len(tagsList)):
            self.tagRef[tagsList[i]]= i
        self.add_books(bookList)
    
    def add_books(self, books):
        for book in books:
            self.bookData[book.title] = [0] * len(self.tagRef)
            for tag in book.tags:
                self.bookData[book.title][self.tagRef[tag]] = 1
    
    def recommend(self, likedBooks):
        def cosine_similarity(v1, v2):
            ans = 0
            norm1, norm2 = 0, 0
            for i in range(len(v1)):
                ans += (v1[i] * v2[i]) #handling dot product
                norm1 += v1[i]**2 #We can probably simplify this but I don't want to risk it.
                norm2 += v2[i]**2
                
            denominator = (norm1**.5 * norm2**.5)
                
            if (denominator == 0):
                return float('-inf')
            else:
                return (ans/denominator)
        
        similarityScores = defaultdict(int)
        
        toIgnore = set()
        for book in likedBooks:
            toIgnore.add(book.title)
            
        for book in likedBooks:
            v1 = self.bookData[book.title]
            for key in self.bookData.keys():
                if key not in toIgnore:
                    v2 = self.bookData[key]
                    similarity = cosine_similarity(v1, v2)
                    similarityScores[key] += similarity
        ranking = list(similarityScores.keys())
        ranking.sort(key = lambda a : similarityScores[a], reverse = True)   
        return ranking[:min(numResults, len(ranking) - 1)]

class matrixFactorizationL:
    def __init__(self, bookList):
    
