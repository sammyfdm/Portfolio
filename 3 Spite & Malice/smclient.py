#Label
#You can set its textvariable option to a StringVar. Then any call to the variable's .set() method will change the text displayed on the label. This is not necessary if the label's text is static; use the text attribute for labels that don't change while the application is running.
'''
Cards are identified by numbers with value first and the suit last
	3 Spades
	2 Hearts
	1 Clubs
	0 Diamonds
	ex: 30 (3 of diamonds), 31 (3 of clubs), 133 (king of spades)
	thus every 5 is greater than every 4, etc..., but two 5's are ordered by suit
	dividing by 10 gives just the card value, while modulo 10 gives just the card suit
Jokers indicated by value 14
Every pile has a 0 at its very base as a placeholder (indicates empty pile)
Cards have height 1.6 times their width

Client is always player 1
Server is always player 2
Server responsible for initial game set up and if there is double-spite(**?alternatively can just use initialization messages from client to server if this happens)
Client/Server handle computation for their own player and signal changes to the other
Each is responsible for knowing the turn has changed based on what change has been signalled by the other
	e.g. if Move command that moves a card to the discard pile => change of turn
Each message will consist of a character identifier followed by a list of number seperated by dashes
	the list of numbers represents either piles or cards depending on context
Common messages:
	'MO<p1>-<p2>' - move card from pile p1 to pile p2
	'SH'+cards - add shuffled pile in this order to the bottom of the play deck
	'GG' - game over
	'QU' - other player quit
Initialization messages (new game or after double spite):
	'PP'+cards - set play pile to this
	'PO'+cards - set point pile for player one to this
	'PT'+cards - set point pile for player two to this
	'HO'+cards - set player one's hand to this
	'HT'+cards - set player two's hand to this
	'SG'+[cur] - start game with self.curplay (current player) set to cur
	'CT'       - explicit your turn (used at discard and during redeals from double spite)

#**essential:
	-override destructors: stop thread for messages
	-test double spite	
	-client/server
#**features to add:
	-TCP/IP without port forwarding (ask todd)
	-combine messages: (ND & CT => CT), (PP, PO, PT => SP set pile), (HO & HT => HS set hand), (SH & PP => PP and make sure to set shuffle pile to [0], since only add shuffled cards when no more play pile anyway)
	-double spite message?
	-ability to view entire pile of cards, not just top one (especially important for discard piles)
	-loading & saving games
	-loading & saving players (long-term score management)
	-type a number and have cards of that value highlighted (don't have to search for them)
	-AI opponent
	-canned images of cards (& different deck backings)
	-indicate to a player when he has no discard options (maybe...can be turned on as an option for novice players)
	-gameover
(#**can make more efficient by changing some for loops into while loops)
'''

from Tkinter import *
from random import shuffle
import math
import time
import socket
import re
import thread

HOST = 'Gizmo-2.local'	#'70.55.222.30' #'192.168.104.1'#'daring.cwi.nl'	# The remote host
PORT = 50007	# Arbitrary non-privileged port (port-forwarded on my home router)

##########################################################
#Player Class
##########################################################

class Player(object):

	def __init__(self,name='guest'):
		self.name = name
		self.score = 0 #to be loaded
	
	def load(self):
		infile = open(self.name,'r')
		self.score = int(infile.readline())
		infile.close()
	
	def save(self):
		outfile = open(self.name,'w')
		infile.writeline(self.score)
		outfile.close()		
	
##########################################################
#SandM Class
##########################################################

