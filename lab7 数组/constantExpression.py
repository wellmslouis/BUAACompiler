#常量表达式

#翻译
from constantExpressionForConst import runConstantExpressionA


def translateConstantExpression(pr,n,symRead,nid,vQs,reg,llvm,bid,layer):
    a=[]
    haveVQ=False
    i=0
    while i<len(pr):
        if not str(pr[i]).isdigit():
            a.append(pr[i])
        elif pr[i]==20:
            a.append(n[nid.getID()])
        elif pr[i]==10:
            if i<len(pr)-1 and pr[i+1]==322:
                arrayA=[]
                while i<len(pr) and pr[i]!=31 and pr[i]!=32 and pr[i]!=36 and pr[i]!=37 and pr[i]!=38 and pr[i]!=39 and pr[i]!=310:
                    arrayA.append(pr[i])
                    i+=1
                a.append(handleArray(arrayA, n, symRead,reg,nid,vQs,llvm,bid,layer))
                if i<len(pr):
                    a.append(symRead[pr[i]])
            else:
                vQs.getNext(layer)
                r = vQs.getValue(layer)
                if r["type"] == 1:
                    b = reg.getID()
                    llvm.addPrintByID(bid, "%" + str(b) + " = load i32, i32* %" + str(r["reg"]))  # 准备
                    a.append("%" + str(b))
                    haveVQ = True
                elif r["type"] == 2:
                    a.append(r["num"])
        else:
            a.append(symRead[pr[i]])
        i+=1
    # print(a)
    return a,haveVQ

#处理
#register=1

def handleConstantExpression(a,b,reg,llvm,bid):
    #消除括号
    i=b
    c=[]
    while i<len(a):
        if a[i]=="(":
            d,e=handleConstantExpression(a,i+1,reg,llvm,bid)
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
                                f.append(printConstantExpression(c[j],c[j-1],c[j+1],reg,llvm,bid))
                                isCounted=True
                        else:
                            f.append(printConstantExpression(c[j], 0, c[j + 1],reg,llvm,bid))
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
                                f.append(printConstantExpression(c[j],c[j-1],c[j+1],reg,llvm,bid))
                                isCounted = True
                        else:
                            f.append(printConstantExpression(c[j], 0, c[j + 1],reg,llvm,bid))
                            isCounted = True
                        g=False
                        j+=2
            if g:
                f.append(c[j])
                j+=1
    return handleConstantExpression(f,0,reg,llvm,bid)[0],i

#输出
def printConstantExpression(sym,a,b,reg,llvm,bid):
    #global register
    c="%"+str(reg.getID())
    d=c+"="
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
    elif sym=="!":
        # d+="miao"
        #     icmp eq i32 %2, 0
        d+="icmp eq i32 "
        d += str(a)
        d += ","
        d += str(b)
        llvm.addPrintByID(bid, d)
        e="%"+str(reg.getID())
        f=e+"=zext i1 "
        f+=c
        f+=" to i32"
        llvm.addPrintByID(bid,f)
        return e
    d+=" i32 "
    d+=str(a)
    d+=","
    d+=str(b)
    llvm.addPrintByID(bid,d)
    #register+=1
    return c

#封装运行,返回：数或寄存器，是否含有变量
def runConstantExpression(constantExpression, number, symRead,reg,nid,vQs,llvm,bid,layer):
    # if len(constantExpression)==1:
    #     a=constantExpression[0]
    #     if a==10:
    #         vQs.getNext(layer)
    #         r = vQs.getValue(layer)
    #         if r["type"] == 1:
    #             b = reg.getID()
    #             llvm.addPrintByID(bid, "%" + str(b) + " = load i32, i32* %" + str(r["reg"]))  # 准备
    #             return "%" + str(b), True
    #         elif r["type"] == 2:
    #             return r["num"]
    #     elif a==20:
    #         c=number[nid.getID()]
    #         return c,False
    # else:
    a,b=translateConstantExpression(constantExpression, number, symRead,nid,vQs,reg,llvm,bid,layer)
    if len(a)==1:
        return a[0], b
    else:
        handleConstantExpression(a, 0,reg,llvm,bid)
        return "%" + str(reg.readID()), b

def runConstantExpressionB(a,reg,llvm,bid):
    handleConstantExpression(a, 0,reg,llvm,bid)
    return "%"+str(reg.readID())

#a形式：数组名+[+...+]
def handleArray(a, number, symRead,reg,nid,vQs,llvm,bid,layer):
    r=vQs.getValue(layer)
    if r["type"]==3:
        i=2
        b=[]
        while i<len(a)-1:
            b.append(a[i])
            i+=1
        valueA,valueB=runConstantExpression(b, number, symRead, reg, nid, vQs, llvm, bid, layer)
        llvm.addPrintByID(bid, "%" + str(reg.getID()) + " = getelementptr i32, i32* %" + str(r["reg"]) + ", i32 " + valueA)
        return reg.readID()
    elif r["type"]==4:
        aa = []
        valueA = 0
        valueC=0
        i = 2
        while i < len(a):
            if a[i] == 323:
                valueA, valueB = runConstantExpression(aa, number, symRead, reg, nid, vQs, llvm, bid, layer)
                i += 1
                break
            aa.append(a[i])
            i += 1
        i += 1
        aa.clear()
        while i < len(a):
            if a[i] == 323:
                valueC, valueD = runConstantExpression(aa, number, symRead, reg, nid, vQs, llvm, bid, layer)
            aa.append(a[i])
            i += 1
        aa = [valueA, "*", a["length"], "+", valueC]
        llvm.addPrintByID(bid,"%" + str(reg.getID()) + " = getelementptr i32, i32* %" + str(r["reg"]) + ", i32 " + runConstantExpressionB(aa,reg,llvm,bid))
        return reg.readID()
    elif r["type"]==5:
        aa = []
        valueA = -1
        valueC = -1
        i = 2
        while i < len(a):
            if a[i] == 323:
                valueA= runConstantExpressionA(aa, number, symRead,  nid, vQs,  layer)
                i += 1
                break
            aa.append(a[i])
            i += 1
        i += 1
        aa.clear()
        while i < len(a):
            if a[i] == 323:
                valueC = runConstantExpressionA(aa, number, symRead,  nid, vQs,  layer)
            aa.append(a[i])
            i += 1
        if valueC==-1:#一维
            return r["num"][int(valueA)]
        else:
            return r["num"][int(valueA)][int(valueC)]