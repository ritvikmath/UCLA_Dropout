import pandas as pd

def grad_status(id, last_qtr, graduated, curr_term, running_gpa):
	if graduated == 1:
		return 0
	elif last_qtr - curr_term <= 1 and running_gpa <= 2.0:
		return 1
	else:
		return 0

def attach_labels(df):
	
	dict_grad = {}
	
	gb_id = df.groupby('ID')
	
	for name,group in gb_id:
		dict_grad[name] = group.Term.max()
	
	df['drops_out_in_next_year'] = df.apply(lambda x: grad_status(x.ID, dict_grad[x.ID], x.Graduated, x.Term, x.rgpa_pure), axis = 'columns')
	
	df.to_csv('feature_table.csv')
	open('attach_labels.s', 'w+')