from syntax_tree import SyntaxTree
from collections import deque
import copy
import itertools

class DFAState:
    def __init__(self, id_set: set, id_num: int, is_final: bool):
        self.id_set = id_set             
        self.id = id_num                   
        self.transitions = {}              
        self.is_final = is_final



class DFA:
    def __init__(self, syntax_tree: SyntaxTree):
    #    print('Передан syntax_tree:', syntax_tree)
    #    print('root:', getattr(syntax_tree, "root", None))
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
        self.start_state = start_state
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
        current = self.start_state
        for c in s:
            if c not in current.transitions:
                return False
            current = current.transitions[c]
        return current.is_final
    
    def print_dfa_console(dfa):
        print("\n📘 DFA (консольная визуализация):")
        print("-" * 40)
        header = f"{'State':<8} | {'Final':<5} | Transitions"
        print(header)
        print("-" * len(header))

        for state in dfa.states:
            final_mark = '✔️' if state.is_final else ''
            transitions = ', '.join(f"{k}→q{v.id}" for k, v in state.transitions.items())
            print(f"q{state.id:<7} | {final_mark:<5} | {transitions}")

        # Определение старта
        start_state = getattr(dfa, 'start_state', dfa.states[0])
        print("-" * 40)
        print(f"🚩 Стартовое состояние: q{start_state.id}")
        final_ids = [s.id for s in dfa.states if s.is_final]
        print(f"🏁 Финальные состояния: {', '.join(f'q{id}' for id in final_ids)}")
        print("-" * 40)

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
        new_id_set = s1.id_set & s2.id_set
        new_state = DFAState(new_id_set, id_counter, s1.is_final and s2.is_final)
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
    dfa = copy.deepcopy(dfa)
    for state in dfa.states:
        state.is_final = not state.is_final
    return dfa

def difference(dfa1, dfa2):
    return intersect(dfa1, complement(dfa2))

def dfa_to_regex(dfa) -> str:

    # 1. Назначим индекс каждой вершине
    states = dfa.states
    id_to_index = {s.id: i for i, s in enumerate(states)}
    index_to_state = {i: s for i, s in enumerate(states)}
    n = len(states)

    # 2. Матрица переходов R[i][j] = regex из i в j
    R = [['' for _ in range(n)] for _ in range(n)]
    for state in states:
        i = id_to_index[state.id]
        for symbol, dest in state.transitions.items():
            j = id_to_index[dest.id]
            if R[i][j]:
                R[i][j] = f"({R[i][j]}|{symbol})"
            else:
                R[i][j] = symbol

    # 3. Добавим новое стартовое и конечное состояние
    start_index = n      # индекс нового старта
    end_index = n + 1    # индекс нового конца
    new_n = n + 2

    # Новая пустая матрица размером (n+2) x (n+2)
    new_R = [['' for _ in range(new_n)] for _ in range(new_n)]

    # Копируем старую R внутрь новой
    for i in range(n):
        for j in range(n):
            new_R[i + 1][j + 1] = R[i][j]

    # ε-переход от нового старта в исходное стартовое состояние
    real_start_index = id_to_index[dfa.start_state.id]
    new_R[start_index][real_start_index + 1] = '$'  # обозначим ε как $

    # ε-переходы из всех финальных состояний в новый конец
    for i, state in enumerate(states):
        if state.is_final:
            new_R[i + 1][end_index] = '$'

    # 4. Применим метод исключения состояний
    # исключаем всё кроме start_index и end_index
    for k in range(new_n):
        if k == start_index or k == end_index:
            continue
        for i in range(new_n):
            if i == k:
                continue
            for j in range(new_n):
                if j == k:
                    continue
                A = new_R[i][j]
                B = new_R[i][k]
                C = new_R[k][k]
                D = new_R[k][j]

                if B and D:
                    middle = f"{B}({C})*{D}" if C else f"{B}{D}"
                    if A:
                        new_R[i][j] = f"({A}|{middle})"
                    else:
                        new_R[i][j] = middle

    # 5. Результат — из start → end
    result = new_R[start_index][end_index]
    return result


def simplify_regex(regex: str) -> str:
    def remove_outer_epsilon(r):
        # Удаляем внешнее оборачивание в ($|...)
        if r.startswith('($|') and r.endswith(')'):
            return r[3:-1]
        # Удаляем внешнее оборачивание в (...|$)
        if r.startswith('(') and r.endswith('|$)'):
            return r[1:-3]
        return r

    def remove_all_epsilon(r):
        return ''.join(c for c in r if c != '$')

    def collapse_double_parens(r):
        # Убираем ((...)) -> (...)
        i = 0
        while i < len(r) - 3:
            if r[i] == '(' and r[i+1] == '(':
                j = i + 2
                depth = 2
                while j < len(r):
                    if r[j] == '(':
                        depth += 1
                    elif r[j] == ')':
                        depth -= 1
                        if depth == 0 and r[j+1:j+2] == ')':
                            # Заменяем ((...)) на (...)
                            r = r[:i] + '(' + r[i+2:j] + ')' + r[j+2:]
                            i = -1  # перезапустить сканирование
                            break
                    j += 1
            i += 1
        return r

    def remove_useless_parens_before_star(r):
        # Заменяет (a)* → a*
        result = ''
        i = 0
        while i < len(r):
            if r[i] == '(':
                j = i + 1
                depth = 1
                while j < len(r):
                    if r[j] == '(':
                        depth += 1
                    elif r[j] == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if j + 1 < len(r) and r[j + 1] == '*':
                    inner = r[i+1:j]
                    result += inner + '*'
                    i = j + 2
                else:
                    result += r[i:j+1]
                    i = j + 1
            else:
                result += r[i]
                i += 1
        return result

    regex = regex.strip()
    regex = remove_outer_epsilon(regex)
    regex = remove_all_epsilon(regex)
    regex = collapse_double_parens(regex)
    regex = remove_useless_parens_before_star(regex)
    return regex
