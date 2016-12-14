import pandas as pd 
import yaml
import os.path
import itertools
from scipy import spatial
from collections import defaultdict

feature_df = pd.read_csv('feature_table.csv')
orig_df = pd.read_csv('cleaned_student_data.csv')
train_tbl = pd.read_csv('train_table.csv')
test_tbl = pd.read_csv('test_table.csv')
majors = ['540', '545', '72', '778', '8D', '536']

train_tbl = train_tbl[train_tbl['MajorCode'].isin(majors)]

def similarity_measures(feature_a, feature_b):
	euclidean = 1-spatial.distance.euclidean(feature_a, feature_b)

	return float(euclidean)

def create_feature_vector(df, shortkey):
	tmp_df = df[df['shortKey'] == shortkey]
	feature_vector = []
	feature_vector.append((tmp_df['running_gpa'].values))
	feature_vector.append((tmp_df['is_male'].values))
	feature_vector.append((tmp_df['gpa_last_quarter'].values))
	feature_vector.append((tmp_df['number_courses_so_far'].values))

	if len(tmp_df['quarter_count'].values) > 0 or len(tmp_df['running_gpa'].values) > 0 or len((tmp_df['quarter_count'].values)) > 0:
		return feature_vector
	return 0 

def find_students(major, quarter, drop_boolean):
	"""Takes as arguments majorCode, quarter for which we are examining student, and whether or not they dropped 
	within the next year (1 = drop, 0 = no drop)
	Returns a list of shortKeys for students who match this criteria"""

	students_with_major = feature_df[feature_df['MajorCode'] == major]
	students_with_major_quarter = students_with_major[students_with_major['quarter_count'] == quarter]
	students_with_major_quarter_drop = students_with_major_quarter[students_with_major_quarter['drops_out_in_next_year'] == drop_boolean]
	lst_of_shortkeys = students_with_major_quarter_drop['shortKey'].values.tolist()

	return lst_of_shortkeys

def get_accuracy_measures(similarity, label_a, label_b, threshold, true_positives, true_negatives, false_positives, false_negatives):
	"""So before, I had it so that for a certain similarity, depending on 
	what B's label was, then we would match... Now if we are considering a body of students, 
	what is label b?
	Well label b is always from students who drop. """
	if similarity > threshold and label_b == 0:
		predicted_label_a = 0
		if label_a == 0:
			true_negatives += 1
		else:
			false_negatives += 1
	if similarity > threshold and label_b == 1:
		predicted_label_a = 1
		if label_a == 1:
			true_positives += 1
		else:
			false_positives += 1
	if similarity <= threshold and label_b == 0:
		predicted_label_a = 1
		if label_a == 1:
			true_negatives +=1
		else:
			false_negatives += 1
	if similarity <= threshold and label_b == 1:
		predicted_label_a = 0
		if label_a == 0:
			true_positives += 1
		else:
			false_positives += 1
	# print true_positives, true_negatives, false_positives, false_negatives
	return true_positives, true_negatives, false_positives, false_negatives

def compare_students(student_a, label_a, students_drop):
	threshold = 0.5
	print "THRESHOLD: ", threshold
	similarity_list = []

	for j, student_b in enumerate(students_drop):
		label_b = float(feature_df[feature_df['shortKey'] == student_b]['drops_out_in_next_year'])
		if len(student_b) > 0 and label_b == 1: 
			feature_a = create_feature_vector(feature_df, student_a)
			feature_b = create_feature_vector(feature_df, student_b)

			if feature_a != 0 and feature_b != 0:
				similarity = similarity_measures(feature_a, feature_b)
				similarity_list.append(similarity)

	if len(similarity_list) > 0:
		print similarity_list
		final_similarity = sum(similarity_list)/float(len(similarity_list))
		print final_similarity
	return get_accuracy_measures(final_similarity, label_a, 1, threshold, true_positives, true_negatives, false_positives, false_negatives)
	 

def testing_function(row, true_positives, true_negatives, false_positives, false_negatives):
	
	if len(row['shortKey']) > 0: 
		student_a = row['shortKey']
		major = row['MajorCode']
		quarter = row['quarter_count']
		label_a = float(row['drops_out_in_next_year'])

		file_name_start = str(major) + "_" + str(quarter) 
		if(os.path.isfile(file_name_start + "_1.yml") and os.path.isfile(file_name_start + "_0.yml")):
			students_drop = yaml.load(open(file_name_start + "_1.yml", 'r'))
			true_positives, true_negatives, false_positives, false_negatives = compare_students(student_a, label_a, students_drop)
		else:
			with open(file_name_start + "_1.yml", 'w') as outfile:
				yaml.dump(find_students(major, quarter,1), outfile, default_flow_style = True)

			students_drop = yaml.load(open(file_name_start + "_1.yml", 'r'))
			true_positives, true_negatives, false_positives, false_negatives = compare_students(student_a, label_a, students_drop)
	
	return true_positives, true_negatives, false_positives, false_negatives

def testing_function2(true_positives, true_negatives, false_positives, false_negatives):
	for index, row in train_tbl.iterrows(): 
		if index < 8:
			if row['MajorCode'] in majors: 
				student = row['shortKey']
				alph_term = row['alph_term']
				major = row['MajorCode']
				quarter = row['quarter_count']
				label = float(row['drops_out_in_next_year'])
				print "LABEL IS: ", label

				print "PERSON A: ", row 

				file_name_start = str(major) + "_" + str(quarter) 
				if(os.path.isfile(file_name_start + "_1.yml")):
					students_drop = yaml.load(open(file_name_start + "_1.yml", 'r'))
					all_terms = students_drop.keys()

					for index_2, term in enumerate(all_terms):
						if term < alph_term:
							print "Term is okay"
							true_postives, true_negatives, false_positives, false_negatives = compare_students(student, label, students_drop[term])

	return true_positives, true_negatives, false_positives, false_negatives 

