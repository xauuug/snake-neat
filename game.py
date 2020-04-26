import pygame as p
import time
import random
import neat
import math
import pickle

import os

import apple
import snake
import opsnake

from math import floor

class SnakeGame:
    """Inicia o ambiente do jogo"""
    def __init__(self,agent2):
        p.init()
        p.display.set_caption('Snake Game')
        self.displayWidth  = 800
        self.displayHeight = 600
        self.gameDisplay   = p.display.set_mode((self.displayWidth,self.displayHeight))
        self.FPS           = 60
        self.font          = p.font.SysFont(None,25)
        self.blockSize     = 25
        self.clock         = p.time.Clock()
        self.player        = opsnake.OpSnake(self.displayWidth/2,self.displayHeight/2,self.blockSize)
        self.gameExit      = False
        self.gameOver      = False
        self.apple         = apple.Apple(self.displayWidth,self.displayHeight,self.blockSize,self.player.snakeList)
        self.fitness       = 0.0
        self.control       = True
        self.outS          = False
        self.debug         = False
        self.agent         = agent2
        #self.hamilton      = hamilton.HamiltonSnake(self.displayWidth/2,self.displayHeight/2,self.blockSize)

        self.player.snakeLength = 3

    """Calcula e rotorna o Fitness"""
    def calcFitness(self,alpha=0.1):
        #return self.player.pts
        #if self.player.snakeLength < 10:
        #    return floor(self.player.life * self.player.life * 2**self.player.snakeLength)
        #else:
        #    fit = self.player.life * self.player.life
        #    fit *= 2**10
        #    fit *= (self.player.snakeLength-9)
        #    return fit
        return self.player.snakeLength - (self.player.turnqt*0.01)
        #return self.player.life/100 - (self.player.turnqt*0.01)


    """Imprime o Fitness"""
    def printFitness(self,msg,color):
        screen_text = self.font.render(msg,True,color)
        self.gameDisplay.blit(screen_text,[self.displayWidth/2-50,self.displayHeight/2-275])

    """Loop do jogo"""
    def gameLoop(self):
        black = (0,0,0)
        while not self.gameExit:
            self.gameDisplay.fill(black)
            self.getEvents(self.debug)
            self.player.drawSnake(self.gameDisplay)
            if self.player.moveSnake():
                self.gameOver = True

            self.apple.draw(self.gameDisplay)
            self.checkAppleColission()
            self.player.fome -= 1
            self.fitness = self.calcFitness()
            self.printFitness(f"Fitness : {'%.2f' % self.fitness}",(255,255,255))
            p.display.update()
            if self.calcFitness() < 0:
                return 0
            if self.gameOver or self.player.fome < 0:
                if self.outS == False:
                    return self.calcFitness()
                else:
                    return self.calcFitness() - 0.7
            self.outScreen()
            self.clock.tick(self.FPS)
        time.sleep(2)
        p.quit()
        quit()

    """Analisa a entrada"""
    def getEvents(self,debug):
        for event in p.event.get() :
            if event.type == p.QUIT:
                self.gameExit = True
            if event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    self.player.moveLeft()
                    self.player.turnqt += 1
                elif event.key == p.K_RIGHT:
                    self.player.moveRight()
                    self.player.turnqt += 1
                elif event.key == p.K_UP:
                    self.player.moveUp()
                    self.player.turnqt += 1
                elif event.key == p.K_DOWN:
                    self.player.moveDown()
                    self.player.turnqt +=1
                elif event.key == p.K_F1:
                    if self.control:
                        self.control = False
                    else:
                        self.control = True
                elif event.key == p.K_F2:
                    self.FPS = 300
                elif event.key == p.K_F3:
                    self.FPS = 15
                elif event.key == p.K_F4:
                    if self.debug:
                        self.debug = False
                    else:
                        self.debug = True

        inputs = self.calcInputs()
        keys   = self.agent.decision(self.calcInputs(debug))
        #keys    = self.player.bestKey(inputs,keys)
        if self.control == True:
            if keys[p.K_UP] and self.player.direction != 3:
                self.player.moveUp()
                self.player.turnqt +=1
            if keys[p.K_DOWN] and self.player.direction != 1:
                self.player.moveDown()
                self.player.turnqt +=1
            if keys[p.K_LEFT] and self.player.direction != 2:
                self.player.moveLeft()
                self.player.turnqt +=1
            if keys[p.K_RIGHT] and self.player.direction != 0:
                self.player.moveRight()
                self.player.turnqt +=1
    """Analisa se a snake saiu da tela"""
    def outScreen(self):
        if (self.player.headX >= self.displayWidth  or
            self.player.headX < 0                  or
            self.player.headY >= self.displayHeight or
            self.player.headY < 0)                 :
           self.gameOver = True
           self.outS     = True
    """Checa a colisão com a maçã"""
    def checkAppleColission(self):
        if (self.player.headX == self.apple.randAppleX and
            self.player.headY == self.apple.randAppleY):
            self.player.snakeLength += 1
            self.player.fome         += 1000
            self.player.pts += 1
            self.apple.randPos(self.displayWidth,self.displayHeight,self.player.snakeList)
    """Debug - Desenha sensor da parade"""
    def drawW(self,vet,c):
        #baixo
        for x in range (0,int(vet[3])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX,self.player.headY+x*self.blockSize,self.blockSize,self.blockSize])

        #cima
        for x in range (0,int(vet[1])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX,(x+1)*self.blockSize,self.blockSize,self.blockSize])

        #direita
        for x in range (0,int(vet[2])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX+x*self.blockSize,self.player.headY,self.blockSize,self.blockSize])

        #esquerda
        for x in range (0,int(vet[0])):
            p.draw.rect(self.gameDisplay,c,[(x+1)*self.blockSize,self.player.headY,self.blockSize,self.blockSize])

        #digaonal cima direita
        for x in range (0,int(vet[4])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX+x*self.blockSize,self.player.headY-x*self.blockSize,self.blockSize,self.blockSize])

        #cima cima esquerda
        for x in range (0,int(vet[5])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX-x*self.blockSize,self.player.headY-x*self.blockSize,self.blockSize,self.blockSize])

        #esquerda baixo direita
        for x in range (0,int(vet[6])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX+x*self.blockSize,self.player.headY+x*self.blockSize,self.blockSize,self.blockSize])

        #esquerda baixo esquerda
        for x in range (0,int(vet[7])):
            p.draw.rect(self.gameDisplay,c,[self.player.headX-x*self.blockSize,self.player.headY+x*self.blockSize,self.blockSize,self.blockSize])
    """Debug - Desenha sensor da maça"""
    def drawA(self,vet):
        #esquerda
        p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX,self.player.headY,self.blockSize*(-vet[0]),self.blockSize])
        #direita
        p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX,self.player.headY,self.blockSize*vet[1],self.blockSize])
        #cima
        p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX,self.player.headY,self.blockSize,self.blockSize*(-vet[2])])
        #baixo
        p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX,self.player.headY,self.blockSize,self.blockSize*vet[3]])

        #cima esquerda
        for x in range(0,int(vet[4])):
            p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX-x*self.blockSize,self.player.headY-x*self.blockSize,self.blockSize,self.blockSize])

        #cima direita
        for x in range (0,int(vet[5])):
            p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX+x*self.blockSize,self.player.headY-x*self.blockSize,self.blockSize,self.blockSize])

        #baixo esquerda
        for x in range (0,int(vet[6])):
            p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX-x*self.blockSize,self.player.headY+x*self.blockSize,self.blockSize,self.blockSize])

        #esquerda baixo direita
        for x in range (0,int(vet[7])):
            p.draw.rect(self.gameDisplay,(255,100,0),[self.player.headX+x*self.blockSize,self.player.headY+x*self.blockSize,self.blockSize,self.blockSize])

    """Desenha sensor do corpo"""
    def drawC(self,vet):
        #esquerda
        p.draw.rect(self.gameDisplay,(0,0,200),[self.player.headX,self.player.headY,self.blockSize*(-vet[0]),self.blockSize])
        #direita
        p.draw.rect(self.gameDisplay,(0,0,200),[self.player.headX,self.player.headY,self.blockSize*(vet[1]+1),self.blockSize])
        #cima
        p.draw.rect(self.gameDisplay,(0,0,200),[self.player.headX,self.player.headY,self.blockSize,self.blockSize*(-vet[2])])
        #baixo
        p.draw.rect(self.gameDisplay,(0,0,200),[self.player.headX,self.player.headY,self.blockSize,self.blockSize*(vet[3]+1)])

    """Calcula vetor de Inputs"""
    def calcInputs(self,debug=False):
        #Parede Normal  -------------------------------------------------------
        posX = self.player.headX
        posY = self.player.headY

        distWDir = (self.displayWidth-posX-self.blockSize)/self.blockSize
        distWEsq = posX/self.blockSize
        distWCim = posY/self.blockSize
        distWBai = (self.displayHeight-posY-self.blockSize)/self.blockSize


        #Parede Diagonal ------------------------------------------------------
        distWCimDir = 0
        distWCimEsq = 0
        distWBaiDir = 0
        distWBaiEsq = 0

        if distWDir >= distWCim:
            distWCimDir = distWCim
        else:
            distWCimDir = distWDir

        if distWEsq >= distWCim:
            distWCimEsq = distWCim
        else:
            distWCimEsq = distWEsq

        if distWDir >= distWBai:
            distWBaiDir = distWBai
        else:
            distWBaiDir = distWDir

        if distWEsq >= distWBai:
            distWBaiEsq = distWBai
        else:
            distWBaiEsq = distWEsq

        #Corpo Normal
        distDir     = 0
        distEsq     = 0
        distCim     = 0
        distBai     = 0

        #Corpo Diagonal
        distCimDir  = 0
        distBaiDir  = 0
        distCimEsq  = 0
        distBaiEsq  = 0


        #Apple Normal
        distADir    = 0
        distAEsq    = 0
        distACim    = 0
        distABai    = 0

        #Apple Diagonal
        distACimDir = 0
        distABaiDir = 0
        distACimEsq = 0
        distABaiEsq = 0


        # NORMAL NORMAL--------------------------------------------------------
        #Dir
        temp2 = 0
        tempX = self.player.headX + self.blockSize
        find  = False
        while tempX < self.displayWidth and not find:
            temp2 += 1
            for c in self.player.snakeList:
                if tempX == c[0] and self.player.headY == c[1]:
                    distDir = temp2
                    find = True
                    break
            tempX += self.blockSize

        #Esq
        temp2 = 0
        tempX = self.player.headX - self.blockSize
        find  = False
        while tempX > 0 and not find:
            temp2 += 1
            for c in self.player.snakeList:
                if tempX == c[0] and self.player.headY == c[1]:
                    distEsq = temp2
                    find = True
                    break
            tempX -= self.blockSize

        #Bai
        temp2 = 0
        tempY = self.player.headY + self.blockSize
        find  = False
        while tempY < self.displayHeight and not find:
            temp2 += 1
            for c in self.player.snakeList:
                if tempY == c[1] and self.player.headX == c[0]:
                    distBai = temp2
                    find = True
                    break
            tempY += self.blockSize
        #Cim
        temp2 = 0
        tempY = self.player.headY - self.blockSize
        find  = False
        while tempY > 0 and not find:
            temp2 += 1
            for c in self.player.snakeList:
                if tempY == c[1] and self.player.headX == c[0]:
                    distCim = temp2
                    find = True
                    break
            tempY -= self.blockSize


        # MAÇA Normal-----------------------------------------------------------
        if self.apple.randAppleY == self.player.headY:
            if self.apple.randAppleX > self.player.headX:
                posX = self.player.headX
                while posX != self.apple.randAppleX:
                    posX += self.blockSize
                    distADir += 1
            if self.apple.randAppleX < self.player.headX:
                posX = self.player.headX
                while posX != self.apple.randAppleX:
                    posX -= self.blockSize
                    distAEsq += 1
        if self.apple.randAppleX == self.player.headX:
            if self.apple.randAppleY > self.player.headY:
                posY = self.player.headY
                while posY != self.apple.randAppleY:
                    posY += self.blockSize
                    distABai += 1
            if self.apple.randAppleY < self.player.headY:
                posY = self.player.headY
                while posY != self.apple.randAppleY:
                    posY -= self.blockSize
                    distACim += 1

        # Maça Diagonal---------------------------------------------------------
        #CimaDir
        if self.apple.randAppleX > self.player.headX and self.apple.randAppleY < self.player.headY:
            posX = self.player.headX
            posY = self.player.headY

            disX = 0
            disY = 0

            while self.apple.randAppleX != posX:
                posX += self.blockSize
                disX += 1
                if posX > self.displayWidth:
                    disX = 0
            while self.apple.randAppleY != posY:
                posY -= self.blockSize
                disY += 1
                if posY < 0:
                    disY = 0
            if disY == disX:
                distACimDir = disY

        #CimEsq
        if self.apple.randAppleX < self.player.headX and self.apple.randAppleY < self.player.headY:
            posX = self.player.headX
            posY = self.player.headY

            disX = 0
            disY = 0

            while self.apple.randAppleX != posX:
                posX -= self.blockSize
                disX += 1
                if posX < 0:
                    disX = 0
            while self.apple.randAppleY != posY:
                posY -= self.blockSize
                disY += 1
                if posY < 0:
                    disY = 0
            if disY == disX:
                distACimEsq = disY

        #BaiDir
        if self.apple.randAppleX > self.player.headX and self.apple.randAppleY > self.player.headY:
            posX = self.player.headX
            posY = self.player.headY

            disX = 0
            disY = 0

            while self.apple.randAppleX != posX:
                posX += self.blockSize
                disX += 1
                if posX > self.displayWidth:
                    disX = 0
            while self.apple.randAppleY != posY:
                posY += self.blockSize
                disY += 1
                if posY > self.displayHeight:
                    disY = 0
            if disY == disX:
                distABaiDir = disY

        #BaiEsq
        if self.apple.randAppleX < self.player.headX and self.apple.randAppleY > self.player.headY:
            posX = self.player.headX
            posY = self.player.headY

            disX = 0
            disY = 0

            while self.apple.randAppleX != posX:
                posX -= self.blockSize
                disX += 1
                if posX < 0:
                    disX = 0

            while self.apple.randAppleY != posY:
                posY += self.blockSize
                disY += 1
                if posY > self.displayHeight:
                    disY = 0
            if disX == disY:
                distABaiEsq = disY

        if self.debug:
            self.drawW([distWEsq,distWCim,distWDir,distWBai,distWCimDir,distWCimEsq,distWBaiDir,distWBaiEsq],(50,50,50))
            self.drawA([distAEsq,distADir,distACim,distABai,distACimEsq,distACimDir,distABaiEsq,distABaiDir])
            self.drawC([distEsq,distDir,distCim,distBai,distCimEsq,distCimDir,distBaiEsq,distBaiDir])

        distAX = (self.player.headX - self.apple.randAppleX)/self.blockSize
        distAY = (self.player.headY - self.apple.randAppleY)/self.blockSize

        return [distWEsq,distWCim,distWDir,distWBai,distWCimEsq,distWCimDir,distWBaiEsq,distWBaiDir,distEsq,distCim,distDir,distBai,distAEsq,distACim,distADir,distABai,distACimEsq,distACimDir,distABaiEsq,distABaiDir,distAX,distAY]

"""Agente que joga o jogo"""
class SmartAgent:

    def __init__(self, network):

        self.net = network

    def decision(self,entries):

        out = self.net.activate(entries)

        list = [
            (p.K_UP,       out[0]),
            (p.K_DOWN,     out[1]),
            (p.K_LEFT,     out[2]),
            (p.K_RIGHT,    out[3]),
        ]
        list.sort(key=lambda x: x[1], reverse=True)

        keys = { x[0]: False for x in list }
        keys[list[0][0]] = True

        return keys

"""Evoluir genoma"""
def eval_genome(genome, config):

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    agent = SmartAgent(net)

    application = SnakeGame(agent)

    max = 3000

    return application.gameLoop()

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config')

#po = neat.Population(config)
po = neat.Checkpointer.restore_checkpoint("neat-checkpoint-11791")
po.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
po.add_reporter(stats)
po.add_reporter(neat.Checkpointer(250))

pe = neat.ParallelEvaluator(1, eval_genome)
winner = po.run(pe.evaluate, 10000)

with open("rede.neat","wb+") as f:
    f.write(pickle.dumps(winner))
