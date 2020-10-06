"""
Robot for minimalistic physics engine

Assumptions:

- The robot body is circular
- There are no obstacles in the environment, only the boundary
- The sensors are of IR type, they only sense the distance from their position
  to the boundary
- The sensors are attached to the boundary of the robot
"""

from math_engine import line, point, algorithms
from sensor import Sensor
import math

class Robot(object):
	"""
	This class contains the implementation of the robot
	iRobot Roomba
	
	Parameters
	----------
	position(default value: (0, 0)): Point object
		The current position of the robot
		
	orientation(default value: pi/2): float
		The current orientation of the robot
	
	linear_velocity(default value: 0): float
		The current linear velocity of the robot along it's orientation
	
	angular_velocity(default value: 0): float
		The current angular velocity of the robot about Z axis
	
	Attributes
	----------
	position(default value: (0, 0)): Point object
		The current position of the robot
		
	orientation(default value: pi/2): float
		The current orientation of the robot
	
	linear_velocity(default value: 0): float
		The current linear velocity of the robot along it's orientation
	
	angular_velocity(default value: 0): float
		The current angular velocity of the robot about Z axis
		
	sensors: list of Sensor object
		A list of sensors attached to the robot
		
	Methods
	-------
	define_sensors()
		Function to initialize sensors on robot
		
	set_linear_velocity()
		Function to set the linear velocity of the robot
		
	set_angular_velocity()
		Function to set the angular velocity of the robot
		
	move(time_step)
		Function to move the robot according to the
		time step and velocity
	"""
	
	def __init__(self, position=point.Point(), orientation=math.pi/2,
	 			linear_velocity=0, angular_velocity=0):
	 	"""
	 	Initialization function for Robot
		...
		
		Parameters
		----------
		Same as described in the class docstring
		
		Returns
		-------
		None
		
		Raises
		------
		None
	 	"""
	 	# These shouldn't be changed by external factors
	 	# Only the internal functions should change them
	 	self.position = position
	 	self.orientation = orientation
	 	
	 	# Except these!
	 	self.linear_velocity = linear_velocity
	 	self.angular_velocity = angular_velocity
	 	
	 	# Number of front and back sensors
	 	self.number_front_sensors = 6
	 	self.number_back_sensors = 2
	 	
	 	# Define the sensors
	 	self.define_sensors()
	 	
	def define_sensors(self):
		"""
		Function to initialize sensors on robot
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
		# Initialize
		self.sensors = []
		angle = -5 * math.pi / 6
		
		# Define the front sensors
		for i in range(self.number_front_sensors):
			sensor_i = Sensor(angle)
			self.sensors.append(sensor_i)
			angle = angle + math.pi / self.number_front_sensors
			
		# Define the back sensors
		angle = math.pi - math.pi / 12
		for i in range(self.number_back_sensors):
			sensor_i = Sensor(angle)
			self.sensors.append(sensor_i)
			angle = angle + math.pi / 6
			
	def set_linear_velocity(self, velocity):
		""" Function to set the linear velocity of the robot """
		self.linear_velocity = velocity
		
	def set_angular_velocity(self, velocity):
		""" Function to set the angular velocity of the robot """
		self.angular_velocity = velocity
		
	def reset_position(self):
		""" Function to reset the robot position """
		self.position.x = 0
		self.position.y = 0
			
	def move(self, time_step):
		"""
		Function to move the robot according to the
		time step and velocity
		...
		
		Parameters
		----------
		time_step: float
			How much to progress time by?
		
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		# Angular velocity
		self.orientation = self.orientation + self.angular_velocity * time_step
		
		# Linear Velocity
		x = self.linear_velocity * math.cos(self.orientation)
		y = self.linear_velocity * math.sin(self.orientation)
		
		self.position.x = self.position.x + x * time_step
		self.position.y = self.position.y + y * time_step
		
	def sensor_values(self, boundary_edges):
		"""
		Function to return the array of sensor outputs
		...
		
		Parameters
		----------
		boundary_edges: list of Line objects
			The edges of the boundary
			
		Returns
		-------
		infrared_output: list of floats
			The array of sensor outputs
			
		Raises
		------
		None
		"""
		infrared_output = []
		for infrared in self.sensors:
			infrared_output.append(infrared.sensor_value(self.position,
								   self.orientation, 0, boundary_edges))
								   
		return infrared_output
		
	 	
	@property
	def position(self):
		""" The current position of the robot """
		return self.__position
		
	@property
	def orientation(self):
		""" The current orientation of the robot """
		return self.__orientation
		
	@property
	def linear_velocity(self):
		""" The linear velocity of the robot """
		return self.__linear_velocity
		
	@property
	def angular_velocity(self):
		""" The angular velocity of the robot """
		return self.__angular_velocity
	
	@property
	def sensors(self):
		""" Array containing the sensors of the robot """
		return self.__sensors
		
	@sensors.setter
	def sensors(self, sensor_list):
		self.__sensors = sensor_list
		
	@position.setter
	def position(self, position):
		self.__position = position
		
	@orientation.setter
	def orientation(self, orientation):
		self.__orientation = orientation % (2 * math.pi)
		
	@linear_velocity.setter
	def linear_velocity(self, velocity):
		self.__linear_velocity = velocity
		
	@angular_velocity.setter
	def angular_velocity(self, velocity):
		self.__angular_velocity = velocity
		
