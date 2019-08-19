class Stack(object):
    '''创建栈'''
    def __init__(self):
        self.__list = []

    def is_empty(self):
        return self.__list == []

    def push(self, item):
        """这里我们以列表尾部作为top端
        当然也可以采用add方法，以头部作为top端，
        但是对于Python的列表，add时间复杂度更高"""
        self.__list.append(item)

    def pop(self):
        """若push采用add方法，则pop对应采用pop(0)"""
        return self.__list.pop()

    def peak(self):
        """返回栈顶元素,注意与pop区别在于不改变stack大小"""
        return self.__list[len(self.__list) - 1]

    def size(self):
        print(len(self.__list))

    def travel(self):
        print(self.__list)


def parChecker(ex_string):
    '''圆括号平衡'''
    s = Stack()
    count = 0
    # 遍历计数器
    while count < len(ex_string):
        par = ex_string[count]
        if par == '(':
            s.push(par)
        if par == ')':
            if s.is_empty():
                # 空栈不可以提前出现闭括号
                return False
            else:
                # 若栈非孔，则弹出最近开括号
                s.pop()
        count += 1
    if s.is_empty():
        # 遍历完毕，所有的括号应该全部闭合
        return True
    else:
        return False


def matcher(opens, close):
    # 检查开闭括号是否属于同一类型
    openers = "([{"
    closers = ")]}"
    return openers.index(opens) == closers.index(close)


def symbolChecker(ex_string):
    '''符号平衡'''
    s = Stack()
    count = 0
    while count < len(ex_string):
        symbol = ex_string[count]
        if symbol in '{([':
            s.push(symbol)
        if symbol in ')]}':
            if s.is_empty():
                # 空栈不可以提前出现闭括号
                return False
            else:
                # 若栈非孔，则弹出最近开括号
                opens = s.pop()
                # 且闭括号与最近开括号同类
                if not matcher(opens, symbol):
                    return False
        count += 1
    if s.is_empty():
        # 遍历完毕，所有的括号应该全部闭合
        return True
    else:
        return False


def baseConverter(decNumber,base):
    '''十进制数转换为其他进制数'''
    rems = Stack()
    while decNumber > 0:
        # 不断求余压栈
        rem = decNumber % base
        if rem in range(10,16):
            # 对于16进制数，要进行字符转换
            hex_str = 'ABCDE'
            hex_num = range(10,16)
            rem = hex_str[hex_num.index(rem)]
        rems.push(rem)
        decNumber = decNumber // base
    output = ''
    while not rems.is_empty():
        # 不断出栈并拼接成字符串
        output += str(rems.pop())
    return output


def infix2postfix(infix_expr):
    '''中缀表达式转后缀表达式'''
    # 为了比较运算符优先级，使用字典映射优先级大小
    operators = {'*':3,'/':3,'+':2,'-':2,'(':1}
    opstack = Stack()
    postfixList = []
    for i in infix_expr:
        if i in 'ABCDEFG':
            postfixList.append(i)
        elif i == ' ':
            continue
        elif i == '(':
            opstack.push(i)
        elif i == ')':
            out = opstack.pop()
            while out != '(':
                postfixList.append(out)
                out = opstack.pop()
        else:
            while (not opstack.is_empty()) and \
            operators[opstack.peak()] >= operators[i]:
                postfixList.append(opstack.pop())
            opstack.push(i)
    while not opstack.is_empty():
        postfixList.append(opstack.pop())
    return ''.join(postfixList)


def doMath(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2

def postfix2result(postfix_expr):
    '''计算后缀表达式结果'''
    operandStack = Stack()
    for i in postfix_expr:
        if i in "0123456789":
            operandStack.push(int(i))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = doMath(i,operand1,operand2)
            operandStack.push(result)
    return operandStack.pop()


if __name__=='__main__':
    '''
    # 栈检验
    s=Stack()
    print(s.is_empty())
    s.push(4)
    s.push('dog')
    print(s.peak())
    s.travel()
    s.push(True)
    s.size()
    print(s.is_empty())
    s.push(8.4)
    s.travel()
    print(s.pop())
    print(s.pop())
    s.travel()
    s.size()
    # 圆括号平衡检验
    print(parChecker('(3*(2+5)+4*(9-7))'))
    print(parChecker('  (2*6))+(5-6)'))
    print(parChecker('  ( (() ) '))
    # 符号平衡检验
    print(symbolChecker('{[(3+6)*2+3]+3*[2+(1-7)]}'))
    print(symbolChecker('{{([][])}()}'))
    print(symbolChecker('[{()]'))
    # 进制转化检验
    print(baseConverter(233, 2))
    print(baseConverter(233, 8))
    print(baseConverter(233, 16))
    '''
    # 中缀表达式转后缀表达式检验
    print(infix2postfix("A * B + C * D"))
    print(infix2postfix("( A + B ) * C - ( D - E ) * ( F + G )"))
    # 后缀表达式计算检验
    print(postfix2result('7 8 + 3 2 + /'))