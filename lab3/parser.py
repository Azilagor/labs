import ply.yacc as yacc
from tokens import tokens
from lexer import lexer

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

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
    '''statement : ID ASSIGN expression
                 | ID LPAREN expression RPAREN ASSIGN expression'''
    if len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = ('assign_index', p[1], p[3], p[6])

def p_statement_forward(p):
    '''statement : FORWARD NUMBER'''
    p[0] = ('forward', p[2])

def p_statement_var_decl(p):
    '''statement : VAR ID
                 | VAR ID LPAREN NUMBER RPAREN'''
    if len(p) == 3:
        p[0] = ('var_decl', p[2])
    else:
        p[0] = ('var_decl', p[2], p[4])



def p_var_ref(p):
    '''var_ref : ID
               | ID LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = ('var_ref', p[1])
    else:
        p[0] = ('var_ref_index', p[1], p[3])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = ('plus', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('minus', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('mul', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('div', p[1], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('uminus', p[2])


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_var(p):
    'expression : var_ref'
    p[0] = p[1]


def p_statement_if(p):
    '''statement : IF condition DO statements DONE
                 | IF condition DO statements DONE ELDEF DO statements DONE
                 | IF condition DO statements DONE ELDEF DO statements DONE ELUND DO statements DONE'''
    if len(p) == 6:
        p[0] = ('if', p[2], p[4], None, None)
    elif len(p) == 10:
        p[0] = ('if', p[2], p[4], p[7], None)
    elif len(p) == 14:
        p[0] = ('if', p[2], p[4], p[7], p[11])

def p_condition(p):
    '''condition : expression LT expression
                 | expression GT expression
                 | expression EQ expression'''
    if p[2] == '<':
        p[0] = ('lt', p[1], p[3])
    elif p[2] == '>':
        p[0] = ('gt', p[1], p[3])
    elif p[2] == '=':
        p[0] = ('eq', p[1], p[3])


def p_statement_while(p):
    '''statement : WHILE condition DO statements DONE
                 | WHILE condition DO statements FINISH statements DONE'''
    if len(p) == 6:
        p[0] = ('while', p[2], p[4], None)
    else:
        p[0] = ('while', p[2], p[4], p[6])


def p_expression_call(p):
    'expression : ID LPAREN expression RPAREN'
    p[0] = ('call_expr', p[1], p[3])

def p_statement_return(p):
    '''statement : RETURN
                 | RETURN expression'''
    if len(p) == 2:
        p[0] = ('return', None)
    else:
        p[0] = ('return', p[2])

def p_error(p):
    if p:
        print(f"Syntax error at {p.value!r}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
