import sys
import random
#print (sys.argv[:])
try:
	x_length = int(sys.argv[1])
	y_length = int(sys.argv[2])
except:
	sys.exit(sys.argv[0]+": Usage argv1=xlength,argv2=ylength")
grid = []
deigma = [ "O" for x in range(x_length) ]

#### PUT FIRST RANDOMLY AS SALT AND PEPPER THE OBSTACLES #######
for y in range(y_length):
  grid.append(deigma[:])
  for k in range(random.randrange(0,x_length)):
    grid[y][random.randrange(0,x_length)]='X'

#### PUT WALLS AND PACKAGES OF OBSTACLE RANDOMLY ###

#### HORIZONTALLY #####

for y in range(y_length):
  if(random.uniform(0,1)>0.8):
    deigma = ['X' for x  in range(random.randrange(0,x_length)) ]
    start_position = random.randrange(0,x_length) 
    for k in range(start_position,start_position+len(deigma)):
      grid[y][k%x_length]='X'


#### VERTICALLY #### 

for x in range(x_length):
  if(random.uniform(0,1)>0.8):
    deigma = ['X' for y  in range(random.randrange(0,y_length)) ]
    start_position = random.randrange(0,y_length) 
    for k in range(start_position,start_position+len(deigma)):
      grid[k%y_length][x]='X'

robot1=[0,0]
robot2=[0,0]
ok = False
while not ok:
  robot1=[random.randrange(y_length),random.randrange(x_length)]
  if grid[robot1[0]][robot1[1]]!='X':
    ok = True
ok = False

while not ok:
  robot2=[random.randrange(y_length),random.randrange(x_length)]
  if grid[robot2[0]][robot2[1]]!='X':
    ok = True

print(str(x_length)+" "+str(y_length))
print(str(robot1[1])+" "+str(robot1[0]))
print(str(robot2[1])+" "+str(robot2[0]))
for row in grid:
  print("".join(row))
