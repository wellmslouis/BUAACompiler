# 具体处理
from constantExpression import runConstantExpression, runConstantExpressionB
from conditionExpression import handleCondition
from constantExpressionForConst import runConstantExpressionA
from syntaxAnalysis import CompUnit
from variableQuantity import rawVQs,vQLayer

#变量分层存入
def layerProcess(procedure):
    rvQs = rawVQs()
    number=[]
    print_=[]
    a = CompUnit(procedure, number, print_, rvQs)
    if not a:
        exit(1)
    layer=0
    v=vQLayer()
    for i in print_:
        if i==33:#{
            layer+=1
        elif i==35:#}
            layer-=1
        elif i==10:
            rvQs.getNext()
            v.add(rvQs.getName(),layer)
    return number,print_,v

def process(pr, vQs, reg, number, symRead, nid,llvm):
    i=0
    while pr[i]!=11 or pr[i+1]!=12:
        a=[]
        while pr[i]!=34:
            a.append(pr[i])
            i+=1
        a.append(pr[i])
        i+=1
        globalProcess(a, vQs, reg, number, symRead, nid,llvm)
    prA=pr[i:]
    b = len(prA) - 1
    prB=prA[5:b]
    paragraphProcess(prB, vQs, reg, number, symRead, nid,llvm,0,1,-1,-1)

#全局变量处理
def globalProcess(pr, vQs, reg, number, symRead, nid,llvm):
    sentenceAProcess(pr, vQs, reg, number, symRead, nid, llvm,0,0)

# 段落处理
#特别的，对于段落处理，会遍历所有传入代码，所以传入前必须进行拆分（能运行到结尾）
def paragraphProcess(pr, vQs, reg, number, symRead, nid,llvm,bid,layer,whileConditionBID,whileBID):
    curBID=bid
    a = []
    i = 0
    while i < len(pr):
        a.append(pr[i])
        if pr[i] == 34:
            if a[0] == 13:
                returnProcess(a, number, symRead, reg, nid, vQs,llvm,curBID,layer)
            else:
                sentenceAProcess(a, vQs, reg, number, symRead, nid,llvm,curBID,layer)
            a.clear()
        elif pr[i] == 15:
            a.pop()
            i,curBID = conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,curBID,layer,whileConditionBID,whileBID)
        elif pr[i]==33:#{
            a.pop()
            b=[]
            braces=[1]
            i+=1
            while len(braces)!=0:
                if pr[i]==33:
                    braces.append(1)
                elif pr[i]==35:
                    braces.pop()
                b.append(pr[i])
                i+=1
            b.pop()
            i-=1
            curBID=paragraphProcess(b,vQs, reg, number, symRead, nid,llvm,curBID,layer+1,whileConditionBID,whileBID)
            vQs.delete(layer+1)
        elif pr[i]==17:
            a.pop()
            i, curBID = conditionBProcess(pr, i, vQs, reg, number, symRead, nid, llvm, curBID, layer)
        elif pr[i]==18:#continue
            a.pop()
            llvm.setBrC(curBID,whileConditionBID)
            return curBID
        elif pr[i]==19:#break
            a.pop()
            llvm.setBrD(curBID, str(whileBID)+"!F")
            return curBID
        i += 1
    return curBID


