class Node(object):
    """单链表节点"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class SinCycLinkList(object):
    """单向循环链表"""
    def __init__(self, p_node=None):
        self.__head = p_node
        # 注意若p_node存在，还需要指向自己：
        if p_node:
            p_node.next = p_node

    def is_empty(self):
        print(self.__head is None)

    def length(self):
        """链表长度"""
        count = 0
        cursor = self.__head
        if cursor:
            # 至少有一个节点存在
            count = 1
            while cursor.next != self.__head:
                count += 1
                cursor = cursor.next
        print(count)

    def travel(self):
        """遍历整个链表"""
        cursor = self.__head
        if cursor:
            print(cursor.elem, end=' ')
            while cursor.next != self.__head:
                cursor = cursor.next
                print(cursor.elem, end=' ')
        print(end='\n')

    def add(self, item):
        """链表头部添加元素"""
        new_node = Node(item)
        cursor = self.__head
        new_node.next = self.__head
        if cursor:
            # 非空链表，要在尾部建立链接
            while cursor.next != self.__head:
                cursor = cursor.next
            cursor.next = new_node
            self.__head = new_node
        else:
            self.__head = new_node
            new_node.next = self.__head

    def append(self, item):
        """链表尾部添加元素"""
        new_node = Node(item)
        cursor = self.__head
        if cursor:
            # 若非空，移动游标到尾部
            while cursor.next != self.__head:
                cursor = cursor.next
            cursor.next = new_node
            new_node.next = self.__head
        else:
            # 若是空链表，相当于add
            self.__head = new_node
            new_node.next = self.__head

    def insert(self, pos, item):
        """指定位置添加元素"""
        new_node = Node(item)
        count = 0
        cursor = self.__head
        if cursor:
            while cursor.next != self.__head and count < pos - 1:
                # 直到计数器游标到达List[pos-1]位置
                # 允许pos超过length情况发生
                count += 1
                cursor = cursor.next
            last_node = cursor.next
            cursor.next = new_node
            new_node.next = last_node
        else:
            self.__head = new_node
            new_node.next = self.__head

    def remove(self, item):
        """删除节点(仅首个相同项)"""
        cursor = self.__head
        if cursor:
            if cursor.elem == item:
                # 如果是首节点首先变更head的指向
                # 并改变尾节点的链接
                while cursor.next != self.__head:
                    cursor = cursor.next
                self.__head = self.__head.next
                cursor.next = self.__head
            else:
                # 若非首节点则让front直接跳过cursor
                while cursor.next != self.__head:
                    front_node = cursor
                    cursor = cursor.next
                    if cursor.elem == item:
                        front_node.next = cursor.next
                        break
                if cursor.next == self.__head and cursor.elem != item:
                    raise ValueError('There is no such item')
        else:
            raise ValueError('There is no such item')

    def search(self, item):
        """查找节点是否存在"""
        # return语句可以减少循环情况，建议看看示例代码
        cursor = self.__head
        if cursor:
            if cursor.elem == item:
                print(True)
            else:
                while cursor.next != self.__head:
                    cursor = cursor.next
                    if cursor.elem == item:
                        print(True)
                        break
                if cursor.next == self.__head and cursor.elem != item:
                    print(False)
        else:
            print(False)


if __name__ == '__main__':
    L = SinCycLinkList()
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
    print('查找节点是否存在，验证search方法：')
    L.search(3)
    L.search(17)
    L.search(7)
    L.search(5)
    print('删除节点,验证remove方法：')
    L.remove(17)
    L.remove(3)
    L.remove(12)
    L.length()
    L.travel()