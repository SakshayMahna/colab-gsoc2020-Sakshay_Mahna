"""
Point module for Math Engine
"""

class Point(object):
	"""
	This class contains the representation of a 2D point
	in the format (x, y) and some functions related to that
	
	Parameters
	----------
	x: float (default: 0)
	
	y: float (default: 0)
	
	Attributes
	----------
	Attributes are the same as the parameters
	"""
	def __init__(self, x=0, y=0):
		"""
		Initialization function for Point
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
		self.x = x
		self.y = y
		
	@property
	def x(self):
		""" (x, y) """
		return self._x
		
	@property
	def y(self):
		""" (x, y) """
		return self._y
		
	@x.setter
	def x(self, x):
		self._x = x
		
	@y.setter
	def y(self, y):
		self._y = y
