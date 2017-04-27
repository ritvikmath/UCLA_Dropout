import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

import pickle
from sklearn.grid_search import ParameterGrid
import os

def binarize_categorical_vars(df, cat_vars):
	new_feats = []
	for var in cat_vars:
		df_temp = pd.get_dummies(df[var], prefix = var+'_is')
		df = pd.concat([df, df_temp], axis=1)
		new_feats+=list(df_temp.columns)
		if var != 'alph_term':
			df = df.drop(var, 1)
	return [df, new_feats]

def run_models():
	stream = open("machine_learning.yml", 'r')
	docs = yaml.load_all(stream)
	for doc in docs:
		for k,v in doc.items():
			if k == 'train_start_year':
				train_start_year = v
			elif k == 'num_train_years':
				num_train_years = v
			elif k == 'num_test_years':
				num_test_years = v
			elif k == 'models_to_run':
				models_to_run = v.split()
			elif k == 'prediction_var':
				prediction_var = v
			elif k == 'feats_to_use':
				feats_to_use = v.replace(',','').split(' ')
			elif k == 'feat_tbl_name':
				feat_tbl_name = v
			elif k == 'date_col':
				date_col = v
			elif k == 'train_tbl_name':
				train_tbl_name = v
			elif k == 'test_tbl_name':
				test_tbl_name = v
	
	gen_train_test_split(feat_tbl_name, train_start_year, num_train_years, num_test_years, date_col, train_tbl_name, test_tbl_name)
	
	train_df = pd.read_csv(train_tbl_name)
	test_df = pd.read_csv(test_tbl_name)
	
	feats = []
	cat_status = []
	
	stream = open("create_feature_table.yml", 'r')
	docs = yaml.load_all(stream)
	for doc in docs:
		for k,v in doc.items():
			if k == 'name':
				feats.append(v)
			if k == 'type': 
				if v == 'cat':
					cat_status.append(1)
				else:
					cat_status.append(0)
			
	cat_feats = [i[0] for i in zip(feats, cat_status) if i[1] == 1]
	
	full_feats = []
	for feat in feats_to_use:
		for col in train_df.columns:
			if feat in col:
				full_feats.append(col)
	full_feats = list(set(full_feats))
	
	feats_to_binarize = [i for i in cat_feats if i in full_feats]
	train_df = binarize_categorical_vars(train_df, feats_to_binarize)[0]
	test_tup = binarize_categorical_vars(test_df, feats_to_binarize)
	test_df = test_tup[0]
	new_feats = test_tup[1]
	full_feats += new_feats
	
	for feat in feats_to_binarize:
		full_feats.remove(feat)
	
	
	X_train = train_df[full_feats]
	X_test = test_df[full_feats]
	
	y_train = train_df[prediction_var]
	y_test = test_df[prediction_var]
	
	clfs, grid = define_clfs_params()
	
	for n in range(1, 2):
		for index,clf in enumerate([clfs[x] for x in models_to_run]):
			parameter_values = grid[models_to_run[index]]
			for p in ParameterGrid(parameter_values):
				try:
					filename = models_to_run[index]+'-'+str(p).replace(' ','').strip('{}').replace('\'','').replace(',','-').replace(':','_')+'-'+'+'.join(feats_to_use)
					if os.path.isfile("../model_output/"+filename+".p"):
						continue
					print clf
					clf.set_params(**p)
					y_pred_probs = clf.fit(X_train, y_train).predict_proba(X_test)[:,1]
					try:
						zipped_imps = sorted(zip(X_train.columns,clf.feature_importances_), key = lambda x:x[1])
						top_3_feats = [i[0] for i in zipped_imps[:3]]
					except AttributeError:
						top_3_feats = ['NA']
					print "---------------"
					result = pd.DataFrame()
					result['true_val'] = y_test
					result['score'] = y_pred_probs
					pickle.dump( [result, top_3_feats], open("../model_output/"+filename+".p", "wb" ))
				except IndexError, e:
					print 'Error:',e
					continue
					
	open('generate_predictions.s', 'w+')
	
	
def gen_train_test_split(feat_tbl_name, train_start_year, num_train_years, num_test_years, date_col, train_tbl_name, test_tbl_name):
	feat_tbl = pd.read_csv(feat_tbl_name)
	train_tbl = feat_tbl[feat_tbl[date_col] <= train_start_year + num_train_years - 0.5 - 2000]
	test_tbl = feat_tbl[(feat_tbl[date_col] > train_start_year + num_train_years - 0.5 - 2000)&(feat_tbl[date_col] <= train_start_year + num_train_years +num_test_years - 0.5 - 2000)]
	train_tbl.to_csv(train_tbl_name)
	test_tbl.to_csv(test_tbl_name)
	
def define_clfs_params():

	clfs = {
		'RF': RandomForestClassifier(n_estimators=50, n_jobs=-1),
		'LR': LogisticRegression(penalty='l1', C=1e5),
        'GB': GradientBoostingClassifier(learning_rate=0.05, subsample=0.5, max_depth=6, n_estimators=10),
		'ET': ExtraTreesClassifier(n_estimators=10, n_jobs=-1, criterion='entropy'),
		'KNN': KNeighborsClassifier(n_neighbors=3),
		'AB': AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), algorithm="SAMME", n_estimators=200)
		
	}

	grid = { 
	'RF':{'n_estimators': [10,100,1000], 'max_depth': [2,5], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5,10]},
	'LR': { 'penalty': ['l1','l2'], 'C': [.1,1,10]},
	'GB': {'n_estimators': [10,100], 'learning_rate' : [0.01,0.05],'subsample' : [0.1,0.5], 'max_depth': [10,50]},
	'ET': { 'n_estimators': [10,100], 'criterion' : ['gini', 'entropy'] ,'max_depth': [10,20,50, 100], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5,10]},
	'KNN' :{'n_neighbors': [50,100,200],'weights': ['uniform','distance'],'algorithm': ['auto','ball_tree','kd_tree']},
	'AB': { 'algorithm': ['SAMME','SAMME.R'], 'n_estimators': [1,10,100,1000,10000]}
	}
	
	return clfs, grid
	
if __name__ == "__main__":
    run_models()