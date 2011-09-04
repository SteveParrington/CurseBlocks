import curses

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
        self.scoreWindow = curses.newwin(1, 40, 3, 40)
        self.scoreWindow.nodelay(1)
        self.gridWindow.border()
        self.gridWindow.nodelay(1)
        self.gameGrid = gameGrid
        
    def printGrid(self):
        grid = self.gameGrid.grid
        gameGrid = self.gameGrid
        offset = 1
        gridWindow = self.gridWindow
        self.__printScore()
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

    def __printScore(self):
       grid = self.gameGrid
       score = grid.score
       scoreWindow = self.scoreWindow
       scoreStr = 'Score: ' + str(score)
       scoreWindow.addstr(0, 0, scoreStr)
       scoreWindow.refresh()
