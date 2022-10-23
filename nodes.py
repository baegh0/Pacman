import pygame
from vector import Vector2
from constants import *

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL: None}
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                            DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                            LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                            RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)
                
    def denyAccess(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allowAccess(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)


class NodeGroup(object):
    def __init__(self, maze):
        self.nodesList = {}
        self.nodeSymbols = ['+', 'p']
        self.pathSymbols = ['.']
        self.mazeData = self.openMaze(maze)
        self.createNodeGraph(self.mazeData)
        self.connectHorizontal(self.mazeData)
        self.connectVertical(self.mazeData)
        self.homekey = None

   # Creates the Nodes based on the x and y positions from our text file
    def createNodeGraph(self, data, add_x=0, add_y=0):
        for row in range(len(data)):
            for column in range(len(data[row])):
                if data[row][column] in self.nodeSymbols:
                    x, y = self.constructKey(column+add_x, row+add_y)
                    self.nodesList[(x,y)] = Node(x,y)
    
    # Open Maze and create it into a list
    def openMaze(self, maze):
        l = []
        with open(maze) as m:
            for line in m:
                newM = ''.join(line.split())
                l.append(list(newM.strip()))
        return l

    # Replaces Numpy's Transpose method
    def transpose(self, data):
        new = [[0] * len(data) for _ in range(len(data[0]))]

        for row in range(len(data)):
            for col in range(len(data[row])):
                new[col][row] = data[row][col]
        return new

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def render(self, screen):
        for node in self.nodesList.values():
            node.render(screen)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    # Connects nodes horizontally
    def connectHorizontal(self, data, x_offset=0, y_offset=0):
        for row in list(range(len(data))):
            key = None
            for column in list(range(len(data[row]))):
                if data[row][column] in self.nodeSymbols:
                    if key is None:
                        key =self.constructKey(column+x_offset, row+y_offset)
                    else:
                        next_key = self.constructKey(column+x_offset, row+y_offset)
                        self.nodesList[key].neighbors[RIGHT] = self.nodesList[next_key]
                        self.nodesList[next_key].neighbors[LEFT] = self.nodesList[key]
                        key = next_key
                elif data[row][column] not in self.pathSymbols:
                    key = None

    # Connects nodes vertically
    def connectVertical(self, data, x_offset=0, y_offset=0):
        transposedData = self.transpose(data)
        for row in range(len(transposedData)):
            key = None
            for col in range(len(transposedData[row])):
                if transposedData[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(row+x_offset, col+y_offset)
                    else:
                        next_key = self.constructKey(row+x_offset, col+y_offset)
                        self.nodesList[key].neighbors[DOWN] = self.nodesList[next_key]
                        self.nodesList[next_key].neighbors[UP] = self.nodesList[key]
                        key = next_key
                elif transposedData[row][col] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesList.keys():
            return self.nodesList[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesList.keys():
            return self.nodesList[(x, y)]
        return None

    def getStartTempNode(self):
        nodes = list(self.nodesList.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesList.keys() and key2 in self.nodesList.keys():
            self.nodesList[key1].neighbors[PORTAL] = self.nodesList[key2]
            self.nodesList[key2].neighbors[PORTAL] = self.nodesList[key1]

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def createHomeNodes(self, xoffset, yoffset):
        homedata = ([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeGraph(homedata, xoffset, yoffset)
        self.connectHorizontal(homedata, xoffset, yoffset)
        self.connectVertical(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):     
        key = self.constructKey(*otherkey)
        self.nodesList[homekey].neighbors[direction] = self.nodesList[key]
        self.nodesList[key].neighbors[direction*-1] = self.nodesList[homekey]

    def denyAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    def denyAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    def allowAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.allowAccess(col, row, direction, entity)

    def denyHomeAccess(self, entity):
        self.nodesList[self.homekey].denyAccess(DOWN, entity)

    def allowHomeAccess(self, entity):
        self.nodesList[self.homekey].allowAccess(DOWN, entity)

    def denyHomeAccessList(self, entities):
        for entity in entities:
            self.denyHomeAccess(entity)

    def allowHomeAccessList(self, entities):
        for entity in entities:
            self.allowHomeAccess(entity)    