# 语句处理（从上一个分号（不含）到下一个分号）
def sentenceAProcess(a, vQs, reg, number, symRead, nid,llvm,bid,layer):
    # 遍寻逗号
    isTwo = False
    for i in a:
        if i == 311:
            isTwo = True
            break
    if isTwo:
        if a[0] == 11:
            c = [11]
            j = 1
            while a[j] != 34:
                if a[j] == 311:
                    sentenceBProcess(c, vQs, reg, number, symRead, nid,llvm,bid,layer)
                    c.clear()
                    c.append(11)
                else:
                    c.append(a[j])
                j += 1
            sentenceBProcess(c, vQs, reg, number, symRead, nid,llvm,bid,layer)
        elif a[0] == 14 and a[1] == 11:
            c = [14, 11]
            j = 2
            while a[j] != 34:
                if a[j] == 311:
                    sentenceBProcess(c, vQs, reg, number, symRead, nid,llvm,bid,layer)
                    c.clear()
                    c.append(14)
                    c.append(11)
                else:
                    c.append(a[j])
                j += 1
        elif a[0] == 10:
            b = []
            for i in a:
                if i == 311:
                    break
                b.append(i)
            sentenceBProcess(b, vQs, reg, number, symRead, nid,llvm,bid,layer)
    else:
        a.pop()
        sentenceBProcess(a, vQs, reg, number, symRead, nid,llvm,bid,layer)


# 1：（定义）某（=某（右可以是常量表达式/输入函数））
# 2：输出函数
# 3.单独语句不处理
def sentenceBProcess(a, vQs, reg, number, symRead, nid,llvm,bid,layer):
    hasInt=False
    hasLeftBracket=False
    for i in a:
        if i==11:
            hasInt=True
        elif i==322:
            hasLeftBracket=True
    if hasInt and hasLeftBracket:
        return sentenceCProcess(a, vQs, reg, number, symRead, nid,llvm,bid,layer)
    if len(a)==0:
        return
    left = []
    right = []
    # 在等号左还是右
    isleft = True
    # 按照等号拆分为左右两个列表
    for i in a:
        if i == 312:
            isleft = False
            continue
        if isleft:
            left.append(i)
        else:
            right.append(i)
    idL,arrayLA,arrayLB = equalLeft(left, vQs, reg, number, symRead, nid,llvm,bid,layer)
    valueR = []
    # if idL!=-1:
    if len(right) != 0:
        func = False  # 是函数
        if right[0] == 10:
            vQs.getNext(layer)
            if vQs.matchName("getint",layer):
                valueR.append("%" + str(reg.getID()))
                #print(valueR[0] + " = call i32 @getint()")
                llvm.addPrintByID(bid,valueR[0] + " = call i32 @getint()")
                func = True
            elif vQs.matchName("getch",layer):
                valueR.append("%" + str(reg.getID()))
                #print(valueR[0] + " = call i32 @getch()")
                llvm.addPrintByID(bid, valueR[0] + " = call i32 @getch()")
                func = True
            else:
                vQs.getLast(layer)
        if func == False:
            valueA, valueB = runConstantExpression(right, number, symRead, reg, nid, vQs,llvm,bid,layer)
            valueR.append(valueA)
            valueR.append(valueB)
        else:
            if len(right)>3:
                rightA=[]
                rightA.append(valueR[0])
                for j in range(3,len(right)):
                    rightA.append(right[j])
                # print(rightA)
                valueA,valueB=runConstantExpression(rightA, number, symRead, reg, nid, vQs, llvm, bid, layer)
                valueR.clear()
                valueR.append(valueA)
                valueR.append(valueB)
    if idL != -1:  # 左不是函数
        if len(right) != 0:
            if layer==0 and valueR[1]:
                print("错误：使用变量为全局变量赋值！")
                exit(1)
            if len(valueR)>1:
                a=vQs.assign(layer,idL,valueR[0],valueR[1])
            else:
                a=vQs.assign(layer,idL,valueR[0],False)
            if a["type"]==1:
                llvm.addPrintByID(bid, "store i32 " + str(valueR[0]) + ", i32* %" + str(a["reg"]))
            elif a["type"]==3:
                llvm.addPrintByID(bid, "%" + str(reg.getID()) + " = getelementptr i32, i32* %" + str(a["reg"]) + ", i32 " + str(arrayLA))
                llvm.addPrintByID(bid, "store i32 " + str(valueR[0]) + ", i32* %" + str(reg.readID()))
            elif a["type"]==4:
                aa=[arrayLA,"*",a["length"],"+",arrayLB]
                llvm.addPrintByID(bid, "%" + str(reg.getID()) + " = getelementptr i32, i32* %" + str(a["reg"]) + ", i32 " + runConstantExpressionB(aa,reg,llvm,bid))
                llvm.addPrintByID(bid, "store i32 " + str(valueR[0]) + ", i32* %" + str(reg.readID()))

