import curses

class CursesInterface:

    def __init__(self, gameGrid):
        self.scr = curses.initscr()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self.gridWidth = gameGrid.gridWidth
        self.gridHeight = gameGrid.gridHeight
        self.gridWindow = curses.newwin(self.gridHeight + 2, self.gridWidth * 2 + 2,
                                        2, 4)
        self.gridWindow.border()
        self.gridWindow.nodelay(1)
        self.gameGrid = gameGrid
        
    def printGrid(self):
        grid = self.gameGrid.grid
        offset = 1
        gridWindow = self.gridWindow
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                try:
                    if grid[i][j]:
                        gridWindow.addstr(i + offset, j * 2 + offset, '  ', curses.A_STANDOUT )
                    else:
                        gridWindow.addstr(i + offset, j * 2 + offset, '  ')
                except curses.error as e:
                    curses.endwin()
                    print(i, j)
                    exit()
