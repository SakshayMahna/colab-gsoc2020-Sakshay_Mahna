"""
Line module for Math Engine
"""
from point import Point
import math

class Line(object):
	"""
	This class contains the representation of a line
	in the format ax + by + c = 0 and some functions
	related to that
	
	Parameters
	----------
	a: float (default: 0)
	
	b: float (default: 0)
	
	c: float (default: 0)
	
	Attributes
	----------
	Attributes are the same as the parameters
	
	Methods
	-------
	line_from_points(point0, point1)
		Define a line from two given points
		
	line_from_orientation(orientation, point)
		Define a line from a point and it's orientation
	"""
	def __init__(self, a=0, b=0, c=0):
		"""
		Initialization function for Line
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
		self.a = a
		self.b = b
		self.c = c
		
	def line_from_points(self, point0, point1):
		"""
		Define a line from two given points
		...
		
		Parameters
		----------
		point0: Point object
			A point in the form of a Point object
			
		point1: Point object
			A point in the form of a Point object
			
		Returns
		-------
		None
		
		Raises
		------
		None
		
		Note
		----
		y - y0 = ((y1-y0)/(x1-x0)) * (x - x0)
		0 = (y1 - y0) * x + (x0 - x1) * y + (x1 - x0) * y0 + (y0 - y1) * x0
			
		a = y1 - y0
		b = x0 - x1
		c = x1*y0 - x0*y1
		"""
		
		self.a = point1.y - point0.y
		self.b = point0.x - point1.x
		self.c = point1.x * point0.y - point0.x * point1.y
		
	def line_from_orientation(self, orientation, point):
		"""
		Define a line from a point and it's orientation
		...
		
		Parmeters
		---------
		orientation: float
			Orientation is the angle measured(in radians) from
			positive X axis in anticlockwise direction
			
		point: Point object
			A point in the form of a Point object
			
		Returns
		-------
		None
		
		Raises
		------
		None
		
		Note
		----
		Orientation is the angle measured from positive X axis in
		anticlockwise direction
			
		y - y0 = tan(o) * (x - x0)
		0 = sin(o) * x (-cos(o)) * y + cos(o) * y0 + (-sin(o)) * x0
			
		a = sin(o)
		b = -cos(o)
		c = cos(o)*y0 - sin(o)*x0  
		"""	
		
		self.a = math.sin(orientation)
		self.b = -1 * math.cos(orientation)
		self.c = math.cos(orientation) * point.y -\
				 math.sin(orientation) * point.x
		
	@property
	def a(self):
		""" ax + by + c = 0 """
		return self._a
		
	@property
	def b(self):
		""" ax + by + c = 0 """
		return self._b
		
	@property
	def c(self):
		""" ax + by + c = 0 """
		return self._c
	
	@a.setter
	def a(self, a):
		self._a = a
		
	@b.setter
	def b(self, b):
		self._b = b
		
	@c.setter
	def c(self, c):
		self._c = c
		
	
