import ply.lex as lex
import ply.yacc as yacc

MAX_LENGTH = 63

# === Токены ===
tokens = ('NFS', 'SLASH', 'NAME')

def t_NFS(t):
    r'nfs://'
    return t

def t_SLASH(t):
    r'/'
    return t

def t_NAME(t):
    r'[a-zA-Z]+'
    return t

t_ignore = ' \t'

def t_error(t):
    raise SyntaxError(f"Неверный символ: {t.value[0]}")

lexer = lex.lex()

# === Парсер состояние
class ParseState:
    def __init__(self):
        self.server = None
        self.is_valid = False

state = ParseState()

# === Парсер правил

def p_start(p):
    '''start : NFS NAME SLASH NAME SLASH rest'''
    total_len = len(p[2]) + len(p[4]) + 2 + sum(len(seg) for seg in p[6])
    if total_len > MAX_LENGTH:
        raise ValueError("Путь слишком длинный")
    state.server = p[2]
    state.is_valid = True

def p_rest(p):
    '''rest : segment rest
            | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_segment(p):
    '''segment : NAME
               | NAME SLASH'''
    if len(p) == 3:
        p[0] = p[1] + "/"
    else:
        p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = []

def p_error(p):
    raise SyntaxError("Синтаксическая ошибка")

parser = yacc.yacc()

# === Метод
def method_ply(line):
    global state
    state = ParseState()
    try:
        parser.parse(line.strip(), lexer=lexer)
    except Exception:
        return False, None
    return state.is_valid, state.server
