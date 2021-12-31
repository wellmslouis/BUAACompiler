#输出
class llvmBlock:
    def __init__(self,bidInput):
        self.blockID=bidInput
        self.print_=[]
        #三段判断
        self.brA=0
        self.brT=0
        self.brF=0
        #一段跳转
        self.brB=0

    def getBID(self):
        return self.blockID

    def addPrint(self,prInput):
        self.print_.append(prInput)

    def printAll(self):
        if self.blockID!=0:
            print(str(self.blockID)+":")
        for i in self.print_:
            print("\t"+i)
        if self.brA!=0:
            #br i1 %7,label %8, label %10
            print("\t"+"br i1 %"+str(self.brA)+",label %"+str(self.brT)+",label %"+str(self.brF))
        elif self.brB!=0:
            if len(self.print_)==0 or not self.print_[-1].startswith("ret"):
                valueA,valueB=self.formatBrB()
                if valueA==0:
                    print("\t"+"br label %"+str(self.brB))
                else:
                    return False,valueA,valueB
        return True,0,'A'

    def setBrA(self,brInput):
        self.brA=brInput

    def setBrT(self,brInput):
        self.brT=brInput

    def getBrT(self):
        return self.brT

    def setBrF(self,brInput):
        self.brF=brInput

    def getBrF(self):
        return self.brF

    def setBrB(self, brInput):
        self.brB = brInput

    def formatBrB(self):
        if str(self.brB).isdigit():
            return 0,'A'
        else:
            a=str(self.brB).split('!')
            return int(a[0]),a[1]

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
        for j in range(len(self.array) - 1, 0, -1):
            for i in range(j):
                if self.array[i].getBID()>self.array[i+1].getBID():
                    self.array[i],self.array[i+1]=self.array[i+1],self.array[i]
        for i in self.array:
            a,b,c=i.printAll()
            if not a:
                d=0
                for i in self.array:
                    if i.getBID()==b:
                        if c=="T":
                            d=i.getBrT()
                        else:
                            d=i.getBrF()
                        break
                print("\t" + "br label %" + str(d))

    def setBrA(self,bidInput,brInput):
        for i in self.array:
            if i.getBID()==bidInput:
                i.setBrA(brInput)

    def setBrT(self,bidInput,brInput):
        for i in self.array:
            if i.getBID()==bidInput:
                i.setBrT(brInput)

    def setBrF(self,bidInput,brInput):
        for i in self.array:
            if i.getBID()==bidInput:
                i.setBrF(brInput)

    def setBrB(self,bidInput,brInput):
        haveID = False
        for i in self.array:
            if i.getBID()==bidInput:
                i.setBrB(brInput)
                haveID = True
        if not haveID:
            self.addBlock(bidInput)
            self.setBrB(bidInput,brInput)