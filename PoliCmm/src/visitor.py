
class Visitor:
    
    '''The base visitor class. This is an abstract base class.'''

    def __init__(self):
        pass

    def visit(self, node):
        '''Visits the given node by telling the node to call the
        visitor's class-specific visitor method for that node's
        class (i.e., double dispatching).'''        
        return node.accept(self)

