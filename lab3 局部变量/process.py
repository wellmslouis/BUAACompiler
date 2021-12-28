#具体处理
from constantExpression import runConstantExpression
#段落处理
def paragraphProcess(pr,vQs,reg,number,symRead,nid):
    #去除最外层
    b = []
    a = False
    d=False
    e=[]
    for i in range(len(pr)):
        if pr[i] == 33:
            a = True
            continue
        elif pr[i] == 13:
            a = False
            d=True
        elif pr[i]==35:
            d=False
        if a:
            b.append(pr[i])
        if d:
            e.append(pr[i])
    #拆分为语句
    c=[]
    for i in b:
        c.append(i)
        if i==34:
            sentenceAProcess(c,vQs,reg,number,symRead,nid)
            c.clear()
    returnProcess(e,number,symRead,reg,nid,vQs)

def sentenceAProcess(a,vQs,reg,number,symRead,nid):
    #遍寻逗号
    isTwo=False
    for i in a:
        if i==311:
            isTwo=True
            break
    if isTwo:
        if a[0]==11:
            c=[11]
            j=1
            while a[j]!=34:
                if a[j]==311:
                    sentenceBProcess(c, vQs, reg, number, symRead, nid)
                    c.clear()
                    c.append(11)
                else:
                    c.append(a[j])
                j+=1
            sentenceBProcess(c, vQs, reg, number, symRead, nid)
        elif a[0]==14 and a[1]==11:
            c = [14,11]
            j = 2
            while a[j] != 34:
                if a[j] == 311:
                    sentenceBProcess(c, vQs, reg, number, symRead, nid)
                    c.clear()
                    c.append(14)
                    c.append(11)
                else:
                    c.append(a[j])
                j += 1
        elif a[0]==10:
            b=[]
            for i in a:
                if i==311:
                    break
                b.append(i)
            sentenceBProcess(b, vQs, reg, number, symRead, nid)
    else:
        a.pop()
        sentenceBProcess(a,vQs,reg,number,symRead,nid)


#语句处理（从上一个分号（不含）到下一个分号）
#1：（定义）某（=某（右可以是常量表达式/输入函数））
#2：输出函数
#3.单独语句不处理
def sentenceBProcess(a,vQs,reg,number,symRead,nid):
    left=[]
    right=[]
    #在等号左还是右
    isleft=True
    #按照等号拆分为左右两个列表
    for i in a:
        if i==312:
            isleft=False
            continue
        if isleft:
            left.append(i)
        else:
            right.append(i)
    idL=equalLeft(left,vQs,reg,number, symRead,nid)
    valueR=[]
    # if idL!=-1:
    if len(right)!=0:
        func=False#是函数
        if right[0]==10:
            vQs.getNext()
            if vQs.matchName("getint"):
                valueR.append("%"+str(reg.getID()))
                print(valueR[0]+" = call i32 @getint()")
                func=True
            elif vQs.matchName("getch"):
                valueR.append( "%" + str(reg.getID()))
                print(valueR[0] + " = call i32 @getch()")
                func=True
            else:
                vQs.getLast()
        if func==False:
            valueR.append(runConstantExpression(right,number, symRead,reg,nid,vQs))
    if idL!=-1:#不是函数
        if len(right)!=0:
            #int类型已定义
            if vQs.getTypeForID(idL)==10 and vQs.getRegForID(idL)!=0:
                #store i32 % 2, i32 * % 1
                print("store i32 "+str(valueR[0])+", i32* %"+str(vQs.getRegForID(idL)))
            #const类型无值
            elif vQs.getTypeForID(idL)==20 and vQs.getNumForID(idL)=="":
                #!没有解决右边可能是变量的问题
                vQs.setNumForID(valueR[0],idL)



#返回vQs.getID()
def equalLeft(left,vQs,reg,number, symRead,nid):
    a=left[0]
    #int
    if a==11:
        if left[1]==10:
            vQs.getNext()
            if vQs.getReg()==0:
                b=reg.getID()
                vQs.setReg(b)
                vQs.setType(10)
                print("%"+str(b)+" = alloca i32")
                return vQs.getID()
            else:
                print("错误：变量重复定义！")
                exit(1)
        else:
            print("错误！")
            exit(1)
    #const
    elif a==14:
        #int
        if left[1]==11:
            if left[2]==10:
                vQs.getNext()
                if vQs.getType() == 0:
                    vQs.setType(20)
                    return vQs.getID()
                else:
                    exit(1)
            else:
                exit(1)
        else:
            exit(1)
    elif a==10:
        vQs.getNext()
        if vQs.matchName("putint"):
            i=2
            b=[]#函数参数
            while left[i]!=32:#不到右括号
                b.append(left[i])
                i+=1
            value=runConstantExpression(b,number, symRead,reg,nid,vQs)
            #call void @ putint(i32 % 4)
            print("call void @putint(i32 "+str(value)+")")
            return -1
        elif vQs.matchName("putch"):
            i = 2
            b = []  # 函数参数
            while left[i] != 32:  # 不到右括号
                b.append(left[i])
                i+=1
            value = runConstantExpression(b, number, symRead, reg, nid, vQs)
            # call void @ putint(i32 % 4)
            print("call void @putch(i32 " + str(value) + ")")
            return -1
        else:
            return vQs.getID()


def returnProcess(a, number, symRead, reg, nid, vQs):
    if a[0]==13:
        i=1
        b=[]
        while a[i]!=34:
            b.append(a[i])
            i+=1
        value = runConstantExpression(b, number, symRead, reg, nid, vQs)
        print("ret i32 " + str(value))