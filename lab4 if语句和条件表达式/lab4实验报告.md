# lab4实验报告

> 19231235 赵晰莹

[TOC]

## part分解

### 未修改part

> 词法分析	exicalAnalysis.py
>
> 语法分析	syntaxAnalysis.py
>
> 常量表达式	constantExpression.py
>
> 寄存器	register.py
>
> 变量	variableQuantity.py

### 修改或新增part

#### 输出

> llvm.py

##### 块类

将输出中每一块存入该类，以达到非顺序输出的效果；

属性包括：

```python
class llvmBlock:
    def __init__(self,bidInput):
        self.blockID=bidInput#块ID
        self.print_=[]#输出语句
        #三段判断
        self.brA=0
        self.brT=0
        self.brF=0
        #一段跳转
        self.brB=0
```

在输出时首先输出`blockID:`，而后输出`print_`全部语句，最后如果`brA!=0`，输出三段判断跳转，否则跳转到`brB`；

#### 语义分析

> process.py

`if`表达式分析

```python
#从if（含）起，读到最后（不含下一个），返回i
def conditionAProcess(pr, index, vQs, reg, number, symRead, nid,llvm,bid)
```

1. 截取两部分，为括号内的条件表达式和后面的执行语句；
2. 条件表达式利用相关函数进行处理（详见下）；
3. 执行语句分为三种情况：
   1. 被大括号包裹的基本块，截取该部分跳转至段落处理；
   2. if语句，递归执行；
   3. 单条语句，调用语句处理函数执行；
4. 如果后面存在`else`，则同上执行语句分析（`else if`相当于else与下属的`if`）；
5. 需要额外注意的是`bid`，也即块ID；在条件表达式判断结束后会返回当前`bid`，在`if`的执行语句判断前更新为`bidTrue`，在else前执行语句判断更新为`bidFalse`（不先设定两个`bid`的原因是，使用llvm数字寄存器是要求连续的）；

#### 条件表达式

> conditionExpression.py

| 函数名            | 作用                         | 执行方法                                                     |
| ----------------- | ---------------------------- | ------------------------------------------------------------ |
| `conditionA`      | 单条语句执行（不存在或、且） | 左和如果存在的右分别进行常量表达式分析，而后进行比较，返回当前`bid`； |
| `conditionOr`     | 或语句                       | 左真一定真，返回结果，否则继续执行；                         |
| `conditionAnd`    | 且语句                       | 返回正确的`bid`；                                            |
| `handleCondition` | 封装条件表达式执行           | 先按照或、且分割语句，分别调用`conditionA`从左至右判断语句真假，再对结果调用或、且语句判断； |



## 踩坑指南

- **或与且**

  以A||B为例，最开始理解的或是A->T指向B->T，A->F指向B，这样写有一个问题，就是假如A||B&&C，A真C假时不成立，后来理解到A->T应当指向结果的T；

  但是且不能前面假直接指向假，例如A&&B||C，如果A假C真也是真的；

- **bid**

  最开始没有注意到数字寄存器的序号要求连续，后来将提前申请寄存器改成了传原来的值，用到时再申请。

  

  

