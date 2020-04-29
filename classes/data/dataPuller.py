# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:35:59 2020

@author: Richard Wang
"""

import pandas as pd
import os

prefix = "C:\\Users\\Richard Wang\\Documents\\UVA 3 - Spring\\Information-Retrieval-Final-Project\\classes\\data\\csvs\\"
path = os.getcwd() + "\\classes\\data\\csvs\\"  # generic path from the current working directory
class book:
    def __init__(self):
        self.title = ""
        self.tags = set()
        self.author = ""
        self.publicationYear = 0

def pull_book_list():
    books = {}
    df = pd.read_csv(path + "\\books.csv")
    for i in range(len(df["book_id"])):
        books[df["book_id"][i]] = book()
        books[df["book_id"][i]].author = df["authors"][i]
        books[df["book_id"][i]].title = df["title"][i]
        books[df["book_id"][i]].publicationYear = df["original_publication_year"][i]
    tag_map = pd.read_csv(path + "\\tags.csv")
    tag_map = {key : value for (key, value) in zip(tag_map["tag_id"], tag_map["tag_name"])}
    df = pd.read_csv(path + "book_tags.csv")
    for i in range(len(df["goodreads_book_id"])):
        books[df["goodreads_book_id"][i]].tags.add(tag_map[df["tag_id"][i]])
    
    for title in books.keys():
        books[title].tags = list(books[title].tags)
        
    return list(books.values())

def pull_tag_list():
    df = pd.read_csv(path + "tags.csv")
    return list(df["tag_name"])
