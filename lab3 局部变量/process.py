#具体处理
from constantExpression import runConstantExpression
#段落处理
def paragraphProcess(pr):
    #去除最外层
    b = []
    a = False
    for i in range(len(pr)):
        if pr[i] == 33:
            a = True
            continue
        if pr[i] == 35:
            a = False
        if a:
            b.append(pr[i])
    #拆分为语句
    c=[]
    for i in b:
        c.append(i)
        if i==34:
            sentenceProcess(c)
            c.clear()


#语句处理（从上一个分号（不含）到下一个分号）
#1：（定义）某（=某（右可以是常量表达式/输入函数））
#2：输出函数
#3.单独语句不处理
def sentenceProcess(a,vQs,reg):
    left=[]
    right=[]
    #在等号左还是右
    isleft=True
    for i in a:
        if i==312:
            isleft=False
            continue
        if isleft:
            left.append(i)
        else:
            right.append(i)
    idL=equalLeft(left,vQs,reg)
    if len(right)!=0:
        func=True#是函数
        if right[0]==10:
            vQs.getNext()
            if vQs.matchName("getint"):

            elif vQs.matchName("getch"):

            else:
                vQs.getLast()
                func=False
        if not func:
            valueR=runConstantExpression(right,)

#返回vQs.getID()
def equalLeft(left,vQs,reg):
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
            #!待调用常量表达式
            return -1
        elif vQs.matchName("putch"):
            #!待调用常量表达式
            return -1
        else:
            return vQs.getID()