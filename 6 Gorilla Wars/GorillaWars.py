from Tkinter import *
from random import randint
import math
import time

class Gorilla(object):

	def __init__(self,x=0,y=0):
		self.x = x
		self.y = y
		self.width = 10
		self.height = 10
		self.health = 100
		

class GorillaWars(Frame):

	def __init__ (self,master=None):
		#initialize variables
		self.width = 600
		self.height = 300
		self.numB = 10 #number of buildings
		self.sepB = 20 #the separation between 2 buildings (pxls)
		self.widB = (self.width-self.sepB) / (self.numB) #width including separation
		self.p1 = Gorilla()
		self.p2 = Gorilla()
		
		#initialize 
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()
		
#		self.c.bind('<Button-1>',self.onSingleClick)
		
		##execute games
		
		#create landscape
		self.createLandscape()
		
		#place players
		temp = randint(1,self.numB*3/10)
		self.p1.x = temp*self.widB-self.widB/2+self.p1.width/2		
		self.p1.y = self.land[temp-1]+self.p1.height+1
		temp = randint(self.numB*7/10,self.numB)
		self.p2.x = temp*self.widB-self.widB/2+self.p1.width/2
		self.p2.y = self.land[temp-1]+self.p2.height+1
				
		##execute turns
		
		#redraw landscape
		self.drawLandscape()
		
	#def onSingleClick(self,event):
	#	print event.x, '\t', event.y
	#	self.throwBanana(80,math.pi/4)

	def createWidgets(self):
		self.c = Canvas(self,width=self.width,height=self.height)
		self.c.pack({'side':'top'})
		self.c.create_rectangle(0,0,self.width,self.height,fill="blue")

		row = Frame(self)
		row.pack(side=BOTTOM)
		
		self.PowerL = Label(row,text='Power: ')
		self.PowerL.pack(side=LEFT)
		
		self.PowerE = Entry(row)
		self.PowerE.pack(side=LEFT)
		
		self.AngleL = Label(row,text='Angle: ')
		self.AngleL.pack(side=LEFT)

		self.AngleE = Entry(row)
		self.AngleE.pack(side=LEFT)
		
		self.Throw = Button(row)
		self.Throw['text']='Throw Banana'
		self.Throw['command'] = self.throwBanana
		self.Throw.pack(side=LEFT)
		
		self.Quit = Button(row)
		self.Quit['text']='Quit'
		#self.Quit['fg']='red'
		self.Quit['command'] = self.quit
		self.Quit.pack(side=LEFT)

	def createLandscape(self):
		self.land = []
		for i in range(self.numB):
			self.land.append(randint(self.height/10,self.height*4/5))
		
	def drawLandscape(self):
		for i in range(len(self.land)):
			x = i*self.widB+self.sepB
			self.c.create_rectangle(x,self.height-self.land[i],x+self.widB-self.sepB,self.height,fill="grey")
		self.c.create_oval(self.p1.x,self.height - self.p1.y,self.p1.x+self.p1.width,self.height - (self.p1.y-self.p1.height),fill='black')
		self.c.create_oval(self.p2.x,self.height - self.p2.y,self.p2.x+self.p2.width,self.height - (self.p2.y-self.p2.height),fill='black')

	def throwBanana (self):
		power = int(self.PowerE.get())
		angle = int(self.AngleE.get())*math.pi/180
		sx1 = self.p1.x+9
		sy1 = self.p1.y+9
		sx2 = sx1+1
		sy2 = sy1+1
		vx = power*math.cos(angle)
		vy = power*math.sin(angle)/vx
		ax = 0
		ay = -9.8/vx/vx
		vx = 1
		hit = False
		while not hit and not sx1 > self.width:
			b = sx2/self.widB #building launching from
			sx1=sx2
			sy1=sy2
			sx2+=vx
			sy2+=vy
			vx+=ax
			vy+=ay
			#print b,'\t',sy2,'\t',self.land[b-1]
			hit = ((sx2%self.widB > self.sepB) and (sy2 < self.land[b])) or (sx2+10 > self.width)
			#self.c.create_line(sx1,self.height-sy1,sx2,self.height-sy2)
			self.c.create_oval(sx1,self.height-sy1,sx1+5,self.height-(sy1+5),outline='blue',fill='blue')
			self.c.create_oval(sx2,self.height-sy2,sx2+5,self.height-(sy2+5),outline='yellow',fill='yellow')
			self.c.update_idletasks() #updates canvas before returning to mainloop
			time.sleep(0.01) #delay for 0.01 seconds
		self.c.create_oval(sx2-7,self.height-sy2+7,sx2+7,self.height-(sy2+7),outline='blue',fill='blue')

root = Tk()
GW = GorillaWars(master=root)
GW.mainloop()
root.destroy()