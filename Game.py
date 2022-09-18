import numpy as np
import random
import copy

class Game:
    startingTiles = [2, 4]
    distribution = [0.9, 0.1]

    def __init__(self, size):
        self.size = size
        self.matrix = np.zeros((size, size), dtype=int)
        self.gameStatus = False
        self.score = 0
        self.addTwoInitialTilesToMatrix()

    def addTwoInitialTilesToMatrix(self):
        firstTile = random.choices(self.startingTiles, self.distribution)[0]
        positionFirstTile = (random.randint(0, 3), random.randint(0, 3))
        self.setMatrixEntry(firstTile, positionFirstTile)

        secondTile = random.choices(self.startingTiles, self.distribution)[0]
        positionSecondTile = (random.randint(0, 3), random.randint(0, 3))
        while positionFirstTile == positionSecondTile:
            positionSecondTile = (random.randint(0, 3), random.randint(0, 3))
        self.setMatrixEntry(secondTile, positionSecondTile)
        self.setGameStatus(True)

    def getSize(self):
        return self.size

    def getMatrix(self):
        return self.matrix

    def getScore(self):
        return self.score

    def getGameStatus(self):
        return self.gameStatus

    def setMatrix(self, matrix):
        self.matrix = matrix

    def setMatrixEntry(self, value: 'int', position: 'tuple'):
        self.matrix[position[0], position[1]] = value

    def setScore(self, value):
        self.score = value

    def setGameStatus(self, status: 'bool'):
        self.gameStatus = status

    def checkGameStatus(self):
        if self.checkLeft() or self.checkRight() or self.checkUp() or self.checkDown():
            return True
        return False

    def checkWin(self):
        for i in self.getMatrix():
            for j in i:
                if j == 2048:
                    return 'You won!'
        return 'You lost!'

    def flipMatrix(self):
        return np.fliplr(self.getMatrix())

    def transposeMatrix(self):
        return np.transpose(self.getMatrix())

    def compress(self):
        changed = False
        newMatrix = np.zeros((self.getSize(), self.getSize()), dtype=int)

        for i, row in enumerate(self.getMatrix()):
            position = 0
            for j, tile in enumerate(row):
                if tile != 0:
                    newMatrix[i, position] = tile
                    if j != position:
                        changed = True
                    position += 1

        return newMatrix, changed

    def merge(self):
        changed = False
        score = self.getScore()
        newMatrix = np.copy(self.getMatrix())

        for i, row in enumerate(self.getMatrix()):
            for j, tile in enumerate(row):
                nextTile = 0
                if j < len(row) - 1:
                    nextTile = int(row[j + 1])
                if tile == nextTile and tile != 0:
                    self.setScore(self.getScore() + tile * 2)
                    newMatrix[i, j] = tile * 2
                    newMatrix[i, j + 1] = 0
                    changed = True

        return newMatrix, changed

    def addTile(self):
        newMatrix = np.copy(self.getMatrix())
        changed = False

        if np.count_nonzero(self.getMatrix()) == (self.getSize() * self.getSize()):
            return newMatrix, changed

        tile = random.choices(self.startingTiles, self.distribution)[0]
        positionTile = (random.randint(0, 3), random.randint(0, 3))

        while newMatrix[positionTile[0]][positionTile[1]] != 0:
            positionTile = (random.randint(0, 3), random.randint(0, 3))
        newMatrix[positionTile] = tile

        changed = True
        return newMatrix, changed

    def moveLeft(self):
        self.setMatrix(self.compress()[0])
        self.setMatrix(self.merge()[0])
        self.setMatrix(self.compress()[0])
        self.setMatrix(self.addTile()[0])
        return self.getMatrix()

    def moveRight(self):
        self.setMatrix(self.flipMatrix())
        self.setMatrix(self.moveLeft())
        self.setMatrix(self.flipMatrix())
        return self.getMatrix()

    def moveUp(self):
        self.setMatrix(self.transposeMatrix())
        self.setMatrix(self.moveLeft())
        self.setMatrix(self.transposeMatrix())
        return self.getMatrix()

    def moveDown(self):
        self.setMatrix(self.transposeMatrix())
        self.setMatrix(self.moveRight())
        self.setMatrix(self.transposeMatrix())
        return self.getMatrix()

    def checkLeft(self):
        matrix = copy.deepcopy(self)
        if matrix.compress()[1] or matrix.merge()[1]:
            return True
        return False

    def checkRight(self):
        matrix = copy.deepcopy(self)
        matrix.setMatrix(matrix.flipMatrix())
        if matrix.checkLeft():
            return True
        return False

    def checkUp(self):
        matrix = copy.deepcopy(self)
        matrix.setMatrix(matrix.transposeMatrix())
        if matrix.checkLeft():
            return True
        return False

    def checkDown(self):
        matrix = copy.deepcopy(self)
        matrix.setMatrix(matrix.transposeMatrix())
        if matrix.checkRight():
            return True
        return False
