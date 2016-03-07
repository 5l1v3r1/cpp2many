
import visitor


class Formatter (visitor.Visitor):

    '''Enriches the Visitor class with basic output functions with format control.'''

    def __init__ (self, out, tab=4):
        visitor.Visitor.__init__(self)
        self.out = out
        self.ind = 0
        self.tab = tab
        self.tabed = False

    def i (self):
        '''Indent.'''
        self.ind += 1

    def u (self):
        '''Unindent.'''
        self.ind -= 1

    def p (self, str=''):
        '''Print with possible indentation and linebreak.'''
        if not self.tabed:
            self.out.write(' ' * (self.tab * self.ind))
        self.out.write(str + '\n')
        self.tabed = False

    def w (self, str):
        '''Print with possible indentation and without linebreak.'''
        if not self.tabed:
            self.out.write(' ' * (self.tab * self.ind))
        self.out.write(str + ' ')
        self.tabed = True

    def ipu (self, str=''):
        '''indent, print, unindent.'''
        self.i()
        self.p(str)
        self.u()

    def upi (self, str=''):
        '''unindent, print, indent.'''
        self.u()
        self.p(str='')
        self.i()

    def pu (self, str=''):
        '''print, unindent.'''
        self.p(str)
        self.u()

    def pi (self, str=''):
        '''print, indent.'''
        self.p(str)
        self.i()

    def up (self, str=''):
        '''unindent, print.'''
        self.u()
        self.p(str)

    def uw (self, str=''):
        '''unindent, write.'''
        self.u()
        self.w(str)
