import pandas as pd

"""
This file contains helper functions for the feature computation
functions in feature_computation.py
"""

def get_sorted_term(term):
	n = term[:2]
	t = term.strip('0123456789')
	if t == 'W':
		return n+'A'
	elif t == 'S':
		return n+'B'
	elif t == 'F':
		return n+'D'
	return n+'C'
	
def get_course_level(course):
	num = int(course.strip(' ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
	if num < 100:
		return 'LD'
	elif num < 200:
		return 'UD'
	return 'GR'