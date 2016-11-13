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
				
	filenames = []
	scores = []
	p_at_k = []
	r_at_k = []
	
	cost_mtx = {'[1, 1]': true_pos_reward, '[0, 0]': true_neg_reward, '[1, 0]': false_pos_penalty, '[0, 1]': false_neg_penalty}
	
	for fn in os.listdir('../model_output/'):
		print fn
		filenames.append(fn)
		result_df = pickle.load(open('../model_output/'+fn, "rb"))
		thresh = np.percentile(result_df.score, 100-k)
		
		result_df['pred_val'] = result_df.score.apply(lambda x: 1 if x > thresh else 0)
		result_df['contribution'] = result_df.apply(lambda x: cost_mtx[str([int(x.pred_val), int(x.true_val)])], axis = 'columns')
		result_df['correct'] = result_df.apply(lambda x: int(x.pred_val == x.true_val), axis = 'columns')
		tot_score = result_df.contribution.mean()
		scores.append(tot_score)
		
		p_at_k.append(result_df.correct.sum()/float(len(result_df)))
		ones_df = result_df[result_df.true_val == 1]
		r_at_k.append(ones_df.correct.sum()/float(len(ones_df)))
		
		
	df = pd.DataFrame()
	df['model'] = filenames
	df['score'] = scores
	df['recall_at_'+str(k)] = r_at_k
	df['precision_at_'+str(k)] = p_at_k
	df.to_csv('model_scores.csv')
	
		