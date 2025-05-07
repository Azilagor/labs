class DFAState:
    def __init__(self, id_set: set, id_num: int, is_final: bool):
        self.id_set = id_set                # множество позиций (по followpos)
        self.id = id_num                    # номер состояния
        self.transitions = {}              # символ: DFAState
        self.is_final = is_final



class DFA:
    def __init__(self, syntax_tree):
        self.alphabet = syntax_tree.alphabet - {'$'}
        self.terminal = syntax_tree.id_counter - 1  # позиция служебного символа '#'
        self.followpos = syntax_tree.followpos
        self.states = []
        self.state_map = {}  # frozenset(id_set) -> DFAState
        self.build_dfa(syntax_tree.root)

    def build_dfa(self, root):
        from collections import deque

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
                    if symbol == syntax_tree.leaves.get(pos):  # только если символ соответствует позиции
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

