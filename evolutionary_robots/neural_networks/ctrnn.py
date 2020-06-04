# This module contains the implementation of Continuous Time Recurrent Neural Network
# The network is more or less similar to the Static Neural Network
# Making the time interval equal to the time constant gives us the Static Neural Network

# CTRNNs work based on a differential equation
# In terms of our computer, the differential equation is modelled in discrete manner
# In this implementation the discrete manner is first order euler solution
# But the user can change this implementation in any way he/she likes!

# https://neat-python.readthedocs.io/en/latest/ctrnn.html

import numpy as np
import pickle
from graphviz import Digraph
from nn import Layer, NeuralNetwork

# CTRNN Layer
# CTRNN has to save the state of the previous output
# and then calculate the weighted average of the previous and the current output
# to get the total output
class CTRNNLayer(Layer):
	# time_interval is a scalar
	# time_constant is a list, as it is different for each i-th neuron
	def __init__(self, input_dim, output_dim, time_interval, time_constant, activation_function, layer_name):
		# Name of the layer
		self.layer_name = layer_name
		
		# Weight and bias dimensions
		self.weight_dim = (output_dim, input_dim)
		self.bias_dim = (output_dim, 1)
		
		# Initialize the weight and bias
		self.weight_matrix = np.random.rand(*self.weight_dim)
		self.bias_vector = np.random.rand(output_dim)
		
		# Generate the weights for the weighted average
		self.time_constant = time_constant
		self.time_weight = np.asarray(float(time_interval) / np.array(time_constant))
		
		# Set the activation function
		self.activation_function = activation_function
		
		# Set the previous state output, zero for initial
		self.previous_output = np.zeros(output_dim)
		
	# First order euler step
	def euler_step(self, input_vector):
		# Convert to numpy array
		input_vector = np.array(input_vector)
		
		# Get the current activation
		current_activation = np.add(np.dot(self.weight_matrix, input_vector), self.bias_vector)
		current_activation = self.activation_function(current_activation)
		
		# Generate the current output
		# This equation is the first order euler solution
		current_output = self.previous_output * (1 - self.time_weight) + current_activation * self.time_weight
		
		# Save it!
		self.previous_output = current_output
		
		return current_output
		
	# Function to set the weight matrix	
	def set_weight_matrix(self, weight_matrix):
		self.weight_matrix = weight_matrix
		
	# Function to return the weight matrix
	def get_weight_matrix(self):
		return self.weight_matrix
	
	# Function to set the bias vector	
	def set_bias_vector(self, bias_vector):
		self.bias_vector = bias_vector
		
	# Function to return the bias vector
	def get_bias_vector(self):
		return self.bias_vector
		
	# Function to return the layer name
	def get_name(self):
		return self.layer_name
		
	# Function to return the weight dimensions
	def get_weight_dim(self):
		return self.weight_dim
		
	# Function return the bias dimensions
	def get_bias_dim(self):
		return self.bias_dim
		
	# Function to return the time constant list
	def get_time_constant(self):
		return self.time_constant
		
	# Function to return the layer name
	def get_name(self):
		return self.layer_name
		
