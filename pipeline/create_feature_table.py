import pandas as pd
import numpy as np
import yaml
import copy
import datetime

import feature_computation

def get_feats_to_compute(df):
	"""
	input: dataframe of cleaned student data
	output: zipped list with each item being a double. 
			The first element of each double is the feature name 
			The second element of each double is the dependencies for this feature
	"""

	#contains list of features in yml file
	feature_list = {}
	
	#include only those with incl:True flag set
	to_add = []
	
	#collect the features which are dimensionally reduced
	not_in_final_feats = []
	
	#collect the categorical vars for binarizaiton 
	cat_vars = []

	#features native to the dataframe
	generated_feats = [i for i in df.columns]
	
	#this tells us which order to compute features in
	queue = copy.copy(generated_feats)

	#read the yml file
	stream = open("create_feature_table.yml", 'r')
	docs = yaml.load_all(stream)
	for doc in docs:
		feature_list[doc['name']] = {}
		for k,v in doc.items():
			if k == 'name':
				continue;
			#store all feature information (dependencies, include or not) in dictionary
			elif k == 'deps':
				feature_list[doc['name']][k] = v.replace(' ','').split(',')
			elif k == 'coll':
				feature_list[doc['name']][k] = v
			elif k == 'type':
				feature_list[doc['name']][k] = v
			else:
				feature_list[doc['name']][k] = v
	#get features to add
	for k,v in feature_list.items():
		if v['incl'] == True:
			to_add.append(k)
			if v['coll'] == False:
				not_in_final_feats.append(k)
			else:
				cat_vars.append(k)
			
	#keep looping as long as we have not accounted for all features
	tgt_len = len(queue) + len(to_add)		
	while len(queue) != tgt_len:
		to_rem = []
		for feat in to_add:
			#if we get a feature to add, add it to the queue and mark it for removal from the to_add list
			if len([i for i in feature_list[feat]['deps'] if i in queue]) == len([i for i in feature_list[feat]['deps']]):
				queue.append(feat)
				to_rem.append(feat)
		#remove features in the to_rem list
		for feat in to_rem:
				to_add.remove(feat)
	#get features which we need to compute (not those native to the dataframe)		
	feats_to_compute = [i for i in queue if i not in generated_feats]
	#get the dependencies
	deps_to_apply = [feature_list[i]['deps'] for i in feats_to_compute]

	#return zipped list
	return [zip(feats_to_compute, deps_to_apply), not_in_final_feats, cat_vars]

def create_feat_table(df):
	"""
	input: dataframe of student data
	output: a csv containing the feature table
	"""

	#get features to generate and their dependencies
	r_val = get_feats_to_compute(df)
	feats_deps = r_val[0]

	
	timing = []
	feats = []
	
	#for each feature
	for feat_dep in feats_deps:
		#get the appropriate generation function
		print "Adding ", feat_dep[0], " feature ... "
		bef = datetime.datetime.now()
		func = getattr(feature_computation, feat_dep[0]+'_feature')
		#apply that function and add the resulting column to the dataframe
		df[feat_dep[0]] = func(df[feat_dep[1]])
		aft = datetime.datetime.now()
		timing.append(float((aft-bef).microseconds))
		feats.append(feat_dep[0])
	
	tot_time = sum(timing)
	pct_times = [i/tot_time*100 for i in timing]
	
	df_timing = pd.DataFrame()
	df_timing['Feature'] = feats
	df_timing['Pct Computation Time'] = pct_times
	print "---------------"
	print df_timing
	print "---------------"
	
	toRemove = r_val[1]
	cat_vars = r_val[2]
	toRemove+=['course','subject','grade']
	df = create_reduced_feature_table(df, 'shortKey', toRemove)
	#generate feature table
	df.to_csv('feature_table.csv')
	
def create_reduced_feature_table(df, reduceOn, removeLabels):
	for item in df.columns:
		if 'Unnamed' in item:
			removeLabels.append(item)
			
	df_reduce = df.groupby(reduceOn).first()
	df_reduce = df_reduce.drop(removeLabels,1)
	
	return df_reduce

		
		
		
	
	
	
