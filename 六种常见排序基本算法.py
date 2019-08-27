'''本例展示冒泡（段冒泡）、选择、插入、希尔、归并、快速六种排序算法比较'''
from datetime import datetime
from random import randint


def Run_time(func):
    def fn(*args, **kwargs):
        start = datetime.now()
        number = 100
        result = []
        for i in range(number):
            result = func(*args, **kwargs)
        end = datetime.now()
        span = end - start
        print('{}运行{}次耗时：{}'.format(func.__name__, number, span))
        # print('{}运行{}次耗时：{}，结果是：'.format(func.__name__, number, span))
        # print(result)
    return fn


@Run_time
def bubbleSort(alist):
    '''冒泡排序，升序'''
    blist = alist.copy()
    n = len(blist)
    for i in range(n-1):
        for j in range(n-i-1):
            if blist[j] > blist[j+1]:
                # Python里，交换两数不需要中间变量
                blist[j], blist[j+1] = blist[j+1], blist[j]
    return blist


@Run_time
def shortbubbleSort(alist):
    '''短冒泡排序'''
    blist = alist.copy()
    n = len(blist)
    for i in range(n-1):
        # 添加一个交换次数计数器
        change = 0
        for j in range(n-i-1):
            if blist[j] > blist[j+1]:
                blist[j], blist[j+1] = blist[j+1], blist[j]
                change += 1
        if change == 0:
            # 没有交换，说明排序完成，提前终止
            return blist


@Run_time
def selectionSort(alist):
    '''选择排序'''
    blist = alist.copy()
    n = len(blist)
    for i in range(n-1):
        # 每次遍历先找到最值位置，最后进行交换
        max_pos = 0
        for j in range(n-i):
            if blist[j] > blist[max_pos]:
                max_pos = j
        if max_pos != n-i-1:
            blist[max_pos], blist[n-i-1] = blist[n-i-1], blist[max_pos]
    return blist


@Run_time
def insertionSort(alist):
    '''插入排序'''
    blist = alist.copy()
    n = len(blist)
    for i in range(1, n):
        j = i-1
        cur_value = blist[i]
        while blist[j] > cur_value and j >= 0:
            blist[j+1] = blist[j]
            j = j - 1
        blist[j+1] = cur_value
    return blist


def insertionSort2(blist, head, h):
    '''改进插入排序，使其满足任意h有序数组'''
    n = len(blist)
    for i in range(head+h, n, h):
        j = i - h
        cur_value = blist[i]
        while blist[j] > cur_value and j >= head:
            blist[j+h] = blist[j]
            j = j - h
        blist[j+h] = cur_value


@Run_time
def shellSort(alist):
    '''希尔排序，递增序列取2^k-1'''
    blist = alist.copy()
    n = len(blist)
    # 求递增序列
    hlist = [2**i-1 for i in range(1,n) if 2**i-1<n]
    for h in hlist[::-1]:
        # 递减降低h
        for head in range(min(h,n-h)):
            # 理论上一个数组有h个独立的h有序数组，但是长仅为1的数组没有排序意义
            insertionSort2(blist, head, h)
    return blist


def handreverse(alist, i, j, index):
    '''给定手摇区间，原地交换、归并'''
    # 最简单的方法是利用Python的切片操作
    # alist[i:j] = (alist[i:index][::-1] + alist[index:j][::-1])[::-1]
    # 下面使用朴素方法：
    for l in range(i, (index+i)//2):
        # 左半部分翻转
        alist[l], alist[index-1+i-l] = alist[index-1+i-l], alist[l]
    for r in range(index, (index+j)//2):
        # 右半部分翻转
        alist[r], alist[j-1+index-r] = alist[j-1+index-r], alist[r]
    for k in range(i, (i+j)//2):
        # 整体翻转
        alist[k], alist[j-1+i-k] = alist[j-1+i-k], alist[k]
    # 还要保证i随着块体移动：
    i += j - index


def in_place_merge(alist, lo, mid, hi):
    '''使用手摇算法原地归并'''
    i, j = lo, mid+1
    if alist[mid] > alist[j]:
        # 如先判断数组是否有序，若是，可以节省一半长度比较数
        while j < hi+1:
            index = j
            while i < j and alist[i] <= alist[j]:
                i += 1
            if i >= j:
                break
            while j < hi+1 and alist[j] <= alist[i]:
                j += 1
            handreverse(alist, i, j, index)


@Run_time
def mergeSort(alist):
    '''归并排序'''
    blist = alist.copy()
    lo, hi = 0, len(blist)-1
    def sort(blist, lo, hi):
        '''分治法先对半分再原地合并'''
        if lo < hi:
            mid = (lo + hi - 1) // 2
            sort(blist, lo, mid)
            sort(blist, mid+1, hi)
            in_place_merge(blist, lo, mid, hi)
    sort(blist, lo, hi)
    return blist


def partition(alist, lo, hi):
    '''切分，并返回切分点位置'''
    i, j = lo+1, hi
    pivot = alist[lo]
    while True:
        while alist[i] <= pivot and i < hi:
            # 实验证明，对于大数组，最好要跳过重复项
            # 注意设置左右指针边界
            i += 1
        while alist[j] >= pivot and j > lo:
            j -= 1
        if i >= j:
            break
        alist[i], alist[j] = alist[j], alist[i]
    alist[lo], alist[j] = alist[j], alist[lo]
    return j


@Run_time
def quickSort(alist):
    '''快速排序'''
    blist = alist.copy()
    lo, hi = 0, len(blist) - 1
    def sort(blist, lo, hi):
        if hi > lo:
            split = partition(blist, lo, hi)
            sort(blist, lo, split-1)
            sort(blist, split+1, hi)
    sort(blist, lo, hi)
    return blist


if __name__ == '__main__':
    alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    for i in range(1991):
        alist.append(randint(1,100))
    print('长为{}的随机整数数组，六种方法的计算时间对比如下：'.format(len(alist)))
    bubbleSort(alist)
    shortbubbleSort(alist)
    selectionSort(alist)
    insertionSort(alist)
    shellSort(alist)
    mergeSort(alist)
    quickSort(alist)