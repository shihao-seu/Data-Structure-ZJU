class Stack(object):
    """创建栈"""

    def __init__(self):
        self.__list = []

    def is_empty(self):
        return self.__list == []

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        return self.__list.pop()

    def peak(self):
        return self.__list[len(self.__list) - 1]


class Queue(object):
    def __init__(self):
        self.__list = []

    def enqueue(self, item):
        """往队列中添加一个item元素"""
        return self.__list.append(item)

    def dequeue(self):
        """从队列头部删除一个元素"""
        return self.__list.pop(0)

    def is_empty(self):
        return self.__list == []


class BinTree:
    """二叉树类"""

    def __init__(self, rootobj=None):
        """创造新的树/根节点,默认为空"""
        self.key = rootobj
        self.leftchild = None
        self.rightchild = None

    def is_empty(self):
        '''空树与非挂载根节点意义不同'''
        return self is None

    def preorder_recur(self):
        """先序遍历，递归方法"""
        seq = ''
        seq += self.key
        if self.leftchild:
            seq += self.leftchild.preorder_recur()
        if self.rightchild:
            seq += self.rightchild.preorder_recur()
        return seq

    def inorder_recur(self):
        """中序遍历，递归方法"""
        seq = ''
        if self.leftchild:
            seq += self.leftchild.inorder_recur()
        seq += self.key
        if self.rightchild:
            seq += self.rightchild.inorder_recur()
        return seq

    def postorder_recur(self):
        """后序遍历，递归方法"""
        seq = ''
        if self.leftchild:
            seq += self.leftchild.postorder_recur()
        if self.rightchild:
            seq += self.rightchild.postorder_recur()
        seq += self.key
        return seq

    def preorder_stack(self):
        """先序遍历，栈方法"""
        s = Stack()
        BT = self
        seq = ''
        while BT or not s.is_empty():
            # 若左右节点均不存在，再次出栈
            # 栈空，循环必定截止
            while BT:
                # 向左压栈
                seq += BT.key
                s.push(BT)
                BT = BT.leftchild
            # 出栈，转向右边
            BT = s.pop().rightchild
        return seq

    def inorder_stack(self):
        """中序遍历，栈方法"""
        s = Stack()
        BT = self
        seq = ''
        while BT or not s.is_empty():
            while BT:
                s.push(BT)
                BT = BT.leftchild
            # 输出即将出栈元素
            seq += s.peak().key
            BT = s.pop().rightchild
        return seq

    def postorder_stack(self):
        """后序遍历，栈方法"""
        # 后序序列也是右左先序序列的逆排序
        s = Stack()
        BT = self
        seq = ''
        while BT or not s.is_empty():
            while BT:
                # 向右压栈
                seq += BT.key
                s.push(BT)
                BT = BT.rightchild
            # 出栈，转向左边
            BT = s.pop().leftchild
        return seq[::-1]

    def levelorder_queue(self):
        """层序遍历"""
        q = Queue()
        BT = self
        q.enqueue(BT)
        seq = ''
        while not q.is_empty():
            BT = q.dequeue()
            seq += BT.key
            if BT.leftchild:
                q.enqueue(BT.leftchild)
            if BT.rightchild:
                q.enqueue(BT.rightchild)
        return seq

    def levelorder2BT(self, levelstr):
        """读取层序列，创建树"""
        i = 0  # i是字符串的动态指针，需要扩大作用域
        n = len(levelstr)
        for i in range(n):
            # 首先确定根节点
            if levelstr[i] == ' ':
                continue
            else:
                self.key = levelstr[i]
                break
        q = Queue()
        BT = self
        q.enqueue(BT)
        while not q.is_empty():
            BT = q.dequeue()
            bothchild = []
            for j in range(i + 1, n):
                # 收集两个非空字符传给左右子树
                if len(bothchild) == 2:
                    i = j - 1
                    break
                elif levelstr[j] == ' ':
                    continue
                else:
                    bothchild.append(levelstr[j])
            # pdb.set_trace()
            if bothchild[0] != '0':
                BT.leftchild = BinTree(bothchild[0])
                q.enqueue(BT.leftchild)
            if bothchild[1] != '0':
                BT.rightchild = BinTree(bothchild[1])
                q.enqueue(BT.rightchild)

    def PrintLeaves(self):
        """输出所有叶节点"""
        seq = ''
        if not self.rightchild and not self.leftchild:
            seq += self.key
        if self.leftchild:
            seq += self.leftchild.PrintLeaves()
        if self.rightchild:
            seq += self.rightchild.PrintLeaves()
        return seq

    def getHeight(self):
        """返回树高"""
        if self.is_empty():
            return 0
        else:
            HL, HR = 0, 0
            if self.leftchild:
                HL = self.leftchild.getHeight()
            if self.rightchild:
                HR = self.rightchild.getHeight()
            return max(HL, HR) + 1


def infix2Bintree(s: str) -> BinTree:
    '''递归法，读取中缀表达式生成表达树'''
    if s.isalnum() or s.isalpha():
        return BinTree(s)
    rank = {'*': 2, '/': 2, '+': 1, '-': 1}
    count = 0  # 左括号+1右括号-1
    mid = 0
    rank_min = 100
    count_min = 100
    for i, c in enumerate(s):
        '''找到表达式根节点'''
        if c == ' ' or c.isalnum() or c.isalpha():
            # 跳过空格和数字
            continue
        elif c == '(':
            count += 1
        elif c == ')':
            count -= 1
        else:
            # 运算符判断
            if count < count_min:
                # 先找到括号最少点
                count_min = count
                rank_min = rank[c]
                mid = i
            elif count == count_min and rank[c] < rank_min:
                # 如果括号计数都最小，比较运算符等级
                rank_min = rank[c]
                mid = i
    BT = BinTree(s[mid])  # 创造二叉树、根节点挂载
    if count_min != 0:
        # 根节点圆括号标记非零，说明整个表达式被一对没用的符号包裹，可去除
        s = s[1:-1]
        mid -= 1
    BT.leftchild = infix2Bintree(s[:mid])
    BT.rightchild = infix2Bintree(s[mid + 1:])
    return BT


def evaluate(BT: BinTree) -> int:
    def doMath(op, num1, num2):
        if op == "+":
            return num1 + num2
        elif op == "-":
            return num1 - num2
        elif op == "*":
            return num1 * num2
        return num1 / num2

    if not BT.leftchild and not BT.rightchild:
        # 找到叶节点，必然是数字
        return int(BT.key)
    num1 = evaluate(BT.leftchild)
    num2 = evaluate(BT.rightchild)
    return doMath(BT.key, num1, num2)


if __name__ == '__main__':
    # 读取层序序列创建树，七种方法遍历
    t = BinTree()
    print(t.is_empty())  # 只要创建树就一定非空
    t.levelorder2BT('A BC DF GI 00 E0 0H 00 00 00')
    print('先序（递归法）：', t.preorder_recur())
    print('先序（栈方法）：', t.preorder_stack())
    print('中序（递归法）：', t.inorder_recur())
    print('中序（栈方法）：', t.inorder_stack())
    print('后序（递归法）：', t.postorder_recur())
    print('后序（栈方法）：', t.postorder_stack())
    print('层序序列：', t.levelorder_queue())
    print('输出所有叶节点：', t.PrintLeaves())
    print('输出树高：', t.getHeight())
    # 读取中缀表达式生成表达式树
    print(infix2Bintree('(A*(B+C)+D*E)/(F+G)+H').postorder_recur())
    print(evaluate(infix2Bintree('(12*(23+34)+45*56)/(67+78)+89')))