'''
to do easily:
	-add draw function for each store (so everything has oval except animals which have rectangle, and able to use food image for food; each one just passes in the x0,y0,x1,y1 coordinates)
to do at some point:
	-keyboard shortcuts (event handler in Agricola class)
	-save/load games (look at tkFileDialog module)
'''

import sys
import random
from Tkinter import *
import tkMessageBox
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
	
	def __init__(self,action=None,image=None,colour=None,h=False):
		self.start=[]
		self.action=action
		self.image=image
		self.colour=colour
		self.harvest=h
	
	def add_start(self,action):
		self.start.append(action)
	
	def get_start(self):
		return self.start
	
	def set_action(self,action):
		self.action=action
	
	def get_action(self):
		return self.action
	
	def set_image(self,i):
		self.image=i
	
	def get_image(self):
		return self.image

	def set_colour(self,c):
		self.colour=c
	
	def get_colour(self):
		return self.colour
	
	def set_harvest(self):
		self.harvest=True

	def get_harvest(self):
		return self.harvest
	
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
	xy :=
		-3D list of x,y values for spaces
		-[[[x11,y11],[x21,y21],[x31,y31]],[[x12,y12],[x22,y22],[x32,y32]],...]
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
		self.xy = []
		for ci in range(5):
			col = []
			for ri in range(3):
				#50+45*ci,125-45*ri
				col.append([10+45*ci,165-45*ri]) #bottom left corner
				#[0,30,145],[0,30,100]
			self.xy.append(col)
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
	

class Player(object):
	
	def __init__(self,n='',f=0,w=0,c=0,r=0,s=0,g=0,v=0,sh=0,b=0,ca=0,colour='green'):
		self.name=n
		self.colour=colour
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
		s+='     Colour:          %s\n'%self.colour
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
	
	def draw_farmyard(self,Canvas):
		pass
	
	def get_name(self):
		return self.name
	
	def get_colour(self):
		return self.colour
	
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

