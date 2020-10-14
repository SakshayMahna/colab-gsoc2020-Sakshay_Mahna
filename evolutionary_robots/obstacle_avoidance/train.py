# An example for creating a robot simulation using genetic_engine
# and training it using Genetic Algorithms, the obstacle avoidance task
import sys
sys.path.append('./../libraries')

import numpy as np
import time
import math
import multiprocessing

from genetic_engine import robot, sensor, simulation
from genetic_engine.math_engine import point, line, algorithms
from genetic_algorithm.ga_engine import GeneticAlgorithmEngine

import MyAlgorithm as algorithm


# The simulation class
class ObstacleAvoidance(simulation.Simulation):
	def __init__(self, neural_network, evaluation_time, fitness_function):
		roombaIR = robot.Robot()
		boundary = [point.Point(-5, 5), point.Point(5, 5),
					point.Point(5, -5), point.Point(-5, -5)]
					
		self.evaluation_time = evaluation_time
		self.neural_network = neural_network
		self.fitness_function = fitness_function
		self.fitness_values = multiprocessing.Array('f', 
							  [0 for i in range(int(evaluation_time / 0.01) + 1)])
					
		simulation.Simulation.__init__(self, roombaIR, boundary, 0.01)
		
	def run(self):
		# Steps in a single run
		self.robot.reset_position()
		self.robot.set_linear_velocity(0)
		self.robot.set_angular_velocity(0)
		
		index = 0
		
		while self.current_time < self.evaluation_time:
			# Increment time
			self.current_time = self.current_time + self.delta_time
			
			# Sense the environment
			infrared = self.robot.sensor_values(self.boundary_edges)
			output = self.neural_network.forward_propagate({"INFRARED": infrared})["MOTORS"]
			
			# Calculate and store fitness
			self.fitness_values[index] = self.fitness_function(output[0], output[1], infrared)
			index = index + 1
			
			# Set the current velocities
			self.robot.set_linear_velocity(2 * (output[0] + output[1]))
			self.robot.set_angular_velocity(2 * (output[0] - output[1]))
			
			# Move the robot
			self.robot.move(self.delta_time)
			#print(self.robot.position.x, self.robot.position.y, self.robot.orientation)
			
			# Collision detection and resolution
			inside = self.collision_checker()
			self.collision_resolver(inside)
		
	@property
	def fitness_function(self):
		return self._fitness_function
		
	@fitness_function.setter
	def fitness_function(self, function):
		self._fitness_function = function
		
	@property
	def fitness_values(self):
		return self._fitness_values
		
	@fitness_values.setter
	def fitness_values(self, values):
		self._fitness_values = values
		
	@property
	def evaluation_time(self):
		return self._evaluation_time
		
	@evaluation_time.setter
	def evaluation_time(self, steps):
		self._evaluation_time = steps
		
	@property
	def neural_network(self):
		return self._neural_network
		
	@neural_network.setter
	def neural_network(self, network):
		self._neural_network = network
		
# Define the Neural Network
neural_network = algorithm.define_neural_network()

# Define the Genetic Algorithm
ga = GeneticAlgorithmEngine(ObstacleAvoidance, neural_network,
							algorithm.EVALUATION_STEPS, 0.01)

# Set the population size of the algorithm
ga.population_size = algorithm.POPULATION_SIZE

# Set the mutation probability
ga.mutation_probability = algorithm.MUTATION_PROBABILITY

# Set the number of elites
ga.number_of_elites = algorithm.NUMBER_OF_ELITES

# Set the number of generations of the algorithm
ga.number_of_generations = algorithm.NUMBER_OF_GENERATIONS

# Set the log folder
ga.log_folder = algorithm.LOG_FOLDER

# Set the fitness function
ga.fitness_function = algorithm.fitness_function

print(ga.run())


		
