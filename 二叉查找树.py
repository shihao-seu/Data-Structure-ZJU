from 二叉树的创建和遍历 import *


class BinSearchTree(BinTree):
    """从二叉树中继承衍生二叉搜索树"""
    def __init__(self, key = None, val = None):
        super().__init__(key)
        self.val = val

    def put(self, key, val):
        """插入键值对，或替换值"""
        if self.key is None:
            # 根节点未挂载
            self.key = key
            self.val = val
        elif self.key == key:
            # 重复键替换值
            self.val = val
        elif self.key > key: # 进入左子树
            if self.leftchild:
                self.leftchild.put(key, val)
            else:
                # 若左子树不存在，创建左子树
                self.leftchild = BinSearchTree(key, val)
        elif self.key < key: # 进入右子树
            if self.rightchild:
                self.rightchild.put(key, val)
            else:
                self.rightchild = BinSearchTree(key, val)

    def get_rec(self, key):
        """递归法搜索"""
        if self.key is None:
            return None
        elif self.key == key:
            return self.val
        elif self.key > key:
            if self.leftchild:
                return self.leftchild.get_rec(key)
            else:
                return None
        elif self.key < key:
            if self.rightchild:
                return self.rightchild.get_rec(key)
            else:
                return None

    def get_iter(self, key):
        """迭代法搜索"""
        BST = self
        while(BST):
            if BST.key == key:
                return BST.val
            elif BST.key > key:
                BST = BST.leftchild
            else:
                BST = BST.rightchild
        return None

    def getMin(self):
        """找到最左叶节点"""
        if self.leftchild is None:
            return self.key
        return self.leftchild.getMin()

    def getminNode(self):
        """寻找子树最小节点,返回节点而非键值"""
        if self.leftchild is None:
            return self
        return self.leftchild.getminNode()

    def getMax(self):
        """找到最右节点"""
        if self.rightchild is None:
            return self.key
        return self.rightchild.getMax()

    def delete(self, key, prev = None, l=0, r=0):
        """删除节点。为了转换父子关系，我们需要关注父节点，
        为此创建一个备忘录prev保存当前节点，即下一步的父节点
        我们还需要知道父子节点的左右关系，因此再设两个变量l和r标记"""
        # 先锁定待删节点
        if self.key > key:
            if self.leftchild:
                prev = self
                l, r = 1, 0 #进入左子树，l打开，r关闭
                self.leftchild.delete(key, prev, l, r)
            else:
                print('There is no such key:', key)
        elif self.key < key:
            if self.rightchild:
                prev = self
                r, l = 1, 0 #进入右子树，l关闭，r打开
                self.rightchild.delete(key, prev, l, r)
            else:
                print('There is no such key', key)
        elif self.key == key:
            # 定位后分情况处理
            if not self.leftchild and not self.rightchild:
                # 情况一，直接删除节点即可
                if prev is None:
                    # 根节点本身是叶节点
                    self.key = None
                    self.val = None
                else:
                    if l:
                        prev.leftchild = None
                    else:
                        prev.rightchild = None
            elif self.leftchild and not self.rightchild:
                # 情况二之只有左孩子
                if prev is None:
                    # 为根节点
                    self.key = self.leftchild.key
                    self.val = self.leftchild.val
                    self.leftchild = self.leftchild.leftchild
                    self.rightchild = self.leftchild.rightchild
                else:
                    if l:
                        prev.leftchild = self.leftchild
                    else:
                        prev.rightchild = self.leftchild
            elif self.rightchild and not self.leftchild:
                # 情况二之只有右孩子
                if prev is None:
                    # 为根节点
                    self.key = self.rightchild.key
                    self.val = self.rightchild.val
                    self.leftchild = self.rightchild.leftchild
                    self.rightchild = self.rightchild.rightchild
                else:
                    if l:
                        prev.leftchild = self.rightchild
                    else:
                        prev.rightchild = self.rightchild
            elif self.leftchild and self.rightchild:
                # 情况三，左右孩子均存在，采用右子树取最小元素为替换节点
                replace = self.rightchild.getminNode()
                # 按情况一或二删除替换节点
                self.delete(replace.key)
                # 替换节点的键值对传给删除节点
                self.key, self.val = replace.key, replace.val

    def __setitem__(self, key, val):
        return self.put(key, val)

    def __getitem__(self, key):
        return self.get_rec(key)

    def __contains__(self, key):
        """重载in运算符"""
        if self.get_rec(key) is not None:
            return True
        else:
            return False

    def __delitem__(self, key):
        """重载del运算符"""
        return self.delete(key)

    def keys(self):
        # 栈方法,迭代输出先序序列,键
        s = []
        BT =self
        while BT or len(s) != 0:
            while BT:
                yield BT.key
                s.append(BT)
                BT = BT.leftchild
            BT = s.pop().rightchild

    def values(self):
        # 栈方法,迭代输出中序序列，值
        s = []
        BT =self
        while BT or len(s) != 0:
            while BT:
                s.append(BT)
                BT = BT.leftchild
            yield s[-1].key
            BT = s.pop().rightchild

    def items(self):
        #  递推法，迭代输出先序序列，键值
        if self:
            yield self.key, self.val
            if self.leftchild:
                for item in self.leftchild:
                    yield item
            if self.rightchild:
                for item in self.rightchild:
                    yield item

    def __iter__(self):
        # 重载for in mytree运算
        return self.items()


if __name__ == '__main__':
    mytree = BinSearchTree()
    mytree[5] = "Jan"
    mytree[4] = "Feb"
    mytree[8] = "Mar"
    mytree[1] = "Apr"
    mytree[9] = "May"
    mytree[7] = "Jun"
    mytree[6] = "Jul"
    mytree[2] = "Aug"
    mytree[12] = "Sep"
    mytree[11] = "Oct"
    mytree[10] = "Nov"
    mytree[3] = "Dec"
    # 检验迭代器
    for i in mytree.keys():
        print(i,end=',')
    print(end='\n')
    for i in mytree.values():
        print(i, end=',')
    print(end='\n')
    for i in mytree.items():
        print(i, end='')
    print(end='\n')
    for i in mytree:
        print(i,end='')
    print(end='\n')
    # 检验put和get
    print(mytree.preorder_recur())
    print(mytree[6], mytree.get_iter(6))
    print(mytree[2], mytree.get_iter(2))
    # 检验最值查询
    print(mytree.getMax(),mytree.getMin())
    # 检验put和get
    mytree[2] = 'shihao'
    print(mytree[2], mytree.get_iter(2))
    # 检验in操作
    print(13 in mytree, 5 in mytree)
    # 检验删除操作
    for i in [8, 1, 5, 12 ,10, 9]:
        del mytree[i]
    print(mytree.preorder_recur())