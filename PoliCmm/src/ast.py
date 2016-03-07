
class Node:

    def __init__ (self):
        pass

    def accept(self, visitor):
        '''Accept method for visitor classes.'''
        return self._accept(self.__class__, visitor)

    def _accept(self, klass, visitor):
        '''Accept implementation.  This is actually a recursive
        function that dynamically figures out which visitor method to
        call.  This is done by appending the class' id to 'v', so if
        the node class is called MyNode, then this method tries
        calling visitor.vMyNode().  If that node doesn't exist, then
        it recursively attempts to call the visitor method
        corresponding to the class' superclass (e.g.,
        visitor.vNode()).'''

        visitor_method = getattr(visitor, "v%s" % klass.__name__, None)
        if visitor_method == None:
            bases = klass.__bases__
            last = None
            for i in bases:
                last = self._accept(i, visitor)
            return last
        else:
            return visitor_method(self)
            
    def isNodeStatement(self):
        return self.__dict__.get('isStatement', False)



class NodeList(Node):

    def __init__(self, node=None):
        self.children = []
        if node != None:
            self.children.append(node)

    def add(self, node):
        self.children.append(node)



class NullNode(Node):

    def __init__ (self):
        self.type = None





class Program (NodeList):
    pass


class Include (Node):

    def __init__(self, module):
        self.module = module


class UsingNamespace (Node):

    def __init__(self, id):
        self.module = id


class CompoundStatement (NodeList):
    pass


class CoutModifier (Node):
    def __init__(self, func, param_list):
        self.func = func
        self.param_list = param_list
    pass

class CoutStatement (NodeList):
    pass

class CoutElement (Node):
    def __init__(self,element):
        self.element=element

class CoutBreakLine (Node):
    pass
    
class CinStatement (NodeList):
    def resolveType(self):
        return Type('bool')

class CinExpression (NodeList):
    def resolveType(self):
        return Type('bool')


class IfStatement (Node):

    def __init__(self, cond, then, elze=None):
        self.cond = cond
        self.then = then
        self.elze = elze


class WhileStatement (Node):

    def __init__(self, cond, loop):
        self.cond = cond
        self.loop = loop

class WhileStatementCin (Node):

    def __init__(self, cin_cond, loop):
        self.cin_cond = cin_cond
        self.loop = loop

class ForStatement (Node):

    def __init__(self, init, cond, incr, loop):
        self.init = init
        self.cond = cond
        self.incr = incr
        self.loop = loop
        
class ForStatementInit (Node):

    def __init__(self, init, cond, incr, loop):
        self.init = init
        self.cond = cond
        self.incr = incr
        self.loop = loop


class AssignmentStatement (Node):

    def __init__(self, lval,operator, expr):
        self.lval = lval
        self.expr = expr
        self.operator=operator	
        
class CastExpression (Node):
    def __init__(self, type, expression):
        self.type=type
        self.expression=expression

    def resolveType(self):
        return self.type.resolveType()


class ReturnStatement (Node):

    def __init__(self, expr):
        self.expr = expr
        self.parent = None

    def resolveType(self):
        if self.expr:
            return self.expr.resolveType()
        else:
            return 'none'

class Type (Node):

    def __init__(self, type):
        self.type = type
        self.constant = False
        self.size = None
        self.is_reference = False
        
    def resolveType(self):
        return self
        
    def isFloat(self):
        return self.type == 'float'
        
    def isDouble(self):
        return self.type == 'double'
        
    def isFloatingPoint(self):
        return self.isFloat() or self.isDouble()
        
    def isBool(self):
        return self.type == 'bool'
        
    def isChar(self):
        return self.type == 'char'
        
    def isInt(self):
        return self.type == 'int'
        
    def isVector(self):
        return self.type == 'vector'
        
    def isStruct(self):
        return False
        
    def isString(self):
        return self.type == 'string'
        
    def isBasic(self):
        return self.isDouble() or self.isBool() or self.isChar() or self.isInt() or self.isString() 
        
    def canCoerceType(self, tpe):
        if self.type == tpe.type:
            return True
        if self.type == 'double':
            return tpe.type == 'double' or tpe.type == 'int' or tpe.type =='char'
        if self.type == 'int':
            return tpe.type == 'double' or tpe.type == 'int' or tpe.type =='char'
        if self.type == 'char':
            return tpe.type == 'double' or tpe.type == 'int' or tpe.type =='char'
        else:
            return False


