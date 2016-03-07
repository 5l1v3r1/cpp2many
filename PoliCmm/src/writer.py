
import formatter
import ast
import symtab


class Writer (formatter.Formatter):
    
    '''Simple visitor that outputs a textual representation of
    the abstract syntax tree, for debugging purposes, to an
    output file. It only distinguishes Node and NodeList.'''
    


    def vNode (self, node):
        self.p(node.__class__.__name__)

        for key in node.__dict__.keys():
            val = node.__dict__[key]
            if isinstance(val, str) or isinstance(val, int):
                self.p('    -%s: %s' % (key, str(val)))
            elif isinstance(val, ast.Node):
                self.p('    -%s: ' % (key))
                self.i()
                self.i()
                self.visit(val)
                self.u()
                self.u()
            elif isinstance(val, symtab.Symtab):
                self.pi('    -%s: ' % (key))
                self.i()
                #for a,b in val.entries.items():
                    #if a != '__typedefs__' and a != '__types__' and 'type' in b.__dict__:
                        #self.p('%s: %s' %(a, b.type))
                self.u()
                self.pu()
            else:
                self.p('    -%s: ?' % (key))
        

    def vNodeList (self, node):
        self.p(node.__class__.__name__+'*')
        self.i()
        for c in node.children:
            self.visit(c)
        self.u()
