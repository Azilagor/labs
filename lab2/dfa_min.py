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
            state_map[id(group[0])] = new_state
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

        return minimized

    def get_partition_index(self, state, partitions):
        for i, group in enumerate(partitions):
            if state in group:
                return i
        return -1
    
    def moore_minimize(dfa):
    # 1. Группируем состояния: финальные и нефинальные
        finals = [s for s in dfa.states if s.is_final]
        non_finals = [s for s in dfa.states if not s.is_final]
        partitions = [non_finals, finals] if non_finals else [finals]

        state_to_group = {}
        for i, group in enumerate(partitions):
            for state in group:
                state_to_group[state] = i

        changed = True
        while changed:
            changed = False
            new_partitions = []

            for group in partitions:
                buckets = {}
                for state in group:
                    # Сигнатура = куда ведут переходы по каждому символу алфавита
                    signature = tuple(
                        state_to_group.get(state.transitions.get(c), -1)
                        for c in sorted(dfa.alphabet)
                    )
                    buckets.setdefault(signature, []).append(state)
                
                if len(buckets) > 1:
                    changed = True
                new_partitions.extend(buckets.values())

            partitions = new_partitions
            # Обновим отображение: состояние -> индекс группы
            state_to_group = {
                state: i for i, group in enumerate(partitions) for state in group
            }

        # 2. Построим минимальный DFA
        minimized_states = []
        state_map = {}
        for i, group in enumerate(partitions):
            # Объединяем id_set всех состояний группы
            combined_id_set = set()
            is_final = any(s.is_final for s in group)
            for s in group:
                combined_id_set |= s.id_set

            new_state = DFAState(combined_id_set, i + 1, is_final)
            minimized_states.append(new_state)
            state_map[id(group[0])] = new_state  # запоминаем по представителю группы

        # 3. Установим переходы
        for i, group in enumerate(partitions):
            repr_state = group[0]
            new_state = state_map[id(repr_state)]
            for c in dfa.alphabet:
                target = repr_state.transitions.get(c)
                if not target:
                    continue
                for tgt_group in partitions:
                    if target in tgt_group:
                        new_state.transitions[c] = state_map[id(tgt_group[0])]
                        break

        # 4. Построим финальный DFA
        minimized = object.__new__(type(dfa))
        minimized.states = minimized_states
        minimized.alphabet = dfa.alphabet
        minimized.leaves = dfa.leaves
        minimized.followpos = dfa.followpos
        minimized.terminal = dfa.terminal

        return minimized


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
