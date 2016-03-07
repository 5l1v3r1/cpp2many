import ply.lex as lex
import ply.yacc as yacc
import lexer
import sys
import ast


tokens = lexer.tokens

precedence = (
    ('right', 'ELSE'),
)


def p_start (t):
    '''start : program'''
    t[0] = t[1]


def p_program_01 (t):
    '''program : program_part'''
    t[0] = ast.Program(t[1])

def p_program_02 (t):
    '''program : program program_part'''
    t[1].add(t[2])
    t[0] = t[1]


def p_program_part (t):
    '''program_part : include_directive
        | typedef
        | structdef
        | using_directive
        | function_definition
        | declaration_statement
        | comment
        '''
        
    t[0] = t[1]

def p_typedef_01 (t):
    '''typedef : typedef_body SEMI'''
    t[0] = t[1]
    
def p_typedef_body (t):
    '''typedef_body : TYPEDEF type IDENTIFIER'''
    lexer.typedefs[t[3]] = 'TYPEID'
    t[0] = ast.TypeDef(t[2], t[3])
    
def p_structdef (t):
    '''structdef : struct_name LBRA struct_elem_list RBRA SEMI'''
    t[3].id = t[1]
    t[0] = t[3]
    
def p_struct_name (t):
    '''struct_name : STRUCT IDENTIFIER'''
    print  "Added typeid " + t[2]
    lexer.typedefs[t[2]] = 'TYPEID'
    t[0] = t[2]
    
    
def p_struct_elem_list_01 (t):
    '''struct_elem_list : declaration_statement'''
    t[0] = ast.StructDef(t[1])
    
def p_struct_elem_list_02 (t):
    '''struct_elem_list : struct_elem_list declaration_statement''' 
    t[1].add(t[2])
    t[0] = t[1]
    
def p_struct_elem (t):
    '''struct_elem : type identifier_list SEMI'''
    for c in t[2].children:
        c.type = t[1]
    t[0] = t[2]

def p_identifier_list_01 (t):
    '''identifier_list : IDENTIFIER'''
    t[0] = ast.VariableDeclarationStatement(ast.VariableDeclaration(t[1]))

def p_identifier_list_02 (t):
    '''identifier_list : identifier_list COMMA IDENTIFIER'''
    t[1].add(ast.VariableDeclaration(t[3]))
    t[0] = t[1]

def p_comment_01 (t):
    '''comment : LINECOM'''
    t[0] = ast.LineComment(t[1])

def p_comment_02 (t):
    '''comment : BLOCKCOM'''
    t[0] = ast.BlockComment(t[1])


def p_include_directive_01 (t):
    '''include_directive : INCLUDE LT IDENTIFIER GT
        | INCLUDE LT STRING GT
        | INCLUDE LT VECTOR GT'''
    t[0] = ast.Include(t[3])

def p_include_directive_02 (t):
    '''include_directive : INCLUDE STRING_LIT'''
    t[0] = ast.Include(t[2])

def p_using_directive (t):
    '''using_directive : USING NAMESPACE IDENTIFIER SEMI'''
    t[0] = ast.UsingNamespace(t[3])


def p_function_definition_01 (t):
    '''function_definition : type IDENTIFIER LPAR  RPAR block'''
    t[0] = ast.Function(t[2], t[1], ast.FormalParametersList(), t[5])
    
    
def p_function_definition_02 (t):
    '''function_definition : type IDENTIFIER LPAR formal_parameters_list RPAR block'''
    t[0] = ast.Function(t[2], t[1], t[4], t[6])

def p_empty (t):
    '''empty :'''
    pass


def p_formal_parameters_list_01 (t):
    '''formal_parameters_list : formal_parameter'''
    t[0] = ast.FormalParametersList(t[1])   

def p_formal_parameters_list_02 (t):
    '''formal_parameters_list : formal_parameters_list COMMA formal_parameter'''
    t[1].add(t[3])
    t[0] = t[1]
    

