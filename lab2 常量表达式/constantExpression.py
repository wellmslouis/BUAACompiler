#常量表达式

#翻译
def translateConstantExpression(pr,n,symRead):
    a=[]
    b=0
    for i in range(len(pr)):
        if pr[i]!=20:
            a.append(symRead[pr[i]])
        else:
            a.append(n[b])
            b+=1
    # print(a)
    return a
#处理
register=1
def handleConstantExpression(a,b):
    global register
    #消除括号
    i=b
    c=[]
    while i<len(a):
        if a[i]=="(":
            d,e=handleConstantExpression(a,i+1)
            c.append(d)
            i=e
        elif a[i]==")":
            break
        else:
            c.append(a[i])
        i+=1

    if len(c)==1:#只有数字或寄存器名称
        return c[0],i
    #判断是否有乘除余
    haveMulDivSrem=False
    for k in range(len(c)):
        if c[k]=="*" or c[k]=="/" or c[k]=="%":
            haveMulDivSrem=True
            break
    f=[]
    j=0
    isCounted=False
    if haveMulDivSrem:
        while j<len(c):
            g=True
            if not isCounted:
                if c[j]=="*" or c[j]=="/" or c[j]=="%":
                    if j<len(c)-1 and c[j+1]!="+" and c[j+1]!="-" and c[j+1]!="*" and c[j+1]!="/" and c[j+1]!="%":
                        if j-1>=0 and (c[j-1]!="+" and c[j-1]!="-" and c[j-1]!="*" and c[j-1]!="/" and c[j-1]!="%"):
                                f.pop()
                                f.append(printConstantExpression(c[j],c[j-1],c[j+1]))
                                isCounted=True
                        else:
                            f.append(printConstantExpression(c[j], 0, c[j + 1]))
                            isCounted=True
                        g=False
                        j+=2
            if g:
                f.append(c[j])
                j+=1
    else:
        while j<len(c):
            g=True
            if not isCounted:
                if c[j]=="+" or c[j]=="-":
                    if j<len(c)-1 and c[j+1]!="+" and c[j+1]!="-" and c[j+1]!="*" and c[j+1]!="/" and c[j+1]!="%":
                        if j-1>=0 and (c[j-1]!="+" and c[j-1]!="-" and c[j-1]!="*" and c[j-1]!="/" and c[j-1]!="%"):
                                f.pop()
                                f.append(printConstantExpression(c[j],c[j-1],c[j+1]))
                                isCounted = True
                        else:
                            f.append(printConstantExpression(c[j], 0, c[j + 1]))
                            isCounted = True
                        g=False
                        j+=2
            if g:
                f.append(c[j])
                j+=1
    return handleConstantExpression(f,0)[0],i

#输出
def printConstantExpression(sym,a,b):
    global register
    c="%"+str(register)
    d="\t"+c+"="
    if sym=="-":
        d+="sub"
    elif sym =="+":
        d+="add"
    elif sym=="*":
        d+="mul"
    elif sym =="/":
        d+="sdiv"
    elif sym=="%":
        d+="srem"
    d+=" i32 "
    d+=str(a)
    d+=","
    d+=str(b)
    print(d)
    register+=1
    return c
#封装运行
def runConstantExpression(constantExpression, number, symRead):
    handleConstantExpression(translateConstantExpression(constantExpression, number, symRead), 0)
    print("\tret i32 %" + str(register - 1))
    print("}")