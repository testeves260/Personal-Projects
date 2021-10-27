import time  # use only for debugging
from random import shuffle
from random import random

from operator import attrgetter

#Global Lists: - Approved []
Deck_Colors = ["|Red", "|Blu", "|Yel", "|Gre"]
ActionCard = ["|Gre Skip|", "|Blu Skip|", "|Red Skip|", "|Yel Skip|", "|Gre Reverse|", "|Blu Reverse|", "|Red Reverse|", "|Yel Reverse|", "|Gre Draw Two|", "|Blu Draw Two|", "|Red Draw Two|", "|Yel Draw Two|"]
WildCards = ["|Wild Draw Four|", "|Wild|"]

#List of Decks:
Deck_CurrentGame = []
Deck_CurrentGame_Obj = []
Deck_TableDeck_Obj = []

#List Of Players and increments
Players_List = []
increment = [0]

#Global Variables:
playingOrder = 1
skipOrder = ""
wildColor = "Undefined"
actualPlayer = 0
penaltySumDraw2 = 2
penaltySumDraw4 = 4
PointsSum = 0

#Create Deck:
def createDeck():
    def createNumbersOnDeck(RangeMin, RangeMax, Ammount):  # Create Deck with numbers
        for i in range(RangeMin, RangeMax):
            for _ in range(Ammount):
                for k in range(4):
                    Deck_CurrentGame.append(Deck_Colors[k] + "  " + str(i) + "|")
    def createActionCardsOnDeck(ACName, Ammount):  # Create Deck with Action Cards
        for i in range(Ammount):
            for k in range(4):
                Deck_CurrentGame.append(Deck_Colors[k] + " " + ACName + "|")
    def createWildCardsOnDeck(WCName, Ammount):  # Create Deck with Wild Cards
        for i in range(Ammount):
            Deck_CurrentGame.append("|" + WCName + "|")
    def compileDeck():  # Compiles all the previous functions and builds and shuffles a deck
        createNumbersOnDeck(1, 10, 2)  # Create Card "1" to "9" for each color
        createActionCardsOnDeck(" 0", 1)  # Create Card "0" for each color (x1 time)
        createActionCardsOnDeck("Draw Two", 2)  # Create Action Cards
        createActionCardsOnDeck("Reverse", 2)  # Create Action Cards
        createActionCardsOnDeck("Skip", 2)  # Create Action Cards
        createWildCardsOnDeck("Wild", 4)  # Create Wild Cards
        createWildCardsOnDeck("Wild Draw Four", 4)  # Create Wild Cards
        shuffle(Deck_CurrentGame)  # Shuffle the deck
    compileDeck()

def refillDeck():
    i = 0
    for card in Deck_TableDeck_Obj:
        if i > 0:
            Deck_CurrentGame_Obj.append(Deck_TableDeck_Obj.pop(card))
            shuffle(Deck_CurrentGame_Obj)  # Shuffle the deck
        i += 1
    print("Main Deck was refilled and shuffled.")

class Card:
    def __init__(self, name, color, number, isAction, actionType, isWild, wildType):
        # Card attributes
        self.name = name
        self.color = color
        self.number = number
        self.isAction = isAction
        self.actionType = actionType
        self.isWild = isWild
        self.wildType = wildType#Class for all the cards in game.

def cardAttrs(card, call_isCardWild=0, call_cardWildType=0, call_isCardAction=0, call_cardActionType=0, call_getCardColor=0, call_getCardNumber=0):
    def isCardWild(card): #bool
        if card in WildCards:
            return True
        else:
            return False
    def cardWildType(card):
        if isCardWild(card) == True:
            if card == "|Wild|":
                type = "Wild"
                return type
            elif card == "|Wild Draw Four|":
                type = "Wild Draw Four"
                return type
        else:
            return False
    def isCardAction(card): #bool
        if card in ActionCard:
            return True
        else:
            return False
    def cardActionType(card):
        if isCardAction(card) == True:
            type = "".join(char for char in card[5:-1:1])
            return type
        else:
            return False
    def getCardColor(card):
        if isCardWild(card) == True:
            return False
        else:
            color = "".join(char for char in card[1:4:1])
        return color
    def getCardNumber(card):
        if isCardWild(card) == True:
            return random()
        elif isCardAction(card) == True:
            return random()
        else:
            number = "".join(char for char in card[6:7:1])
            return number

    if call_isCardWild == 1:
        return isCardWild(card)
    elif call_cardWildType == 1:
        return cardWildType(card)
    elif call_isCardAction == 1:
        return isCardAction(card)
    elif call_cardActionType == 1:
        return cardActionType(card)
    elif call_getCardColor == 1:
        return getCardColor(card)
    elif call_getCardNumber == 1:
        return getCardNumber(card)

