import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import traceback
from src.SurroundingPheromone import SurroundingPheromone as SP
from src.Coordinate import Coordinate as Coordinate

# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.pheromones = [[0 for x in range(width)] for y in range(length)]
        self.initialize_pheromones()

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        initial_p = SP(0, 0, 0, 0)
        for i in range(self.get_width()):
            for j in range(self.get_length()):
                self.pheromones[i][j] = initial_p
        #return
    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

      # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        cur = route.get_start()
        route = route.get_route()
        i = 0
        while True:

            # update neighboring pheromones of the neighboring positions
            to_add = q/route.size()
            self.pheromones[cur.x-1][cur.y] = self.pheromones[cur.x-1][cur.y].get(0) + to_add
            self.pheromones[cur.x][cur.y-1] = self.pheromones[cur.x][cur.y-1].get(1) + to_add
            self.pheromones[cur.x+1][cur.y] = self.pheromones[cur.x+1][cur.y].get(2) + to_add
            self.pheromones[cur.x][cur.y+1] = self.pheromones[cur.x][cur.y+1].get(3) + to_add
            cur = cur.add_direction(route[i])
            i += 1

     # Update pheromones for a list of routes
     # @param routes A list of routes
     # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):
        for i in range(self.get_length()):
            for j in range(self.get_width()):
                self.pheromones[i][j] = self.pheromones[i][j] * (1 - rho)

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        return self.pheromones[position.get_x()][position.get_y()]
        #check type of position

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        amount_p = SP.get(pos)
        if self.in_bounds(amount_p):
            return amount_p
        else:
            return 0


    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])
            
            #make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])
            
            for y in range(length):
                line = lines[y+1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()