import random
from termcolor import colored
import time
import sys
import copy

MAIZE_SIZE = 20
BLOCKS = 100

write = sys.stdout.write

class Cell:
    def __init__ (self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__ (self, other):
        if (self.x == other.x and self.y == other.y):
            return True
        else:
            return False

# Create Maize
maize = [ [' ' for i in range(MAIZE_SIZE)] for i in range(MAIZE_SIZE) ]
maize[0] = [colored('X', 'red') for i in range (MAIZE_SIZE)]
maize[MAIZE_SIZE - 1] = [colored('X', 'red') for i in range (MAIZE_SIZE)]
for i in range(MAIZE_SIZE):
    maize[i][0] = colored('X', 'red')
    maize[i][MAIZE_SIZE - 1] = colored('X', 'red')

# Select start and end points
start = Cell(random.randint(1, MAIZE_SIZE-2), random.randint(1, MAIZE_SIZE-2), None)
goal = Cell(random.randint(1, MAIZE_SIZE-2), random.randint(1, MAIZE_SIZE-2), None)

maize[start.x][start.y] = colored('S', 'blue')
maize[goal.x][goal.y] = colored('G', 'green')

# Select random boundary places
blocks = []
for i in range(BLOCKS):
    blockCell = Cell(random.randint(1, MAIZE_SIZE-2), random.randint(1, MAIZE_SIZE-2), None)
    while((blockCell) in blocks or (blockCell == start) or (blockCell == goal)):
        blockCell = Cell(random.randint(1, MAIZE_SIZE-2), random.randint(1, MAIZE_SIZE-2), None)
    blocks.append(blockCell)
    maize[blockCell.x][blockCell.y] = colored('X', 'red')

def printMaize(maize, temp = True):
    for i in maize:
        for j in i:
            print(j, end=" ")
        print ("")
    if (temp):
        for i in maize:
            write ('\b' * len(i))
            write ('\033[F')
    time.sleep(.1)

printMaize(maize)

def heuristic(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y))

def popFromOpenSet(openSet):
    minVal = 0
    for i in range(len(openSet)):
        if (openSet[i].f < openSet[minVal].f):
            minVal = i
        if (openSet[i].f == openSet[minVal].f):
            if (openSet[i].g > openSet[minVal].g):
                        minVal = i
    cell = openSet[minVal]
    del openSet[minVal]
    return cell

openSet = []
closedSet = []

openSet.append(start)

current = start

while (len(openSet) > 0):
    current = popFromOpenSet(openSet)

    # print (openSet)
    if(current == goal):
        # print ("Got Solution")
        break

    # print Map
    tempMaize = copy.deepcopy(maize)
    tempMaize[start.x][start.y] = colored('S', 'blue')
    tempCurrent = current
    while tempCurrent.parent is not None:
        tempMaize[tempCurrent.x][tempCurrent.y] = colored('O', 'yellow')
        tempCurrent = tempCurrent.parent
    tempMaize[goal.x][goal.y] = colored('G', 'green')

    printMaize(tempMaize)

    # Searching
    closedSet.append(current)
    maize[current.x][current.y] = colored('O', 'blue')

    top = Cell(current.x - 1, current.y, current)
    bottom = Cell(current.x + 1, current.y, current)
    left = Cell(current.x, current.y - 1, current)
    right = Cell(current.x, current.y + 1, current)

    neighbors = [top, bottom, left, right]

    for neighbor in neighbors:
        if (str(maize[neighbor.x][neighbor.y]) != str(colored('X', 'red'))):
            if(neighbor not in closedSet):

                # distance from start to neighbor
                tempG = current.g + 1

                if (neighbor not in openSet):
                    openSet.append(neighbor)
                else:
                    if (tempG >= neighbor.g):
                        #This is not a better path
                        continue

                neighbor.g = tempG
                neighbor.f = neighbor.g + heuristic(neighbor, goal)

maize[start.x][start.y] = colored('S', 'blue')

if (current == goal):
    while current.parent is not None:
        maize[current.x][current.y] = colored('0', 'yellow')
        current = current.parent
    maize[goal.x][goal.y] = colored('G', 'green')
else:
    print ("NO SOLUTION")

printMaize(maize, False)
