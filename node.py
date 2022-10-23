import pygame as pg
import settings as setting
from vector import Vector

up = setting.UP
down = setting.DOWN
right = setting.RIGHT
left = setting.LEFT
portal = setting.PORTAL

class Node:
    def __init__(self, x, y):
        self.position = Vector(x,y)
        self.neighbor = {up:None, 
                         down:None,
                         right:None,
                         left:None,
                         portal:None}
    
    def draw(self, screen):
        for i in self.neighbor.keys():
            if self.neighbor[i] is not None:
                start = self.position.pos()
                end = self.neighbor[i].position.pos()
                pg.draw.line(screen, setting.WHITE, start, end, 2)
                pg.draw.circle(screen, setting.RED, self.position.pos(), 4)

class Nodes(object):
    def __init__(self, maze):
        self.nodesLIST = {}
        self.nodeSymbols = ['+', 'p']
        self.pathSymbols = ['.']
        self.mazeData = self.openMaze(maze)
        self.createNodeGraph(self.mazeData)
        self.connectHorizontal(self.mazeData)
        self.connectVertical(self.mazeData)

    # Creates the Nodes based on the x and y positions from our text file
    def createNodeGraph(self, data, add_x=0, add_y=0):
        for row in range(len(data)):
            for column in range(len(data[row])):
                if data[row][column] in self.nodeSymbols:
                    x, y = self.createKey(column+add_x, row+add_y)
                    self.nodesLIST[(x,y)] = Node(x,y)
    
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

    # Creates Key depending on XY location
    def createKey(self, x, y):
        return x * setting.BLOCK_WIDTH, y * setting.BLOCK_HEIGHT

    # Connects nodes horizontally
    def connectHorizontal(self, data, x_offset=0, y_offset=0):
        for row in list(range(len(data))):
            key = None
            for column in list(range(len(data[row]))):
                if data[row][column] in self.nodeSymbols:
                    if key is None:
                        key =self.createKey(column+x_offset, row+y_offset)
                    else:
                        next_key = self.createKey(column+x_offset, row+y_offset)
                        self.nodesLIST[key].neighbor[right] = self.nodesLIST[next_key]
                        self.nodesLIST[next_key].neighbor[left] = self.nodesLIST[key]
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
                        key = self.createKey(row+x_offset, col+y_offset)
                    else:
                        next_key = self.createKey(row+x_offset, col+y_offset)
                        self.nodesLIST[key].neighbor[down] = self.nodesLIST[next_key]
                        self.nodesLIST[next_key].neighbor[up] = self.nodesLIST[key]
                        key = next_key
                elif transposedData[row][col] not in self.pathSymbols:
                    key = None

    def getPixelLocation(self, x, y):
        if (x,y) in self.nodesLIST.keys():
            return self.nodesLIST[(x,y)]
        else:
            return None

    def getTileLocation(self, column, row):
        x, y = self.createKey(column, row)
        if(x,y) in self.nodesLIST.keys():
            return self.nodesLIST[(x,y)]
        else:
            return None
    
    #This is temporary
    def getStartNode(self):
        nodes = list(self.nodesLIST.values())
        return nodes[0]
    
    def draw(self, screen):
        for node in self.nodesLIST.values():
            node.draw(screen)

    def setSides(self, left_side, right_side):
        key1 = self.createKey(*left_side)
        key2 = self.createKey(*right_side)
        if key1 in self.nodesLIST.keys() and key2 in self.nodesLIST.keys():
            self.nodesLIST[key1].neighbor[portal] = self.nodesLIST[key2]
            self.nodesLIST[key2].neighbor[portal] = self.nodesLIST[key1]
