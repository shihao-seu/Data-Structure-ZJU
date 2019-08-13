class Node(object):
    """链表节点"""
    def __init__(self, elem):
        """仅有一个元素作为参数"""
        self.elem = elem
        # 创建指针，我们在链表里串接节点，因此默认指向None
        self.next = None


class SingleLinkList(object):
    """单链表"""
    def __init__(self, p_node=None):
        """构造单链表时近传入头节点P,默认为空"""
        # 创建一个私有属性，头指针，始终指向头节点
        self.__head = p_node

    def is_empty(self):
        """链表是否为空"""
        # 仅需判断头指针是否指向None
        print(self.__head is None)

    def length(self):
        """链表长度"""
        # 创建一个计数器，每次路过一个节点+1
        count = 0
        # 创建一个动态指针，初始时指向头节点P
        cursor = self.__head
        while cursor:
            count += 1
            cursor = cursor.next
        print(count)

    def travel(self):
        """遍历整个链表"""
        # 与length类似，通过游标移动遍历节点
        cursor = self.__head
        while cursor:
            print(cursor.elem, end=' ')
            cursor = cursor.next
        print(end='\n')

    def add(self, item):
        """链表头部添加元素"""
        # 首先构造新的节点保存item
        new_node = Node(item)
        # 新节点指向原P点，头指针指向新节点
        new_node.next = self.__head
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
                # 之所以加上.next是为了避免cursor变为none
                cursor = cursor.next
            cursor.next = new_node

    def insert(self, pos, item):
        """指定位置添加元素"""
        new_node = Node(item)
        # 类似于length，要利用游标和计数器，但对计数器设限
        count = 0
        cursor = self.__head
        if self.__head is None:
            # 若为空链表，相当于add
            self.__head = new_node
        else:
            # 若非空，在指定位置创建过渡指针，用来承上启下
            while cursor.next and count < pos-1:
                # 直到计数器游标到达List[pos-1]位置
                # 允许pos超过length情况发生
                count += 1
                cursor = cursor.next
            last_node = cursor.next
            cursor.next = new_node
            new_node.next = last_node

    def remove(self, item):
        """删除节点(仅首个相同项)"""
        cursor = self.__head
        # 创建一个cursor的前一节点指针
        front_node = cursor
        if cursor.elem == item:
            # 如果是首节点直接变更head的指向
            self.__head=cursor.next
        else:
            # 若非首节点则让front直接跳过cursor
            while cursor:
                if cursor.elem == item:
                    front_node.next = cursor.next
                    break
                front_node = cursor
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
    L = SingleLinkList()
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
    L.search(7)
    L.search(5)
    print('删除节点,验证remove方法：')
    L.remove(17)
    L.remove(3)
    L.remove(12)
    L.length()
    L.travel()