def p_formal_parameter_01 (t):
    '''formal_parameter : type IDENTIFIER'''
    t[0] = ast.FormalParameter(t[2], t[1])
    t[0].is_ref = False
    
def p_formal_parameter_02 (t):
    '''formal_parameter : type AND IDENTIFIER'''
    t[0] = ast.FormalParameter(t[3], t[1])
    t[0].is_ref = True
    t[0].type.is_reference = True

def p_statement_list_01 (t):
    '''statement_list : statement'''
    t[1].isStatement = True
    t[0] = ast.CompoundStatement(t[1])
    
def p_statement_list_02 (t):
    '''statement_list : statement_list statement'''
    t[2].isStatement = True
    t[1].add(t[2])
    t[0] = t[1]

    
def p_statement (t):
    '''statement : declaration_statement
        | cout_statement
        | cin_statement
        | while_statement
        | for_statement
        | if_statement
        | assignment_statement
        | return_statement
        | block
        | comment
        | empty_statement
        '''
 #              | while_statement_cin
    t[0] = t[1]


def p_empty_statement (t):
    '''empty_statement : '''
    t[0] = ast.NullNode()

def p_block (t):
    '''block : LBRA statement_list RBRA'''
    t[0] = t[2]


def p_cout_statement_01 (t):
    '''cout_statement : COUT cout_elements_list SEMI'''
    t[0] = t[2]
    
def p_cout_statement_02 (t):
    '''cout_statement : CERR cout_elements_list SEMI'''
    t[0] = t[2]
    
def p_cout_statement_03 (t):
    '''cout_statement : COUT DOT IDENTIFIER LPAR actual_parameters_list RPAR SEMI'''
    t[0] = ast.CoutModifier(t[3], t[5])
    
def p_cout_statement_04 (t):
    '''cout_statement : CERR DOT IDENTIFIER LPAR actual_parameters_list RPAR SEMI'''
    t[0] = ast.CoutModifier(t[3], t[5])
    

def p_cout_elements_list_01 (t):
    '''cout_elements_list : LPUT cout_element'''
    t[0] = ast.CoutStatement(t[2])
    
def p_cout_elements_list_02 (t):
    '''cout_elements_list : cout_elements_list LPUT cout_element'''
    t[1].add(t[3])
    t[0] = t[1]

def p_cout_element_01 (t):
    '''cout_element : ENDL'''
    t[0] = ast.CoutBreakLine();
        
def p_cout_element_02 (t):
    '''cout_element : lor_expression'''
    t[0] = ast.CoutElement(t[1])



def p_cin_bloc (t):
    '''cin_bloc : CIN cin_elements_list'''
    t[0] = t[2]
    t[0].is_expression = True
    
def p_cin_statement (t):
    '''cin_statement : CIN cin_elements_list SEMI'''
    t[0] = t[2]
    t[0].is_expression = False
    
def p_cin_elements_list_01 (t):
    '''cin_elements_list : RPUT reference_expression'''
    t[0] = ast.CinStatement(t[2])
  
def p_cin_elements_list_02 (t):
    '''cin_elements_list : cin_elements_list RPUT reference_expression'''
    t[1].add(t[3])
    t[0] = t[1]



def p_literal_01 (t):
    '''literal : INTEGER_LIT'''
    t[0]=ast.IntLiteral(t[1])
    
def p_literal_02 (t):
    '''literal : REAL_LIT'''
    t[0]=ast.FloatLiteral(t[1])
    
def p_literal_03 (t):
    '''literal : TRUE
                | FALSE'''
    t[0]=ast.BoolLiteral(t[1])
   
def p_literal_04 (t):
	'''literal : STRING_LIT'''
	t[0]=ast.StringLiteral(t[1])
	   
def p_literal_05 (t):
	'''literal : CHAR_LIT'''
	t[0]=ast.CharLiteral(t[1])
	
def p_factor_01 (t):
    '''factor : literal'''
    t[0] = t[1]
	   
def p_factor_02 (t):
    '''factor : reference_expression''' 
    t[0] = t[1]
    
