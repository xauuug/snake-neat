import pygame as p
import apple

class Snake:
    """Inicia Snake"""
    def __init__(self,headX,headY,blockSize):
        self.headX       = headX
        self.headY       = headY
        self.headXVel    = 0
        self.headYVel    = -blockSize
        self.prevdirection = 0
        self.direction   = 0
        self.snakeList   = []
        self.blockSize   = blockSize
        self.snakeLength = 1
        self.turnqt      = 0
        self.fome        = 100
        self.life        = 0
        self.pts         = 0

    """Desenha a Snake"""
    def drawSnake(self,gameDisplay):
        i = 0
        for snake in self.snakeList:
            c = p.Color(0)
            c.hsva = i, 100, 100, 100
            p.draw.rect(gameDisplay,c,[snake[0],snake[1],self.blockSize,self.blockSize])
            i += 10
            if i > 360:
                i = 0

    def moveLeft(self):
        self.prevdirection = self.direction
        self.headXVel = -self.blockSize
        self.headYVel = 0
        self.direction = 0

    def moveRight(self):
        self.prevdirection = self.direction
        self.headXVel = +self.blockSize
        self.headYVel = 0
        self.direction = 2

    def moveUp(self):
        self.prevdirection = self.direction
        self.headYVel = -self.blockSize
        self.headXVel = 0
        self.direction = 1

    def moveDown(self):
        self.prevdirection = self.direction
        self.headYVel = self.blockSize
        self.headXVel = 0
        self.direction = 3

    """Movimenta Snake"""
    def moveSnake(self):
        self.life += 1
        self.headX += self.headXVel
        self.headY += self.headYVel
        snakeHead = []
        snakeHead.append(self.headX)
        snakeHead.append(self.headY)
        i = 0
        for snake in self.snakeList:
            i += 1
            if snake[0] == snakeHead[0] and snake[1] == snakeHead[1] and i < self.snakeLength:
                return True
        self.snakeList.append(snakeHead)
        if len(self.snakeList) > self.snakeLength:
            del self.snakeList[0]
