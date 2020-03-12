import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
from src.Direction import Direction
from src.Route import Route


# Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):
        #TODO: check for walls
        route = Route(self.start)
        pheromones = self.maze.pheromones
        iterations = 0
        while self.current_position != self.end:
            print('--')
            print('I am there : ', self.current_position)
            north = Direction.north
            south = Direction.south
            east = Direction.east
            west = Direction.west

            north_dir = self.current_position.add_direction(north)
            south_dir = self.current_position.add_direction(south)
            east_dir = self.current_position.add_direction(east)
            west_dir = self.current_position.add_direction(west)

            directions = [north_dir, south_dir, east_dir, west_dir]
            share_p = []
            directions_p = []
            for i in range(4):
                if directions[i].x_between(0, self.maze.get_width()) and directions[i].y_between(0, self.maze.get_length()):

                    share_p.append(pheromones[directions[i].get_y()][directions[i].get_x()])
                    if i == 0:
                        share_p[-1] = share_p[-1].get(Direction.south)
                        directions_p.append(north)
                    elif i == 1:
                        share_p[-1] = share_p[-1].get(Direction.north)
                        directions_p.append(south)
                    elif i == 2:
                        share_p[-1] = share_p[-1].get(Direction.west)
                        directions_p.append(east)
                    elif i == 3:
                        share_p[-1] = share_p[-1].get(Direction.east)
                        directions_p.append(west)
                    else:
                        raise ArithmeticError
            total_p = sum(share_p) if sum(share_p) > 0 else 1
            #print('directions : ', directions_p)

            # if no pheromones :
            if sum(share_p) == 0:
                share_p = [1/len(share_p) for x in range(len(share_p))]

            end_share_p = [0 for x in range(len(share_p))]
            share_p = list(map(lambda x: x/total_p, share_p))
            for i in range(len(share_p)):
                 end_share_p[i] = sum(share_p[0:i+1])
            #print('pheromones : ', end_share_p)
            #TODO: map with the sum of the last cells
            ran_number = self.rand.uniform(0, 1)
            for i in range(len(end_share_p)):
                if ran_number <= end_share_p[i]:
                    self.current_position = self.current_position.add_direction(directions_p[i])
                    route.add(directions_p[i])
                    #print(directions_p[i])
                    #print('going that way : ', directions_p[i])
                    break
            iterations += 1
        #print(route.get_route())
        return route