#专为定义数组
def sentenceCProcess(a, vQs, reg, number, symRead, nid,llvm,bid,layer):
    left = []
    right = []
    # 在等号左还是右
    isleft = True
    # 按照等号拆分为左右两个列表
    for i in a:
        if i == 312:
            isleft = False
            continue
        if isleft:
            left.append(i)
        else:
            right.append(i)

    #左边
    w=0#维度
    c=-1#left返回ID
    g=0#int数组首地址指针
    arrayLengthA=0#二维数组一维长度
    arrayLengthB=0
    for i in a:
        if i==322:
            w+=1
    if left[0]==11:#int
        if left[1] == 10:
            vQs.getNext(layer)
            j=2
            d=[]
            e=[]
            isPar=False
            while j <len(left):
                if left[j]==322:
                    isPar=True
                    j+=1
                    continue
                elif left[j]==323:
                    f=runConstantExpressionA(d, number, symRead,  nid, vQs,  layer)
                    e.append(f)
                    d.clear()
                    isPar=False
                    j+=1
                    continue
                if isPar:
                    d.append(left[j])
                j+=1
            c = vQs.defArrayInt(layer, w,e)
            if c!=-1:
                b = reg.getID()
                if w==1:
                    llvm.addPrintByID(bid, "%" + str(b) + " = alloca ["+str(e[0])+" x i32]")
                    g=reg.getID()
                    #%4 = getelementptr [2 x i32], [2 x i32]* %3, i32 0, i32 0
                    llvm.addPrintByID(bid, "%" + str(g) + " = getelementptr ["+str(e[0])+" x i32], ["+str(e[0])+" x i32]* %"+str(b)+", i32 0, i32 0")
                    vQs.defArrayIntReg(layer,g)
                elif w==2:
                    arrayLengthA=e[0]
                    llvm.addPrintByID(bid, "%" + str(b) + " = alloca ["+str(e[0])+" x ["+str(e[1])+" x i32]]")
                    #%3 = getelementptr [2 x [2 x i32]], [2 x [2 x i32]]* %2, i32 0, i32 0
                    #%4 = getelementptr [2 x i32], [2 x i32]* %3, i32 0, i32 0
                    llvm.addPrintByID(bid,"%" + str(reg.getID())+ " = getelementptr ["+str(e[0])+" x ["+str(e[1])+" x i32]], ["+str(e[0])+" x ["+str(e[1])+" x i32]]* %"+str(b)+", i32 0, i32 0")
                    g = reg.getID()
                    llvm.addPrintByID(bid, "%" + str(g) + " = getelementptr [" + str(e[1]) + " x i32], [" + str(e[1]) + " x i32]* %" + str(reg.readID()-1) + ", i32 0, i32 0")
                    vQs.defArrayIntReg(layer, g)
            else:
                print("错误：int数组重复定义！")
                exit(1)
        else:
            print("错误！")
            exit(1)
    elif left[0]==14:
        if left[1]==11:
            if left[2]==10:
                vQs.getNext(layer)
                j = 3
                d = []
                e = []
                isPar = False
                while j < len(left):
                    if left[j] == 322:
                        isPar = True
                        j += 1
                        continue
                    elif left[j] == 323:
                        f = runConstantExpressionA(d, number, symRead, nid, vQs, layer)
                        e.append(f)
                        d.clear()
                        isPar = False
                        j += 1
                        continue
                    if isPar:
                        d.append(left[j])
                    j += 1
                c = vQs.defArrayConst(layer, w, e)
                arrayLengthA=e[0]
                if len(e)==2:
                    arrayLengthB=e[1]
                if c == -1:
                    print("错误：int数组重复定义！")
                    exit(1)

    #右边
    if len(right)!=0:
        if left[0]==11:#int
            if w==1:
                #去除最外层大括号
                if right[0]==33:
                    right.pop(0)
                if right[len(right)-1]==35:
                    right.pop()
                d=[]
                e=[]
                for i in right:
                    if i==",":
                        e.append([])
                        for j in d:
                            e[len(e)-1].append(j)
                        d.clear()
                        i+=1
                        continue
                    d.append(i)
                    i+=1
                for i in range(len(e)):
                    valueA, valueB = runConstantExpression(e[i], number, symRead, reg, nid, vQs, llvm, bid, layer)
                    #%5 = getelementptr i32, i32* %4, i32 2
                    leftReg=reg.getID()
                    llvm.addPrintByID(bid, "%" + str(leftReg) + " = getelementptr i32, i32* %"+str(g)+", i32 "+str(i))
                    llvm.addPrintByID(bid,"store i32 "+str(valueA)+", i32* %"+str(leftReg))
            elif w==2:
                # 去除最外层大括号
                if right[0] == 33:
                    right.pop(0)
                if right[len(right) - 1] == 35:
                    right.pop()
                d = []
                e = []
                for i in right:
                    if i == ",":
                        e.append([])
                        for j in d:
                            e[len(e) - 1].append(j)
                        d.clear()
                        i += 1
                        continue
                    d.append(i)
                    i += 1
                h = []
                for k in range(len(e)):
                    e[k].pop(0)
                    e[k].pop()
                    f=[]
                    h.append([])
                    for i in e:
                        if i == ",":
                            h[k].append([])
                            for j in f:
                                h[k][len(h[k]) - 1].append(j)
                            f.clear()
                            i += 1
                            continue
                        f.append(i)
                        i += 1
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        valueA, valueB = runConstantExpression(h[i][j], number, symRead, reg, nid, vQs, llvm, bid, layer)
                        # %5 = getelementptr i32, i32* %4, i32 2
                        leftReg = reg.getID()
                        llvm.addPrintByID(bid,"%" + str(leftReg) + " = getelementptr i32, i32* %" + str(g) + ", i32 " + str(i*arrayLengthA+j))
                        llvm.addPrintByID(bid, "store i32 " + str(valueA) + ", i32* %" + str(leftReg))
        elif left[0]==14:#const
            if w==1:
                #去除最外层大括号
                if right[0]==33:
                    right.pop(0)
                if right[len(right)-1]==35:
                    right.pop()
                d=[]
                e=[]
                for i in right:
                    if i==",":
                        e.append([])
                        for j in d:
                            e[len(e)-1].append(j)
                        d.clear()
                        i+=1
                        continue
                    d.append(i)
                    i+=1
                arrayNum=[]
                for i in range(arrayLengthA):
                    arrayNum.append(0)
                for i in range(len(e)):
                    value = runConstantExpressionA(e[i], number, symRead, nid, vQs,layer)
                    arrayNum[i]=value
                vQs.assign(layer, c, arrayNum, False)
            elif w==2:
                # 去除最外层大括号
                if right[0] == 33:
                    right.pop(0)
                if right[len(right) - 1] == 35:
                    right.pop()
                d = []
                e = []
                for i in right:
                    if i == ",":
                        e.append([])
                        for j in d:
                            e[len(e) - 1].append(j)
                        d.clear()
                        i += 1
                        continue
                    d.append(i)
                    i += 1
                h = []
                for k in range(len(e)):
                    e[k].pop(0)
                    e[k].pop()
                    f=[]
                    h.append([])
                    for i in e:
                        if i == ",":
                            h[k].append([])
                            for j in f:
                                h[k][len(h[k]) - 1].append(j)
                            f.clear()
                            i += 1
                            continue
                        f.append(i)
                        i += 1
                arrayNum=[]
                for i in range(arrayLengthA):
                    arrayNum.append([])
                    for j in range(arrayLengthB):
                        arrayNum[i].append(0)
                for i in range(len(h)):
                    for j in range(len(h[i])):
                        value = runConstantExpressionA(h[i][j], number, symRead, nid, vQs,layer)
                        arrayNum[i][j]=value
                vQs.assign(layer, c, arrayNum, False)


