from datetime import datetime


def Run_time(func):
    '''装饰器，计算函数运行时间'''
    def run(*args,**kwargs):
        '''装饰器，并计算运行时间'''
        start_time = datetime.now()
        result = False
        for i in range(100000):
            result=func(*args,**kwargs)
        end_time = datetime.now()
        span= end_time - start_time
        print('{}的计算结果是：{}，运行时间:{}'.format(func.__name__,result,span))
    return run


@Run_time
def binarySearch1(alist, item):
    def binarySearch1_core(alist, item):
        '''递归法+二分查找'''
        n = len(alist)
        # 第一步：确定终止条件——切到长为1为止
        if n == 1:
            return alist[0] == item
        # 第二步：一分为二
        # 涉及切片操作，总步骤数为N
        mid = n//2
        left_list = alist[:mid]
        right_list = alist[mid:]
        # 第三步：依情况治理
        if item == alist[mid]:
            return True
        elif item > alist[mid//2]:
            return binarySearch1_core(right_list, item)
        else:
            return binarySearch1_core(left_list, item)
    return binarySearch1_core(alist, item)


@Run_time
def binarySearch2(alist, item):
    '''非递归方法，避免Python切片操作的影响'''
    n = len(alist)
    head = 0
    tail = n-1
    result = False
    while head <= tail and not result:
        mid = (head + tail)//2
        if item == alist[mid]:
            return True
        elif item > alist[mid]:
            head = mid + 1
        else:
            tail = mid - 1
    return result


if __name__ == '__main__':
    testlist=list(range(10000))
    binarySearch1(testlist, 3)
    binarySearch2(testlist, 3)
    binarySearch1(testlist, -25)
    binarySearch2(testlist, -25)
