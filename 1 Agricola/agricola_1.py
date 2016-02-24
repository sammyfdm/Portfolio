import sys
import random
from Tkinter import *
import thread
#from PIL import Image, ImageTk

class Action(object):
	def __init__(self,name,func,store=None):
		self.name=name
		self.func=func
		self.store=store
	
	def __str__(self):
		return self.name
	
	def get_name(self):
		return self.name

	def get_func(self):
		return self.func
	
	def set_func(self,f):
		self.func=f
	
	def get_store(self):
		return self.store

	def set_store(self,s):
		self.store=s

class Round(object):
	
	'''
	start := actions to take when the round begins, encoded as 2D list, a list for each "action" with the first parameter being an integer representing the type of action
		[0,resource,amount,player]
			give <amount> number of <resource> to <player>
			(e.g. receive 1 food)
		[1,function,resource,cost,player]
			<player> has option of paying <cost> of <resource> to perform <function>
			(e.g. plow field for 1 food)
	action := the action that is added by this round card (function in Agricola class)
		[<Action object>,<amount to increment store by if applicable, else -1>]
	harvest := boolean, True iff harvest at the end of this round
	'''
	
	def __init__(self,action=None,h=False):
		self.start=[]
		self.action=action
		self.harvest=h
	
	def add_start(self,action):
		self.start.append(action)
	
	def get_start(self):
		return self.start
	
	def set_action(self,action):
		self.action=action
	
	def get_action(self):
		return self.action
	
	def set_harvest(self):
		self.harvest=True
	
'''
class Farmspace(object):
	def __init__():
		self.type=None

class Field(Farmspace):
	self.grain_sown=0
	self.vegetable_sown=0
'''
class Farmyard(object):
	'''
	spaces :=
		-holds integer values representing each space of the farm yard
		-1D list with 15 values
		-first 3 values represent first column, next 3 represent second column, etc.
	values:
		0 == empty
		1 == wooden room
		2 == clay room
		3 == stone room
		4 == pasture w/o stable
		5 == pasture w/ stable (note that if a pasture includes more than one space, only the space with the stable on it will be valued 5, the rest will be 4)
		6 == field w/ nothing sown
		7 == field w/ 1 grain sown
		8 == field w/ 2 grain sown
		9 == field w/ 3 grain sown
		10 == field w/ 4 grain sown
		11 == field w/ 5 grain sown
		12 == field w/ 1 vegetable sown
		13 == field w/ 2 vegetable sown
		14 == field w/ 3 vegetable sown
		15 == field w/ 4 vegetable sown
	fences :=
		-1D list of pairs (i,j)
		-i and j are the indices of the two farm spaces that the fence separates
	animal_capacity :=
		-1D list of integers
		-each integer represents the amount of a single type of animal that can be housed somewhere
	'''
	def __init__(self):
		self.spaces=[1]*2+[0]*13#start with two wooden rooms
		self.fences=[]
		self.animal_capacity=[1]#1 in your house
		#image
		#self.farmcanvas.create_rectangle(0,0,100,100,fill='gray')
	
	def get_spaces(self):
		return self.spaces
	
	def val_to_str(self,v):
		if 0 == v:
			return 'empty'
		if 1 == v:
			return 'wood rm'
		if 2 == v:
			return 'clay rm'
		if 3 == v:
			return 'stone rm'
		if 4 == v:
			return 'pasture'
		if 5 == v:
			return 'pasture + stbl'
		if 6 == v:
			return 'field 0'
		if 7 == v:
			return 'field 1 gr'
		if 8 == v:
			return 'field 2 gr'
		if 9 == v:
			return 'field 3 gr'
		if 10 == v:
			return 'field 4 gr'
		if 11 == v:
			return 'field 5 gr'
		if 12 == v:
			return 'field 1 veg'
		if 13 == v:
			return 'field 2 veg'
		if 14 == v:
			return 'field 3 veg'
		if 15 == v:
			return 'field 4 veg'
	
	#return string description of the space at index n
	def str_space(self,n):
		return self.val_to_str(self.spaces[n])
	
	#return a list
	def get_animal_capacity(self):
		return self.animal_capacity
	
	#return a list of "undominated" sets representing the maximum numbers of animals you can get and still keep
	#*should this be a function of the player; their the one that knows how many sheep/boar/cows they have
	def get_animals_allowed(self):
		pass
	

