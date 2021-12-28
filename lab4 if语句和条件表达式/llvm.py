#输出
class llvmBlock:
    def __init__(self,bidInput):
        self.blockID=bidInput
        self.print_=[]

    def getBID(self):
        return self.blockID

    def addPrint(self,prInput):
        self.print_.append(prInput)

    def printAll(self):
        if self.blockID==0:
            for i in self.print_:
                print("\t"+i)
        else:
            print(str(self.blockID)+":")
            for i in self.print_:
                print("\t"+i)


class llvm:
    def __init__(self):
        self.array=[]
        a=llvmBlock(0)
        self.array.append(a)

    #为bid为bidInput的块添加输出语句
    def addPrintByID(self,bidInput,prInput):
        haveID=False
        for i in self.array:
            if i.getBID()==bidInput:
                i.addPrint(prInput)
                haveID=True
        if not haveID:
            self.addBlock(bidInput)
            self.addPrintByID(bidInput,prInput)


    #添加一个bid为bidInput的块
    def addBlock(self,bidInput):
        a=llvmBlock(bidInput)
        self.array.append(a)

    def printAll(self):
        for i in self.array:
            i.printAll()