import sys
from syntaxAnalysis import CompUnit
from constantExpression import runConstantExpression
from variableQuantity import variableQuantitys


if __name__ == '__main__':
    # 程序存在于这个字符串中
    # 标准读入
    # procedure = ""
    # for l in sys.stdin:
    #     procedure += l
    # 测试读入
    with open("test/testF.txt", "r") as f:
        procedure = f.read()
    #print(procedure.replace("[]","\n"))
    number = []
    nid=0
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
    print(print_)
    vQs.printQs()
    if not a:
        exit(1)

    # if CompUnit(procedure, number, print_):
    #     # print(print_)
    #     print("define dso_local i32 @main() {")
    #     constantExpression = []
    #     a = False
    #     for i in range(len(print_)):
    #         if print_[i] == 13:
    #             a = True
    #             continue
    #         if print_[i] == 34:
    #             a = False
    #         if a:
    #             constantExpression.append(print_[i])
    #     runConstantExpression(constantExpression, number, symRead)
    # else:
    #     exit(1)
