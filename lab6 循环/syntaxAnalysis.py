# 语法分析
from lexicalAnalysis import getSym, ungetSym, ungetTheSym


# CompUnit -> Decl* FuncDef
def CompUnit(p, n, pr, v):
    while True:
        a = getSym(p, n, v)
        b= getSym(p, n, v)
        if a==11 and b==12:
            ungetTheSym(2,n,v)
            if FuncDef(p, n, pr, v):
                return True
        else:
            ungetTheSym(2,n,v)
            if Decl(p,n,pr,v):
                continue
    return False


# Decl -> ConstDecl | VarDecl
# ConstDecl首字为'const'
# VarDecl首字为BType->'int'
def Decl(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 14:
        ungetSym(n, v)
        if ConstDecl(p, n, pr, v):
            return True
    elif a == 11:
        ungetSym(n, v)
        if VarDecl(p, n, pr, v):
            return True
    return False


# ConstDecl -> 'const' BType ConstDef { ',' ConstDef } ';'
def ConstDecl(p, n, pr, v):
    if getSym(p, n, v) == 14:
        pr.append(14)
        if BType(p, n, pr, v):
            if ConstDef(p, n, pr, v):
                while getSym(p, n, v) != 34:
                    ungetSym(n, v)
                    if getSym(p, n, v) == 311:
                        pr.append(311)
                        if ConstDef(p, n, pr, v):
                            continue
                    return False
                pr.append(34)
                return True
    return False


# BType -> 'int'
def BType(p, n, pr, v):
    if getSym(p, n, v) == 11:
        pr.append(11)
        return True
    return False


# ConstDef -> Ident(10) '=' ConstInitVal
def ConstDef(p, n, pr, v):
    if getSym(p, n, v) == 10:
        pr.append(10)
        if getSym(p, n, v) == 312:
            pr.append(312)
            if ConstInitVal(p, n, pr, v):
                return True
    return False


# ConstInitVal -> ConstExp
def ConstInitVal(p, n, pr, v):
    if ConstExp(p, n, pr, v):
        return True
    return False


# ConstExp -> AddExp
def ConstExp(p, n, pr, v):
    if AddExp(p, n, pr, v):
        return True
    return False


# VarDecl -> BType VarDef { ',' VarDef } ';'
def VarDecl(p, n, pr, v):
    if BType(p, n, pr, v):
        if VarDef(p, n, pr, v):
            while getSym(p, n, v) != 34:
                ungetSym(n, v)
                if getSym(p, n, v) == 311:
                    pr.append(311)
                    if VarDef(p, n, pr, v):
                        continue
                return False
            pr.append(34)
            return True
    return False


# VarDef -> Ident(10) VarDefA
def VarDef(p, n, pr, v):
    if getSym(p, n, v) == 10:
        pr.append(10)
        if VarDefA(p, n, pr, v):
            return True
    return False


# VarDefA -> '=' InitVal | ε
def VarDefA(p, n, pr, v):
    if getSym(p, n, v) == 312:
        pr.append(312)
        if InitVal(p, n, pr, v):
            return True
    else:
        ungetSym(n, v)
        return True


# InitVal -> Exp
def InitVal(p, n, pr, v):
    if Exp(p, n, pr, v):
        return True
    return False


# FuncDef -> FuncType Ident '(' ')' Block
# Ident仅为main(13)
def FuncDef(p, n, pr, v):
    if FuncType(p, n, pr, v):
        if Ident(p, n, pr, v):
            if getSym(p, n, v) == 31:
                pr.append(31)
                if getSym(p, n, v) == 32:
                    pr.append(32)
                    if Block(p, n, pr, v):
                        return True
                else:
                    ungetSym(n, v)
            else:
                ungetSym(n, v)
    return False


# FuncType -> 'int'
def FuncType(p, n, pr, v):
    if getSym(p, n, v) == 11:
        pr.append(11)
        return True
    else:
        ungetSym(n, v)
    return False


# Ident仅为main(13)
def Ident(p, n, pr, v):
    if getSym(p, n, v) == 12:
        pr.append(12)
        return True
    else:
        ungetSym(n, v)
    return False


# Block -> '{' { BlockItem } '}'
def Block(p, n, pr, v):
    if getSym(p, n, v) == 33:
        pr.append(33)
        while getSym(p, n, v) != 35:
            ungetSym(n, v)
            if BlockItem(p, n, pr, v):
                continue
            return False
        pr.append(35)
        return True
    return False


# BlockItem -> Decl | Stmt
# Decl首字为ConstDecl->'const'或VarDecl->Btype->'int'
# Stmt首字太过复杂，不予判断
def BlockItem(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 14 or a == 11:
        ungetSym(n, v)
        if Decl(p, n, pr, v):
            return True
    else:
        ungetSym(n, v)
        if Stmt(p, n, pr, v):
            return True
    return False


# Stmt -> LVal(10) '=' Exp ';' | [Exp] ';' | 'return' Exp ';' | Block | 'if' '(' Cond ')' Stmt [ 'else' Stmt | 'while' '(' Cond ')' Stmt ]
# 1首二字为VQ和‘=’
# 3首字为‘return'
# 4首字为’{‘
# 5首字为'if'
# 6首字为'while'
def Stmt(p, n, pr, v):
    a = getSym(p, n, v)
    b = getSym(p, n, v)
    if a == 13:
        pr.append(13)
        ungetSym(n, v)  # 把b退回去
        if Exp(p, n, pr, v):
            if getSym(p, n, v) == 34:
                pr.append(34)
                return True
    elif a == 33:
        ungetTheSym(2, n, v)  # 把a,b都退回去
        if Block(p, n, pr, v):
            return True
    elif a == 15:
        if b == 31:
            pr.append(15)
            pr.append(31)
            if Cond(p, n, pr, v):
                if getSym(p, n, v) == 32:
                    pr.append(32)
                    if Stmt(p, n, pr, v):
                        c = getSym(p, n, v)
                        if c == 16:
                            pr.append(16)
                            if Stmt(p, n, pr, v):
                                return True
                        else:
                            ungetSym(n, v)
                            return True
    elif a == 10 and b == 312:
        pr.append(10)
        pr.append(312)
        if Exp(p, n, pr, v):
            if getSym(p, n, v) == 34:
                pr.append(34)
                return True
    elif a==17:
        pr.append(17)
        if b==31:
            pr.append(31)
            if Cond(p,n,pr,v):
                if getSym(p, n, v)==32:
                    pr.append(32)
                    if Stmt(p,n,pr,v):
                        return True

    else:
        ungetTheSym(2, n, v)
        while getSym(p, n, v) != 34:
            ungetSym(n, v)
            if Exp(p, n, pr, v):
                continue
            return False
        pr.append(34)
        return True
    return False


# Exp -> AddExp
def Exp(p, n, pr, v):
    if AddExp(p, n, pr, v):
        return True
    return False


# Cond -> LOrExp
def Cond(p, n, pr, v):
    if LOrExp(p, n, pr, v):
        return True
    return False


# AddExp -> MulExp AddExpA
def AddExp(p, n, pr, v):
    if MulExp(p, n, pr, v):
        if AddExpA(p, n, pr, v):
            return True
    return False


# AddExpA -> ('+' | '−') MulExp AddExpA
def AddExpA(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 36 or a == 37:
        pr.append(a)
        if MulExp(p, n, pr, v):
            if AddExpA(p, n, pr, v):
                return True
    else:
        ungetSym(n, v)
        return True
    return False


# MulExp -> UnaryExp MulExpA
def MulExp(p, n, pr, v):
    if UnaryExp(p, n, pr, v):
        if MulExpA(p, n, pr, v):
            return True
    return False


# MulExpA -> ('*' | '/' | '%') UnaryExp MulExpA
def MulExpA(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 38 or a == 39 or a == 310:
        pr.append(a)
        if UnaryExp(p, n, pr, v):
            if MulExpA(p, n, pr, v):
                return True
    else:
        ungetSym(n, v)
        return True
    return False


# UnaryExp -> PrimaryExp | UnaryOp UnaryExp | Ident '(' [FuncRParams] ')'
# 后者首字为'+' | '-' | '|'
def UnaryExp(p, n, pr, v):
    a = getSym(p, n, v)
    b = getSym(p, n, v)
    if a == 36 or a == 37 or a==313:
        ungetTheSym(2, n, v)
        if UnaryOp(p, n, pr, v):
            if UnaryExp(p, n, pr, v):
                return True
    elif a == 10 and b == 31:
        pr.append(10)
        pr.append(31)
        # !待完善成1次
        while getSym(p, n, v) != 32:
            ungetSym(n, v)
            if FuncRParams(p, n, pr, v):
                continue
            return False
        pr.append(32)
        return True
    else:
        ungetTheSym(2, n, v)
        if PrimaryExp(p, n, pr, v):
            return True
    return False


# FuncRParams -> Exp { ',' Exp }
def FuncRParams(p, n, pr, v):
    if Exp(p, n, pr, v):
        while getSym(p, n, v) == 311:
            pr.append(311)
            if Exp(p, n, pr, v):
                continue
            return False
        ungetSym(n, v)
        return True
    return False


# PrimaryExp -> '(' Exp ')' | LVal(10) | Number(20)
def PrimaryExp(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 31:
        pr.append(31)
        if Exp(p, n, pr, v):
            if getSym(p, n, v) == 32:
                pr.append(32)
                return True
            else:
                ungetSym(n, v)
    elif a == 20 or a == 10:
        pr.append(a)
        return True
    return False


# UnaryOp -> '+' | '-' | '!'
def UnaryOp(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 36 or a == 37 or a == 313:
        pr.append(a)
        return True
    return False


# LOrExp -> LAndExp { '||' LAndExp }
def LOrExp(p, n, pr, v):
    if LAndExp(p, n, pr, v):
        while getSym(p, n, v) == 314:
            pr.append(314)
            if LAndExp(p, n, pr, v):
                continue
            return False
        ungetSym(n, v)
        return True
    return False


# LAndExp -> EqExp { '&&' EqExp }
def LAndExp(p, n, pr, v):
    if EqExp(p, n, pr, v):
        while getSym(p, n, v) == 315:
            pr.append(315)
            if EqExp(p, n, pr, v):
                continue
            return False
        ungetSym(n, v)
        return True
    return False

# EqExp -> RelExp { ('==' | '!=') RelExp }
def EqExp(p, n, pr, v):
    if RelExp(p, n, pr, v):
        a=getSym(p, n, v)
        while a==316 or a==317:
            pr.append(a)
            if RelExp(p, n, pr, v):
                a = getSym(p, n, v)
                continue
            return False
        ungetSym(n, v)
        return True
    return False

# RelExp -> AddExp { ('<' | '>' | '<=' | '>=') AddExp }
def RelExp(p, n, pr, v):
    if AddExp(p, n, pr, v):
        a=getSym(p, n, v)
        while a==318 or a==319 or a==320 or a==321:
            pr.append(a)
            if AddExp(p, n, pr, v):
                a = getSym(p, n, v)
                continue
            return False
        ungetSym(n, v)
        return True
    return False