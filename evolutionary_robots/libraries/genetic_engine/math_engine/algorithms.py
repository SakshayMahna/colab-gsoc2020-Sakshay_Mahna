"""
Module for algorithms and functions on lines and points

Functions defined in this module

intersection_point(line1, line2)
	Function to determine the point of intersection
	of this line with some other line
	
point_inside_perimeter(point, boundary_edges)
	Function to determine whether the point is inside
	a perimeter of a boundary
	
dot_product(point1, point2)
	Function to calculate the dot product of 2 vectors
	represented as points
	
euclidean_distance(point1, point2)
	Calculate the euler distance between two points
"""

from line import Line
from point import Point
import math

def intersection_point(line1, line2):
	"""
	Function to determine the point of intersection
	of this line with some other line
	...
	
	Parameters
	----------
	line1: Line object
		The line with which intersection has to be calculated
		
	line2: Line object
		The line with which intersection has to be calculated
		
	Returns
	-------
	point: Point object
		The point of intersection
		
	Raises
	------
	AssertionError:
		The lines should be intersecting
	
	Notes
	-----
	a1x + b1y + c1 = 0
	a2x + b2y + c2 = 0
	
	x = (b1c2 - b2c1) / (a1b2 - a2b1)
	y = (a1c2 - a2c1) / (a2b1 - a1b2)
	"""
	
	a1 = line1.a; b1 = line1.b; c1 = line1.c
	a2 = line2.a; b2 = line2.b; c2 = line2.c
	
	assert (a1*b2)-(b1*a2) != 0, "The lines are either parallel or collinear"
	
	point = Point()
	point.x = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)
	point.y = (a1 * c2 - a2 * c1) / (a2 * b1 - a1 * b2)
	
	return point
	
def point_inside_perimeter(point, boundary_edges):
	"""
	Function to determine whether the point is inside
	a perimeter of a boundary
	...
	
	Parameters
	----------
	point: Point object
		The point whose check is to be done
	
	boundary_edges: List of Line objects
		The lines that compose the perimeter
		
	Returns
	-------
	inside: Boolean
		Boolean of whether it is is on/inside or not
		
	Raises
	------
	None
	
	Notes
	-----
	Ray Tracing Algorithm is used. A ray is drawn towards the right.
	If the number of intersections with boundary are even then the point lies
	outside and otherwise inside for odd
	
	For on the boundary points, we can have a ray with x coordinate greater
	than or equal to the point one
	"""
	
	# Determine the line from which our ray is to be derived
	ray = Line()
	ray.line_from_orientation(0, point)
	
	# Loop over the edges and check with their intersection
	# Keeping the count of intersections
	intersection_count = 0
	
	for edge in boundary_edges:
		try:
			intersection = intersection_point(ray, edge)
			if(intersection.x >= point.x):
				intersection_count += 1
		except AssertionError:
			# This assertion error is due to the non parallel and collinear
			# nature of some lines
			pass
			
	if(intersection_count % 2 == 1):
		return True
	else:
		return False
		
def dot_product(point1, point2):
	"""
	Function to calculate the dot product of 2 vectors
	represented as points
	...
	
	Parameters
	----------
	point1: Point object
	
	point2: Point object
	
	Returns
	-------
	product: Float
		The dot product of the two vectors
		
	Raises
	------
	None
	
	Notes
	-----
	The dot product is calculated by multiplying individual
	x and y coordinates
	"""
	product = point1.x * point2.x + point1.y * point2.y
	
	return product
	
def euclidean_distance(point1, point2):
	""" Calculate the euler distance between two points """
	value = (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2
	mag = math.sqrt(value)
	
	return mag
				
	
	
	
	
