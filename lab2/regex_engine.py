from regex_parser import tokenize, insert_concat, to_postfix
from syntax_tree import SyntaxTree
from nfa_dfa import DFA 
from dfa_min import DFAOptimizer, intersect, difference

class Regex:
    def __init__(self, pattern: str):
        if pattern == "":
            raise ValueError("Пустой шаблон запрещён для обычного конструктора. Используйте from_dfa.")\
        
        self.pattern = pattern
        self.dfa = None
        self.tree = None
        self.compiled = False

    @classmethod
    def from_dfa(cls, dfa):
        obj = cls.__new__(cls)
        obj.dfa = dfa
        obj.compiled = True
        obj.tree = None
        obj.pattern = None
        return obj
    
    def compile(self):
        tokens = tokenize(self.pattern)
        tokens_with_concat = insert_concat(tokens)
        postfix = to_postfix(tokens_with_concat)

        self.tree = SyntaxTree(postfix)
        if self.tree.root is None:
            raise ValueError("Ошибка построения дерева: root is None")

        original_dfa = DFA(self.tree)
        minimized_dfa = DFAOptimizer(original_dfa).minimize()

        # 🔁 Критически важный момент — перенос нужных данных
        minimized_dfa.alphabet = original_dfa.alphabet
        minimized_dfa.leaves = original_dfa.leaves
        minimized_dfa.terminal = original_dfa.terminal
        minimized_dfa.followpos = original_dfa.followpos

        self.dfa = minimized_dfa
        self.compiled = True
        return self


    def match(self, text: str) -> bool:
        if not self.compiled:
            raise ValueError("Regex not compiled. Call compile() first.")
        return self.dfa.match(text)

    def intersect(self, other: 'Regex') -> 'Regex':
        if not self.compiled or not other.compiled:
            raise ValueError("Both Regex must be compiled before intersection.")
        return Regex.from_dfa(intersect(self.dfa, other.dfa))

    def difference(self, other: 'Regex') -> 'Regex':
        if not self.compiled or not other.compiled:
            raise ValueError("Both Regex must be compiled before difference.")
        return Regex.from_dfa(difference(self.dfa, other.dfa))
