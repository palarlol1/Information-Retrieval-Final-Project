# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:58:29 2020

@author: Richard Wang
"""
import math

class evaluator:
    def __init__(self, spamBooks):
        self.spam = set()
        for book in spamBooks:
            self.spam.add(book)
                   
    
    def precisionK(self, rankings, k, relDocs):
        precision = []
        countRel = 0
        for i in range(min(len(rankings), k)):
            if rankings[i] in relDocs:
                countRel += 1
                precision.append((countRel / (i + 1)))
        
        return (sum(precision) / len(precision))
    
    
    def rr(self, rankings, relDocs):
        for i in range(len(rankings)):
            if rankings[i] in relDocs:
                return (1 / (i + 1))
            
    def average_precision(self, rankings, relDocs):
        countRel = 0
        precision = 0
        for i in range(len(rankings)):
            if rankings[i] in relDocs:
                countRel += 1
                precision += (countRel / (i + 1))
        return (precision / countRel)
                
            
    #Will simply be using dcg, because we are not comparing between separate queries,
    #We simply want to see how highly the spam documents are mapped.
    def dcg(self, rankings, relDocs):
        dcg = 0
        for i in range(len(rankings)):
            if rankings[i] in relDocs:
                dcg += (1 / math.log(i + 2)) #Since i starts at 0 for us, but we need it to start at 1
        return dcg
    
    def evaluate(self, rankings, relDocs = False):
        if not relDocs:
            relDocs = self.spam
        answer = {}
        answer["average precision"] = self.average_precision( rankings, relDocs)
        answer["precision @ 15"] = self.precisionK( rankings, 15 , relDocs)
        answer["reciprocal rank"] = self.rr( rankings, relDocs)
        answer["dcg"] = self.dcg( rankings, relDocs)
        return answer        