"""Docstring for ga_engine.py

This module implements the Genetic
Algorithm class adapted to the Genetic
Engine Library
"""

import numpy as np
from copy import deepcopy
import threading
from genetic_algorithm.ga_nn import GeneticAlgorithmNN

class GeneticAlgorithmEngine(GeneticAlgorithmNN):
	"""
	An inherited class from GeneticAlgorithmNN
	This class provides an interface to use
	GeneticAlgorithm and ArtificialNeuralNetwork 
	class with Genetic Engine Library
	
	...
	Parameters
	----------
	neural_network: ArtificialNeuralNetwork object
		An instance of the ArtificialNeuralNetwork object
		
	evaluation_steps: integer
		The number of time steps for which
		to evaluate the simulation
		
	Rest of the parameters are the same
	
	Attributes
	----------
	evaluation_steps: integer
		The number of time steps for which
		to evaluate the simulation
		
	test_network: array_like
		Sets a network whose parameters we don't
		require to change too much.
		
		Takes in a list of paramters and converts
		it to the required neural network
		
	Rest of the attributes are the same
	
	Methods
	-------
	calculate_fitness(chromosome)
		Takes the chromosome and generates it's
		fitness for one time step
		
	determine_fitness(individual_fitness)
		Takes the fitness values for evaluation time steps
		Averages the values and returns them
		
	test_output(input_dict)
		Calculates the output of the test network
		
	Rest of the methods are the same
	"""
	def __init__(self, genetic_engine, neural_network, evaluation_steps=100, population_size=100,
				 number_of_generations=10, mutation_probability=0.01,
				 number_of_elites=0):
				 
		"""
		Initialization function of the class
		...
		
		Parameters
		----------
		Specified in the class docstring
		
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		self.evaluation_steps = evaluation_steps
		self.genetic_engine = genetic_engine
		
		# Initialize the Parent Class
		GeneticAlgorithmNN.__init__(self, neural_network, population_size,
									number_of_generations, mutation_probability,
									number_of_elites)
									
	# Calculates the fitness of a single chromosome
	def calculate_fitness(self, individual_fitness, chromosome):
		"""
		Calculates the fitness of a single chromosome
		(that is passed as argument) according to the
		fitness function
		"""
		# For simple GA, fitness depends on chromosome
		# For GA + NN, fitness will depend on output + chromosome
		# For Gazebo, fitness will depend on the simulation
		# In the case of simulation, the fitness will be calculated
		# iteratively for some evaluation time set by user!
		
		# Fitness calculated according to fitness function
		# defined by the user
		fitness = np.sum(individual_fitness) / self.evaluation_steps
		
		# Determine the best fitness
		# And when it occured the first time
		if(fitness != self.best_fitness):
			self.best_fitness = max(self.best_fitness, fitness)
			if(fitness == self.best_fitness):
				self.best_chromosome = chromosome
				self.best_generation = self.current_generation
			
		return fitness
		
	# Generate the fitness value of the current population
	def determine_fitness(self):
		"""
		Calculates the fitness of the entire population
		"""
		# Fitness vector stores the fitness of the current population
		self.fitness_vector = []
		simulation_threads = []
		
		# Iterate over the population
		for individual in self.population:
			simulation = self.ready_simulation(individual)
			simulation.start()
			simulation_threads.append((simulation, individual))
			simulation.join()
			
		# Join the threads
		for simulation in simulation_threads:
			#simulation[0].join()
			self.fitness_vector.append(self.calculate_fitness(simulation[0].fitness_values,
															  simulation[1]))
		
		# Numpy conversion, to maintain defaut settings
		self.fitness_vector = np.array(self.fitness_vector, np.float64)
		
		# Work on the statistics
		self.generate_statistics()
		
	def ready_simulation(self, individual):
		self.test_network = individual
		simulation = self.genetic_engine(self.test_network, 
					 self.evaluation_steps, self.fitness_function)
		
		return simulation
			
	@property
	def test_network(self):
		"""
		Used to save the network with parameters,
		so we don't have to change again and again
		"""
		return self._test_network
		
	@test_network.setter
	def test_network(self, individual):
		ready_individual = self.convert_chromosome(individual)
		self.neural_network.load_parameters_from_vector(ready_individual)
		self._test_network = self.neural_network
		
	@property
	def evaluation_steps(self):
		""" 
		The number of time steps for which
		the fitness function should be evaluated
		"""
		return self._evaluation_steps
		
	@evaluation_steps.setter
	def evaluation_steps(self, steps):
		if(steps <= 0):
			steps = 100
			
		self._evaluation_steps = steps
	
