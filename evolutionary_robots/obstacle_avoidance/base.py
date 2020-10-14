#!/usr/bin/python
#-*- coding: utf-8 -*-
import threading
import time
import sys
import os
import glob
from datetime import datetime

import math
import cv2
import numpy as np
import rospy
from std_srvs.srv import Empty

import MyAlgorithm as algorithm

sys.path.append('./../libraries')
from genetic_algorithm.ga_simulation import GeneticAlgorithmGazebo

time_cycle = 80

class MyAlgorithm(threading.Thread):
    def __init__(self, sensor, motors):
        # Initializing the Algorithm object
        self.sensor = sensor
        self.motors = motors
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_sensor_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
        
        self.log_folder = algorithm.LOG_FOLDER
        self.get_latest_file()
        
        self.reset_simulation = rospy.ServiceProxy("gazebo/reset_simulation", Empty)
        
    def get_latest_file(self):
        files = glob.glob(self.log_folder + '/generation*[0-9].txt')
        files = sorted(files, key = lambda x: (len(x), x))
        
        try:
            self.latest_generation = int(files[-1][(len(self.log_folder) + 11):-4])
        except IndexError:
            self.latest_generation = 0
    	
    def select_individual(self):
    	# Define the Genetic Algorithm
		neural_network = algorithm.define_neural_network()
		self.genetic_algorithm = GeneticAlgorithmGazebo(neural_network)

		test_number = int(self.run_state)
    	
		try:
			test_population = self.genetic_algorithm.load_chromosome(self.log_folder + "/best_chromosomes")
			if(test_number != 0):
				test_individual = test_population[test_number]
			else:
				test_individual = test_population
		except IOError:
			print("File not found!")
			
		self.genetic_algorithm.test_network = test_individual
		self.reset_simulation()
    
    def getRange(self):
        self.lock.acquire()
        values = self.sensor.data.values
        self.lock.release()
        return values

    def run (self):
        self.select_individual()
    		
    	while(not self.kill_event.is_set()):
    		start_time = datetime.now()
    		
    		if(not self.stop_event.is_set()):
    			self.algorithm()
    			
    		finish_time = datetime.now()
    		
    		dt = finish_time - start_time
    		ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    		
    		if(ms < time_cycle):
    		    time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        output = self.genetic_algorithm.test_output({"INFRARED": self.getRange()})["MOTORS"]
        output = output / 2
        self.motors.sendV(4 * (output[0] + output[1]))
        self.motors.sendW(4 * (output[0] - output[1]))
    		
        
