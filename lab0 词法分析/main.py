import sys

# 读取到程序的哪一个字符
keyForProcedure = 0


# 读取程序的下一个字符
def getC(procedure):
    global keyForProcedure
    keyForProcedure += 1
    if keyForProcedure-1>=len(procedure):
        return ' '
    return procedure[keyForProcedure - 1]


# 读取程序的上一个字符
def ungetC(procedure):
    global keyForProcedure
    keyForProcedure -= 1
    return procedure[keyForProcedure - 1]


# 查找保留字对应的类别码，如果不是保留字返回0
def getSymForReservedWord(token):
    if token == "if":
        return 3
    elif token == "else":
        return 4
    elif token == "while":
        return 5
    elif token == "break":
        return 6
    elif token == "continue":
        return 7
    elif token == "return":
        return 8
    else:
        return 0


# 返回类别码
def getSym(procedure, ident, number):
    global keyForProcedure
    a = getC(procedure)
    if a == " " or a == "\n" or a == "\t":
        return -1
    token = ""
    if a.isalpha() or a == "_":
        token += a
        b = getC(procedure)
        while b.isalpha() or b.isdigit() or b == "_":
            token += b
            b = getC(procedure)
        ungetC(procedure)
        c = getSymForReservedWord(token)
        if c == 0:  # 不是保留字
            ident.append(token)
            return 1
        else:
            return c
    elif a.isdigit():
        token += a
        b = getC(procedure)
        while b.isdigit():
            token += b
            b = getC(procedure)
        ungetC(procedure)
        number.append(token)
        return 2
    elif a == "=":
        token += a
        b = getC(procedure)
        token += b
        if token == "==":
            return 20
        else:
            ungetC(procedure)
            return 9
    elif a == ";":
        return 10
    elif a == "(":
        return 11
    elif a == ")":
        return 12
    elif a == "{":
        return 13
    elif a == "}":
        return 14
    elif a == "+":
        return 15
    elif a == "*":
        return 16
    elif a == "/":
        return 17
    elif a == "<":
        return 18
    elif a == ">":
        return 19
    else:
        return 21


if __name__ == '__main__':
    # 程序存在于这个字符串中
    procedure=""
    for l in sys.stdin:
        procedure += l
    # 类别码-输出字典
    symPrint = {
        1: "Ident",
        2: "Number",
        3: "If",
        4: "Else",
        5: "While",
        6: "Break",
        7: "Continue",
        8: "Return",
        9: "Assign",
        10: "Semicolon",
        11: "LPar",
        12: "RPar",
        13: "LBrace",
        14: "RBrace",
        15: "Plus",
        16: "Mult",
        17: "Div",
        18: "Lt",
        19: "Gt",
        20: "Eq",
        21: "Err"
    }
    ident = []
    keyForIdent = 0
    number = []
    keyForNumber = 0
    # 程序转化而成的类别码存在于这个数组中
    syms = []

    while keyForProcedure < len(procedure):
        a = getSym(procedure, ident, number)
        if a!=-1:
            syms.append(a)
        if a == 21:
            break

    for i in syms:
        print(symPrint[i],end='')
        if i == 1:
            print("(" + ident[keyForIdent] + ")")
            keyForIdent += 1
        elif i == 2:
            print("(" + number[keyForNumber] + ")")
            keyForNumber += 1
        elif i == 21:
            break
        else:
            print()
