from kivy.app import App
from  kivy.uix.floatlayout import FloatLayout
from  kivy.uix.button import Button
from  kivy.uix.label import Label
from  kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *
from win32api import GetSystemMetrics
import Data as BigData
from Game import GameHandle
import Logic
import random
import MC_AI
import time
from threading import Thread

positions = BigData.relativePositions
SizeOfPawn = (42.66666, 24) # relative to screen size

class DiamondGame(Screen):
    def __init__(self, **kwargs):
        self.gameHandler = GameHandle()             # instance of GameHandle
        self.pawns = []                             # an array of the pawn. presented by (('a', 4), eclipse)
        self.gameFinished = (False, -1)             # tuple that indicates whether the game finished and by who
        self.waitingForMove = [False, (-1,-1)]      # if waiting for new move, what pawn do i move

        super(DiamondGame, self).__init__(**kwargs)

        with self.canvas:   # create game background
            size = (GetSystemMetrics(0) / 2, GetSystemMetrics(1))
            Rectangle(source="DiamondBoard.jpg", size=size)

        with self.canvas:   # create text background
            size = (GetSystemMetrics(0) / 2, GetSystemMetrics(1))
            Rectangle(source="white.png", size=size, pos = (size[0], 0))

        self.notifications = Label(markup=True, pos_hint={'center_x': .6, 'center_y': .3},
                                   size_hint=(None, None), font_size = 18)
        self.notifications.text += "[color=0]Game Started, Good Luck!\n[/color]"

        self.add_widget(self.notifications)

        self.cancelMoving = Button(text="Cancel", on_press=lambda a: self.cancelMove(),
                           pos_hint={'center_x': .07, 'center_y': .07}, size_hint=(None, None), width=100, font_size=25,
                           height=50)
        self.cancelMoving.disabled = True
        self.cancelMoving.opacity = 0

        self.add_widget(self.cancelMoving)

    def on_touch_down(self, touch):
        super(DiamondGame, self).on_touch_down(touch)

        if self.gameFinished[0]:    # if game is finished we dont need to get a click
            self.notifications.text += "[color=0]" + str(self.gameFinished[1])+" WON!\n[/color]"
            return

        if self.gameHandler.getTurn() == 1:    # CPU turn
            return

        clickedOn = self.gameHandler.convertXYtoSpot((touch.x, touch.y))  # clickedOn: [0] = (x,y) , [1] = ('a',4)
        if clickedOn == (-1,-1):   # clicked spot not available
            return

        if self.gameHandler.movingPhase[self.gameHandler.getTurn()]:  # it is a moving phase
            return self.ClickedMovingPhase(clickedOn, (-1,-1))
        else:
            return self.ClickedPlacementPhase(clickedOn)

    def CPUturn(self):
        '''will call the Clicked functions with the CPU's move'''

        if self.gameHandler.movingPhase[1]:         # its a moving phase
            spot = self.CPUmovingPhase()        # spot[0] will move to spot[1]
            XYold = self.gameHandler.convertPointTOXY(spot[0])
            XYnew = self.gameHandler.convertPointTOXY(spot[1])
            return self.ClickedMovingPhase( (XYold,spot[0]), (XYnew,spot[1]) )          # send ( (XYspot,spot), (XYnew,newSpot) )


        else:                                       # its a placement phase
            spot = self.CPUplacementPhase()[1]
            XYspot = self.gameHandler.convertPointTOXY(spot)
            return self.ClickedPlacementPhase( (XYspot,spot) )

    def createNewPawn(self, spot, natural):
        '''This function will create a new pawn'''
        elipse = None

        if not natural:
            with self.canvas:
                Color(self.gameHandler.getTurn(), self.gameHandler.getTurn(), self.gameHandler.getTurn())
                elipse = Ellipse(pos=spot[0], size=(GetSystemMetrics(0) / SizeOfPawn[0], GetSystemMetrics(1) / SizeOfPawn[1]))
        else:
            with self.canvas:
                Color(1, 0, 0, 1)
                elipse = Ellipse(pos=spot[0], size=(GetSystemMetrics(0) / SizeOfPawn[0], GetSystemMetrics(1) / SizeOfPawn[1]))

        self.pawns.append((spot[1], elipse))

    def DeleteExistingPawn(self, pawn):
        '''This function will delete a pawn'''
        for i in self.pawns:                # find the pawn and delete him
            if i[0] == pawn:                # if this is the pawn i need to delete
                self.canvas.remove(i[1])
                self.pawns.remove(i)
                return

    def ClickedMovingPhase(self, clickedOn, CPUmove):
        '''if a player or the CPU made a move and its a moving phase'''

        if CPUmove!= (-1,-1):         # CPU selected move

            if not self.waitingForMove[0] and self.gameHandler.clickedOnNatural(clickedOn[1]):  # if player chose to remove a natural pawn
                print "CPU removed a Neutral pawn"
                self.notifications.text += "[color=0]CPU removed a Neutral pawn\n[/color]"
                self.DeleteExistingPawn(clickedOn[1])
                self.gameHandler.removeNatural(clickedOn[1])
                self.gameHandler.updateLast50()
                # move finished
                self.gameHandler.newMoveMade(self.waitingForMove[1], clickedOn[1])
                self.waitingForMove = [False, (-1, -1)]
                return


            # create new pawn and delete old one:
            if self.gameHandler.isEaten(CPUmove[1]):
                print "CPU preformed a Safe Move!"
                self.notifications.text += "[color=0]CPU preformed a Safe Move!\n[/color]"

            self.DeleteExistingPawn(clickedOn[1])  # delete old pawn
            self.createNewPawn(CPUmove, False) # create new pawn

            #check if eating:
            eating = self.gameHandler.isEating(CPUmove[1], clickedOn[1])  # get if a pawn is eating


            if eating[0] and self.gameFinished[0]== False:  # if so
                self.gameHandler.pawnEatenByCPU(eating[1])  # add to natural pawns
                print "CPU ate ", eating[1]
                self.notifications.text += "[color=0]CPU ate " + str(eating[1])+ "\n[/color]"

                self.DeleteExistingPawn(eating[1])  # delete the eaten pawns
                if len(self.gameHandler.playersPawns[0])==0:
                    self.gameFinished = (True, 1)
                self.createNewPawn((self.gameHandler.convertPointTOXY(eating[1]), eating[1]), True)  # create natural point
                self.gameHandler.updateLast50()


            print "CPU moved " , clickedOn[1], " to " , CPUmove[1]
            print ""
            self.notifications.text += "[color=0]CPU moved "+ str(clickedOn[1]) +" to "+ str(CPUmove[1]) + "\n[/color]"

            # move finished, call newMoveMade:
            self.gameHandler.newMoveMade(clickedOn[1], CPUmove[1])
            self.gameFinished = self.gameHandler.winORdraw()
            self.waitingForMove = [False, (-1, -1)]

            return

        moveFinished = False

        if not self.waitingForMove[0] and self.gameHandler.clickedOnNatural(clickedOn[1]):     # if player chose to remove a natural pawn
            if self.gameHandler.canRemoveNatural(clickedOn[1]):
                print "Player removed a Neutral pawn"
                self.notifications.text += "Player removed a Neutral Pawn\n[/color]"

                self.DeleteExistingPawn(clickedOn[1])
                self.gameHandler.removeNatural(clickedOn[1])
                self.gameHandler.updateLast50()
                # move finished
                self.gameHandler.newMoveMade(self.waitingForMove[1], clickedOn[1])
                self.waitingForMove = [False, (-1, -1)]
                return
            else:
                print "can not remove a Neutral pawn if adjacent to a black or white pawn"
                return

        if self.gameHandler.isSpotMine(clickedOn[1]) and not self.waitingForMove[0]:  # it is my pawn in that spot and we are not waiting to move
            if not self.gameHandler.pawnCanMove(clickedOn[1]):      # no where to move
                print "ERROR: No where to move, please select a different pawn !"
                return
            print "you chose to move ", clickedOn[1]
            print "now select where you want to move"

            self.notifications.text += "[color=0]Player selected: " + str(clickedOn[1]) +"\n[/color]"

            self.waitingForMove = [True, clickedOn[1]]
            self.cancelMoving.disabled = False
            self.cancelMoving.opacity = 1
            return

        if self.gameHandler.isSpotAvailable(clickedOn) and self.waitingForMove[0]:                          # spot Available: (and waiting for move)
                if self.CanMoveAtoB(self.waitingForMove[1], clickedOn[1]):       # if move is ok
                    if self.gameHandler.isEaten(clickedOn[1]):
                        print "Player ", self.gameHandler.getTurn(), " preformed a Safe Move!"
                        self.notifications.text += "[color=0]Player preformed a Safe Move!\n[/color]"
                    self.DeleteExistingPawn(self.waitingForMove[1])              # delete old pawn
                    self.createNewPawn(clickedOn, False)                         # create new pawn
                    moveFinished = True

        else:       # spot not available or not waiting for move
            if not self.waitingForMove[0]:     # waiting for player to select where to go but spot not available
                print "ERROR: please select one of your pawns"

            if not self.gameHandler.isSpotAvailable(clickedOn):
                print "ERROR: spot not available!"

            return


        if moveFinished:
            self.cancelMoving.disabled = True
            self.cancelMoving.opacity = 0
            eating = self.gameHandler.isEating(clickedOn[1], self.waitingForMove[1])     # get if a pawn is eating
            if eating[0]:                                        # if so
                self.gameHandler.pawnEaten(eating[1])            # add to natural pawns
                self.DeleteExistingPawn(eating[1])               # delete the eaten pawns
                self.createNewPawn((self.gameHandler.convertPointTOXY(eating[1]), eating[1]), True)   # create natural point
                self.gameHandler.updateLast50()
                self.notifications.text += "[color=0]Player ate " + str(eating[1]) +"\n[/color]"

            else:
                if eating[1] == (-2,-2):        # 15 natural pawns
                    print "there are 15 natural pawns, cant eat!"

            # if move finished, call newMoveMade:
            self.gameHandler.newMoveMade(self.waitingForMove[1], clickedOn[1])
            print "Player moved ", self.waitingForMove[1], " to ", clickedOn[1]
            self.notifications.text += "[color=0]Player moved "+ str(self.waitingForMove[1]) +" to "+ str(clickedOn[1])+"\n[/color]"

            self.gameFinished = self.gameHandler.winORdraw()

            self.waitingForMove = [False, (-1, -1)]

            if self.gameFinished[0] == False:
                thread = Thread(target=self.CPUturn, args=())  # it is now the CPU's turn
                thread.start()

    def ClickedPlacementPhase(self, clickedOn):
        '''if a player or the CPU made a move and its a placment phase'''

        if self.gameHandler.getTurn() == 1: # if CPU turn (no need to check i legal move)
            print "CPU clicked on:", clickedOn[1]
            print ""
            st = "[color=0]CPU placed a pawn at: " + str(clickedOn[1]) +"\n[/color]"
            self.notifications.text += st

            self.createNewPawn(clickedOn, False)
            self.gameHandler.newMoveMade((-1, -1), clickedOn[1])
            self.gameFinished = self.gameHandler.winORdraw()
            return

        if self.gameHandler.isSpotAvailable(clickedOn):  # spot Available
            if self.gameHandler.isEaten(clickedOn[1]):  # cant put it because it will be eaten
                if self.gameHandler.getTurn() == 0:
                    print "ERROR: Cant suicide"
                clickedOn = (-1, clickedOn[1])

            if self.gameHandler.isEating(clickedOn[1], (-1,-1))[0]:  # cant put it because it will eat (not allowed in placement phase)
                if self.gameHandler.getTurn() == 0:
                    print "ERROR: Cant eat during Placement phase"
                clickedOn = (-1, clickedOn[1])

        else: # spot not Available
            clickedOn = (-1, clickedOn[1])

        if (clickedOn[0] != -1):  # if clicked and free, create pawn
            if self.gameHandler.getTurn()==0:
                print "player clicked on:", clickedOn[1]
                self.notifications.text += "[color=0]Player placed a pawn at: " + str(clickedOn[1]) + "\n[/color]"

            else:
                print "CPU clicked on:", clickedOn[1]
            print ""

            self.createNewPawn(clickedOn, False)

            self.gameHandler.newMoveMade((-1,-1), clickedOn[1])

            self.gameFinished = self.gameHandler.winORdraw()

            if self.gameHandler.getTurn() == 1 and not self.gameFinished[0]:   # now its the CPU's turn
                thread = Thread(target= self.CPUturn, args = ())
                thread.start()

        else:   # IF CPU's turn was not legal
            if self.gameHandler.getTurn() == 1:   #CPU needs to select a currect spot
                self.CPUturn()

    def CanMoveAtoB(self, A, B):
        '''Will return if pawn A can move to spot B'''

        # A is an avilable spot, and it waitnig for a move
        errorString = []
        if not self.gameHandler.isSpotAvailable(B):
            errorString.append("Spot chosen not available")

        if not Logic.isNeighbors(A,B):
            errorString.append("can only move to a neighbour of " + str(A))

        # safe move: (?)
        #if self.gameHandler.isEaten(B):
        #    errorString.append("can't suicide")

        if len(errorString):
            print str(len(errorString))," ERRORS:"
            for i in errorString:
                print "   ",i
            return False
        return True

    def cancelMove(self):
        '''this function will cancel the move on a moving phase'''
        self.waitingForMove = [False, (-1, -1)]
        self.cancelMoving.disabled = True
        self.cancelMoving.opacity=0
        print "Player chose to cancel the selection\n"
        return
