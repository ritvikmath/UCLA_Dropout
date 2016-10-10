import pandas as pd

"""
This file contains helper functions for the feature computation
functions in feature_computation.py
"""

def get_sortable_term(term):
	n = term[:2]
	t = term.strip('0123456789')
	if t == 'W':
		return n+'.0'
	elif t == 'S':
		return n+'.25'
	elif t == 'F':
		return n+'.75'
	return n+'.5'
	
def get_course_level(course):
	num = int(course.strip(' ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
	if num < 100:
		return 'LD'
	elif num < 200:
		return 'UD'
	return 'GR'

def get_math_units(f):
	if f['course'] == "115A":
		return 5
	if f['subject'] == "COMPTNG":
		return 5
	return 4