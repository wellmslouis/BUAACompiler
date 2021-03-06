import sys

from register import register,nid
from syntaxAnalysis import CompUnit
from constantExpression import runConstantExpression
from variableQuantity import variableQuantitys
from process import paragraphProcess
from llvm import llvm


if __name__ == '__main__':
    # 程序存在于这个字符串中
    # 标准读入
    procedure = ""
    for l in sys.stdin:
        procedure += l
    # 测试读入
    # with open("test/testB.txt", "r") as f:
    #     procedure = f.read()
    # print(procedure.replace("[]","\n"))
    number = []
    vQs=variableQuantitys()
    print_ = []
    # 类别码-读取字典
    symRead = {
        10:"Ident",
        11: "int",
        12: "main",
        13: "return",
        14:"const",
        20: "Number",
        31: "(",
        32: ")",
        33: "{",
        34: ";",
        35: "}",
        36: "+",
        37: "-",
        38: "*",
        39: "/",
        310: "%",
        311:",",
        312:"=",
        313:"!",
        40: "Error",
        50:"Notes",
        60: "Finish"
    }
    a=CompUnit(procedure, number, print_,vQs)
    # print(print_)
    # print(print_[len(print_)-1])
    # vQs.printQs()
    if not a:
        exit(1)

    reg = register()
    nid=nid()
    llvm=llvm()

    if vQs.selectName("getint"):
        print("declare i32 @getint()")
    if vQs.selectName("getch"):
        print("declare i32 @getch()")
    if vQs.selectName("putint"):
        print("declare void @putint(i32)")
    if vQs.selectName("putch"):
        print("declare void @putch(i32)")
    print("define dso_local i32 @main(){")
    # 去除main函数外层
    b=len(print_)-1
    print_A=print_[5:b]
    # print(print_A)
    paragraphProcess(print_A, vQs, reg, number, symRead, nid, llvm, 0)
    llvm.printAll()
    # try:
    #     paragraphProcess(print_A,vQs,reg,number,symRead,nid,llvm,0)
    #     llvm.printAll()
    # except:
    #     llvm.printAll()
    print("}")
