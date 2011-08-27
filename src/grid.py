import random
from shape import Shape
import curses

class Grid:

    def __init__(self, shapes, clockwise, antiClockwise, lock):
        self.shapes = shapes
        self.clockwise = clockwise
        self.antiClockwise = antiClockwise
        self.gridWidth = 14
        self.gridHeight = 20
        self.initialX = 4
        self.initialY = 3
        self.lock = lock
        self.lose = False
        self.grid = [[0 for i in range(self.gridWidth)] 
                        for j in range(self.gridHeight)]
        self.fullLine = [1 for i in range(self.gridWidth)]
        self.clearLine = [0 for i in range(self.gridWidth)]
        self.noOfShapes = len(shapes)
        self.__getNextShape()
        self.__drawShape()

    def __getNextShape(self):
        shapeId = random.randint(0, self.noOfShapes - 1)
        nextShape = Shape(self.shapes[shapeId][0], self.initialX, self.initialY, 
                          self.shapes[shapeId][1])
        self.currentShape = nextShape
    
    def __drawShape(self):
        currentShape = self.currentShape
        offset = int(len(currentShape.grid) / 2)
        startingX = currentShape.x - offset
        startingY = currentShape.y - offset
        
        for i in range(len(currentShape.grid)):
            for j in range(len(currentShape.grid[i])):
                x = startingX + i
                y = startingY + j
                if currentShape.grid[i][j]:
                    if x >= self.gridWidth or x < 0:
                        return False
                    if y >= self.gridHeight or y < 0:
                        return False
                if currentShape.grid[i][j] and self.grid[y][x]:
                    return False

        for i in range(len(currentShape.grid)):
            for j in range(len(currentShape.grid[i])):
                if currentShape.grid[i][j]:
                    x = startingX + i
                    y = startingY + j
                    self.grid[y][x] = currentShape.grid[i][j]
        return True

    def __undrawShape(self):
        currentShape = self.currentShape
        offset = int(len(currentShape.grid) / 2)
        startingX = currentShape.x - offset
        startingY = currentShape.y - offset

        for i in range(len(currentShape.grid)):
            for j in range(len(currentShape.grid[i])):
                if currentShape.grid[i][j]:
                    x = startingX + i
                    y = startingY + j
                    self.grid[y][x] = 0

    def clearLines(self):
        try:
            while True:
                self.grid.remove(self.fullLine)     
        except ValueError as e:
            pass 
        while len(self.grid) < self.gridHeight:
            self.grid.insert(0, [0 for j in range(self.gridWidth)])
            
    def up(self):
        self.__undrawShape()
        self.currentShape.rotate(self.clockwise)
        if not self.__drawShape():
            self.currentShape.rotate(self.antiClockwise)
            self.__drawShape()

    def down(self):
        self.__undrawShape()
        self.currentShape.y += 1
        if not self.__drawShape():
            self.currentShape.y -= 1
            self.__drawShape()
            self.clearLines()
            self.__getNextShape()
            if not self.__drawShape():
                self.lose = True

    def left(self):
        self.__undrawShape()
        self.currentShape.x -= 1
        if not self.__drawShape():
            self.currentShape.x += 1
            self.__drawShape()

    def right(self):
        self.__undrawShape()
        self.currentShape.x += 1
        if not self.__drawShape():
            self.currentShape.x -= 1
            self.__drawShape()       
