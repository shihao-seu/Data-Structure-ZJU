class Queue(object):
    def __init__(self):
        self.__list = []

    def enqueue(self, item):
        """往队列中添加一个item元素"""
        return self.__list.append(item)

    def dequeue(self):
        """从队列头部删除一个元素"""
        return self.__list.pop(0)

    def travel(self):
        print(self.__list)

    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)


def hotpotato(n, m):
    q = Queue()
    for i in range(1,n+1):
        # n个人依次进入队列
        q.enqueue(i)
    while q.size() > 1:
        # 直到决出最后一人
        for j in range(m-1):
            # 前m-1人重新进入队列尾部
            out = q.dequeue()
            q.enqueue(out)
        # 第m个人退出队列
        q.dequeue()
    # 返回胜者编号
    return q.dequeue()


if __name__ == '__main__':
    # 队列检验
    q = Queue()
    q.enqueue("hello")
    q.enqueue("world")
    q.enqueue("it!")
    q.travel()
    print(q.size())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    # 烫手山芋问题
    print(hotpotato(n=6, m=8))