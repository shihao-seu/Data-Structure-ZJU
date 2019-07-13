from datetime import datetime
def Run_time(func):
    '''装饰器，计算函数运行时间'''
    def run(*args,**kwargs):
        '''装饰器，并计算运行时间'''
        start_time = datetime.now()
        result=func(*args,**kwargs)
        end_time = datetime.now()
        span=(end_time-start_time).microseconds
        print('{}的计算结果是：{}，运行时间:{} ms'.format(func.__name__,result,span))
    return run
@Run_time
def Max_SubSeq_sum_1(Seq):
    '''总复杂度为三处复杂度的积，即O(n3)'''
    N=len(Seq)
    Max_sum=0
    for i in range(N):
        # 子列头部逐项前移，复杂度O(N)
        for j in range(i,N):
        # 子项尾部逐项前移，至少领先头部,复杂度O(N)
            This_sum=sum(Seq[i:j+1])
            # 计算子列和，复杂度O(N)
            if This_sum>Max_sum:
                # 对比已知最大和,复杂度忽略不计
                Max_sum=This_sum
    return Max_sum
@Run_time
def Max_SubSeq_sum_2(Seq):
    '''在算法1上进行改进，即O(n2)'''
    N=len(Seq)
    Max_sum=0
    for i in range(N):
        This_sum = 0
        for j in range(i,N):
            This_sum+=Seq[j]
            if This_sum>Max_sum:
                Max_sum=This_sum
    return Max_sum
@Run_time
def Max_SubSeq_sum_3(Seq):
    '''分治法，算法复杂度为O(nlog(n))'''
    N = len(Seq)
    def Divide_and_Conquer(Left,Right):
        if Right-Left==1:
            # 递归的终止条件,即切到只剩1个或2个元素
            return max(Seq[Right],Seq[Left],Seq[Right]+Seq[Left])
        if Right-Left==0:
            return Seq[Right]
        Center=(Right+Left)//2
        '''二分法递归求左右两边最大值'''
        Max_Left_sum=Divide_and_Conquer(Left,Center)
        #把中间数留给左边
        Max_Right_sum=Divide_and_Conquer(Center+1,Right)
        """下面从中间点向左右两边扫描最大值"""
        Left_border,Right_border =0,0
        Max_Left_border,Max_Right_border=0,0
        for i in range(Center,Left-1,-1):
            # 注意range函数步长与初始步无关,且终止步不含自身
            Left_border += Seq[i]
            if Left_border>Max_Left_border:
                Max_Left_border=Left_border
        for j in range(Center+1,Right+1,1):
            Right_border+= Seq[j]
            if Right_border>Max_Right_border:
               Max_Right_border=Right_border
        return max(Max_Left_sum,Max_Right_sum,Max_Left_border+Max_Right_border)
    return Divide_and_Conquer(0,N-1)
@Run_time
def Max_SubSeq_sum_4(Seq):
    N=len(Seq)
    This_sum,Max_sum=0,0
    for i in Seq:
        # 复杂度为O(n)
        This_sum+=i
        if This_sum>Max_sum:
            Max_sum=This_sum
        if This_sum<0:
            This_sum=0
    return Max_sum
if __name__=='__main__':
    from random import randint
    Seq=[]
    for i in range(500):
        Seq.append(randint(-50,50))
    Max_SubSeq_sum_1(Seq)
    Max_SubSeq_sum_2(Seq)
    Max_SubSeq_sum_3(Seq)
    Max_SubSeq_sum_4(Seq)
