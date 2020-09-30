# An example for creating a robot simulation using genetic_engine
# and training it using Genetic Algorithms, the obstacle avoidance task
import sys
sys.path.append('./../')

import numpy as np
import time
import math

from genetic_engine import robot, sensor, simulation
from genetic_engine.math_engine import point, line, algorithms
from genetic_algorithm.ga_engine import GeneticAlgorithmEngine
from neural_networks.ann import ArtificialNeuralNetwork
from neural_networks.interface import Layer
from neural_networks.activation_functions import *


# The simulation class
class ObstacleAvoidance(simulation.Simulation):
	def __init__(self, neural_network, evaluation_time, fitness_function):
		roombaIR = robot.Robot()
		boundary = [point.Point(-300, 300), point.Point(300, 300),
					point.Point(300, -300), point.Point(-300, -300)]
					
		self.evaluation_time = evaluation_time
		self.neural_network = neural_network
		self.fitness_function = fitness_function
		self.fitness_values = []
					
		simulation.Simulation.__init__(self, roombaIR, boundary)
		
	def run(self):
		# Steps in a single run
		while self.current_time < self.evaluation_time:
			# Increment time
			self.current_time = self.current_time + self.delta_time
			
			# Sense the environment and 
			# Set the current velocities
			infrared = self.robot.sensor_values(self.boundary_edges)
			output = self.neural_network.forward_propagate({"INFRARED": infrared})["MOTORS"]
			self.robot.set_linear_velocity(output[0] + output[1])
			self.robot.set_angular_velocity(output[0] - output[1])
			
			# Calculate and store fitness
			self.fitness_values.append(
				self.fitness_function(output[0], output[1], infrared)
			)
			
			# Move the robot
			self.robot.move(self.delta_time)
			
			# Collision detection and resolution
			inside = self.collision_checker()
			self.collision_resolver(inside)
			
		return self.fitness_values
		
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
		
##########################################################################		

# Define the Neural Network
inputLayer = Layer("inputLayer", 8, IdentityActivation(), "INFRARED", ["outputLayer"])
outputLayer = Layer("outputLayer", 2, TanhActivation(), "", ["MOTORS"])

neural_network = ArtificialNeuralNetwork([inputLayer, outputLayer], "STATIC")

###########################################################################

# Define the fitness function
def fitness_function(left_motor_speed, right_motor_speed, infrared):
	# Code the fitness function here
	V = abs(left_motor_speed) + abs(right_motor_speed)
	delta_v = abs(right_motor_speed - left_motor_speed)
	i = np.max(infrared)
	
	fitness = V * (1 - math.sqrt(delta_v)) * (1 - i) * (left_motor_speed + 0.5) * (right_motor_speed + 0.5)
	return fitness
	
###########################################################################

# Define the Genetic Algorithm
ga = GeneticAlgorithmEngine(ObstacleAvoidance, neural_network)

# Set the population size of the algorithm
ga.population_size = 50

# Set the mutation probability
ga.mutation_probability = 0.01

# Set the number of elites
ga.number_of_elites = 0

# Set the number of generations of the algorithm
ga.number_of_generations = 1000

# Set the fitness function
ga.fitness_function = fitness_function

print(ga.run())


		
