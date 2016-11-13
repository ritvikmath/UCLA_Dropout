import pandas as pd
import numpy as np
import hashlib
import os

def make_unique_key(df):
	"""
	input: dataframe with student data
	output: same dataframe now with a unique identifier for each row
	"""
	
	#apply hash so that we have unique identifier for each row 
	df['Key'] = df.apply(lambda x: hashlib.sha224(str(x.ID) + str(x.course) + str(x.Term)).hexdigest(), 1)
	df['shortKey'] = df.apply(lambda x: hashlib.sha224(str(x.ID) + str(x.Term)).hexdigest(), 1)
	
	df.to_csv('uniq_key_student_data.csv')
	
	