class Board(Frame):
	def __init__(self,master=None,nump=1):
		self.width = 800
		self.height = 600
		self.nump = nump
		
		Frame.__init__(self,master)
		self.pack()
		
		self.main_board_frame=Frame(master=self)
		self.main_board_frame.grid(row=0,column=0)
		board_all = PhotoImage(file='images/board_all.gif')
		old_width = board_all.width()
		old_height = board_all.height()
		print old_width
		self.main_board_canvas=Canvas(self.main_board_frame,width=old_width,height=old_height)
		self.main_board_canvas.create_image(0,0,image=board_all,anchor=NW)
		self.main_board_canvas.grid(row=0,column=0)
		self.main_board_frame.pack()
		self.main_board_canvas.pack()

		self.farms_frame = Frame(master=self)
		self.farms_frame.grid(row=1,column=0)
		self.farms=[]
		self.farms_canvas=[]
		for i in range(nump):
			self.farms.append(Frame(master=self.farms_frame))
			self.farms[i].grid(row=0,column=i)
			#self.farmimage = Frame(master=self.main)
			#self.farmimage.pack()
			#image = Image.open("images/farm.jpg")
			empty_farm = PhotoImage(file='images/farm.gif')
			old_width = empty_farm.width()
			old_height = empty_farm.height()
			#new_width = 400
			#new_height = old_height*new_width/old_width
			#image.resize((new_width,new_height))
			#empty_farm = ImageTk.PhotoImage(image)
			#empty_farm.subsample((new_width+0.0)/old_width,(new_height+0.0)/old_height)
			self.farms_canvas.append(Canvas(self.farms[i],width=old_width,height=old_height))
			self.farms_canvas[i].create_image(0,0,image=empty_farm,anchor=NW)
			self.farms_canvas[i].grid(row=0,column=0)
		

