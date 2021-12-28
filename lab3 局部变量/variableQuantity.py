# 变量
class variableQuantity:
    def __init__(self, nameInput):
        self.name = nameInput
        self.register=0#寄存器
        #self.load=0
        self.type=0#数据类型 10是int 20是const int
        self.numConst=""#仅供常量使用的数据存储

    def store(self, registerInput):
        self.register= registerInput

    def use(self):
        return self.register

    def define_(self,typeInput):
        self.type=typeInput

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def setNum(self,numInput):
        self.numConst+=numInput

    def getNum(self):
        return self.numConst


class variableQuantitys:
    def __init__(self):
        self.array=[]#存储所有变量
        self.order=[]#存储变量顺序
        self.id=-1

    def addNewVQ(self,nameInput):
        vQ=variableQuantity(nameInput)
        self.array.append(vQ)

    def findByName(self,nameInput):
        for i in range(len(self.array)):
            if self.array[i].name==nameInput:
                return i
        return -1

    def addNewQ(self,nameInput):
        a=self.findByName(nameInput)
        if a==-1:
            self.addNewVQ(nameInput)
            self.order.append(len(self.array)-1)
        else:
            self.order.append(a)

    def deleteLastQ(self):
        self.order.pop()

    def printQs(self):
        for i in self.order:
            print(self.array[i].name)

    # 下一个变量
    def getNext(self):
        self.id += 1

    # 上一个变量
    def getLast(self):
        self.id-=1

    #对于当前id处理寄存器和类型
    def setReg(self, r):
        a = self.order[self.id]
        #当前变量 self.array[a]
        self.array[a].store(r)

    def getReg(self):
        a = self.order[self.id]
        return self.array[a].use()

    def setType(self, t):
        a = self.order[self.id]
        self.array[a].define_(t)

    def getType(self):
        a = self.order[self.id]
        return self.array[a].getType()

    def matchName(self,nameInput):
        a = self.order[self.id]
        name=self.array[a].getName()
        if name == nameInput:
            return True
        else:
            return False

    #传出id
    def getID(self):
        return self.id

    #对于特定id处理寄存器等
    def setRegForID(self, r,id):
        a = self.order[id]
        # 当前变量 self.array[a]
        self.array[a].store(r)

    def getRegForID(self,id):
        a = self.order[id]
        return self.array[a].use()

    def setTypeForID(self, t,id):
        a = self.order[id]
        self.array[a].define_(t)

    def getTypeForID(self,id):
        a = self.order[id]
        return self.array[a].getType()

    def setNumForID(self,n,id):
        a = self.order[id]
        self.array[a].setNum(n)

    def getNumForID(self,id):
        a = self.order[id]
        return self.array[a].getNum()