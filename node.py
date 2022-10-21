import pygame as pg
import settings as setting
from vector import Vector
import numpy as np

up = setting.UP
down = setting.DOWN
right = setting.RIGHT
left = setting.LEFT

class Node:
    def __init__(self, x, y):
        self.position = Vector(x,y)
        self.neighbor = {up:None, 
                         down:None,
                         right:None,
                         left:None}
    
    def draw(self, screen):
        for i in self.neighbor.keys():
            if self.neighbor[i] is not None:
                start = self.position.pos()
                end = self.neighbor[i].position.pos()
                pg.draw.line(screen, setting.WHITE, start, end, 2)
                pg.draw.circle(screen, setting.RED, self.position.pos(), 4)

class Nodes(object):
    def __init__(self, maze):
        # self.nodes = []
        self.maze = maze
        self.nodesLIST = {}
        self.nodeSymbols = ['+']
        self.pathSymbols = ['.']
        mazeData = self.readMazeFile(maze)
        self.createNodeGraph(mazeData)
        self.connectHorizontal(mazeData)
        self.connectVertical(mazeData)

    # TEST
    # def test(self):
    #     nodeA = Node(80 ,80)
    #     nodeB = Node(160, 80)
    #     nodeC = Node(80, 160)
    #     nodeD = Node(160, 160)
    #     nodeE = Node(208, 160)
    #     nodeF = Node(80, 320)
    #     nodeG = Node(208, 320)
    #     nodeA.neighbor[right] = nodeB
    #     nodeA.neighbor[down] = nodeC
    #     nodeB.neighbor[left] = nodeA
    #     nodeB.neighbor[down] = nodeD
    #     nodeC.neighbor[up] = nodeA
    #     nodeC.neighbor[right] = nodeD
    #     nodeC.neighbor[down] = nodeF
    #     nodeD.neighbor[up] = nodeB
    #     nodeD.neighbor[left] = nodeC
    #     nodeD.neighbor[right] = nodeE
    #     nodeE.neighbor[left] = nodeD
    #     nodeE.neighbor[down] = nodeG
    #     nodeF.neighbor[up] = nodeC
    #     nodeF.neighbor[right] = nodeG
    #     nodeG.neighbor[up] = nodeE
    #     nodeG.neighbor[left] = nodeF
    #     self.nodes = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    # Reads and returns data from our maze.txt
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    # Creates the Nodes based on the x and y positions from our text file
    def createNodeGraph(self, data, add_x=0, add_y=0):
        for row in list(range(data.shape[0])):
            for column in list(range(data.shape[1])):
                if data[row][column] in self.nodeSymbols:
                    x, y = self.createKey(column+add_x, row+add_y)
                    self.nodesLIST[(x,y)] = Node(x,y)

    # Creates Key depending on XY location
    def createKey(self, x, y):
        return x * setting.BLOCK_WIDTH, y * setting.BLOCK_HEIGHT

    # Connects nodes horizontally
    def connectHorizontal(self, data, x_offset=0, y_offset=0):
        for row in list(range(data.shape[0])):
            key = None
            for column in list(range(data.shape[1])):
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
        transposedData = data.transpose()
        for column in list(range(transposedData.shape[0])):
            key = None
            for row in list(range(transposedData.shape[1])):
                if transposedData[column][row] in self.nodeSymbols:
                    if key is None:
                        key = self.createKey(column+x_offset, row+y_offset)
                    else:
                        next_key = self.createKey(column+x_offset, row+y_offset)
                        self.nodesLIST[key].neighbor[down] = self.nodesLIST[next_key]
                        self.nodesLIST[next_key].neighbor[up] = self.nodesLIST[key]
                        key = next_key
                elif transposedData[column][row] not in self.pathSymbols:
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
