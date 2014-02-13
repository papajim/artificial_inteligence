####this code runs optimally with python 3.x

import sys
from queue import PriorityQueue
from random import randrange
from time import time

####admissible heuristic using Manhattan distance
def heuristic (my_pos, target):
	h = abs(my_pos[0] - target[0])
	h += abs(my_pos[1] - target[1])
	return h

####moves R2 randomly
def random_move(current, grid, grid_size):
	one_step = [[0,1],[0,-1],[1,0],[-1,0]]
	ok = False
	while not ok:
		i = randrange(4)
		new = current[:]
		new[0] += one_step[i][0]
		new[1] += one_step[i][1]
		if (new[0] >= 0) and (new[0] < grid_size[0]) and (new[1] >= 0) and (new[1] < grid_size[1]):
			if (grid[new[0]][new[1]] != 'X'):
				ok = True
	return new

#finds new states from our expansion (current) point
def find_states(current, target, steps, guard, grid, grid_size):
	states = []
	i = 0
	for s in steps:
		if guard[i]:
			temp = current[2][:]
			temp[0] += s[0]
			temp[1] += s[1]
			if (temp[0] >= 0) and (temp[0] < grid_size[0]) and (temp[1] >= 0) and (temp[1] < grid_size[1]):
				if (grid[temp[0]][temp[1]] != 'X'):
					g = current[1] + abs(s[0]) + abs(s[1])
					f = g + heuristic(temp, target)
					state = [f, g, temp]
					states.append(state)
				else:
					guard[i] = False
		i += 1
	
	return states
####expand returns the new states R1 can reach from its current position
####taking one and two steps accordingly
def expand(current, target, grid, grid_size):
	nodes = []
	one_step = [[0,1],[0,-1],[1,0],[-1,0]]
	two_steps = [[0,2],[0,-2],[2,0],[-2,0]]
	guard = [True,True,True,True] #keeps R1 from jumping over obstacles
	nodes = find_states(current, target, one_step, guard, grid, grid_size)
	nodes += find_states(current, target, two_steps, guard, grid, grid_size)
	return nodes

####A_star uses two types of datastractures a dictionary (hash table) and a priority queue (heap)
####the dictionary uses the coords as key and for value uses the list of f_value and the parent
####for example (1,2):[100, [0,0]], where f_value is the g_value + heuristic
####the priority queue contains lists with the f_value, g_value, and coords
####for example [100, 0, [1,2]]
def A_star (start, target, grid, grid_size):
	states = {}
	next_state = PriorityQueue()
	current = [heuristic(start, target), 0, start]
	next_state.put(current)
	states[tuple(start)] = [current[0],[-1,-1]]
	found = False
	
	while not found and next_state.qsize() > 0:
		current = next_state.get()
		coords = current[2]
		if (states[tuple(coords)][0] != current[0]):
			continue	
		if (coords[0] != target[0]) or (coords[1] != target[1]):
			keys = states.keys()
			temp_states = expand(current, target, grid, grid_size)
			for state in temp_states:
				if tuple(state[2]) not in keys:
					next_state.put(state)
					states[tuple(state[2])] = [state[0], coords]
				elif states[tuple(state[2])][0] > state[0]:
					next_state.put(state)
					states[tuple(state[2])] = [state[0], coords]
		else:
			found = True

	if not found and next_state.qsize() == 0:
		return [[-1, -1], len(states.keys())]
	####creates the list of moves for the optimal path
	moves = []
	parent = current[2]
	while states[tuple(parent)][1] != [-1,-1]:
		moves.append(parent)
		parent = states[tuple(parent)][1]
	#print(moves)
	####returns the last element (1st move)
	return [moves[len(moves)-1], len(states.keys())]

inputFile = input("Insert input file: ")
f = open(inputFile, 'r')
###################################################################################
####reads the input file
grid_size = list(map(int, f.readline().replace('\n','').split(' ')))
robot1 = list(map(int, f.readline().replace('\n','').split(' ')))
robot2 = list(map(int, f.readline().replace('\n','').split(' ')))
grid = f.read().splitlines()
f.close()

valid = ['X','O']
####outputs input file for demonstration reasons
print("grid_x = " + str(grid_size[0]))
print("grid_y = " + str(grid_size[1]))
print("Robot1 Xcoord = " + str(robot1[0]))
print("Robot1 Ycoord = " + str(robot1[1]))
print("Robot2 Xcoord = " + str(robot2[0]))
print("Robot2 Ycoord = " + str(robot2[1]) + "\n")
for row in grid:
    print(row)
print()
for row in grid:
	for element in row:
		if element not in valid:
			print("Invalid Input")
			sys.exit()

###################################################################################
####initialize
start_time = time()
start = robot1[:]
target = robot2[:]
#grid_size.reverse()
#start.reverse()
#target.reverse()
impossible = False
caught = False
R1_moves = [start]
R2_moves = [target]
total_nodes = 0
####start chasing R2
####if A_start returns [-1,-1] as the next move its impossible to catch R2
####else appends the the move to R1_moves
####then if R1 hasn't caught R2, R2 moves randomly in the area
while not (caught or impossible):
	[move, nodes] = A_star(start, target, grid, grid_size)
	total_nodes += nodes
	if move == [-1,-1]:
		impossible = True
	else:
		start = move[:]
		R1_moves.append(move)
		if (start == target):
			caught = True
	if not caught:
		target = random_move(target, grid, grid_size)
		R2_moves.append(target)
###################################################################################
####outputs data
end_time = time()
print("Time needed:", end_time - start_time, "seconds")
print("Total number of nodes produced:",total_nodes)
if caught:
	grid = list(map(list,grid))
	for m in range(len(R2_moves)):
		grid = list(map(list,grid))
		grid[R1_moves[m][0]][R1_moves[m][1]] = '1'
		grid[R2_moves[m][0]][R2_moves[m][1]] = '2'
		temp_grid = list(map("".join,grid))
		for row in temp_grid:
			print(row)
		print("R1 move:", R1_moves[m])
		print("R2 move:", R2_moves[m])
		print()
	l = len(R1_moves)
	grid[R1_moves[l-1][0]][R1_moves[l-1][1]] = '1'
	temp_grid = list(map("".join,grid))
	for row in temp_grid:
		print(row)
	print("R1 moves to", R1_moves[l-1],"and catches R2")
	print("R1 did", l,"moves to catch R2")
else:
	print('Impossible to catch. R2 is really clever !!!\n')

