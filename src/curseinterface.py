import curses

class CursesInterface:

    def __init__(self, gameGrid):
        self.scr = curses.initscr()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self.gridWidth = gameGrid.gridWidth
        self.gridHeight = gameGrid.gridHeight
        self.gridWindow = curses.newwin(self.gridHeight + 2, self.gridWidth + 2,
                                        2, 4)
        self.gridWindow.border()
        self.gridWindow.nodelay(1)
        self.gameGrid = gameGrid
        
    def printGrid(self):
        ch = '#'
        ch = ch.encode(encoding="ascii", errors="strict")
        grid = self.gameGrid.grid
        offset = 1
        gridWindow = self.gridWindow
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                try:
                    if grid[i][j]:
                        gridWindow.addch(i + offset, j + offset, ch)
                    else:
                        gridWindow.addch(i + offset, j + offset, ' ')
                except curses.error as e:
                    curses.endwin()
                    print(i, j)
                    exit()