# 返回vQs.getID()
def equalLeft(left, vQs, reg, number, symRead, nid,llvm,bid,layer):
    a = left[0]
    # int
    if a == 11:
        if left[1] == 10:
            vQs.getNext(layer)
            b = reg.getID()
            c=vQs.defInt(layer,b)
            if c!=-1:
                llvm.addPrintByID(bid,"%" + str(b) + " = alloca i32")
                return c,-1,-1
            else:
                print("错误：变量重复定义！")
                exit(1)
        else:
            print("错误！")
            exit(1)
    # const
    elif a == 14:
        # int
        if left[1] == 11:
            if left[2] == 10:
                vQs.getNext(layer)
                c=vQs.defConst(layer)
                if c!=-1:
                    return vQs.getID(layer),-1,-1
                else:
                    exit(1)
            else:
                exit(1)
        else:
            exit(1)
    elif a == 10:
        vQs.getNext(layer)
        if vQs.matchName("putint",layer):
            i = 2
            b = []  # 函数参数
            parenthese=[1]
            while len(parenthese)!=0:  # 不到右括号
                if left[i]==31:
                    parenthese.append(1)
                elif left[i]==32:
                    parenthese.pop()
                b.append(left[i])
                i += 1
            b.pop()
            valueA, valueB = runConstantExpression(b, number, symRead, reg, nid, vQs,llvm,bid,layer)
            # call void @ putint(i32 % 4)
            # print("call void @putint(i32 " + str(valueA) + ")")
            llvm.addPrintByID(bid, "call void @putint(i32 " + str(valueA) + ")")
            return -1,-1,-1
        elif vQs.matchName("putch",layer):
            i = 2
            b = []  # 函数参数
            parenthese = [1]
            while len(parenthese) != 0:  # 不到右括号
                if left[i] == 31:
                    parenthese.append(1)
                elif left[i] == 32:
                    parenthese.pop()
                b.append(left[i])
                i += 1
            b.pop()
            valueA, valueB = runConstantExpression(b, number, symRead, reg, nid, vQs,llvm,bid,layer)
            # call void @ putint(i32 % 4)
            # print("call void @putch(i32 " + str(valueA) + ")")
            llvm.addPrintByID(bid, "call void @putch(i32 " + str(valueA) + ")")
            return -1,-1,-1
        else:
            w=0
            for i in left:
                if i==322:
                    w+=1
            #如果左侧不只一个
            # if len(left)>1:
            #     for i in left:
            #         if i==20:
            #             nid.getID()
            if w==0:
                return vQs.getID(layer),-1,-1
            elif w==1:
                aa=[]
                i=2
                while i<len(left):
                    if left[i]==323:
                        valueA, valueB = runConstantExpression(aa, number, symRead, reg, nid, vQs, llvm, bid, layer)
                        return vQs.getID(layer),valueA,-1
                    aa.append(left[i])
                    i+=1
            elif w==2:
                aa = []
                valueA=0
                i = 2
                while i < len(left):
                    if left[i] == 323:
                        valueA, valueB = runConstantExpression(aa, number, symRead, reg, nid, vQs, llvm, bid, layer)
                        i+=1
                        break
                    aa.append(left[i])
                    i += 1
                i+=1
                aa.clear()
                while i<len(left):
                    if left[i] == 323:
                        valueC, valueD = runConstantExpression(aa, number, symRead, reg, nid, vQs, llvm, bid, layer)
                        return vQs.getID(layer),valueA,valueC
                    aa.append(left[i])
                    i += 1


