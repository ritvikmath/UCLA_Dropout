import pandas as pd
import numpy as np
import feature_helpers

"""
Add code for feature generation to this file
Example:
Suppose your new feature is called 'area' and you have specified in the yml file to include 'length' and 'width'
Then your function should look as follows:

def area_feature(df):
	return df.apply(lambda x: x.length * x.width, 1)	
"""

def alph_term_feature(df):
	return df.Term.apply(feature_helpers.get_sorted_term)

def running_gpa_feature(df):
	gr_list = []
	
	for i,row in df.iterrows():
		gr_list.append(np.mean(df[(df['ID'] == row.ID) & (df['alph_term'] < row.alph_term)]['grade']))
		
	return gr_list
		
def course_level_feature(df):
	return df.course.apply(feature_helpers.get_course_level)