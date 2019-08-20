class Deque(object):
    def __init__(self):
        self.__list = []

    def add_front(self,item):
        """从队头加入一个item元素"""
        return self.__list.insert(0, item)

    def add_rear(self, item):
        """从队尾加入一个item元素"""
        return self.__list.append(item)

    def remove_front(self):
        """从队头删除一个item元素"""
        return self.__list.pop(0)

    def remove_rear(self):
        """从队尾删除一个item元素"""
        return self.__list.pop()

    def travel(self):
        print(self.__list)

    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)


def palchecker(ex_str):
    de = Deque()
    for i in ex_str:
        # 选择复杂度最小的一短传入
        de.add_rear(i)
    while de.size() > 0:
        if de.size() == 1:
            # 单字符当然回文
            return True
        fron = de.remove_front()
        rear = de.remove_rear()
        if fron != rear:
            return False

if __name__ == "__main__":
    # deque检验
    deque = Deque()
    deque.add_front(1)
    deque.add_front(2)
    deque.add_rear(3)
    deque.add_rear(4)
    deque.travel()
    print(deque.size())
    print(deque.remove_front())
    print(deque.remove_front())
    print(deque.remove_rear())
    print(deque.remove_rear())
    # 回文检查
    print(palchecker("lsdkjfskf"))
    print(palchecker("s"))
    print(palchecker("radar"))