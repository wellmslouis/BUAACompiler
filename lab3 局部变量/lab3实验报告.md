# lab3实验报告

> 19231235 赵晰莹

[TOC]

## part分解

### 词法分析

> lexicalAnalysis.py

相对于上一实验增加了退回多个单词的函数；`ungetTheSym()`

### 语法分析

> syntaxAnalysis.py

对于更加复杂的语法规则根据首字提前分析；

```python
#示例：提取前两个单词分析
# Stmt -> LVal(10) '=' Exp ';' | [Exp] ';' | 'return' Exp ';'
def Stmt(p, n, pr, v):
    a = getSym(p, n, v)
    b = getSym(p, n, v)
    if a == 13:
        pr.append(13)
        ungetSym(n, v)  # 把b退回去
        if Exp(p, n, pr, v):
            if getSym(p, n, v) == 34:
                pr.append(34)
                return True
    elif a == 10 and b == 312:
        pr.append(10)
        pr.append(312)
        if Exp(p, n, pr, v):
            if getSym(p, n, v) == 34:
                pr.append(34)
                return True
    else:
        ungetTheSym(2, n, v)
        while getSym(p, n, v) != 34:
            ungetSym(n, v)
            if Exp(p, n, pr, v):
                continue
            return False
        pr.append(34)
        return True
    return False
```

### 常量表达式

> constantExpression.py

相对于上一实验修改了翻译和封装函数，保证输入为常量表达式的数字列表；

翻译函数`translateConstantExpression()`对列表进行翻译，输出结果仅含数字、寄存器、括号与符号的列表；

封装函数`runConstantExpression()`中对只有一项元素的列表进行了特殊处理，其它情况正常运行；

### 寄存器

> register.py

#### 寄存器类

由于变量也需要用到寄存器，所以将寄存器写成了一个类`register`，方法包括跳转下一个（`getID(()`）和读取上一个（`readID()`）；

### 变量

> variableQuantity.py

将变量和所有变量写成了两个类；

#### 变量类

属性包括：

```python
class variableQuantity:
    def __init__(self, nameInput):
        self.name = nameInput#变量名
        self.register=0#寄存器
        self.type=0#数据类型 10是int 20是const int
        self.numConst=""#仅供常量使用的数据存储
```

#### 所有变量类

属性包括：

```python
class variableQuantitys:
    def __init__(self):
        self.array=[]#存储所有变量
        self.order=[]#存储变量顺序
        self.id=-1#指示读取变量位置
```

重要方法包括：

| 方法名      | 用途                 | 实现思路                                                     |
| ----------- | -------------------- | ------------------------------------------------------------ |
| `addNewQ()` | 词法分析时添加新变量 | 在`array`中遍历寻找所有同名变量，如果有，保存`array`中变量位置进`order`数组，否则创建变量，保存位置。 |
| `getNext()` | 读取下一个变量       | `id++`                                                       |

### 语义分析

> process.py

1. 段落分析`paragraphProcess()`

   1. 保留`main()`函数大括号内部分；
   2. 切分语句，每一分号跳转语句分析`sentenceAProcess()`；
   3. `return`语句跳转返回分析`returnProcess()`；

2. 语句分析`sentenceAProcess()`

   1. 如果含逗号则去除逗号，将类型赋予所有定义式，跳转下一语句分析`sentenceBProcess()`；
   2. 如果不含逗号则直接跳转下一语句分析；

3. 语句分析`sentenceBProcess()`

   1. 判断有无等号，切分至等号左右两个列表；

   2. 等号左列表跳转`equalLeft()`函数处理，返回变量位置；

      <u>不返回寄存器地址的原因是常量没有寄存器地址；</u>

   3. 如果存在等号右，且右边是函数，则按照函数返回，否则处理常量表达式，均得到寄存器地址或数字；

   4. 如果存在等号右，则分`int`和`const`两种类型将右式存入左式；

## 踩坑指南

![image-20211230232954328](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20211230232954328.png)

- **拒绝使用变量为常量赋值**

  在`constantExpression/runConstantExpression()`中，增加了对是否含有变量的判断，传回结果；

  在`process.py/equalLeft()`的定义中予以判断；

  

