import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        # s1.transition[sym] = s2
        s1.transition[sym] = {s2}
        pass 
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        for num, isAccept in self.is_accepting.items():
            self.is_accepting[num] = not isAccept
        pass
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        while queue:
            currS, pos = queue.pop(0)
            if pos == len(string):
                # if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                #     return self.is_accepting[currS.id]
                return self.is_accepting[currS.id]
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stat = s.transition[string[pos]]
                        for stat_subset in stat:
                            queue.append((stat_subset, pos+1))
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
        pass
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        # bfs
        statesQueue = [self.states[0]]
        stringQueue = []
        currState = self.states[0]
        visited = []
        while statesQueue:
            currState = statesQueue.pop(0)
            if stringQueue:
                currString = stringQueue.pop(0)
            else:
                currString = ""
            # print(pos)
            if self.is_accepting[currState.id]:
                return currString
            if currState not in visited:
                visited.append(currState)
                for sym, state in currState.transition.items():
                    newString = currString + sym
                    stringQueue.append(newString)
                    for stat in state:
                        statesQueue.append(stat)
        return currString
    pass