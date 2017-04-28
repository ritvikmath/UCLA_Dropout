import pandas as pd
import numpy as np

full_df = pd.read_csv('joined_table.csv')

def term2float(s):
    year = s[:-1]
    qtr = s[-1]
    if qtr == 'W':
        fpart=0.00
    elif qtr=='S':
        fpart=0.25
    elif qtr=='1':
        fpart=0.5
    else:
        fpart=0.75
    return int(year)+fpart
	
def grade2float(s):
    grade_dict = {'A': 4, 'B': 3, 'C':2, 'D':1, 'F':0, '+': .3, '-':-.3}
    tot = 0
    for l in s:
        if l in grade_dict.keys():
            tot+=grade_dict[l]
        else:
            return -1
    return min(4, tot)
    
full_df.Term = full_df.Term.apply(term2float)

full_df.course = full_df.course.apply(lambda x: x.lstrip('0'))

full_df.AdmitMajor = full_df.AdmitMajor.apply(lambda x: str(x).lstrip('0'))

full_df.HighSchool = full_df.HighSchool.apply(lambda x: int(x) if str(x)!='nan' else x)
full_df.LastSchool = full_df.LastSchool.apply(lambda x: int(x) if str(x)!='nan' else x)
full_df.ChangeSchool = full_df.ChangeSchool.apply(lambda x: int(x) if str(x)!='nan' else x)

full_df.DegreeExp = full_df.DegreeExp.apply(lambda x: term2float(x) if str(x)!='nan' else x)

full_df.OfficialGrade = full_df.OfficialGrade.apply(lambda x: grade2float(x) if str(x)!='nan' else -1)
full_df = full_df[full_df.OfficialGrade != -1]

full_df.rename(index=str, columns={'Hash':'ID', 'OfficialGrade':'grade'}, inplace=True)
full_df = full_df[full_df.course.apply(lambda x: x.strip(' ABCDEFGHIJKLMNOPQRSTUVWXYZ') != '')]

full_df.Graduated = full_df.Graduated.apply(lambda x: 0 if str(x)=='nan' else x)

acceptable_majors = ['72', '6Q', '8D', '8E', '540', '737', 'G', '6P', '536', '6R', '545', '6S', '54B', '778', '6T']
acceptable_admits = ['UFR', 'USO']
full_df = full_df[full_df.AdmitMajor.isin(acceptable_majors)]
full_df = full_df[full_df.AdmitClass.isin(acceptable_admits)]



full_df.to_csv('cleaned_joined_table.csv')

full_df.to_csv('../UCLA_Dropout/pipeline/cleaned_joined_table.csv')