from nfa import *
from state import *

class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass


class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        symNfa = NFA()
        state0 = State(0)
        state1 = State(1)
        symNfa.addTransition(state0, state1, self.sym)
        # state0.transition = {self.sym:{state1}}
        # state1.transition = {'&':{state1}}
        symNfa.states = [state0, state1]
        # symNfa.accepting = {1:True, 0:False}
        symNfa.is_accepting[0] = False
        symNfa.is_accepting[1] = True
        symNfa.alphabet = [self.sym]
        return symNfa
        pass
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        epsilonNfa = NFA()
        state0 = State(0)
        state1 = State(1)
        epsilonNfa.addTransition(state0, state1, '&')
        epsilonNfa.states = [state0, state1]
        epsilonNfa.is_accepting = {0:False, 1:True}
        epsilonNfa.alphabet = ['&']
        return epsilonNfa
        pass
    pass


class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        leftReg = self.children[0]
        rightReg = self.children[1]
        leftNfa = leftReg.transformToNFA()
        rightNfa = rightReg.transformToNFA()
        endIndex = 0
        ## find the end state
        for num, isAccept in leftNfa.is_accepting.items():
            if isAccept:
                endIndex = num
                break
        # end = leftNfa.states[-1]
        end = leftNfa.states[endIndex]
        start = rightNfa.states[0]

        leftNfa.addTransition(end, start, '&')
        dfaMapping = leftNfa.addStatesFrom(rightNfa)
        # ## change id
        # for index in range(len(rightNfa.states)):
        #     rightNfa.states[index].id = dfaMapping[index]
        leftNfa.is_accepting[end.id] = False
        for num, isAccept in rightNfa.is_accepting.items():
            convertedNum = dfaMapping[num]
            leftNfa.is_accepting[convertedNum] = isAccept
        # leftNfa.alphabet = leftNfa.alphabet | rightNfa.alphabet
        for item in rightNfa.alphabet:
            if item in leftNfa.alphabet:
                continue
            else:
                leftNfa.alphabet.append(item)
        if '&' not in leftNfa.alphabet:
            leftNfa.alphabet.append('&')
        return leftNfa
        pass
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        leftNfa = EpsilonRegex().transformToNFA()
        rightNfa = self.children[0].transformToNFA()
        leftStart = leftNfa.states[0]
        leftEnd = leftNfa.states[-1]
        rightStart = rightNfa.states[0]
        ## find the end state
        endIndex = 0
        for num, isAccept in rightNfa.is_accepting.items():
            if isAccept:
                endIndex = num
                break
        # rightEnd = rightNfa.states[-1]
        rightEnd = rightNfa.states[endIndex]
        ## add transition
        leftNfa.addTransition(leftStart, rightStart, '&')
        rightNfa.addTransition(rightEnd, leftEnd, '&')
        rightNfa.addTransition(rightEnd, rightStart, '&')
        rightNfa.is_accepting[rightEnd.id] = False

        dfaMapping = leftNfa.addStatesFrom(rightNfa)
        for num, isAccept in rightNfa.is_accepting.items():
            convertedNum = dfaMapping[num]
            leftNfa.is_accepting[convertedNum] = isAccept
        # leftNfa.alphabet = leftNfa.alphabet | rightNfa.alphabet
        for item in rightNfa.alphabet:
            if item in leftNfa.alphabet:
                continue
            else:
                leftNfa.alphabet.append(item)
        return leftNfa
        pass
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        leftNfa = EpsilonRegex().transformToNFA()
        rightNfa1 = self.children[0].transformToNFA()
        rightNfa2 = self.children[1].transformToNFA()
        ## get state
        leftStart = leftNfa.states[0]
        leftEnd = leftNfa.states[-1]
        leftStart.transition = {}

        rightStart1 = rightNfa1.states[0]
        rightStart2 = rightNfa2.states[0]
        ## find the end state
        endIndex1 = 0
        for num, isAccept in rightNfa1.is_accepting.items():
            if isAccept:
                endIndex1 = num
                break
        endIndex2 = 0
        for num, isAccept in rightNfa2.is_accepting.items():
            if isAccept:
                endIndex2 = num
                break
        # rightEnd1 = rightNfa1.states[-1]
        # rightEnd2 = rightNfa2.states[-1]
        rightEnd1 = rightNfa1.states[endIndex1]
        rightEnd2 = rightNfa2.states[endIndex2]

        leftNfa.addTransition(leftStart, rightStart1, '&')
        leftNfa.addTransition(leftStart, rightStart2, '&')
        ## nfa
        rightNfa1.addTransition(rightEnd1, leftEnd, '&')
        rightNfa1.is_accepting[rightEnd1.id] = False
        ## nfa2
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
        pass
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()