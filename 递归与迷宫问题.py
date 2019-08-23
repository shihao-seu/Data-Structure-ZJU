import turtle

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'


class Maze:
    def __init__(self, mazeFileName):
        """读取文本创建地图列表"""
        mazeFile = open(mazeFileName, 'r')
        # 创建一个二维嵌套列表,并得到起点、行宽、列高三个参数
        self.mazelist = []
        self.rowsInMaze = 0
        self.columnsInMaze = 0
        for line in mazeFile:
            rowList = []
            col = 0
            for ch in line:
                rowList.append(ch)
                # 寻找乌龟起点坐标
                if ch == 'S':
                    self.startRow = self.rowsInMaze
                    self.startCol = col
                col += 1
            self.rowsInMaze += 1
            self.mazelist.append(rowList)
            self.columnsInMaze = len(rowList)
        '''
        原代码中设置了一个偏心距离，为了程序简洁性，现去除这两个参数
        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        '''
        self.t = turtle.Turtle()
        self.t.shape('turtle') # 画笔形状是一个小乌龟
        self.wn = turtle.Screen()
        # 两个对角点确定画布大小，目的是调整窗口，包含全幅
        '''
        原代码是通过调整x\y坐标间距将矩形拉成方形。下面修改为真实大小
        self.wn.setworldcoordinates(-self.columnsInMaze/2-1, -self.rowsInMaze/2-1,
                                    self.columnsInMaze/2+1, self.rowsInMaze/2+1)
        '''
        maxsize = max(self.columnsInMaze, self.rowsInMaze)
        self.wn.setworldcoordinates(0,-3*maxsize/4, maxsize, maxsize/4)

    def drawMaze(self):
        '''绘制迷宫'''
        self.t.speed(10)
        # 设置图片刷新延迟时间，若不设置，则可以看到乌龟画迷宫的全过程
        self.wn.tracer(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    # 注意-y，为了使y轴转向
                    self.drawCenteredBox(x, -y,'orange')
        self.t.color('black')
        self.t.fillcolor('blue')
        # 执行一次屏幕刷新
        self.wn.update()
        self.wn.tracer(1)

    def drawCenteredBox(self, x, y, color):
        '''绘制方形障碍物，长为1'''
        self.t.up()
        self.t.goto(x - .5, y - .5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self,x,y):
        '''移动乌龟'''
        self.t.up()
        self.t.setheading(self.t.towards(x,-y))
        self.t.goto(x,-y)

    def dropBreadcrumb(self,color):
        '''撒一粒面包屑'''
        self.t.dot(10,color)

    def updatePosition(self,row,col,val=None):
        '''移动乌龟位置，并根据位置属性做下标记'''
        self.moveTurtle(col, row)
        if val:
            # 改变乌龟所在迷宫格的属性，并投下相应颜色的面包
            self.mazelist[row][col] = val

        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)

    def isExit(self,row,col):
        '''四周全封闭仅一个缺口，因此到达墙的位置就说明到达出口'''
        return (row == 0 or
                row == self.rowsInMaze-1 or
                col == 0 or
                col == self.columnsInMaze-1 )

    def __getitem__(self,idx):
        '''重载索引运算符'''
        return self.mazelist[idx]


def searchFrom(maze, startRow, startColumn):
    # try each of four directions from this point until we find a way out.
    # base Case return values:
    #  1. We have run into an obstacle, return false
    maze.updatePosition(startRow, startColumn)
    if maze[startRow][startColumn] == OBSTACLE :
        return False
    #  2. We have found a square that has already been explored
    if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
        return False
    # 3. We have found an outside edge not occupied by an obstacle
    if maze.isExit(startRow,startColumn):
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        return True
    # 普通路径内部标记‘来过’
    maze.updatePosition(startRow, startColumn, TRIED)
    # Otherwise, use logical short circuiting to try each direction
    # in turn (if needed)
    found = searchFrom(maze, startRow-1, startColumn) or \
            searchFrom(maze, startRow+1, startColumn) or \
            searchFrom(maze, startRow, startColumn-1) or \
            searchFrom(maze, startRow, startColumn+1)
    # 出栈的过程，从出口标注绿色面包直到起点
    if found:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)
    return found


myWin = turtle.Screen()
myMaze = Maze(r'c:\Python\py\maze2.txt')
myMaze.drawMaze()
# 移动乌龟到起点
myMaze.updatePosition(myMaze.startRow, myMaze.startCol)
searchFrom(myMaze, myMaze.startRow, myMaze.startCol)
myWin.exitonclick()