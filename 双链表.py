class Node(object):
    """双链表节点"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None
        self.prev = None


class DoubleLinkList(object):
    """双链表"""
    def __init__(self, p_node=None):
        """传入头节点P,默认为空"""
        self.__head = p_node

    def is_empty(self):
        """判断链表是否为空"""
        print(self.__head is None)

    def length(self):
        """求链表长度"""
        count = 0
        cursor = self.__head
        while cursor:
            count += 1
            cursor = cursor.next
        print(count)

    def travel(self):
        """遍历整个链表"""
        cursor = self.__head
        while cursor:
            print(cursor.elem, end=' ')
            cursor = cursor.next
        print(end='\n')

    def rev_travel(self):
        """基于双链表的反向通道，增加一个反向遍历方法"""
        cursor = self.__head
        # 移动cursor到末端
        while cursor.next:
            cursor = cursor.next
        while cursor:
            print(cursor.elem, end=' ')
            cursor = cursor.prev
        print(end='\n')

    def add(self, item):
        """链表头部添加元素"""
        new_node = Node(item)
        # 新节点向后指向原P点
        new_node.next = self.__head
        # 原P点向前指向新节点
        self.__head.prev = new_node
        # 头指针移动到新P点
        self.__head = new_node

    def append(self, item):
        """链表尾部添加元素"""
        new_node = Node(item)
        cursor = self.__head
        if self.__head is None:
            # 若是空链表，则将head指向新节点
            self.__head = new_node
        else:
            # 若非空，移动游标到尾部，并指向新节点
            while cursor.next:
                cursor = cursor.next
            cursor.next = new_node
            # 还要建立新节点与原尾节点的的回溯链接
            new_node.prev = cursor

    def insert(self, pos, item):
        """指定位置添加元素"""
        new_node = Node(item)
        cursor = self.__head
        if pos <= 0:
            self.add(item)
        elif self.__head is None:
            self.__head = new_node
        else:
            count = 0
            while cursor.next and count < pos:
                # 直到计数器游标到达List[pos]位置
                # 允许pos超过length情况发生
                count += 1
                cursor = cursor.next
            if cursor.next:
                # 此时pos未超过length
                # 前节点与新节点相连
                cursor.prev.next = new_node
                new_node.prev = cursor.prev
                # 后节点与新节点向量
                new_node.next = cursor
                cursor.prev = new_node
            else:
                # 此时pos超过length
                self.append(item)

    def remove(self, item):
        """删除节点(仅首个相同项)"""
        cursor = self.__head
        if cursor.elem == item:
            # 如果是首节点直接变更head的指向
            self.__head = cursor.next
            # 反向通道也要设置新的终点
            cursor.next.prev = None
        else:
            # 若非首节点则跳过待删除的节点
            while cursor:
                if cursor.elem == item:
                    cursor.prev.next = cursor.next
                    if cursor.next:
                        cursor.next.prev = cursor.prev
                    break
                cursor = cursor.next
        if cursor is None:
            # 如果最终没找到这个数，需要报错
            raise ValueError('There is no such item')

    def search(self, item):
        """查找节点是否存在"""
        cursor = self.__head
        while cursor:
            if cursor.elem == item:
                print(True)
                break
            cursor = cursor.next
        if cursor is None:
            print(False)


if __name__ == '__main__':
    L = DoubleLinkList()
    print('创建一个空链表，验证is_empty方法：')
    L.is_empty()
    print('添加节点,验证add/append/insert方法：')
    L.append(12)
    L.append(15)
    L.add(5)
    L.add(3)
    L.insert(2, 8)
    L.insert(2, 6)
    L.insert(8, 17)
    L.length()
    L.travel()
    L.rev_travel()
    print('查找节点是否存在，验证search方法：')
    L.search(7)
    L.search(5)
    print('删除节点,验证remove方法：')
    L.remove(17)
    L.remove(3)
    L.remove(12)
    L.length()
    L.travel()
    L.rev_travel()