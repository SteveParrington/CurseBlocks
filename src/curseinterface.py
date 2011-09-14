import curses
import time

class CursesInterface:

    def __init__(self, gameGrid):
        self.scr = curses.initscr()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self.gridWidth = gameGrid.gridWidth
        self.gridHeight = gameGrid.gridHeight
        self.gridVisibleAt = gameGrid.gridVisibleAt
        self.gridWindow = curses.newwin(self.gridHeight + 2 - self.gridVisibleAt,
                                        self.gridWidth * 2 + 2, 2, 4)
        self.nextShapeWindow = curses.newwin(7, 12, 2, 40)
        self.nextShapeWindow.border()
        self.nextShapeWindow.addstr(0, 1, 'Next')
        self.scoreWindow = curses.newwin(1, 40, 10, 40)
        self.scoreWindow.nodelay(1)
        self.gridWindow.border()
        self.gridWindow.nodelay(1)
        self.gameGrid = gameGrid
     
    def loseRoutine(self):
        curses.endwin()

    def printGrid(self):
        grid = self.gameGrid.grid
        gameGrid = self.gameGrid
        offset = 1
        gridWindow = self.gridWindow
        self.__printScore()
        self.__printNextShape()
        for i in range(gameGrid.gridVisibleAt, len(grid)):
            for j in range(len(grid[i])):
                try:
                    if grid[i][j]:
                        gridWindow.addstr(i + offset - gameGrid.gridVisibleAt, j * 2 + offset, '  ', curses.A_STANDOUT)
                    else:
                        gridWindow.addstr(i + offset - gameGrid.gridVisibleAt, j * 2 + offset, '  ')
                except curses.error as e:
                    curses.endwin()
                    print(i, j)
                    raise e
                    exit()
    
    def __printNextShape(self):
        shapeGrid = self.gameGrid.nextShape.grid
        offset = 1
        nextShapeWindow = self.nextShapeWindow
        for i in range(len(shapeGrid)):
            for j in range(len(shapeGrid[i])):
                try:
                    if shapeGrid[i][j]:
                        nextShapeWindow.addstr(j + offset, i * 2 + offset, '  ', curses.A_STANDOUT)
                    else:
                        nextShapeWindow.addstr(j + offset, i * 2 + offset, '  ')
                except curses.error as e:
                    curses.endwin()
                    raise e
                    exit()
        nextShapeWindow.refresh()

    def __printScore(self):
       grid = self.gameGrid
       score = grid.score
       scoreWindow = self.scoreWindow
       scoreStr = 'Score: ' + str(score)
       scoreWindow.addstr(0, 0, scoreStr)
       scoreWindow.refresh()
