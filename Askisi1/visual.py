# Visualization code for simulated robots.
import math
import time
import random
from tkinter import *

class RobotVisualization:
    def __init__(self, height, width, delay = 0.2):
    	#"Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay
        self.max_dim = max(width,height)
        self.width = width
        self.height = height
        self.num_robots = 2
        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()
        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
       	# Draw gray squares for dirty tiles
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,fill = "gray")
        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)
        
        self.robots = None
        self.time = 0
        self.master.update()
 

#	"Maps grid positions to window positions (in pixels)."
    def _map_coords(self, x, y):
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),250 + 450 * ((self.height / 2.0 - y) / self.max_dim))
 


#		"Returns a polygon representing a robot with the specified parameters."
    def _draw_robot(self, x ,y , who):
        direction = random.randrange(360)
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 0.6 * math.sin(math.radians(d1)),y + 0.6 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 0.6 * math.sin(math.radians(d2)),y + 0.6 * math.cos(math.radians(d2)))
        if (who == 1):
            return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")
        else:
            return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="blue")


	 	# "Redraws the visualization with the specified room and robot state."
		# Removes a gray square for any tiles has not an obstacle.
    def update(self, grid, robot1, robot2, step):
        tgrid = [[grid[x][y] for x in range(self.height)] for y in range(self.width)]
        for i in range(len(tgrid)):
            tgrid[i].reverse()
        for j in range(self.height):
            for i in range(self.width):
                if tgrid[i][j]=='X':
                    self.w.delete(self.tiles[(i,j)])
		
		# Delete all existing robots.
        if self.robots:
            for robot in self.robots:
                self.w.delete(robot)
                self.master.update_idletasks()

		# Draw new robots
        self.robots = []
        x, y = self.height-robot1[0]-1,robot1[1]
        x, y = y, x
        x1, y1 = self._map_coords(x - 0.08, y - 0.08)
        x2, y2 = self._map_coords(x + 0.08, y + 0.08)
        self.robots.append(self.w.create_oval(x1, y1, x2, y2,fill = "black"))
        self.robots.append(self._draw_robot(x,y,1))
        x, y = self.height-robot2[0]-1,robot2[1]
        x, y = y, x
        x1, y1 = self._map_coords(x - 0.08, y - 0.08)
        x2, y2 = self._map_coords(x + 0.08, y + 0.08)
        self.robots.append(self.w.create_oval(x1, y1, x2, y2,fill = "black"))
        self.robots.append(self._draw_robot(x,y,2))
        self.time = step
        self.master.update()
        time.sleep(self.delay)
