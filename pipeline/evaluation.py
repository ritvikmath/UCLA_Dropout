import pandas as pd
import os
import yaml
import numpy as np
import pickle

def eval_models():

	stream = open("evaluation.yml", 'r')
	docs = yaml.load_all(stream)
	for doc in docs:
		for key,v in doc.items():
			if key == 'k':
				k = v
			elif key == 'true_pos_reward':
				true_pos_reward = v
			elif key == 'true_neg_reward':
				true_neg_reward = v
			elif key == 'false_pos_penalty':
				false_pos_penalty = v
			elif key == 'false_neg_penalty':
				false_neg_penalty = v
				
	if os.path.isfile('./model_scores.csv'):
		model_scores_df = pd.read_csv('./model_scores.csv')
		for col in model_scores_df.columns:
			if 'Unnamed' in col:
				model_scores_df = model_scores_df.drop(col, 1)
	else:
		model_scores_df = pd.DataFrame(columns = ['model','score','recall_at_'+str(k),'precision_at_'+str(k)])
				
	filenames = []
	scores = []
	p_at_k = []
	r_at_k = []
	
	cost_mtx = {'[1, 1]': true_pos_reward, '[0, 0]': true_neg_reward, '[1, 0]': false_pos_penalty, '[0, 1]': false_neg_penalty}
	
	for fn in os.listdir('../model_output/'):
		if (os.path.isfile('../model_output/tracker.s') == False) or (os.path.isfile('../model_output/tracker.s') == True and os.path.getmtime('../model_output/'+fn) > os.path.getmtime('../model_output/tracker.s')):
			print fn
			filenames.append(fn)
			result_df = pickle.load(open('../model_output/'+fn, "rb"))
			thresh = np.percentile(result_df.score, 100-k)
			
			result_df['pred_val'] = result_df.score.apply(lambda x: 1 if x > thresh else 0)
			result_df['contribution'] = result_df.apply(lambda x: cost_mtx[str([int(x.pred_val), int(x.true_val)])], axis = 'columns')
			result_df['correct'] = result_df.apply(lambda x: int(x.pred_val == x.true_val), axis = 'columns')
			tot_score = result_df.contribution.mean()
			
			ones_df = result_df[result_df.true_val == 1]
			
			temp_df = pd.DataFrame(columns = ['model','score','recall_at_'+str(k),'precision_at_'+str(k)])
			temp_df.model = [fn]
			temp_df.score = [tot_score]
			temp_df['precision_at_'+str(k)] = [result_df.correct.sum()/float(len(result_df))]
			temp_df['recall_at_'+str(k)] = [ones_df.correct.sum()/float(len(ones_df))]
			
			model_scores_df = model_scores_df.append(temp_df, ignore_index = True)
			model_scores_df.to_csv('model_scores.csv')
			
	if os.path.isfile('../model_output/tracker.s') == False:
		open('../model_output/tracker.s', 'w+')
	else:
		os.utime('../model_output/tracker.s', None)
	
	
	
		