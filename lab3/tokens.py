# token.py

reserved = {
    'var': 'VAR',
    'int': 'INT',
    'bool': 'BOOL',
    'cell': 'CELL',
    'true': 'TRUE',
    'false': 'FALSE',
    'undef': 'UNDEF',
    'empty': 'EMPTY',
    'wall': 'WALL',
    'box': 'BOX',
    'exit': 'EXIT',
    'while': 'WHILE',
    'do': 'DO',
    'finish': 'FINISH',
    'done': 'DONE',
    'if': 'IF',
    'eldef': 'ELDEF',
    'elund': 'ELUND',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'main': 'MAIN',
    'forward': 'FORWARD',
    'backward': 'BACKWARD',
    'left': 'LEFT',
    'right': 'RIGHT',
    'load': 'LOAD',
    'drop': 'DROP',
    'look': 'LOOK',
    'test': 'TEST',
}

tokens = [
    'NUMBER', 'HEXNUMBER', 'INF', 'MINUS_INF', 'NAN',
    'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'ASSIGN', 'EQ', 'LT', 'GT',
    'XOR', 'HASH', 'COLON', 'COMMA'
] + list(reserved.values())