class SandM(Frame):

	##########################################################
	#Initialization
	##########################################################

	def __init__ (self,master=None,sock=None):
		self.sock = sock
		
		#initialize frame variables
		self.width = 700
		self.height = 500
		self.cardh = min(self.height/5-10,(self.width/6)*1.6-10) #height of a card in pixels (allows for 5 pixels to border each card [10 between cards])
		self.cardw = self.cardh/1.6
		
		#initialize game variables
		self.cardset = []
		for i in range(13):
			for j in range(4):
				self.cardset.append((i+1)*10+j)
		self.piles = [[0]]*26 #list of all piles in the game
		'''order:
		0		P1 point pile
		1		play pile
		2		P2 point pile
		3-6		P1 discard piles (screen left to right)
		7-10	play piles (screen left to right)
		11-14	P2 discard piles (screen left to right)
		15-19	P1 hand
		20-24	P2 hand
		25		cards to shuffle back into play pile
		'''
		self.points = {1:0,2:2}
		self.discards = {1:[3,4,5,6],2:[11,12,13,14]}
		self.hands = {1:[15,16,17,18,19],2:[20,21,22,23,24]}
		self.pileLoc = []
		self.initLoc(self.pileLoc)
		self.pileselected = -1 #indicates which pile is selected (corresponding to the same scheme as pileLoc locations)
								#-1 indicates no selection
		self.doublespite = 0 #indicates whether a doublespite might occur by turning 1 if a player NoDiscards with 5 cards in their hand
		
		#initialize widgets
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()
		
		#define function for mouse click
		self.board.bind('<Button-1>',self.onSingleClick)
		
		#get player names
		#for now just guests
		self.p1 = Player()
		self.p2 = Player()
		self.player = 1
		self.curplay = 0	#who's turn (1 or 2), 0 indicates game hasn't started
		
		self.inprogress = False
		thread.start_new_thread(self.otherplayer,())
		print 'init over'
	
	def newGame(self):
		self.piles = [[0]]*26 #reset piles
		self.piles[1] = self.cardset[:]+[140,140]	#play pile
		shuffle(self.piles[1])
		self.piles[1] += [0]
		'''#the following is for testing purposes; when ready remove and reinstate the above line
		self.piles[1] = []
		for i in range(1):
			for j in range(13):
				self.piles[1].append((j+1)*10+i)
		self.piles[1] += [0]
		#self.piles[25] = [11,21,31,41,51,61,71,81,91,101,111,121,131,0]
		'''
		shuffle(self.cardset)
		self.piles[0] = self.cardset[:26]+[0] #P1 point pile
		self.piles[2] = self.cardset[26:]+[0] #P2 point pile
		self.curplay = (self.piles[0][0] < self.piles[2][0]) + 1
		#deal hands
		for p in self.hands[self.curplay]:
			self.piles[p] = [self.piles[1][0],0]
			self.piles[1] = self.piles[1][1:]
		for p in self.hands[3-self.curplay]:
			self.piles[p] = [self.piles[1][0],0]
			self.piles[1] = self.piles[1][1:]
		#self.drawBoard()
		
		#communicate the initial state to client
		self.sendmsg('PP',self.piles[1]) #set play pile
		self.sendmsg('PO',self.piles[0]) #set player one's point pile
		self.sendmsg('PT',self.piles[2]) #set play two's point pile
		hand1 = []
		for p in self.hands[1]:
			hand1.append(self.piles[p][0])
		hand2 = []
		for p in self.hands[2]:
			hand2.append(self.piles[p][0])
		self.sendmsg('HO',hand1) #set player one's hand
		self.sendmsg('HT',hand2) #set player two's hand
		
		self.inprogress = True
		self.sendmsg('SG',[self.curplay])	#'game has started'
		self.drawBoard()
	
	def startgame(self):
		if self.inprogress:
			return
		self.inprogress = True
		if self.curplay != self.player:
			self.sendmsg('CT',[])	#indicate it's client's turn
		self.drawBoard()
		#self.otherplayer()
	
	def createWidgets(self):	
		self.board = Canvas(self,width=self.width,height=self.height)
		self.board.pack(side=TOP) #{'side':'top'})
		
		row = Frame(self)
		row.pack(side=BOTTOM)
		
		self.NoDiscard = Button(row)
		self.NoDiscard['text']='No Discard'
		self.NoDiscard['command'] = self.nodiscard
		self.NoDiscard.pack(side=LEFT)
		
		self.StartGame = Button(row)
		self.StartGame['text']='Start Game'
		self.StartGame['command'] = self.startgame
		self.StartGame.pack(side=LEFT)
		
		self.NewGame = Button(row)
		self.NewGame['text']='New Game'
		self.NewGame['command'] = self.newGame
		self.NewGame.pack(side=LEFT)
		
		self.Quit = Button(row)
		self.Quit['text']='Quit'
		self.Quit['command'] = self.quit
		self.Quit.pack(side=LEFT)
	
	def initLoc(self,pileLoc):
		self.spacex = (self.width - self.cardw*6)/7
		self.spacey = (self.height - self.cardh*5)/6
		#pointpile1
		pileLoc.append((self.cardw*1+self.spacex*2,self.cardh*1+self.spacey*2))
		#playpile
		pileLoc.append((self.cardw*1+self.spacex*2,self.cardh*2+self.spacey*3))
		#pointpile2
		pileLoc.append((self.cardw*1+self.spacex*2,self.cardh*3+self.spacey*4))
		#discardpiles for player 1
		pileLoc.append((self.cardw*2+self.spacex*3,self.cardh*1+self.spacey*2))
		pileLoc.append((self.cardw*3+self.spacex*4,self.cardh*1+self.spacey*2))
		pileLoc.append((self.cardw*4+self.spacex*5,self.cardh*1+self.spacey*2))
		pileLoc.append((self.cardw*5+self.spacex*6,self.cardh*1+self.spacey*2))
		#playpiles
		pileLoc.append((self.cardw*2+self.spacex*3,self.cardh*2+self.spacey*3))
		pileLoc.append((self.cardw*3+self.spacex*4,self.cardh*2+self.spacey*3))
		pileLoc.append((self.cardw*4+self.spacex*5,self.cardh*2+self.spacey*3))
		pileLoc.append((self.cardw*5+self.spacex*6,self.cardh*2+self.spacey*3))
		#discardpiles for player 2
		pileLoc.append((self.cardw*2+self.spacex*3,self.cardh*3+self.spacey*4))
		pileLoc.append((self.cardw*3+self.spacex*4,self.cardh*3+self.spacey*4))
		pileLoc.append((self.cardw*4+self.spacex*5,self.cardh*3+self.spacey*4))
		pileLoc.append((self.cardw*5+self.spacex*6,self.cardh*3+self.spacey*4))
		#hand for player 1
		pileLoc.append((self.cardw*1+self.spacex*2,self.cardh*0+self.spacey*1))
		pileLoc.append((self.cardw*2+self.spacex*3,self.cardh*0+self.spacey*1))
		pileLoc.append((self.cardw*3+self.spacex*4,self.cardh*0+self.spacey*1))
		pileLoc.append((self.cardw*4+self.spacex*5,self.cardh*0+self.spacey*1))
		pileLoc.append((self.cardw*5+self.spacex*6,self.cardh*0+self.spacey*1))
		#hand for player 2
		pileLoc.append((self.cardw*1+self.spacex*2,self.cardh*4+self.spacey*5))
		pileLoc.append((self.cardw*2+self.spacex*3,self.cardh*4+self.spacey*5))
		pileLoc.append((self.cardw*3+self.spacex*4,self.cardh*4+self.spacey*5))
		pileLoc.append((self.cardw*4+self.spacex*5,self.cardh*4+self.spacey*5))
		pileLoc.append((self.cardw*5+self.spacex*6,self.cardh*4+self.spacey*5))
		#shuffle pile
		pileLoc.append((self.cardw*0+self.spacex*1,self.cardh*2+self.spacey*3))
	
	##########################################################
	#Gameplay
	##########################################################

	def gameover(self):
		pass
		#**gameover = tkFont.Font ( family="Helvetica", size=36, weight="bold")
		#self.board.create_text(self.width/2,self.height/2,text="GAME OVER")#,font=gameover)
		#self.wait_window() #**fix this
	
	def takecards(self):
		for p in self.hands[self.curplay]:#range(15+(self.curplay-1)*5,20+(self.curplay-1)*5):#hand:
			if self.piles[p][0] == 0:	#room to pick up
				if self.piles[1][0] == 0:	#if no cards in play pile
					if self.piles[25][0] == 0:	#if no cards available to shuffle in
						self.sendmsg('GG',[])	#msg game over
						self.gameover()
					else:
						addin = self.piles[25][:len(self.piles[25])-1]	#exclude 0 on end
						shuffle(addin)	#shuffle them
						self.piles[1] = addin+[0]	#add onto play pile
						self.sendmsg('SH',addin)	#msg shuffle pile added to play pile in this order
						self.piles[25] = [0]	#empty shuffle pile
				self.piles[p] = [self.piles[1][0],0]
				self.piles[1] = self.piles[1][1:]
				self.sendmsg('MO',[1,p])	#msg move from play pile to hand
		self.drawBoard()
	
	def respite(self):
		self.piles[1] = self.piles[1][:len(self.piles[1])-1] #remove 0 from end
		#put cards from players' hands back into deck
		for p in self.hands[1]+self.hands[2]:
			self.piles[1] += self.piles[p][0]
		#put shuffle cards back into deck
		self.piles[1] += self.piles[25][:len(self.piles[25])-1] #except for 0 on the end
		self.piles[25] = [0]
		shuffle(self.piles[1])	#shuffle deck
		self.piles[1] = self.piles[1]+[0] #add 0 to the end again
		#reset the turn
		self.curplay = (self.piles[0][0] < self.piles[2][0]) + 1
		#redeal hands (alternating deal)
		i = 0
		for p in self.hands[self.curplay]:
			self.piles[p] = [self.piles[1][i],0]
			i += 2
		i = 1
		for p in self.hands[3-self.curplay]:
			self.piles[p] = [self.piles[1][0],0]
			i += 2
		self.piles[1] = self.piles[1][10:]
		#communicate new state to other player (don't need to communicate point piles)
		self.sendmsg('PP',self.piles[1]) #set play pile
		hand1 = []
		for p in self.hands[1]:
			hand1.append(self.piles[p][0])
		hand2 = []
		for p in self.hands[2]:
			hand2.append(self.piles[p][0])
		self.sendmsg('HO',hand1) #set player one's hand
		self.sendmsg('HT',hand2) #set player two's hand
		#redraw board
		self.drawBoard()
		if self.curplay != self.player:
			self.sendmsg('CT',[])
			#self.otherplayer()
	
	#decides whether to move card from pile1 to pile2 and if so implements the consequences
	#pre: it's legal to move from pile1 to pile2 (ex. can't move onto other player's discard pile)
	def checklegal(self,pile1i,pile2i):
		legal = False
		card1 = self.piles[pile1i][0]	#card to be moved
		card2 = self.piles[pile2i][0]	#card onto which card1 will be moved
		if pile2i in [7,8,9,10]:	#if trying to play a card to centre piles
			#if card is one greater or card is a joker and two greater than the one below it, or is a joker and not being used as 1,2,7,K
			if (card1/10 == card2/10+1) or (card2/10==14 and card1/10==self.piles[pile2i][1]/10+2) or (card1/10==14 and not card2/10 in [0,1,6,12]):
				#move card from pile1 to pile2
				self.piles[pile2i] = [self.piles[pile1i][0]] + self.piles[pile2i]
				self.piles[pile1i] = self.piles[pile1i][1:]
				self.sendmsg('MO',[pile1i,pile2i])	#msg move from pile1i to pile2i
				print 'moved card ', card1, ' onto card ', card2
				legal = True
				#**the following can be made simpler by keeping track of how many cards are in each player's hand, decrementing when a card is moved from it, checking if it's at 0, and setting back to 5 at the beginning of a turn
				if pile1i in self.hands[self.curplay]:	#if card was moved from hand
					empty=0								#and was last in hand pick up 5 more
					for p in self.hands[self.curplay]:
						empty += (self.piles[p][0]==0)
					if empty == 5:
						self.takecards()
				if card1/10 == 13:	#if the move finished a play pile
					self.piles[25] = self.piles[pile2i][:13] + self.piles[25]
					self.piles[pile2i] = [0]
		else: #if discard move
			#check if 1's or 2's in hand or discard piles can be played
			if self.check12():
				print "you must play Aces and 2's if possible before ending your turn"
			#if card is same or one greater or it's an empty pile, and card can't be a joker
			elif (((0 <= (card2/10) - (card1/10) <= 1) or card2==0) and card1/10 != 14):
				#move card from pile1 to pile2
				self.piles[pile2i] = [self.piles[pile1i][0]] + self.piles[pile2i]
				self.piles[pile1i] = self.piles[pile1i][1:]
				self.sendmsg('MO',[pile1i,pile2i])	#msg move from pile1i to pile2i
				print 'moved card ', card1, ' onto card ', card2
				legal = True
				self.doublespite = 0	#since ended turn with less than 5 cards in hand
				self.curplay = 3 - self.curplay	#change turns
				self.sendmsg('CT',[])
				#self.takecards() #will draw cards for the player (doesn't effect the return flow from this point)
		return legal
	
	#returns true if the current player can play an Ace or a two on the board
	def check12(self):
		found1 = False	#player has access to an Ace
		found2 = False	#player has access to a 2
		for p in ([self.points[self.curplay]]+self.discards[self.curplay]+self.hands[self.curplay]):
			found1 = found1 or (self.piles[p][0]/10 == 1)
			found2 = found2 or (self.piles[p][0]/10 == 2)
		#if player has an ace and there is an open space on the board
		if found1 and (self.piles[7][0] == 0 or self.piles[8][0] == 0 or self.piles[9][0] == 0 or self.piles[10][0] == 0):
			return True
		#if player has a two there is an ace on the board
		elif found2 and (self.piles[7][0]/10 == 1 or self.piles[8][0]/10 == 1 or self.piles[9][0]/10 == 1 or self.piles[10][0]/10 == 1):
			return True
		return False
	
	def nodiscard(self):
		#check if 1's or 2's in hand or discard piles can be played
		if self.check12():
			print "you must play Aces and 2's if possible"
			return
		#check if discard available
		found = -1
		hand = []
		for p in self.hands[self.curplay]:
			if self.piles[p][0] != 0 and self.piles[p][0]/10 != 14: #cards other than 0 and Joker
				hand.append(self.piles[p][0]/10)
		for p in self.discards[self.curplay]:
			card = self.piles[p][0]/10
			if card in hand or (card-1) in hand or (card == 0  and len(hand) > 0):
				found = card
		if found >= 0:
			if found == 0:
				print 'you can discard to the empty pile'
			else:
				print 'you can discard onto the %d'%found
			return
		#change turns
		print 'no discard'
		self.doublespite = 0
		if len(hand) == 5:
			if self.doublespite == 1:
				self.doublespite = 0
				self.respite()
				return
			else:
				self.doublespite = 1
		self.curplay = 3 - self.curplay
		self.sendmsg('CT',[])
	
	##########################################################
	#GUI Calc
	##########################################################

	def findLoc(self,x,y):
		found = False
		l = 0
		while not found and l < 26:
			found = (self.pileLoc[l][0] <= x <= self.pileLoc[l][0] + self.cardw) and (self.pileLoc[l][1] <= y <= self.pileLoc[l][1] + self.cardh)
			l += 1
		return l - found #if found a pile undo the last increment, else leave at 25
	
	def onSingleClick(self,event):
		#only allow interaction if it is this player's turn
		if self.player != self.curplay or not self.inprogress:
			return
		#figure out which pile was selected if any
		l = self.findLoc(event.x,event.y)
		#can't select play pile or shuffle pile or non-player piles
		forbidden = ([1,25]+[self.points[3-self.curplay]]+self.discards[3-self.curplay]+self.hands[3-self.curplay])
		if l == 26:	#no pile clicked on
			print 'no pile selected'
			self.pileselected = -1
		elif l in forbidden:	#no permitted piles selected
			print "this pile can't be selected for moving cards"
		elif self.pileselected < 0:	#if no pile was previously selected
			if l in [1,7,8,9,10]:
				print "you can't move cards from here"
			elif self.piles[l][0]==0:
				print "there are no cards in this pile"
			else:
				print 'selected pile ', l
				self.pileselected = l
		#pile was previously selected
		elif self.pileselected == l: #if clicked on same pile as before
			self.pileselected = -1 #deselect it
		elif l in ([self.points[self.curplay]]+self.hands[self.curplay]): #this pile can't have card put onto it
			print "can't put a card onto points pile or into your hand"
		elif self.pileselected == self.points[self.curplay] and l in self.discards[self.curplay]:
			print "can't discard a point card"
		elif self.checklegal(self.pileselected,l): #the move is legal
			print 'moved from ', self.pileselected, ' to ', l
			self.pileselected = -1
		else: #the move is not legal
			print "illegal move: didn't move card from ", self.pileselected, ' to ', l
			#print message about illegality? (or this can be done in self.checklegal)
		self.drawBoard()
	
	##########################################################
	#GUI Display
	##########################################################

	def drawCardUp(self,(xx,yy),pile=[0]):
		if pile[0] == 0:
			self.board.create_rectangle(xx,yy,xx+self.cardw,yy+self.cardh)
		elif pile[0]/10 == 14: #joker
			self.board.create_rectangle(xx,yy,xx+self.cardw,yy+self.cardh,fill="white")
			self.board.create_text(xx+10,yy+10,text='J',fill="red")
		else:
			suit = (pile[0]%10)
			self.board.create_rectangle(xx,yy,xx+self.cardw,yy+self.cardh,fill="white")
			cx = xx+self.cardw/2
			cy = yy+self.cardh/2
			colour=''
			if suit == 0: #diamonds
				self.board.create_polygon(cx-10,cy,cx,cy-20,cx+10,cy,cx,cy+20,fill='red')
				colour = 'red'
			elif suit == 1: #clubs
				self.board.create_polygon(cx-3,cy+6,cx-1,cy,cx-10,cy+3,cx-10,cy-3,cx-1,cy-1,cx-3,cy-10,cx+3,cy-10,cx+1,cy-1,cx+10,cy-3,cx+10,cy+3,cx+1,cy,cx+3,cy+6,fill='black')
				colour = 'black'
			elif suit == 2: #hearts
				self.board.create_polygon(cx,cy-5,cx+5,cy-10,cx+10,cy-5,cx,cy+20,cx-10,cy-5,cx-5,cy-10,fill='red')
				colour = 'red'
			elif suit == 3: #spades
				self.board.create_polygon(cx-3,cy+15,cx-1,cy+10,cx-10,cy+13,cx-5,cy,cx,cy-10,cx+5,cy,cx+10,cy+13,cx+1,cy+10,cx+3,cy+15,fill='black')
				colour = 'black'
			self.board.create_text(xx+10,yy+10,text='%d'%(pile[0]/10),fill=colour)
	
	def drawCardDown(self,(xx,yy),pile=[0]):
		if pile[0] == 0:
			self.board.create_rectangle(xx,yy,xx+self.cardw,yy+self.cardh)
		else:
			self.board.create_rectangle(xx,yy,xx+self.cardw,yy+self.cardh,fill="red")
			self.board.create_text(xx+self.cardw/2,yy+self.cardh/2,text='%d'%(len(pile)-1))
	
	def drawBoard(self):
		self.board.create_rectangle(0,0,self.width,self.height,fill="gray")
		for pi in range(len(self.piles)):
			if pi in [1,25]+(self.hands[3-self.player]):
				self.drawCardDown(self.pileLoc[pi],self.piles[pi])
			else:
				self.drawCardUp(self.pileLoc[pi],self.piles[pi])
		
		#draw boarder around selected pile
		if self.pileselected >= 0:
			tx = self.pileLoc[self.pileselected][0]
			ty = self.pileLoc[self.pileselected][1]
			self.board.create_rectangle(tx,ty,tx+self.cardw,ty+self.cardh,outline='blue',width=5)
		#remaining labels
		self.board.create_text(self.pileLoc[0][0]-self.spacex/2,self.pileLoc[0][1]+self.cardh/2,text='%d'%(len(self.piles[0])-1))
		self.board.create_text(self.pileLoc[2][0]-self.spacex/2,self.pileLoc[2][1]+self.cardh/2,text='%d'%(len(self.piles[2])-1))
		
		#indicate player turn
		self.board.create_text(self.spacex/2,25,text="Player")
		self.board.create_text(self.spacex/2,50,text="%d's"%self.curplay)
		self.board.create_text(self.spacex/2,75,text="Turn")
	
	##########################################################
	#Client/Server
	##########################################################

	def sendmsg (self,msg,l):
		for c in l:
			msg += '-' + str(c)
		self.sock.send(msg)
		print 'client sent message: ', msg
	
	def getmsg (self,extra,msg):
		msg = extra + msg
		m = re.search('[^\d-]',msg[2:])	#get index next command if there is one
		if m:
			extra = msg[2+m.start():]
			msg = msg[:2+m.start()]
		else:
			extra = ''	#no additional command parts
		cmd = msg[:2]
		l = []
		m = re.findall('-(\d+)',msg)
		for c in m:
			l.append(int(c))
		return [cmd,l,extra]
	
	#this function takes care of dealing with server when it's their turn
	def otherplayer(self):
		extra = ''
		#while their turn isn't over
		while True:#self.curplay != self.player:
			print 'test', self.curplay
			#**dangerous: can a message be cut off? An entire sequence of play should be less than 1024, shouldn't it? What if it is read part-way between being read?
			if extra == '':
				data = self.sock.recv(1024)
			else:
				data = ''	
			print 'client received message: ', data
			[cmd,l,extra] = self.getmsg(data,extra)
			if cmd == 'MO':	#move card from pile p1 to pile p2
				#n/a
				self.piles[l[1]] = [self.piles[l[0]][0]] + self.piles[l[1]]
				self.piles[l[0]] = self.piles[l[0]][1:]
				print 'other player moved card ', l[0], ' onto card ', l[1]
				#**don't need to check for all the things that need to be checked for (change of turn, empty hand, etc)?
			elif cmd == 'SH':	#add shuffled pile in this order to the bottom of the play deck
				#list has no '0'
				self.piles[1] = l+[0]	#add onto play pile (play pile should be 0)
				self.piles[25] = [0]	#empty shuffle pile
			elif cmd == 'GG':	#game over
				#no list
				self.gameover()
			elif cmd == 'PP':	#set play pile to this
				#list has ending '0'
				self.piles[1] = l
			elif cmd == 'PO':	#set point pile for player one to this
				#list has ending '0'
				self.piles[0] = l
			elif cmd == 'PT':	#set point pile for player two to this
				#list has ending '0'
				self.piles[2] = l
			elif cmd == 'HO':	#set player one's hand to this
				#list has no '0'
				i = 0
				print self.piles[0]
				print self.piles[2]
				print l
				for p in self.hands[1]:
					self.piles[p] = [l[i],0]
					i += 1
			elif cmd == 'HT':	#set player two's hand to this
				#list has no '0'
				i = 0
				for p in self.hands[2]:
					self.piles[p] = [l[i],0]
					i += 1
			elif cmd == 'CT':	#explicit your turn (required at initialization and during redeals from double spite)
				#no list
				self.curplay = self.player
				self.takecards()
			elif cmd == 'SG':	#explicit start game
				#list with single element indicating turn
				self.inprogress = True
				self.curplay = l[0]
			elif cmd == 'QU':	#other player quit
				pass #**
			self.drawBoard()
	
##########################################################
#Main
##########################################################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

root = Tk()
Game = SandM(master=root,sock=s)
Game.master.title("Player 1 - Client")
Game.mainloop()
root.destroy()

s.close()