def returnProcess(a, number, symRead, reg, nid, vQs,llvm,bid,layer):
    if a[0] == 13:
        i = 1
        b = []
        while a[i] != 34:
            b.append(a[i])
            i += 1
        valueA, valueB = runConstantExpression(b, number, symRead, reg, nid, vQs,llvm,bid,layer)
        llvm.addPrintByID(bid, "ret i32 " + str(valueA))

# 从if（含）起，读到最后（不含下一个），返回i
def conditionAProcess(pr, index, vQs, reg, number, symRead, nid,llvm,bid,layer,whileConditionBID,whileBID):
    i = index
    bidCT=0
    bidCF=0
    condition = []

    if pr[i] == 15:  # if
        i += 1
        if pr[i] == 31:  # (
            i += 1
            parentheses=[1]
            # while pr[i] != 32:  # )
            #     condition.append(pr[i])
            #     i += 1
            while i<len(pr):
                condition.append(pr[i])
                if pr[i]==31:
                    parentheses.append(1)
                elif pr[i]==32:
                    parentheses.pop()
                if len(parentheses) == 0:
                    break
                i+=1
            condition.pop()
    bidN=handleCondition(condition,vQs, reg, number, symRead, nid,llvm,bid,layer)
    bidNT=reg.getID()
    llvm.setBrT(bidN,bidNT)
    i+=1
    if pr[i]==33:
        braces=[1]#大括号栈，左1右2
        a=[]
        i+=1
        while i<len(pr):
            a.append(pr[i])
            if pr[i]==33:#{
                braces.append(1)
            elif pr[i]==35:#}
                braces.pop()
            if len(braces)==0:
                break
            i+=1
        a.pop()#最后一个}推出去
        bidCT=paragraphProcess(a, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1,whileConditionBID,whileBID)
        vQs.delete(layer + 1)
    elif pr[i]==15:
        i,bidCT=conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1,whileConditionBID,whileBID)
        vQs.delete(layer + 1)
    elif pr[i]==17:
        i, bidCT = conditionBProcess(pr, i, vQs, reg, number, symRead, nid, llvm, bidNT, layer + 1)
        vQs.delete(layer + 1)
    elif pr[i]==18:#continue
        llvm.setBrC(bidNT,whileConditionBID)
    elif pr[i]==19:
        llvm.setBrD(bidNT, str(whileBID) + "!F")
    #！待完善：不含大括号的定义
    else:
        a=[]
        while i<len(pr):
            a.append(pr[i])
            if pr[i] == 34:
                if a[0] == 13:
                    returnProcess(a, number, symRead, reg, nid, vQs,llvm,bidNT,layer+1)
                    vQs.delete(layer + 1)
                else:
                    sentenceAProcess(a, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1)
                    vQs.delete(layer + 1)
                break
            i+=1
    i+=1
    bidNF = reg.getID()
    llvm.setBrF(bidN, bidNF)
    if i<len(pr) and pr[i]==16:#else
        i+=1
        if pr[i] == 33:
            braces = [1]  # 大括号栈，左1右2
            a = []
            i += 1
            while i < len(pr):
                a.append(pr[i])
                if pr[i] == 33:  # {
                    braces.append(1)
                elif pr[i] == 35:  # }
                    if braces[len(braces) - 1] == 1:
                        braces.pop()
                    else:
                        braces.append(2)
                if len(braces) == 0:
                    break
                i += 1
            a.pop()  # 最后一个}推出去
            bidCF=paragraphProcess(a, vQs, reg, number, symRead, nid,llvm,bidNF,layer+1,whileConditionBID,whileBID)
            vQs.delete(layer + 1)
        elif pr[i] == 15:
            i,bidCF = conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,bidNF,layer,whileConditionBID,whileBID)
            vQs.delete(layer + 1)
        elif pr[i] == 17:
            i,bidCF = conditionBProcess(pr, i, vQs, reg, number, symRead, nid,llvm,bidNF,layer+1)
            vQs.delete(layer + 1)
        elif pr[i] == 18:  # continue
            llvm.setBrC(bidNF, whileConditionBID)
        elif pr[i] == 19:
            llvm.setBrD(bidNF, str(whileBID) + "!F")
        else:
            a = []
            while i < len(pr):
                a.append(pr[i])
                if pr[i] == 34:
                    if a[0] == 13:
                        returnProcess(a, number, symRead, reg, nid, vQs,llvm,bidNF,layer+1)
                        vQs.delete(layer + 1)
                    else:
                        sentenceAProcess(a, vQs, reg, number, symRead, nid,llvm,bidNF,layer+1)
                        vQs.delete(layer + 1)
                    break
                i += 1
    else:
        i-=1
    newBID=reg.getID()
    if bidCT==0:
        # llvm.addPrintByID(bidT,"br label %"+str(newBID))
        llvm.setBrB(bidNT,newBID)
    else:
        # llvm.addPrintByID(bidCT, "br label %" + str(newBID))
        llvm.setBrB(bidCT, newBID)
    if bidCF==0:
        llvm.setBrB(bidNF, newBID)
    else:
        llvm.setBrB(bidCF,newBID)
    return i,newBID


