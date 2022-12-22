import copy
from regex import *
from state import * 
from nfa import *
from dfa import *

# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    ans = DFA()
    ## get episilon closure for every state
    epsilonList = []
    for stat in nfa.states:
        curEpsilon = []
        # curEpsilon.append(stat)
        # curEpsilon.extend(nfa.epsilonClose([stat]))
        curEpsilon = nfa.epsilonClose([stat])
        epsilonList.append(curEpsilon)
    currS = epsilonList[0]
    queue = [(currS, 0)]
    index = 0
    isVisitedState = []
    isVisitedID = []
    ans.states.append(State(index))
    ## change the accepting state
    acceptingFlag = False
    for num, isAccept in nfa.is_accepting.items():
        if nfa.states[num] in currS and isAccept:
            acceptingFlag = True
    ans.is_accepting[index] = acceptingFlag
    ## bfs
    while queue:
        currS, pos = queue.pop(0)
        for sym in nfa.alphabet:
            if sym == '&':
                continue
            nextS = []
            for s in currS:
                if sym in s.transition:
                    stats = s.transition[sym]
                    for s1 in stats:
                        nextS.append(s1)
            # nextS.extend(nfa.epsilonClose(nextS))
            nextS = nfa.epsilonClose(nextS)
            if nextS not in isVisitedState:
                index = index + 1
                isVisitedState.append(nextS)
                isVisitedID.append(index)
                desState = State(index)
                ans.states.append(desState)
                ans.addTransition(ans.states[pos], desState, sym)  
                ## change the is_accpeting
                acceptingFlag = False
                for num, isAccept in nfa.is_accepting.items():
                    if nfa.states[num] in nextS and isAccept:
                        acceptingFlag = True
                ans.is_accepting[index] = acceptingFlag
                queue.append((nextS, index))
            else:
                ## find the des state id
                for i in range(len(isVisitedState)):
                    if nextS == isVisitedState[i]:
                        nextStateID = isVisitedID[i]
                        ans.addTransition(ans.states[pos], ans.states[nextStateID], sym)  
    ## change the is_accepting
    # ans.is_accepting[{}] = False
    for cha in nfa.alphabet:
        if cha != '&':
            ans.alphabet.append(cha)
    return ans
                
                


    pass
# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa = NFA()
    # for stat in dfa.states:
    #     for sym, s in stat.transition.items():
    #         newStat = State(stat.id)
    #         newStat.transition[sym] = {s}
    #         nfa.states.append((newStat))

    nfa.states = dfa.states
    nfa.is_accepting = dfa.is_accepting
    nfa.alphabet = dfa.alphabet
    return nfa
    pass
def draw(nfa):
    size = len(nfa.states)
    t = 0
    currS = nfa.states[nfa.startS]
    queue = [currS]
    isVisited = []
    while queue:
        currS = queue.pop(0)
        if currS not in isVisited:
            isVisited.append(currS)
            for sym in nfa.alphabet:
                if sym in currS.transition:
                    stats = currS.transition[sym]
                    for stat in stats:
                        print("from:{} {} through {} -> {} ac:{}".format(currS.id, nfa.is_accepting[currS.id], sym, stat.id, nfa.is_accepting[stat.id]))
                        queue.append(stat)
    print()
# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    re1_nfa = re1.transformToNFA()
    re2_nfa = re2.transformToNFA()
    # draw(re1_nfa)
    # draw(re2_nfa)
    re1_dfa = nfaToDFA(re1_nfa)
    re2_dfa = nfaToDFA(re2_nfa)
    # draw(re1_dfa)
    # draw(re2_dfa)
    re1_dfa.complement()
    # draw(re1_dfa)
    re1_dfa2Nfa = dfaToNFA(re1_dfa)
    # draw(re1_dfa2Nfa)
    re1_re2_Union = unionNfa(re1_dfa2Nfa, re2_nfa)
    # draw(re1_re2_Union)
    re1_re2_Union_DFA = nfaToDFA(re1_re2_Union)
    re1_re2_Union_DFA.complement()
    draw(re1_re2_Union_DFA)
    print(re1_re2_Union_DFA.shortestString())
    if re1_re2_Union_DFA != None:
        return False
    else:
        return True

    return re1_re2_Union_DFA
    pass



