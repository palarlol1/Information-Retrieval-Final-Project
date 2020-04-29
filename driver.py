from classes.data.dataPuller import pull_book_list
from classes.spamMaker import spammer
from classes.recommendationAlgorithms import TFIDF, nearestNeighbor, hybrid
from classes.evaluationAlgorithms import evaluator
import math
import random


TESTTIMES = 50

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
#Now we're going to create the recommendation algorithms
tfidfAlgorithm = TFIDF(data)
#Holding off on the algorithms until we implement guards
#nnAlgorithm = nearestNeighbor(data)
#hybridAlgorithm = hybrid(data)

#Storing in a list for easy access

#Generating our users and their corresponding spamTargeters
users = []
spammers = []
pureRecommendations = []
for i in range(TESTTIMES):
    users.append(user())
    users[-1].likes = [data[key] for key in users[-1].likes]
    spammers.append(spammer(users[-1].likes, i))
    pureRecommendations.append(tfidfAlgorithm.recommend(users[-1].likes))


spammerBooks = []
for attacker in spammers:
    tfidfAlgorithm.add_books(attacker.get_books())
    spammerBooks += [bk.title for bk in attacker.get_books()]

e = evaluator([])

collectedData = []
for i in range(len(users)):
    collectedData.append({})
    unguardedRecommendations = tfidfAlgorithm.recommend(users[i].likes)
    collectedData[-1]["Unguarded Scores"] = e.evaluate(unguardedRecommendations, spammerBooks)
    
    tfidfAlgorithm.guard = "randomizationElement"
    guardedRecommendations = tfidfAlgorithm.recommend(users[i].likes)
    collectedData[-1]["Guarded Randomization Score (SPAM)"] = e.evaluate(guardedRecommendations, spammerBooks)
    collectedData[-1]["Guarded Randomization Score (PURE)"] = e.evaluate(guardedRecommendations, pureRecommendations[i])
    
    tfidfAlgorithm.guard = "probability"
    guardedRecommendations = tfidfAlgorithm.recommend(users[i].likes)
    collectedData[-1]["Guarded Probability Scores (SPAM)"] = e.evaluate(guardedRecommendations, spammerBooks)
    collectedData[-1]["Guarded Probability Score (PURE)"] = e.evaluate(guardedRecommendations, pureRecommendations[i])
    tfidfAlgorithm.guard = False
    

minorKeys = list(collectedData[0]['Unguarded Scores'].keys())
majorKeys = list(collectedData[0].keys())
line = []
with open("exported_data.csv", "w+") as writeFile:
    for major in majorKeys:
        for minor in minorKeys:
            line.append(major + " " + minor)
    
    writeFile.write(",".join(line) + "\n")
            
    for dataSet in collectedData:
        line = []
        for major in majorKeys:
            for minor in minorKeys:
                line.append(str(dataSet[major][minor]))
        writeFile.write(",".join(line) + "\n")
        
