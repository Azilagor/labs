class Node:
    def __init__(self, type_, label, left=None, right=None, id=None):
        self.type = type_       # 'leaf', 'concat', 'or', 'star'
        self.label = label      
        self.left = left
        self.right = right
        self.id = id            

        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

class SyntaxTree:
    def __init__(self, postfix_tokens):
        self.leaves = {}  
        self.followpos = {}  
        self.alphabet = set()
        self.id_counter = 1

        self.root = self.build_tree(postfix_tokens)
        if self.root is None:
             raise ValueError("Ошибка построения дерева разбора (неправильная регулярка?)")
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
            elif token == '+':
                base = stack.pop()
                star = Node('star', '*', left=self.clone(base))
                node = Node('concat', '.', base, star)
            elif token == '?':
                base = stack.pop()
                epsilon = Node('leaf', '$', id=self.id_counter)
                self.leaves[self.id_counter] = '$'
                self.followpos[self.id_counter] = set()
                self.id_counter += 1
                node = Node('or', '|', base, epsilon)
            elif token.startswith("{") and token.endswith("}"):
                # ----- Обработка повторов -----
                body = token[1:-1]
                if ',' in body:
                    parts = body.split(',')
                    if len(parts) == 2 and parts[0].isdigit() and (parts[1].isdigit() or parts[1] == ''):
                        min_count = int(parts[0])
                        max_count = int(parts[1]) if parts[1] else min_count + 3  # ограничим "бесконечность"
                    else:
                        raise ValueError(f"Неверный формат повторения: {token}")
                elif body.isdigit():
                    min_count = max_count = int(body)
                else:
                    raise ValueError(f"Неверный формат повторения: {token}")

                base = stack.pop()
                # n обязательных копий
                if min_count == 0:
                    node = Node('leaf', '$', id=self.id_counter)
                    self.leaves[self.id_counter] = '$'
                    self.followpos[self.id_counter] = set()
                    self.id_counter += 1
                else:
                    node = self.clone(base)
                    for _ in range(min_count - 1):
                        node = Node('concat', '.', self.clone(base), node)
                # (m-n) опциональных копий (через or с epsilon)
                for _ in range(max_count - min_count):
                    epsilon = Node('leaf', '$', id=self.id_counter)
                    self.leaves[self.id_counter] = '$'
                    self.followpos[self.id_counter] = set()
                    self.id_counter += 1
                    opt = Node('or', '|', self.clone(base), epsilon)
                    node = Node('concat', '.', node, opt)
            else:
                node = Node('leaf', token, id=self.id_counter)
                self.leaves[self.id_counter] = token
                self.followpos[self.id_counter] = set()
                self.alphabet.add(token)
                self.id_counter += 1
            stack.append(node)

    #    print(">>> Стек после основного разбора:", stack)

        if len(stack) != 1:
            raise ValueError("Ошибка парсинга: стек не пуст после построения дерева.")
        main_node = stack.pop()

        # Добавляем служебный символ #
        end_node = Node('leaf', '#', id=self.id_counter)
        self.leaves[self.id_counter] = '#'
        self.followpos[self.id_counter] = set()
        self.alphabet.add('#')
        self.id_counter += 1

        root = Node('concat', '.', main_node, end_node)
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

    def clone(self, node):
        if node is None:
            return None
        new_node = Node(node.type, node.label, id=node.id)
        new_node.left = self.clone(node.left)
        new_node.right = self.clone(node.right)
        return new_node