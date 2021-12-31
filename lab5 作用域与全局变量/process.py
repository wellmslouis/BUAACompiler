# 具体处理
from constantExpression import runConstantExpression
from conditionExpression import handleCondition
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


# 段落处理
#特别的，对于段落处理，会遍历所有传入代码，所以传入前必须进行拆分
def paragraphProcess(pr, vQs, reg, number, symRead, nid,llvm,bid,layer):
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
            i,curBID = conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,curBID,layer)
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
            curBID=paragraphProcess(b,vQs, reg, number, symRead, nid,llvm,curBID,layer+1)
            vQs.delete(layer+1)
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
    idL = equalLeft(left, vQs, reg, number, symRead, nid,llvm,bid,layer)
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
    if idL != -1:  # 不是函数
        if len(right) != 0:
            # # int类型已定义
            # if vQs.getTypeForID(idL,layer) == 10 and vQs.getRegForID(idL,layer) != 0:
            #     # store i32 % 2, i32 * % 1
            #     llvm.addPrintByID(bid, "store i32 " + str(valueR[0]) + ", i32* %" + str(vQs.getRegForID(idL,layer)))
            # # const类型无值
            # elif vQs.getTypeForID(idL,layer) == 20:
            #     if vQs.getNumForID(idL,layer) == "":
            #         if len(valueR) > 1:
            #             if valueR[1]:
            #                 print("错误：使用变量为常量赋值！")
            #                 exit(1)
            #         vQs.setNumForID(valueR[0], idL,layer)
            #     else:
            #         print("错误：常量已赋值！")
            #         exit(1)
            if len(valueR)>1:
                a=vQs.assign(layer,idL,valueR[0],valueR[1])
            else:
                a=vQs.assign(layer,idL,valueR[0],False)
            if a["type"]==1:
                llvm.addPrintByID(bid, "store i32 " + str(valueR[0]) + ", i32* %" + str(a["reg"]))


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
                return c
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
                    return vQs.getID(layer)
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
            while left[i] != 32:  # 不到右括号
                b.append(left[i])
                i += 1
            valueA, valueB = runConstantExpression(b, number, symRead, reg, nid, vQs,llvm,bid,layer)
            # call void @ putint(i32 % 4)
            # print("call void @putint(i32 " + str(valueA) + ")")
            llvm.addPrintByID(bid, "call void @putint(i32 " + str(valueA) + ")")
            return -1
        elif vQs.matchName("putch",layer):
            i = 2
            b = []  # 函数参数
            while left[i] != 32:  # 不到右括号
                b.append(left[i])
                i += 1
            valueA, valueB = runConstantExpression(b, number, symRead, reg, nid, vQs,llvm,bid,layer)
            # call void @ putint(i32 % 4)
            # print("call void @putch(i32 " + str(valueA) + ")")
            llvm.addPrintByID(bid, "call void @putch(i32 " + str(valueA) + ")")
            return -1
        else:
            return vQs.getID(layer)


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
def conditionAProcess(pr, index, vQs, reg, number, symRead, nid,llvm,bid,layer):
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
        bidCT=paragraphProcess(a, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1)
        vQs.delete(layer + 1)
    elif pr[i]==15:
        i,bidCT=conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,bidNT,layer+1)
        vQs.delete(layer + 1)
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
            bidCF=paragraphProcess(a, vQs, reg, number, symRead, nid,llvm,bidNF,layer+1)
            vQs.delete(layer + 1)
        elif pr[i] == 15:
            i,bidCF = conditionAProcess(pr, i, vQs, reg, number, symRead, nid,llvm,bidNF,layer+1)
            vQs.delete(layer + 1)
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