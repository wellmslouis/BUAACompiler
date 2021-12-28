import sys

from register import register,nid
from syntaxAnalysis import CompUnit
from constantExpression import runConstantExpression
from variableQuantity import variableQuantitys
from process import paragraphProcess


if __name__ == '__main__':
    # 程序存在于这个字符串中
    # 标准读入
    procedure = ""
    for l in sys.stdin:
        procedure += l
    # 测试读入
    # with open("test/testA.txt", "r") as f:
    #     procedure = f.read()
    #print(procedure.replace("[]","\n"))
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
        40: "Error",
        50:"Notes",
        60: "Finish"
    }
    a=CompUnit(procedure, number, print_,vQs)
    #print(print_)
    #vQs.printQs()
    if not a:
        exit(1)

    reg = register()
    nid=nid()

    if vQs.selectName("getint"):
        print("declare i32 @getint()")
    if vQs.selectName("getch"):
        print("declare i32 @getch()")
    if vQs.selectName("putint"):
        print("declare void @putint(i32)")
    if vQs.selectName("putch"):
        print("declare void @putch(i32)")
    print("define dso_local i32 @main(){")
    paragraphProcess(print_,vQs,reg,number,symRead,nid)
    print("}")
