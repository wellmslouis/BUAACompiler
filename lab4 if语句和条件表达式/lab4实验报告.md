# lab4实验报告

> 19231235 赵晰莹

[TOC]

## part分解

### 未修改内容

> 词法分析	exicalAnalysis.py
>
> 语法分析	syntaxAnalysis.py
>
> 常量表达式	constantExpression.py
>
> 寄存器	register.py
>
> 变量	variableQuantity.py

### 修改或新增内容

#### 输出

> llvm.py

##### 块类

将输出中每一块存入该类



#### 语义分析

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

  

