"""
Sensor for minimalistic physics engine

Assumptions:

- The robot body is circular
- There are no obstacles in the environment, only the boundary
- The sensors are of IR type, they only sense the distance from their position
  to the boundary
"""

from math_engine import line, point, algorithms
import math

class Sensor(object):
	"""
	This class contains the implementation of IR sensors
	to be attached to the body
	
	Parameters
	----------
	sensor_position: float
		The relative yaw with respective to the robot orientation
	
	Attributes
	----------
	Attributes are the same as the parameters
	Additionally, 
	
	sensor_range: float
		The maximum distance the sensor can read
		
	Methods
	-------
	read(robot_pose, robot_yaw, boundary_edges)
		Get a reading from sensor
		
	sensor_value(robot_pose, robot_yaw, robot_radius, boundary_edges)
		A wrapper function for read just to give the exact
		sensor value by clipping the euclidean distance
	"""
	def __init__(self, sensor_position):
		"""
		Initialization function for Sensor
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
		self.position = sensor_position
		self.sensor_range = 1
		
	def read(self, robot_pose, robot_yaw, boundary_edges):
		"""
		Get a reading from sensor
		...
		
		Parmeters
		---------
		robot_pose: Point object
			The coordinates of the robot in Cartesian Plane
			
		robot_yaw: float
			The orientation of the robot
			
		boundary_edges: list of Line objects
			The list of the Line objects constituting the boundary
			
		Returns
		-------
		None
		
		Raises
		------
		None
		
		Note
		----
		The algorithm is as follows:
			- Determine the line that is formed by the sensor
			- Determine the points of intersection of the 
			  sensor line and boundary
			- The point that is facing towards the orientation of the robot
			  (dot product) and is inside the boundary is returned
			  
		Assumption taken is that our boundary is going to rectangular,
		Therefore at most 2 seperate points are going to intersect 
		"""
		#Calculating position from robot pose
		yaw = self.position + robot_yaw
		
		# Make line from the position of sensor
		sensor_line = line.Line()
		sensor_line.line_from_orientation(yaw, robot_pose)
		
		# Generate lines from boundary and get intersection points
		intersection_points = []
		for edge in boundary_edges:
			try:
				inter_point = algorithms.intersection_point(sensor_line, edge)
				intersection_points.append(inter_point)
			except AssertionError:
				pass
				
		# Loop over intersection points(only going to be 2 in our case)
		# and return the one with a positive constant
		for i_point in intersection_points:
			inside = algorithms.point_inside_perimeter(i_point, boundary_edges)
			vector1 = point.Point(math.cos(robot_yaw), math.sin(robot_yaw))
			vector2 = point.Point(i_point.x - robot_pose.x, 
								  i_point.y - robot_pose.y)
			dot_product = algorithms.dot_product(vector1, vector2)
			
			if(inside == True and \
			(abs(self.position) <= math.pi/2 and dot_product >= 0)):
				return i_point
			elif(inside == True and \
			(abs(self.position) > math.pi/2 and dot_product < 0 )):
				return i_point
				
	def sensor_value(self, robot_pose, robot_yaw, robot_radius, boundary_edges):
		"""
		A wrapper function for read just to give the exact
		sensor value by clipping the euclidean distance
		...
		Parmeters
		---------
		robot_pose: Point object
			The coordinates of the robot in Cartesian Plane
			
		robot_yaw: float
			The orientation of the robot
			
		robot_radius: float
			The radius of the robot
			
		boundary_edges: list of Line objects
			The list of the Line objects constituting the boundary
			
		Returns
		-------
		None
		
		Raises
		------
		None
		"""
		
		point1 = robot_pose
		point2 = self.read(robot_pose, robot_yaw, boundary_edges)
		
		try:
			distance = algorithms.euclidean_distance(point1, point2) - robot_radius
		except AttributeError:
			distance = 0
		
		if(distance <= self.sensor_range):
			return 1 - distance
		else:
			return 1 - self.sensor_range
		
	@property
	def position(self):
		""" The relative yaw with respect to the robot """
		return self._position
		
	@property
	def sensor_range(self):
		""" The maximum value that the sensor can provide """
		return self._sensor_range
		
	@sensor_range.setter
	def sensor_range(self, sensor_range):
		self._sensor_range = sensor_range
		
	@position.setter
	def position(self, sensor_position):
		self._position = sensor_position	
