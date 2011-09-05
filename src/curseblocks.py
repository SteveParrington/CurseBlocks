from grid import Grid
from curseinterface import CursesInterface
import curses
import time
from threading import Thread, RLock 

GRID_WIDTH = 14
GRID_HEIGHT = 25
SHAPE_WIDTH = 5
SHAPE_HEIGHT = 5

def makeShape(textShape):
    shapeGrid = []
    rotates = True
    count = 0
    for i in textShape:
        if len(i) < 3:
            count += 1
            if count == 1:
                if i[0] == '0':
                    rotates = False
            elif count == 2:
                if i[0].isdigit():
                    y = int(i[0])
            elif count == 3:
                if i[0].isdigit():
                    x = int(i[0])
        else:
            shapeLine = []
            for j in list(i):
                if j.isdigit():
                    shapeLine.append(int(j))
            shapeGrid.append(shapeLine)
    return shapeGrid, rotates, y, x

def readShapes():
    shapeFile = open('shapes', 'r')
    lines = shapeFile.readlines()
    noOfShapes = int(len(lines) / (SHAPE_WIDTH + 3))
    textShapes = []
    for i in range(noOfShapes):
        j = i + 1
        if j == noOfShapes:
            textShapes.append(lines[i * (SHAPE_WIDTH + 3):])
        else:
            textShapes.append(lines[i * (SHAPE_WIDTH + 3):j * (SHAPE_WIDTH + 3)])
    shapes = []
    for i in textShapes:
        shapes.append(makeShape(i))
        
    return shapes

def makeRotationMap(textRMap):
    pairsPerLine = int(len(textRMap[0]) / 2)
    rotationMap = []
    for line in textRMap:
        rotationMapLine = []
        for i in range(pairsPerLine):
            item1 = line[i * 2]
            item2 = line[i * 2 + 1]
            if item1.isdigit and item2.isdigit:
                pair = (item1, item2)
                rotationMapLine.append(pair)
        rotationMap.append(rotationMapLine)
    return rotationMap

def readRotationMaps():
    rmapFile = open('rmap', 'r')
    lines = rmapFile.readlines()
    textClockwise = lines[0:SHAPE_WIDTH]
    textAntiClockwise = lines[SHAPE_WIDTH+1:]
    clockwise = makeRotationMap(textClockwise)
    antiClockwise = makeRotationMap(textAntiClockwise)
    return clockwise, antiClockwise

def descentFunc(interface):
    gameGrid = interface.gameGrid
    lock = gameGrid.lock
    waitTime = gameGrid.waitTime 
    while True:
        time.sleep(waitTime)
        lock.acquire()
        gameGrid.down()
        interface.printGrid()
        if gameGrid.lose:
            if not interface.loseRoutineCalled:
                interface.loseRoutine()
                curses.endwin()
            lock.release()
            exit()
        lock.release()
        waitTime = gameGrid.waitTime

def controlFunc(interface):
    gameGrid = interface.gameGrid
    lock = gameGrid.lock
    gridWindow = interface.gridWindow
    while True:
        ch = -1
        while ch == -1:
            lock.acquire()
            ch = gridWindow.getch()
            if gameGrid.lose:
                if not interface.loseRoutineCalled:
                    interface.loseRoutine()
                    curses.endwin()
                lock.release()
                exit()
            lock.release()
        if ch == 119:
            lock.acquire()
            gameGrid.up()
            lock.release()
        elif ch == 115:
            lock.acquire()
            gameGrid.down()
            lock.release()
        elif ch == 97:
            lock.acquire()
            gameGrid.left()
            lock.release()
        elif ch == 100:
            lock.acquire()
            gameGrid.right()
            lock.release()
        lock.acquire()
        interface.printGrid()
        lock.release()
        if ch == 113:
            lock.acquire()
            gameGrid.lose = True
            lock.release()
        ch = -1

def initialise():
    shapes = readShapes()
    clockwise, antiClockwise = readRotationMaps()
    lock = RLock()
    gameGrid = Grid(shapes, clockwise, antiClockwise, GRID_WIDTH, GRID_HEIGHT, lock)
    try:
        interface = CursesInterface(gameGrid)
        descentThread = Thread(group=None, target=descentFunc, name=None, args=(interface,), kwargs=None)
        descentThread.daemon = True
        controlThread = Thread(group=None, target=controlFunc, name=None, args=(interface,), kwargs=None)
        descentThread.start()
        controlThread.start()
    except (curses.error, TypeError, IndexError, NameError) as e:
        curses.endwin()
        print(len(gameGrid.grid))
        raise e
        exit()
        
if __name__ == '__main__':
    initialise()
