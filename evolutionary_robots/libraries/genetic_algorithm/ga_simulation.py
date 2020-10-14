"""Docstring for ga_simulation.py

This module implements the Genetic
Algorithm class adapted to the Robotics
Academy Template simulation

To be used for testing the parameters of the network
"""

import numpy as np
from copy import deepcopy
from genetic_algorithm.ga_nn import GeneticAlgorithmNN

class GeneticAlgorithmGazebo(GeneticAlgorithmNN):
	"""
	An inherited class from GeneticAlgorithmNN
	This class provides an interface to use
	GeneticAlgorithm and ArtificialNeuralNetwork 
	class with Robotics Academy Template Gazebo
	Simulation
	
	...
	Parameters
	----------
	neural_network: ArtificialNeuralNetwork object
		An instance of the ArtificialNeuralNetwork object
		
	Rest of the parameters are the same
	
	Attributes
	----------
	test_network: array_like
		Sets a network whose parameters we don't
		require to change too much.
		
		Takes in a list of paramters and converts
		it to the required neural network
		
	Rest of the attributes are the same
	
	Methods
	-------
	test_output(input_dict)
		Calculates the output of the test network
		
	Rest of the methods are the same
	"""
	def __init__(self, neural_network, population_size=100,
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
		# Initialize the Parent Class
		GeneticAlgorithmNN.__init__(self, neural_network, population_size,
									number_of_generations, mutation_probability,
									number_of_elites)
									
		self._test_network = None
									
	def test_output(self, input_dict):
		"""
		Function used to work with test network
		It calculates the output for a given input_dict
		"""
		output = self.test_network.forward_propagate(input_dict)
		
		return output
			
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
	