class CustomType (Type):

    def __init__(self, type):
        self.type = type
        self.constant = False
        self.is_reference = False
        
    def resolveType(self):
        typedefs = self.symtab.get('__typedefs__')
        if typedefs:
            tpe = typedefs.get(self.type, Type('error'))
            tpe.symtab = self.symtab
            tpe = tpe.resolveType()
            tpe.is_reference = self.is_reference
            return tpe
        else:
            return Type('error')
            
    def canCoerceType(self, tpe):
        return self.resolveType().canCoerceType(tpe)

class VectorType (Type):

    def __init__(self, type, subtype):
        self.type = type
        self.subtype = subtype
        self.size = None
        self.constant = False
        self.hasTypeName = True
        self.is_reference = False
        
    def resolveType(self):
        tpe =  VectorType(self.type, self.subtype.resolveType())
        tpe.is_reference = self.is_reference
        return tpe
        #self.subtype = self.subtype.resolveType()
        #return self
        
    def canCoerceType(self, tpe):
        if isinstance(tpe.resolveType(), VectorType):
            return self.subtype.canCoerceType(tpe.subtype)
        else:
            return False
            
class StructType (Type):

    def __init__(self, id, elements):
        self.id = id
        self.type = id
        self.elements = elements
        self.constant = False
        self.is_reference = False
    def addElement(self, id, type):
        self.elements[id] = type
        
    def resolveType(self):
        elems = {}
        for id, tpe in self.elements.iteritems():
            elems[id] = tpe.resolveType()
        return StructType(self.id, elems)
    def canCoerceType(self, tpe):
        if isinstance(tpe.resolveType(), StructType) and self.id == tpe.id:
            return True
        else:
            return False
    
    def isStruct(self):
        return True
        

        
class FunctionType(Type):

    def __init__(self, returnType, params):
        self.returnType = returnType
        self.params = params
        self.constant = False
        self.type = 'function'
        
    def resolveType(self):
        newParams = []
        for p in self.params:
            newParams.append(p.resolveType())
        return FunctionType(self.returnType.resolveType(), newParams)
        
        
    def canCoerceType(self, tpe):
        if isinstance(tpe, FunctionType):
            if len(self.params.children) == len(tpe.params.children):
                for i in range(0, len(self.params.children)):
                    if not self.params.children[i].resolveType().canCoerceType(tpe.params.children[i].resolveType()):
                        return False
                return self.returnType.canCoerceType(tpe.returnType)
            else:
                return self.returnType.canCoerceType(tpe.returnType)
        else:
            return False

class FormalParametersList (NodeList):
    pass


class FormalParameter (Node):

    def __init__(self, id, type):
        self.id = Identifier.resolveIdentifier(id)
        self.type = type


class ActualParametersList (NodeList):
    pass



class Function (Node):

    def __init__(self, id, returnType, params, block):
        if id != 'main' and id != 'size':
            id = 'f_' + id
        self.id = Identifier.resolveIdentifier(id)
        self.returnType = returnType
        self.params = params
        self.block = block


class Comment (Node):

    def __init__(self, text):
        self.text = text


class LineComment (Comment):
    pass

class BlockComment (Comment):
    pass

class StructDef (NodeList):
    def __init__(self,node):
        NodeList.__init__(self,node)


class VariableDeclarationStatement (NodeList):
    
    def __init__(self,node,init=None):
        self.init = init
        self.isTopLevel = False
        NodeList.__init__(self,node)


class VariableDeclaration (Node):

    def __init__(self, id, init=None):
        self.id = Identifier.resolveIdentifier(id)
        self.type = None
        self.init = init
        self.isTopLevel = False
        self.params = None

class ConstantType (Type):
    def __init__(self, type):
        self.type = type
    def resolveType(self):
        return self
        
        
class Expression (Node):
    pass

class Parenthesis(Expression):
    def __init__(self, expr):
        self.expr = expr
    def resolveType(self):
        return self.expr.resolveType()


class Literal (Expression):
    def __init__(self, lit):
        self.lit = lit
        
class IntLiteral (Literal):
    def resolveType(self):
        return Type('int')
        
class BoolLiteral (Literal):
    def resolveType(self):
        return Type('bool')
        
