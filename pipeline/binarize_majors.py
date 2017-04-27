import pandas as pd

filename = 'Fixed_Sample_Students.csv'

info_df = pd.read_csv(filename)

info_df['is_pure'] = info_df.MajorCode.apply(lambda x: 1 if x == '540' else 0)

info_df['is_applied'] = info_df.MajorCode.apply(lambda x: 1 if x == '72' else 0)

info_df['is_mecon'] = info_df.MajorCode.apply(lambda x: 1 if x == '778' else 0)

info_df.to_csv('Fixed_Sample_Students_Major.csv')