def convertCardToObject(originalDeck, objectDeck):
    idCount = 0
    for card in originalDeck: #Append each card as an object to a new deck
                                    #Card(name,color,number,isAction,actionType,isWild,wildType)
                                    #(card, call_isCardWild=0, call_cardWildType=0, call_isCardAction=0, call_cardActionType=0, call_getCardColor=0, call_getCardNumber=0)
        objectDeck.append(Card(card,cardAttrs(card, 0, 0, 0, 0, 1, 0),
                                    cardAttrs(card, 0, 0, 0, 0, 0, 1),
                                    cardAttrs(card, 0, 0, 1, 0, 0, 0),
                                    cardAttrs(card, 0, 0, 0, 1, 0, 0),
                                    cardAttrs(card, 1, 0, 0, 0, 0, 0),
                                    cardAttrs(card, 0, 1, 0, 0, 0, 0)))
        idCount += 1

#Class Player (Create Player):
class Player(Card):  # Define Players and Player Hand
    def __init__(self, playerID, playerName, playerAge, playerScore, mainDeck):
        self.playerID = playerID
        self.playerName = playerName
        self.playerAge = playerAge
        self.playerScore = playerScore
        self.mainDeck = mainDeck
        self.playerHand = []

    def setPlayerHand(self, Ammount):
        for i in range(Ammount):
            self.playerHand.append(self.mainDeck.pop(0))
    def showPlayerHand(self):
        count = 0
        time.sleep(1)
        print(self.playerName, "'s Hand:")
        for i in self.playerHand:
            print(count, " - ", i.name)
            count += 1
    def setPlayerID(self, playerID):
        self.playerID = playerID
    def setPlayerScore(self, score):
        self.playerScore = score

def createPlayer(mainDeck, playerlist):
    playersCount = int(input("Choose how many players will be playing (Max. 6): "))
    playerID = 0
    for player in range(playersCount):
        playerName = str(input("Player's Name: "))
        playerAge = int(input("Player's Age: "))
        playerlist.append(Player(playerID, playerName, playerAge, 0, mainDeck))
        playerID += 1

def lowestAge():
    Players_List.sort(key=lambda x: x.playerAge, reverse=False)
    x = 0
    for player in Players_List:
        player.playerID = x
        x += 1
    print(f"\nPlayer Starting the Round by Lowest Age is: {Players_List[0].playerName}\n")

#Moves
def playerHandToTable(move):
    global actualPlayer
    indexPlayer = Players_List[actualPlayer]

    Deck_TableDeck_Obj.insert(0, indexPlayer.playerHand[move])
    indexPlayer.playerHand.pop(move)
    print(f"{indexPlayer.playerName} played the card: {Deck_TableDeck_Obj[0].name}")

def deckToTable():
    Deck_TableDeck_Obj.insert(0, Deck_CurrentGame_Obj.pop(-1))

def seeCardOnTable():
    print("------------------------------------------------------")
    if Deck_TableDeck_Obj[0].name == "|Wild|":
        print(f"Card on the table is:\n{Deck_TableDeck_Obj[0].name} and the color chosen is {Deck_TableDeck_Obj[0].color}\n")
    elif Deck_TableDeck_Obj[0].name == "|Wild Draw Four|":
        print(f"Card on the table is:\n{Deck_TableDeck_Obj[0].name} and the color chosen is {Deck_TableDeck_Obj[0].color}\n")
    else:
        print(f"Card on the table is:\n{Deck_TableDeck_Obj[0].name}\n")

def chooseNewColor():
    global wildColor
    global actualPlayer

    count = 0
    indexPlayer = Players_List[actualPlayer]

    print(f"\n{indexPlayer.playerName} choose the color to next card: ")
    for color in Deck_Colors:
        print(count, " - ", color)
        count += 1
    userChoise = int(input("Color: "))
    wildColor = "".join(char for char in Deck_Colors[userChoise][1:4]) #slice the color in list to get without the "|"
    Deck_TableDeck_Obj[0].color = wildColor
    print(f"Color choosed by {indexPlayer.playerName} for next round is {wildColor}")
    return wildColor

