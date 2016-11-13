import pandas as pd

def attach_labels(df):
	grad_data = pd.read_csv('extra_data.csv')
	grad_ids = set(grad_data.UIDHASH)
	df['graduation_status'] = df.ID.apply(lambda x: int(x in grad_ids))
	df.to_csv('feature_table.csv')
	open('attach_labels.s', 'w+')
	