# ------------------------------------------------------------- AI ----------------------------------------------------- #


    def CPUplacementPhase(self):
        ''' will return the CPU move on a placement phase via MCTS'''
        start = time.time()
        CPUmove = MC_AI.getMoveAI(self.gameHandler)
        end = time.time()
        print (end - start), " sec"
        return CPUmove

    def CPUmovingPhase(self):
        ''' will return the CPU move on a moving phase via MCTS'''
        start = time.time()
        CPUmove = MC_AI.getMoveAI(self.gameHandler)
        end = time.time()
        print (end - start), " sec"
        return CPUmove


class Menu(Screen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        with self.canvas:
            size = (5000,5000)
            Rectangle(source="BackGround.jpg", size=size)

        self.layout = FloatLayout()
        self.play = Button(text="Play", on_press=lambda a: self.switchToGame(),
                           pos_hint={'center_x': .5, 'center_y': .6}, size_hint=(None, None), width=200, font_size=40)

        self.ins = Button(text="Instructions", on_press=lambda a: self.switchToIn(),
                           pos_hint={'center_x': .5, 'center_y': .4}, size_hint=(None, None), width=250, font_size=40)

        self.text = Label(text='[color=0]Diamond[/color]', pos_hint={'center_x': .5, 'center_y': .8},
                          size_hint=(None, None), width=200, font_size=80, markup=True)

        self.add_widget(self.play)
        self.add_widget(self.text)
        self.add_widget(self.ins)

    def switchToGame(self):
        self.manager.current = 'Game'

    def switchToIn(self):
        self.manager.current = 'Instructions'

class Instructions(Screen):
    def __init__(self, **kwargs):
        super(Instructions, self).__init__(**kwargs)
        with self.canvas:
            size = (5000,5000)
            Rectangle(source="BackGround.jpg", size=size)

        self.layout = FloatLayout()

        self.back = Button(text="Back", on_press=lambda a: self.switchToMenu(),
                           pos_hint={'center_x': .07, 'center_y': .07}, size_hint=(None, None), width=100, font_size=25, height=50)

        self.text = Label(text='[color=0]Instructions[/color]', pos_hint={'center_x': .5, 'center_y': .9},
                          size_hint=(None, None), width=200, font_size=80, markup=True)

        str1 = "[color=0]The game begins with an empty Diamond board. Black moves first, then turns alternate. Passing a turn is not permitted.[/color]"
        str2 = "[color=0]\n\nThe game is executed in two phases:\n[/color]"
        str3 = "[color=0]\n     1.    Placement phase:\n             Players take turns placing one of their pieces on any open point on the board.\n             No placements result in a capture in this phase. \n             A player can win the game in this phase if they are able to occupy all four corners of a board square.\n             otherwise, play proceeds to the Movement phase once all 24 pieces have been placed.[/color]"
        str4 = "[color=0]\n\n     2.    Movement phase:\n             For their turn, a player may either:\n             move one of their pieces along a straight line to an adjacent empty point;\n             or, remove a neutral piece from the board - but only if no white or black piece is adjacent to it.[/color]"
        str5 = "[color=0]\n\n\nA player will win when he will capture all 4 corners off any square.[/color]"

        self.str1 = Label(text=str1+str2+str3+str4+str5, pos_hint={'center_x': .40, 'center_y': .52},
                          size_hint=(None, None), width=200, font_size=18, markup=True)

        self.add_widget(self.back)
        self.add_widget(self.text)
        self.add_widget(self.str1)

    def switchToMenu(self):
        self.manager.current = 'Menu'

class DiamondApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(Menu(name= 'Menu'))
        sm.add_widget(DiamondGame(name= 'Game'))
        sm.add_widget(Instructions(name='Instructions'))
        return sm

DiamondApp().run()