def setPlayingOrder():
    global playingOrder

    if playingOrder == 1:
        playingOrder = -1
        print("Playing Order set to: Counterclockwise")
    elif playingOrder == -1:
        playingOrder = 1
        print("Playing Order set to: Clockwise")

#Checks card moves:
def checkFirstCardOnPile():
    global skipOrder
    global playingOrder

    while(Deck_TableDeck_Obj[0].isAction or Deck_TableDeck_Obj[0].isWild == True):
        if Deck_TableDeck_Obj[0].actionType == "Skip":
            #Player to dealer's left misses a turn (The present player will miss the round and starts the second player.)
            print("Bad Luck! Will skip to the next Player!")
            time.sleep(1)
            Deck_TableDeck_Obj.append(Deck_CurrentGame_Obj[0])
            return True
        elif Deck_TableDeck_Obj[0].actionType == "Reverse":
            setPlayingOrder()
            return True #gets out of the while loop
        elif Deck_TableDeck_Obj[0].actionType == "Draw Two":
            checkActionCardsStartOfRound()
            return True
        elif Deck_TableDeck_Obj[0].wildType == "Wild":
            #Choose a color and plays after it with the new color choosed.
            chooseNewColor()
            return True
        elif Deck_TableDeck_Obj[0].wildType == "Wild Draw Four":
            if len(Deck_TableDeck_Obj) == 1:
                #puts the card back to pile and shuffles it again.
                print("The First card is  not allowed as a first card. "
                      "Deck will be shuffled again and a new card  will be present.\n"
                      "Shuffling...")
                time.sleep(1)
                print("...")
                time.sleep(2)
                Deck_CurrentGame_Obj.append(Deck_TableDeck_Obj.pop(0))
                shuffle(Deck_CurrentGame_Obj)
                deckToTable()
                seeCardOnTable()
                return True
    else:
        return False

def checkActionCardsStartOfRound():
    global actualPlayer
    global penaltySumDraw2
    global penaltySumDraw4

    indexPlayer = Players_List[actualPlayer]

    if Deck_TableDeck_Obj[0].actionType == "Draw Two":
        #check if player has the Draw Two card present in hand and plays it.
        if any(Deck_TableDeck_Obj[0].actionType == card.actionType for card in Players_List[actualPlayer].playerHand):
            #cardIndex = Players_List[actualPlayer].playerHand.index(card)
            print("You have one 'Draw Two' card that you can play. Play it.")
            penaltySumDraw2 += 2
            return False
        else:
            print(f"OOPS!! Card on table is {Deck_TableDeck_Obj[0].name}, pick up {penaltySumDraw2} cards from the main deck!\n")
            time.sleep(2)
            indexPlayer.setPlayerHand(penaltySumDraw2)
            Deck_TableDeck_Obj[0].actionType = "None" #This way, the next player wont end up in this function again...
            penaltySumDraw2 = 2
            return True #if return true, will move to next player in while loop. cant do it here.
    elif Deck_TableDeck_Obj[0].wildType == "Wild Draw Four":
        if Deck_TableDeck_Obj[0] in indexPlayer.playerHand:
            print("You have one 'Wild Draw Four' that you can play.")
            penaltySumDraw4 +=  4
            for card in indexPlayer.playerHand:
                if card.wildType == "Wild Draw Four":
                    index = indexPlayer.playerHand.index(card)
            playerHandToTable(index)
            time.sleep(2)
        else:
            print(f"Someone is unlucky! {indexPlayer.playerName} pick up {penaltySumDraw4} cards from the main deck!")
            time.sleep(2)
            indexPlayer.setPlayerHand(penaltySumDraw4)
            Deck_TableDeck_Obj[0].wildType = "None" #This way, the next player wont end up in this function again...
            penaltySumDraw4 = 4
            return True #if return true, will move to next player in while loop. cant do it here.

