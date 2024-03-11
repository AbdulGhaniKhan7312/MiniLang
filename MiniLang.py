import ply.lex as lex
import ply.yacc as yacc

# Lexer
tokens = (
    'NUMBER', 'VARIABLE', 'PLUS', 'MINUS', 'TIMES', 'LPAREN', 'RPAREN',
    'ASSIGN', 'IF', 'ELSE', 'PRINT'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_IF = r'if'
t_ELSE = r'else'
t_PRINT = r'print'

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
)

def p_statement_assign(p):
    'statement : VARIABLE ASSIGN expr'
    p[0] = ('assign', p[1], p[3])

def p_statement_if_else(p):
    '''statement : IF expr statement ELSE statement
                 | IF expr statement'''
    if len(p) == 6:
        p[0] = ('if_else', p[2], p[3], p[5])
    else:
        p[0] = ('if', p[2], p[3])

def p_statement_print(p):
    'statement : PRINT LPAREN expr RPAREN'
    p[0] = ('print', p[3])

def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr'''
    p[0] = (p[2], p[1], p[3])

def p_expr_number(p):
    'expr : NUMBER'
    p[0] = ('number', p[1])

def p_expr_variable(p):
    'expr : VARIABLE'
    p[0] = ('variable', p[1])

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()

# Test the parser
while True:
    try:
        input_expr = input("Enter a MiniLang statement: ")
        result = parser.parse(input_expr)
        print("Parsed successfully:", result)
    except EOFError:
        break
