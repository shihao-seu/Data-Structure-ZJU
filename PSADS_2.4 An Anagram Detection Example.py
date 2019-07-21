from datetime import datetime
from copy import deepcopy
def Run_time(func):
    '''装饰器，计算函数运行时间'''
    def run(s1,s2):
        '''装饰器，并计算运行时间'''
        start_time = datetime.now()
        result=False
        for _ in range(10):
            # 由于程序运行过快，因此取n次运行时间总和
            s1_renew,s2_renew=map(deepcopy,(s1,s2))
            # 每次遍历，重新赋值(至少用到浅度拷贝)，保证每一步方程中的参数一致
            result=func(s1_renew,s2_renew)
        end_time = datetime.now()
        span=(end_time-start_time).microseconds
        print('{}的计算结果是：{}，运行时间:{} ms'.format(func.__name__,result,span))
    return run
@Run_time
def s_check(s1,s2):
    """遍历查找法，时间复杂度为1+2+...n=0.5n^2+0.5n,即为O(n2),Quadratic"""
    for i in s2:
        if i in s1:
            s1.remove(i)
        #  每一次遍历的最大复杂度为s1长度，而s1长度逐渐降低，从n降到1；
        else:
            return False
    return True
@Run_time
def s_sort(s1,s2):
    '''排序和遍历比较，时间复杂度为O(nlog(n))'''
    s1.sort()
    '''注意sort方法时间复杂度为O(nlog(n)),log linear'''
    s2.sort()
    for i in range(len(s1)):
        '''linear'''
        if s1[i]!=s2[i]:
            return False
    return True
@Run_time
def s_brute_force(s1,s2):
    '''将s1中所有字符打乱排序，暴力穷举所有可能，
    然后查看s2是否在其中。该法复杂度最大，为n!'''
    from itertools import product
    s1_pool = []
    for i in range(len(s1)):
        s1_pool.append(s1)
    source= list(product(*s1_pool))
    if tuple(s2) in source:
        return True
    else:
        return False
@Run_time
def s_count(s1,s2):
    '''统计字符串中各字符个数，复杂度为2n+261,linear'''
    c1 = [0]*26
    c2 = [0]*26
    for i in s1:
        '''linear'''
        pos=ord(i)-ord('a')
        # ord函数返回字符的ASCII码
        c1[pos]+=1
    for j in s2:
        '''linear'''
        pos=ord(j)-ord('a')
        c2[pos]+=1
    if c1==c2:
        '''复杂度为26'''
        return True
    else:
        return False
if __name__=='__main__':
    s1,s2=map(list,input().split())
    s_check(s1,s2)
    s_sort(s1,s2)
    s_brute_force(s1,s2)
    s_count(s1,s2)
