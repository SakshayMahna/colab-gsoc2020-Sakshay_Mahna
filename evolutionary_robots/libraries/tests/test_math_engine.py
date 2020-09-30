# This part is specific to each user, not recommended to be copied
import sys
sys.path.append('./../')

# Tests for Math Engine

from genetic_engine.math_engine import point, line, algorithms 
from genetic_engine import sensor
import math
import unittest

# Unit Test Activation Class
class TestMathEngine(unittest.TestCase):
	def setUp(self):
		self.point1 = point.Point()
		self.point2 = point.Point()
		self.point3 = point.Point()
		self.point4 = point.Point()
		self.line1 = line.Line()
		self.line2 = line.Line()
		self.line3 = line.Line()
		self.line4 = line.Line()
		
		self.sensor = sensor.Sensor(math.pi / 4)
	
	def test_intersection_orientation(self):
		self.point1.x = 1; self.point1.y = 2
		self.point2.x = 1; self.point2.y = 1
		
		self.line1.line_from_orientation(-math.pi/4, self.point1)
		self.line2.line_from_orientation(math.pi/4, self.point2)
		
		point = algorithms.intersection_point(self.line1, self.line2)
		
		self.assertEqual(round(point.x, 1), 1.5)
		self.assertEqual(round(point.y, 1), 1.5)
		
	def test_intersection_points(self):
		self.point1.x = -2; self.point1.y = 2
		self.point2.x = 2; self.point2.y = -2
		self.line1.line_from_points(self.point1, self.point2)
		
		self.point1.x = 2; self.point1.y = 2
		self.point2.x = -2; self.point2.y = -2
		self.line2.line_from_points(self.point1, self.point2)
		
		point = algorithms.intersection_point(self.line1, self.line2)
		
		self.assertEqual(point.x, 0)
		self.assertEqual(point.y, 0)
	
	def test_point_inside_perimeter(self):
		self.point1.x = 0; self.point1.y = 1
		self.point2.x = -1; self.point2.y = 0
		self.point3.x = 1; self.point3.y = 0
		
		point_inside = point.Point()
		point_outside = point.Point(-2, 0)
		
		self.line1.line_from_points(self.point1, self.point2)
		self.line2.line_from_points(self.point2, self.point3)
		self.line3.line_from_points(self.point3, self.point1)
		
		inside = algorithms.point_inside_perimeter(point_inside, [self.line1, self.line2, self.line3])
		outside = algorithms.point_inside_perimeter(point_outside, [self.line1, self.line2, self.line3])
		
		self.assertEqual(inside, True)
		self.assertEqual(outside, False)
		
	def test_sensor(self):
		self.point1.x = -10; self.point1.y = 10
		self.point2.x = 10; self.point2.y = 10
		self.point3.x = 10; self.point3.y = -10
		self.point4.x = -10; self.point4.y = -10
		
		self.line1.line_from_points(self.point1, self.point2)
		self.line2.line_from_points(self.point2, self.point3)
		self.line3.line_from_points(self.point3, self.point4)
		self.line4.line_from_points(self.point4, self.point1)
		
		value = self.sensor.read(point.Point(1, 2), math.pi / 2, 
				[self.line1, self.line2, self.line3, self.line4])
				
		self.assertEqual(round(value.x, 0), -7)
		self.assertEqual(value.y, 10)
	
if __name__ == "__main__":
	unittest.main()



