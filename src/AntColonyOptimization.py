import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from src.Maze import Maze
from src.PathSpecification import PathSpecification
from src.Ant import Ant
from src.Route import Route

# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, iterations, maze, ants_per_gen, generations, q, evaporation):
        self.maze = maze
        self.iter = iterations
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation

    # Loop that starts the shortest path process
    # @param spec Spefication of the route we wish to optimize
    # @return ACO optimized route
    def find_shortest_route(self, path_specification):
        self.maze.reset()
        route = None

        for gen in range(0, self.generations):
            a = 0
            routes = []
            while a < self.ants_per_gen:
                ant = Ant(self.maze, path_specification, self.iter)
                new_route = ant.find_route()
                routes.append(new_route)
                if route is None:
                    route = new_route

                if new_route.shorter_than(route):
                    route = new_route
                a = a + 1
            self.maze.add_pheromone_routes(routes, self.q)
            self.maze.evaporate(self.evaporation)
        return route


# Driver function for Assignment 1
if __name__ == "__main__":
    # parameters
    iterations = 10000
    gen = 20
    no_gen = 20
    q = 1600
    evap = 0.1

    # construct the optimization objects
    maze = Maze.create_maze("./../data/medium maze.txt")
    spec = PathSpecification.read_coordinates("./../data/medium coordinates.txt")

    aco = AntColonyOptimization(iterations, maze, gen, no_gen, q, evap)

    # save starting time
    start_time = int(round(time.time() * 1000))

    # run optimization
    shortest_route = aco.find_shortest_route(spec)

    # print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))

    # save solution
    shortest_route.write_to_file("./../data/32_medium.txt")

    # print route size
    print("Route size: " + str(shortest_route.size()))
