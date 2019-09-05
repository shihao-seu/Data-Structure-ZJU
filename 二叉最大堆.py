class BinMaxHeap:
    def __init__(self):
        # 堆的本质是在列表操作，第0项不保存元素为负
        self.heaplist = [-1]

    def swim(self, k):
        """上浮"""
        while self.heaplist[k] > self.heaplist[k//2] and k > 1:
            self.heaplist[k], self.heaplist[k//2] = self.heaplist[k//2], self.heaplist[k]
            k = k//2

    def sink(self, k):
        """下沉"""
        N = len(self.heaplist)-1
        if N == 2:
            # 特殊情况: 堆内只余下2个值
            if self.heaplist[1] < self.heaplist[2]:
                self.heaplist[1], self.heaplist[2] = self.heaplist[2], self.heaplist[1]
        else:
            while 2*k + 1 <= N and self.heaplist[k] < max(self.heaplist[2*k],self.heaplist[2*k+1]):
                j = 2*k if self.heaplist[2*k] >= self.heaplist[2*k+1] else 2*k+1
                self.heaplist[k], self.heaplist[j] = self.heaplist[j], self.heaplist[k]
                k = j

    def insert(self, key):
        """插入"""
        self.heaplist.append(key)
        self.swim(len(self.heaplist)-1)

    def delMax(self):
        """删除最大值"""
        N = len(self.heaplist) - 1
        if N <= 0:
            # 空堆报错
            raise IndexError('delete from empty heap')
        else:
            Max = self.heaplist[1]
            self.heaplist[1] = self.heaplist[N]
            self.heaplist.pop()
            if N > 2:
                self.sink(1)
            return Max

    def creatMaxHeap(self, alist):
        for i in alist:
            self.insert(i)

    def __str__(self):
        # 打印优先队列
        return str(self.heaplist[1:])


def sink(k, hl, END):
    # 需要一个终点参数
    while 2*k+1 <= END or 2*k == END:
        if 2*k == END:  # n1节点
            if hl[k] < hl[2 * k]:
                hl[k], hl[2 * k] = hl[2 * k], hl[k]
            break
        j = 2*k if hl[2*k] >= hl[2*k+1] else 2*k+1
        if hl[j] > hl[k]:
            hl[k], hl[j] = hl[j], hl[k]
        k = j


def Heapsort(alist):
    # 堆排序算法
    heaplist = [0] + alist
    N = len(alist)
    # 确定切分点
    if N % 2 ==0:
        i = N//2
    else:
        i = (N-1)//2
    while i > 0:
        sink(i, heaplist, END = N)
        i -= 1
    while N > 1:
        heaplist[1], heaplist[N] = heaplist[N], heaplist[1]
        sink(1, heaplist, END = N-1)
        # 切操作时浅层copy，因此原列表不会变！
        N -= 1
    return heaplist[1:]


if __name__ == '__main__':
    bmh = BinMaxHeap()
    bmh.creatMaxHeap([1,2,2,7,7,9,5,3])
    print(bmh)
    for i in range(8):
        print(bmh.delMax(),end=',')
    print(end='\n')
    print(bmh)
    # 堆排序算法检验
    print(Heapsort([1,2,2,7,7,9,5,3]))

