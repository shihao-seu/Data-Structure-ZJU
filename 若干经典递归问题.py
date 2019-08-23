import turtle
import numpy as np


def n2str(n):
    """16进制字符转换"""
    if n in range(10, 16):
        hex_str = 'ABCDEF'
        hex_num = range(10, 16)
        return hex_str[hex_num.index(n)]
    else:
        return str(n)


def baseConverter(n, base):
    '''递归求进制转换'''
    if n < base:
        # 满足定律一：具有终止条件
        return n2str(n % base)
    # 满足定律二：向基本情况逼近
    # 满足定律三：调用自身函数
    # 向后添加余数
    return baseConverter(n//base, base)+ n2str(n % base)


def drawSpiral(myTurtle, lineLen):
    # 最大运动长度LineLen
    if lineLen > 0:
        myTurtle.forward(lineLen)
        myTurtle.right(90)
        # 右转90°
        drawSpiral(myTurtle,lineLen-5)
        # 每次转向前进长度-5


def tree(branchLen, t):
    '''分形树问题'''
    if branchLen > 5:
        t.forward(branchLen)
        t.right(20)
        # 画出右分支并回到开叉点
        tree(branchLen - 15, t)
        t.left(40)
        # 画出做分支并回到开叉点
        tree(branchLen - 15, t)
        # 回到最终的起点
        t.right(20)
        t.backward(branchLen)


def drawTriangle(points, color, t):
    # 三点绘制三角形
    t.fillcolor(color)
    t.up() #提笔，笔移动时不划线
    t.goto(points[0][0],points[0][1])
    t.down() #下笔，划线
    t.begin_fill()
    t.goto(points[1][0],points[1][1])
    t.goto(points[2][0],points[2][1])
    t.goto(points[0][0],points[0][1])
    t.end_fill()


def div3(points):
    '''求三角形左上右三个小三角顶点'''
    p0, p1, p2 = points
    p3 = (p0 + p1) / 2
    # list不支持这样的运算，所以我们用了ndarray对象
    p4 = (p0 + p2) / 2
    p5 = (p1 + p2) / 2
    return [[p0,p3,p4],[p3,p1,p5],[p4,p5,p2]]


def sierpinski(points, degree, t):
    colors = ['blue','red','green','white']
    if degree >= 0:
        # 绘制大三角
        drawTriangle(points, colors[degree], t)
        # 绘制左三角
        sierpinski(div3(points)[0], degree-1, t)
        # 绘制上三角
        sierpinski(div3(points)[1], degree-1, t)
        # 绘制右三角
        sierpinski(div3(points)[2], degree-1, t)


if __name__ == '__main__':
    # 进制转换检验
    print(baseConverter(233, 2))
    print(baseConverter(233, 8))
    print(baseConverter(233, 16))
    # 绘制螺旋线
    myTurtle = turtle.Turtle() # 创建乌龟
    myWin = turtle.Screen() # 创建绘图窗口
    drawSpiral(myTurtle,100)
    myWin.exitonclick() # 绘图停止，单击叉号关闭窗口
    # 绘制分形树
    t = turtle.Turtle()
    myWin = turtle.Screen()
    t.left(90)
    t.color("red")
    tree(75,t)
    myWin.exitonclick()
    # Sierpinski三角
    t = turtle.Turtle()
    myWin = turtle.Screen()
    myPoints = np.asarray([[-100, -50], [0, 100], [100, -50]])  # 大三角三顶点（左下、中上、右下）
    sierpinski(myPoints, 3, t)
    myWin.exitonclick()