if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(nfa, s, expected):
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA1(strRe, s, expected):
        # test your dfa conversion
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
    pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass

    # # test your NFA:
    # testNFA('&', '', True) 
    # testNFA('a', '', False)
    # testNFA('a', 'a', True)
    # testNFA('a', 'ab', False)
    # testNFA('ab', 'ab', True)
    # testNFA('ab', 'aba', False)
    # testNFA('a*', '', True)
    # testNFA('a*', 'a', True)
    # testNFA('a*', 'aaa', True)
    # testNFA('a*', 'aab', False)
    # testNFA('a|b', '', False)
    # testNFA('a|b', 'a', True)
    # testNFA('a|b', 'b', True)
    # testNFA('a|b', 'ab', False)
    # testNFA('ab|cd', '', False)
    # testNFA('ab|cd', 'ab', True)
    # testNFA('ab|cd', 'cd', True)
    # testNFA('ab|cd', 'ac', False)
    # testNFA('ab|cd', 'aa', False)
    # testNFA('ab|cd*', '', False)
    # testNFA('ab|cd*', 'c', True)
    # testNFA('ab|cd*', 'cd', True)
    # testNFA('ab|cd*', 'cddddddd', True)
    # testNFA('ab|cd*', 'ab', True)
    # testNFA('ab|cd*', 'ac', False)
    # testNFA('((ab)|(cd))*', '', True)
    # testNFA('((ab)|(cd))*', 'ab', True)
    # testNFA('((ab)|(cd))*', 'cd', True)
    # testNFA('((ab)|(cd))*', 'abab', True)
    # testNFA('((ab)|(cd))*', 'abcd', True)
    # testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    # # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', False)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    
    # # testDFA
    # testDFA1('&', '', True)
    # testDFA1('a', '', False)
    # testDFA1('a', 'a', True)
    # testDFA1('a', 'ab', False)
    # testDFA1('ab', 'ab', True)
    # testDFA1('ab', 'aba', False)
    # testDFA1('a*', '', True)
    # testDFA1('a*', 'a', True)
    # testDFA1('a*', 'aaa', True)
    # testDFA1('a*', 'aab', False)
    # testDFA1('a|b', '', False)
    # testDFA1('a|b', 'a', True)
    # testDFA1('a|b', 'b', True)
    # testDFA1('a|b', 'ab', False)
    # testDFA1('ab|cd', '', False)
    # testDFA1('ab|cd', 'ab', True)
    # testDFA1('ab|cd', 'cd', True)
    # testDFA1('ab|cd', 'ac', False)
    # testDFA1('ab|cd', 'aa', False)
    # testDFA1('ab|cd*', '', False)
    # testDFA1('ab|cd*', 'c', True)
    # testDFA1('ab|cd*', 'cd', True)
    # testDFA1('ab|cd*', 'cddddddd', True)
    # testDFA1('ab|cd*', 'ab', True)
    # testDFA1('ab|cd*', 'ac', False)
    # testDFA1('((ab)|(cd))*', '', True)
    # testDFA1('((ab)|(cd))*', 'ab', True)
    # testDFA1('((ab)|(cd))*', 'cd', True)
    # testDFA1('((ab)|(cd))*', 'abab', True)
    # testDFA1('((ab)|(cd))*', 'abcd', True)
    # testDFA1('((ab)|(cd))*', 'cdcdabcd', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    # # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', False)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    # testDFA1('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)

    # testEquivalence('a', 'a', True)
    # testEquivalence('ab', 'ab', True)
    # testEquivalence('a*', 'a*', True)
    # testEquivalence('a|b', 'a|b', True)
    # testEquivalence('ab|cd', 'ab|cd', True)
    # testEquivalence('ab|cd*', 'ab|cd*', True)
    # testEquivalence('((ab)|(cd))*', '((ab)|(cd))*', True)
    # testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', True)
    
    
    testEquivalence('a', 'ab', False)

    pass
    
