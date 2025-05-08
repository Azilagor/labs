from nfa_dfa import DFAState
from collections import defaultdict, deque

class DFAOptimizer:
    def __init__(self, dfa):
        self.original_dfa = dfa
        self.alphabet = dfa.alphabet
    
    def minimize(self):
        
        partitions = [
            [s for s in self.original_dfa.states if not s.is_final],
            [s for s in self.original_dfa.states if s.is_final]
        ]
        partitions = [p for p in partitions if p]  # убрать пустые

        changed = True
        while changed:
            changed = False
            new_partitions = []
            for group in partitions:
                subgroups = defaultdict(list)
                for state in group:
                    signature = tuple(
                        self.get_partition_index(state.transitions.get(c), partitions)
                        for c in self.alphabet
                    )
                    subgroups[signature].append(state)
                if len(subgroups) > 1:
                    changed = True
                new_partitions.extend(subgroups.values())
            partitions = new_partitions

        # строим минимальный DFA
        state_map = {}
        for i, group in enumerate(partitions):
            repr_state = group[0]
            new_state = DFAState(set(), i + 1, repr_state.is_final)
            state_map[id(repr_state)] = new_state

        for i, group in enumerate(partitions):
            repr_state = group[0]
            current = state_map[id(repr_state)]
            for c in self.alphabet:
                target = repr_state.transitions.get(c)
                if target:
                    target_index = self.get_partition_index(target, partitions)
                    repr_target = partitions[target_index][0]
                    current.transitions[c] = state_map[id(repr_target)]

        minimized = type(self.original_dfa)(None)
        minimized.states = list(state_map.values())
        minimized.alphabet = self.alphabet
        return minimized
    
    def get_partition_index(self, state, partitions):
        for i, group in enumerate(partitions):
            if state in group:
                return i
        return -1


def intersect(dfa1, dfa2):
    
    start_pair = (dfa1.states[0], dfa2.states[0])
    visited = {}
    queue = deque([start_pair])

    result_states = []
    state_map = {}

    def get_state_id(a, b):
        return (a.id, b.id)

    while queue:
        s1, s2 = queue.popleft()
        key = get_state_id(s1, s2)
        if key in visited:
            continue
        new_state = DFAState(set(), len(visited) + 1, s1.is_final and s2.is_final)
        result_states.append(new_state)
        visited[key] = new_state
        state_map[key] = new_state

        for c in dfa1.alphabet & dfa2.alphabet:
            if c in s1.transitions and c in s2.transitions:
                next_pair = (s1.transitions[c], s2.transitions[c])
                queue.append(next_pair)

    for (s1_id, s2_id), state in visited.items():
        s1 = next(filter(lambda s: s.id == s1_id, dfa1.states))
        s2 = next(filter(lambda s: s.id == s2_id, dfa2.states))
        for c in dfa1.alphabet & dfa2.alphabet:
            if c in s1.transitions and c in s2.transitions:
                target = state_map.get(get_state_id(s1.transitions[c], s2.transitions[c]))
                if target:
                    state.transitions[c] = target

    result_dfa = type(dfa1)(None)
    result_dfa.states = list(visited.values())
    result_dfa.alphabet = dfa1.alphabet & dfa2.alphabet
    return result_dfa
    
def complement(dfa):
    for state in dfa.states:
        state.is_final = not state.is_final
    return dfa

def difference(dfa1, dfa2):
    return intersect(dfa1, complement(dfa2))
