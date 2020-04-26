import snake
import pygame as p
class OpSnake(snake.Snake):
    """
    [0-3]
    00 distWEsq,
    01 distWCim,
    02 distWDir,
    03 distWBai,
    [4-7]
    04 distWCimEsq,
    05 distWCimDir,
    06 distWBaiEsq,
    07 distWBaiDir
    [8-11]
    08 distEsq,
    09 distCim,
    10 distDir,
    11 distBai
    [12-15]
    12 distAEsq,
    13 distACim,
    14 distADir,
    15 distABai
    [16-19]
    16 distACimEsq,
    17 distACimDir,
    18 distABaiEsq,
    19 distABaiDir,
    [20-21]
    20 distAX,
    21 distAY
    """
    def bestKey(self,inputs,keys):
        def setFalse(keys):
            keys[p.K_UP]    = False
            keys[p.K_DOWN]  = False
            keys[p.K_LEFT]  = False
            keys[p.K_RIGHT] = False
            return keys

        """
        [0-3]
        00 distWEsq,
        01 distWCim,
        02 distWDir,
        03 distWBai,
        [8-11]
        08 distEsq,
        09 distCim,
        10 distDir,
        11 distBai
        """
        # ------------------ Quinas
        # Esquerda Cima
        if inputs[0] == 0 and inputs[1] == 0:
            keys = setFalse(keys)
            # Dir Livre
            if inputs[10] == 0:
                keys[p.K_RIGHT] = True
                return keys
            # Bai Livre
            elif inputs[11] == 0:
                keys[p.K_DOWN] = True
                return keys

        # Esquerda Baixo
        if inputs[0] == 0 and inputs[3] == 0:
            keys = setFalse(keys)
            # Esq Livre
            if inputs[8] == 0:
                keys[p.K_LEFT] = True
                return keys
            # Cim Livre
            elif inputs[9] == 0:
                keys[p.K_UP] = True
                return keys

        # Dir Cima
        if inputs[2] == 0 and inputs[1] == 0:
            keys = setFalse(keys)
            # Esq Livre
            if inputs[8] == 0:
                keys[p.K_LEFT] = True
                return keys
            # Bai Livre
            elif inputs[11] == 0:
                keys[p.K_DOWN] = True
                return keys

        # Dir Bai
        if inputs[2] == 0 and inputs[3] == 0:
            keys = setFalse(keys)
            # Esq Livre
            if inputs[8] == 0:
                keys[p.K_LEFT] = True
                return
            # Cim Livre
            elif inputs[9] == 0:
                keys[p.K_UP] = True
                return keys
        """
        [0-3]
        00 distWEsq,
        01 distWCim,
        02 distWDir,
        03 distWBai,
        [8-11]
        08 distEsq,
        09 distCim,
        10 distDir,
        11 distBai
        """
        # ---------Paredes
        # Esq
        if inputs[0] == 0:
            keys = setFalse(keys)
            if inputs[9] == 0 or inputs[9] > inputs[11]:
                keys[p.K_UP] = True
            elif inputs[11] == 0 or inputs[11] > inputs[9]:
                keys[p.K_DOWN] = True




        return keys
