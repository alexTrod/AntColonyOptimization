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
        north = Direction.north
        south = Direction.south
        east = Direction.east
        west = Direction.west

        route = Route(self.start)
        pos_checked = [[False for y in range(self.maze.get_length())] for x in range(self.maze.get_width())]

        while self.current_position != self.end:
            chance = random.uniform(0, 1)
            pie_slice = 0
            total_pher = 0
            sp = self.maze.get_surrounding_pheromone(self.current_position)

            north_dir = self.current_position.add_direction(north)
            south_dir = self.current_position.add_direction(south)
            east_dir = self.current_position.add_direction(east)
            west_dir = self.current_position.add_direction(west)
            print('--')
            print('I am there : ', self.current_position)
            pos_checked[self.current_position.get_x()][self.current_position.get_y()] = True
            directions = []

            if self.maze.maze_check(north_dir):
                if not pos_checked[north_dir.get_x()][north_dir.get_y()]:
                    direc = sp.get(north)
                    total_pher += direc
                    print("north", north)
                    directions.append(north)

            if self.maze.maze_check(south_dir):
                if not pos_checked[south_dir.get_x()][south_dir.get_y()]:
                    direc = sp.get(south)
                    total_pher += direc
                    print("south", south)
                    directions.append(south)

            if  self.maze.maze_check(east_dir):
                if not pos_checked[east_dir.get_x()][east_dir.get_y()]:
                    direc = sp.get(east)
                    total_pher += direc
                    print("east", east)
                    directions.append(east)

            if  self.maze.maze_check(west_dir):
                if not pos_checked[west_dir.get_x()][west_dir.get_y()]:
                    direc = sp.get(west)
                    total_pher += direc
                    print("west",west)
                    directions.append(west)

            if len(directions) > 0:
                for dirs in directions:
                    print("crazy" ,dirs)
                    pie_slice += sp.get(dirs) / total_pher
                    if chance <= pie_slice:
                        self.current_position = self.current_position.add_direction(dirs)
                        route.add(dirs)
                        break
            else:
                prev_dir = route.remove_last()
                if prev_dir == north:
                    back_dir = south
                if prev_dir == south:
                    back_dir = north
                if prev_dir == east:
                    back_dir = west
                if prev_dir == west:
                    back_dir = west
                print("HIII")
                self.current_position = self.current_position.add_direction(back_dir)

        return route
