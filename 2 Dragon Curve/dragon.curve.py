from Tkinter import *
from math import *
import time

class Pic(Frame):

	def __init__(self,master=None):
		#initialize variables
		self.w = 1000
		self.h = 700
		self.x1 = 820	#220	500		800
		self.y1 = 350	#220	500		350
		self.l = 1		#5		2		1
		self.n = 1		#iterations: 15, 16, 18
		self.fract = [(0,-1)]
		Frame.__init__(self,master)
		self.pack()
		self.c = Canvas(self,width=self.w,height=self.h)
		self.c.pack()
		
		#self.c.bind('<Button-1>',self.step)
		x = time.time()
		for i in xrange(18):
			self.step()
#			time.sleep(0.5)
			print time.time()-x
			x = time.time()

	def step(self):
		for l in self.fract[::-1]:
			self.fract.append((l[1],-l[0]))
		self.n = 2*self.n
		self.draw()
	
	def draw(self):
		for i in xrange(self.n/2,self.n):
			x2 = self.x1 + self.fract[i][0]*self.l
			y2 = self.y1 + self.fract[i][1]*self.l
			self.c.create_line(self.x1,self.y1,x2,y2)
			self.x1 = x2
			self.y1 = y2
		self.c.update_idletasks()
	

root = Tk()
inst = Pic(master=root)
inst.mainloop()
root.destroy
