import visitor
import pascal
import sys
import ast

class Symtab:
    """A symbol table.  This is a simple object that just keeps a
    hashtable of symbol names and the Declaration or FunctionDefn
    nodes that they refer to.

    There is a separate symbol table for each code element that
    has its own scope (for instance, each compound statement will
    have its own symbol table).  As a result, symbol tables can
    be nested if the code elements are nested, and symbol table
    lookups will recurse upwards through parents to represent
    lexical scoping rules."""

    class SymbolDefinedError(Exception):
        """Exception raised when the code tries to add a symbol
        to a table where the symbol has already been defined.
        Note that 'defined' is used in the C sense here--i.e.,
        'space has been allocated for the symbol', as opposed
        to a declaration."""

        pass

    class SymbolConflictError(Exception):
        """Exception raised when the code tries to add a
        symbol to a tamble where the symbol already exists
        and its type differs from the previously existing
        one."""
        
        pass

    def __init__(self, parent=None):
        """Creates an empty symbol table with the given
        parent symbol table."""
        
        self.entries = {}
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)
        self.children = []
    
    def add(self, name, value):
        """Adds a symbol with the given value to the symbol table.
        The value is usually an AST node that represents the
        declaration or definition of a function/variable (e.g.,
        Declaration or FunctionDefn)."""
        #print 'Name: %s, value %s '%(name,value)
        #pascal.Pascal(sys.stdout).visit(value)
        #print '\n'
        real_name = name
        if isinstance(value, ast.FunctionType):
            long_name = name
            for p in value.params:
                long_name = long_name + '_' + self.createName(p.resolveType())
            self.addFunctionName(name, long_name, value.resolveType())
            real_name = long_name
            
        if self.entries.has_key(real_name):
            print 'EEEE ' + name
            print value.type
            print self.entries[real_name]
            if not self.entries[real_name].extern:
                raise Symtab.SymbolDefinedError()
            # TODO Type equality verification
            #elif self.entries[name].type.get_string() != \
                 #value.type.get_string():
                #raise Symtab.SymbolConflictError()
        self.entries[real_name] = value
        return real_name
        
    def addFunctionName(self, name, long_name, tpe):
        if self.parent != None:
            self.parent.addFunctionName(name, long_name, tpe)
        else:
            names = self.entries.get('__functionnames__', {})
            values = names.get(name, {})
            if long_name in values:
                print 'Function definition repeated'
            values[long_name] = tpe
            names[name] = values
            self.entries['__functionnames__'] = names
        
    def addTypeDef(self, type, id):
        if self.parent != None:
            self.parent.addTypeDef(type, id)
        else:
            typedefs = self.entries.get('__typedefs__', {})
            if typedefs.get(id):
                print 'Typedef repeated'
            typedefs[id] = type
            self.entries['__typedefs__'] = typedefs
            
        
    def createName(self, type):
        if isinstance(type, ast.StructType):
            return type.id
        elif isinstance(type, ast.VectorType):
            return type.type + self.createName(type.subtype)
        else:
            return type.type
    
    def addType(self, type):
        if isinstance(type, ast.VectorType):
            self.addType(type.subtype)
        if self.parent != None:
            self.parent.addType(type)
        else:
            types = self.entries.get('__types__', {})
            if not types.get(type):
                name = self.createName(type.resolveType())
                types[type] = name
                types[type.resolveType()] = name
                self.entries['__types__'] = types

    def GetTypes(self):
        return self.entries.get('__types__', {})

    def CanDefineType(self, tpe, order, nested=False):
        if (self.createName(tpe) in order):
            return True
        elif isinstance(tpe, ast.VectorType):
            if nested:
                return False
            return self.CanDefineType(tpe.subtype, order, True)
        elif isinstance(tpe, ast.CustomType):
            return (self.createName(tpe) in order)
        elif isinstance(tpe, ast.StructType):
            if nested:
                return False
            for n,t in tpe.elements.iteritems():
                if not self.CanDefineType(t, order, True):
                    return False
            return True
        else:
            return True



    def OrderTypes(self):
        types = self.entries.get('__types__', {})
        order = []
        while True:
            addedNew = False
            for tpe, name in types.iteritems():
                name2 = self.createName(tpe)
                if not (name2 in order):
                    if self.CanDefineType(tpe, order):
                        order.append(name2)
                        addedNew = True
            if not addedNew:
                break
        return order
                
    def addSortCall(self, tpe, comp):
        if self.parent != None:
            return self.parent.addSortCall(tpe, comp)
        else:
            calls = self.entries.get('__sortcalls__', {})
            name = 'sort' + self.createName(tpe.resolveType()) + comp
            if not calls.get(name):
                calls[name] = [tpe, comp]
                self.entries['__sortcalls__'] = calls
                dependencies = self.entries.get('__sortcalldeps__', {})
                depscomp = dependencies.get(comp, [])
                if not name in depscomp:
                    depscomp.append(name)
                dependencies[comp] = depscomp
                self.entries['__sortcalldeps__'] = dependencies
            return name

    def get(self, name):
        """Retrieves the symbol with the given name from the symbol
        table, recursing upwards through parent symbol tables if it is
        not found in the current one."""

        if self.entries.has_key(name):
            return self.entries[name]
        else:
            if self.parent != None:
                return self.parent.get(name)
            else:
                return ast.Type('error')
                
    def resolve(self, node):
        node.resolveType()
        
    def resolveFunctionName(self, id, params):
        funcnames = self.get('__functionnames__')
        if funcnames == None:
            return id
            
        funcs = funcnames.get(id, None)
        if funcs:
            bestCandidate = None
            for long_name, tpe in funcs.iteritems():
                if len(tpe.params) == len(params.children):
                    good = True
                    for i in range(0, len(tpe.params)):
                        if tpe.params[i].resolveType().type != params.children[i].resolveType().type:
                            good = False
                    if good:
                        bestCandidate = long_name
            if bestCandidate:
                return bestCandidate
            else:
                return id[2:]
        else:
            return id
        
    def getTypeName(self, type):
        if self.parent != None:
            return self.parent.getTypeName(type)
        else:          
            types = self.entries.get('__types__', {})
            if types.has_key(type):
                return types[type]
            else:
                if isinstance(type, ast.VectorType):
                    type.size = None
                    
                    if types.has_key(type):
                        return types[type]
                    else:
                        return 'errortypename2'
                else:
                    return 'errortypename1'
                    
                    
    def getReturnType(self):
        return self.get('__return__')
        
    def getSortCallsDependencies(self):
        return self.entries.get('__sortcalldeps__', {}) 
        
    def getSortCalls(self):
        return self.entries.get('__sortcalls__', {}) 

