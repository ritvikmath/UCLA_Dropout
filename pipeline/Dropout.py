import create_feature_table
import pandas as pd
from create_unique_key import make_unique_key

"""
This is the top level function which calls all others.
Note that the task this does right now is feature table generation
but that will change
"""

df = pd.read_csv('cleaned_student_data.csv')
	
make_unique_key(df)

df = pd.read_csv('uniq_key_student_data.csv')
df.set_index('Key', inplace=True)

create_feature_table.create_feat_table(df)