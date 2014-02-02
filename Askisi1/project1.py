#this code runs optimally with python 3.x

inputFile = input("Insert input file: ")
f = open(inputFile, 'r')

#reads the input file
[max_x, max_y] = f.readline().replace('\n','').split(' ')
[robot1_x, robot1_y] = f.readline().replace('\n','').split(' ')
[robot2_x, robot2_y] = f.readline().replace('\n','').split(' ')
grid = f.read().splitlines()

#outputs input file for demonstration reasons
print("grid_x = " + str(max_x))
print("grid_y = " + str(max_y))
print("Rogbot1 Xcoord = " + str(robot1_x))
print("Rogbot1 Ycoord = " + str(robot1_y))
print("Rogbot2 Xcoord = " + str(robot2_x))
print("Rogbot2 Ycoord = " + str(robot2_y) + "\n")
for row in grid:
    print(row)
print()

f.close()
input("press enter")
