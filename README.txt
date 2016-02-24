General Disclaimer

	Much of the code in this examples folder was written before working in a professional software development. I think that these are the two most important features of good code that I learned from my work experience:
	1. Clean and consistent code styling is important to make code easier to understand in the future and by other people.
	2. The best code does not require comments as documentation, but is written with self-evident organization and names. Comments may be required sometimes, but can often be avoided with verbose variable/method names and simple organization.
	These two features may not come across in the code examples of this folder.

1 Agricola

	Agricola is a board game that is turn-based, from 1 to 4 players, with the goal of building a "successful" farm.
	This project was an attempt to create a virtual version of the board game that would help my friends and I enjoy it with less setup/cleanup time and eventually online.
	It is currently incomplete, but you can run agricola_2.py to see the most recent version:
		1. Click New Game
		2. Select number of players, starting player, names and colours
		3. Click start game
		4. Players take turns clicking on the "action" spaces on the board, which will place one of their tokens on it.
		5. After all players place all their tokens, the round is over.
	The project remains incomplete since it is missing gameplay features, including screens to show players their current stock. I had planned to improve the graphical interface eventually as well.
	(A PDF of the rules are available in the folder)
	
2 Dragon Curve

	This is a very simple program that I wrote to draw out a fractal I learned while reading Jurassic Park.
	
3 Spite & Malice

	Spite and Malice is a card game that I enjoyed playing with my boyfriend, but I couldn't find an online version to play with him, so I started to write one. This is also an incomplete game. I tried to run it, and the server didn't start up; I'm not sure why, but the code should still be able to give you some insight to my python coding style.
	
4 Sudoku Solver

	In university I was interested in codifying my own strategies of solving sudoku puzzles into an algorithm and seeing how fast I could make it. After several iterations, "sudokuComplete.py" was the result. "archive.py" contains an archive of several incomplete sudokus that you can use sudokuComplete to solve. To solve a specific sudoku, change line 452 of sudokuComplete to use the name of the sudoku you want to solve (currently it is "s7").
	There's no user input method, since that wasn't important to me at the time, just the algorithm itself. There is also method to run the solver on the same sudoku puzzle multiple times to get a more precise average solving time.
	
5 Snakes on a Plane

	I wrote these java programs a very long time ago (just after graduating high school) as part of this programming competition: http://www.recmath.org/contest/Snakes/description.php
	It was before I learned to use subversion tools, so I would manually increment the file names when I felt I'd improved the algorithm significantly. (You can actually still see the standings on that site with my score).
	
6 Gorilla Wars

	An incomplete recreation of a simple game I liked when I was a child. You're two gorillas throwing bananas at each other with a certain angle and power; whoever hits the other first wins.
	
7 Swarm

	This is a quick script I wrote to test out an idea about mimicking insect swarms and bird flocks. As commented in the code: in each temporal update each insect retains a small portion of their previous velocity (changing momentum is hard sometimes) and then tries to move towards the centre of all the other members of the swarm that it can see (within a certain radius)
	
8 Game of Life

	An implementation of Conway's Game of Life. Clicking on the screen runs it for another 100 generations and then stops. The text output is the number of cells that are "alive" in each generation.