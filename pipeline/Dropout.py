import create_feature_table
import attach_labels
import evaluation
import pandas as pd
from create_unique_key import make_unique_key
import generate_predictions
import os

"""
This is the top level function which calls all others.
"""

proceed = False

df = pd.read_csv('cleaned_student_data.csv')

#############CREATE UNIQUE KEY TABLE#############
if (proceed == True) or (not os.path.isfile('./uniq_key_student_data.csv')):
	print "---------------"
	print "Creating Unique Key Table"
	print "---------------"
	make_unique_key(df)
	proceed = True
else:
	print "---------------"
	print "Uniq Key Task Skipped"
	print "---------------"
	
df = pd.read_csv('uniq_key_student_data.csv')
df.set_index('Key', inplace=True)
#################################################

#############CREATE FEATURE TABLE################
if (proceed == True) or (os.path.isfile('./feature_table.csv') == False) or (os.path.getmtime('./create_feature_table.yml') > os.path.getmtime('feature_table.csv')):
	print "Creating Feature Table"
	print "---------------"
	create_feature_table.create_feat_table(df)
	proceed = True
else:
	print "Feature Table Task Skipped"
	print "---------------"
#################################################

#############CREATE LABELED FEATURE TABLE################
if (proceed == True) or (os.path.isfile('./attach_labels.s') == False) or (os.path.getmtime('./attach_labels.s') < os.path.getmtime('./create_feature_table.yml')):
	print "Attaching Labels"
	print "---------------"
	attach_labels.attach_labels(pd.read_csv('feature_table.csv'))
	proceed = True
else:
	print "Label Attachment Task Skipped"
	print "---------------"
#################################################
	
#############CREATE MACHINE LEARNING OUTPUT######
if (proceed == True) or (os.path.isfile('./generate_predictions.s') == False) or (os.path.getmtime('./machine_learning.yml') > os.path.getmtime('./generate_predictions.s')):
	print "Running ML Models"
	print "---------------"
	generate_predictions.run_models()
	proceed = True
else:
	print "Machine Learning Task Skipped"
	print "---------------"
#################################################

#############CREATE EVALUATION OUTPUT############
if (proceed == True) or (os.path.isfile('./model_scores.csv') == False) or (os.path.getmtime('./evaluation.yml') > os.path.getmtime('./model_scores.csv')):
	print "---------------"
	print "Running Model Evaluation"
	print "---------------"
	evaluation.eval_models()
else:
	print "Model Evaluation Task Skipped"
	print "---------------"
#################################################