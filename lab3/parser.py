import ply.yacc as yacc
from tokens import tokens
from lexer import lexer

def p_program(p):
    '''program : function_list'''
    p[0] = ('program', p[1])

def p_function_list(p):
    '''function_list : function_list function
                     | function'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_function(p):
    '''function : FUNCTION ID LPAREN ID RPAREN DO statements DONE'''
    p[0] = ('function', p[2], p[4], p[7])

def p_main_function(p):
    '''function : MAIN LPAREN ID RPAREN DO statements DONE'''
    p[0] = ('function', 'main', p[3], p[6])
def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_var(p):
    '''statement : VAR ID ASSIGN NUMBER'''
    p[0] = ('var_assign', p[2], p[4])

def p_statement_assign(p):
    '''statement : ID ASSIGN NUMBER'''
    p[0] = ('assign', p[1], p[3])

def p_statement_forward(p):
    '''statement : FORWARD NUMBER'''
    p[0] = ('forward', p[2])

def p_error(p):
    if p:
        print(f"Syntax error at {p.value!r}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
