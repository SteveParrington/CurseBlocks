class Shape:

    def __init__(self, grid, x, y, rotates):
        self.grid = grid
        self.x = x
        self.y = y
        self.rotates = rotates
        
    def rotate(self, rotationMap):
        if self.rotates:
            newGrid = [[0 for i in range(5)] for j in range(5)]
                  
            for i in range(len(rotationMap)):
                for j in range(len(rotationMap[i])):
                    x = int(rotationMap[i][j][0])
                    y = int(rotationMap[i][j][1])
                    newGrid[x][y] = self.grid[i][j]
                
            self.grid = newGrid
