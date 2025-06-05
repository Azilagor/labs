from regex_parser import tokenize, insert_concat, to_postfix
from syntax_tree import SyntaxTree
from nfa_dfa import DFA, DFAState
from dfa_min import DFAOptimizer

# def test_syntax_tree(pattern):
#     tokens = tokenize(pattern)
#     print("Токены:", tokens)
#     tokens_with_concat = insert_concat(tokens)
#     print("С конкатенацией:", tokens_with_concat)
#     postfix = to_postfix(tokens_with_concat)
#     print("Постфикс:", postfix)
#     tree = SyntaxTree(postfix)
#     print("--- Корень дерева ---")
#     print("type:", tree.root.type)
#     print("label:", tree.root.label)
#     print("left:", getattr(tree.root, 'left', None))
#     print("right:", getattr(tree.root, 'right', None))
#     print("--- Leaves ---")
#     print(tree.leaves)
#     print("--- Followpos ---")
#     print(tree.followpos)
#     print("--- Алфавит ---")
#     print(tree.alphabet)

# # Пример вызова:
# test_syntax_tree("a|b")

# def print_dfa_states(dfa):
#     print("--- DFA состояния ---")
#     for state in dfa.states:
#         print(f"State {state.id}: ids={state.id_set}, is_final={state.is_final}")
#         for symbol, target in state.transitions.items():
#             print(f"  '{symbol}' -> State {target.id}")
#     print()

# def test_dfa(pattern, test_strings):
#     print(f"\n=== Тест для: '{pattern}' ===")
#     tokens = tokenize(pattern)
#     print("Токены:", tokens)
#     tokens_with_concat = insert_concat(tokens)
#     print("С конкатенацией:", tokens_with_concat)
#     postfix = to_postfix(tokens_with_concat)
#     print("Постфикс:", postfix)
#     tree = SyntaxTree(postfix)
#     print("--- Структура дерева (корень):", tree.root.type, tree.root.label)
#     dfa = DFA(tree)
#     print_dfa_states(dfa)

#     for s in test_strings:
#         result = dfa.match(s)
#         print(f"Строка '{s}': {'MATCH' if result else 'NO MATCH'}")

# # Пример использования
# test_dfa("a|b", ["", "a", "b", "c", "ab"])

def print_dfa_states(dfa):
    print("--- DFA состояния ---")
    for state in dfa.states:
        print(f"State {state.id}: ids={state.id_set}, is_final={state.is_final}")
        for symbol, target in state.transitions.items():
            print(f"  '{symbol}' -> State {target.id}")
    print()

pattern = "a|b"
tokens = tokenize(pattern)
tokens_with_concat = insert_concat(tokens)
postfix = to_postfix(tokens_with_concat)
tree = SyntaxTree(postfix)

# После создания DFA:
dfa = DFA(tree)
print("== DFA до минимизации ==")
print_dfa_states(dfa)

dfa_min = DFAOptimizer(dfa).minimize()
print("== DFA после минимизации ==")
print_dfa_states(dfa_min)

tests = [
    # Должны принять
    "abb", "aabb", "babb", "aaabb", "abababb", "bbaabb", "bbbbabb", "aababb", "baabb", "ababb", "babababb", "aaaaabb",
    # Должны отклонить
    "ab", "aab", "aabbb", "aba", "baab", "bab", "aaba", "bbaab", "baa", "a", "b", "abbaa", "abbab", "abbabb"
]
