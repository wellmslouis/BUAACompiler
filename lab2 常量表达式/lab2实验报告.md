# lab2实验报告

> 19231235 赵晰莹

[TOC]

## part分解

将不同part拆分为了不同文件；

### 词法分析

> lexicalAnalysis.py

相对于上一实验增加了返回一个单词的函数；`ungetSym()`

### 语法分析

> syntaxAnalysis.py

相对于上一实验重新写了语法分析部分；

对于不含或情况的语法规则采用多`if`嵌套判断；

```python
#示例
def FuncDef(p,n,pr):
    if FuncType(p, n, pr):
        if Ident(p,n,pr):
            if getSym(p,n)==31:
                pr.append(31)
                if getSym(p,n)==32:
                    pr.append(32)
                    if Block(p,n,pr):
                        return True
                else:
                    ungetSym()
            else:
                ungetSym()
    return False
```

对于含有或情况的语法规则使用`if-elif-...-else`判断；

```python
#示例
def PrimaryExp(p,n,pr):
    a=getSym(p,n)
    if a==31:
        pr.append(31)
        if Exp(p,n,pr):
            if getSym(p,n)==32:
                pr.append(32)
                return True
            else:
                ungetSym()
    elif a==20:
        pr.append(20)
        return True
    else:
        ungetSym()
    return False
```

对于特殊语句需要对提供的语法规则进行修改，消除左递归；

```python
#示例
#原规则为：AddExp     -> MulExp | AddExp ('+' | '−') MulExp
# AddExp -> MulExp AddExpA
def AddExp(p, n, pr, v):
    if MulExp(p, n, pr, v):
        if AddExpA(p, n, pr, v):
            return True
    return False
# AddExpA -> ('+' | '−') MulExp AddExpA
def AddExpA(p, n, pr, v):
    a = getSym(p, n, v)
    if a == 36 or a == 37:
        pr.append(a)
        if MulExp(p, n, pr, v):
            if AddExpA(p, n, pr, v):
                return True
    else:
        ungetSym(n, v)
        return True
    return False
```

### 常量表达式

> constantExpression.py

使用四个函数处理常量表达式；

| 函数名                         | 用途     |
| ------------------------------ | -------- |
| `translatConstantExpression()` | 输入处理 |
| `handleConstantExpression()`   | 核心代码 |
| `printConstantExpression()`    | 输出处理 |
| `runConstantExpression()`      | 封装运行 |

对于`handleConstantExpression()`核心工作包括：

1. 消除括号，即进入到第一个括号进行递归；
2. 如果没有括号，只有一项，直接返回寄存器名或数值；
3. 判断是否有乘除模，如果有，优先判断，如果无，优先判断第一句；
4. 按照如上条件，持续判断这一句；
5. 返回寄存器名或数值；

其中，对于寄存器使用全局变量`register`进行储存，使用时++；
