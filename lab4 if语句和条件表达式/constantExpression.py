#常量表达式

#翻译
def translateConstantExpression(pr,n,symRead,nid,vQs,reg,llvm,bid):
    a=[]
    haveVQ=False
    for i in range(len(pr)):
        if pr[i]==20:
            a.append(n[nid.getID()])
        elif pr[i]==10:
            vQs.getNext()
            if vQs.getType()==10 and vQs.getReg()!=0:
                # %5 = load i32, i32* %2
                b = reg.getID()
                llvm.addPrintByID(bid,"%"+str(b)+" = load i32, i32* %"+str(vQs.getReg()))#准备
                a.append("%"+str(b))
                haveVQ=True
            elif vQs.getType()==20 and vQs.getNum()!="":
                a.append(vQs.getNum())
            else:
                print("错误：未定义的变量！")
                exit(1)
        else:
            a.append(symRead[pr[i]])
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
def runConstantExpression(constantExpression, number, symRead,reg,nid,vQs,llvm,bid):
    if len(constantExpression)==1:
        a=constantExpression[0]
        if a==10:
            vQs.getNext()
            if vQs.getType() == 10 and vQs.getReg() != 0:
                b = reg.getID()
                if vQs.getReg() != 0:
                    # %5 = load i32, i32* %2
                    llvm.addPrintByID(bid,"%" + str(b) + " = load i32, i32* %" + str(vQs.getReg()))#准备
                    return "%"+str(b),True
            elif vQs.getType()==20 and vQs.getNum()!="":
                return vQs.getNum(),False
            else:
                print("错误：未定义的变量！")
                exit(1)
        elif a==20:
            c=number[nid.getID()]
            return c,False
    else:
        a,b=translateConstantExpression(constantExpression, number, symRead,nid,vQs,reg,llvm,bid)
        handleConstantExpression(a, 0,reg,llvm,bid)
        return "%"+str(reg.readID()),b