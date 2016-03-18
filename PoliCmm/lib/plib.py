import re, sys
allinput = ""
inputpos = 0
precision = 3
precisionstring = '%%.3f'
def readinput():
    global allinput, inputpos
    l = []
    while True:
        try:
            t = raw_input('') + '\n'
        except EOFError:
            break
        else:
            l.append(t)
    allinput = ''.join(l)
    inputpos = 0
        
patternint = re.compile('\s*\-?\d+')
def readint():
    global allinput, inputpos
    m = patternint.match(allinput, inputpos)
    inputpos += len(m.group(0))
    #allinput = allinput[len(m.group(0)):]
    return int(m.group(0))
    
def checkreadint(obj):
    global allinput, inputpos
    m = patternint.match(allinput, inputpos)
    if m:
        obj.value = int(m.group(0).strip())
        inputpos += len(m.group(0))
        #allinput = allinput[len(m.group(0)):]
        return True
    else: 
        return False
        
        
patterndouble = re.compile('\s*\-?\d+(\.\d*)?')
def readdouble():
    global allinput, inputpos
    m = patterndouble.match(allinput, inputpos)
    inputpos += len(m.group(0))
    #allinput = allinput[len(m.group(0)):]
    return float(m.group(0))
    
def checkreaddouble(obj):
    global allinput, inputpos
    m = patterndouble.match(allinput, inputpos)
    if m:
        obj.value = float(m.group(0).strip())
        inputpos += len(m.group(0))
        #allinput = allinput[len(m.group(0)):]
        return True
    else: 
        return False
        
patternchar = re.compile('\s*\S')
def readchar():
    global allinput, inputpos
    m = patternchar.match(allinput, inputpos)
    if m:
        inputpos += len(m.group(0))
        #allinput = allinput[len(m.group(0)):]
        return m.group(0).strip()[0]
    return '0'
    
def checkreadchar(obj):
    global allinput, inputpos
    m = patternchar.match(allinput, inputpos)
    if m:
        obj.value = m.group(0).strip()[0]
        inputpos += len(m.group(0))
        #allinput = allinput[len(m.group(0)):]
        return True
    else: 
        return False
        
        
patternstring = re.compile('\s*\S+')
def readstring():
    global allinput, inputpos
    m = patternstring.match(allinput, inputpos)
    inputpos += len(m.group(0))
    #allinput = allinput[len(m.group(0)):]
    return m.group(0).strip()
    
def checkreadstring(obj):
    global allinput, inputpos
    m = patternstring.match(allinput, inputpos)
    if m:
        obj.value = m.group(0).strip()
        
        inputpos += len(m.group(0))
        #allinput = allinput[len(m.group(0)):]
        return True
    else: 
        return False
        
def setprecision(p):
    global precision
    global precisionstring
    precision = p
    precisionstring = '%%.%df' % precision
        
class Wrapper:
    def __init__(self, obj):
        self.value = obj
        
class Stack:
    def __init__(self):
        self.st = []
    def push(self, obj):
        self.st.append(obj)
        return obj
    def pop(self):
        return self.st.pop()


class Var:
    def __init__(self, value):
        self.value = value
    def setValue(self, value):
        self.value = value
        return True
        
def inc(var):
    var.value += 1
    return var.value - 1
        
def preinc(var):
    var.value += 1
    return var.value
    
    
def dec(var):
    var.value -= 1
    return var.value + 1
        
def predec(var):
    var.value -= 1
    return var.value
    
def idem(var, p):
    return var
    
def setcharat(s, i, c):
    return s[0:i]+c+s[i+1:]