class Player(object):
	
	def __init__(self,n='',f=0,w=0,c=0,r=0,s=0,g=0,v=0,sh=0,b=0,ca=0):
		self.name=n
		#family members
		self.family=2
		#resources
		self.food=f#will be set to 0 if solo, 2 if starting player, 3 otherwise
		self.wood=w
		self.clay=c
		self.reed=r
		self.stone=s
		self.grain=g
		self.vegetable=v
		self.sheep=sh
		self.boar=b
		self.cattle=ca
		#farmyard
		self.farmyard=Farmyard()
		#occupations
		self.occupations_played=[]
		self.occupations_inhand=[]#will be randomly set to include 7 of them
		#minor improvements
		self.minor_improvements_played=[]
		self.minor_improvements_inhand=[]#will be randomly set to include 7 of them

	def __str__ (self):
		s='Player %s:\n'%self.name
		s+='     Family size:     %d\n'%self.family
		s+='     Food:            %d\n'%self.food
		s+='     Wood:            %d\n'%self.wood
		s+='     Clay:            %d\n'%self.clay
		s+='     Reed:            %d\n'%self.reed
		s+='     Stone:           %d\n'%self.stone
		s+='     Grain:           %d\n'%self.grain
		s+='     Vegetable:       %d\n'%self.vegetable
		s+='     Sheep:           %d\n'%self.sheep
		s+='     Boar:            %d\n'%self.boar
		s+='     Cattle:          %d'%self.cattle
		return s
	
	def print_farmyard(self):
		spaces = self.farmyard.get_spaces()
		width = 20
		s = ''
		for i in range(3):
			s += '-'+'-'*((width+1)*5)+'\n'
			s += '|'
			for j in range(5):
				num = (3-i)+3*j
				if num < 10:
					s += str(num) + ' '*(width-1)+'|'
				else:
					s += str(num) + ' '*(width-2)+'|'
			s+='\n'
			s+= ('|'+(' '*width+'|')*5+'\n')
			s+='|'
			for j in range(5):
				num = (3-i)+3*j
				strng = self.farmyard.str_space(num-1)
				s += ' '*((width-len(strng))/2)+ strng + ' '*((width-len(strng)+1)/2) + '|'
			s+='\n'
			s+= ('|'+(' '*width+'|')*5+'\n')
		s += '-'+'-'*((width+1)*5)+'\n'
		print s
	
	def get_name(self):
		return self.name
	
	def get_family(self):
		return self.family
	
	def add_resource(self,r,a):
		if r == 0:
			self.food += a
		elif r == 1:
			self.wood += a
		elif r == 2:
			self.clay += a
		elif r == 3:
			self.reed += a
		elif r == 4:
			self.stone += a
		elif r == 5:
			self.grain += a
		elif r == 6:
			self.vegetable += a
		elif r == 7:
			self.sheep += a
		elif r == 8:
			self.boar += a
		elif r == 9:
			self.cattle += a

	def pay_resource(self,r,a):
		if r == 0:
			self.food -= a
		elif r == 1:
			self.wood -= a
		elif r == 2:
			self.clay -= a
		elif r == 3:
			self.reed -= a
		elif r == 4:
			self.stone -= a
		elif r == 5:
			self.grain -= a
		elif r == 6:
			self.vegetable -= a
		elif r == 7:
			self.sheep -= a
		elif r == 8:
			self.boar -= a
		elif r == 9:
			self.cattle -= a

	#return value of that resource
	def get_resource(self,r):
		if r == 0:
			return self.food
		elif r == 1:
			return self.wood
		elif r == 2:
			return self.clay
		elif r == 3:
			return self.reed
		elif r == 4:
			return self.stone
		elif r == 5:
			return self.grain
		elif r == 6:
			return self.vegetable
		elif r == 7:
			return self.sheep
		elif r == 8:
			return self.boar
		elif r == 9:
			return self.cattle
	
	def add_food(self,n):
		self.food+=n

	def pay_food(self,n):
		self.food-=n

	def add_wood(self,n):
		self.wood+=n

	def pay_wood(self,n):
		self.wood-=n

	def add_clay(self,n):
		self.clay+=n

	def pay_clay(self,n):
		self.clay-=n

	def add_reed(self,n):
		self.reed+=n

	def pay_reed(self,n):
		self.reed-=n

	def add_stone(self,n):
		self.stone+=n

	def pay_stone(self,n):
		self.stone-=n

	def add_grain(self,n):
		self.grain+=n

	def pay_grain(self,n):
		self.grain-=n

	def add_vegetable(self,n):
		self.vegetable+=n

	def pay_vegetable(self,n):
		self.vegetable-=n

	def add_sheep(self,n):
		self.sheep+=n

	def pay_sheep(self,n):
		self.sheep-=n

	def add_boar(self,n):
		self.boar+=n

	def pay_boar(self,n):
		self.boar-=n

	def add_cattle(self,n):
		self.cattle+=n

	def pay_cattle(self,n):
		self.cattle-=n

