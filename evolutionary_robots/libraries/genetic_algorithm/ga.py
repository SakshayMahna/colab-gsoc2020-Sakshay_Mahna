"""Docstring for ga.py module

This module implements Genetic Algorithm
class. The class contains predefined functions
of selection, crossover and mutation. The user
is required to design the fitness function.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
import multiprocessing

# The Genetic Algorithm class
class GeneticAlgorithm(object):
	"""
	The Genetic Algorithm Class
	Selection, Crossover and Mutation are defined
	The user needs to input the fitness function only
	
	...
	
	Parameters
	----------
	population_size(optional): integer
		The size of the population of the Genetic Algorithm
		
	number_of_generations(optional): integer
		The number of generations for which the Genetic
		Algorithm should run
		
	mutation_probability(optional): float
		The probability of mutation
		
	chromosome_length(optional): integer
		The length of the chromosome of each individual
		
	number_of_elites(optional): integer
		The number of elites in each generation
		
	Attributes
	----------
	fitness_function: function
		The fitness function according to which the
		fitness of individuals are calculated
	
	population_size: integer
		The size of the population of the Genetic Algorithm
		
	number_of_generations: integer
		The number of generations for which the Genetic
		Algorithm should run
		
	mutation_probability: float
		The probability of mutation
		
	chromosome_length: integer
		The length of the chromosome of each individual
		
	number_of_elites: integer
		The number of elites in each generation
		
	replay_fraction: float
		A float between 0 to 1 that specifies the fraction
		of generations the algorithm should save
		
	Methods
	-------
	run()
		Simulate the complete run of the Genetic Algorithm
	
	plot_fitness()
		Function to plot the max, min and average fitness v/s
		the generation
		
	save_chromosome(filename)
		Function to save a chromosome or an array of chromosomes
		to a file
		
	load_chromosome(filename)
		Function to load generation from which to resume
		from a file
		
	Other Methods
	-------------
	generate_population()
		Generates a new random population according to size of
		population and the number of chromosomes
		
	calculate_fitness(chromsome)
		Calculates the fitness of a single chromosome according
		to the fitness function
		
	determine_fitness()
		Calculates the fitness of the entire generation
		
	selection()
		Selects the individuals of a generation according to 
		a probability distribution(list_of_fitness_value)
		
	crossover()
		Crosses over two chromsomes(mum and dad) and generates
		two other chromosomes(son and daughter) by crossing over
		The parents are replaced by their offspring. Hence,
		the entire new population is generated by this function
		
	mutation()
		Mutates the genes of the chromosomes of the indviduals
		according to the mutation probability
		
	stop_handler()
		Function that handles the execution when SIGINT signal is
		received. It saves the files from where the user can resume
		
	save_statistics(filename)
		Function to save the statistics of the runtime
		of algorithm in a specified file
		
	"""
	def __init__(self, population_size=100, number_of_generations=10, 
				 mutation_probability=0.01, chromosome_length=5, 
				 number_of_elites=0):
		"""
		Initialization function of Genetic Algorithm
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
		# Initializations
		self.population_size = population_size
		self.number_of_generations = number_of_generations
		self.mutation_probability = mutation_probability
		self.chromosome_length = chromosome_length
		self.number_of_elites = number_of_elites
		
		# Other adjustable constants
		self.replay_fraction = 0.25
		
		# Some constants
		self.__minimum_crossover_length = 1		# Always 1
		self.__do_crossover = True
		
		# Settings to adjust some non required warnings
		np.seterr(divide='ignore', invalid='ignore')
	
	# Generates a population of individuals
	def generate_population(self):
		"""
		Generates a new random population according to
		the size of population and the chromsome length
		"""
		# Using the range
		self.population = np.random.uniform(0, 1, 
						  (self.population_size, self.chromosome_length))
		
		# Initialize the plots and the BEST individual
		self.best_chromosome = None
		self.best_fitness = float('-inf')
		self.best_generation = None
		
		# Lists to be saved
		self.__best_chromosomes = []
		self.__generations = []
		self.__statistics = []
		
		# Plotting lists
		self.max_fitness = []
		self.min_fitness = []
		self.avg_fitness = []
		
	# Calculates the fitness of a single chromosome
	def calculate_fitness(self, chromosome):
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
		fitness = self.fitness_function(chromosome)
		
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
		
		# Iterate over the population
		for individual in self.population:
			self.fitness_vector.append(self.calculate_fitness(individual))
		
		# Numpy conversion, to maintain defaut settings
		self.fitness_vector = np.array(self.fitness_vector, np.float64)	
		
		# Get some statistics and print
		min_fitness = self.fitness_vector.min()
		max_fitness = self.fitness_vector.max()
		sum_fitness = np.sum(self.fitness_vector)
		
		# Append to best chromsomes
		self.__best_chromosomes.append(self.population[
									   np.where(self.fitness_vector == np.amax(self.fitness_vector))
									   ][0])
		
		# Append to statistics: Generation, Max Fitness, Average Fitness,
		# Min Fitness and Best Chromosome of the generation
		self.__statistics.append([self.current_generation, max_fitness, 
								  sum_fitness / self.population_size, min_fitness])
		
		print("{: <10} {: >20} {: >20} {: >20}".format(
												*self.__statistics[self.current_generation - self.generation_start]
												))
		
		# Append to plots
		self.min_fitness.append(min_fitness)
		self.max_fitness.append(max_fitness)
		self.avg_fitness.append(sum_fitness / self.population_size)
		
		# Remove the elites from the calculation
		if(self.number_of_elites != 0):
			# Paritition the list and get the best individuals(number_of_elites)
			elite_index = np.argpartition(self.fitness_vector, -self.number_of_elites)[-self.number_of_elites:]
			# Get the chromosomes of elites
			self.elites = self.population[elite_index]
			# Delete the elites from current population
			self.fitness_vector = np.delete(self.fitness_vector, elite_index)
			
		# Normalize the fitness values to lie between 0 and 1 and sum to 1
		min_fitness = self.fitness_vector.min()
		max_fitness = self.fitness_vector.max()
		
		try:
			self.fitness_vector = (self.fitness_vector - min_fitness) / (max_fitness - min_fitness)
		except ZeroDivisionError:
			pass
			
		# Average the fitness vector
		self.fitness_vector = self.fitness_vector / np.sum(self.fitness_vector)
		
	# Selection of individuals
	def selection(self):
		"""
		Selects the individuals that are to be crossovered
		according to a probability distribution
		"""
		# Random choice, roullete selection
		# The probility function is the fitness vector itself
		try:
			effective_population = self.population_size - self.number_of_elites
			self.roullete_selection = np.random.choice(effective_population, 
														effective_population, 
														p = self.fitness_vector)
		except ValueError:
			pass
				
	# Cross over
	def crossover(self):
		"""
		Cross Over two individuals to generate two new
		individuals and generate the next generation
		"""
		# Check whether it is legal to do crossover or not
		if(self.__do_crossover == False):
			return
		
		# New population
		new_population = []
		# Based on the roullete selection, we crossover mum and dad
		for index in range(0, self.population_size - self.number_of_elites, 2):
			mum = self.population[self.roullete_selection[index]]
			dad = self.population[self.roullete_selection[index + 1]]
			
			cross_position = np.random.randint(self.__minimum_crossover_length, 
											   self.chromosome_length)
			
			# Cross over
			son = np.concatenate([mum[:cross_position], dad[cross_position:]])
			daughter = np.concatenate([dad[:cross_position], mum[cross_position:]])
			
			# Append to new population
			new_population.append(son); new_population.append(daughter)
			
		# The offsprings are the new population now
		# Along with the elites
		self.population = np.array(new_population)
		try:
			self.population = np.concatenate([self.population, self.elites])
		except AttributeError:
			pass
	
	# Mutation
	def mutation(self):
		"""
		Mutate the alleles of a generation according
		to the probability of mutation
		"""
		# Iterate over all the elements
		for row in range(self.population.shape[0] - self.number_of_elites):
			for column in range(self.population.shape[1]):
				# Mutate or not
				mutate = np.random.choice(2, 1, p = [1 - self.mutation_probability, 
													 self.mutation_probability
													])
				if(mutate[0] == 1):
					# Mutate
					self.population[row, column] = np.random.uniform(0, 1)
				
	# Plotting Function
	def plot_fitness(self, filename, show=False):
		"""
		Plots the Fitness statistics of a population
		as a function of generation
		"""
		# Generate the range of Generations
		generations = range(self.generation_start, self.number_of_generations+1)
		
		# Plot Max Fitness
		plt.plot(generations, self.max_fitness, label="MAX")
		
		# Plot Min Fitness
		plt.plot(generations, self.min_fitness, label="MIN")
		
		# Plot Average Fitness
		plt.plot(generations, self.avg_fitness, label="AVERAGE")
		
		# Name the axes
		plt.xlabel('Generations')
		plt.ylabel('Fitness Value')
		
		# Show the plots and the legend
		plt.title("Fitness Plot")
		plt.legend()
		
		# Make a directory if it does not exist
		if not os.path.exists('./repr'):
			os.makedirs('./repr')
		
		plt.savefig(filename + '.png')
		
		if(show == True):
			plt.show()
		
	# Function to save statistics
	def save_statistics(self, filename):
		"""
		Function to save the statistics of the runtime
		of algorithm in a specified file
		"""
		# Save the statistics to a txt file
		legend = ["Generation", "Maximum Fitness", "Average Fitness", "Minimum Fitness"]
		header = "{: <10} {: >20} {: >20} {: >20}".format(*legend)
		fmt = '%-10d', '%20.10f', '%20.10f', '%20.10f'
		np.savetxt(filename + '.txt', self.__statistics, fmt=fmt, header=header)
		
	# Function to save chromosomes
	def save_chromosome(self, chromosome, filename, header=None):
		"""
		Function to save a chromosome to a file
		
		Parameters
		----------
		chromosome: array like
			The chromosome array should be a 1D or 2D array
			Either representing a single chromosome or a
			group of chromosomes
		
		filename: string
			The name of the file to which the chromosome is
			going to be saved
			
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		# Convert to numpy array
		chromosome = np.array(chromosome)
		
		# Save the chromosome to a txt file
		if(header == None):
			np.savetxt(filename + '.txt', chromosome, fmt="%.10f", delimiter=' , ')
		else:
			np.savetxt(filename + '.txt', chromosome, fmt="%.10f", delimiter=' , ', header=header)
			
	# Function to load the chromosomes of a
	# generation and the parameters
	def load_chromosome(self, filename):
		"""
		Function to load generation from which to resume
		from a file
		
		Parameters
		----------
		filename: string
			The name of the file from which the generation
			is going to be loaded
			
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		# Load the file
		self.population = np.loadtxt(filename, delimiter=' , ')
		self.__generations[0] = self.population
		
		# Get the filename explicitly without
		# path. Since the path is not that big
		# A simple for loop will suffice
		slice_index = 0
		for index in range(len(filename)):
			if(filename[index] == '/'):
				slice_index = index
		
		# Slice the .txt extension
		filename = filename[slice_index+1:-4]
		
		# Get the generation number 
		# It can be a percentage or an
		# exact number
		name_size = len(filename)
		if(filename[name_size-1] == '%'):
			filename = filename[:name_size-1]
			generation_resume = int(float(filename[10:]) * self.number_of_generations / 100)
		else:
			generation_resume = int(filename[10:])
			
		# Make the parameters same
		self.population_size = self.population.shape[0]
		self.chromosome_length = self.population.shape[1]
		self.generation_start = generation_resume
		
	# Function to remove a chromosome
	# file
	def remove_chromosome(self, filename):
		"""
		Function to remove a generation file
		"""
		# Simple removal
		os.remove(filename + '.txt')
	
	# Run the complete Genetic Algorithm
	def run(self, filename=None):
		"""
		Simulate the complete run of the algorithm
		
		Parameters
		----------
		filename(optional): string
			A filename specifying from what parameters
			or generation to start the algorithm
			
			The filename should be the same as generated
			by the algorithm.
		
		Returns
		-------
		best_chromosome: array like
			An array of alleles ranging from [0, 1] that has the best
			fitness value among all the generations
			
		Raises
		------
		None
		"""
		# Make a directory if it does not exist
		if not os.path.exists('./log'):
			os.makedirs('./log')
		
		# Generate a random population
		self.generate_population()
		
		# Append to the Generations
		self.__generations.append(self.population)
		
		# Print the legend
		legend = ["Generation", "Maximum Fitness", "Average Fitness", "Minimum Fitness"]
		print("{: <10} {: >20} {: >20} {: >20}".format(*legend))
		
		# Save the current generation
		self.save_chromosome(self.population, './log/generation0%', header="Generation #0")
		
		# Set the start variable
		self.generation_start = 1
		
		if(filename != None):
			self.load_chromosome(filename)
		
		# Keep going through generations with selection,
		# crossover and mutation
		for generation in range(self.generation_start, self.number_of_generations + 1):
			# For statistics
			self.current_generation = generation - 1
			
			# Check the current fraction and save if required
			if(generation % int(self.replay_fraction * (self.number_of_generations)) == 0):
				fraction = float(generation) / float(self.number_of_generations)
				self.save_chromosome(self.population, './log/generation' + str(int(100 * fraction)) + "%", 
									 "Generation #" + str(self.current_generation))
			
			# Determine the fitness of all the individuals
			self.determine_fitness()
			
			# Select the individuals for crossover
			self.selection()
			
			# Cross over generates the next generation
			self.crossover()
			
			# Apply mutation
			self.mutation()
			
			# Append to generations
			self.__generations.append(self.population)
			
			# Save the current generation
			self.save_handler()
			# Delete the previous one
			if(self.current_generation > 0):
				delete_process = multiprocessing.Process(target=self.remove_chromosome,
													 args=('./log/generation' + str(self.current_generation-1),))
													
				delete_process.start()
			
		
		# Save the required values
		self.save_statistics('./log/stats')
		self.save_chromosome(self.__best_chromosomes, './log/best_chromosomes')
		
		# Print the best fitness and return the chromosome
		print("The best fitness value acheived is: " + str(self.best_fitness))
		print("Found in generation # " + str(self.best_generation))
		
		return self.best_chromosome
		
	# Function that actually runs the training phase
	def evolve(self, filename=None):
		evolve_process = multiprocessing.Process(target=self.run, args=(filename,))
		evolve_process.start()
	
	# Function that is run to save
	# the current generation
	def save_handler(self):
		"""
		Function to handle the saving of the
		generations
		"""
		# Save the current generation chromosomes
		self.save_chromosome(self.__generations[self.current_generation - self.generation_start], 
							 './log/generation' + str(self.current_generation - 1), 
							 header='Generation #' + str(self.current_generation - 1))
		
		# Save the current best
		self.save_chromosome(np.array([self.best_chromosome]), './log/current_best', 
							 header="Found in generation #" + str(self.best_generation))
		
	# Getters and Setters
	@property
	def population_size(self):
		""" Attribute for the size of population 
			Population Size should be an even number
		"""
		return self._population_size
		
	@population_size.setter
	def population_size(self, population_size):
		if(population_size <= 0):
			self._population_size = 10
		else:
			self._population_size = population_size
			
		if(self._population_size % 2 == 1):
			warnings.warn("The population size should be even!")
			
	@property
	def number_of_generations(self):
		""" Attribute for the number of generations """
		return self._number_of_generations
		
	@number_of_generations.setter
	def number_of_generations(self, number_of_generations):
		if(number_of_generations <= 0):
			self._number_of_generations = 10
		else:
			self._number_of_generations = number_of_generations
			
	@property
	def mutation_probability(self):
		""" Attribute for the probability of mutation """
		return self._mutation_probability
		
	@mutation_probability.setter
	def mutation_probability(self, mutation_probability):
		if(mutation_probability > 1 or mutation_probability < 0):
			self._mutation_probability = 0.01
		else:
			self._mutation_probability = mutation_probability
			
	@property
	def chromosome_length(self):
		""" Attribute for the length of chromosome """
		return self._chromosome_length
		
	@chromosome_length.setter
	def chromosome_length(self, chromosome_length):
		if(chromosome_length <= 0):
			self._chromosome_length = 5
		else:
			self._chromosome_length = chromosome_length
			
	@property
	def number_of_elites(self):
		""" Attribute for the number of elites in the algorithm """
		return self._number_of_elites
		
	@number_of_elites.setter
	def number_of_elites(self, number_of_elites):
		if(number_of_elites < 0):
			self._number_of_elites = 0
		elif(number_of_elites > self.population_size):
			self._number_of_elites = self.population_size
		else:
			self._number_of_elites = number_of_elites
			
		# Trick, sum of numbers with same partiy is even
		if((self._number_of_elites + self._population_size) % 2 == 1):
			# Reduce the number of elites by 1, as the algorithm
			# would not work otherwise
			self._number_of_elites -= 1
			
	@property
	def replay_fraction(self):
		""" Attribute to specify the fraction of 
			number of generations to save
		"""
		return self._replay_fraction
		
	@replay_fraction.setter
	def replay_fraction(self, fraction):
		# Some adjustments
		if(abs(fraction) > 1 and abs(fraction) <= self.number_of_generations):
			fraction = fraction / self.number_of_generations
		elif(abs(fraction) > self.number_of_generations):
			fraction = self.number_of_generations
		
		self._replay_fraction = fraction
			
	@property
	def fitness_function(self):
		""" Attribute for the fitness function 
			The user is required to set it 
			according to their use case
			
			The fitness function is requried to take
			a single argument of chromosome and return
			the fitness value of the chromosome
		"""
		return self._fitness_function
		
	@fitness_function.setter
	def fitness_function(self, fitness_function):
		self._fitness_function = fitness_function
		
		
		
	
		
		
