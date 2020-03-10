import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
import numpy as np
from src.TSPData import TSPData

# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    def __init__(self, generations, pop_size):
        self.generations = generations
        self.pop_size = pop_size

     # Knuth-Yates shuffle, reordering a array randomly
     # @param chromosome array to shuffle.
    def shuffle(self, chromosome):
        n = len(chromosome)
        for i in range(n):
            r = i + int(random.uniform(0, 1) * (n - i))
            swap = chromosome[r]
            chromosome[r] = chromosome[i]
            chromosome[i] = swap
        return chromosome

    # This method should solve the TSP.
    # @param pd the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self, tsp_data : TSPData):
        chromosome = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]
        N = 25
        Pm= 0.1
        x = []    #List of chromosomes

        for i in range(N):
            x.append(self.shuffle(chromosome))

        distances = tsp_data.get_distances()


        iter = 0
        fitness_list = []  # intiialized to be usable in the end
        max_iterations = 100
        done = False
        while not done:
            iter +=1
            new_population = []
            population = x
            num = N
            fitness_list = self.calculate_fitness(x, N, distances)

            #calcualate whether a cromosome is going to be mutated or not

            for i in range(N):
                r  = random.random()
                if r <= Pm:
                    #x[i] goin to be mutated and removed from the list
                    el = x[i]
                    del population[i]
                    del fitness_list[i]
                    num -= 1
                    new_population.append(self.mutate(el))

            outcome = self.roulette(population, fitness_list, num)

            for element in outcome:
                new_population.append(self.cross_over(element[0], element[1]))

            x = new_population

            if iter == max_iterations:  # Stopping criterion
                done = True

        fitness = np.asarray(fitness_list)

        return x[np.argmin(fitness)]


    def roulette(self, population, fitness_list, N):
        total_fitness = float(sum(fitness_list))
        rel_fitness = [f / total_fitness for f in fitness_list]
        # Generate probability intervals for each individual
        probs = [sum(rel_fitness[:i + 1]) for i in range(len(rel_fitness))]
        # Draw new population

        N_pairs = []

        for n in range(N):
            pair = []
            r = random.random()

            for (i, individual) in enumerate(population):
                if r <= probs[i]:
                    pair.append(individual)
                    break

            r = random.random()
            for (i, individual) in enumerate(population):
                if r <= probs[i]:
                    pair.append(individual)
                    break
            N_pairs.append(pair)

        return N_pairs

    def calculate_fitness(self, x, N, distances):
        fitness_list = []

        for i in range(N):
            chromosome = x[i]
            for index in range(len(chromosome)-1):
                # add distance from start to l[0]
                # add distance l[18] to end
                fitness_list[i] += 1 / distances[chromosome[index]][chromosome[index + 1]]

        return fitness_list

    def mutate(self, chromosome):
        r = int(random.randrange(0, 17))
        r1 = int(random.randrange(0, 17))

        if r != r1:
            temp = chromosome[r]
            chromosome[r] = chromosome[r1]
            chromosome[r1] = temp

    def cross_over(self, parent1, parent2):

        # 0-5 parent1 13-17 parent1 else parent2 offspring 2 will be the opposite

        offspring1 = parent1
        offspring2 = parent2

        for i in range(6, 12):
            offspring1[i] = -1
            offspring2[i] = -1

        for i in range(6,12):
            if parent2[i] not in offspring1:
                offspring1[i] = parent2[i]
            else:
                offspring1[i] = parent1[i]

            if parent1[i] not in offspring2:
                offspring2[i] = parent1[i]
            else:
                offspring2[i] = parent2[i]

        return offspring1, offspring2


# Assignment 2.b
if __name__ == "__main__":
    #parameters
    population_size = 20
    generations = 20
    persistFile = "./../tmp/productMatrixDist"
        
    #setup optimization
    tsp_data = TSPData.read_from_file(persistFile)
    ga = GeneticAlgorithm(generations, population_size)

    #run optimzation and write to file
    solution = ga.solve_tsp(tsp_data)
    tsp_data.write_action_file(solution, "./../data/TSP solution.txt")