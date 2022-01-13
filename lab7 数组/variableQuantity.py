# 变量
class variableQuantity:
    def __init__(self, nameInput):
        self.name = nameInput
        self.register = 0  # 寄存器
        self.type = 0  # 数据类型 10是int 20是const int 30是一维数组 31是二维数组
        self.numConst = ""  # 仅供常量使用的数据存储

    def store(self, registerInput):
        self.register = registerInput

    def use(self):
        return self.register

    def define_(self, typeInput):
        self.type = typeInput

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def setNum(self, numInput):
        self.numConst += numInput

    def getNum(self):
        return self.numConst

    def delete(self):
        self.register = 0  # 寄存器
        self.type = 0  # 数据类型 10是int 20是const int
        self.numConst = ""  # 仅供常量使用的数据存储


class variableQuantitys:
    def __init__(self):
        self.array = []  # 存储所有变量
        self.order = []  # 存储变量顺序
        self.id = -1

    def delete(self):
        for i in range(self.id+1):
            a = self.order[i]
            self.array[a].delete()

    def addNewVQ(self, nameInput):
        vQ = variableQuantity(nameInput)
        self.array.append(vQ)

    def findByName(self, nameInput):
        for i in range(len(self.array)):
            if self.array[i].name == nameInput:
                return i
        return -1

    def addNewQ(self, nameInput):
        a = self.findByName(nameInput)
        if a == -1:
            self.addNewVQ(nameInput)
            self.order.append(len(self.array) - 1)
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
        # test
        # print("get "+self.getName())

    # 上一个变量
    def getLast(self):
        self.id -= 1

    # 对于当前id处理寄存器和类型
    def setReg(self, r):
        a = self.order[self.id]
        # 当前变量 self.array[a]
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

    def getNum(self):
        a = self.order[self.id]
        return self.array[a].getNum()

    def getName(self):
        a = self.order[self.id]
        return self.array[a].getName()

    def matchName(self, nameInput):
        a = self.order[self.id]
        name = self.array[a].getName()
        if name == nameInput:
            return True
        else:
            return False

    # 传出id
    def getID(self):
        return self.id

    # 对于特定id处理寄存器等
    def setRegForID(self, r, id):
        a = self.order[id]
        # 当前变量 self.array[a]
        self.array[a].store(r)

    def getRegForID(self, id):
        a = self.order[id]
        return self.array[a].use()

    def setTypeForID(self, t, id):
        a = self.order[id]
        self.array[a].define_(t)

    def getTypeForID(self, id):
        a = self.order[id]
        return self.array[a].getType()

    def setNumForID(self, n, id):
        a = self.order[id]
        self.array[a].setNum(n)

    def getNumForID(self, id):
        a = self.order[id]
        return self.array[a].getNum()

    def getNameForID(self, id):
        a = self.order[id]
        return self.array[a].getName()

    # 查询变量
    def selectName(self, nameInput):
        for i in self.array:
            if i.getName() == nameInput:
                return True
        return False

    def locateName(self,nameInput):
        for i in range(len(self.array)):
            if self.array[i].getName() == nameInput:
                return i
        return -1

    def getTypeForLoc(self,locInput):
        return self.array[locInput].getType()

    def getRegForLoc(self,locInput):
        return self.array[locInput].use()

    def getNumForLoc(self,locInput):
        return self.array[locInput].getNum()

    def setNumForLoc(self,numInput,locInput):
        self.array[locInput].setNum(numInput)

