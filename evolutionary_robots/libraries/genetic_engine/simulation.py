""" Docstring for the simulation.py module

This module contains the simulation aspect of our parallel physics engine
named genetic_engine. The simulation module will be executed in a Thread based
fashion. In this way, multiple threads of simulation can be run, making the
training faster. Also, we are going to have a time step control over the 
simulation, making it deterministic as well.

"""

import multiprocessing
from math_engine import line, point, algorithms

class Simulation(multiprocessing.Process, object):
	"""
	Simulation class. The various exercises can
	subclass this class to create their own environments
	
	...
	Parameters
	----------
	boundary: list of Point objects
		Vertex points of the boundary
		
	robot: Robot class object
		The robot in the environment
	
	delta_time(optional): float
		The time with which the simulation proceeds
	
	Attributes
	----------
	delta_time: float
		The time with which the simulation proceeds
		
	current_time: float
		The current time of the simulation
		
	boundary_points: list of Point objects
		The list of vertices of boundary
		
	boundary_edges: list of Line objects
		The list of edges of the boundary
		
	robot: Robot object
		The robot used in the simulation
	
	Methods
	-------
	run()
		This function is supposed to be designed according to
		the exercise
	
	collision_checker()
		Function to check if the robot has crossed the boundary
	
	collision_resolver(collision_list)
		Function to resolve the collisions/illegal move of the robot
	"""
	def __init__(self, robot, boundary, delta_time=0.0001):
		"""
		Initialization function of the class
		
		...
		Parameters
		----------
		delta_time: float
			The time with which the simulation proceeds
		
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		# Constructor of Thread parent class
		multiprocessing.Process.__init__(self)
		
		# Initialize variables
		self.delta_time = delta_time
		self.current_time = 0
		self.boundary_points = boundary
		self.robot = robot
		
	def _define_boundary(self):
		"""
		Auxillary function to define the edges of the boundary
		using the points of boundary
		...
		
		Parameters
		----------
		None
		
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		boundary = self.boundary_points
		
		# Loop over the points and generate the edges
		self.boundary_edges = []
		
		for index in range(len(boundary) - 1):
			edge = line.Line()
			edge.line_from_points(boundary[index], boundary[index + 1])
			self.boundary_edges.append(edge)
			
		# Loop over the complete ones
		edge = line.Line()
		edge.line_from_points(boundary[0], boundary[-1])
		self.boundary_edges.append(edge)
	
	def run(self):
		"""
		This function is supposed to be designed according to
		the exercise
		"""
		pass
		
	def collision_checker(self):
		"""
		Function to check whether the robot has collided or
		made an illegal movee
		
		...
		Parameters
		----------
		None
		
		Returns
		-------
		inside: Boolean
			Whether the robot is in legal space
			
		Raises
		------
		None
		
		Note
		----
		The robot is considered a point for now, for simplification
		"""
		
		# Considering the robot a point object
		# We just need to check if the robot is 
		# inside the boundary points or not
		inside = algorithms.point_inside_perimeter(self.robot.position,
												   self.boundary_edges)
		
		return inside
		
	def collision_resolver(self, inside):
		"""
		Function to resolve the collisions/illegal move
		of the robot
		
		...
		Parameters
		----------
		None
			
		Returns
		-------
		None
		
		Raises
		------
		None
			
		Notes
		-----
		For now, the collision resolution is simple, only the
		last move of the robot is reverted
		"""
		
		if(inside == False):
			# Revert to the previous state of the robot
			self.robot.move(-1 * self.delta_time)	
	
	@property
	def delta_time(self):
		""" The factor of time which to increment """
		return self._delta_time
		
	@property
	def current_time(self):
		""" The current time of the simulation """
		return self._current_time
		
	@property
	def boundary_points(self):
		""" List of points defining the boundary of the environment """
		return self._boundary_points
		
	@property
	def boundary_edges(self):
		""" List of edges defining the boundary of the environment """
		return self._boundary_edges
		
	@property
	def robot(self):
		""" The robot used for the simulation """
		return self._robot
	
	@delta_time.setter
	def delta_time(self, delta):
		self._delta_time = delta
		
	@current_time.setter
	def current_time(self, current):
		self._current_time = current
		
	@boundary_points.setter
	def boundary_points(self, points):
		self._boundary_points = points
		self._define_boundary()
		
	@boundary_edges.setter
	def boundary_edges(self, edges):
		self._boundary_edges = edges
		
	@robot.setter
	def robot(self, robot):
		self._robot = robot

	
