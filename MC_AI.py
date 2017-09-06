import math
import random
import copy
import Logic
import Data as BigData
from sets import Set

class Node():
    Player = 0          # the player's turn
    parent = None       # parent of the node
    children = []       # children of this node
    wins = 0.0          # number of games won from this position
    plays = 0.0         # total number of games played from this position
    gameHandler = None  # state of game at this node's board (gameHandler)
    move = None         # move that broght me here

    def __init__(self, _gameState, _parent, _move=None, win=0, played=0):
        self.children = []
        self.playerNum = _gameState.getTurn()
        self.gameHandler = copy.deepcopy(_gameState)

        self.parent = _parent
        self.wins = win
        self.plays = played
        self.move = _move


    def GetValueOfNode(self):
        ''' This function will return the value of a node based on his simulation'''
        return ( (float(self.wins)/float(self.plays)) + math.sqrt(1.7)*math.sqrt( math.log(self.parent.plays, math.e) / self.plays) )

        # if I dont want to use the formula:
        #return (float(self.wins)/float(self.plays))

    def RollOut(self):
        ''' Plays a random game from this node and Backpropagates to the top '''

        tempGame = copy.deepcopy(self.gameHandler)

        while (tempGame.winORdrawMC()[0] == False):   # while the game is not finished
            allPossibleMoves = tempGame.getPossibleMoves()  # all the possible moves
            possibleMoves = moveForRollOut(tempGame)        # moves that MoveForRollOut returned

            if len(possibleMoves) == 0:
                randomMove = random.choice(allPossibleMoves)
                while tempGame.CanPlacePawn(randomMove) == False:
                    randomMove = random.choice(allPossibleMoves)
            else:
                randomMove = random.choice(possibleMoves)

            tempGame.newMoveMade(randomMove[0], randomMove[1])  # make new move in the temporary game


        won = tempGame.winORdrawMC()[1]     # remember who won

        currnentNode = self

        # Backpropagation:
        while currnentNode!= None:
            currnentNode.plays+=1

            if currnentNode.gameHandler.getTurn() == won:   # if this is the player who won
                currnentNode.wins+=1

            if won == 2:    #draw
                currnentNode.wins+=0.5

            currnentNode = currnentNode.parent  # go up in the tree



def MonteCarlo(node):
    ''' Monte Carlo Tree Search for a given node '''

    if (node.gameHandler.winORdrawMC()[0] == True):   # game is finished, need to roll out
        node.RollOut()
        return

    if len(node.children)==0:    # if im a leaf, selection is finished, need to expand
        moves = expansionPolicy(node)   # moves from expansion policy

        for i in xrange(len(moves)):    # create node for each child
            newGameState = copy.deepcopy(node.gameHandler)
            newGameState.newMoveMade(moves[i][0], moves[i][1])  # make temp move

            newChild = Node( newGameState, node, moves[i])  # creating new child node
            node.children.append(newChild)
            newChild.RollOut()  # will preform a simulation and Backpropagation



    else: # selection
        ''' The policy for the selection, is to go to the max valued child'''
        maxValue = -1.
        maxChild = None
        for child in node.children:
            if child.GetValueOfNode() > maxValue:
                maxValue = child.GetValueOfNode()
                maxChild = child

        # at this point, we have the max child, so we will continue the monte carlo from him
        MonteCarlo(maxChild)

def getMoveAI(gameHandler):
    '''this function gets a GameHandle object and will return the best move for the CPU'''
    numberOfRounds = 20
    root = Node( gameHandler, None)

    for i in xrange(numberOfRounds):    # run Monte Carlo (numberOfRounds) times
        MonteCarlo(root)

    # find best move:
    maxValue = -1
    bestMove = None
    for child in root.children:

        if (child.GetValueOfNode() > maxValue):
            maxValue = child.GetValueOfNode()
            bestMove = child.move

    return bestMove



# --------------- Policies --------------- #

def expansionPolicy(node):
    ''' The expansion policy for the expansion move, returns a list with the possible moves'''

    if node.gameHandler.numOfTurns == 1:
        a = []
        a.append(node.gameHandler.getCloseQuarter(node.gameHandler.playersPawns[0][0]))
        return a

    allPossibleMoves = copy.deepcopy(node.gameHandler.getPossibleMoves())   # all the possible moves
    blockingMoves = node.gameHandler.getBlockingMoves()                     # moves that block the other player's win
    winningMoves = node.gameHandler.getWinningMoves()
    eatingMoves = node.gameHandler.getEatingMoves()

    moves = []

    if len(winningMoves) != 0:     # if I have moves that win
        return winningMoves

    if len(blockingMoves) != 0:     # if I have moves to block
        return blockingMoves

    if len(eatingMoves) != 0:  # if I have moves that eat
        return eatingMoves

    for i in node.gameHandler.getMySquares():   #  moves that add to my square
        moves.append(i)


    if len(moves)!=0:
        for i in moves:  # remove illegal moves
            if (node.gameHandler.movingPhase[node.gameHandler.getTurn()] == False and node.gameHandler.CanPlacePawn(i) == False) or type(i[0]) == type('str'):
                moves.remove(i)

        if len(moves) > 5:
            random.shuffle(moves)
            moves =  moves[:5]

        return moves

    for i in allPossibleMoves:  # remove illegal moves
        if node.gameHandler.movingPhase[node.gameHandler.getTurn()] == False and node.gameHandler.CanPlacePawn(i) == False:
            allPossibleMoves.remove(i)

    if len(allPossibleMoves) > 5:
        random.shuffle(allPossibleMoves)
        return allPossibleMoves[:5]

    return allPossibleMoves

def moveForRollOut(gameHandler):
    # same as Expansion policy:

    allPossibleMoves = copy.deepcopy(gameHandler.getPossibleMoves())   # all the possible moves
    blockingMoves = gameHandler.getBlockingMoves()                     # moves that block the other player's win
    winningMoves = gameHandler.getWinningMoves()
    eatingMoves = gameHandler.getEatingMoves()
    removeNatual = gameHandler.removeNaturalMoves()

    moves = []

    if len(winningMoves) != 0:     # if I have moves that win
        return winningMoves

    if len(blockingMoves) != 0:     # if I have moves to block
        return blockingMoves

    if len(removeNatual) != 0:     # if I can remove a natural pawn
        return removeNatual

    if len(eatingMoves) != 0:  # if I have moves that eat
        return eatingMoves

    for i in gameHandler.getMySquares():   #  moves that add to my square
        moves.append(i)

    for i in moves:     # remove illegal moves
        if gameHandler.movingPhase[gameHandler.getTurn()] == False and gameHandler.CanPlacePawn(i) == False:
            moves.remove(i)

    if len(moves)!=0:
        if len(moves) > 5:
            random.shuffle(moves)
            return moves[:5]

        return moves

    for i in allPossibleMoves:  # remove illegal moves
        if (gameHandler.movingPhase[gameHandler.getTurn()] == False and gameHandler.CanPlacePawn(i) == False) or type(i) == type('str'):
            allPossibleMoves.remove(i)

    if len(allPossibleMoves) > 5:
        random.shuffle(allPossibleMoves)
        return allPossibleMoves[:5]

    return allPossibleMoves
