import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.grid_search import ParameterGrid
import os

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
	
	X_train = train_df[feats_to_use]
	X_test = test_df[feats_to_use]
	
	y_train = train_df[prediction_var]
	y_test = test_df[prediction_var]
	
	clfs, grid = define_clfs_params()
	
	for n in range(1, 2):
		for index,clf in enumerate([clfs[x] for x in models_to_run]):
			parameter_values = grid[models_to_run[index]]
			for p in ParameterGrid(parameter_values):
				try:
					filename = models_to_run[index]+'-'+str(p).replace(' ','').strip('{}').replace('\'','').replace(',','-').replace(':','_')+'-'+'+'.join(feats_to_use)
					if os.path.isfile('../model_output/filename'+'.p'):
						continue
					print clf
					clf.set_params(**p)
					y_pred_probs = clf.fit(X_train, y_train).predict_proba(X_test)[:,1]
					result = pd.DataFrame()
					result['true_val'] = y_test
					result['score'] = y_pred_probs
					pickle.dump( result, open("../model_output/"+filename+".p", "wb" ))
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
	}

	grid = { 
	'RF':{'n_estimators': [10,100], 'max_depth': [10,20], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5]},
	'LR': { 'penalty': ['l1','l2'], 'C': [.01,.1,1,10]},
	}
	
	return clfs, grid
	
if __name__ == "__main__":
    run_models()