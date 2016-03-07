#!/usr/bin/python -W ignore::DeprecationWarning


import sys
import optparse
import os.path
import ply.lex as lex
import ply.yacc as yacc
import parser
import writer
import pascal
import java
import python
import ada
import symtab


extensions = {
    'writer'    : '.ast',
    'pascal'    : '.pas',
    'java'      : '.java',
    'python'    : '.py',
    'scheme'    : '.scm',
    'ada'       : '.ada',
}


usage = 'usage: %prog [options] ccfiles'
version = '%prog 1.0'

parser = optparse.OptionParser(usage=usage, version=version)
parser.add_option('-w', '--writer',
                  action='store_true', dest='writer', default=False,
                  help='write the AST')
parser.add_option('-p', '--pascal',
                  action='store_true', dest='pascal', default=False,
                  help='compile to Pascal')
parser.add_option('-j', '--java',
                  action='store_true', dest='java', default=False,
                  help='compile to Java')
parser.add_option('-y', '--python',
                  action='store_true', dest='python', default=False,
                  help='compile to Python')
parser.add_option('-a', '--ada',
                  action='store_true', dest='ada', default=False,
                  help='compile to Ada')
parser.add_option('-o', '--stdout',
                  action='store_true', dest='stdout', default=False,
                  help='output to stdout rather than a file')
parser.add_option('-i', '--ignoreerrors',
                  action='store_true', dest='ignoreerrors', default=False,
                  help='ignore errors')
(options, args) = parser.parse_args()



for filename in args:

    try:
        # Get the input program
        # print >>sys.stderr, 'reading ' + filename
        f = open(filename)
        s = f.read()
        f.close()

        # Parse and get AST
        # print >>sys.stderr, 'parsing'
        ast = yacc.parse(s)#, debug=1)

        # Semantic analysis.
        symtab.SymtabVisitor().visit(ast)

        # Output for each active visitor in the options dicst
        for lan, ext in extensions.iteritems():
            if options.__dict__.get(lan, False):
                if options.stdout:
                    name = 'stdout'
                    f = sys.stdout
                else:
                    name = os.path.splitext(filename)[0]+ext
                    f = open(name, 'w')
                #print >>sys.stderr, lan + ': ' + name
                eval('%s.%s(f).visit(ast)' % (lan, lan.capitalize()))
                if (lan=='writer'):
                    symtab.SymtabVisitor().visit(ast)
                    #print ast.symtab.entries

                if not options.stdout:
                    f.close()

    except Exception, e:
        if options.ignoreerrors:
            print >>sys.stderr, 'exception:', e.args
        else:
            raise
    finally:
        #print >>sys.stderr
        pass


