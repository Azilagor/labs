# ply_parser.py
import ply.lex as lex
import ply.yacc as yacc

MAX_LENGTH = 63
server_name = None
is_valid = False

# === Лексер ===
tokens = ('NFS', 'SLASH', 'WORD')

t_NFS = r'nfs://'
t_SLASH = r'/'
t_WORD = r'[a-z]+'

t_ignore = ' \t'

def t_error(t):
    raise SyntaxError(f"Неверный символ: {t.value[0]}")

lexer = lex.lex()

# === Парсер ===

def p_start(p):
    "start : NFS WORD path"
    global is_valid, server_name
    total_len = len(p[2]) + len(''.join(p[3]))
    if total_len > MAX_LENGTH:
        raise ValueError("Превышена длина пути")
    server_name = p[2]
    is_valid = True

def p_path(p):
    """path : SLASH WORD path
            | empty"""
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

def method_ply(line):
    global is_valid, server_name
    is_valid = False
    server_name = None
    try:
        parser.parse(line)
    except Exception:
        return False, None
    return is_valid, server_name
