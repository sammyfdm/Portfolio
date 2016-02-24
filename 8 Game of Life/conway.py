from Tkinter import *
from random import randint
import math
import time

class Conway(Frame):

	def __init__ (self,master=None):
		#initialize variables
		self.width = 600
		self.height = 600
		self.pixwid = 5
		self.life = []
		for row in range(self.height/self.pixwid):
			temp = []
			for col in range(self.width/self.pixwid):
				temp.append(randint(0,1))
			self.life.append(temp)
		
		#initialize
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()
		
		self.c.bind('<Button-1>',self.onSingleClick)
				
		#run
		self.sim()
		suml=0
		for row in range(self.height/self.pixwid):
			for col in range(self.width/self.pixwid):
				suml += self.life[row][col]
		print suml
		
	def onSingleClick(self,event):
		for i in range(100):
			self.sim()
			suml=0
			for row in range(self.height/self.pixwid):
				for col in range(self.width/self.pixwid):
					suml += self.life[row][col]
			print suml
		#	print event.x, '\t', event.y

	def createWidgets(self):
		self.c = Canvas(self,width=self.width,height=self.height)
		self.c.pack({'side':'top'})
		self.c.create_rectangle(0,0,self.width,self.height,fill="white")

		row = Frame(self)
		row.pack(side=BOTTOM)

	def sim (self):
		self.c.create_rectangle(0,0,self.width,self.height,fill='white')
		NN = []
		for row in range(self.height/self.pixwid):
			temp = []
			for col in range(self.width/self.pixwid):
				temp.append(self.numNeighbours(row,col))
			NN.append(temp)
			
		self.c.delete(ALL)
		self.c.create_rectangle(1,1,self.width,self.height,fill='white')
		tempNN = []
		for row in range(self.height/self.pixwid):
			temp_row=[]
			for col in range(self.width/self.pixwid):
				x = col*self.pixwid
				y = row*self.pixwid
				if self.life[row][col]:
					self.c.create_rectangle(x,y,x+self.pixwid,y+self.pixwid,fill='black')
				nn = NN[row][col]
				if self.life[row][col] and nn != 2 and nn != 3:
					#self.life[row][col] = 0
					temp_row.append(0)
				elif not self.life[row][col] and nn == 3:
					#self.life[row][col] = 1
					temp_row.append(1)
				else:
					temp_row.append(self.life[row][col])
			tempNN.append(temp_row)
		for row in range(self.height/self.pixwid):
			self.life[row][:]=tempNN[row][:]
		#print b,'\t',sy2,'\t',self.land[b-1]
		#self.c.create_line(sx1,self.height-sy1,sx2,self.height-sy2)
		#self.c.create_oval(sx1,self.height-sy1,sx1+5,self.height-(sy1+5),outline='blue',fill='blue')
		self.c.update_idletasks() #updates canvas before returning to mainloop
		#time.sleep(1) #delay for __ seconds

	def numNeighbours(self,row,col):
		nn = 0
		nR = self.height/self.pixwid
		nC = self.width/self.pixwid
		nn += self.life[(row-1)%nR][(col-1)%nC]
		nn += self.life[(row-1)%nR][col]
		nn += self.life[(row-1)%nR][(col+1)%nC]
		nn += self.life[row][(col-1)%nC]
		nn += self.life[row][(col+1)%nC]
		nn += self.life[(row+1)%nR][(col-1)%nC]
		nn += self.life[(row+1)%nR][col]
		nn += self.life[(row+1)%nR][(col+1)%nC]
		return(nn)

root = Tk()
life = Conway(master=root)
life.mainloop()
root.destroy()