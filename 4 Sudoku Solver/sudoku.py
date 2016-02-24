import time

used = [[[],[],[]],[[],[],[]],[[],[],[]]]

#count number of known elements
def count1(s):
	cnt = 0
	for br in xrange(3):
		for bc in xrange(3):
			for r in xrange(3):
				for c in xrange(3):
					if s[br][bc][r][c] != 0:
						cnt = cnt + 1
	return cnt

#count elements remaining to solved
def count2(s):
	cnt = 0
	for br in xrange(3):
		for bc in xrange(3):
			for r in xrange(3):
				for c in xrange(3):
					if len(s[br][bc][r][c]) > 1:
						cnt = cnt + 1
	return cnt

def remove2(lst,item):
	for i in range(len(lst)):
		if lst[i] == item:
			lst[:] = lst[:i]+lst[i+1:]
			return

def printS(s):
	for br in xrange(3):
		for bc in xrange(3):
			print "box(",br,",",bc,"):"
			for r in xrange(3):
				print "   row ", r, ":   ",s[br][bc][r]

def printS2(s):
	mw = [[0,0,0],[0,0,0],[0,0,0]]
	for br in xrange(3):
		for bc in xrange(3):
			for r in xrange(3):
				for c in xrange(3):
					x = s[br][bc][r][c]
					if len(x) > mw[bc][c]:
						mw[bc][c] = len(x)
	print ('||' + '-'*(3*(sum(mw[0])+sum(mw[1])+sum(mw[2]))+28)+'||')
	for br in xrange(3):
		for r in xrange(3):
			row = '||'
			for bc in xrange(3):
				for c in xrange(3):
					x = s[br][bc][r][c]
					if len(x) == 1:
						row = row + '   ' + str(x[0])
					else:
						row = row + ' ' + str(x)
					for i in xrange(3*mw[bc][c]-len(str(s[br][bc][r][c]))):
						row = row + ' '
					row = row + ' |'
				row = row + '|'
			print row
		#for i in xrange(len(row))
		#	s = s + '-'
		print ('||'+'-'*(len(row)-4)+'||')
	print

#all possible values for all boxes (empty sudoku)
def init1 ():
	s = [
		 [[[],[],[]],
		  [[],[],[]],
		  [[],[],[]]],
		 [[[],[],[]],
		  [[],[],[]],
		  [[],[],[]]],
		 [[[],[],[]],
		  [[],[],[]],
		  [[],[],[]]]]
	for br in xrange(3):
		for bc in xrange(3):
			for r in xrange(3):
				for c in xrange(3):
					s[br][bc][r].append(range(1,10))
	return s

def found(s,u,br,bc,r,c,x):
#	print "Found: ", x, " @ ", br, bc, r, c
	f = 0
	u[br][bc].append(x)
	#removal from same box
	for r2 in xrange(3):
		for c2 in xrange(3):
			if r2 != r or c2 != c:
				y = s[br][bc][r2][c2]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br,bc,r2,c2,y[0])
	#removal from same column
	for br2 in xrange(3):
		if br2 != br:
			for r2 in xrange(3):
				y = s[br2][bc][r2][c]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br2,bc,r2,c,y[0])
	#removal from same row
	for bc2 in xrange(3):
		if bc2 != bc:
			for c2 in xrange(3):
				y = s[br][bc2][r][c2]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br,bc2,r,c2,y[0])
	return f

#initialize sudoku from values in s
def init2 (sudoku,s,u):
	d = 0
	for br in xrange(3):
		for bc in xrange(3):
			for r in xrange(3):
				for c in xrange(3):
					x = s[br][bc][r][c]
					if x != 0:
						sudoku[br][bc][r][c] = [x]
						d = d + found(sudoku,u,br,bc,r,c,x)
						#print d
	return d
