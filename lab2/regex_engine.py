from regex_parser import tokenize, insert_concat, to_postfix
from syntax_tree import SyntaxTree
from nfa_dfa import DFA
from dfa_min import DFAOptimizer, intersect, difference

class Regex:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.dfa = None
        self.tree = None
        self.compiled = False

    def compile(self):
        tokens = to_postfix(insert_concat(tokenize(self.pattern)))
        self.tree = SyntaxTree(tokens)

        if self.tree.root is None:
            raise ValueError("Ошибка построения дерева: root is None")


        self.dfa = DFA(self.tree)
        self.dfa = DFAOptimizer(self.dfa).minimize()
        self.compiled = True
        return self

    def match(self, text: str) -> bool:
        if not self.compiled:
            raise ValueError("Regex not compiled. Call compile() first.")
        return self.dfa.match(text)

    def intersect(self, other: 'Regex') -> 'Regex':
        if not self.compiled or not other.compiled:
            raise ValueError("Both Regex must be compiled before intersection.")
        new_regex = Regex("")
        new_regex.dfa = intersect(self.dfa, other.dfa)
        new_regex.compiled = True
        return new_regex

    def difference(self, other: 'Regex') -> 'Regex':
        if not self.compiled or not other.compiled:
            raise ValueError("Both Regex must be compiled before difference.")
        new_regex = Regex("")
        new_regex.dfa = difference(self.dfa, other.dfa)
        new_regex.compiled = True
        return new_regex
