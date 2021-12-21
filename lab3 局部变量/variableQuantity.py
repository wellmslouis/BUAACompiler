# 变量
class variableQuantity:
    def __init__(self, nameInput):
        self.name = nameInput
        self.register=""#寄存器
        self.type=""#数据类型

    def store(self, registerInput):
        self.register += registerInput

    def use(self):
        return self.register


class variableQuantitys:
    def __init__(self):
        self.array=[]#存储所有变量
        self.order=[]#存储变量顺序

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