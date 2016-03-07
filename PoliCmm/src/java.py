
import formatter
import ast



class Java (formatter.Formatter):
    

    # translation
    t = {
        'int': 'int',
        'double': 'double',
        'char': 'char',
        'bool': 'boolean',
        'string': 'String',
        '+': '+',
        '-': '-',
        '++': '++',
        '--': '--',
        '*': '*',
        '/': '/',
        '%': '%',
        '==': '==',
        '!=': '!=',
        '<': '<',
        '>': '>',
        '<=': '<=',
        '>=': '>=',
        'and': '&&',
        'AND': '&&',
        'or': '||',
        'OR': '||',
        'not': '!',
        'NOT': '!'
    }


    def vNode (self, node):
        '''Base rule.'''
        self.w('?'+node.__class__.__name__+'?')


    def vProgram (self, node):
        self.p('// Translated to Java with PoliCmm')
        self.p()
        self.p('import java.util.Scanner;')
        self.p('import java.util.Comparator;')
        self.p('import java.util.Arrays;')
        self.p('import java.io.*;')
        self.p('import java.util.regex.Pattern;')
        self.p()
        self.p('public class solution {')
        self.p()
        self.i()
        
        
        self.p('public static Scanner _scanner_;')
        #self.p('public static Scanner _intscanner_;')
        #self.p('public static Scanner _doublescanner_;')
        self.p('public static int _precision_;')
        self.p('public static int _int_;')
        self.p('public static String _string_;')
        self.p('public static double _double_;')
        self.p('public static char _char_;')
        self.p('public static boolean _bool_;')
        self.p('public static String _precision_string_;')
        self.p('public static Pattern p_int, p_double, p_string, p_char;')
        classes = ['CInt', 'CChar', 'CDouble', 'CBoolean', 'CString', 'CObject']
        names = ['int', 'char', 'double', 'bool', 'string', 'object']
        inits = ['0', '\'0\'', '0', 'false', '""', 'null']
        for i in range(len(classes)):
            self.w('public static MyStack<%s>' % classes[i])
            for j in range(10):
                if j > 0:
                    self.w(',')
                self.w('_%s%d_' % (names[i], j))
            self.p(';')
             #%s _%s_0, _%s_1, _%s_2, _%s_3;', classes[i], names[i], names[i], names[i], names[i])
        #self.p('public static CInt _int0_, _int1_, _int2_, _int3_;')
        #self.p('public static CChar _char0_, _char1_, _char2_, _char3_;')
        #self.p('public static CDouble _double0_, _double1_, _double2_, _double3_;')
        #self.p('public static CBoolean _boolean0_, _boolean1_, _boolean2_, _boolean3_;')
        #self.p('public static CString _string0_, _string1_, _string2_, _string3_;')
        
        self.pi('public static boolean check_read_int() {')
        self.p('_scanner_.useDelimiter(p_int);')
        self.pi('if (_scanner_.hasNextInt()) {')
        self.p('_int_ = _scanner_.nextInt();')
        self.pu('return true;')
        self.p('}')
        self.pu('return false;')
        self.p('}')
        
        self.pi('public static int read_int() {')
        self.p('_scanner_.useDelimiter(p_int);')
        self.p('int t = _scanner_.nextInt();')
        self.pu('return t;')
        self.p('}')
        
        self.pi('public static boolean check_read_string() {')
        self.p('_scanner_.useDelimiter(p_string);')
        self.pi('if (_scanner_.hasNext()) {')
        self.p('_string_ = _scanner_.next();')
        self.pu('return true;')
        self.p('}')
        self.pu('return false;')
        self.p('}')
        
        self.pi('public static String read_string() {')
        self.p('_scanner_.useDelimiter(p_string);')
        self.p('String t = _scanner_.next();')
        self.pu('return t;')
        self.p('}')
        
        self.pi('public static boolean check_read_double() {')
        #self.p('_scanner_.useDelimiter(p_double);')
        #self.pi('if (_scanner_.hasNextDouble()) {')
        #self.p('_double_ = _scanner_.nextDouble();')
        #self.pu('return true;')
        #self.p('}')
        #self.pu('return false;')
        
        
        self.p('String t = _scanner_.findWithinHorizon(p_double, 0);')
        self.p('if (t == null || t.length() == 0) return false;')
        self.p('_double_ = Double.valueOf(t);')
        self.pu('return true;')
        
        self.p('}')
        
        self.pi('public static double read_double() {')
        self.p('_scanner_.useDelimiter(p_double);')
        self.p('String s = _scanner_.findWithinHorizon(p_double, 0);')
        self.p('double t = Double.valueOf(s);')
        #self.p('double t = _scanner_.nextDouble();')
        self.pu('return t;')
        self.p('}')
        
        self.pi('public static boolean check_read_char() {')
        #self.pi('try {')
        #self.p('int i = System.in.read();')
        #self.p('while (i >= 0 && i < 32) i = System.in.read();')
        #self.p('if (i < 0) return false;')
        #self.p('_char_ = (char) i;')
        
        #self.p('return true;')
        #self.u();
        #self.pi('} catch (IOException e) {')
        #self.pu('return false;')
        #self.pu('}')
        self.p('String t = _scanner_.findWithinHorizon(p_char, 0);')
        self.p('if (t == null || t.length() == 0) return false;')
        self.p('_char_ = t.charAt(0);')
        self.pu('return true;')

        
        
        #self.p('_scanner_.useDelimiter("[^\\\\s\\\\w]+");')
        #self.pi('if (_scanner_.hasNextByte()) {')
        #self.p('_char_ = (char)_scanner_.nextByte();')
        #self.pu('return true;')
        #self.p('}')
        #self.pu('return false;')
        self.p('}')
        
        
        self.pi('public static char read_char() {')
        
        
        #self.pi('try {')
        #self.p('int i = System.in.read();')
        #self.p('while (i >= 0 && i < 32) i = System.in.read();')
        #self.p('if (i < 0) return \'0\';')
        #self.p('char c = (char) i;')
        
        #self.p('return c;')
        #self.u();
        #self.pi('} catch (IOException e) {')
        #self.pu('return \'0\';')
        #self.pu('}')
        
        #self.p('_scanner_.useDelimiter("[^\\\\s\\\\w\\\\d\\\\\\\\]+");')
        #self.p('char t = (char)_scanner_.nextByte();')
        #self.p('char t = _scanner_.next("\\\\w").charAt(0);')
        self.p('char t = _scanner_.findWithinHorizon(p_char, 0).charAt(0);')
        self.pu('return t;')
        
        self.p('}')
        
        self.pi('public static boolean check_read_bool() {')
        self.pi('if (_scanner_.hasNextBoolean()) {')
        self.p('_bool_ = _scanner_.nextBoolean();')
        self.pu('return true;')
        self.p('}')
        self.pu('return false;')
        self.p('}')
        
        
        self.pi('public static boolean read_bool() {')
        self.p('boolean t = _scanner_.nextBoolean();')
        self.pu('return t;')
        self.p('}')
        
        self.p('public int idemint(int x, boolean b) { return x;};')
        self.p('public char idemchar(char x, boolean b) { return x;};')
        self.p('public String idemstring(String x, boolean b) { return x;};')
        self.p('public double idemdouble(double x, boolean b) { return x;};')
        self.p('public boolean idembool(boolean x, boolean b) { return x;};')
        self.p('public Object idemobject(Object x, boolean b) { return x;};')
        self.p('public String setCharAt(String s, int idx, char c) { StringBuffer sb = new StringBuffer(s); sb.setCharAt(idx, c); return sb.toString();}')
        self.p('public String constructString(int n, char c) { StringBuffer sb = new StringBuffer(n); for (int i =0; i < n; i++) sb.setCharAt(i, c); return sb.toString();}')

        self.p('public double M_PI = 3.1415926535897932384626433;')
        for c in node.children:
            if isinstance(c, ast.VariableDeclarationStatement):
                c.isTopLevel = True
            self.visit(c)
        self.p()
        self.pi('public static void main ( String [] args ) {')
        self.p('_scanner_ = new Scanner(System.in);')
        self.p('p_int = Pattern.compile("[^0-9\\\\-]+");')
        #self.p('p_double = Pattern.compile("[^0-9\\\\-\\\\.]+");')
        self.p('p_double = Pattern.compile("(\\\\-)?(\\\\d)+(\\\\.(\\\\d)*)?");')
        self.p('p_char = Pattern.compile("\\\\S");')
        self.p('p_string = Pattern.compile("\\\\s+");')
        
        #self.p('_intscanner_ = new Scanner(System.in);')
        #self.p('_doublescanner_ = new Scanner(System.in);')
        #self.p('_intscanner_.useDelimiter("[^0-9\\\\-]");')
        #self.p('_doublescanner_.useDelimiter("[^0-9\\\\.\\\\-]");')
        self.p('_precision_string_ = "%.3f";')
        self.p('_precision_ = 3;')
        
        for i in range(len(classes)):
            for j in range(10):
                #self.p('_%s%d_ = new MyStack<%s>(%s);' % (names[i], j, classes[i], inits[i]))
                self.p('_%s%d_ = new MyStack<%s>();' % (names[i], j, classes[i]))
            #self.p('public static %s _%s_0, _%s_1, _%s_2, _%s_3;', classes[i], names[i], names[i], names[i], names[i])
        
        #self.p('_int0_ = new CInt(0);')
        #self.p('_int1_ = new CInt(0);')
        #self.p('_int2_ = new CInt(0);')
        #self.p('_int3_ = new CInt(0);')
        #self.p('_int0_ = new CInt(0);')
        #self.p('_int1_ = new CInt(0);')
        #self.p('_int2_ = new CInt(0);')
        #self.p('_int3_ = new CInt(0);')
        #self.p('_int0_ = new CInt(0);')
        #self.p('_int1_ = new CInt(0);')
        #self.p('_int2_ = new CInt(0);')
        #self.p('_int3_ = new CInt(0);')
        #self.p('_int0_ = new CBoolean(0);')
        #self.p('_int1_ = new CBoolean(0);')
        #self.p('_int2_ = new CBoolean(0);')
        #self.p('_int3_ = new CBoolean(0);')
        #self.p('_int0_ = new CString(0);')
        #self.p('_int1_ = new CString(0);')
        #self.p('_int2_ = new CString(0);')
        #self.p('_int3_ = new CString(0);')
        self.p('solution s = new solution();')
        self.p('s.main();')
        self.u()
        self.p('}')
        
        self.u()
        self.p('}')


    def vLineComment (self, node):
        self.p('//' + node.text)


    def vBlockComment (self, node):
        self.p('/*' + node.text + '*/')


    def vInclude (self, node):
        pass


    def vUsingNamespace (self, node):
        pass


    def vFunction (self, node):
        uses_ref = False
        refs = []
        for c in node.params.children:
            refs.append(c.type.is_reference)
            if c.type.is_reference:
                uses_ref = True
        #print node.id
        #print refs
        if uses_ref:
            for c in node.params.children:
                c.type.is_reference = False
            if node.type.resolveType().returnType.type != 'void':
                self.visit(node.type.resolveType().returnType)
            else:
                self.w('void')
            self.w(node.id)            
            self.visit(node.params)
            self.visit(node.block)
            self.p()
            
            for i in range(len(node.params.children)):
                node.params.children[i].type.is_reference = refs[i]
            
        self.p()
        self.w('public')
        if node.id=='main':
            self.w('int')
            self.w(node.id)            
            self.w('()')
        else:
            if node.type.resolveType().returnType.type != 'void':
                self.visit(node.type.resolveType().returnType)
            else:
                self.w('void')
            self.w(node.id)            
            self.visit(node.params)
        if node.id=='main':
            self.pi('{')
            self.visit(node.block)
            self.pu('return 0;')
            self.p('}')
        else:
            self.visit(node.block)
        #self.visit(node.block)

        self.p()
            


    def vFormalParametersList (self, node):
        self.w('(')
        first = True
        for c in node.children:
            if first: first = False
            else: self.w(',')
            self.visit(c)
        self.w(')')


    def vFormalParameter (self, node):
        if node.type.is_reference:
            if node.type.isInt():
                self.w('CInt')
            elif node.type.isChar():
                self.w('CChar')
            elif node.type.isString():
                self.w('CString')
            elif node.type.isDouble():
                self.w('CDouble')
            elif node.type.isBool():
                self.w('CBoolean')
            else:
                self.w('CObject')
            self.w(node.id)
        else:
            self.visit(node.type)
            self.w(node.id)

    def vCustomType (self, node):
        tpe = node.resolveType()
        tpe = tpe.resolveType()
        tpe.symtab = node.symtab
        self.visit(tpe)

    def vType (self, node):
        self.w(self.t.get(node.type, 'error'))
        
    def vStructType(self, node):
        self.w(node.id)
        
    def vVectorType(self, node):
        self.visit(node.subtype)
        self.w('[]')

    def vCompoundStatement (self, node):
        self.p('{')
        self.i()
        for c in node.children:
            self.visit(c)
            if not (isinstance(c, ast.IfStatement) or isinstance(c, ast.WhileStatement) or isinstance(c, ast.ForStatement) or isinstance(c, ast.ForStatementInit) or isinstance(c, ast.Comment) or isinstance(c, ast.CompoundStatement)):
                self.p(';')
            else:
                self.p()
        self.u()
        self.w('}')


    def vCinStatement (self, node):
        first = True
        
        if node.is_expression:
            self.w('(')
            for c in node.children:
                if first: 
                    first = False
                else: 
                    self.p('&&')
                tpe = c.resolveType()
                #print tpe.type
                self.w('(check_read_%s() && ((' % tpe.type)
                self.w(c.id)
                if tpe.isString() :
                    self.w(' = _%s_).equals("") || true))' % tpe.type)
                else:
                    self.w(' = _%s_) > 0 || true))' % tpe.type)
            self.w(')')
        else:
            for c in node.children:
                if first: first = False
                else: self.p(';')
                tpe = c.resolveType()
                self.visit(c)
                self.w('=')
                if tpe.isInt():
                    self.w('read_int()')
                if tpe.isFloat():
                    self.w('read_double()')
                if tpe.isDouble():
                    self.w('read_double()')
                if tpe.isString():
                    self.w('read_string()')
                if tpe.isChar():
                    self.w('read_char()')
                if tpe.isBool():
                    self.w('read_int() != 0')

            
    def vCoutStatement (self, node):
        first = True
        for c in node.children:
            if first: first = False
            else: self.p(';')
            self.visit(c)

    def vCoutElement (self,node):
        if node.element.resolveType().isFloatingPoint():
            self.w('System.out.printf (_precision_string_, ')
            self.visit(node.element)
            self.w(')')
        else:
                
            self.w('System.out.print (')
            self.visit(node.element)
            if node.element.resolveType().isBool():
                self.w(' ? 1 : 0')
            self.w(')')
            
    def vCoutBreakLine (self,node):
        self.w('System.out.println()')
        
        
    def vCoutModifier (self, node):
        if node.func == 'precision':
            self.pi('{')
            self.w('_precision_ = ')
            self.visit(node.param_list.children[0])
            self.p(';')
            self.pu('_precision_string_ = "%." + _precision_ + "f";')
            self.p('}')
            
    def doCondition(self, node, cond):
        if not node.cond.resolveType().isBool():
            newcond = ast.BinaryOp(node.cond, '!=', ast.IntLiteral('0'))
            newcond.symtab = node.symtab
            self.visit(newcond)
        else:
            self.visit(node.cond)
        
            
    def vWhileStatement (self, node):
        self.w('while')
        self.w('(')
        self.doCondition(node, node.cond)
        self.w(')')
        
        if not isinstance(node.loop, ast.CompoundStatement):
            t = ast.CompoundStatement()
            t.add(node.loop)
            self.visit(t)
        else:
            self.visit(node.loop)

            
    def vIfStatement (self, node):
        self.w('if')
        self.w('(')
        self.doCondition(node, node.cond)
        self.w(')')
        if not isinstance(node.then, ast.CompoundStatement):
            t = ast.CompoundStatement()
            t.add(node.then)
            self.visit(t)
        else:
            self.visit(node.then)
        
        if node.elze:
            self.w('else')
                
            if not isinstance(node.elze, ast.CompoundStatement):
                t = ast.CompoundStatement()
                t.add(node.elze)
                self.visit(t)
            else:
                self.visit(node.elze)
            

    def vAssignmentStatement (self, node):
        node.lval.is_lval = True
        if isinstance(node.expr, ast.Constructor):
            node.expr.recv = node.lval
        if isinstance(node.lval, ast.Reference) and node.lval.value.resolveType().isString():
            self.visit(node.lval.value)
            self.w('=')
            self.w('setCharAt(')
            self.visit(node.lval.value)
            self.w(',')
            self.visit(node.lval.idx)
            self.w(',')
            if node.operator == '=':
                self.visit(node.expr)
            else:
                self.w('(char)((int)')
                self.visit(node.lval.value)
                self.w('.charAt(')
                self.visit(node.lval.idx)
                self.w(')')
                if node.operator == '+=': self.w('+')
                if node.operator == '-=': self.w('-')
                self.w('(int)')
                self.visit(node.expr)
                self.w(')')
            self.w(')')
        else:
            self.visit(node.lval)
            self.w(node.operator)
            self.visit(node.expr)


    def vReturnStatement (self, node):
        self.w('return')
        if not node.expr:
            return
        tpe = node.symtab.getReturnType().resolveType()
        if tpe.type == 'void':
            return
        self.visit(node.expr)


    def vVariableDeclarationStatement (self, node):
        first = True
        for c in node.children:
            if not first:
                self.p(';')
            first = False
            if node.isTopLevel:
                self.w('public static')
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
        self.pi('{')
        name_iter = 'aux_i%d' % idx
        indices.append(name_iter)
        self.w('for (int %s = 0; %s < ' % (name_iter, name_iter))
        self.visit(node.params.children[0])
        self.p('; %s++)' % name_iter)
        if (len(node.params.children) > 1) and isinstance(node.params.children[1], ast.Constructor):
            self.pi('{')
            self.initializeVector(node.params.children[1], tpe.subtype, indices, idx + 1, id)
            self.pu()
            self.w('}')
        else:
            self.i()
            self.w(id)
            self.w('[')
            first = True
            for idx in indices:
                if not first:
                    self.w('][')
                first = False
                self.w(idx)
            self.w(']')
            self.w(' = ')
            if tpe.subtype.resolveType().isStruct():
                self.w('new')
                self.w(tpe.subtype.resolveType().type)
                self.w('()')
            else:
                self.visit(node.params.children[1])
            self.pu(';')
        self.pu()
        self.w('}')
        
    def initializeVector2(self, node, tpe, indices, idx, lvalnode):
        self.pi('{')
        name_iter = 'aux_i%d' % idx
        indices.append(name_iter)
        self.w('for (int %s = 0; %s < ' % (name_iter, name_iter))
        self.visit(node.params.children[0])
        self.p('; %s++)' % name_iter)
        if (len(node.params.children) > 1) and isinstance(node.params.children[1], ast.Constructor):
            self.pi('{')
            self.initializeVector(node.params.children[1], tpe.subtype, indices, idx + 1, id)
            self.pu()
            self.w('}')
        else:
            self.i()
            #idnode = ast.Identifier(id)
            #idnode.symtab = node.symtab
            prevlval = lvalnode.is_lval
            lvalnode.is_lval = False
            #print lvalnode
            self.visit(lvalnode)
            lvalnode.is_lval = prevlval
            self.w('[')
            first = True
            for idx in indices:
                if not first:
                    self.w('][')
                first = False
                self.w(idx)
            self.w(']')
            self.w(' = ')
            if tpe.subtype.resolveType().isStruct():
                self.w('new')
                self.w(tpe.subtype.resolveType().type)
                self.w('()')
            else:
                self.visit(node.params.children[1])
            self.pu(';')
        self.pu()
        self.w('}')
        
    def needsInitialization(self, node):
        if (len(node.params.children) > 1) and isinstance(node.params.children[1], ast.Constructor):
            return self.needsInitialization(node.params.children[1])
        elif len(node.params.children) > 1:
            return True
        else:
            return False
            
    def finalType(self, tpe, params):
        if tpe.isVector() and (hasattr(params, 'children') and len(params.children) > 1):
            return self.finalType(tpe.subtype, params.children[1])
        if tpe.isVector(): return tpe.subtype
        else: return tpe

    def vVariableDeclaration (self, node):
        self.visit(node.type)
        self.w(node.id)
        
        tpe = node.type.resolveType()
        if tpe.isVector() and node.params:
            
            
            if tpe.isVector() or tpe.isString():
                #print "initVectorType" + tpe.type
                tpe = self.initializeVectorType(tpe, node)
                tpe.symtab = node.symtab

            
            if tpe.isVector() and node.params:
                self.w(' = ')
                self.w('new')
                self.visit(self.finalType(tpe, node.params))
                self.w('[')
                t = tpe
                first = True
                while t.isVector():
                    if t.size != None:
                        if not first:
                            self.w('][')
                        first = False
                        self.visit(t.size)
                    else:
                        print 'Vectors need to be initialized fully at creation.'
                        break
                    t = t.subtype
                self.w(']')
                if self.needsInitialization(node) or self.finalType(tpe, node.params).isStruct():
                    self.p(';')
                    self.initializeVector(node, node.type.resolveType(), [], 1, node.id)
            

            #self.w('=')
            #self.w('new')
            #self.visit(tpe.subtype)
            #self.w('[')
            #self.visit(node.params.children[0])
            #self.w(']')
            
        elif node.init:
            self.w('=')
            self.visit(node.init)
        elif tpe.isString():
            self.w('=')
            if not node.params or len(node.params.children) == 0:
                self.w('new String ("")')
            elif len(node.params.children) == 1:
                self.w('constructString(')
                self.visit(node.params.children[0])
                self.w(', \' \')')
            elif len(node.params.children) == 2:
                self.w('constructString(')
                self.visit(node.params.children[0])
                self.w(',')
                self.visit(node.params.children[1])
                self.w(')')
            elif len(node.params.children) == 3:
                self.visit(node.params.children[0])
                self.w('.substring(')
                self.visit(node.params.children[1])
                self.w(',')
                self.visit(node.params.children[2])
                self.w(')')
            #self.w('=')
            #self.w('new String("")')
        elif tpe.isInt() or node.type.isDouble():
            self.w('=')
            self.w('0')
        elif tpe.isChar():
            self.w('=')
            self.w('\'0\'')
        elif tpe.isBool():
            self.w('=')
            self.w('false')
        elif tpe.isStruct():
            self.w('=')
            self.w('new')
            self.w(tpe.id)
            self.w('()')
        else:
            self.w('=')
            self.w('null')
            
    def vIdentifier (self, node):
        if (not node.resolveType().isBasic()) and node.resolveType().is_reference and (not node.is_lval):
            self.w('(')
            self.w('(')
            self.visit(node.resolveType())
            self.w(')')
            self.w(node.id)
            self.w('.value')
            self.w(')')
        else:
            self.w(node.id)
            if node.resolveType().is_reference:
                self.w('.value')


    def vLiteral (self, node):
        if node.resolveType().isString():
            self.w("\"" + node.lit + "\"")
        elif node.resolveType().isChar():
            self.w("'" + node.lit + "'")
        else:
            self.w(str(node.lit))


    def vBinaryOp (self, node):
        left_tpe = node.left.resolveType()
        right_tpe = node.right.resolveType()
        if left_tpe.isString() and right_tpe.isString() and (node.oper == '==' or node.oper == '!='):
            if node.oper == '!=':
                self.w('!')
            
            self.visit(node.left)
            self.w('.equals(')
            self.visit(node.right)
            self.w(')')
            
        elif left_tpe.isString() and right_tpe.isString() and (node.oper == '<=' or node.oper == '<' or node.oper == '>=' or node.oper == '>'):
            self.visit(node.left)
            self.w('.compareTo(')
            self.visit(node.right)
            self.w(')')
            self.w(node.oper)
            self.w('0')
        else:
            if (left_tpe.isChar() or right_tpe.isChar()) and (left_tpe.isInt() or right_tpe.isInt()) and not (node.oper =='<=' or node.oper == '<' or node.oper == '>=' or node.oper == '>' or node.oper == '==' or node.oper == '!='):
                self.w('(char)(')
                if left_tpe.isChar():
                    self.w('(int)')
                self.visit(node.left)
                self.w(self.t[node.oper])
                if right_tpe.isChar():
                    self.w('(int)')
                self.visit(node.right)
                self.w(')')
                return
                    
            self.visit(node.left)
            self.w(self.t[node.oper])
            self.visit(node.right)

    def vUnaryOp (self, node):
        if node.pre:
            self.w(self.t[node.oper])
            self.visit(node.right)
        else:
            self.visit(node.right)
            self.w(self.t[node.oper])
            

    def vFunctionCall (self, node):
        #print node.id
        if node.isSortCall:
            self.w('Arrays.sort(')
            self.visit(node.sortVector)
            basetype = node.sortVector.resolveType().subtype.resolveType()
            if node.sortComp == 'standardless':
                self.p(')')
            else:
                self.pi(', new Comparator () {')
                self.pi('public int compare(Object a, Object b) {')
                if len(node.params.children) > 2:
                    compfun = node.sortComp
                    self.w('if (%s((' % compfun)
                    self.visit(basetype)
                    self.w(')a, (')
                    self.visit(basetype)
                    self.p(')b)) return -1;')
                    
                    self.w('if (%s((' % compfun)
                    self.visit(basetype)
                    self.w(')b, (')
                    self.visit(basetype)
                    self.p(')a)) return 1;')
                else:
                    self.w('if ((')
                    self.visit(basetype)
                    self.w(')a < (')
                    self.visit(basetype)
                    self.p(')b) return -1;')
                    
                    
                    self.w('if ((')
                    self.visit(basetype)
                    self.w(')b < (')
                    self.visit(basetype)
                    self.p(')a) return 1;')
                    
                self.pu('return 0;')
                self.pu('}')
                self.w('})')
                
            return
        if node.callee and node.callee.resolveType().isVector() and node.id == 'size':
            self.visit(node.callee)
            self.w('.length')
            return
        if node.callee and node.callee.resolveType().isString() and node.id == 'size':
            self.visit(node.callee)
            self.w('.length()')
            return
            
        if not hasattr(node, 'type'):
            self.w('Math.%s' % node.id)
            self.w('(')
            self.visit(node.params)
            self.w(')')
            return
            
        
        has_ref = False
        ftype = node.type
        for i in range(len(node.params.children)):
            if ftype.params[i].is_reference:
                has_ref = True
        rettype = node.type.resolveType().returnType    
        
        if has_ref and rettype.type != 'void':
            
            if not rettype.isBasic():
                self.w('(')
                self.visit(rettype)
                self.w(')')
            if rettype.isBasic():
                self.w('idem%s(' % rettype.type)
            else:
                self.w('idemobject( (Object)')
            
        self.w(node.id)
        
        self.w('(')
        first = True
        for i in range(len(node.params.children)):
            if first: first = False
            else: self.w(',')
            
            if node.type.params[i].is_reference:
                if node.type.params[i].resolveType().isBasic():
                    dic = {'int': 'CInt', 'char': 'CChar', 'double': 'CDouble', 'string' : 'CString', 'bool': 'CBoolean'}
                    self.w('_%s%d_.push(new %s(' % (node.type.params[i].resolveType().type, i, dic[node.type.params[i].resolveType().type]))
                    self.visit(node.params.children[i])
                    self.w(') )')
                else:
                    self.w('_object%d_.push(new CObject( (Object) ' % i)
                    self.visit(node.params.children[i])
                    self.w(') )')
            else:
                self.visit(node.params.children[i])
            
        self.w(')')
        
        if has_ref:
            if rettype.type != 'void':
                self.w(',')
            else:
                self.p(';')
            first = True
            #print "here"
            for i in range(len(node.type.params)):
                if node.type.params[i].is_reference:
                    if not first:
                            
                        if rettype.type != 'void':
                            self.w('&&')
                        else:
                            self.w(';')
                        
                    first = False
                    
                        
                    if node.type.params[i].resolveType().isBasic():
                        if rettype.type != 'void':
                            self.w('(')
                        if node.type.params[i].resolveType().isChar() and isinstance(node.params.children[i], ast.Reference) and node.params.children[i].value.resolveType().isString():
                            self.visit(node.params.children[i].value)
                            self.w('=')
                            self.w('setCharAt(')
                            
                            self.visit(node.params.children[i].value)
                            self.w(',')
                            self.visit(node.params.children[i].idx)
                            self.w(',')
                            self.w('_%s%d_.pop().value)' % (node.type.params[i].resolveType().type, i))
                            
                        else:
                            self.visit(node.params.children[i])
                            self.w('=')
                            self.w('_%s%d_.pop().value' % (node.type.params[i].resolveType().type, i))
                        
                        if rettype.type != 'void':
                            self.w(')')
                            if node.type.params[i].resolveType().isString() :
                                self.w('.equals("") ')
                            else:
                                self.w('> 0')
                    else:
                        
                        if rettype.type != 'void':
                            self.w('(')
                        node.params.children[i].is_lval = True
                        self.visit(node.params.children[i])
                        node.params.children[i].is_lval = False
                        
                        self.w('=')
                        self.w('(')
                        self.visit(node.type.params[i].resolveType())
                        self.w(')')
                        self.w('_object%d_.pop().value' % i)
                        if rettype.type != 'void':
                            self.w(')')
                            self.w('!= null')
                        
             
            if rettype.type != 'void':           
                self.w(')')
                


    def vActualParametersList (self, node):
        first = True
        for c in node.children:
            if first: first = False
            else: self.w(',')
            self.visit(c)
            
            
    def vForStatement (self, node): 
        self.w('for')
        self.w('(')
        #print node.init
        self.visit(node.init)
        self.w(';')
        self.doCondition(node, node.cond)
        self.w(';')
        self.visit(node.incr)
        self.w(')')
        if not isinstance(node.loop, ast.CompoundStatement):
            t = ast.CompoundStatement()
            t.add(node.loop)
            self.visit(t)
        else:
            self.visit(node.loop)
        
    def vForStatementInit (self, node):
        self.w('for')
        self.w('(')
        self.visit(node.init)
        self.w(';')
        self.doCondition(node, node.cond)
        self.w(';')
        self.visit(node.incr)
        self.w(')')
        self.p();
        if not isinstance(node.loop, ast.CompoundStatement):
            t = ast.CompoundStatement()
            t.add(node.loop)
            self.visit(t)
        else:
            self.visit(node.loop)
        

    def vParenthesis (self, node):
        self.w('(')
        self.visit(node.expr)
        self.w(')')

    def vConstructor (self, node):
        #if len(node.params.children) > 1 or len(node.params.children) == 0:
            #print "Constructors are only allowed for simple params if not in variable declarations"
        #else:
            #tpe = node.params.children[0].resolveType()
            #if tpe.isInt() and node.type.isFloatingPoint():
                #self.w('castint2%s(' % node.type.type);
                #self.visit(node.params.children[0])
                #self.w(')')
            #elif node.type.isInt() and tpe.isFloatingPoint():
                #self.w('cast%s2int(' % tpe.type);
                #self.visit(node.params.children[0])
                #self.w(')')
            #else:
        #print node.resolveType()
        #print node.resolveType().type
        if node.resolveType().isBasic() and not node.resolveType().isString():
            self.w('(')
            self.visit(node.type)
            self.w(')')
            self.w('(')
            self.visit(node.params.children[0])
            self.w(')')
        elif node.resolveType().isString():
            if len(node.params.children) == 0:
                self.w('new String ("")')
            elif len(node.params.children) == 1:
                self.w('constructString(')
                self.visit(node.params.children[0])
                self.w(', \' \')')
            elif len(node.params.children) == 2:
                self.w('constructString(')
                self.visit(node.params.children[0])
                self.w(',')
                self.visit(node.params.children[1])
                self.w(')')
            elif len(node.params.children) == 3:
                self.visit(node.params.children[0])
                self.w('.substring(')
                self.visit(node.params.children[1])
                self.w(',')
                self.visit(node.params.children[2])
                self.w(')')
                
        else:
            self.w('new')
            if node.resolveType().isVector():
                self.visit(node.resolveType().subtype)
                self.w('[')
                self.visit(node.params.children[0])
                self.w(']')
            else:
                self.visit(node.resolveType())
                self.w('(')
                self.visit(node.params)
                self.w(')')
            tpe = node.resolveType()

            if self.needsInitialization(node) or self.finalType(tpe, node.params).isStruct():
                id = 'error'
                if hasattr(node, 'recv') and isinstance(node.recv, ast.Identifier):
                    id = node.recv.id
                self.p(';')
                self.initializeVector2(node, node.type.resolveType(), [], 1, node.recv)
        
    def vReference (self, node):
        node.value.is_lval = False
        self.visit(node.value)
        
        if node.value.resolveType().isString():
            self.w('.charAt(')
            self.visit(node.idx)
            self.w(')')
        else:
            self.w('[')
            self.visit(node.idx)
            self.w(']')

    def vStructDef (self, node):
        self.w('public class')
        self.w(node.id)
        self.pi('{')
        self.w(node.id)
        self.pi('() {')
        for c in node.children:
            self.visit(c)
            self.p(';')
        self.u()
        self.p('}')
        for c in node.children:
            self.visit(c)
            self.p(';')
        self.u()
        self.p('};')
        
    def vStructReference (self, node):
        self.visit(node.object)
        self.w('.')
        self.w(node.id)
        
    def vTypeDef (self, node):
        pass
    
    
    def vCastExpression (self, node):
        self.w('(')
        self.visit(node.type)
        self.w(')')
        self.visit(node.expression)
        #tpe = node.expression.resolveType()
        #if tpe.isInt() and node.type.isFloatingPoint():
            #self.w('castint2%s(' % node.type.type);
            #self.visit(node.expression)
            #self.w(')')
        #elif node.type.resolveType().isInt() and tpe.isFloatingPoint():
            #self.w('cast%s2int(' % tpe.type);
            #self.visit(node.expression)
            #self.w(')')
        #elif node.type.resolveType().isString():
            #self.visit(node.expression)
        #elif node.type.resolveType().isBool() and tpe.isInt():
            #op = ast.BinaryOp(node.expression, '!=', ast.IntLiteral('0'))
            #op.symtab = node.symtab
            #op.right.symtab = node.symtab
            #self.visit(op)
        #else:
            #self.visit(node.type.resolveType())
            #self.w('(')
            #self.visit(node.expression)
            #self.w(')')
            
    def vNullNode(self, node):
        pass