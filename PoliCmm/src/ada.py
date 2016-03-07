
import formatter
import ast
import copy


class Ada (formatter.Formatter):

    current_function_id = None
    

    # translation
    t = {
        '+': '+',
        '-': '-',
        '*': '*',
        '/': 'DIV',
        '%': 'MOD',
        '==': '=',
        '!=': '/=',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>=',
        'int': 'INTEGER',
        'double': 'FLOAT',
        'char': 'CHARACTER',
        'bool': 'BOOLEAN',
        'string': 'STRING',
    }


    def vNode (self, node):
        '''Base rule.'''
        self.w('?'+node.__class__.__name__+'?')


    def vProgram (self, node):
        self.p('-- Translated to GNAT Ada with PoliCmm')
        self.p()
        self.p('WITH Ada.Text_IO;')
        self.pi('')
        for c in node.children:
            self.visit(c)        
        self.up('PROCEDURE Program IS')
        self.ipu('ret : INTEGER;')
        self.p('BEGIN')
        self.ipu('ret := main();')
        self.p('END Program;')


    def vLineComment (self, node):
        self.p('--' + node.text)


    def vBlockComment (self, node):
        for lines in node.text.split('\n'):
            self.p('--' + lines)
        self.p()

    def vInclude (self, node):
        pass


    def vUsingNamespace (self, node):
        pass


    def vFunction (self, node):
        self.current_function_id = node.id
        self.p()
        proc = node.type.type == 'void'
        if proc: self.w('PROCEDURE')
        else: self.w('FUNCTION')
        self.w(node.id)            
        self.visit(node.params)
        if not proc:
            self.w('RETURN')
            self.visit(node.type)
        self.p('IS')

        self.pi('BEGIN')
        if node.id == 'main':
            # hack for main
            block = copy.deepcopy(node.block)
            block.add(ast.ReturnStatement(ast.Literal(0)))
            self.visit(block)
        else:
            self.visit(node.block)
        self.uw('END')
        self.w(self.current_function_id)
        self.p(';')
        self.p()
        self.current_function_id = None
            

    def vFormalParametersList (self, node):
        self.w('(')
        first = True
        for c in node.children:
            if first: first = False
            else: self.w(';')
            self.visit(c)
        self.w(')')


    def vFormalParameter (self, node):
        self.w(node.id)
        self.w(':')
        self.visit(node.type)


    def vType (self, node):
        self.w(self.t[node.type])


    def vCompoundStatement (self, node):
        for c in node.children:
            self.visit(c)


    def vCinStatement (self, node):
        for c in node.children:
            self.w('read (')
            self.w(c.id)
            self.w(') ;')
        self.p()

            
    def vCoutStatement (self, node):
        for c in node.children:
            self.w('write (')
            self.visit(c)
            self.w(') ;')
        self.p()

            
    def vWhileStatement (self, node):
        self.w('WHILE')
        self.visit(node.cond)
        self.pi('LOOP')
        self.visit(node.loop)
        self.up('END LOOP ;')

            
    def vIfStatement (self, node):
        self.w('IF')
        self.visit(node.cond)
        self.pi('THEN')
        self.visit(node.then)
        if node.elze:
            self.upi('ELSE')
            self.visit(node.elze)
        self.up('END IF ;')
            

    def vAssignmentStatement (self, node):
        self.visit(node.lval)
        self.w(':=')
        self.visit(node.expr)
        self.p(';')


    def vReturnStatement (self, node):
        self.w('RETURN')
        self.visit(node.expr)
        self.p(';')


    def vVariableDeclarationStatement (self, node):
        for c in node.children:
            self.visit(c)            
            

    def vVariableDeclaration (self, node):
        self.w('VAR')
        self.w(node.id)
        self.w(':')
        self.visit(node.type)
        if node.init:
            self.w(':=')
            self.visit(node.init)
        self.p(';')
            
            
    def vIdentifier (self, node):
        self.w(node.id)


    def vLiteral (self, node):
        if type(node.lit)==str:
            self.w("'" + node.lit + "'")
        else:
            self.w(str(node.lit))


    def vBinaryOp (self, node):
        self.w('(')
        self.visit(node.left)
        self.w(')')
        self.w(self.t[node.oper])
        self.w('(')
        self.visit(node.right)
        self.w(')')


    def vFunctionCall (self, node):
        self.w(node.id)
        self.w('(')
        self.visit(node.params)
        self.w(')')


    def vActualParametersList (self, node):
        first = True
        for c in node.children:
            if first: first = False
            else: self.w(',')
            self.visit(c)

