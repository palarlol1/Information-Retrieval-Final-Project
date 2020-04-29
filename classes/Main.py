# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 23:00:00 2020

@author: Alec Ross
"""
from collections import defaultdict
from recommendationAlgorithms import TFIDF, hybrid, nearestNeighbor
from evaluationAlgorithms import evaluator
from data.dataPuller import pull_book_list, pull_tag_list
import math

def Main(): # for centralization purposes, currently we have a good API
    eval = evaluator(ModifiedBooks) # initialize all of our needed algorithms
    tfidf = TFIDF(books)
    hybrid_algor = hybrid(books)
    nn = nearestNeighbor(books)

    evaluate_recommendations(eval, tfidf, []) # start processing them
    evaluate_recommendations(eval, hybrid_algor, [])
    evaluate_recommendations(eval, nn, [])

def evaluate_recommendations(Evaluator, Algorithm, likedBooks): # generically evaluates each algorithm
    book_rankings = Algorithm.recommend(likedBooks)
    results = Evaluator.evaluate(book_rankings)
    print(results)

# pull all our data
print("Loading Data")
books = pull_book_list()
print(f"{len(books)} books loaded.")
tags = pull_tag_list()
print(f"{len(tags)} tags loaded.")
print("Finished Loading...")
#
ModifiedBooks = []
#run all of our processing
Main()