from timeit import Timer


def rec_numCoins1(coinList,change):
    '''递归法一，多次冗余重复调用，浪费时间'''
    if change in coinList:
        # 注意终止条件不是change到0为止
        return 1
    num = []
    for i in [c for c in coinList if c <= change]:
        # 列表生成式——杜绝change<0的情况
        num.append(1+rec_numCoins1(coinList, change-i))
    return min(num)


def rec_numCoins2(coinList,change,cache):
    '''算法一改进型，添加了一个“缓存"列表，存储各change下的num'''
    if change in coinList:
        cache[change]=1 # 缓存内添加最基本情况
        return 1
    elif cache[change]:
        # 非零说明某change项已算出，直接返回该项结果即可
        return cache[change]
    num = []
    for i in [c for c in coinList if c <= change]:
        num.append(1+rec_numCoins2(coinList, change-i, cache))
    cache[change] = min(num)  # 新鲜算出的change项立刻放入cache之中
    return cache[change]


def DP_numCoins1(coinList,change):
    ''' DP算法，关键是找到’状态转移方程‘ '''
    known=[0]*(change+1)
    for i in range(1,change+1):
        # 从1分钱到输入值全体遍历，一步遍历得到一个结果
        num = []
        for j in [c for c in coinList if c <= i]:
            # 只需关注锚节点即可
            num.append(1+known[i-j])
        known[i] = min(num)
    return known[change]


class CoinsDict(object):
    def __init__(self, coin_List=None, new_dict = None):
        '''读取货币种类构造空字典，或者读取一个字典（为了方便后续的add方法）'''
        if coin_List:
            self.coindict = dict()
            for i in coin_List:
                self.coindict[i] = 0
        if new_dict:
            self.coindict = new_dict

    def __add__(self, other):
        '''加法重载'''
        add_dict = dict()
        for i in self.coindict:
            add_dict[i] = self.coindict[i]+other.coindict[i]
        # 为了返回一个同类对象，特意增加一个由字典构造类的方法
        return CoinsDict(new_dict=add_dict)

    def __getitem__(self, idx):
        '''重载索引'''
        return self.coindict[idx]

    def __setitem__(self, key, value):
        '''重载键值设置'''
        self.coindict[key] = value

    def __str__(self):
        '''打印自定义字典'''
        return '%s'%(self.coindict)


def DP_numCoins2(coinList,change):
    '''改进DP算法，增加硬币方案输出'''
    known = [0] * (change + 1)
    solution = [CoinsDict(coinList)]* (change + 1)
    for i in range(1,change+1):
        min = i
        for j in [c for c in coinList if c <= i]:
            if 1+known[i-j] <= min:
                min = 1+known[i-j]
                if i == j:
                    # 对于锚节点，先重置为空，再在对应位置加上一枚硬币
                    solution[i] = CoinsDict(coinList)
                    solution[i][j] = 1
                else:
                    solution[i] = solution[j] + solution[i-j]
        known[i] = min
    print(solution[change])
    return known[change]



if __name__ == '__main__':
    t1 = Timer("rec_numCoins1([1, 5, 10, 25],63)", "from __main__ import rec_numCoins1")
    print("运行结果：{}, 运行时间：{:.4f}".format(rec_numCoins1([1, 5, 10, 25], 63), t1.timeit(number=1) * 1), "s")
    t2 = Timer("rec_numCoins2([1, 5, 10, 25],63,cache=[0]*64)", "from __main__ import rec_numCoins2")
    print("运行结果：{}, 运行时间：{:.4f}".format(rec_numCoins2([1, 5, 10, 25], 63, cache=[0]*64), t2.timeit(number=1) * 1000), "ms")
    t3 = Timer("DP_numCoins1([1, 5, 10, 25],63)", "from __main__ import DP_numCoins1")
    print("运行结果：{}, 运行时间：{:.4f}".format(DP_numCoins1([1, 5, 10, 25], 63), t3.timeit(number=1) * 1000), "ms")
    print(DP_numCoins2([1,5,10,21,25],63))