class Agricola(Frame):
	'''
	Variables
		players - list of Player objects, one for each person playing the game, in order of turns (but starting with starting player)
		starting_player - index of the current starting player
		current_player - index of the current player (the one taking their turn)
		actions - list of actions now on the board (/not/ the list of actions still available for play), each action represented by an Action object
		stores - list of integers, one for each store of resources, representing how much is currently there
		dstores - list of integers, one for each store of resources, representing how much it is replenished per round currently
		player_tokens - [player #][token #][0=>board, 1=>x, 2=>y] the board number is 1 if token on main board and 0 if on player's farmyard
	'''
	#initialize GUI
	def __init__(self,master=None):
		#self
		Frame.__init__(self,master)
		
		self.current_player=-1
		
		#Splash Frame
		self.splash_frame=Toplevel()
		self.splash_frame.title("Agricola")
		#self.splash_frame.grid(row=0,column=0)
		
		self.splash_bg = PhotoImage(file='images/cover.gif')
		old_width=self.splash_bg.width()
		old_height=self.splash_bg.height()
		self.splash_canvas=Canvas(self.splash_frame,width=old_width,height=old_height)
		self.splash_canvas.pack(expand=True,fill=BOTH)
		self.splash_canvas.create_image(0,0,anchor=NW,image=self.splash_bg)
		
		self.controls_frame=Frame(master=self.splash_canvas)
		#self.controls_frame.grid(row=0,column=0)
		self.new_game_button = Button(self.splash_canvas,text='New Game',command=self.start_game_1)
		#self.new_game_button.grid(row=0,column=0)
		self.quit_button = Button(self.splash_canvas,text='Quit',command=self.quit)
		#self.quit_button.grid(row=0,column=1)
		self.splash_canvas.create_window(old_width/2,old_height/2-25,window=self.new_game_button,anchor=CENTER)
		self.splash_canvas.create_window(old_width/2,old_height/2+25,window=self.quit_button,anchor=CENTER)
				
		#Board Frame
		self.main_board_frame=Toplevel()
		self.main_board_frame.title("Agricola")
		#self.main_board_frame.grid(row=0,column=0)
		
		self.board_all = PhotoImage(file='images/board_all.gif')
		old_width = self.board_all.width()
		old_height = self.board_all.height()
		self.main_board_canvas=Canvas(self.main_board_frame,width=old_width,height=old_height)
		self.main_board_canvas.grid(row=0,column=0)
		self.main_board_canvas.create_image(0,0,image=self.board_all,anchor=NW)
		
		self.action_space_x = [0,83,163,250,340,416,500,580,655,733,820,917,988,1060,1130,old_width]
		self.action_space_y = [0,60,120,180,240,300,old_height]
		self.action_at_xy = {}
		#for xi in range(len(self.action_space_x)-1):
		#	for yi in range(len(self.action_space_y)-1):
		#		self.main_board_canvas.create_rectangle(self.action_space_x[xi],self.action_space_y[yi],self.action_space_x[xi+1],self.action_space_y[yi+1],fill='#%d%d%d'%(xi%7+2,xi%7+2,xi%7+2))
		self.round_to_x = {0:295,1:380,2:380,3:380,4:460,5:460,6:460,7:540,8:540,9:620,10:620,11:700,12:700,13:775}
		self.round_to_y = {0:60,1:60,2:175,3:290,4:60,5:175,6:290,7:60,8:175,9:60,10:175,11:60,12:175,13:60}
		self.store_x = [285,315,285,310]
		self.store_y = [140,200,260,320]
		self.store_colour = ['brown','red','white','yellow']#wood_1,clay_1,reed_1,fish,sheep,stone_1,boar,stone_2,cattle
		self.token_size = 15
		
		self.controls_frame=Frame(master=self.main_board_frame)
		self.controls_frame.grid(row=1,column=0)
		self.new_game_button = Button(self.controls_frame,text='New Game',command=self.start_game_1)
		self.new_game_button.grid(row=0,column=0)
		self.quit_button = Button(self.controls_frame,text='Quit',command=self.quit)
		self.quit_button.grid(row=0,column=1)
		self.main_menu_button=Button(self.controls_frame,text="Return to Main Menu",command=self.return_to_main)
		self.main_menu_button.grid(row=0,column=2)
		self.take_back_action_button = Button(self.controls_frame,text='Take Back Action',command=self.take_back_action)
		self.take_back_action_button.grid(row=0,column=4)
		
		self.main_board_canvas.bind("<1>",self.take_action)
		
		self.main_board_frame.withdraw()
		
		#Player number/name/colour selection frame
		self.player_info_frame=Toplevel()
		self.player_info_frame.title('Player Information')
		
		#Number of Players
		self.num_players_label = Label(self.player_info_frame,text='Number of players:')
		self.num_players_label.grid(row=0,column=0)
		self.num_players_radio_frame=Frame(self.player_info_frame)
		self.num_players_radio_frame.grid(row=0,column=1)
		self.num_players_var=IntVar()
		self.num_players_radio=[]
		for i in range(5):
			self.num_players_radio.append(Radiobutton(self.num_players_radio_frame,text=str(i+1),value=(i+1),variable=self.num_players_var,command=self.change_player_num))
			self.num_players_radio[i].grid(row=0,column=i)
		self.num_players_radio[0].select()

		#Starting Player
		self.start_player_label = Label(self.player_info_frame,text='Starting player:')
		self.start_player_label.grid(row=1,column=0)
		self.start_player_radio_frame=Frame(self.player_info_frame)
		self.start_player_radio_frame.grid(row=1,column=1)
		self.start_player_var=IntVar()
		self.start_player_radio=[]
		for i in range(5):
			self.start_player_radio.append(Radiobutton(self.start_player_radio_frame,text=str(i+1),value=(i+1),variable=self.start_player_var,state=DISABLED))
			self.start_player_radio[i].grid(row=0,column=i)
		self.start_player_radio.append(Radiobutton(self.player_info_frame,text='Random',value=-1,variable=self.start_player_var,state=DISABLED))
		self.start_player_radio[5].grid(row=1,column=2)
		self.start_player_radio[0].configure(state=NORMAL)
		self.start_player_radio[0].select()
		
		#Player Names
		self.player_labels=[]
		for i in range(5):
			self.player_labels.append(Label(self.player_info_frame,text="Player %d Name: "%(i+1)))
			self.player_labels[i].grid(row=i+2,column=0)
		
		self.player_name_vars=[]
		self.player_name_entries=[]
		for i in range(5):
			self.player_name_vars.append(StringVar())
			self.player_name_entries.append(Entry(self.player_info_frame,width=30,state=DISABLED,disabledbackground='#eee',relief=SUNKEN,textvariable=self.player_name_vars[i]))
			self.player_name_entries[i].grid(row=(i+2),column=1)
		self.player_name_entries[0].configure(state=NORMAL)
		
		#Player Colours
		self.colour_labels_frame=Frame(self.player_info_frame)
		self.colour_labels_frame.grid(row=7,column=0)
		
		self.player_colour_labels=[]
		for i in range(5):
			self.player_colour_labels.append(Label(self.colour_labels_frame,text="Player %d Colour: "%(i+1)))
			self.player_colour_labels[i].grid(row=i+1,column=0)
		
		self.colours=['green','blue','red','white','purple']
		
		self.colours_radio_frame=Frame(self.player_info_frame)
		self.colours_radio_frame.grid(row=7,column=1)
		self.colour_labels = []
		for i in range(5):
			self.colour_labels.append(Label(self.colours_radio_frame,text=self.colours[i]))
			self.colour_labels[i].grid(row=0,column=i)

		self.colours_fun=[self.change_player_colour_1,self.change_player_colour_2,self.change_player_colour_3,self.change_player_colour_4,self.change_player_colour_5]
		self.colours_var=[]
		self.colours_radio=[]
		for pi in range(5):
			self.colours_var.append(IntVar())
			self.colours_radio.append([])
			for ci in range(5):
				self.colours_radio[pi].append(Radiobutton(self.colours_radio_frame,text='',value=ci,variable=self.colours_var[pi],command=self.colours_fun[pi]))
				self.colours_radio[pi][ci].grid(row=pi+1,column=ci)
				if pi > 0:
					self.colours_radio[pi][ci].configure(state=DISABLED)
			self.colours_radio[pi][pi].select()
		
		#Buttons
		#self.player_info_button_frame=Frame(self.player_info_frame)
		#self.player_info_button_frame.grid(row=7,column=1)
		self.continue_button=Button(self.player_info_frame,text="Start Game",command=self.collect_player_info)
		self.continue_button.grid(row=8,column=1)
		self.main_menu_button=Button(self.player_info_frame,text="Return to Main Menu",command=self.return_to_main)
		self.main_menu_button.grid(row=9,column=1)
		self.continue_button=Button(self.player_info_frame,text="Exit Program",command=self.quit)
		self.continue_button.grid(row=10,column=1)
		
		self.player_info_frame.withdraw()
	
	def return_to_main(self):
		self.main_board_frame.withdraw()
		self.player_info_frame.withdraw()
		self.splash_frame.deiconify()
	
	def change_player_num(self):
		#print self.num_players_var.get()
		for i in range(self.num_players_var.get()):
			self.start_player_radio[i].configure(state=NORMAL)
			self.player_name_entries[i].configure(state=NORMAL)
		for i in range(self.num_players_var.get(),5):
			self.start_player_radio[i].configure(state=DISABLED)
			self.player_name_entries[i].configure(state=DISABLED)
		if self.start_player_var.get() > self.num_players_var.get():
			self.start_player_radio[self.num_players_var.get()-1].select()
		#disable/enable random starting player option if number of players is =/> 1
		if self.num_players_var.get() > 1:
			self.start_player_radio[5].configure(state=NORMAL)
		else:
			self.start_player_radio[5].configure(state=DISABLED)
		#disable/enable colour choices
		for pi in range(self.num_players_var.get()):
			for ci in range(5):
				self.colours_radio[pi][ci].configure(state=NORMAL)
				#self.player_name_entries[i].configure(state=NORMAL)
		for pi in range(self.num_players_var.get(),5):
			for ci in range(5):
				self.colours_radio[pi][ci].configure(state=DISABLED)
				#self.player_name_entries[i].configure(state=DISABLED)

	def change_player_colour(self,pi):
		selected=[]
		for i in range(pi)+range(pi+1,5):
			selected.append(self.colours_var[i].get())
		selected[pi:pi]=[-1]
		missing=range(5)
		for n in selected[:pi]+selected[pi+1:]:
			missing.remove(n)
		self.colours_radio[selected.index(self.colours_var[pi].get())][missing[0]].select()

	def change_player_colour_1(self):
		self.change_player_colour(0)

	def change_player_colour_2(self):
		self.change_player_colour(1)

	def change_player_colour_3(self):
		self.change_player_colour(2)

	def change_player_colour_4(self):
		self.change_player_colour(3)

	def change_player_colour_5(self):
		self.change_player_colour(4)

	def collect_player_info(self):
		if self.start_player_var.get() > 0:
			self.starting_player=self.start_player_var.get()-1
		else:
			self.starting_player=random.randint(0,4)
		self.players=[]
		self.player_tokens=[]
		for pi in range(self.num_players_var.get()):
			food=2+(pi != self.starting_player-1)-3*(self.num_players_var.get()==1)
			self.players.append(Player(n=self.player_name_entries[pi].get(),f=food,colour=self.colours[self.colours_var[pi].get()]))
			self.player_tokens.append([[0,30,145],[0,30,100]])
		for P in self.players:
			print P
		
		self.player_info_frame.withdraw()
		self.main_board_frame.deiconify()
		self.start_game_2()

	def init_player_farms(self):
		self.farms_frame = Frame(master=self.main_board_frame)
		self.farms_frame.grid(row=2,column=0)
		self.farms=[]
		self.farms_canvas=[]
		self.farm_images=[]
		for i in range(len(self.players)):
			self.farms.append(Frame(master=self.farms_frame))
			self.farms[i].grid(row=0,column=i)
			#self.farmimage = Frame(master=self.main)
			#self.farmimage.pack()
			#image = Image.open("images/farm.jpg")
			self.farm_images.append(PhotoImage(file='images/farm.gif'))
			old_width = self.farm_images[i].width()
			old_height = self.farm_images[i].height()
			#new_width = 400
			#new_height = old_height*new_width/old_width
			#image.resize((new_width,new_height))
			#empty_farm = ImageTk.PhotoImage(image)
			#empty_farm.subsample((new_width+0.0)/old_width,(new_height+0.0)/old_height)
			self.farms_canvas.append(Canvas(self.farms[i],width=old_width,height=old_height))
			self.farms_canvas[i].create_image(0,0,image=self.farm_images[i],anchor=NW)
			self.farms_canvas[i].grid(row=0,column=0)		
	
	def pixel_to_index(self,x,y):
		xi = 0
		while self.action_space_x[xi] < x:
			xi+=1
		xi-=1
		yi = 0
		while self.action_space_y[yi] < y:
			yi+=1
		yi-=1
		return(xi,yi)
	
	def take_action(self,event):
		if self.current_player==-1:
			return
		#check where mouse click happened
		(xi,yi)=self.pixel_to_index(event.x,event.y)
		print "Mouse click at pixels: ", (event.x, event.y)
		print "Mouse click at action space: ", (xi,yi)
		print "Action at that space:", self.action_at_xy.get((xi,yi),None)
		new_action = self.action_at_xy.get((xi,yi),None)
		if new_action:
			if new_action in self.played_actions:
				tkMessageBox.showwarning(title="Action Already Taken",message="The action %s has already been done this round, please select a different one."%str(new_action))
			else:
				#take appropriate steps for that action
				new_action.get_func()()#call action's function
				#draw the current player's token on this action space
				self.player_tokens[self.current_player][self.players[self.current_player].get_family()-self.family_left[self.current_player_index]] = [1,(self.action_space_x[xi]+self.action_space_x[xi+1])/2,(self.action_space_y[yi]+self.action_space_y[yi+1])/2]
				#continue the round
				self.played_actions.append(new_action)
				self.current_player=-1 #disable interaction until next player chosen
				self.play_round_2()
	
	def take_back_action(self):
		pass
	
	def draw_board(self):
		#draw main board
		self.main_board_canvas.delete(ALL)#delete everything
		self.main_board_canvas.create_image(0,0,image=self.board_all,anchor=NW)#background image
		#draw round cards
		for ri in range(self.round_number+1):
			self.main_board_canvas.create_image(self.round_to_x[ri],self.round_to_y[ri],image=self.rounds[ri].get_image(),anchor=CENTER)
		#draw store tokens
		for si in range(len(self.store_x)):
			self.main_board_canvas.create_oval(self.store_x[si]-self.token_size/2,self.store_y[si]-self.token_size/2,self.store_x[si]+self.token_size/2,self.store_y[si]+self.token_size/2,fill=self.store_colour[si])
			self.main_board_canvas.create_text(self.store_x[si]-5,self.store_y[si]-5,text=str(self.stores[si]),anchor=NW)
		#draw farmyards & player tokens
		for pi in range(len(self.players)):
			self.farms_canvas[pi].delete(ALL)#delete everything
			self.farms_canvas[pi].create_image(0,0,image=self.farm_images[pi],anchor=NW)#background image
			for ci in range(5):
				for ri in range(3):
					#xy = self.players[pi].getFarmyard().getXY(ci,ri)
					self.farms_canvas[pi].create_rectangle(10+45*ci,165-45*ri,50+45*ci,125-45*ri)
			self.players[pi].draw_farmyard(self.farms_canvas[pi])
			for fi in range(self.players[pi].get_family()):
				if self.player_tokens[pi][fi][0]: #token on main board
					self.main_board_canvas.create_oval(self.player_tokens[pi][fi][1]-self.token_size,self.player_tokens[pi][fi][2]-self.token_size,self.player_tokens[pi][fi][1]+self.token_size,self.player_tokens[pi][fi][2]+self.token_size,fill=self.players[pi].get_colour())
				else: #token on farmyard
					self.farms_canvas[pi].create_oval(self.player_tokens[pi][fi][1]-self.token_size,self.player_tokens[pi][fi][2]-self.token_size,self.player_tokens[pi][fi][1]+self.token_size,self.player_tokens[pi][fi][2]+self.token_size,fill=self.players[pi].get_colour())
	
	#########################################
	# Player Action Functions
	#########################################
	
	#initially available actions:
	
	def build_rooms_stables(self):
		pass
		
	def starting_minor(self):
		pass

	def take_grain(self):
		self.players[self.current_player].add_grain(1)

	def plow_field(self):
		pass

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
		max_fences = self.players[self.current_player].get_resource(1) #wood
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
		self.action_at_xy[(2,0)]=self.actions[0]
		self.action_at_xy[(2,1)]=self.actions[1]
		self.action_at_xy[(2,2)]=self.actions[2]
		self.action_at_xy[(2,3)]=self.actions[3]
		self.action_at_xy[(2,4)]=self.actions[4]
		self.action_at_xy[(2,5)]=self.actions[5]
		self.action_at_xy[(3,2)]=self.actions[6]
		self.action_at_xy[(3,3)]=self.actions[7]
		self.action_at_xy[(3,4)]=self.actions[8]
		self.action_at_xy[(3,5)]=self.actions[9]
		
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
			[Action("Sow and/or Bake Bread",self.sow_bake),PhotoImage(file='images/round/sow_bake.gif'),None],
			[Action("Major or Minor Improvement",self.major_minor),PhotoImage(file='images/round/major_minor.gif'),None],
			[Action("Take Sheep",self.take_sheep,4),PhotoImage(file='images/round/take_sheep.gif'),'#fdd'],
			[Action("Fences",self.fences),PhotoImage(file='images/round/fences.gif'),None]]
		stage2 = [
			[Action("Take Stone A",self.take_stoneA,5),PhotoImage(file='images/round/take_stone.gif'),'black'],
			[Action("After Renovating, a Major or Minor Improvement ",self.renovate_major_minor),PhotoImage(file='images/round/renovate_major_minor.gif'),None],
			[Action("After Family Growth, a Minor Improvement",self.family_minor),PhotoImage(file='images/round/family_minor.gif'),None]]
		stage3 = [
			[Action("Take One Vegetable",self.take_vegetable),PhotoImage(file='images/round/take_vegetable.gif'),None],
			[Action("Take Board",self.take_boar,6),PhotoImage(file='images/round/take_boar.gif'),'#222']]
		stage4 = [
			[Action("Take Stone B",self.take_stoneB,7),PhotoImage(file='images/round/take_stone.gif'),'black'],
			[Action("Take Cattle",self.take_cattle,8),PhotoImage(file='images/round/take_cattle.gif'),'#a77']]
		stage5 = [
			[Action("Plow and/or Sow",self.plow_sow),PhotoImage(file='images/round/plow_sow.gif'),None],
			[Action("Family Growth without Room",self.family_noroom),PhotoImage(file='images/round/family_noroom.gif'),None]]
		stage6 = [
			[Action("After Renovating, Fences",self.renovate_fences),PhotoImage(file='images/round/renovate_fences.gif'),None]]
		random.shuffle(stage1)
		random.shuffle(stage2)
		random.shuffle(stage3)
		random.shuffle(stage4)
		random.shuffle(stage5)
		order = stage1+stage2+stage3+stage4+stage5+stage6
		self.rounds=[]
		for ri in range(14):
			self.rounds.append(Round(action=order[ri][0],image=order[ri][1],colour=order[ri][2]))
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

	def play_round(self):
		Round = self.rounds[self.round_number]
		print 'Beginning Round #%d'%(self.round_number+1)
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
		#place round card on board and update store_x,_y,_colour
		new_action = Round.get_action()
		self.actions.append(new_action)
		(tmp_x,tmp_y)=self.pixel_to_index(self.round_to_x[self.round_number],self.round_to_y[self.round_number])
		self.action_at_xy[tmp_x,tmp_y]=new_action
		self.action_at_xy[tmp_x,tmp_y+1]=new_action
		if new_action.get_store():
			self.dstores[new_action.get_store()] = 1
			self.store_x.append(self.round_to_x[self.round_number])
			self.store_y.append(self.round_to_y[self.round_number])
			if Round.get_colour():
				self.store_colour.append(Round.get_colour())
		#replenish
		for si in range(len(self.stores)):
			self.stores[si]+=self.dstores[si]
		#prepare player info
		self.players_left=self.players[:]
		self.family_left=[]
		for p in self.players:
			self.family_left.append(p.get_family())
		self.current_player_index=self.starting_player
		self.current_player=self.starting_player
		#reset log of played actions
		self.played_actions=[]
		#draw updated board
		self.draw_board()
		
	def play_round_2(self):
		print self.current_player_index
		print self.family_left
		#remove from turns if out of family members
		if self.family_left[self.current_player_index] == 1:
			print "removed"
			self.players_left = self.players_left[:self.current_player_index]+self.players_left[self.current_player_index+1:]
			self.family_left = self.family_left[:self.current_player_index]+self.family_left[self.current_player_index+1:]
			self.current_player_index-=1
		else:
			self.family_left[self.current_player_index]-=1
		#if still players to take turns, update players and board and wait for actions
		if self.players_left:
			#increment turn index
			self.current_player_index += 1
			if self.current_player_index >= len(self.players_left):
				self.current_player_index = 0
			self.current_player=self.players.index(self.players_left[self.current_player_index])
			self.draw_board()
		else:
			self.current_player=-1 #*for disabling event listeners?
			for pi in range(len(self.players)):
				pass
			#harvest if applicable
			if self.rounds[self.round_number].get_harvest():
				self.harvest()
			self.draw_board()
			tkMessageBox.showinfo("Round #%d Complete."%(self.round_number+1),"Round #%d has been completed. Please click OK when you are ready to continue."%(self.round_number+1))
			self.round_number+=1
			if self.round_number<14:
				self.play_round()
			else:
				self.end_game()

	def harvest(self):
		pass
		#field phase
		#feed phase
			#show all options available one player at a time
			#e.g. you need to feed your family with x food, and can take the following actions:
			#	1 grain --> 1 food (or better if have baker/windmill cards)
			#	if cooking enabled then 1 vegetable --> ...
		#breed phase
	
	#return the score for player number p
	def compute_score(self,p):
		pass
	
	#go through the process of ending the game
	def end_game(self):
		#score players
		#report scores
		#high scores
		#save game log
		#play again with same players? (e.g. solo player sequence => pick occupation to save, start with x food if above target)
		print "Game Over!"
	
	
	#show screen for initializing player information
	#this screen has the button that calls start_game_2
	def start_game_1(self):
		self.splash_frame.withdraw()
		self.player_info_frame.deiconify()
		self.player_info_frame.lift()
	
	#start game play
	def start_game_2(self):
		self.actions=[]
		self.stores=[0]*9 #*for now: wood_1,clay_1,reed_1,fish,sheep,stone_1,boar,stone_2,cattle
		self.dstores=[0]*9
		#still need to add the >=3 player action space stores
		
		self.init_player_farms()
		#load actions
		self.load_actions()
		#load then play 14 rounds
		self.load_rounds()
		self.round_number=0
		self.play_round()

root = Tk()
root.withdraw()
game=Agricola(master=root)
game.mainloop()
game.destroy()