def p_factor_03(t):
    '''factor : LPAR assignment_expression RPAR'''
    t[0] = ast.Parenthesis(t[2])

def p_factor_04 (t):
    '''factor : IDENTIFIER LPAR actual_parameters_list RPAR''' 
    t[0] = ast.FunctionCall(t[1], t[3])    
    
def p_factor_05 (t):
    '''factor : IDENTIFIER COLONCOLON assignment_expression''' 
    t[0] = t[3]
    
def p_factor_06 (t):
    '''factor : reference_expression DOT IDENTIFIER LPAR actual_parameters_list RPAR'''
    t[0] = ast.FunctionCall(t[3], t[5], t[1])
    
def p_factor_07 (t):
    '''factor : type LPAR actual_parameters_list RPAR'''
    t[0] = ast.Constructor(t[1], t[3])
    
    
def p_factor_08 (t):
    '''factor : LPAR type RPAR assignment_expression'''
    t[0] = ast.CastExpression(t[2], t[4])
    
def p_reference_expression_01 (t):
    '''reference_expression : IDENTIFIER'''
    t[0] = ast.Identifier(t[1])
    
def p_reference_expression_02 (t):
    '''reference_expression : reference_expression LCOR relational_expression RCOR'''
    t[0] = ast.Reference(t[1], t[3])
    
def p_reference_expression_03 (t):
    '''reference_expression : reference_expression DOT IDENTIFIER'''
    t[0] = ast.StructReference(t[1], t[3])

def p_unary_expression_01(t):
    '''unary_expression : unary_operator factor
        | PLUSPLUS unary_expression
        | MINUSMINUS unary_expression
        '''
    t[0]=ast.UnaryOp(t[1],t[2])
    t[0].pre = True
    
def p_unary_expression_02(t):
    '''unary_expression : unary_expression PLUSPLUS
        | unary_expression MINUSMINUS
        '''
    t[0]=ast.UnaryOp(t[2],t[1])
    t[0].pre = False

def p_unary_expression_03(t):
	'''unary_expression : factor
	'''
	   
        
	t[0]=t[1]

# me faltara tema ++

def p_cast_expression_01(t):
	'''
		cast_expression : unary_expression
	'''
	t[0]=t[1]

def p_cast_expression_02(t):
	'''
		cast_expression : type LPAR lor_expression RPAR
	'''
	t[0]=ast.CastExpression(t[1],t[3])


def p_multiplicative_expression_01(t):
	'''
		multiplicative_expression : unary_expression
	'''
	t[0]=t[1]

def p_multiplicative_expression_02(t):
	'''
		multiplicative_expression : multiplicative_expression multiplicative_operator unary_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3]);


def p_additive_expression_01(t):
	'''
		additive_expression : multiplicative_expression	
	'''
	t[0]=t[1]

def p_additive_expression_02(t):
	'''
		additive_expression : additive_expression additive_operator multiplicative_expression	
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])
	

#def p_shift_expression_01(t):
	#'''
		#shift_expression : additive_expression 
	#'''
	#t[0]=t[1]
	
#def p_shift_expression_02(t):
	#'''
		#shift_expression : shift_expression shift_operator additive_expression
	#'''
	#t[0]=ast.BinaryOp(t[1],t[2],t[3])


def p_relational_expression_01(t):
	'''
		relational_expression : additive_expression
	'''
	t[0]=t[1]
	
def p_relational_expression_02(t):
	'''
		relational_expression : relational_expression relational_operator additive_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])


def p_equality_expression_01(t):
	'''
		equality_expression : relational_expression
	'''
	t[0]=t[1]

def p_equality_expression_02(t):
	'''
		equality_expression : equality_expression equality_operator relational_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])	

def p_and_expression_01(t):
	'''
		and_expression : equality_expression
	'''
	t[0]=t[1]	

def p_and_expression_02(t):
	'''
		and_expression : and_expression AND equality_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])	

def p_xor_expression_01(t):
	'''
		xor_expression : and_expression
	'''
	t[0]=t[1]	

def p_xor_expression_02(t):
	'''
		xor_expression : xor_expression XOR and_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])	

