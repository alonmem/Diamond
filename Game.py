import Logic
import Data as BigData
import random
from win32api import GetSystemMetrics
from sets import Set
SizeOfPawn = (42.66666, 24) # relative to screen size
NumberOfPawnsForEachPlayer = 12

class GameHandle(object):
    def __init__(self):
        self.numOfTurns = 0
        self.playerTurn = 0         # 0=Player, 1=CPU
        self.playersPawns = [[],[]]        # each player's pawn location
        self.naturalPawns = []
        self.movingPhase = [False,False]
        self.timesPlaced = [0,0]     # number of times a player placed a pawn
        self.last50 = 0

    def getTurn(self):      # return who's turn it is now. 0 or 1
        if self.playerTurn:
            return 1
        return 0

    def getNumOfTurnes(self):     # number of turnes so far
        return self.numOfTurns

    def moveMade(self):          # after a play has been made, need to update
        self.numOfTurns += 1
        self.last50 += 1
        if not self.movingPhase[self.getTurn()]:
            self.timesPlaced[self.getTurn()] += 1
        if self.timesPlaced[self.getTurn()] == NumberOfPawnsForEachPlayer and not self.movingPhase[self.getTurn()]:
            self.movingPhase[self.getTurn()] = True
        self.playerTurn = not(self.playerTurn)

    def newMoveMade(self, From ,To):    # new move has been made, appends new pawn to array
        if not type(To) == type(5):
            self.playersPawns[self.getTurn()].append(To)

        if not From[0] == -1:
            if  From in self.playersPawns[self.getTurn()]:
                self.playersPawns[self.getTurn()].remove(From)

        self.moveMade()

    def isSpotAvailable(self, spot):     # return if place is available on the board
        if spot[0] == -1:
            return False

        for i in range(0,2):
            for j in self.playersPawns[i]:
                if j == spot[1]:
                    return False
        for i in self.naturalPawns:
            if i == spot[1]:
                return False
        return True

    def isSpotMine(self, spot):        # return if spot is the currents player's pawn  (to know if its a movement turn)
        for j in self.playersPawns[self.getTurn()]:
            if j == spot:
                return True
        return False

    def convertXYtoSpot(self, XY):
        range = 20
        for pos in BigData.relativePositions:  # find where the user clicked
            if abs(XY[0] - int(GetSystemMetrics(0) / pos[1][0])) < range and abs( XY[1] - int(GetSystemMetrics(1) / pos[1][1])) < range:
                clickedOn = (int(GetSystemMetrics(0) / pos[1][0]) - (SizeOfPawn[0] / 2), int(GetSystemMetrics(1) / pos[1][1]) - (SizeOfPawn[1] / 2))
                return (clickedOn,pos[0])

        return (-1,-1)

    def isEaten(self, spot):    # returns True if this spot will get eaten which means the player cant put there a new pawn

        otherTrun = (self.getTurn() + 1) % 2
        count = 0
        triangles = Logic.vertexPartOfTriangle(spot)
        for tri in triangles:
            count = 0
            for i in tri:
                if i == spot:
                    continue

                if i in self.playersPawns[otherTrun]:
                    count += 1
            if count==2:
                return True

        return False

    def isEating(self, spot, oldSpot):
        '''returns True if this spot will eat someone else which can also say that the player cant put there a new pawn (in a placement phase)'''
        if len(self.naturalPawns)==15:  # cannot eat more
            return (False,(-2,-2))


        howManyIate = []  # only 1 allowed

        otherTurn = (self.getTurn() + 1) % 2
        eaten = (-1,-1)
        triangles = Logic.vertexPartOfTriangle(spot)

        for tri in triangles:
            countA = 0
            countB = 0

            for vertex in tri:

                if vertex == spot or vertex == oldSpot:
                    continue

                if vertex in self.playersPawns[otherTurn]:
                    eaten = vertex
                    countA += 1
                if vertex in self.playersPawns[self.getTurn()]:
                    countB +=1
            if countA == 1 and countB == 1:
                howManyIate.append(eaten)

        if len(Set(howManyIate)) == 1:    # if i ate only one (or more but ate the same)
            return (True, howManyIate[0])

        return (False,(-1,-1))

    def isWin(self):    # check if this turn made a win
        for squreSpot in BigData.UpperLeftOfSquars:
            a = self.PawnBelongsTo(squreSpot)
            b = self.PawnBelongsTo((squreSpot[0],squreSpot[1] + 1))
            c = self.PawnBelongsTo((chr(ord(squreSpot[0]) - 1),squreSpot[1]))
            d = self.PawnBelongsTo((chr(ord(squreSpot[0]) - 1),squreSpot[1] +1 ))

            if a == b and c == d and b == c and a != -1:
                return True
        return False

    def spotPartOfSquere(self, spot, squreSpot):    # check if a spot is a part of a square

        a = squreSpot
        b = (squreSpot[0],squreSpot[1] + 1)
        c = (chr(ord(squreSpot[0]) - 1),squreSpot[1])
        d = (chr(ord(squreSpot[0]) - 1),squreSpot[1] +1 )

        if (a == spot or c == spot or b == spot or d== spot):
            return True

        return False

    def squaresPawns(self, squreSpot):
        ''' Will return the number of pawns is a square for each player '''
        a = []
        Player = 0
        CPU = 0
        a.append(self.PawnBelongsTo(squreSpot))
        a.append(self.PawnBelongsTo((squreSpot[0], squreSpot[1] + 1)))
        a.append(self.PawnBelongsTo((chr(ord(squreSpot[0]) - 1), squreSpot[1])))
        a.append(self.PawnBelongsTo((chr(ord(squreSpot[0]) - 1), squreSpot[1] + 1)))

        for i in a:
            if i==1:
                CPU+=1
            if i==0:
                Player+=1

        return (Player,CPU)

    def pawnEaten(self, eaten):
        self.naturalPawns.append(eaten)
        self.playersPawns[1].remove(eaten)

    def pawnEatenByCPU(self, eaten):
        self.naturalPawns.append(eaten)
        self.playersPawns[0].remove(eaten)

    def convertPointTOXY(self,spot):
        pos = 0
        rel = 0
        for i in BigData.positions:
            if i[0]==spot:
                pos = i[1]
        for i in BigData.relativePositions:
            if i[0]==spot:
                rel = i[1]

        return self.convertXYtoSpot((GetSystemMetrics(0) / rel[0], GetSystemMetrics(1)/rel[1]))[0]

    def printPlayerPawns(self):    # only for debugging, delete later
        print ""
        print ""
        print ""
        for i in self.playersPawns:
            for j in i:
                print j
            print ""
        print ""
        print ""
        print ""

    def PawnBelongsTo(self, pawn):
        for i in xrange(0,2):
            for j in self.playersPawns[i]:
                if j == pawn:
                    return i
        for i in self.naturalPawns:
            if i == pawn:
                return 55   # it is natural

        return -1       # does not belong to anyone

    def clickedOnNatural(self, spot):
        if spot in self.naturalPawns:
            return True
        return False

    def removeNatural(self, spot):
        self.naturalPawns.remove(spot)

    def canRemoveNatural(self, spot):    # check if natural point has a black or white adjacent to it
        for i in BigData.board[spot]:
            if i in self.playersPawns[0] or i in self.playersPawns[1]:
                return False
        return True

    def pawnCanMove(self, spot):        # check if pawn in spot has where to move
        for i in BigData.board[spot]:
            if self.isSpotAvailable((0,i)):
                return True
        return False

    def allPawnsCantMove(self):      # checks if all pawns cant move
        for i in self.playersPawns[self.getTurn()]:
            if self.pawnCanMove(i):
                return False
        return True

    def winORdraw(self):
        gameFinished = (False, -1)

        if self.last50 == 50:
            gameFinished = (True, "Draw")

        if self.isWin():  # check if win
            gameFinished = (True, (self.getTurn()+1)%2)

        if self.allPawnsCantMove() and self.movingPhase[0] and self.movingPhase[1]:
            gameFinished = (True, "Draw")

        if ( len(self.playersPawns[0]) == 0 or len(self.playersPawns[1])==0 ) and self.movingPhase[0] and self.movingPhase[1]:    # if one of the players has not more pawns, its a draw
            gameFinished = (True, "Draw")

        if gameFinished[0]:
            # check who won or if a draw
            if gameFinished[1] == "Draw":
                print "DRAW!"
            else:
                if gameFinished[1] == 0:
                    print "player WON!!!"
                else:
                    print "CPU WON!!!"

        return gameFinished

    def winORdrawMC(self):
        '''same as winORdraw but called only for MonteCarlo'''
        gameFinished = (False, -1)

        if self.last50 == 50:
            gameFinished = (True, 2)

        if self.isWin():  # check if win and returns the player who won (previous player that played)
            gameFinished = (True, (self.getTurn() + 1) % 2)

        if self.allPawnsCantMove() and self.movingPhase[0] and self.movingPhase[1]:
            gameFinished = (True, 2)

        if (len(self.playersPawns[0]) == 0 or len(self.playersPawns[1]) == 0) and self.movingPhase[0] and \
                self.movingPhase[1]:  # if one of the players has not more pawns, its a draw
            gameFinished = (True, 2)

        return gameFinished

    def updateLast50(self):
        self.last50 = 0

    def threePawnsInSquare(self, Player):
        '''This function will return an array with all the spots that Player need to win'''

        L = []  # spots for win

        for square in BigData.UpperLeftOfSquars:
            x = self.squaresPawns(square)       # number of my pawns and number of other player
            if (x[Player] == 3) and ( x[(Player+1)%2] == 0 ):
                L.append( (self.squareEmptySpots(square), square ))

        return L

    def squareBelongsToMe(self, Player):
        '''Will return a array of all the empty spots of a square that belongs to me'''
        L = []  # spots that belong to me

        for square in BigData.UpperLeftOfSquars:
            x = self.squaresPawns(square)  # number of my pawns and number of other player
            if (x[Player] == 2) and (x[(Player + 1) % 2] == 0):
                L.append((self.squareEmptySpots(square) , square))

        if len(L) != 0:
            return L


        for square in BigData.UpperLeftOfSquars:
            x = self.squaresPawns(square)  # number of my pawns and number of other player
            if (x[Player] == 1) and (x[(Player + 1) % 2] == 0):
                L.append((self.squareEmptySpots(square) , square))

        if len(L) != 0:
            return L

        return []

    def squareEmptySpots(self, spot):

        '''This function will return the empty spot of a square with 3 pawns'''
        empty = []
        a = spot
        b = (spot[0], spot[1] + 1)
        c = (chr(ord(spot[0]) - 1), spot[1])
        d = (chr(ord(spot[0]) - 1), spot[1] + 1)

        if self.PawnBelongsTo(a) == -1:
            empty.append(a)
        if self.PawnBelongsTo(b) == -1:
            empty.append(b)
        if self.PawnBelongsTo(c) == -1:
            empty.append(c)
        if self.PawnBelongsTo(d) == -1:
            empty.append(d)

        if len(empty) == 1:
            return  empty[0]

        return empty

    def CanPlacePawn(self, spot):
        ''' Will return if a pawn can be placed'''

        if self.isSpotAvailable(spot):  # spot Available
            if self.isEaten(spot[1]):  # cant put it because it will be eaten
                return False

            if self.isEating(spot[1], (-1,-1))[0]:  # cant put it because it will eat (not allowed in placement phase)
                return False

        else: # spot not Available
            return False

        return True

    def getCloseQuarter(self,spot):
        x = ord(spot[0]) - 96
        y = spot[1]

        q = 0
        if x<5 :
            if y<5:
                q = 1
            if y>5:
                q=2
        else:
            if y<5:
                q=3
            else:
                q = 4

        if q == 1:
            return ( (-1,-1), (chr(random.randint(2,4)+96), (random.randint(4,7)) ) )
        if q==2:
            return ( (-1,-1), (chr(random.randint(4,7)+96), (random.randint(4,7)) ) )
        if q==3:
            return ( (-1,-1), (chr(random.randint(2,4)+96), (random.randint(2,4)) ) )

        return ( (-1,-1), (chr(random.randint(4,7)+96), (random.randint(2,4)) ) )


    # ------------------------------------------------------- AI ----------------------------------------------------- #

    def possibleCpuMoving(self):
        '''This function will return the possible moving spots for the CPU'''
        possible = []
        for i in BigData.board.keys():
            if self.PawnBelongsTo(i) == self.getTurn():
                for neighbor in BigData.board[i]:
                    if self.PawnBelongsTo(neighbor) == -1:
                        possible.append((i,neighbor))

        return possible

    def possibleCpuPlacement(self):
        '''This function will return the possible placement spots for the CPU'''
        possible = []
        for i in BigData.board.keys():
            if self.PawnBelongsTo(i) == -1:
                possible.append( ((-1,-1),i) )

        return possible

    def getPossibleMoves(self):
        ''' This function will return all the possible moves '''
        if self.movingPhase[self.getTurn()] == False:
            return self.possibleCpuPlacement()
        return self.possibleCpuMoving()

    def getBlockingMoves(self):
        '''This function will return the blocking moves'''
        Blocking = []

        for spot in self.threePawnsInSquare( ((self.getTurn()+1)%2) ):
            for move in self.getPossibleMoves():
                if spot[0] == move[1]:
                    Blocking.append(move)

        return Blocking

    def getWinningMoves(self):
        '''This function will return the winning moves'''
        winning = []

        for i in self.threePawnsInSquare(self.getTurn()):
            for move in self.getPossibleMoves():
                if i[0] == move[1]:
                    if self.spotPartOfSquere(move[0], i[1]) == False:
                        winning.append(move)

        return winning

    def getMySquares(self):
        '''returns the moves that add to my squars'''
        addToMySquares = []

        for i in self.squareBelongsToMe(self.getTurn()):
            for spot in i[0]:
                for move in self.getPossibleMoves():
                    if spot == move[1]:
                        if self.spotPartOfSquere(move[0], i[1]) == False:
                            addToMySquares.append(move)

        return addToMySquares

    def getEatingMoves(self):
        '''returns all the moves that eat'''
        eating = []

        for move in self.getPossibleMoves():
            if self.isEating(move[1], move[0])[0] == True:
                if self.movingPhase[self.getTurn()] == True:
                    eating.append(move)

        return eating

    def removeNaturalMoves(self):
        '''returns all the moves that remove a natural pawn'''
        remove = []

        for pawn in self.naturalPawns:
            if self.canRemoveNatural(pawn) == True:
                remove.append(pawn)

        return remove
