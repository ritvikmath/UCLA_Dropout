import pandas as pd

"""
This file contains helper functions for the feature computation
functions in feature_computation.py
"""

def get_sortable_term(term):
	n = term[:2]
	t = term.strip('0123456789')
	if t == 'W':
		return float(n+'.0')
	elif t == 'S':
		return float(n+'.25')
	elif t == 'F':
		return float(n+'.75')
	return float(n+'.5')
	
def get_course_level(course):
	num = int(course.strip(' ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
	if num < 100:
		return 'LD'
	elif num < 200:
		return 'UD'
	return 'GR'

def get_math_units(row):
	if row['course'] == "115A":
		return 5
	if row['subject'] == "COMPTNG":
		return 5
	return 4

def get_boolean_A_plus(grade):
	if float(grade) == 4.3:
		return 1
	return 0

def get_boolean_female(gender):
	if str(gender) == 'F':
		return 1
	return 0 

def get_boolean_male(gender):
	if str(gender) == 'M':
		return 1
	return 0 

def get_actual_grade(grade):
	if float(grade) == 4.3:
		return 4
	return grade 

def get_term_list(df, row):
	student_ID = row.ID
		
	student_df = df[df['ID'] == student_ID]
	term_list = [float(x) for x in student_df['alph_term'].values.tolist()]

	return term_list 

def get_terms_and_grades_dictionary(df, row, term_list):
	student_ID = row.ID
	student_df = df[df['ID'] == student_ID]

	return dict(zip(term_list, zip(student_df['actual_grade'].values.tolist(), student_df['math_units'].values.tolist()) ))

def get_start_and_most_recent_term(stop_term, term_list):
	start_term = float(min(term_list))

	most_recent_term = 0 
	for index, value in enumerate(term_list):
		if value > most_recent_term and value < stop_term:
			most_recent_term = value

	return start_term, most_recent_term 

def get_unit_sum_and_grades_times_units(most_recent_term, start_term, term_and_grade, term_list):
	unit_sum = 0
	grade_sum = 0
	grade_times_units = 0

	term = most_recent_term

	while term >= start_term:
		if term in term_list: 
			unit_sum += float(term_and_grade[term][1])
			grade_sum += term_and_grade[term][0]
			grade_times_units += (float(term_and_grade[term][1]) * term_and_grade[term][0]) 
		term -= 0.25

	return unit_sum, grade_times_units

def get_average_previous_gpa(unit_sum, grades_times_units):
	if unit_sum > 0:
		average_previous_gpa = (grades_times_units/unit_sum)
	else: 
		average_previous_gpa = 0

	return average_previous_gpa


