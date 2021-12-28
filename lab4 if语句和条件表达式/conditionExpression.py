#条件表达式
from constantExpression import runConstantExpression

#不含且或的表达式
#左 (符号 右)
def conditionA(c, vQs, reg, number, symRead, nid,llvm,bid):
    hasSym=False
    symNum=0
    left=[]
    right=[]
    for i in c:
        if i==316 or i==317 or i==318 or i==319 or i==320 or i==321:
            hasSym=True
            symNum=i
            continue
        if hasSym:
            right.append(i)
        else:
            left.append(i)
    numOperator={
        316:'eq',
        317:'ne',
        318:'slt',
        319:'sgt',
        320:'sle',
        321:'sge'
    }
    if hasSym:
        valueLA,valueLB=runConstantExpression(left,number,symRead,reg,nid,vQs,llvm,bid)
        valueRA,valueRB=runConstantExpression(right,number,symRead,reg,nid,vQs,llvm,bid)
        a = str(reg.getID())
        llvm.addPrintByID(bid, "%" + a + "=icmp "+numOperator[symNum]+" i32 " + valueLA + ", "+valueRA)
    else:
        valueA,valueB=runConstantExpression(c,number,symRead,reg,nid,vQs,llvm,bid)
        a=str(reg.getID())
        llvm.addPrintByID(bid,"%"+a+"=icmp ne i32 "+valueA+", 0")
    bidT=reg.getID()
    bidF=reg.getID()
    # br i1 %7,label %8, label %10
    llvm.addPrintByID(bid,"br i1 %"+a+",label %"+str(bidT)+", label %"+str(bidF))
    return bidT,bidF

#或表达式
def conditionOr(bidAT,bidAF,right, vQs, reg, number, symRead, nid,llvm):
    bidBT,bidBF=conditionA(right,vQs, reg, number, symRead, nid,llvm,bidAF)
    llvm.addPrintByID(bidAT, "br label %"+str(bidBT))
    return bidBT,bidBF

#且表达式
def conditionAnd(bidAT, bidAF ,right, vQs, reg, number, symRead, nid,llvm):
    bidBT, bidBF = conditionA(right, vQs, reg, number, symRead, nid, llvm, bidAT)
    llvm.addPrintByID(bidAF, "br label %" + str(bidBF))
    return bidBT, bidBF

#封装条件表达式
def handleCondition(c, vQs, reg, number, symRead, nid,llvm,bid):
    i=0
    a=[]
    b=[]
    while i<len(c):
        if c[i]==314 or c[i]==315:
            #待完善！
            b.append(a)
            b.append(c[i])
            a.clear()
        else:
            a.append(c[i])
        i+=1
    b.append(a)
    j=0
    bidCT,bidCF=conditionA(b[j],vQs, reg, number, symRead, nid,llvm,bid)
    j+=1
    while j<len(b):
        if b[j]==314:
            bidCT,bidCF=conditionOr(bidCT, bidCF,b[j+1], vQs, reg, number, symRead, nid, llvm)
        elif b[j]==315:
            bidCT, bidCF = conditionAnd(bidCT, bidCF, b[j + 1], vQs, reg, number, symRead, nid, llvm)
        j+=2
    return bidCT,bidCF