class SymtabVisitor(visitor.Visitor):
    """Visitor that creates and attaches symbol tables to the AST."""
    def __init__ (ast):
        visitor.Visitor.__init__(ast)
       
    
    def push_symtab(self, node):
        """Pushes a new symbol table onto the visitor's symbol table
        stack and attaches this symbol table to the given node.  This
        is used whenever a new lexical scope is encountered, so the
        node is usually a CompoundStatement object."""

        self.curr_symtab = Symtab(self.curr_symtab)
        node.symtab = self.curr_symtab

    def pop_symtab(self):
        """Pops a symbol table off the visitor's symbol table stack.
        This is used whenever a new lexical scope is exited."""
        
        self.curr_symtab = self.curr_symtab.parent

    def _add_symbol(self, node):
        """Attempts to add a symbol for the given node to the current
        symbol table, catching any exceptions that occur and printing
        errors if necessary."""
        
        try:
            self.curr_symtab.add(node.id, node.type)
        except Symtab.SymbolDefinedError:
            self.error("Symbol '%s' already defined." % node.name)
        except Symtab.SymbolConflictError:
            self.error("Symbol '%s' has multiple differing declarations." % node.name)


    def vNode(self, node):
        pass

    def vNodeList (self , node):
        for child in node.children:
            self.visit(child)

    def vProgram (self, node): 
        self.root_symtab = Symtab()
        doubleType = ast.Type('double')
        doubleType.symtab = self.root_symtab
        self.root_symtab.entries['M_PI'] = doubleType
        self.curr_symtab = self.root_symtab
        self.vNodeList(node)
        node.symtab = self.root_symtab
    #def vLineComment (self, node):
    #def vBlockComment (self, node):
    #def vInclude (self, node):
    #def vUsingNamespace (self, node):
    def vFunction (self, node):
        #self._add_symbol(node)
        paramTypes = []
        for p in node.params.children:
            paramTypes.append(p.type)
        node.type = ast.FunctionType(node.returnType, paramTypes) 
        self.visit(node.type)
        real_name = self.curr_symtab.add(node.id, node.type)
        self.push_symtab(node)
        self.visit(node.params)
        self.curr_symtab.add('__return__', node.returnType)
        self.visit(node.block)
        self.pop_symtab()
        node.id = real_name
        
    def vFunctionType(self, node):
        self.visit(node.returnType)
        for p in node.params:
            self.visit(p)
            
    def vFormalParametersList (self, node):
        node.symtab = self.curr_symtab
        for c in node.children:
            self.visit(c)

    def vFormalParameter (self, node):
        self._add_symbol(node)
        self.visit(node.type)
        
    def vType (self, node):
        node.symtab = self.curr_symtab
    def vVectorType (self, node):
        node.symtab = self.curr_symtab
        self.visit(node.subtype)
        
    def vCustomType (self, node):
        node.symtab = self.curr_symtab

    def vCompoundStatement (self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        for child in node.children:
            self.visit(child)
        self.pop_symtab()
    def vCinStatement (self, node):
        node.symtab = self.curr_symtab
        for c in node.children:
            self.visit(c)
    #def vCoutStatement (self, node):
    def vCoutElement (self,node):
        node.symtab = self.curr_symtab
        self.visit(node.element)
    #def vCoutBreakLine (self,node):

    def vWhileStatement (self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        self.visit(node.cond)
        self.visit(node.loop)
        self.pop_symtab()
        
        
    def vWhileStatementCin (self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        self.visit(node.cin_cond)
        self.visit(node.loop)
        self.pop_symtab()

    def vIfStatement (self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        self.visit(node.cond)
        self.visit(node.then)
        if node.elze:
            self.visit(node.elze)
        self.pop_symtab()
        
        
    def vForStatement (self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        self.visit(node.init)
        self.visit(node.cond)
        self.visit(node.loop)
        self.visit(node.incr)
        self.pop_symtab()

    def vForStatementInit (self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        self.visit(node.init)
        self.visit(node.cond)
        self.visit(node.loop)
        self.visit(node.incr)
        self.pop_symtab()

    def vCastExpression (self, node):
        self.visit(node.type)
        self.visit(node.expression)
    def vAssignmentStatement (self, node):
        node.symtab = self.curr_symtab
        self.visit(node.expr)   #???? int a= int b= 3 ?????????
        self.visit(node.lval)   #???? int a= int b= 3 ?????????
    def vReturnStatement (self, node):
        node.symtab = self.curr_symtab
        if node.expr:
            self.visit(node.expr)

    def vVariableDeclarationStatement (self, node):
        for c in node.children:
            self.visit(c)            
            
    def vVariableDeclaration (self, node):
        node.symtab = self.curr_symtab
        self._add_symbol(node)
        self.visit(node.type)
        node.symtab.addType(node.type)
        if node.init:
            self.visit(node.init)
        if node.params:
            self.visit(node.params)
        
        
    def vIdentifier (self, node):
        node.symtab = self.curr_symtab
    def vLiteral (self, node):
        node.symtab = self.curr_symtab
    def vStringLiteral (self, node):
        node.symtab = self.curr_symtab
    def vCharLiteral (self, node):
        node.symtab = self.curr_symtab
    def vBinaryOp (self, node): # falta and or xor bit a bit
        node.symtab = self.curr_symtab
        self.visit(node.left)
        self.visit(node.right)
    def vUnaryOp (self, node):
        node.symtab = self.curr_symtab
        self.visit(node.right)
        
    def findFunction(self, symtab, id, node_params):
        
        funcnames = symtab.get('__functionnames__')
        #print funcnames
        bestCandidate = None
        bestCandidateType = ast.Type('error')
        if isinstance(funcnames, ast.Type) and funcnames.type == 'error':
            return (bestCandidate, bestCandidateType)
        funcs = funcnames.get(id, None)
        #print id
        if funcs:
            #print "here1"
            
            for long_name, tpe in funcs.iteritems():
                
                if len(tpe.params) == len(node_params):
                    good = True
                    #print tpe.params
                    for i in range(0, len(tpe.params)):
                        if not node_params[i].resolveType().canCoerceType(tpe.params[i].resolveType()):
                            good = False
                    if good:
                        bestCandidate = long_name
                        bestCandidateType = tpe
            #if bestCandidate:
                #node.id = bestCandidate
                #node.type = bestCandidateType
        
        return (bestCandidate, bestCandidateType)
        
        
    def vFunctionCall (self, node):
        node.symtab = self.curr_symtab
        self.visit(node.params)
        if node.callee:
            self.visit(node.callee)
        if node.id == 'sort' and node.params and len(node.params.children) >= 2:
            par1 = node.params.children[0]
            if isinstance(par1, ast.FunctionCall) and par1.callee and isinstance(par1.callee.resolveType(), ast.VectorType):
                
                tpeSorted = par1.callee.resolveType().subtype.resolveType()
                node.isSortCall = True
                node.sortComp = 'standardless'
                if len(node.params.children) == 3 and isinstance(node.params.children[2], ast.Identifier):
                    node.sortComp = 'f_' + node.params.children[2].id + '_' + tpeSorted.type + '_' + tpeSorted.type
                node.sortFuncName = self.curr_symtab.addSortCall(par1.callee.resolveType(), node.sortComp)
                node.sortVector = par1.callee
                node.sortType = par1.callee.resolveType()
                if len(node.params.children) > 2:
                    (a, b) =  self.findFunction(node.symtab, 'f_' + node.params.children[2].id, [node.sortType.subtype, node.sortType.subtype])
                    #(node.sortFuncOrigName, node.sortFuncType) =  self.findFunction(node.symtab, 'f_' + node.params.children[2].id, [node.sortType.subtype, node.sortType.subtype])
                    node.sortFuncOrigName = a
                    node.sortFuncType = b
                else:
                    node.sortFuncOrigName = ""
                    node.sortFuncType = ast.Type('error')
                #print node.sortFuncOrigName
                #print node.sortFuncType
                #print node.sortFuncType.type
        else:
            funcnames = node.symtab.get('__functionnames__')
            if isinstance(funcnames, ast.Type) and funcnames.type == 'error':
                return
            funcs = funcnames.get(node.id, None)
            if funcs:
                bestCandidate = None
                bestCandidateType = ast.Type('error')
                for long_name, tpe in funcs.iteritems():
                    
                    if len(tpe.params) == len(node.params.children):
                        good = True
                        #print tpe.params
                        for i in range(0, len(tpe.params)):
                            if not node.params.children[i].resolveType().canCoerceType(tpe.params[i].resolveType()):
                                good = False
                        if good:
                            bestCandidate = long_name
                            bestCandidateType = tpe
                if bestCandidate:
                    node.id = bestCandidate
                    node.type = bestCandidateType
                    
    def vActualParametersList (self, node):
        node.symtab = self.curr_symtab
        for c in node.children:
            self.visit(c)
        
    def vParenthesis (self, node):
        self.visit(node.expr)

    def vReference(self, node):
        node.symtab = self.curr_symtab
        self.visit(node.value)
        self.visit(node.idx)

    def vTypeDef(self, node):
        node.symtab = self.curr_symtab
        self.visit(node.type)
        self.curr_symtab.addTypeDef(node.type, node.id)
        self.curr_symtab.addType(node.type)
        
    def vConstructor(self, node):
        node.symtab = self.curr_symtab
        self.visit(node.type)
        self.visit(node.params)
        
    def vStructDef(self, node):
        self.push_symtab(node)
        node.symtab = self.curr_symtab
        tpe = ast.StructType(node.id, {})
        for c in node.children:
            self.visit(c)
            for c2 in c.children:
                tpe.addElement(c2.id, c2.type)
        #print 'StructDef ' + node.id
        node.symtab.addType(tpe)
        self.curr_symtab.addTypeDef(tpe, node.id)
        self.visit(tpe)
        self.pop_symtab()
        
    def vStructReference(self, node):
        node.symtab = self.curr_symtab
        self.visit(node.object)
        
    def vNullNode(self, node):
        pass