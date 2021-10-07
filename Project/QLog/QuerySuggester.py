import pickle
import constants
import os
from Models.Query import QueryModel
from QLog.QueryLogParser import QueryLogParser

class QuerySuggester:
    candidateList = None
    categorizedIndex = None
    queryAppears = None
    def __init__(self):
        self.categorizedIndex = {}
        self.queryAppears = 0
    def __indexCandidates(self,query):
        querySet = set(query.split(" "))
        for x in self.candidateList:
            for model in x:
                if(model.query == query):
                    self.queryAppears+=1
                else:
                    currentWordSet = set(model.query.split(" "))
                    intersection = querySet.intersection(currentWordSet)

                    if(len(intersection) == len(query.split(" "))):
                        if(model.query in self.categorizedIndex.keys()):
                             self.categorizedIndex[model.query] += 1
                        else:
                            self.categorizedIndex[model.query] = 1
                       
    def __getRanks(self,query):
        self.__indexCandidates(query)
        ranks = {}
        divisor = 1

        if(self.queryAppears >=1):
            divisor = self.queryAppears
        for key in self.categorizedIndex.keys():
            changedCount = self.categorizedIndex[key]
            rank = changedCount/divisor
            ranks[key] = rank
        sortedDict = dict(sorted(ranks.items(),key=lambda item: item[1],reverse=True))
        keys = list(sortedDict.keys())
        suggestionList = []
        if(len(keys) >= 5):
            suggestionList = keys[0:5]
        else:
            suggestionList = keys[0:len(keys)-1]
        return suggestionList

    def getQuerySuggestions(self, query, range=3):
        parser = QueryLogParser()
        candidates = parser.loadQueryLog(query, range)
        self.candidateList = candidates
        suggestedQueries = self.__getRanks(query)

        return suggestedQueries
        
            


            




                    

                
        

