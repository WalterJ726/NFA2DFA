from state import *
from regex import *
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        # print(sym)
        if sym in s1.transition:
            # print(1)
            s1.transition[sym].add(s2)
        else:
            s1.transition[sym] = {s2}
        pass
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        leftNfa_length = len(self.states)
        dfaMapping = {}
        for i in range(len(nfa.states)):
            nfa.states[i].id = leftNfa_length + i
            self.states.append(nfa.states[i])
            dfaMapping[i] = leftNfa_length + i
        return dfaMapping
        pass
    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    # def epsilonClose(self, ns):
    #     states = []
    #     for n in ns:
    #         for sym, nn in self.states[n.id].transition.items():  
    #             if sym == '&':
    #                 for s in nn:
    #                     states.append(s)
    #     return states
    #     pass
    def epsilonClose(self, ns):
        ans = ns
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():  
                if sym == '&':
                    for s in nn:
                        # print(sym)
                        # print(nn)
                        if s not in ans:
                            ans.append(s)   
        if ans != ns:
            return self.epsilonClose(ans)
        else: 
            return ans
        pass

    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop(0)
            visited.append((currS,pos))
            # print(pos)
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    if (n, pos) not in visited:
                        queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    # print(string[pos], s.transition)
                    if string[pos] in s.transition:
                        # print(string[pos], s.id)
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            if (n, pos) not in visited:
                                queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass


# union funtion
# It takes two NFAs and return the NFA which is the union of the two NFAs
def unionNfa(nfa1, nfa2):
        ## create epsilon nfa
        leftNfa = NFA()
        state0 = State(0)
        state1 = State(1)
        leftNfa.addTransition(state0, state1, '&')
        leftNfa.states = [state0, state1]
        leftNfa.is_accepting = {0:False, 1:True}
        leftNfa.alphabet = ['&']

        ## 
        rightNfa1 = nfa1
        rightNfa2 = nfa2
        ## get state
        leftStart = leftNfa.states[0]
        leftEnd = leftNfa.states[-1]
        leftStart.transition = {}

        rightStart1 = rightNfa1.states[0]
        rightStart2 = rightNfa2.states[0]
        ## find the end state
        endIndex1 = []
        for num, isAccept in rightNfa1.is_accepting.items():
            if isAccept:
                endIndex1.append(num)
        endIndex2 = []
        for num, isAccept in rightNfa2.is_accepting.items():
            if isAccept:
                endIndex2.append(num)
        # rightEnd1 = rightNfa1.states[-1]
        # rightEnd2 = rightNfa2.states[-1]

        leftNfa.addTransition(leftStart, rightStart1, '&')
        leftNfa.addTransition(leftStart, rightStart2, '&')
        ## nfa
        for idx1 in endIndex1:
            rightEnd1 = rightNfa1.states[idx1]
            rightNfa1.addTransition(rightEnd1, leftEnd, '&')
            rightNfa1.is_accepting[rightEnd1.id] = False
        ## nfa2
        for idx2 in endIndex2:
            rightEnd2 = rightNfa2.states[idx2]
            rightNfa2.addTransition(rightEnd2, leftEnd, '&')
            rightNfa2.is_accepting[rightEnd2.id] = False
        ## add the first regular expression
        dfaMapping = leftNfa.addStatesFrom(rightNfa1)
        for num, isAccept in rightNfa1.is_accepting.items():
            convertedNum = dfaMapping[num]
            leftNfa.is_accepting[convertedNum] = isAccept
        # leftNfa.alphabet = leftNfa.alphabet | rightNfa.alphabet
        for item in rightNfa1.alphabet:
            if item in leftNfa.alphabet:
                continue
            else:
                leftNfa.alphabet.append(item)
        # add the second regular expression
        dfaMapping = leftNfa.addStatesFrom(rightNfa2)
        for num, isAccept in rightNfa2.is_accepting.items():
            convertedNum = dfaMapping[num]
            leftNfa.is_accepting[convertedNum] = isAccept
        # leftNfa.alphabet = leftNfa.alphabet | rightNfa.alphabet
        for item in rightNfa2.alphabet:
            if item in leftNfa.alphabet:
                continue
            else:
                leftNfa.alphabet.append(item)
        return leftNfa