class Agricola(object):
	'''
	Variables
		players - list of Player objects, one for each person playing the game, in order of turns (but starting with starting player)
		starting_player - index of the current starting player
		current_player - index of the current player (the one taking their turn)
		actions - list of actions now on the board (/not/ the list of actions still available for play), each action represented by an Action object
		stores - list of integers, one for each store of resources, representing how much is currently there
		dstores - list of integers, one for each store of resources, representing how much it is replenished per round currently
	'''
	
	def __init__(self):
		self.players=[]
		self.actions=[]
		self.stores=[0]*9 #*for now: wood_1,clay_1,reed_1,fish,sheep,stone_1,boar,stone_2,cattle
		self.dstores=[0]*9
		#still need to add the >=3 player action space stores
	
	#########################################
	# Player Action Functions
	#########################################
	
	#initially available actions:
	
	def build_rooms_stables(self):
		print "Your farmyard looks like this:"
		self.players[self.current_player].print_farmyard()

	def starting_minor(self):
		pass

	def take_grain(self):
		self.players[self.current_player].add_grain(1)

	def plow_field(self):
		print "Your farmyard looks like this:"
		self.players[self.current_player].print_farmyard()

	def occupation(self):
		pass

	def daylabour(self):
		pass

	def take_wood(self):
		self.players[self.current_player].add_wood(self.stores[0])
		self.stores[0]=0

	def take_clay(self):
		self.players[self.current_player].add_clay(self.stores[1])
		self.stores[1]=0

	def take_reed(self):
		self.players[self.current_player].add_reed(self.stores[2])
		self.stores[2]=0

	def take_fish(self):
		self.players[self.current_player].add_food(self.stores[3])
		self.stores[3]=0
	
	#round card actions:
	
	def sow_bake(self):
		pass

	def major_minor(self):
		pass

	def take_sheep(self):
		self.players[self.current_player].add_sheep(self.stores[4])
		self.stores[4]=0

	def fences(self):
		max_fences = self.players[self.current_player].get_wood()
		print "Your farmyard looks like this:"
		self.players[self.current_player].print_farmyard()
		print "You can place at most %d fences."%max_fences

	def take_stoneA(self):
		self.players[self.current_player].add_wood(self.stone[5])
		self.stores[5]=0

	def renovate_major_minor(self):
		pass

	def family_minor(self):
		pass

	def take_vegetable(self):
		self.players[self.current_player].add_vegetable(1)
		
	def take_boar(self):
		self.players[self.current_player].add_boar(self.stores[6])
		self.stores[6]=0
		
	def take_stoneB(self):
		self.players[self.current_player].add_stone(self.stores[7])
		self.stores[7]=0

	def take_cattle(self):
		self.players[self.current_player].add_cattle(self.stores[8])
		self.stores[8]=0

	def plow_sow(self):
		pass

	def family_noroom(self):
		pass

	def renovate_fences(self):
		pass
	
	#########################################
	#
	#########################################
	
	#each action is a pair function
	#initial store replenishment variables are set here (i.e. replenish 2/3 wood, replenish 1 clay, etc.)
	def load_actions(self):
		#*add these in
		if len(self.players) >= 3:
			pass
		if len(self.players) >= 4:
			pass
		if len(self.players) >= 5:
			pass
		self.actions+=[
			Action("Build Rooms and/or Stables",self.build_rooms_stables),
			Action("Starting Player and/or Minor Improvement",self.starting_minor),
			Action("Take 1 Grain",self.take_grain),
			Action("Plow 1 Field",self.plow_field),
			Action("Occupation",self.occupation),
			Action("Daylabourer",self.daylabour),
			Action("Take Wood",self.take_wood,0),
			Action("Take Clay",self.take_clay,1),
			Action("Take Reed",self.take_reed,2),
			Action("Take Fish",self.take_fish,3)]
		#wood replenishment depends on if solo game or not
		if len(self.players) == 1:
			self.dstores[0]=2#wood
		else:
			self.dstores[0]=3#wood
		self.dstores[1]=1 #clay
		self.dstores[2]=1 #reed
		self.dstores[3]=1 #fish

	def load_rounds(self):
		stage1 = [
			Action("Sow and/or Bake Bread",self.sow_bake),
			Action("Major or Minor Improvement",self.major_minor),
			Action("Take Sheep",self.take_sheep,4),
			Action("Fences",self.fences)]
		stage2 = [
			Action("Take Stone A",self.take_stoneA,5),
			Action("After Renovating, a Major or Minor Improvement ",self.renovate_major_minor),
			Action("After Family Growth, a Minor Improvement",self.family_minor)]
		stage3 = [
			Action("Take One Vegetable",self.take_vegetable),
			Action("Take Board",self.take_boar,6)]
		stage4 = [
			Action("Take Stone B",self.take_stoneB,7),
			Action("Take Cattle",self.take_cattle,8)]
		stage5 = [
			Action("Plow and/or Sow",self.plow_sow),
			Action("Family Growth without Room",self.family_noroom)]
		stage6 = [
			Action("After Renovating, Fences",self.renovate_fences)]
		random.shuffle(stage1)
		random.shuffle(stage2)
		random.shuffle(stage3)
		random.shuffle(stage4)
		random.shuffle(stage5)
		order = stage1+stage2+stage3+stage4+stage5+stage6
		self.rounds=[]
		for ri in range(14):
			self.rounds.append(Round(order[ri]))
		self.rounds[3].set_harvest()
		self.rounds[6].set_harvest()
		self.rounds[8].set_harvest()
		self.rounds[10].set_harvest()
		self.rounds[12].set_harvest()
		self.rounds[13].set_harvest()

	#return a 2D list, with one list per player of 7 occupations
	def load_occupations(self):
		pass

	def load_minor_improvements(self):
		pass

	def play_round(self,Round):
		#start if applicable
		for start in Round.get_start():
			if action[0] == 0:#receive resource
				self.players[start[3]].add_resource(start[1],start[2])
			elif start[0] == 1:#non-resource action (e.g. plow field)
				if self.players[start[4]].get_resource(start[2]) < start[3]:
					print self.players[start[4]].get_name() + ' does not have enough resources to take this action.'
				else:
					perform = None
					while not perform in ['y','n']:
						perform = raw_input("Do you want to %s? (y/n) ")
						if not perform in ['y','n']:
							print 'Unrecognized response.'
					if perform == 'y':
						start[1]() #call the action
						self.players[start[4]].pay_resource(start[2],start[3]) #pay 1 food
		#add action
		new_action = Round.get_action()
		self.actions.append(new_action)
		if new_action.get_store():
			self.dstores[new_action.get_store()] = 1
		#replenish
		for si in range(len(self.stores)):
			self.stores[si]+=self.dstores[si]
		#determine turn order
		t = 0
		i = self.starting_player
		turns = []
		out_of_family = 0
		while out_of_family < len(self.players):
			if i == self.starting_player:
				out_of_family = 0
				t+=1
			if t <= self.players[i].get_family():
				turns.append(i)
			else:
				out_of_family+=1
			i = (i+1)%len(self.players)
		#play each turn
		print "Turns for this round: ", turns
		played_actions=[]#list of indices of actions (in self.actions) that have been played this round
		for p in turns:
			#p is the player index whose turn it is
			self.current_player = p
			print "Current player: "+self.players[p].get_name()
			print "Current stores: ",self.stores
			
			s = 'Available non-game actions:\n'
			s += '\tf. View Farm Yard\n'
			s += 'Available game actions:\n'
			ai = 0
			for a in self.actions:
				if not ai in played_actions:
					s += '\t%d. %s'%(ai,a)
					if a.get_store() >= 0:
						s+=' (%d units)'%self.stores[a.get_store()]
					s += '\n'
				ai += 1
			print s
			acceptable = False
			while not acceptable:
				action_selection = raw_input('\nWhich action would you like to perform? ')
				if action_selection in ['f']:
					if action_selection == 'f':
						print "Your farmyard looks like this:"
						self.players[self.current_player].print_farmyard()
						raw_input("Press any key to continue.")
				else:
					action_selection = int(action_selection)
					if action_selection in range(len(self.actions)) and not action_selection in played_actions:
						self.actions[action_selection].get_func()()#do that action
						played_actions.append(action_selection)#make it unplayable for the rest of this round
						acceptable = True
					else:
						print "Unrecognized or unavailable action."
				
			
		#harvest if applicable
		if Round.harvest:
			self.harvest()
		raw_input("Round Complete. Press any key to continue...")
	
	def harvest(self):
		pass
		#field phase
		#feed phase
		#breed phase
	
	def start_game(self):
		#initialize
		num_p = -1
		while num_p < 1 or num_p != int(num_p):
			num_p = int(raw_input("How many players are there?\n"))
			if num_p < 1:
				print "The number of players must be at least one."
			elif num_p != int(num_p):
				print "The number of players must be an integer."
		names=[]
		if num_p > 1:
			print "Note that the play order will be determined by the order in which you enter the player names now.\n For instance, with 3 players, and player 2 as starting player, then player 3 will go second, then player 1."
		for i in range(1,num_p+1):
			names.append(raw_input("Please enter name for player %d: "%i))
		if num_p > 1:
			self.starting_player = int(raw_input("Please enter who will be the starting player (1-%d) or -1 for random: "%num_p))
			if not (1 <= self.starting_player <= num_p):
				self.starting_player=random.randint(1,num_p)
				print "Randomly selected starting player: Player %d"%self.starting_player
			self.starting_player-=1 #indexing starts at 0
			self.players=[]
			for p in range(num_p):
				food = 3
				if p == self.starting_player:
					food = 2
				self.players.append(Player(n=names[p],f=food))
		else: #if num_p == 1:
			self.starting_player=0
			self.players.append(Player(n=names[0]))
		for P in self.players:
			print P		
		#load actions
		self.load_actions()
		#load then play 14 rounds
		self.load_rounds()
		for r in self.rounds[0:1]:#*just for testing, only do first round
			#print r.get_action()
			self.play_round(r)
		#calculate scores and print them
		pass
		for P in self.players:
			print P
		return

game=Agricola()
game.start_game()