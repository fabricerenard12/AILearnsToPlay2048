from Game import *
import multiprocessing as mp

def randomMove(game):
    i = random.randint(0, 3)
    if i == 0 and game.checkLeft():
        game.moveLeft()
    elif i == 1 and game.checkRight():
        game.moveRight()
    elif i == 2 and game.checkUp():
        game.moveUp()
    elif i == 3 and game.checkDown():
        game.moveDown()

def bestMove(index, game):
    if index == 0:
        return game.moveLeft()
    elif index == 1:
        return game.moveRight()
    elif index == 2:
        return game.moveUp()
    elif index == 3:
        return game.moveDown()

def simulation(gameObj, iterations, i, score = 0):
    simulation = copy.deepcopy(gameObj)
    if i % 4 == 0:
        simulation.moveLeft()
        for _ in range(iterations):
            randomMove(simulation)
        score = simulation.getScore()
    elif i % 4 == 1:
        simulation.moveRight()
        for _ in range(iterations):
            randomMove(simulation)
        score = simulation.getScore()
    elif i % 4 == 2:
        simulation.moveUp()
        for _ in range(iterations):
            randomMove(simulation)
        score = simulation.getScore()
    elif i % 4 == 3:
        simulation.moveDown()
        for _ in range(iterations):
            randomMove(simulation)
        score = simulation.getScore()

    return score

def compute(gameObj, numberOfsimulations, iterations):
    scoresLeft = []
    scoresRight = []
    scoresUp = []
    scoresDown = []
    p = mp.Pool(mp.cpu_count())

    for i in range(4):
        for _ in range(numberOfsimulations):
            if i == 0:
                p.apply_async(simulation, args=(gameObj, iterations, i), callback = lambda x: scoresLeft.append(x))
            elif i == 1:
                p.apply_async(simulation, args=(gameObj, iterations, i), callback = lambda x: scoresRight.append(x))
            elif i == 2:
                p.apply_async(simulation, args=(gameObj, iterations, i), callback = lambda x: scoresUp.append(x))
            elif i == 3:
                p.apply_async(simulation, args=(gameObj, iterations, i), callback = lambda x: scoresDown.append(x))
    p.close()
    p.join()

    return np.array((np.average(scoresLeft), np.average(scoresRight), np.average(scoresUp), np.average(scoresDown)), dtype = float)

#-------------------------------------------------------------
print("Number of cpus : ", mp.cpu_count())
numberOfSimulations = int(input('Number of simulations?\n'))
iterations = int(input('Number of iterations (moves per game)?\n'))

g = Game(4)
while g.getGameStatus():
    g.setGameStatus(g.checkGameStatus())
    print(f'Game:\n{g.getMatrix()}')
    g.setMatrix(bestMove(np.argmax(compute(g, numberOfSimulations, iterations)), g))
    