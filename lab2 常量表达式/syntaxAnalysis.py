#语法分析
from lexicalAnalysis import getSym,ungetSym

def CompUnit(p,n,pr):
    if FuncDef(p,n,pr):
        return True
    else:
        return False

def FuncDef(p,n,pr):
    if FuncType(p, n, pr):
        if Ident(p,n,pr):
            if getSym(p,n)==31:
                pr.append(31)
                if getSym(p,n)==32:
                    pr.append(32)
                    if Block(p,n,pr):
                        return True
                else:
                    ungetSym()
            else:
                ungetSym()
    return False

def FuncType(p,n,pr):
    if getSym(p,n)==11:
        pr.append(11)
        return True
    else:
        ungetSym()
    return False

def Ident(p,n,pr):
    if getSym(p, n) == 12:
        pr.append(12)
        return True
    else:
        ungetSym()
    return False

def Block(p,n,pr):
    if getSym(p,n)==33:
        pr.append(33)
        if Stmt(p,n,pr):
            if getSym(p,n)==35:
                pr.append(35)
                return True
            else:
                ungetSym()
    else:
        ungetSym()
    return False

def Stmt(p,n,pr):
    if getSym(p,n)==13:
        pr.append(13)
        if Exp(p,n,pr):
            if getSym(p,n)==34:
                pr.append(34)
                return True
            else:
                ungetSym()
    else:
        ungetSym()
    return False

def Exp(p,n,pr):
    if AddExp(p,n,pr):
        return True
    return False

def AddExp(p,n,pr):
    if MulExp(p,n,pr):
        if AddExpA(p,n,pr):
            return True
    return False

def AddExpA(p,n,pr):
    a=getSym(p,n)
    if a==36 or a==37:
        pr.append(a)
        if MulExp(p,n,pr):
            if AddExpA(p,n,pr):
                return True
    else:
        ungetSym()
        return True
    return False


def MulExp(p,n,pr):
    if UnaryExp(p,n,pr):
        if MulExpA(p,n,pr):
            return True
    return False

def MulExpA(p,n,pr):
    a = getSym(p, n)
    if a == 38 or a == 39 or a==310:
        pr.append(a)
        if UnaryExp(p, n, pr):
            if MulExpA(p,n,pr):
                return True
    else:
        ungetSym()
        return True
    return False

def UnaryExp(p,n,pr):
    if PrimaryExp(p,n,pr):
        return True
    elif UnaryOp(p,n,pr):
        if UnaryExp(p,n,pr):
            return True
    return False

def PrimaryExp(p,n,pr):
    a=getSym(p,n)
    if a==31:
        pr.append(31)
        if Exp(p,n,pr):
            if getSym(p,n)==32:
                pr.append(32)
                return True
            else:
                ungetSym()
    elif a==20:
        pr.append(20)
        return True
    else:
        ungetSym()
    return False

def UnaryOp(p,n,pr):
    a=getSym(p,n)
    if a==36:
        pr.append(36)
        return True
    elif a==37:
        pr.append(37)
        return True
    else:
        ungetSym()
    return False