#寄存器
class register:
    def __init__(self):
        self.id=1

    def getID(self):
        a=self.id
        self.id+=1
        return a

    def readID(self):
        return self.id-1


#数字
class nid:
    def __init__(self):
        self.id=0

    def getID(self):
        a=self.id
        self.id+=1
        return a

    def readID(self):
        return self.id-1