def p_or_expression_01(t):
	'''
		or_expression : xor_expression
		| cin_bloc
	'''
	t[0]=t[1]	

def p_or_expression_02(t):
	'''
		or_expression : or_expression OR xor_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])	

	
def p_land_expression_01(t):
	'''
		land_expression : or_expression
	'''
	t[0]=t[1]	

def p_land_expression_02(t):
	'''
		land_expression : land_expression LAND or_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])	

	
def p_lor_expression_01(t):
	'''
		lor_expression : land_expression
	'''
	t[0]=t[1]	

def p_lor_expression_02(t):
	'''
		lor_expression : lor_expression LOR land_expression
	'''
	t[0]=ast.BinaryOp(t[1],t[2],t[3])


def p_assignment_expression_01(t):
	'''
		assignment_expression : lor_expression
	'''
	t[0]=t[1]	

def p_assignment_expression_02(t): # a=b=3
	'''
		assignment_expression :  reference_expression assignment_operator assignment_expression
	'''
	t[0]=ast.AssignmentStatement(t[1],t[2],t[3]) # ojo q se puede liar una buena asignandoCONTROLAR			
	



def p_declaration_statement_01(t):
	'''
		declaration_statement : type declaration_list SEMI
	'''
	# para cada elemento de la declarator list crear un nodo declaracion
	for c in t[2].children:
		c.type=t[1]
	t[0]=t[2]


#def p_declaration_statement_02(t):
    #'''
        #declaration_statement : declaration_statement_init
    #'''
    ## para cada elemento de la declarator list crear un nodo declaracion

    #t[0]=t[1]
	
#def p_declaration_statement_init(t):
    #'''
        #declaration_statement_init : type declaration_list EQUALS initializer SEMI
    #'''
    ## para cada elemento de la declarator list crear un nodo declaracion

    #for c in t[2].children:
        #c.type=t[1]
        #c.init=t[4]
    #t[0]=t[2]




#def p_declaration_statement_03(t):
#	'''
#		declaration_statement : struct ID LBRA RBRA
#	'''
	

	
def p_declaration_list_01(t):
	'''
		declaration_list : declaration_list COMMA declaration
	'''
	t[1].add(t[3])
	t[0]=t[1]
	
def p_declaration_list_02(t):
	'''
		declaration_list : declaration
	'''
	t[0]=ast.VariableDeclarationStatement(t[1])		

def p_declaration_01(t):
    '''
        declaration : IDENTIFIER
    '''
    t[0]=ast.VariableDeclaration(t[1])


def p_declaration_02(t):
    '''
        declaration : IDENTIFIER EQUALS initializer
    '''
    t[0]=ast.VariableDeclaration(t[1])
    t[0].init = t[3]

def p_declaration_03(t):
    '''
        declaration : IDENTIFIER LPAR actual_parameters_list RPAR
    '''
    t[0]=ast.VariableDeclaration(t[1])
    t[0].params = t[3]
    
    
def p_declaration_04(t):
    '''
        declaration : IDENTIFIER LPAR  RPAR
    '''
    t[0]=ast.VariableDeclaration(t[1])
    t[0].cons = ast.ActualParametersList()



	
def p_initializer(t): # ampliable con vectores
	'''
		initializer : lor_expression
	'''
	t[0]=t[1]
	
	
	
def p_assignment_statement(t):
	'''
		assignment_statement : assignment_expression SEMI
	'''
	t[0]=t[1]
	

def p_type_01 (t):
    '''type : TYPEID'''
    t[0] = ast.CustomType(t[1])
    
def p_type_02 (t):
    '''type : VOID
        | INT
        | FLOAT
        | DOUBLE
        | CHAR
        | BOOL
        | STRING'''
    t[0] = ast.Type(t[1])   
    
    

def p_type_03 (t): #PRODUCE AMBIGUEDAD
    '''type : CONST type'''
    t[0] = t[2]
    t[0].constant = True

