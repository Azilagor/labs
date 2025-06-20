from nfa_dfa import DFAState
from collections import defaultdict, deque

class DFAOptimizer:
    def __init__(self, dfa):
        self.original_dfa = dfa
        self.alphabet = dfa.alphabet

    def minimize(self):
        # начальное разбиение: финальные и нефинальные
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
                        for c in sorted(self.alphabet)
                    )
                    subgroups[signature].append(state)
                if len(subgroups) > 1:
                    changed = True
                new_partitions.extend(subgroups.values())
            partitions = new_partitions

        # создаем новое множество состояний
        state_map = {}
        new_states = []
        for i, group in enumerate(partitions):
            # объединяем id_set всех состояний группы
            merged_id_set = set()
            is_final = False
            for s in group:
                merged_id_set |= s.id_set
                if s.is_final:
                    is_final = True
            new_state = DFAState(merged_id_set, i + 1, is_final)
            
            for s in group:
                state_map[id(s)] = new_state
            new_states.append(new_state)

        # заполняем переходы
        for i, group in enumerate(partitions):
            repr_state = group[0]
            current = state_map[id(repr_state)]
            for c in self.alphabet:
                targets = [
                    self.get_partition_index(s.transitions.get(c), partitions)
                    for s in group if c in s.transitions
                ]
                if not targets:
                    continue
                # считаем, что все переходы ведут в одну группу
                target_index = targets[0]
                target_group = partitions[target_index]
                repr_target = state_map[id(target_group[0])]
                current.transitions[c] = repr_target

        # создаём новый DFA без вызова __init__
        minimized = object.__new__(type(self.original_dfa))
        minimized.states = new_states
        minimized.alphabet = self.alphabet

        # важно для to_regex()
        minimized.leaves = self.original_dfa.leaves
        minimized.followpos = self.original_dfa.followpos
        minimized.terminal = self.original_dfa.terminal
        
        start_partition_index = self.get_partition_index(self.original_dfa.start_state, partitions)
        minimized.start_state = state_map[id(partitions[start_partition_index][0])]

        return minimized

    def get_partition_index(self, state, partitions):
        if state is None:
            return -1
        for i, group in enumerate(partitions):
                if state in group:
                    return i
        return -1
    


def intersect(dfa1, dfa2):
    start_pair = (dfa1.states[0], dfa2.states[0])
    visited = {}
    queue = deque([start_pair])
    state_map = {}

    def get_state_id(a, b):
        return (a.id, b.id)

    while queue:
        s1, s2 = queue.popleft()
        key = get_state_id(s1, s2)
        if key in visited:
            continue
        new_state = DFAState(set(), len(visited) + 1, s1.is_final and s2.is_final)
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

    # Создаём пустой объект DFA без вызова __init__
    result_dfa = object.__new__(type(dfa1))
    result_dfa.states = list(visited.values())
    result_dfa.alphabet = dfa1.alphabet & dfa2.alphabet
    return result_dfa

def complement(dfa):
    for state in dfa.states:
        state.is_final = not state.is_final
    return dfa

def difference(dfa1, dfa2):
    return intersect(dfa1, complement(dfa2))


def to_regex(self):
    states = self.states
    n = len(states)

    id2idx = {s.id: i for i, s in enumerate(states)}
    try:
        start_idx = id2idx[self.start_state.id]
    except AttributeError:
        start_idx = 0

    final_idxs = [i for i, s in enumerate(states) if s.is_final]

    # Инициализируем R[i][j][k]
    R = [[[set() for _ in range(n+1)] for _ in range(n)] for _ in range(n)]

    # Базовые переходы
    for i, s in enumerate(states):
        for sym, t in s.transitions.items():
            j = id2idx[t.id]
            R[i][j][0].add(sym)
    for i in range(n):
        R[i][i][0].add('$')  # ε на диагонали

    def regex_union(s):
        s = {x for x in s if x}
        if not s:
            return ''
        if len(s) == 1:
            return next(iter(s))
        return '|'.join(sorted(f"({x})" if '|' in x or len(x) > 1 else x for x in s))

    def wrap(x):
        if not x or x == '$':
            return ''
        if '|' in x or len(x) > 1:
            return f'({x})'
        return x

    # Алгоритм восстановления (аналог алгоритма Элгота-Макнота)
    for k in range(1, n+1):
        for i in range(n):
            for j in range(n):
                prev = R[i][j][k-1]
                left = R[i][k-1][k-1]
                loop = R[k-1][k-1][k-1]
                right = R[k-1][j][k-1]

                # left . (loop)* . right
                loop_part = wrap(regex_union(loop))
                if loop_part:
                    loop_part = f"{loop_part}*"
                concat_part = wrap(regex_union(left)) + loop_part + wrap(regex_union(right))

                R[i][j][k] = prev | {concat_part} if concat_part else prev

    # Все пути из стартового в финальные
    result_exprs = set()
    for f in final_idxs:
        result_exprs |= R[start_idx][f][n]

    return regex_union(result_exprs).replace('$', '')

