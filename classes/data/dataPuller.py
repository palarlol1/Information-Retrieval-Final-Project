# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:35:59 2020

@author: Richard Wang
"""

import pandas as pd
import os

prefix = "C:\\Users\\Richard Wang\\Documents\\UVA 3 - Spring\\Information-Retrieval-Final-Project\\classes\\data\\csvs\\"

class book:
    def __init__(self):
        self.name = ""
        self.tags = []
        self.author = ""

def pull_book_list():
    books = {}
    df = pd.read_csv(prefix + "books.csv")
    for i in range(len(df["book_id"])):
        books[df["book_id"][i]] = book()
        books[df["book_id"][i]].author = df["authors"][i]
        books[df["book_id"][i]].title = df["title"][i]
    tag_map = pd.read_csv(prefix + "tags.csv")
    tag_map = {key : value for (key, value) in zip(tag_map["tag_id"], tag_map["tag_name"])}
    df = pd.read_csv(prefix + "book_tags.csv")
    for i in range(len(df["goodreads_book_id"])):
        books[df["goodreads_book_id"][i]].tags.append(tag_map[df["tag_id"][i]])
    return list(books.values())

def pull_tag_list():
    df = pd.read_csv(prefix + "tags.csv")
    return list(df["tag_name"])
