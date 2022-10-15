import pygame as pg
import settings as setting
from vector import Vector

up = setting.UP
down = setting.DOWN
right = setting.RIGHT
left = setting.LEFT

class Nodes(object):
    def __init__(self):
        self.nodes = []

    # TEST
    def test(self):
        nodeA = Node(80 ,80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)
        nodeA.neighbor[right] = nodeB
        nodeA.neighbor[down] = nodeC
        nodeB.neighbor[left] = nodeA
        nodeB.neighbor[down] = nodeD
        nodeC.neighbor[up] = nodeA
        nodeC.neighbor[right] = nodeD
        nodeC.neighbor[down] = nodeF
        nodeD.neighbor[up] = nodeB
        nodeD.neighbor[left] = nodeC
        nodeD.neighbor[right] = nodeE
        nodeE.neighbor[left] = nodeD
        nodeE.neighbor[down] = nodeG
        nodeF.neighbor[up] = nodeC
        nodeF.neighbor[right] = nodeG
        nodeG.neighbor[up] = nodeE
        nodeG.neighbor[left] = nodeF
        self.nodes = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

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