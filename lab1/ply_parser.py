import ply.lex as lex
import ply.yacc as yacc

MAX_LENGTH = 63

# === Токены ===
tokens = ('NFS', 'SLASH', 'NAME')

# === Лексер с ручным приоритетом ===

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

# === Парсер ===
class ParseState:
    def __init__(self):
        self.server = None
        self.is_valid = False

state = ParseState()

def p_start(p):
    'start : NFS NAME path'
    total_len = len(p[2]) + len(''.join(p[3]))  # имя сервера + путь
    if total_len > MAX_LENGTH:
        raise ValueError("Путь слишком длинный")
    state.server = p[2]
    state.is_valid = True

def p_path(p):
    'path : SLASH NAME more_path'
    # хотя бы один каталог обязателен
    p[0] = ["/", p[2]] + p[3]

def p_more_path(p):
    '''more_path : SLASH NAME more_path
                 | empty'''
    if len(p) == 4:
        p[0] = ["/", p[2]] + p[3]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    p[0] = []

def p_error(p):
    raise SyntaxError("Синтаксическая ошибка")

parser = yacc.yacc()

# === Метод для main.py ===
def method_ply(line):
    global state
    state = ParseState()
    try:
        parser.parse(line.strip(), lexer=lexer)
    except Exception:
        return False, None
    return state.is_valid, state.server
