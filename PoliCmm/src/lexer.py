import ply.lex as lex

from ply.lex import TOKEN

# List of reserved words:
reserved_words = {
    'using'             :   'USING',
    'namespace'         :   'NAMESPACE', 
    'return'            :   'RETURN',
    'if'                :   'IF',
    'while'             :   'WHILE',
    'else'              :   'ELSE',
    'for'               :   'FOR',
    'const'             :   'CONST',
    'void'              :   'VOID',
    'int'               :   'INT',
    'float'             :   'FLOAT',
    'double'            :   'DOUBLE',
    'char'              :   'CHAR',
    'string'            :   'STRING',
    'bool'              :   'BOOL',
    'not'               :   'LNOT',
    'and'               :   'LAND',
    'or'                :   'LOR',
    'cout'              :   'COUT',             
    'cin'               :   'CIN',
    'endl'              :   'ENDL',
    'struct'            :   'STRUCT', 
    'true'              :   'TRUE',
    'false'             :   'FALSE',
    'vector'            :   'VECTOR',
    'typedef'           :   'TYPEDEF',
    'cerr'              :   'CERR'
}

# List of token names
tokens = [
    'IDENTIFIER',
    'INTEGER_LIT', 'REAL_LIT', 'CHAR_LIT', 'STRING_LIT',
    'LPAR', 'RPAR', 'LCOR', 'RCOR', 'LBRA', 'RBRA', 'LPUT','RPUT',
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'OR', 'AND', 'NOT', 'XOR',
    'LOR', 'LAND', 'LNOT',
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE', 'CONDOP',
    'EQUALS', 'MULTEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'ANDEQUAL', 'OREQUAL', 'XOREQUAL','LEFTSHIFTEQUAL','RIGHTSHIFTEQUAL',
    'PLUSPLUS', 'MINUSMINUS',
    'COMMA', 'SEMI', 'COLON', 'DOT', 'THREEDOTS', 'PTR',
    'LINECOM', 'BLOCKCOM',
    'INCLUDE', 'COLONCOLON', 'TYPEID'
]

# Add reserved words tokens
for rw, tok in reserved_words.items():
    if tok not in tokens:
        tokens.append(tok)


# Ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Operators
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULT              = r'\*'
t_DIV               = r'/'
t_MOD               = r'%'
t_OR                = r'\|'
t_AND               = r'&'
t_NOT               = r'~'
t_XOR               = r'\^'
t_LOR               = r'\|\|'
t_LAND              = r'&&'
t_LNOT              = r'!'
t_LPUT              = r'<<'
t_RPUT              = r'>>'
t_EQ                = r'=='
t_NE                = r'!='
t_LT                = r'<'
t_GT                = r'>'
t_LE                = r'<='
t_GE                = r'>='
t_CONDOP            = r'\?'

# Assignment operators
t_EQUALS            = r'='
t_MULTEQUAL        = r'\*='
t_DIVEQUAL          = r'/='
t_MODEQUAL          = r'%='
t_PLUSEQUAL         = r'\+='
t_MINUSEQUAL        = r'-='
t_ANDEQUAL          = r'&='
t_OREQUAL           = r'\|='
t_XOREQUAL          = r'^='
t_LEFTSHIFTEQUAL    = r'<<='
t_RIGHTSHIFTEQUAL   = r'>>=' 

# Increment/decrement
t_PLUSPLUS          = r'\+\+'
t_MINUSMINUS        = r'--'

# Delimeters
t_LPAR              = r'\('
t_RPAR              = r'\)'
t_LCOR              = r'\['
t_RCOR              = r'\]'
t_LBRA              = r'\{'
t_RBRA              = r'\}'
t_COMMA             = r','
t_DOT               = r'\.'
t_SEMI              = r';'
t_COLON             = r':'
t_COLONCOLON        = r'::'
t_THREEDOTS         = r'\.\.\.'
t_PTR               = r'->'


simple_escape = r"""([a-zA-Z\\?'"])"""
octal_escape = r"""([0-7]{1,3})"""
hex_escape = r"""(x[0-9a-fA-F]+)"""
bad_escape = r"""([\\][^a-zA-Z\\?'"x0-7])"""

escape_sequence = r"""(\\("""+simple_escape+'|'+octal_escape+'|'+hex_escape+'))'
cconst_char = r"""([^'\\\n]|"""+escape_sequence+')'    
char_const = "'"+cconst_char+"'"

string_char = r"""([^"\\\n]|"""+escape_sequence+')'    
string_literal = '"'+string_char+'*"'

# Pragmas
t_INCLUDE           = r'\#include'
typedefs = {}

def t_IDENTIFIER (t):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    t.type = reserved_words.get(t.value, 'IDENTIFIER')
    if t.type == 'IDENTIFIER':
        t.type = typedefs.get(t.value, 'IDENTIFIER')
    return t

def t_REAL_LIT (t) :
    r'([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)'
    t.value = t.value
    t.type= "REAL_LIT"
    return t

def t_INTEGER_LIT (t) :
    r'[0-9]+'
    t.value = int(t.value)
    t.type="INTEGER_LIT"
    return t



def t_CHAR_LIT (t) :
    r"'[ -~]'" # improve!
    t.value = t.value[1:-1]
    t.type="CHAR_LIT"
    return t
    
@TOKEN(string_literal)
def t_STRING_LIT (t) :
    #string_literal # improve!
    t.value = t.value[1:-1]
    t.type="STRING_LIT"
    return t

    
def t_LINECOM (t):
    r'//.*\n'
    t.value = t.value[2:-1]
    t.lexer.lineno += 1
    return t


def t_BLOCKCOM (t):
    r'\/\*(.|\n)*?\*\/'
    # In the above regexp. *? is the non-greedy version of *
    t.value = t.value[2:-2]
    return t


# Rule to track line numbers
def t_newline (t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print "Illegal character.'%s' " %t.value[0]
    raise Exception("Illegal character.")


# Build the lexer
lexer = lex.lex()
