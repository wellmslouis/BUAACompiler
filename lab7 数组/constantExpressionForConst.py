#能即时求值的常量表达式

#翻译
def translateConstantExpression(pr,n,symRead,nid,vQs,layer):
    a=[]
    for i in range(len(pr)):
        if not str(pr[i]).isdigit():
            a.append(pr[i])
        elif pr[i]==20:
            a.append(n[nid.getID()])
        elif pr[i]==10:
            vQs.getNext(layer)
            r=vQs.getValue(layer)
            if r["type"]==2:
                a.append(r["num"])
        else:
            a.append(symRead[pr[i]])
    # print(a)
    return a

#处理
#register=1

def handleConstantExpression(a,b):
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
                    if j<len(c)-1 and c[j+1]!="+" and c[j+1]!="-" and c[j+1]!="!" and c[j+1]!="*" and c[j+1]!="/" and c[j+1]!="%":
                        if j-1>=0 and (c[j-1]!="+" and c[j-1]!="-" and c[j-1]!="!" and c[j-1]!="*" and c[j-1]!="/" and c[j-1]!="%"):
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
                if c[j]=="+" or c[j]=="-" or c[j]=="!":
                    if j<len(c)-1 and c[j+1]!="+" and c[j+1]!="-" and c[j+1]!="!" and c[j+1]!="*" and c[j+1]!="/" and c[j+1]!="%":
                        if j-1>=0 and (c[j-1]!="+" and c[j-1]!="-" and c[j-1]!="!" and c[j-1]!="*" and c[j-1]!="/" and c[j-1]!="%"):
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
    c=0
    a=int(a)
    b=int(b)
    if sym=="-":
        c=a-b
    elif sym =="+":
        c=a+b
    elif sym=="*":
        c=a*b
    elif sym =="/":
        c=a/b
    elif sym=="%":
        c=a%b
    return c

#封装运行,返回：数
def runConstantExpressionA(constantExpression, number, symRead,nid,vQs,layer):
    if len(constantExpression)==1:
        a=constantExpression[0]
        if a==10:
            vQs.getNext(layer)
            r = vQs.getValue(layer)
            if r["type"] == 2:
                return r["num"]
        elif a==20:
            c=number[nid.getID()]
            return c
    else:
        a=translateConstantExpression(constantExpression, number, symRead,nid,vQs,layer)
        b,c=handleConstantExpression(a, 0)
        return b