def checkCardPlay(move):
    global actualPlayer
    indexPlayer = Players_List[actualPlayer]

    if indexPlayer.playerHand[move].isWild == True:
        print("DEBUG: Compatibility Check: isWild = True")
        playerHandToTable(move)
        time.sleep(2)
    elif indexPlayer.playerHand[move].isAction == True:
        if Deck_TableDeck_Obj[0].isAction == True:
            if Deck_TableDeck_Obj[0].actionType == indexPlayer.playerHand[move].actionType:
                print("DEBUG: Compatibility Check: actionType = True")
                playerHandToTable(move)
                time.sleep(2)
    elif indexPlayer.playerHand[move].color == Deck_TableDeck_Obj[0].color:
        print("DEBUG: Compatibility Check: COLOR")
        playerHandToTable(move)
        time.sleep(2)
    elif indexPlayer.playerHand[move].number == Deck_TableDeck_Obj[0].number:
        print("DEBUG: Compatibility Check: NUMBER")
        playerHandToTable(move)
        time.sleep(2)
    else:
        print("You failed the move, go draw 1 card.")
        time.sleep(2)
        indexPlayer.setPlayerHand(1)
        print(f"You draw 1 card from the deck. Is the card {indexPlayer.playerHand[-1].name}.")
        time.sleep(2)
        if indexPlayer.playerHand[-1].color == Deck_TableDeck_Obj[0].color:
            userChoise = input("You got a compatible card! Want to use it now? (y/n)")
            if userChoise == "y" or "Y":
                playerHandToTable(-1)
            else:
                print("Moving to next Player")
        elif indexPlayer.playerHand[-1].number == Deck_TableDeck_Obj[0].number:
            userChoise = input("You got a compatible card! Want to use it now? (y/n)")
            if userChoise == "y":
                playerHandToTable(-1)
            else:
                print("Moving to next Player")
        elif indexPlayer.playerHand[-1].isWild == True:
            userChoise = input("You got a compatible card! Want to use it now? (y/n)")
            if userChoise == "y":
                playerHandToTable(-1)
            else:
                print("Moving to next Player")
        else:
            if Deck_TableDeck_Obj[0].actionType == "Skip":
                Deck_TableDeck_Obj[0].isAction == "False" #So the next player wont have to skip either
            elif Deck_TableDeck_Obj[0].actionType == "Reverse":
                Deck_TableDeck_Obj[0].isAction == "False" #So the next player wont have to skip either
            print("The card you picked up is not eligible neither... Moving to Next Player.")

def checkActionCardsEndOfRound():
    global actualPlayer
    global playingOrder
    global skipOrder

    if Deck_TableDeck_Obj[0].isAction == True:
        if Deck_TableDeck_Obj[0].actionType == "Skip":
            print("Will skip to the next Player!")
            skipOrder = True
        elif Deck_TableDeck_Obj[0].actionType == "Reverse":
            setPlayingOrder()
    elif Deck_TableDeck_Obj[0].isWild == True:
        if Deck_TableDeck_Obj[0].wildType == "Wild":
            chooseNewColor()
        elif Deck_TableDeck_Obj[0].wildType == "Wild Draw Four":
            chooseNewColor()

#Player Turns:
def nextPlayer():
    global skipOrder
    global actualPlayer

    lenOfList = len(Players_List)
    # non reverse
    if playingOrder == 1:
        if skipOrder == True:
            if actualPlayer == lenOfList-1:
                actualPlayer = 1
                increment.append(0)
                return actualPlayer
            elif actualPlayer == lenOfList-2:
                actualPlayer = 0
                increment.append(0)
                return actualPlayer
            else:
                try:
                    increment.append(2)
                    actualPlayer = Players_List[actualPlayer].playerID + increment[-1]
                    skipOrder = False
                    return actualPlayer
                except IndexError:
                    actualPlayer = 0
                    increment.append(0)
                    skipOrder = False
                    return actualPlayer
        else:
            print("Debug Line 396: Actualplayer = ", actualPlayer)
            if actualPlayer == lenOfList-1:
                actualPlayer = 0
                increment.append(0)
                return actualPlayer
            else:
                try:
                    increment.append(1)
                    actualPlayer = Players_List[actualPlayer].playerID + increment[-1]
                    return actualPlayer
                except IndexError:
                    actualPlayer = -1
                    increment.append(0)
                    return actualPlayer
    # reverse order
    elif playingOrder == -1:
        if skipOrder == True:
            if actualPlayer == (lenOfList*-1)+1:
                actualPlayer = -1
                increment.append(0)
                skipOrder = False
                return actualPlayer
            else:
                try:
                    increment.append(-2)
                    actualPlayer = Players_List[actualPlayer].playerID + increment[-1]
                    skipOrder = False
                    return actualPlayer
                except IndexError:
                    actualPlayer = -1
                    increment.append(0)
                    skipOrder = False
                    return actualPlayer
        else:
            if actualPlayer == (lenOfList * -1) + 1:
                actualPlayer = 0
                increment.append(0)
                return actualPlayer
            else:
                increment.append(-1)
                actualPlayer = Players_List[actualPlayer].playerID + increment[-1]
                return actualPlayer