def p_type_04 (t):
    '''type : VECTOR LT type GT'''
    t[0] = ast.VectorType(t[1], t[3])

def p_unary_operator(t):
	'''
		unary_operator : MINUS 
		| LNOT
	'''
	t[0]=t[1]
	
def p_multiplicative_operator(t):
	''' 
		multiplicative_operator : MULT
		| DIV
		| MOD
	'''
	t[0]=t[1]
	
def p_additive_operator(t):
	'''
		additive_operator : PLUS
		| MINUS
	'''
	t[0]=t[1]

def p_shift_operator(t):
	'''
		shift_operator : RPUT
		| LPUT
	'''
	t[0]=t[1]
	
def p_relational_operator(t):
	'''
		relational_operator : GT
		| LT
		| LE
		| GE
	'''
	t[0]=t[1]
	

def p_equality_operator(t):
	'''
		equality_operator : EQ
		| NE
	'''
	t[0]=t[1]

def p_assignment_operator(t):
	'''
		assignment_operator : EQUALS
		| MULTEQUAL
		| DIVEQUAL
		| MODEQUAL
		| PLUSEQUAL
		| MINUSEQUAL
		| ANDEQUAL
		| OREQUAL
		| XOREQUAL
		| RIGHTSHIFTEQUAL
		| LEFTSHIFTEQUAL
	'''
	t[0]=t[1]
	

def p_while_statement_01 (t):
    '''while_statement : WHILE LPAR lor_expression RPAR statement'''
    t[0] = ast.WhileStatement(t[3], t[5])
    t[5].isStatement = True
    
    
def p_while_statement_02 (t):
    '''while_statement : WHILE LPAR lor_expression RPAR SEMI'''
    t[0] = ast.WhileStatement(t[3], ast.NullNode())

#def p_while_statement_cin (t):
    #'''while_statement_cin : WHILE LPAR cin_bloc RPAR statement'''
    #t[0] = ast.WhileStatementCin(t[3], t[5])
    
def p_for_statement (t):
    '''for_statement : FOR LPAR assignment_statement assignment_statement assignment_expression RPAR statement'''
    t[0] = ast.ForStatement(t[3], t[4], t[5], t[7])
    t[7].isStatement = True
    
def p_for_statement_init (t):
    '''for_statement : FOR LPAR declaration_statement assignment_statement assignment_expression RPAR statement'''
    t[0] = ast.ForStatementInit(t[3], t[4], t[5], t[7])
    t[7].isStatement = True

def p_if_statement_01 (t):
    '''if_statement : IF LPAR assignment_expression RPAR statement'''
    t[0] = ast.IfStatement(t[3], t[5])
    t[5].isStatement = True

def p_if_statement_02(t):
    '''if_statement : IF LPAR assignment_expression RPAR statement ELSE statement'''
    t[0] = ast.IfStatement(t[3], t[5], t[7])
    t[5].isStatement = True
    t[7].isStatement = True


def p_return_statement_01 (t):
    '''return_statement : RETURN assignment_statement'''
    t[0] = ast.ReturnStatement(t[2])

def p_return_statement_02 (t):
    '''return_statement : RETURN SEMI'''
    t[0] = ast.ReturnStatement(None)


def p_actual_parameters_list_01 (t):
    '''actual_parameters_list : empty'''
    t[0] = ast.ActualParametersList()   

def p_actual_parameters_list_02 (t):
    '''actual_parameters_list : actual_parameter'''
    t[0] = ast.ActualParametersList(t[1])   

def p_actual_parameters_list_03 (t):
    '''actual_parameters_list : actual_parameters_list COMMA actual_parameter'''
    t[1].add(t[3])
    t[0] = t[1]

    
def p_actual_parameter (t):
    '''actual_parameter : assignment_expression'''
    t[0] = t[1]
    

    
    


def p_error (t):
    print 'Syntax error around line %d in token %s.' % (t.lineno, t.type)
    yacc.errok()
    #raise Exception('Syntax error around line %d in token %s.' % (t.lineno, t.type))




# Build the parser
parser = yacc.yacc()



