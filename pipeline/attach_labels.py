import pandas as pd

def grad_status(id, last_qtr, grad_ids, curr_term):
	if id in grad_ids:
		return 0
	elif last_qtr - curr_term <= 1:
		return 1
	else:
		return 0

def attach_labels(df):
	grad_data = pd.read_csv('extra_data.csv')
	grad_ids = set(grad_data.UIDHASH)
	
	dict_grad = {}
	
	
	gb_id = df.groupby('ID')
	
	for name,group in gb_id:
		dict_grad[name] = group.alph_term.max()
	
	df['drops_out_in_next_year'] = df.apply(lambda x: grad_status(x.ID, dict_grad[x.ID], grad_ids, x.alph_term), axis = 'columns')
	df.to_csv('feature_table.csv')
	open('attach_labels.s', 'w+')