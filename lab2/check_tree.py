from regex_parser import tokenize, insert_concat, to_postfix
from syntax_tree import SyntaxTree
from nfa_dfa import DFA, DFAState
from dfa_min import DFAOptimizer
from regex_engine import Regex


pattern = "(a|bc)*|(a|bc)*ba(c)*"

tokens = tokenize(pattern)
print("📥 Токены:", tokens)

tokens_concat = insert_concat(tokens)
print("➕ С конкатенацией:", tokens_concat)

postfix = to_postfix(tokens_concat)
print("📤 Постфикс:", postfix)

tree = SyntaxTree(postfix)
print("🌳 Дерево построено, root.label:", tree.root.label)


 
dfa = DFA(tree)

dfa.print_dfa_console()


regex = Regex("(a|bc)*|(a|bc)*ba(c)*").compile()

print("🔁 restored 1:", regex.dfa.to_regex())

# Для контроля — создаём DFA вручную и проверяем его
tokens = to_postfix(insert_concat(tokenize("(a|bc)*|(a|bc)*ba(c)*")))
tree = SyntaxTree(tokens)
dfa = DFA(tree)  # без минимизации

dfa_min = DFAOptimizer(dfa).moore_minimize()
print("✅ Moore dfa min:", dfa_min.to_regex())
print("🔁 restored 2:", dfa.to_regex())

def test_restore():
    pattern = "(a|bc)*|(a|bc)*ba(c)*"



    # Ручной DFA (без оптимизации)
    tokens = to_postfix(insert_concat(tokenize(pattern)))
    tree = SyntaxTree(tokens)
    dfa = DFA(tree)
    dfa_opt = DFAOptimizer(dfa).minimize()

    restored1 = dfa.to_regex()
    print("✅ to_regex до минимизации:", restored1)

    # После минимизации с переносом полей
    minimized = DFAOptimizer(dfa).minimize()
    minimized.alphabet = dfa.alphabet
    minimized.leaves = dfa.leaves
    minimized.terminal = dfa.terminal
    minimized.followpos = dfa.followpos

    restored2 = minimized.to_regex()
    print("✅ to_regex после минимизации (вручную):", restored2)

    # Через Regex.compile()
    regex = Regex(pattern).compile()
    restored3 = regex.dfa.to_regex()
    print("✅ to_regex через Regex.compile:", restored3)


    dfa_opt.leaves = dfa.leaves
    dfa_opt.followpos = dfa.followpos
    dfa_opt.terminal = dfa.terminal
    dfa_opt.alphabet = dfa.alphabet

    print("✅ TO_REGEX (ручной DFA):", dfa_opt.to_regex())
   
    # Теперь через Regex.compile()
    regex = Regex(pattern).compile()
    print("✅ TO_REGEX (через regex.dfa):", regex.dfa.to_regex())


if __name__ == "__main__":
    test_restore()