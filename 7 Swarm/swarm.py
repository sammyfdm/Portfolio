from Tkinter import *
from random import random
from math import sqrt
import time

class Swarm(Frame):
	
	def __init__(self,master=None,numI=10, c=100,v=40):
		#init variables
		self.width = 600
		self.height = 600
		self.cycles = c
		self.vision = v
		self.insects = []
		for i in xrange(numI):
			self.insects.append([[0,0,0],[0,0,0]])
		
		#init frame, canvas
		Frame.__init__(self,master)
		self.pack()
		self.c = Canvas(self,width=self.width,height=self.height)
		self.c.pack()
		self.c.create_rectangle(10,10,self.width-10,self.height-10)
		
		#createI(insects,v)
		for i in xrange(numI):
			self.insects[i][0][0] = random()*2*v + self.width/2
			self.insects[i][0][1] = random()*2*v + self.height/2
			self.insects[i][0][2] = random()*2*v - v/2
		
		#run(cycles,insects)
		for cyc in xrange(self.cycles):
			for i in xrange(numI):
				self.update(i)
			self.draw()
	
	def dist(self,s1,s2):
		s = (s2[0] - s1[0])*(s2[0] - s1[0])
		s = s + (s2[1] - s1[1])*(s2[1] - s1[1])
		s = s + (s2[2] - s1[2])*(s2[2] - s1[2])
		return(sqrt(s))
	
	def createI(self):
		pass
	
	def update(self,i):
		#weight on individual velocity vector
		e = 0.05
		#keep 20% of previous velocity
		self.insects[i][1][0] = self.insects[i][1][0]*0.2
		self.insects[i][1][1] = self.insects[i][1][1]*0.2
		self.insects[i][1][2] = self.insects[i][1][2]*0.2
		#add velocity vectors towards other insects in visual range
		for j in xrange(len(self.insects)):
			if i != j:
				if self.dist(self.insects[i][0],self.insects[j][0]) < self.vision:
					print random()*self.vision/4
					self.insects[i][1][0] = self.insects[i][1][0] + e*(self.insects[i][0][0]-self.insects[j][0][0])
					self.insects[i][1][1] = self.insects[i][1][1] + e*(self.insects[i][0][1]-self.insects[j][0][1])
					self.insects[i][1][2] = self.insects[i][1][2] + e*(self.insects[i][0][2]-self.insects[j][0][2])
		self.insects[i][0][0] = self.insects[i][0][0] + self.insects[i][1][0] + (random()-0.5)*self.vision/4
		self.insects[i][0][1] = self.insects[i][0][1] + self.insects[i][1][1] + (random()-0.5)*self.vision/4
		self.insects[i][0][2] = self.insects[i][0][2] + self.insects[i][1][2] + (random()-0.5)*self.vision/4
	
	def draw(self):
		print 'draw'
		self.c.create_rectangle(0,0,self.width,self.height,fill="white")
		for i in xrange(len(self.insects)):
			#project onto 2D
			x = int(self.insects[i][0][0])
			y = int(self.insects[i][0][1])
			#draw
			self.c.create_oval(x,self.height-y,x+5,self.height-(y+5),outline='black')#,fill='grey')
		self.c.update_idletasks() #updates canvas before returning to mainloop
		time.sleep(0.1) #delay for 0.01 seconds

root = Tk()
swarm1 = Swarm(master=root,numI=20,c=100)
swarm1.mainloop()
swarm1.destroy()