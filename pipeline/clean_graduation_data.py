import pandas as pd 
import numpy as np


############################################################
##                    Graduation Data
##
############################################################

print "Cleaning Graduation Data ..."

df_grad = pd.read_excel("Graduation.xlsx")
print list(df_grad.columns.values)
columns_to_keep = ['Hash', 'Major']

df_grad2 = df_grad[columns_to_keep]
graduated_students = df_grad['Hash'].values.tolist()
listOfOnes = [1] * len(graduated_students)

df_grad2['Graduated'] = listOfOnes

df_grad2.to_csv('Graduation_Cleaned.csv', index=False)
df_grad = pd.read_csv("Graduation_Cleaned.csv")
print "Getting Graduation data..."
print df_grad.head()

# #############################################################################
# #					   Transfer Credit
# #			GET RID 
# ###############################################################################################
# print "Cleaning Transfer Data ..."

# df_transfer = pd.read_excel("dbo_tbl_TransferCredit (rev cj).xlsx")
# print list(df_transfer.columns.values)
# columns_to_keep = ['Hash', 'TRF_CRED_CRS_TTL', 'SUBJ_AREA_CD', 'DISP_CATLG_NO']

# df_transfer2 = df_transfer[columns_to_keep]
# df_transfer2.to_csv('dbo_tbl_TransferCredit_Cleaned.csv', index=False)

# df_transfer_csv = pd.read_csv('dbo_tbl_TransferCredit_Cleaned.csv')
# IDs = list(set(df_transfer_csv['Hash'].values.tolist()))
# transfer_courses = []

# for index, student in enumerate(IDs):
# 	subset_df = df_transfer_csv[df_transfer_csv['Hash'] == student]
# 	lst = zip(subset_df['TRF_CRED_CRS_TTL'], subset_df['SUBJ_AREA_CD'], subset_df['DISP_CATLG_NO'])
# 	transfer_courses.append(lst)

# final_transfer_df = pd.DataFrame(np.column_stack([IDs, transfer_courses]), columns = ['Hash', 'TransferCourses'])
# final_transfer_df.to_csv('dbo_tbl_TransferCredit_Cleaned.csv', index = False)


###################################################################################################
#					   SAT ACT
#
#############################################################

print "Cleaning SAT ACT Data ..."

df_SATACT = pd.read_excel('dbo_tbl_Scores_SAT_ACT (rev cj).xlsx')
print list(df_SATACT.columns.values)
columns_to_keep = ['Hash', 'SR_TEST_SUBJ_DESC', 'TEST_SCORE_1', 'TEST_SCORE_2', 'TEST_SCORE_3']
df_SATACT.head()
df_SATACT2 = df_SATACT[columns_to_keep]
df_SATACT2['full_score'] = df_SATACT2.apply(lambda x: (x.SR_TEST_SUBJ_DESC, [i for i in [x.TEST_SCORE_1, x.TEST_SCORE_2, x.TEST_SCORE_3] if str(i) != 'nan']), 1)

reduced_df = df_SATACT2.groupby('Hash').full_score.apply(list)
reduced_df = reduced_df.to_frame()
reduced_df.reset_index(inplace=True)
reduced_df.to_csv('dbo_tbl_Scores_SAT_ACT_Cleaned.csv', index=False)

df_SAT = pd.read_csv("dbo_tbl_Scores_SAT_ACT_Cleaned.csv")
print "Getting SAT data..."
print df_SAT.head()


#############################################################
#					   Enrollment Data
#
#############################################################

print "Cleaning Enrollment Data ..."

df_enroll = pd.read_excel("dbo_tbl_Enroll (rev cj).xlsx")
print list(df_enroll.columns.values)
df_enroll = df_enroll[df_enroll.section.apply(lambda x: not x[-1].isalpha())]
enroll_cols_to_drop = ['section', 'srs']
df_enroll = df_enroll.drop(enroll_cols_to_drop, 1)
df_enroll.to_csv('dbo_tbl_Enroll_Cleaned.csv', index=False)

df_enroll = pd.read_csv("dbo_tbl_Enroll_Cleaned.csv")
print "Getting Enrollment data..."
print df_enroll.head()

#############################################################
#					   Keyfile Data
#
#############################################################

print "Cleaning Keyfile Data ..."

df_keyfile = pd.read_excel("dbo_tbl_KeyFileArchive (rev cj).xlsx")
print list(df_keyfile.columns.values)
keyfile_cols_to_drop = ['Ferpa', 'DirectRestrict', 'AsAdmit', 'AlumRel', 'EthRel' , 'AdmitCollege', 'ReadTerm','AAP', 'HonorsFlg','Athlete', 'TermAdvanced', 'Deg1', 'Deg2']
df_keyfile = df_keyfile.drop(keyfile_cols_to_drop, 1)
df_keyfile.to_csv('dbo_tbl_KeyFileArchive_Cleaned.csv', index=False)

df_keyfile = pd.read_csv("dbo_tbl_KeyFileArchive_Cleaned.csv")
print "Getting KeyFile data..."
print df_keyfile.head()

#############################################################
#					   Registration Data
#
#############################################################

print "Cleaning Registration Data ..."

df_registration = pd.read_excel("dbo_tbl_Registration (rev cj).xlsx")
print list(df_registration.columns.values)
registration_cols_to_keep = ['Hash', 'Term', 'MajorCode', 'Classification', 'LOATerm']
# registration_cols_to_drop = ['RegStatus','WithdrawlCode','Joint','MinProgress']
# df_registration = df_registration.drop(registration_cols_to_drop, 1)
df_registration = df_registration[registration_cols_to_keep]
df_registration.to_csv('dbo_tbl_Registration_Cleaned.csv', index=False)

df_registration = pd.read_csv("dbo_tbl_Registration_Cleaned.csv")
print "Getting Registration data..."
print df_registration.head()

# ['Term', 'subject', 'course', 'OfficialGrade', 'Hash', 'Gender', 'AdmitTerm', 'EthnicityCode', 'AdmitCollege', 
# 'AdmitMajor', 'AdmitClass','HighSchool', 'LastSchool', 'DegreeExp', 'GPA', 'UnitsTotal',
# 'LastTerm', 'MajorCode', 'Degree1','Classification', 'GradePoints', 'DegSpec', 
# 'LOATerm','ResTuit', 'full_score','Overall GPA', 'Graduated']