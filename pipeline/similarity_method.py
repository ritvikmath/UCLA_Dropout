import pandas as pd 
from scipy import spatial

feature_df = pd.read_csv('feature_table.csv')
orig_df = pd.read_csv('cleaned_student_data.csv')
train_tbl = pd.read_csv('train_table.csv')
test_tbl = pd.read_csv('test_table.csv')


# DESIRED_FEATURES = ['quarter_count', 'running_gpa', 'is_male', 'is_female']

""""Say that we have a student on quarter X. 
This student has a bunch of features we have already calculated. 
We want to see how similar this student is to other students at quarter count X. 
We also want to test how good this is. So we want to measure the accuracy with different
similarity metrics.

We have a student with a feature vector. We compare this student with students who don't drop out. 
We compare this student with students who do drop out. We pick the higher similarity. 

So maybe I can run a bunch of tests by major"""
def similarity_measures(feature_a, feature_b):
	euclidean = 1-spatial.distance.euclidean(feature_a, feature_b)
	canberra = 1-spatial.distance.canberra(feature_a, feature_b)
	return (euclidean + canberra)/2

def create_feature_vector(df, shortkey):
	tmp_df = df[df['shortKey'] == shortkey]
	feature_vector = []

	feature_vector.append((tmp_df['quarter_count'].values))
	feature_vector.append((tmp_df['running_gpa'].values))
	feature_vector.append((tmp_df['is_male'].values))
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

	# print students_with_major_quarter_drop.head()

	return lst_of_shortkeys

if __name__ == "__main__":
	for index, row in train_tbl.iterrows(): 

		if len(row['shortKey']) > 0: 
			print "YES\n"
			student_a = row['shortKey']
			major = row['MajorCode']
			quarter = row['quarter_count']
			label_a = float(row['drops_out_in_next_year'])


			students_drop = find_students(major, quarter, 1)
			students_no_drop = find_students(major, quarter, 0)

			true_positive = 0
			true_negatives = 0
			false_positives = 0
			false_negatives = 0

			for index, student_b in enumerate(students_drop):
				label_b = float(feature_df[feature_df['shortKey'] == student_b]['drops_out_in_next_year'])
				if len(student_b) > 0: 
					feature_a = create_feature_vector(feature_df, student_a)
					feature_b = create_feature_vector(feature_df, student_b)

					# print "Feature A: ", feature_a
					# print "Feature B: ", feature_b

					if feature_a != 0 and feature_b != 0:
						similarity = similarity_measures(feature_a, feature_b)
						if similarity > 0.5 and label_b == 0:
							predicted_label_a = 0
							if label_a == 0:
								true_negatives += 1
							else:
								false_negatives += 1
						if similarity > 0.5 and label_b == 1:
							predicted_label_a = 1
							if label_a == 1:
								true_positive += 1
							else:
								false_positives
						if similarity <= 0.5 and label_b == 0:
							predicted_label_a = 0
							if label_a == 0:
								true_negatives +=1
							else:
								false_negatives += 1
						if similarity <= 0.5 and label_b == 1:
							predicted_label_a = 1
							if label_a == 1:
								true_positive += 1
							else:
								false_positives += 1

	print "Accuracy, ", float(true_positive + true_negatives)/float(true_positive + true_negatives + false_negatives + false_positives)