# 从while（含）起，读到最后（不含下一个），返回i
def conditionBProcess(pr, index, vQs, reg, number, symRead, nid,llvm,bid,layer):
    i = index
    condition = []
    #得到条件表达式condition
    if pr[i] == 17:  # while
        i += 1
        if pr[i] == 31:  # (
            i += 1
            parentheses=[1]
            # while pr[i] != 32:  # )
            #     condition.append(pr[i])
            #     i += 1
            while i<len(pr):
                condition.append(pr[i])
                if pr[i]==31:
                    parentheses.append(1)
                elif pr[i]==32:
                    parentheses.pop()
                if len(parentheses) == 0:
                    break
                i+=1
            condition.pop()
    bidCondition=reg.getID()
    llvm.setBrB(bid,bidCondition)
    bidN=handleCondition(condition,vQs, reg, number, symRead, nid,llvm,bidCondition,layer)#条件语句判断结束bid
    bidNT=reg.getID()
    llvm.setBrT(bidN,bidNT)
    i+=1
    bidC=bidNT
    if pr[i]==33:
        braces=[1]#大括号栈，左1右2
        a=[]
        i+=1
        while i<len(pr):
            a.append(pr[i])
            if pr[i]==33:#{
                braces.append(1)
            elif pr[i]==35:#}
                braces.pop()
            if len(braces)==0:
                break
            i+=1
        a.pop()#最后一个}推出去
        bidC=paragraphProcess(a, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1,bidCondition,bidN)
        vQs.delete(layer + 1)
    elif pr[i]==15:
        i,bidC=conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1,bidCondition,bidN)
        vQs.delete(layer + 1)
    elif pr[i]==17:
        i, bidC = conditionBProcess(pr, i, vQs, reg, number, symRead, nid, llvm, bidNT, layer + 1)
        vQs.delete(layer + 1)
    elif pr[i]==18:#continue
        llvm.setBrC(bidNT,bidCondition)
    elif pr[i]==19:
        llvm.setBrD(bidNT,str(bidN)+"!F")
    #！待完善：不含大括号的定义
    else:
        a=[]
        while i<len(pr):
            a.append(pr[i])
            if pr[i] == 34:
                if a[0] == 13:
                    returnProcess(a, number, symRead, reg, nid, vQs,llvm,bidNT,layer+1)
                    vQs.delete(layer + 1)
                else:
                    sentenceAProcess(a, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1)
                    vQs.delete(layer + 1)
                break
            i+=1
    llvm.setBrB(bidC,bidCondition)#while段落语句结束跳转回条件语句初
    newBID=reg.getID()
    llvm.setBrF(bidN, newBID)
    return i,newBID