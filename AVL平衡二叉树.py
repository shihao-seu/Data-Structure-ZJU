class Node:
    def __init__(self, key = None, val = None):
        self.key = key
        self.val = val
        self.leftchild = None
        self.rightchild = None
        # 树高直接和节点绑定
        self.height = 0

class AVLtree():
    def __init__(self):
        self.root = None

    def preorder_recur(self):
        def core(node):
            seq = ''
            seq += str(node.key)
            if node.leftchild:
                seq += core(node.leftchild)
            if node.rightchild:
                seq += core(node.rightchild)
            return seq
        if self.root is None:
            return None
        return core(self.root)

    def postorder_recur(self):
        def core(node):
            seq = ''
            if node.leftchild:
                seq += core(node.leftchild)
            if node.rightchild:
                seq += core(node.rightchild)
            seq += str(node.key)
            return seq
        if self.root is None:
            return None
        return core(self.root)

    def inorder_recur(self):
        def core(node):
            seq = ''
            if node.leftchild:
                seq += core(node.leftchild)
            seq += str(node.key)
            if node.rightchild:
                seq += core(node.rightchild)
            return seq
        if self.root is None:
            return None
        return core(self.root)

    def __setitem__(self, key, value):
        return self.newput(key,value)

    def __getitem__(self, key):
        return self.newget(key, self.root)

    def getH(self, node):
        # 注意与getHeight区别,这里树与节点已经分开
        # 为了能返回任意节点的高度，包括None
        if node is None:
            return 0
        return node.height

    def SingleLeftRotate(self, naught):
        # 左单旋
        New = naught.leftchild
        naught.leftchild = New.rightchild
        New.rightchild = naught
        # 由于子树根节点易位，需要更新树高
        naught.height = max(self.getH(naught.leftchild),
                            self.getH(naught.rightchild))+1
        New.height = max(self.getH(New.leftchild),
                         naught.height)+1
        return New

    def SingleRightRotate(self, naught):
        # 右单旋
        New = naught.rightchild
        naught.rightchild = New.leftchild
        New.leftchild = naught
        naught.height = max(self.getH(naught.leftchild),
                            self.getH(naught.rightchild))+1
        New.height = max(self.getH(New.rightchild),
                         naught.height) + 1
        return New

    def DoubleLeftRight(self, naught):
        # 左右双旋
        naught.leftchild = self.SingleRightRotate(naught.leftchild)
        return self.SingleLeftRotate(naught)

    def DoubleRightLeft(self, naught):
        # 右左双旋
        naught.rightchild = self.SingleLeftRotate(naught.rightchild)
        return self.SingleRightRotate(naught)

    def newput(self, key, val):
        """添加自平衡的插入方法"""
        if self.root is None:
            # 创建根节点
            self.root = Node(key, val)
            self.root.height = 1
        else:
            self.root = self.__put(key, val, self.root)
    
    def __put(self, key, val, node):
        """该方法的含义是：从给定根节点开始插入新节点，最终返回根节点
        在二叉搜索树里，给定初始节点就是最终根节点，而AVL树不一定"""
        if node.key == key:
            node.val = val
        elif node.key > key:
            if node.leftchild:
                node.leftchild = self.__put(key, val, node.leftchild)
                # 递归回来后，以node为根的树，其左右子树均已平衡
                if self.getH(node.leftchild)-self.getH(node.rightchild)==2:
                    # 判断node的BF是否平衡，是LL型还是LR型
                    # 此时的node就是最近不平衡点，记作naughty boy
                    if node.leftchild.key > key: # LL型
                        # 以node为根的子树左单旋重新排列，返回新的根节点
                        node = self.SingleLeftRotate(node)
                    else: # LR型
                        node = self.DoubleLeftRight(node)
            else:
                node.leftchild = Node(key,val)
                node.leftchild.height += 1
        elif node.key < key:
            if node.rightchild:
                node.rightchild = self.__put(key, val, node.rightchild)
                # 递归回来后，以node为根的树，其左右子树均已平衡
                if self.getH(node.leftchild) - self.getH(node.rightchild) == -2:
                    # 判断node的BF是否平衡，是RR型还是RL型
                    if node.rightchild.key < key:  # RR型
                        node = self.SingleRightRotate(node)
                    else:  # RL型
                        node = self.DoubleRightLeft(node)
            else:
                node.rightchild = Node(key, val)
                node.rightchild.height += 1
        node.height = max(self.getH(node.leftchild),self.getH(node.rightchild))+1
        return node

    def newget(self, key, node):
        if node is None:
            return None
        elif node.key == key:
            return node.val
        elif node.key > key:
            if node.leftchild:
                return self.newget(key,node.leftchild)
            else:
                return None
        elif node.key < key:
            if node.rightchild:
                return self.newget(key,node.rightchild)
            else:
                return None


if __name__ == '__main__':
    myAVL = AVLtree()
    myAVL[5] = "Jan"
    myAVL[4] = "Feb"
    myAVL[8] = "Mar"
    myAVL[1] = "Apr"
    myAVL[9] = "May"
    myAVL[7] = "Jun"
    myAVL[6] = "Jul"
    myAVL[2] = "Aug"
    myAVL[12] = "Sep"
    myAVL[11] = "Oct"
    myAVL[10] = "Nov"
    myAVL[3] = "Dec"
    print('先序：', myAVL.preorder_recur())
    print('后序：', myAVL.postorder_recur())
    print('中序：', myAVL.inorder_recur())
    myAVL[3] = "ced"
    myAVL[12] = "pes"
    myAVL[11] = "tco"
    myAVL[10] = "von"
    print(myAVL[3])
    print(myAVL[12])
    print(myAVL[11])
    print(myAVL[10])
    print(myAVL.getH(myAVL.root))