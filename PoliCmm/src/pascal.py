
import formatter
import ast
import copy


class Pascal (formatter.Formatter):

    current_function_id = None
    

    # translation
    t = {
        '+': '+',
        '-': '-',
        '*': '*',
        '/': 'DIV',
        'DIV': 'DIV',
        '%': 'MOD',
        'MOD': 'MOD',
        '==': '=',
        '!=': '<>',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>=',
        'int': 'INTEGER',
        'double': 'DOUBLE',
        'float': 'SINGLE',
        'char': 'CHAR',
        'bool': 'BOOLEAN',
        'string': 'STRING',
        'and': 'AND',
        'AND': 'AND',
        'or': 'OR',
        'OR': 'OR',
        'not': 'NOT',
        'NOT': 'NOT'
    }
    assignmentOperators = {
        '*=': '*',
        '/=': 'DIV',
        '%=': 'MOD',
        '+=': '+',
        '-=': '-',
        '&=': 'AND',
        '\|=': 'OR',
        '^=': 'XOR',
        '<<=': '', # no hay traduccion
        '>>=': '' # no hay traduccion
    }
    


    def vNode (self, node):
        '''Base rule.'''
        self.w('?'+node.__class__.__name__+'?')


    def createName(self, type):
        if isinstance(type, ast.StructType):
            return type.id
        elif isinstance(type, ast.VectorType):
            return type.type + self.createName(type.subtype)
        else:
            return type.type


    def CreateTypes(self, node):
        types = node.symtab.GetTypes()
        #print types
        typeBlock = False
        names = {}
        for tpe, name in types.iteritems():
            #print "type " + tpe.type + " " + name
            #if isinstance(tpe, ast.VectorType):
                #print "   subtype " + tpe.subtype.type
            names[name] = tpe
        order = node.symtab.OrderTypes()
        #print order
        #already_defined = ['vectorint']
        for name in order:
            tpe = names[name]
            tpe = tpe.resolveType()
            #if name in already_defined:
                #continue
            if isinstance(tpe, ast.VectorType):
                if not typeBlock:
                    self.pi('TYPE')
                typeBlock = True
                self.w(name)
                self.w('(')
                innertpe = tpe
                ind = 1
                while isinstance(innertpe, ast.VectorType):
                    if ind > 1:
                        self.w(';')
                    self.w('n%d : INTEGER' % ind)
                    innertpe = innertpe.subtype
                    ind = ind + 1
                self.w(')')
                self.w('=')
                self.w('ARRAY [')
                for ind2 in range(1, ind):
                    if ind2 > 1:
                        self.w(',')
                    self.w('0')
                    self.w('..')
                    self.w('n%d' % ind2)
                self.w('] OF ')
                self.visit(innertpe)
                self.p(';')
                self.w(name+"Ptr")
                self.w('=')
                self.w('^')
                self.w(name)
                self.p(';')
            if isinstance(tpe, ast.StructType):
                if not typeBlock:
                    self.pi('TYPE')
                typeBlock = True
                self.w(name)
                self.w('=')
                self.pi('RECORD')
                for id, tpe in tpe.elements.iteritems():
                    self.w(id)
                    self.w(':')
                    self.visit(tpe)
                    self.p(';')
                self.u()
                self.p('END;')
        if typeBlock:
            self.pu()
            
    def CreateSortCall(self, func_name, tpe, comp_name):
        self.p('procedure q%s(var v : %sPtr; left : Integer; right : Integer);' % (func_name, self.createName(tpe.resolveType())))
        self.p('Var l_ptr, r_ptr, pivot_ptr : Integer;')
        self.w('Var pivot :')
        self.visit(tpe.subtype.resolveType())
        self.p(';')
        self.pi('begin')
        self.p('l_ptr := left;')
        self.p('r_ptr := right;')
        self.p('pivot := v^[left];')
        self.p('while (left < right) do')
        self.pi('begin')
        if comp_name == 'standardless':
            self.pi('while ((v^[right] >= pivot) AND (left < right)) do')
        else:
            self.pi('while ((not %s(v^[right], pivot)) AND (left < right)) do' % comp_name)
        self.pu('right := right - 1;')
        self.p('if (left <> right) then')
        self.pi('begin')
        self.p('v^[left] := v^[right];')
        self.pu('left := left + 1;')
        self.p('end;')
        if comp_name == 'standardless':
            self.pi('while ((v^[left] <= pivot) AND (left < right)) do')
        else:
            self.pi('while ((not %s(pivot, v^[left])) AND (left < right)) do' % comp_name)
        self.pu('left := left + 1;')
        self.p('if (left <> right) then')
        self.pi('begin')
        self.p('v^[right] := v^[left];')
        self.pu('right := right - 1;')
        self.pu('end;')
        self.p('end;')
        self.p('v^[left] := pivot;')
        self.p('pivot_ptr:= left;')
        self.p('left := l_ptr;')
        self.p('right := r_ptr;')
        self.pi('if (left < pivot_ptr) then')
        self.pu('q%s(v, left, pivot_ptr-1);' % func_name)
        self.pi('if (right > pivot_ptr) then')
        self.pu('q%s(v, pivot_ptr+1, right);' % func_name)
        self.u()
        self.p('end;')
        
        
        self.p()
        
        
        self.p('procedure %s(var v : %sPtr);' % (func_name, self.createName(tpe.resolveType())))
        self.pi('begin')
        self.pu('q%s(v, 0, High(v^) - 1);' % func_name)
        self.p('end;')

    
    def CreateSortCalls(self, node):
        calls = node.symtab.getSortCalls()
        for name, data in calls.iteritems():
            if data[1] == 'standardless':
                self.CreateSortCall(name, data[0].resolveType(), data[1])

    def vProgram (self, node):
        self.p('(* Translated to GPC Pascal with PoliCmm *)')
        self.p()
        self.p('PROGRAM MyProgram;')
        self.p('USES PascalLib;')
        self.p()
        #for l in open('lib/pascal.pas', 'r').readlines():
        #    self.p(l.replace('\n', ''))
        self.pi('')
        
        self.CreateTypes(node)
        self.CreateSortCalls(node)
        for c in node.children:
            if isinstance(c, ast.VariableDeclarationStatement): 
                c.isTopLevel = True
            self.visit(c)        
            if isinstance(c, ast.Function):
                deps = node.symtab.getSortCallsDependencies()
                #print deps
                sortcalls = deps.get(c.id, [])
                for callName in sortcalls:
                    allcalls = node.symtab.getSortCalls()
                    data = allcalls[callName]
                    self.CreateSortCall(callName, data[0].resolveType(), data[1])
        self.up('BEGIN')
        self.ipu('VAR ret : INTEGER := main();')
        self.p('END.')


    def vLineComment (self, node):
        self.w('(*' + node.text + ' *)')


    def vBlockComment (self, node):
        self.p('(*' + node.text + '*)')

    def vInclude (self, node):
        pass


    def vUsingNamespace (self, node):
        pass


    def vFunction (self, node):
        self.current_function_id = node.id
        self.p()
        proc = node.returnType.type == 'void'
        if proc: self.w('PROCEDURE')
        else: self.w('FUNCTION')
        self.w(node.id)            
        self.visit(node.params)
        if not proc:
            self.w(':')
            self.visit(node.returnType)
        self.p(';')

        if node.id == 'main':
            # hack for main
            block = copy.deepcopy(node.block)
            ret = ast.ReturnStatement(ast.IntLiteral(0))
            ret.symtab = node.symtab
            block.add(ret)
            self.visit(block)
        else:
            self.visit(node.block)
            
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
        if node.is_ref:
            self.w('VAR')
        self.w(node.id)
        self.w(':')
        self.visit(node.type)


    def vType (self, node):
        #tpe = self.t.get(node.type, 'error')
        self.w(self.t.get(node.type, 'error'))
        
    def createName(self, type):
        if isinstance(type, ast.StructType):
            return type.id
        elif isinstance(type, ast.VectorType):
            return type.type + self.createName(type.subtype)
        else:
            return type.type
            
    def vVectorType (self, node):
        if node.hasTypeName:
            self.w(self.createName(node.resolveType())+"Ptr")
            #self.w(node.symtab.getTypeName(node))
        else:
            self.w('ARRAY')
            if node.size:
                self.w(' [0 .. ')
                self.visit(node.size)
                self.w(']')
            self.w(' OF ')
            self.visit(node.subtype)
        
        
    def vCustomType (self, node):
        #print node.type
        tpe = node.resolveType()
        #print tpe.type
        tpe = tpe.resolveType()
        #print tpe.type
        tpe.symtab = node.symtab
        self.visit(tpe)

    def vParenthesis (self, node):
        self.w('(')
        self.visit(node.expr)
        self.w(')')

    def vCompoundStatement (self, node):
        self.pi('BEGIN')
        first = True
        for c in node.children:
            if first: first = False
            else: self.p(';')
            self.visit(c)
        self.pu(';')
        self.w('END')


    def vCinStatement (self, node):
        if node.is_expression:
            first = True
            self.w('(')
            for c in node.children:
                if first: first = False
                else: 
                    self.w('AND')
                tpe = c.resolveType()
                aux = tpe.type
                if tpe.isFloat():
                    aux = 'single'
                    
                self.w('read%s(' % aux)
                self.visit(c)
                self.w(')')
            self.w(')')
        else:
            first = True
            for c in node.children:
                if first: first = False
                else: 
                    self.w(';')
                tpe = c.resolveType()
                aux = tpe.type
                if tpe.isFloat():
                    aux = 'single'
                self.w('pread%s(' % aux)
                self.visit(c)
                self.w(')')

    def vCoutModifier (self, node):
        if node.func == 'precision':
            self.w('precision := ')
            self.visit(node.param_list.children[0])

    def vCoutStatement (self, node):
        first = True
        for c in node.children:
            if first: first=False
            else:
				self.w(';')
				self.p()	
            self.visit(c)
            
    def vCoutElement (self,node):
        tpe = node.element.resolveType()
        if tpe.isDouble() or tpe.isFloat() or tpe.isBool():
            aux = tpe.type
            if tpe.isFloat():
                aux = 'single'
            if tpe.isBool():
                aux = 'boolean'
            self.w('write%s' % aux)
            self.w('(')
            self.visit(node.element)
            self.w(')')
        else:
            self.w('write (')
            self.visit(node.element)
            self.w(')')

    def vCoutBreakLine (self,node):
        self.w('WRITELN')
            
    def vWhileStatement (self, node):
        self.w('WHILE')
        if not node.cond.resolveType().isBool():
            cast = ast.CastExpression(ast.Type('bool'), node.cond)
            cast.type.symtab = node.symtab
            cast.symtab = node.symtab
            self.visit(cast)
        else:
            self.visit(node.cond)
        self.w('DO')
        self.pi('BEGIN')
        self.visit(node.loop)
        self.pu()
        self.w('END')
        
        
    def vWhileStatementCin (self, node):
        self.p()
        self.w('WHILE')
        self.w('NOT EOF')
        self.w('DO')
        self.pi('BEGIN')
        
        
        self.visit(node.cin_cond)
        self.w(';')
        
        self.visit(node.loop)
        self.pu(';')
    
        self.w('END')

            
    def vIfStatement (self, node):
        self.w('IF')
        if not node.cond.resolveType().isBool():
            cast = ast.CastExpression(ast.Type('bool'), node.cond)
            cast.type.symtab = node.symtab
            cast.symtab = node.symtab
            self.visit(cast)
        else:
            self.visit(node.cond)
        #self.visit(node.cond)
        self.w('THEN')
        self.pi('BEGIN')
        self.visit(node.then)
        self.pu(';')
        self.w('END')
        if node.elze:
            self.p()
            self.w('ELSE')
            self.pi('BEGIN')
            self.visit(node.elze)
            self.pu(';')
            self.w('END')
            

    def vCastExpression (self, node):
        tpe = node.expression.resolveType()
        if tpe.isInt() and node.type.isFloatingPoint():
            self.w('castint2%s(' % node.type.type);
            self.visit(node.expression)
            self.w(')')
        elif node.type.resolveType().isInt() and tpe.isFloatingPoint():
            self.w('cast%s2int(' % tpe.type);
            self.visit(node.expression)
            self.w(')')
        elif node.type.resolveType().isString():
            self.visit(node.expression)
        elif node.type.resolveType().isBool() and tpe.isInt():
            op = ast.BinaryOp(node.expression, '!=', ast.IntLiteral('0'))
            op.symtab = node.symtab
            op.right.symtab = node.symtab
            self.visit(op)
        else:
            self.visit(node.type.resolveType())
            self.w('(')
            self.visit(node.expression)
            self.w(')')
            
    def vConstructor (self, node):
        if len(node.params.children) > 1 or len(node.params.children) == 0:
            print "Constructors are only allowed for simple params if not in variable declarations"
        else:
            tpe = node.params.children[0].resolveType()
            if tpe.isInt() and node.type.isFloatingPoint():
                self.w('castint2%s(' % node.type.type);
                self.visit(node.params.children[0])
                self.w(')')
            elif node.type.isInt() and tpe.isFloatingPoint():
                self.w('cast%s2int(' % tpe.type);
                self.visit(node.params.children[0])
                self.w(')')
            else:
                self.visit(node.type)
                self.w('(')
                self.visit(node.params.children[0])
                self.w(')')

    def vAssignmentStatement (self, node):
        if isinstance(node.expr, ast.Constructor) and node.expr.type.resolveType().isVector():
            self.w('New')
            self.w('(')
            self.visit(node.lval)
            cons = node.expr
            while isinstance(cons, ast.Constructor):
                self.w(',')
                #print cons.params
                self.visit(cons.params.children[0])
                if len(cons.params.children) == 1:
                    cons = None
                    break
                else:
                    cons =  cons.params.children[1]
            if cons != None:
                print '****************Need to initialize******************'
            self.w(')')
        elif isinstance(node.expr, ast.AssignmentStatement):
            self.visit(node.expr)
            self.p(';')
            tmp = node.expr
            if isinstance(node.expr.lval, str):
                node.expr = ast.Identifier(node.expr.lval)
            else: 
                node.expr = node.expr.lval
            node.expr.symtab = node.symtab
            self.visit(node)
            node.expr = tmp
        else:
            ident = node.lval
            ident.symtab = node.symtab
            oldexpr = node.expr
            if node.operator != '=':
                node.expr = ast.BinaryOp(ident, self.assignmentOperators[node.operator], ast.Parenthesis(node.expr))
                node.expr.symtab = node.symtab
            tpe_ident = ident.resolveType().type
            tpe_expr = node.expr.resolveType().type
            #if isinstance(ident.resolveType(), ast.StructType):
                #print ident.resolveType().id
            #print tpe_ident
            #if isinstance(node.expr.resolveType().resolveType(), ast.StructType):
                #print node.expr.resolveType().resolveType().id
            #print tpe_expr
            if tpe_ident != tpe_expr and not ((tpe_ident == 'float' and tpe_expr == 'double') or (tpe_ident == 'double' and tpe_expr == 'float')):
                node.expr = ast.CastExpression(ast.Type(tpe_ident), node.expr)
                node.expr.symtab = node.symtab
            self.visit(node.lval)
            self.w(':=')
            self.visit(node.expr)
            node.expr = oldexpr
			

    def vReturnStatement (self, node):
        if not node.expr:
            self.w('RETURN')
        else:
            tpe = node.symtab.getReturnType().resolveType()
            if isinstance(node.expr, ast.Constructor) and len(node.expr.params.children) > 0 and node.expr.params.children[0].resolveType().type == node.expr.resolveType().type:
                self.w('RETURN')
                self.visit(node.expr.params.children[0])
            elif isinstance(node.expr, ast.Constructor):
                print node.expr.params.children[0].resolveType()
                self.pi('BEGIN')
                decl = ast.VariableDeclaration('auxaux')
                decl.type = node.expr.type
                decl.params = node.expr.params
                decl.symtab = node.expr.symtab
                self.visit(decl)
                self.p(';')
                self.w('RETURN')
                self.w('auxaux')
                self.w(';')
                self.pu()
                self.w('END')
            else:
                self.w('RETURN')
                if tpe.type != node.expr.resolveType().type:
                    self.visit(ast.CastExpression(tpe, node.expr))
                else:
                    self.visit(node.expr)

    #TODO: Commas should not be written when in program!
    def vVariableDeclarationStatement (self, node):
        first = True
        for c in node.children:
            if not node.isTopLevel:
                if first: 
                    first = False
                else:
                    self.p(';')
            c.isTopLevel = node.isTopLevel
            self.visit(c)       
            if node.isTopLevel:
                self.p(';')
            
    def initializeVectorType(self, tpe, node):
        tpe = tpe.resolveType()
        if (tpe.isVector() or tpe.isString()) and node.params:
            tpe.size = node.params.children[0]
            if len(node.params.children) > 1:
                tpe.cons = node.params.children[1]
                if isinstance(tpe, ast.VectorType):
                    tpe.subtype = self.initializeVectorType(tpe.subtype.resolveType(), node.params.children[1])
        return tpe
        
    def initializeVector(self, node, tpe, indices, idx, id):
        self.pi('BEGIN')
        name_iter = 'aux_i%d' % idx
        indices.append(name_iter)
        self.p('VAR %s : INTEGER = 0;' % name_iter)
        self.w('FOR %s := 0 TO (' % name_iter)
        self.visit(node.params.children[0])
        self.p(' - 1) DO ')
        if (len(node.params.children) > 1) and isinstance(node.params.children[1], ast.Constructor):
            self.pi('BEGIN')
            self.initializeVector(node.params.children[1], tpe.subtype, indices, idx + 1, id)
            self.pu()
            self.w('END')
        else:
            self.i()
            self.w(id)
            if tpe.type != 'string':
                self.w('^')
            self.w('[')
            first = True
            for idx in indices:
                if not first:
                    self.w(',')
                first = False
                self.w(idx)
                if isinstance(tpe, ast.Type) and tpe.type == 'string':
                    self.w('+ 1')
            self.w(']')
            self.w(' := ')
            self.visit(node.params.children[1])
            self.pu(';')
        self.pu()
        self.w('END')
        
    def needsInitialization(self, node):
        if (len(node.params.children) > 1) and isinstance(node.params.children[1], ast.Constructor):
            return self.needsInitialization(node.params.children[1])
        elif len(node.params.children) > 1:
            return True
        else:
            return False
            

    def vVariableDeclaration (self, node):
        tpe = node.type.resolveType()
        tpe.symtab = node.symtab
        if tpe.isVector() and node.params:
            self.w('VAR')
            self.w(node.id)
            self.w(':')
            if tpe.isVector() or tpe.isString():
                #print "initVectorType" + tpe.type
                tpe = self.initializeVectorType(tpe, node)
                tpe.symtab = node.symtab

            self.visit(tpe)
            
            if tpe.isVector() and node.params:
                self.p(';')
                self.w('New')
                self.w('(')
                self.w(node.id)
                t = tpe
                while t.isVector():
                    if t.size != None:
                        self.w(',')
                        self.visit(t.size)
                    else:
                        print 'Vectors need to be initialized fully at creation.'
                        break
                    t = t.subtype
                self.w(')')
            if (tpe.isVector() or tpe.isString()) and node.params and len(node.params.children) == 2:
                self.w(';')
                if self.needsInitialization(node):
                    self.p(';')
                    self.initializeVector(node, node.type.resolveType(), [], 1, node.id)
            
            return
        if tpe.constant and node.isTopLevel:
            self.w('CONST')
        else:
            self.w('VAR')
        self.w(node.id)
        self.w(':')
        if tpe.isVector() or tpe.isString():
            #print "initVectorType" + tpe.type
            tpe = self.initializeVectorType(tpe, node)
            tpe.symtab = node.symtab

        self.visit(tpe)
        if tpe.isVector() and node.params:
            self.w('(')
            t = tpe
            while t.isVector():
                self.visit(t.size)
                if t.subtype.isVector():
                    self.w(',')
                t = t.subtype
            self.w(')')
        elif tpe.isString():
            if tpe.size:
                self.w('[')
                if not tpe.size.resolveType().isInt():
                    tpe_int = ast.Type('int')
                    tpe_int.symtab = node.symtab
                    cast = ast.CastExpression(tpe_int, tpe.size)
                    cast.symtab = node.symtab
                    self.visit(cast)
                else:
                    self.visit(tpe.size)
                self.w(']')
        
        if (tpe.isVector() or tpe.isString()) and node.params and len(node.params.children) == 2:
            if self.needsInitialization(node):
                self.p(';')
                self.initializeVector(node, node.type.resolveType(), [], 1, node.id)
                
        elif node.init:
            expr = node.init
            tpe_expr = expr.resolveType()
            tpe_ident = node.type
            if tpe_ident.type != tpe_expr.type  and not (tpe_ident.isFloatingPoint() and tpe_expr.isFloatingPoint()):
                expr = ast.CastExpression(tpe_ident, node.init)
            self.w('=')
            self.visit(expr)

    def vConstantType(self,node):
        self.w(self.t[node.type])
        
        
    def vIdentifier (self, node):
        self.w(node.id)


    def vLiteral (self, node):
        self.w(str(node.lit))
	
    def vStringLiteral (self, node):
		self.w('"' + node.lit + '"')
	
    def vCharLiteral (self, node):
		self.w("'" + node.lit + "'")


    def vBinaryOp (self, node): # falta and or xor bit a bit
        pascalOp=self.t[node.oper];
        if (pascalOp=='AND') or (pascalOp=='OR'): # podriamos necesitar para todos los operadores hacer un in!
            self.w('(')
            self.visit(node.left)
            self.w(')')
            self.w(pascalOp)
            self.w('(')
            self.visit(node.right)
            self.w(')')
        elif (pascalOp == 'DIV'):
            left_type  = node.left.resolveType().type
            right_type = node.right.resolveType().type
            divOp = 'DIV'
            if (left_type == 'float' or left_type == 'double' or right_type == 'float' or right_type == 'double'):
                divOp = '/'
                
            self.visit(node.left)
            self.w(divOp)
            self.visit(node.right)
        elif pascalOp == '-' or pascalOp == '+' or pascalOp == '=': 
            left_type  = node.left.resolveType().type
            right_type = node.right.resolveType().type
            #print "left " + left_type
            #print "right " + right_type
            if (left_type == 'char'):
                node.left = ast.CastExpression(ast.Type('int'), node.left)
                
            if (right_type == 'char'):
                node.right = ast.CastExpression(ast.Type('int'), node.right)
                
            self.visit(node.left)
            self.w(pascalOp)
            self.visit(node.right)
        else:
            self.visit(node.left)
            self.w(pascalOp)
            self.visit(node.right)

    def vUnaryOp (self, node):
        if node.oper=='++':
            if node.right.resolveType().type == 'int':
                id = 'Increment'
                if node.pre:
                    id = 'pre' + id
                else:
                    id = 'post' + id
                if node.isNodeStatement():
                    id = 'p' + id
                func = ast.FunctionCall(id, ast.ActualParametersList(node.right))
                func.symtab = node.symtab
                if node.isNodeStatement():
                    func.isStatement = True
                self.visit(func)
            else:
                binaryOp = ast.BinaryOp(node.right, '+', ast.IntLiteral(1))
                binaryOp.symtab = node.symtab
                assignment = ast.AssignmentStatement(node.right, '=', binaryOp)
                assignment.symtab = node.symtab
                self.visit(assignment)
        elif node.oper=='--':
            if node.right.resolveType().isInt():
                id = 'Decrement'
                if node.pre:
                    id = 'pre' + id
                else:
                    id = 'post' + id
                if node.isNodeStatement():
                    id = 'p' + id
                func = ast.FunctionCall(id, ast.ActualParametersList(node.right))
                func.symtab = node.symtab
                if node.isNodeStatement():
                    func.isStatement = True
                self.visit(func)
            else:
                binaryOp = ast.BinaryOp(node.right, '-', ast.IntLiteral(1))
                binaryOp.symtab = node.symtab
                assignment = ast.AssignmentStatement(node.right, '=', binaryOp)
                assignment.symtab = node.symtab
                self.visit(assignment)
            #binaryOp = ast.BinaryOp(node.right, '-', ast.IntLiteral(1))
            #binaryOp.symtab = node.symtab
            #assignment = ast.AssignmentStatement(node.right, '=', binaryOp)
            #assignment.symtab = node.symtab
            #self.visit(assignment)
        else:
            self.w(self.t[node.oper])
            self.visit(node.right)

    def vFunctionCall (self, node):
        if node.isSortCall:
            self.w(node.sortFuncName)
            self.w('(')
            self.visit(node.sortVector)
            self.w(')')
        elif node.callee and node.callee.resolveType().isVector() and node.id == 'size':
            self.w('High')
            self.w('(')
            self.visit(node.callee)
            if not isinstance(node.callee, ast.Reference):
                self.w('^')
            self.w(')')
        elif node.callee and node.callee.resolveType().isString() and node.id == 'size':
            self.w('Length')
            self.w('(')
            self.visit(node.callee)
            #self.w('^')
            self.w(')')
        else:
            funcname = node.symtab.resolveFunctionName(node.id, node.params)
            
            self.w(funcname)
            self.w('(')
            self.visit(node.params)
            self.w(')')
            #funcnames = node.symtab.GetFunctionName('__functionnames__')
            #funcs = funcnames.get(node.id, None)
            #if funcs:
                #bestCandidate = None
                #for long_name, tpe in funcs.iteritems():
                    #if len(tpe.params) == len(node.params.children):
                        #good = True
                        #for i in range(0, len(tpe.params)):
                            #if tpe.params[i].resolveType().type != node.params.children[i].resolveType().type:
                                #good = False
                        #if good:
                            #bestCandidate = long_name
                #if bestCandidate:
                    #self.w(bestCandidate)
                    #self.w('(')
                    #self.visit(node.params)
                    #self.w(')')
                #else:
                    #self.w(node.id[2:])
                    #self.w('(')
                    #self.visit(node.params)
                    #self.w(')')
            #else:
                #self.w(node.id)
                #self.w('(')
                #self.visit(node.params)
                #self.w(')')

    def vActualParametersList (self, node):
        first = True
        for c in node.children:
            if first: first = False
            else: self.w(',')
            self.visit(c)

    def vForStatement (self, node): 
        self.visit(node.init)
        self.w(';')
        self.p()
        self.w('WHILE')
        self.visit(node.cond)
        self.w('DO')
        if not isinstance(node.loop, ast.CompoundStatement):
            node.loop = ast.CompoundStatement(node.loop)
        node.incr.isStatement = True
        node.loop.add(node.incr)
        self.visit(node.loop)
        self.p()
        
    def vForStatementInit (self, node):
        self.p('BEGIN')
        self.i()
        self.visit(node.init)
        self.w(';')
        self.p()
        self.w('WHILE')
        self.visit(node.cond)
        self.w('DO')
        if not isinstance(node.loop, ast.CompoundStatement):
            node.loop = ast.CompoundStatement(node.loop)
        node.incr.isStatement = True
        node.loop.add(node.incr)
        self.visit(node.loop)
        self.pu()
        self.w('END')
        
    def vReference(self, node):
        if isinstance(node.value, ast.Reference):
            node.value.isNestedReference = True
        self.visit(node.value)
        if (not isinstance(node.value, ast.Reference)) and node.value.resolveType().isVector():
            self.w('^')
        tpe = node.value.resolveType()
        if isinstance(node.value, ast.Reference):
            self.w(',')
        else:
            self.w('[')
        self.visit(node.idx)
        if tpe.isString():
            self.w(' + 1')
        if not node.isNestedReference:
            self.w(']')

    def vStructReference(self, node):
        self.visit(node.object)
        self.w('.')
        self.w(node.id)
        
    def vStructType(self, node):
        self.w(node.id)
        
    def vTypeDef(self, node):
        pass
   
    def vStructDef(self, node):
        pass
    def vNullNode(self, node):
        pass