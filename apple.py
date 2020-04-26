import random
import pygame as p

class Apple:
    """Inicia a maçã"""
    def __init__(self,displayWidth,displayHeight,blockSize,snakeList):
        #random.seed(42)
        Col = True
        self.blockSize = blockSize
        while(Col):
            Col = False
            self.randAppleX = round((random.randrange(0,displayWidth-blockSize))/blockSize) * blockSize
            self.randAppleY = round((random.randrange(0,displayHeight-blockSize))/blockSize) * blockSize
            for snake in snakeList:
                if self.randAppleX == snake[0] and self.randAppleY == snake[1]:
                    Col = True
                    self.randPos(displayWidth,displayHeight)

    """Define posição aleatoria pra maçã"""
    def randPos(self,displayWidth,displayHeight,snakeList):
        dif = True
        self.randAppleX = round((random.randrange(0,displayWidth-self.blockSize))/self.blockSize) * self.blockSize
        self.randAppleY = round((random.randrange(0,displayHeight-self.blockSize))/self.blockSize) * self.blockSize
        while dif:
            acho = False
            for s in snakeList:
                if self.randAppleX == s[0] and self.randAppleY == s[1]:
                    acho = True
                    self.randAppleX = round((random.randrange(0,displayWidth-self.blockSize))/self.blockSize) * self.blockSize
                    self.randAppleY = round((random.randrange(0,displayHeight-self.blockSize))/self.blockSize) * self.blockSize
            if acho == False:
                dif = False

    """Desenha a maçã"""
    def draw(self,gameDisplay):
        p.draw.rect(gameDisplay,(255,255,255),[self.randAppleX,self.randAppleY,self.blockSize,self.blockSize])