def setUpGame(): #Setup the Decks, players, etc
    #First - Deck Build:
    createDeck()
    convertCardToObject(Deck_CurrentGame, Deck_CurrentGame_Obj)
    #Second - Create Players:
    createPlayer(Deck_CurrentGame_Obj, Players_List)
    #Third - Give Cards to Players:
    for player in Players_List: player.setPlayerHand(7)
    #Fourth - Put card on table:
    deckToTable()
    #                               name,        color, number, isAction, actionType, isWild, wildType)
    # Deck_TableDeck_Obj.append(Card("|Red Skip|", "Red", None, True, "Skip", False, None))
    #Seventh - Select first player to play by Age
    lowestAge() # = index[0]
    seeCardOnTable()

def sumCardPoints(PlayerHand):
    global PointsSum
    PointsSum = 0 #Reset the number for a new calculation
    for card in PlayerHand:
        if card.isAction == True:
            PointsSum += 20
        elif card.isWild == True:
            PointsSum += 50
        else:
            PointsSum += int(card.number)
    return PointsSum
#Check Win:
def checkWin():
    global PointsSum
    if len(Players_List[actualPlayer].playerHand) == 0:
        print("Game is Over.")
        #Calculate other players hand and sum the points.
        for player in Players_List:
            sumCardPoints(player.playerHand)
        Players_List[actualPlayer].setPlayerScore(PointsSum)
        print(f"You gained {PointsSum}. You have now a total of {Players_List[actualPlayer].playerScore}")
        if Players_List[actualPlayer].playerScore > 500:
            print(f"Congratulations, the game is now over! {Players_List[actualPlayer].playerName} won the game with more points!")
            for player in Players_List:
                print(f"{player.playerName} has a total of {player.playerScore} points.")
        elif Players_List[actualPlayer].playerScore < 500:
            print(f"{Players_List[actualPlayer].playerName} wins the round! Starting a new round.")
            #Reset the whole game with exception of the player details and scores. Player hand goes away as well.
        PointsSum = 0
        return True
    elif len(Players_List[actualPlayer].playerHand) == 1:
        print("As there is only 1 remaining card in your hand, CALL UNO by typing 'UNO'")
        unoCall = input()
        if unoCall != "UNO":
            print("You failed to call UNO this time! Go draw 2 Cards!")
            Players_List[actualPlayer].setPlayerHand(2)
    else:
        return False

def drawDashboard():
    print("-------- D A S H B O A R D ---------\n"
        f"\033[91mPlayer Round: {Players_List[actualPlayer].playerName}\n\033[0m"
        f"Player Score: {Players_List[actualPlayer].playerScore}\n"
        f"Points of CIH (Cards in Hand):{sumCardPoints(Players_List[actualPlayer].playerHand)}\n"
        f"Playing Order: {playingOrder}\n"
        f"\033[1mCard in table:{Deck_TableDeck_Obj[0].name}\n\n\033[0m") #Prints in bold
#--------------------------------------------------------------------------------------------------------------------
setUpGame()#WORKKING

if checkFirstCardOnPile() == True:
    nextPlayer()
else:
    Players_List[actualPlayer].showPlayerHand()
    move = int(input("Select a card to play: "))
    checkCardPlay(move)
    checkActionCardsEndOfRound()
    nextPlayer()

while(checkWin() == False):
    if checkActionCardsStartOfRound() == True:
        nextPlayer()
        continue
    Players_List[actualPlayer].showPlayerHand()
    move = int(input("Select a card to play: "))
    checkCardPlay(move)
    checkActionCardsEndOfRound()
    checkWin()
    nextPlayer()
    seeCardOnTable()