if __name__ == "__main__":

	true_positives = 0
	true_negatives = 0
	false_positives = 0
	false_negatives = 0

	grouped_major = train_tbl.groupby('MajorCode')
	for name, group_major in grouped_major:
		grouped_quarter = group_major.groupby('quarter_count')
		
		for name_2, group_quarter in grouped_quarter:
			grouped_term = group_quarter.groupby('alph_term')
			term_student_quarter_drop = defaultdict(list)
			term_student_quarter_no_drop = defaultdict(list)

			for name_3, group_term in grouped_term:
				grouped_label = group_term.groupby('drops_out_in_next_year')

				for name_4, group_label in grouped_label:
					if group_label['drops_out_in_next_year'].values.all() == 1:
						term_student_quarter_drop[group_term['alph_term'].values.tolist()[0]] = group_term['shortKey'].values.tolist()
					if group_label['drops_out_in_next_year'].values.all() == 0:
						term_student_quarter_no_drop[group_term['alph_term'].values.tolist()[0]] = group_term['shortKey'].values.tolist()
			
			major = group_quarter['MajorCode'].values.tolist()[0]
			quarter = group_quarter['quarter_count'].values.tolist()[0]

			file_name_start = str(major) + "_" + str(quarter) 
			if(os.path.isfile(file_name_start + "_1.yml")):
				students_drop = yaml.load(open(file_name_start + "_1.yml", 'r'))
			else:
				with open(file_name_start + "_1.yml", 'w') as outfile:
					print "Creating file: ", file_name_start
					yaml.dump(term_student_quarter_drop, outfile, default_flow_style = True)
					
			if(os.path.isfile(file_name_start + "_0.yml")):
				students_drop = yaml.load(open(file_name_start + "_0.yml", 'r'))
				apple = 2
			else:
				with open(file_name_start + "_0.yml", 'w') as outfile:
					print "Creating file: ", file_name_start
					yaml.dump(term_student_quarter_no_drop, outfile, default_flow_style = True)

	# testing_function2(true_positives, true_negatives, false_positives, false_negatives)
	for index, row in train_tbl.iterrows(): 
		if index < 500:
			threshold = 0.5
			if row['MajorCode'] in majors: 
				student_a = row['shortKey']
				alph_term = row['alph_term']
				major = row['MajorCode']
				quarter = row['quarter_count']
				label_a = float(row['drops_out_in_next_year'])
				print "Label: ", label_a

				file_name_start = str(major) + "_" + str(quarter) 
				if(os.path.isfile(file_name_start + "_1.yml")):
					students_drop = yaml.load(open(file_name_start + "_1.yml", 'r'))
					all_terms = students_drop.keys()

					for index_2, term in enumerate(all_terms):
						if term < alph_term:
							print "THRESHOLD: ", threshold
							similarity_list_1 = []
							for j, student_b in enumerate(students_drop[term]):
								label_b = float(train_tbl[train_tbl['shortKey'] == student_b]['drops_out_in_next_year'])
								if len(student_b) > 0 and label_b == 1: 
									feature_a = create_feature_vector(feature_df, student_a)
									feature_b = create_feature_vector(feature_df, student_b)

									if feature_a != 0 and feature_b != 0:
										similarity = similarity_measures(feature_a, feature_b)
										similarity_list_1.append(similarity)

							if len(similarity_list_1) > 0:
								
								final_similarity = sum(similarity_list_1)/float(len(similarity_list_1))
								print "Similarity for Drop Out: ", final_similarity

							true_positives, true_negatives, false_positives, false_negatives = get_accuracy_measures(final_similarity, label_a, 1, threshold, true_positives, true_negatives, false_positives, false_negatives)
				
				if(os.path.isfile(file_name_start + "_0.yml")):
					students_drop = yaml.load(open(file_name_start + "_0.yml", 'r'))
					all_terms = students_drop.keys()
					for index_2, term in enumerate(all_terms):
						if term < alph_term:
							print "THRESHOLD: ", threshold
							similarity_list_0 = []
							for j, student_b in enumerate(students_drop[term]):
								label_b = float(train_tbl[train_tbl['shortKey'] == student_b]['drops_out_in_next_year'])
								if len(student_b) > 0 and label_b == 0: 
									feature_a = create_feature_vector(feature_df, student_a)
									feature_b = create_feature_vector(feature_df, student_b)

									if feature_a != 0 and feature_b != 0:
										similarity = similarity_measures(feature_a, feature_b)
										similarity_list_0.append(similarity)

							if len(similarity_list_0) > 0:
								final_similarity = sum(similarity_list_0)/float(len(similarity_list_0))
								print "Similarity for No Drop Out: ", final_similarity


	 						true_positives, true_negatives, false_positives, false_negatives = get_accuracy_measures(final_similarity, label_a, 0, threshold, true_positives, true_negatives, false_positives, false_negatives)
	print "Accuracy: ", float(true_positives + true_negatives)/float(true_positives + true_negatives + false_negatives + false_positives)
