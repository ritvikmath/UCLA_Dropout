import pandas as pd

print "Reading Data Files ..."
df_enroll = pd.read_csv('dbo_tbl_Enroll_Cleaned.csv')
df_keyfile = pd.read_csv('dbo_tbl_KeyFileArchive_Cleaned.csv')
df_registration = pd.read_csv('dbo_tbl_Registration_Cleaned.csv')
df_exams = pd.read_csv('dbo_tbl_Scores_SAT_ACT_Cleaned.csv')
df_graduation = pd.read_csv('Graduation_Cleaned.csv')

df_enroll.rename(index=str, columns={'term':'Term'}, inplace=True)

print "Joining Keyfile"
temp_df = pd.merge(df_enroll, df_keyfile, on=['Hash', 'Term'], how='left')
print "Joining Registration"
temp_df = pd.merge(temp_df, df_registration, on=['Hash', 'Term'], how='left')
print "Joining Exams"
temp_df = pd.merge(temp_df, df_exams, on='Hash', how='left')
print "Joining Graduation"
temp_df = pd.merge(temp_df, df_graduation, on='Hash', how='left')

print "Outputing to CSV"
temp_df.to_csv('joined_table.csv', index=False)