"""
def calcPoss(s,u,br,bc,r,c):
	used = u[br][bc][:]
	for bbr in xrange(3):
		if bbr != br:
			box = s[bbr][bc]
			for bbr2 in xrange(3):
				if not (box[bbr2][bc][0] in used):
					used.append(box[bbr2][bc][0])
	for bbc in xrange(3):
		if bbc != bc:
			box = s[br][bbc]
			for bbc2 in xrange(3):
				if not (box[br][bbc2][0] in used):
					used.append(box[br][bbc2][0])
	s[br][bc][r][c] = []
	for p in range(1,10):
		if not (p in used):
			s[br][bc][r][c].append(p)
	#iff this element's value was determined
	if len(used) == 8:
		found(s,u,br,bc,r,c,s[br][bc][r][c][0])
"""
#check whether in box there are numbers that are possible in only one place
def checkBox(s,u,br,bc):
	su = 0
	for num in xrange(1,10):
		if not (num in u[br][bc]):
			poss = []
			for r in xrange(3):
				for c in xrange(3):
					if num in s[br][bc][r][c]:
						poss.append((r,c))
			if len(poss) == 1:
				r = poss[0][0]
				c = poss[0][1]
#				print "  Found ", num, " @ ", br,bc,r,c
				s[br][bc][r][c] = [num]
				su = su + 1 + found(s,u,br,bc,r,c,num)
	return su

def checkBoxes(s,u):
	d = 0
	br = 0
	while br < 3:
		bc = 0
		while bc < 3:
			det = checkBox(s,u,br,bc)
			if det > 0:
				bc = -1
				br = 0
				d = d + det
			bc = bc + 1
		br = br + 1
	return d

#check whether in row there are numbers that are possible in only one place
def checkRow(s,u,br,r):
	su = 0
	for num in xrange(1,10):
		poss = []
		for bc in xrange(3):
			for c in xrange(3):
				#if the number is a possibility for this element
				#and the number is not already known to be here
				if num in s[br][bc][r][c] and len(s[br][bc][r][c]) > 1:
					poss.append((bc,c))
		if len(poss) == 1:
			bc = poss[0][0]
			c = poss[0][1]
#			print "  Found ", num, " @ ", br,bc,r,c
			s[br][bc][r][c] = [num]
			su = su + 1 + found(s,u,br,bc,r,c,num)
	return su

def checkRows(s,u):
	d = 0
	br = 0
	while br < 3:
		r = 0
		while r < 3:
			det = checkRow(s,u,br,r)
			if det > 0:
				r = -1
				br = 0
				d = d + det
			r = r + 1
		br = br + 1
	return d

#check whether in col there are numbers that are possible in only one place
def checkCol(s,u,bc,c):
	su = 0
	for num in xrange(1,10):
		poss = []
		for br in xrange(3):
			for r in xrange(3):
				#if the number is a possibility for this element
				#and the number is not already known to be here
				if num in s[br][bc][r][c] and len(s[br][bc][r][c]) > 1:
					poss.append((br,r))
		if len(poss) == 1:
			br = poss[0][0]
			r = poss[0][1]
#			print "  Found ", num, " @ ", br,bc,r,c
			s[br][bc][r][c] = [num]
			su = su + 1 + found(s,u,br,bc,r,c,num)
	return su

def checkCols(s,u):
	d = 0
	bc = 0
	while bc < 3:
		c = 0
		while c < 3:
			det = checkCol(s,u,bc,c)
			if det > 0:
				c = -1
				bc = 0
				d = d + det
			c = c + 1
		bc = bc + 1
	return d

#
#desparate check
#

def foundR(s,u,br,bc,r,x):
#	print "FoundR: ", x, " @ ", br, bc, "row", r
	f = 0
	u[br][bc].append(x)
	#removal from same row
	for bc2 in xrange(3):
		if bc2 != bc:
			for c2 in xrange(3):
				y = s[br][bc2][r][c2]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br,bc2,r,c2,y[0])
	return f

def foundC(s,u,br,bc,c,x):
#	print "FoundC: ", x, " @ ", br, bc, "col", c
	f = 0
	#removal from same column
	for br2 in xrange(3):
		if br2 != br:
			for r2 in xrange(3):
				y = s[br2][bc][r2][c]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br2,bc,r2,c,y[0])
	return f

def foundBr(s,u,br,bc,r,x):
#	print "FoundC: ", x, " @ ", br, bc, "col", c
	f = 0
	#removal from same box
	for r2 in xrange(3):
		if r2 != r:
			for c in xrange(3):
				y = s[br][bc][r2][c]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br,bc,r2,c,y[0])
	return f

