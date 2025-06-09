from syntax_tree import SyntaxTree
from collections import deque
import copy

class DFAState:
    def __init__(self, id_set: set, id_num: int, is_final: bool):
        self.id_set = id_set             
        self.id = id_num                   
        self.transitions = {}              
        self.is_final = is_final



class DFA:
    def __init__(self, syntax_tree: SyntaxTree):
        print('Передан syntax_tree:', syntax_tree)
        print('root:', getattr(syntax_tree, "root", None))
        if syntax_tree is None or syntax_tree.root is None:
            raise ValueError("Регулярное выражение не скомпилировано: дерево разбора отсутствует.")
        self.alphabet = syntax_tree.alphabet - {'$'}  # исключаем ε
        self.terminal = syntax_tree.id_counter - 1    # позиция служебного символа '#'
        self.followpos = syntax_tree.followpos
        self.leaves = syntax_tree.leaves             
        self.states = []
        self.state_map = {} 
        self.build_dfa(syntax_tree.root)

    def build_dfa(self, root):
        start_set = root.firstpos
        id_counter = 1
        start_state = DFAState(start_set, id_counter, self.terminal in start_set)
        self.states.append(start_state)
        self.state_map[frozenset(start_set)] = start_state

        queue = deque([start_state])

        while queue:
            current = queue.popleft()
            for symbol in self.alphabet:
                u = set()
                for pos in current.id_set:
                    if self.leaves.get(pos) == symbol:  
                        u |= self.followpos[pos]
                if not u:
                    continue
                frozen_u = frozenset(u)
                if frozen_u not in self.state_map:
                    id_counter += 1
                    new_state = DFAState(u, id_counter, self.terminal in u)
                    self.states.append(new_state)
                    self.state_map[frozen_u] = new_state
                    queue.append(new_state)
                current.transitions[symbol] = self.state_map[frozen_u]

    def match(self, s: str) -> bool:
        current = self.states[0]
        for c in s:
            if c not in current.transitions:
                return False
            current = current.transitions[c]
        return current.is_final
    
    def to_regex(self):
        states = self.states
        n = len(states)
        id2idx = {s.id: i for i, s in enumerate(states)}

        R = [[set() for _ in range(n)] for _ in range(n)]
        for i, s in enumerate(states):
            for sym, t in s.transitions.items():
                j = id2idx[t.id]
                R[i][j].add(sym)

        start_idx = 0  # первый стартовый
        final_idxs = [i for i, s in enumerate(states) if s.is_final]
        non_special = [i for i in range(n) if i != start_idx and i not in final_idxs]

        for k in non_special:
            for i in range(n):
                if i == k:
                    continue
                for j in range(n):
                    if j == k:
                        continue
                    if not R[i][k] or not R[k][j]:
                        continue
                    loop = regex_union(R[k][k])
                    path_ik = regex_union(R[i][k])
                    path_kj = regex_union(R[k][j])
                    mid = f"({loop})*" if loop else ""
                    addition = f"{path_ik}{mid}{path_kj}"
                    R[i][j].add(addition)
            for row in R:
                row[k] = set()
            R[k] = [set() for _ in range(n)]

        regexes = []
        for f in final_idxs:
            reg = regex_union(R[start_idx][f])
            if reg:
                regexes.append(reg)
        return '|'.join(regexes) if regexes else ''

def intersect(dfa1, dfa2):
    alphabet = dfa1.alphabet & dfa2.alphabet
    queue = deque()
    state_map = {}

    start1 = dfa1.states[0]
    start2 = dfa2.states[0]
    queue.append((start1, start2))
    new_states = []
    id_counter = 1

    def key(s1, s2): return (id(s1), id(s2))

    while queue:
        s1, s2 = queue.popleft()
        k = key(s1, s2)
        if k in state_map:
            continue
        new_state = DFAState({}, id_counter, s1.is_final and s2.is_final)
        id_counter += 1
        state_map[k] = new_state
        new_states.append(new_state)

        for c in alphabet:
            if c in s1.transitions and c in s2.transitions:
                next1 = s1.transitions[c]
                next2 = s2.transitions[c]
                queue.append((next1, next2))

    # Заполняем переходы
    for (s1_id, s2_id), new_state in state_map.items():
        s1 = next(s for s in dfa1.states if id(s) == s1_id)
        s2 = next(s for s in dfa2.states if id(s) == s2_id)
        for c in alphabet:
            if c in s1.transitions and c in s2.transitions:
                target = state_map.get(key(s1.transitions[c], s2.transitions[c]))
                if target:
                    new_state.transitions[c] = target


    dfa = DFA.__new__(DFA)   
    dfa.states = list(state_map.values())
    dfa.alphabet = alphabet
    return dfa

def complement(dfa):
    for state in dfa.states:
        state.is_final = not state.is_final
    return dfa

def difference(dfa1, dfa2):
    return intersect(dfa1, complement(dfa2))

def regex_union(s):
    if not s:
        return ''
    if len(s) == 1:
        return next(iter(s))
    return '|'.join(f"({x})" if '|' in x or '.' in x else x for x in s)