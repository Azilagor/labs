import ply.lex as lex
from tokens import tokens, reserved

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN  = r':='
t_EQ      = r'='
t_LT      = r'<'
t_GT      = r'>'
t_XOR     = r'\^'
t_HASH    = r'\#'
t_COLON   = r':'
t_COMMA   = r','

def t_HEXNUMBER(t):
    r'0[xX][0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_INF(t):
    r'INF'
    t.value = float('inf')
    return t

def t_MINUS_INF(t):
    r'-INF'
    t.value = float('-inf')
    return t

def t_NAN(t):
    r'NAN'
    t.value = float('nan')
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'//.*'
    pass

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
