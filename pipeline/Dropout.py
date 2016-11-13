import create_feature_table
import attach_labels
import evaluation
import pandas as pd
from create_unique_key import make_unique_key
import generate_predictions
import os

"""
This is the top level function which calls all others.
Note that the task this does right now is feature table generation
but that will change
"""

df = pd.read_csv('cleaned_student_data.csv')

#############CREATE UNIQUE KEY TABLE#############
if os.path.isfile('./uniq_key_student_data.csv'):
	print "Uniq Key Task Skipped"
	print "---------------"
else:
	print "Creating Unique Key Table"
	print "---------------"
	make_unique_key(df)

df = pd.read_csv('uniq_key_student_data.csv')
df.set_index('Key', inplace=True)
#################################################

#############CREATE FEATURE TABLE################
if (os.path.isfile('./feature_table.csv') == False) or (os.path.getmtime('./create_feature_table.yml') > os.path.getmtime('feature_table.csv')):
	print "Creating Feature Table"
	print "---------------"
	create_feature_table.create_feat_table(df)
else:
	print "Feature Table Task Skipped"
	print "---------------"
#################################################

#############CREATE FEATURE TABLE################
if (os.path.isfile('./attach_labels.s') == False) or (os.path.getmtime('./attach_labels.s') < os.path.getmtime('./create_feature_table.yml')):
	print "Attaching Labels"
	print "---------------"
	attach_labels.attach_labels(pd.read_csv('feature_table.csv'))
else:
	print "Label Attachment Task Skipped"
	print "---------------"
#################################################
	
#############CREATE MACHINE LEARNING OUTPUT######
if (os.path.isfile('./generate_predictions.s') == False) or (os.path.getmtime('./machine_learning.yml') > os.path.getmtime('./generate_predictions.s')):
	print "Running ML Models"
	print "---------------"
	generate_predictions.run_models()
else:
	print "Machine Learning Task Skipped"
	print "---------------"
#################################################

#############CREATE EVALUATION OUTPUT############
if (os.path.isfile('./model_scores.csv') == False) or (os.path.getmtime('./evaluation.yml') > os.path.getmtime('./model_scores.csv')):
	print "Running Model Evaluation"
	print "---------------"
	evaluation.eval_models()
else:
	print "Model Evaluation Task Skipped"
	print "---------------"
#################################################