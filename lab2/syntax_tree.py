class Node:
    def __init__(self, type_, label, left=None, right=None, id=None):
        self.type = type_       # 'leaf', 'concat', 'or', 'star'
        self.label = label      # символ или оператор
        self.left = left
        self.right = right
        self.id = id            # уникальный id (только для листа)

        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

class SyntaxTree:
    def __init__(self, postfix_tokens):
        self.leaves = {}  # id: label
        self.followpos = {}  # id: set()
        self.alphabet = set()
        self.id_counter = 1

        self.root = self.build_tree(postfix_tokens)
        self.compute_nullable_first_last_follow(self.root)
        
    def build_tree(self, tokens):
        stack = []
        for token in tokens:
            if token in {'.', '|'}:
                right = stack.pop()
                left = stack.pop()
                node = Node('concat' if token == '.' else 'or', token, left, right)
            elif token == '*':
                child = stack.pop()
                node = Node('star', token, child)
            else:
                node = Node('leaf', token, id=self.id_counter)
                self.leaves[self.id_counter] = token
                self.followpos[self.id_counter] = set()
                self.alphabet.add(token)
                self.id_counter += 1
            stack.append(node)

        # добавим служебный символ конца строки
        end_node = Node('leaf', '#', id=self.id_counter)
        self.leaves[self.id_counter] = '#'
        self.followpos[self.id_counter] = set()
        self.alphabet.add('#')
        self.id_counter += 1

        root = Node('concat', '.', stack.pop(), end_node)
        return root

    def compute_nullable_first_last_follow(self, node):
        if node is None:
            return

        self.compute_nullable_first_last_follow(node.left)
        self.compute_nullable_first_last_follow(node.right)

        if node.type == 'leaf':
            node.nullable = False if node.label != '$' else True
            node.firstpos = {node.id}
            node.lastpos = {node.id}
        elif node.type == 'or':
            node.nullable = node.left.nullable or node.right.nullable
            node.firstpos = node.left.firstpos | node.right.firstpos
            node.lastpos = node.left.lastpos | node.right.lastpos
        elif node.type == 'concat':
            node.nullable = node.left.nullable and node.right.nullable
            node.firstpos = node.left.firstpos if not node.left.nullable else node.left.firstpos | node.right.firstpos
            node.lastpos = node.right.lastpos if not node.right.nullable else node.left.lastpos | node.right.lastpos
            for i in node.left.lastpos:
                self.followpos[i] |= node.right.firstpos
        elif node.type == 'star':
            node.nullable = True
            node.firstpos = node.left.firstpos
            node.lastpos = node.left.lastpos
            for i in node.left.lastpos:
                self.followpos[i] |= node.left.firstpos