class vQLayer:
    def __init__(self):
        self.array = []

    def add(self, nameInput, layerInput):
        # 添加层数
        a = len(self.array)
        while a < layerInput + 1:
            self.array.append(variableQuantitys())
            a = len(self.array)
        # 在该层数添加变量
        self.array[layerInput].addNewQ(nameInput)

    def print_(self):
        for i in range(len(self.array)):
            print(str(i) + ":")
            self.array[i].printQs()
    #清除同层前述变量
    def delete(self,layerInput):
        if layerInput>=len(self.array):
            return
        self.array[layerInput].delete()

    def selectName(self, nameInput):
        for i in self.array:
            if i.selectName(nameInput):
                return True
        return False

    def getNext(self, layerInput):
        self.array[layerInput].getNext()

    def getID(self, layerInput):
        return self.array[layerInput].getID()

    def getLast(self,layerInput):
        self.array[layerInput].getLast()

    def defInt(self,layerInput,regInput):
        if self.array[layerInput].getType()==0:
            self.array[layerInput].setReg(regInput)
            self.array[layerInput].setType(10)
            return self.getID(layerInput)
        return -1

    def defConst(self,layerInput):
        if self.array[layerInput].getType()==0:
            self.array[layerInput].setType(20)
            return self.getID(layerInput)
        return -1

    #赋值
    def assign(self,layerInput,IDLeftInput,numInput,isVInput):
        r={}
        #int 已定义
        if self.array[layerInput].getTypeForID(IDLeftInput)==10 and self.array[layerInput].getRegForID(IDLeftInput)!=0:
            r["type"]=1
            r["reg"]=self.array[layerInput].getRegForID(IDLeftInput)
            return r
        elif self.array[layerInput].getTypeForID(IDLeftInput)==20:#const
            if self.array[layerInput].getNumForID(IDLeftInput)=="":#未赋值
                if isVInput:
                    print("错误：使用变量为常量赋值！")
                    exit(1)
                else:
                    self.array[layerInput].setNumForID(numInput,IDLeftInput)
                r["type"]=2
                return r
            else:
                print("错误：常量已赋值！")
                exit(1)
        else:#当前层数找不到定义
            if layerInput==0:
                print("错误：未定义量！")
                exit(1)
            else:
                name=self.array[layerInput].getNameForID(IDLeftInput)
                return self.assignForLastLayer(layerInput-1,name,numInput,isVInput)

    def assignForLastLayer(self,layerInput,nameInput,numInput,isVInput):
        a=self.array[layerInput].locateName(nameInput)
        r={}
        if a!=-1:
            # int 已定义
            if self.array[layerInput].getTypeForLoc(a) == 10 and self.array[layerInput].getRegForLoc(a) != 0:
                r["type"] = 1
                r["reg"] = self.array[layerInput].getRegForLoc(a)
                return r
            elif self.array[layerInput].getTypeForLoc(a) == 20:  # const
                if self.array[layerInput].getNumForLoc(a) == "":  # 未赋值
                    if isVInput:
                        print("错误：使用变量为常量赋值！")
                        exit(1)
                    else:
                        self.array[layerInput].setNumForLoc(numInput, a)
                    r["type"] = 2
                    return r
                else:
                    print("错误：常量已赋值！")
                    exit(1)
            else:  # 当前层数找不到定义
                if layerInput == 0:
                    print("错误：未定义量！")
                    exit(1)
                else:
                    return self.assignForLastLayer(layerInput - 1, nameInput,numInput,isVInput)
        else:#没找到
            if layerInput==0:
                print("错误：未定义量！")
                exit(1)
            else:
                return self.assignForLastLayer(layerInput-1,nameInput,numInput,isVInput)


    def getValue(self,layerInput):
        r={}
        if self.array[layerInput].getType() == 10 and self.array[layerInput].getReg() != 0:
            r["type"]=1
            r["reg"]=self.array[layerInput].getReg()
            return r
        elif self.array[layerInput].getType() == 20:
            if self.array[layerInput].getNum()!="":
                r["type"]=2
                r["num"]=self.array[layerInput].getNum()
                return r
            else:
                print("错误：常量未赋值！")
                exit(1)
        else:
            if layerInput==0:
                print("错误：未定义量！")
                exit(1)
            else:
                name = self.array[layerInput].getName()
                return self.getValueForLastLayer(layerInput-1,name)

    def getValueForLastLayer(self,layerInput,nameInput):
        a = self.array[layerInput].locateName(nameInput)
        r = {}
        if a != -1:
            # int 已定义
            if self.array[layerInput].getTypeForLoc(a) == 10 and self.array[layerInput].getRegForLoc(a) != 0:
                r["type"] = 1
                r["reg"] = self.array[layerInput].getRegForLoc(a)
                return r
            elif self.array[layerInput].getTypeForLoc(a) == 20:  # const
                if self.array[layerInput].getNumForLoc(a) != "":  # 已赋值
                    r["type"] = 2
                    r["num"] = self.array[layerInput].getNumForLoc(a)
                    return r
                else:
                    print("错误：常量未赋值！")
                    exit(1)
            else:  # 当前层数找不到定义
                if layerInput == 0:
                    print("错误：未定义量！")
                    exit(1)
                else:
                    return self.getValueForLastLayer(layerInput - 1, nameInput)
        else:  # 没找到
            if layerInput == 0:
                print("错误：未定义量！")
                exit(1)
            else:
                return self.getValueForLastLayer(layerInput - 1, nameInput)



    def getType(self, layerInput):
        return self.array[layerInput].getType()

    def getReg(self, layerInput):
        return self.array[layerInput].getReg()

    def getNum(self, layerInput):
        return self.array[layerInput].getNum()

    def setType(self, typeInput, layerInput):
        self.array[layerInput].setType(typeInput)

    def setReg(self, regInput, layerInput):
        return self.array[layerInput].setReg(regInput)

    def matchName(self, nameInput, layerInput):
        return self.array[layerInput].matchName(nameInput)

    def getTypeForID(self, idInput, layerInput):
        return self.array[layerInput].getTypeForID(idInput)

    def getRegForID(self, idInput, layerInput):
        return self.array[layerInput].getRegForID(idInput)

    def getNumForID(self, idInput, layerInput):
        return self.array[layerInput].getNumForID(idInput)

    def setNumForID(self, idInput, layerInput):
        self.array[layerInput].setNumForID(idInput)


# 未经处理的变量们
class rawVQs:
    def __init__(self):
        self.array = []
        self.id = -1

    def addNewQ(self, a):
        self.array.append(a)

    def deleteLastQ(self):
        self.array.pop()

    def printQs(self):
        print(self.array)

    def getNext(self):
        self.id += 1

    def getName(self):
        return self.array[self.id]
