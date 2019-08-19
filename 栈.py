class Stack(object):
    def __init__(self):
        self.__list = []

    def is_empty(self):
        print(self.__list == [])

    def push(self, item):
        """这里我们以列表尾部作为top端
        当然也可以采用add方法，以头部作为top端，
        但是对于Python的列表，add时间复杂度更高"""
        self.__list.append(item)

    def pop(self):
        """若push采用add方法，则pop对应采用pop(0)"""
        print(self.__list.pop())

    def peak(self):
        """返回栈顶元素,注意与pop区别在于不改变stack大小"""
        print(self.__list[len(self.__list) - 1])

    def size(self):
        print(len(self.__list))

    def travel(self):
        print(self.__list)


if __name__ == '__main__':
    s = Stack()
    s.is_empty()
    s.push(4)
    s.push('dog')
    s.peak()
    s.travel()
    s.push(True)
    s.size()
    s.is_empty()
    s.push(8.4)
    s.travel()
    s.pop()
    s.pop()
    s.travel()
    s.size()
