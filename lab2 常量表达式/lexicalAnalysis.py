#词法分析

# 读取到程序的哪一个字符
keyForProcedure = 0
lastKeyForProcedure=0

#程序读完
readAllProcedure=False


# 读取程序的下一个字符
def getC(procedure):
    global keyForProcedure
    global readAllProcedure
    keyForProcedure += 1
    if keyForProcedure - 1 >= len(procedure):
        readAllProcedure=True
        return "\n"
    return procedure[keyForProcedure - 1]


# 读取程序的上一个字符
def ungetC(procedure):
    global keyForProcedure
    keyForProcedure -= 1
    return procedure[keyForProcedure - 1]


# 查找保留字对应的类别码，如果不是保留字返回0
def getSymForReservedWord(token):
    if token == "int":
        return 11
    elif token == "main":
        return 12
    elif token == "return":
        return 13
    else:
        return 10

#八进制转十进制
def octalToDecimal(token):
    a=len(token)-1
    b=0
    for i in range(len(token)):
        b+=int(token[i])*(8**a)
        a-=1
    return b

#十六进制转十进制
def hexadecimalToDecimal(token):
    a=len(token)-1
    b=0
    c=0
    for i in range(len(token)):
        if token[i]=="a" or token[i]=="A":
            c=10
        elif token[i]=="b" or token[i]=="B":
            c=11
        elif token[i]=="c" or token[i]=="C":
            c=12
        elif token[i]=="d" or token[i]=="D":
            c=13
        elif token[i]=="e" or token[i]=="E":
            c=14
        elif token[i]=="f" or token[i]=="F":
            c=15
        else:
            c=int(token[i])
        b+=c*(16**a)
        a-=1
    return b


# 读入一个单词
def getSym(procedure,number):
    global keyForProcedure
    global readAllProcedure
    global lastKeyForProcedure
    a = getC(procedure)
    while a == " " or a == "\n" or a == "\t" or a=="\r":
        if readAllProcedure:
            return 60
        a = getC(procedure)
    lastKeyForProcedure=keyForProcedure-1
    token=""
    if a.isalpha():
        token += a
        b = getC(procedure)
        while b.isalpha()or b.isdigit() or b == "_":
            token += b
            b = getC(procedure)
        ungetC(procedure)
        c = getSymForReservedWord(token)
        return c
    elif a.isdigit():
        if a=="0":#八进制或十六进制或0
            b=getC(procedure)
            if b=="x" or b=="X":#十六进制
                c = getC(procedure)
                while c.isdigit() or c.isalpha():
                    if c.isdigit() or c=="a" or c=="b" or c=="c" or c=="d" or c=="e" or c=="f" or c=="A" or c=="B" or c=="C" or c=="D" or c=="E" or c=="F":
                        token += c
                        c = getC(procedure)
                    else:
                        return 40
                ungetC(procedure)
                number.append(hexadecimalToDecimal(token))
                return 20
            elif b.isdigit():#八进制
                if 0<=int(b)<=7:
                    token+=b
                    c=getC(procedure)
                    while c.isdigit()or c.isalpha():
                        if c.isalpha()or int(c)>7:
                            return 40
                        token+=c
                        c = getC(procedure)
                    ungetC(procedure)
                    number.append(octalToDecimal(token))
                    return 20
                else:
                    return 40
            else:
                number.append(a)
                ungetC(procedure)
                return 20
        else:#十进制
            token += a
            b = getC(procedure)
            while b.isdigit() or b.isalpha():
                if b.isalpha():
                    return 40
                token += b
                b = getC(procedure)
            ungetC(procedure)
            number.append(token)
            return 20
    elif a=="(":
        return 31
    elif a==")":
        return 32
    elif a=="{":
        return 33
    elif a==";":
        return 34
    elif a=="}":
        return 35
    elif a=="+":
        return 36
    elif a=="-":
        return 37
    elif a=="*":
        return 38
    elif a=="/":
        b=getC(procedure)
        if b=="/":
            c=getC(procedure)
            while c!="\n":
                c=getC(procedure)
            ungetC(procedure)
        elif b=="*":
            c=getC(procedure)
            d=getC(procedure)
            while c!="*" or d!="/":
                if readAllProcedure:
                    return 40
                ungetC(procedure)
                c = getC(procedure)
                d = getC(procedure)
        else:
            return 39
        return getSym(procedure,number)
    elif a=="%":
        return 310
    else:
        return 40

#退回一个单词
def ungetSym():
    global keyForProcedure,lastKeyForProcedure
    keyForProcedure=lastKeyForProcedure