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
        print("Токены:", tokens)
        tokens_with_concat = insert_concat(tokens)
        print("С конкатенацией:", insert_concat(tokens))
        postfix = to_postfix(tokens_with_concat)
        print("Постфикс:", to_postfix(insert_concat(tokens)))

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
        return Regex.from_dfa(intersect(self.dfa, other.dfa))

    def difference(self, other: 'Regex') -> 'Regex':
        if not self.compiled or not other.compiled:
            raise ValueError("Both Regex must be compiled before difference.")
        return Regex.from_dfa(difference(self.dfa, other.dfa))