# CTRNN Network
class CTRNN(NeuralNetwork):
	# The layer_dimensions is an array with the following layout
	# [[number_of_nodes_in_first_layer(input_layer), list_of_time_constants, activation_function], [number_of_nodes_in_second_layer, list_of_time_constants, activation_function], ..., [number_of_nodes_in_output]]
	def __init__(self, layer_dimensions, time_interval):
		# Initialize a layer vector, a list of Layer objects
		self.layer_vector = []
		
		# Append the Layer classes
		for i in range(len(layer_dimensions) - 1):
			self.layer_vector.append(CTRNNLayer(layer_dimensions[i][0], layer_dimensions[i+1][0], time_interval, layer_dimensions[i][1], layer_dimensions[i][2], "Layer " + str(i)))
			
		# Number of layers
		self.number_of_layers = len(self.layer_vector)
		# Construct a visual component
		self.visual = Digraph(comment="Continous Time Recurrent Neural Network", graph_attr={'rankdir': "LR", 'splines': "line"}, node_attr={'fixedsize': "true", 'label': ""})
		
	# Function to get output from input_vector
	def forward_propagate(self, input_vector):
		# Convert the input_vector to numpy array
		intermediate_output = np.array(input_vector)
		
		# Forward propagate for each layer
		for layer in self.layer_vector:
			intermediate_output = layer.euler_step(intermediate_output)
			
		return intermediate_output

	# Function to save the layer weights
	def save_weights_to_file(self, file_name):
		# Use pickle to save the layer_vector
		with open(file_name, 'wb') as f:
			pickle.dump(self.layer_vector, f)
			
	# Function to load the layer weights
	def load_weights_from_file(self, file_name):
		# Use pickle to load the layer_vector
		with open(file_name, 'rb') as f:
			self.layer_vector = pickle.load(f)
			
	# Function to return the weights and bias in the form of a vector
	def return_weights_as_vector(self):
		# Initialize the output vector
		# Determine an individual layer's weight matrix in row major form and then it's bias
		# Then concatenate it with the previous output vector
		output = np.array([])
	
		for layer in self.layer_vector:
			# The vector we get from flattening the weight matrix
			# flatten() works in row major order
			weight_vector = layer.get_weight_matrix().flatten()
			
			# The vector we get from flattening the bias vector
			bias_vector = layer.get_bias_vector().flatten()
			
			# The output vector is concatenated form of weight_vector and bias_vector
			output = np.concatenate([output, weight_vector, bias_vector])
		
		return output
	
	# Function to load the weights and bias from vector
	def load_weights_from_vector(self, weight_vector):
		# Convert to numpy array
		weight_vector = np.array(weight_vector)
	
		# Interval counter maintains the current layer index
		interval_counter = 0
		
		for layer in self.layer_vector:
			# Get the dimensions of the weight matrix and bias vector
			weight_dim = layer.get_weight_dim()
			bias_dim = layer.get_bias_dim()
			
			# Get the interval at which weight and bias seperate
			weight_interval = weight_dim[0] * weight_dim[1]
			
			# Get the interval at which the bias and next weight vector seperate
			bias_interval = bias_dim[0] * bias_dim[1]
			
			# Seperate the weights and bias and then reshape them
			layer.set_weight_matrix(weight_vector[interval_counter:interval_counter + weight_interval].reshape(weight_dim))
			interval_counter = interval_counter + weight_interval
			layer.set_bias_vector(weight_vector[interval_counter:interval_counter + bias_interval].reshape(bias_dim[0],))
			interval_counter = interval_counter + bias_interval
			
	
	# Function to generate the visual representation
	def generate_visual(self, filename, view=False):
		# We need many subgraphs
		for layer in range(self.number_of_layers):
			subgraph = Digraph(name="cluster_" + str(layer), graph_attr={'color': "white", 'label': "Layer " + str(layer)}, node_attr={'style': "solid", 'color': "black", 'shape': "circle"})
			
			# Get the weight dimensions for generating the nodes
			weight_dim = self.layer_vector[layer].get_weight_dim()
			
			# Get the time constants
			if layer != 0:
				time_constants = self.layer_vector[layer-1].get_time_constant()
			
			for node_number in range(weight_dim[1]):
				if layer == 0:
					subgraph.node("layer_" + str(layer) + str(node_number+1))
				else:
					subgraph.node("layer_" + str(layer) + str(node_number+1), label=str(time_constants[node_number]), fontcolor='green')
				
			# Declare subgraphs
			self.visual.subgraph(subgraph)
			
			
		# The final layer needs to be done manually
		subgraph = Digraph(name="cluster_" + str(self.number_of_layers), graph_attr={'color': "white", 'label': "Layer " + str(self.number_of_layers)}, node_attr={'style': "solid", 'color': "black", 'shape': "circle"})
		
		# Get the weight dimensions
		weight_dim = self.layer_vector[self.number_of_layers - 1].get_weight_dim()
		
		# Get the time constants
		time_constants = self.layer_vector[self.number_of_layers - 1].get_time_constant()
		
		for node_number in range(weight_dim[0]):
			subgraph.node("layer_" + str(self.number_of_layers) + str(node_number+1), label=str(time_constants[node_number]), fontcolor='green')
			
		# Declare the subgraph
		self.visual.subgraph(subgraph)
		
		
		for layer in range(self.number_of_layers):
			# Get the weight dimensions for generating the nodes
			weight_dim = self.layer_vector[layer].get_weight_dim()
		
			# Put the edges in the graph
			for input_node in range(weight_dim[1]):
				for output_node in range(weight_dim[0]):
					self.visual.edge("layer_" + str(layer) + str(input_node+1), 'layer_' + str(layer + 1) + str(output_node+1))
		
		# Render the graph		
		self.visual.render('representations/' + filename + '.gv', view=view)		
	
		
		
		
		
		
