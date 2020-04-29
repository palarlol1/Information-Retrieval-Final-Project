from classes.data.dataPuller import pull_book_list
from classes.spamMaker import spammer
from classes.recommendationAlgorithms import TFIDF, nearestNeighbor, hybrid
import math
import random


TESTTIMES = 1

class user:
    def __init__(self):
        self.likes = [random.randint(0, 9999) for i in range(random.randint(50,75))]
        

#Start by pulling all the books into an array format - this is 10k samples
data = pull_book_list()

'''
Threat Model:
    We are handling an attacker who has a bad book series they want recommended.
    We will assume they have access to a list of books that have been "liked" by a user
    We will assume the attacker will modify of the books they wish to push by copying the tags
        of the books that John has 
    In the interest of fairness, we will be randomizing the user's liked books. 
    This way, we can also run multiple trials
'''

#Generating our users and their corresponding spamTargeters
users = []
spammers = []
for i in range(TESTTIMES):
    users.append(user())
    users[-1].likes = [data[key] for key in users[-1].likes]
    spammers.append(spammer(users[-1].likes, i))


#Now we're going to create the recommendation algorithms
tfidfAlgorithm = TFIDF(data)
nnAlgorithm = nearestNeighbor(data)
hybridAlgorithm = hybrid(data)

#Storing in a list for easy access
algorithms = [tfidfAlgorithm, nnAlgorithm, hybridAlgorithm]

for attacker in spammers:
    for algo in algorithms:
        algo.add_books(attacker.get_books())
        
for algo in algorithms:
    print(algo.recommend(users[0].likes))