def foundBc(s,u,br,bc,c,x):
#	print "FoundC: ", x, " @ ", br, bc, "col", c
	f = 0
	#removal from same box
	for c2 in xrange(3):
		if c2 != c:
			for r in xrange(3):
				y = s[br][bc][r][c2]
				z = len(y)
				remove2(y,x)
				if z == 2 and len(y) == 1:
					f = f + 1 + found(s,u,br,bc,r,c2,y[0])
	return f

def doubleCheckBoxes(s,u):
	su = 0
	for br in xrange(3):
		for bc in xrange(3):
			for num in xrange(1,10):
				temp = su
				if not (num in u[br][bc]):
					poss = []
					for r in xrange(3):
						for c in xrange(3):
							if num in s[br][bc][r][c]:
								poss.append((r,c))
					if len(poss) == 2:
						if poss[0][0] == poss[1][0]: #if both in same row
							su = su + foundR(s,u,br,bc,poss[0][0],num)
						elif poss[0][1] == poss[1][1]: #if both in same col
							su = su + foundC(s,u,br,bc,poss[0][1],num)
					elif len(poss) == 3:
						if poss[0][0] == poss[1][0] == poss[2][0]: #if all in same row
							su = su + foundR(s,u,br,bc,poss[0][0],num)
						elif poss[0][1] == poss[1][1] == poss[2][1]: #if all in same col
							su = su + foundC(s,u,br,bc,poss[0][1],num)
	return su

def doubleCheckRows(s,u):
	su = 0
	for br in xrange(3):
		for r in xrange(3):
			for num in xrange(1,10):
				temp = su
				poss = []
				for bc in xrange(3):
					for c in xrange(3):
						if num in s[br][bc][r][c]:
							poss.append(bc)
				if len(poss) == 2 and poss[0] == poss[1]: #if both in same box
					su = su + foundBr(s,u,br,poss[0],r,num)
				elif len(poss) == 3 and poss[0] == poss[1] == poss[2]: #if all in same box
					su = su + foundBr(s,u,br,poss[0],r,num)
	return su

def doubleCheckCols(s,u):
	su = 0
	for bc in xrange(3):
		for c in xrange(3):
			for num in xrange(1,10):
				temp = su
				poss = []
				for br in xrange(3):
					for r in xrange(3):
						if num in s[br][bc][r][c]:
							poss.append(br)
				if len(poss) == 2 and poss[0] == poss[1]: #if both in same box
					su = su + foundBc(s,u,poss[0],bc,c,num)
				elif len(poss) == 3 and poss[0] == poss[1] == poss[2]: #if all in same box
					su = su + foundBc(s,u,poss[0],bc,c,num)
	return su

def check(s,u):
	d = 0
	det = -1
	prev = -1
	while det != 0 or prev != 0:
		prev = det
		det = -1
		while det != 0:
			det = 0
			det = det + checkBoxes(s,u)
			det = det + checkRows(s,u)
			det = det + checkCols(s,u)
			d = d + det
		det = det + doubleCheckBoxes(s,u)
		det = det + doubleCheckRows(s,u)
		det = det + doubleCheckCols(s,u)
		d = d + det
	return d

def solve(s,u):
	sudoku = init1()
	init2(sudoku,s,u)
	check(sudoku,u)

def testTime(n,sudoku):
	u = [[[],[],[]],[[],[],[]],[[],[],[]]]
	x = time.time()
	for i in xrange(n):
		solve(sudoku,u[:])
		u = [[[],[],[]],[[],[],[]],[[],[],[]]]
	y = time.time()
	i = init1()
	init2(i,sudoku,u)
	printS2(i)
	check(i,u)
	printS2(i)
	print "Average time to solve:", ((y - x)/n), "seconds"
	# for s1 so far ~0.04 seconds to 22 remaining

from archive import *
s = s5
"""
sudoku = init1()
print "#'s known initially : ", count1(s), '\n'
print "#'s determined I    : ", init2(sudoku,s,used)
print "#'s determined II   : ", check(sudoku,used), '\n'
print "#'s remaining       : ", count2(sudoku), '\n'
printS2(sudoku)
"""
testTime(100,s)
"""
s1 ~ 0.048s
s2 ~ 0.025s
s3 ~ 0.025s
s4 ~ 0.039s
"""