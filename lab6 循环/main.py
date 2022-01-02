import sys

from register import register,nid
from process import paragraphProcess, layerProcess, process
from llvm import llvm


if __name__ == '__main__':
    # 程序存在于这个字符串中
    # 标准读入
    # procedure = ""
    # for l in sys.stdin:
    #     procedure += l
    # 测试读入
    with open("test/testD.txt", "r") as f:
        procedure = f.read()
    # print(procedure.replace("[]","\n"))
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
    reg = register()
    nid=nid()
    llvm=llvm()

    number,print_,vQL=layerProcess(procedure)
    print(print_)
    # # vQL.print_()
    #
    # if vQL.selectName("getint"):
    #     print("declare i32 @getint()")
    # if vQL.selectName("getch"):
    #     print("declare i32 @getch()")
    # if vQL.selectName("putint"):
    #     print("declare void @putint(i32)")
    # if vQL.selectName("putch"):
    #     print("declare void @putch(i32)")
    # print("define dso_local i32 @main(){")
    # # 去除main函数外层
    # # b=len(print_)-1
    # # print_A=print_[5:b]
    # # print(print_A)
    # process(print_, vQL, reg, number, symRead, nid, llvm)
    # llvm.printAll()
    # # try:
    # #     paragraphProcess(print_A,vQs,reg,number,symRead,nid,llvm,0)
    # #     llvm.printAll()
    # # except:
    # #     llvm.printAll()
    # print("}")