class FloatLiteral (Literal):
    def resolveType(self):
        return Type('float')

class StringLiteral (Literal):
    def resolveType(self):
        return Type('string')

class CharLiteral (Literal):
    def resolveType(self):
        return Type('char')

class UnaryOp (Expression):

    def __init__(self, oper, right):
        self.oper = oper
        self.right = right
        
    def resolveType(self):
        return self.right.resolveType()


class BinaryOp (Expression):

    def __init__(self, left, oper, right):
        self.left = left
        self.oper = oper
        self.right = right
        
    def resolveType(self):       
        left_type  = self.left.resolveType().type
        right_type = self.right.resolveType().type

        #print left_type
        #print right_type
        if self.oper == '>' or self.oper == '>=' or self.oper == '<' or self.oper == '<=' or self.oper == '==' or self.oper == '!=':
            return Type('bool')
        if left_type == 'char' and right_type == 'char' and (self.oper == '+' or self.oper == '-'):
            return Type('int')
        elif left_type == right_type:
            return self.left.resolveType()
        elif (left_type == 'int' and right_type == 'double') or (left_type == 'double' and right_type == 'int'):
            return Type('double')
        elif (left_type == 'int' and right_type == 'float') or (left_type == 'float' and right_type == 'int'):
            return Type('float')
        elif (left_type == 'double' and right_type == 'float') or (left_type == 'float' and right_type == 'double'):
            return Type('double')
        elif (left_type == 'int' and right_type == 'char') or (left_type == 'char' and right_type == 'int'):
            return Type('int')
        else:
            return Type('error')


class FunctionCall (Expression):
    reservedFunctionNames = ['max', 'sin', 'cos', 'min', 'sqrt', 'abs', 'preIncrement', 'postIncrement', 'ppreIncrement', 'ppostIncrement', 'preDecrement', 'postDecrement', 'ppreDecrement', 'ppostDecrement']
    def __init__(self, id, params, callee = None):
        if id != 'main' and id != 'size' and id != 'begin' and id != 'sort' and id != 'end' and not (id in FunctionCall.reservedFunctionNames):
            id = 'f_' + id
        self.id = id
        self.params = params
        self.callee = callee
        self.isSortCall = False
    def resolveType(self):
        #funcnames = self.symtab.get('__functionnames__')
        #names = funcnames
        if self.id == 'size':
            intType = Type('int')
            intType.symtab = self.symtab
            return intType
        if self.id == 'sqrt' or self.id == 'cos' or self.id == 'sin':
            doubleType = Type('double')
            doubleType.symtab = self.symtab
            return doubleType
        tpe = self.symtab.get(self.id).resolveType()
        #tpe.is_reference = self.symtab.get(self.id).is_reference
        if isinstance(tpe, FunctionType):
            return tpe.returnType
        else:
            return tpe
            
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Identifier (Expression):
    reservedKeywords = ['of', 'div', 'mod', 'type', 'array', 'in', 'final']
    def resolveIdentifier(id):
        if id.lower() in Identifier.reservedKeywords:
            id = id + id
        return id
    resolveIdentifier = Callable(resolveIdentifier)
    def __init__(self, id):
        self.id = Identifier.resolveIdentifier(id)
        self.is_lval = False
    def resolveType(self):
        tpe = self.symtab.get(self.id).resolveType()
        tpe.is_reference = self.symtab.get(self.id).is_reference
        return tpe
        
        
class Reference (Expression):

    def __init__(self, value, idx):
        self.value = value
        self.idx = idx
        self.isNestedReference = False
    def resolveType(self):
        tpe = self.value.resolveType()
        if tpe.type == 'vector':
            return tpe.subtype.resolveType()
        elif tpe.type == 'string':
            return Type('char')
        else:
            return Type('error')

class StructReference (Expression):
    def __init__(self, object, id):
        self.object = object
        self.id = Identifier.resolveIdentifier(id)
    def resolveType(self):
        tpe = self.object.resolveType()
        if isinstance(tpe, StructType):
            return tpe.elements.get(self.id, Type('error')).resolveType()
        else:
            return Type('error')
            
class Error():
    
    pass

class TypeDef(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id
        
class Constructor(Node):
    def __init__(self, type, params):
        self.type = type
        self.params = params
    def resolveType(self):
        return self.type.resolveType()