import numpy
import random
import csv
import matplotlib.pyplot as plt

AVERAGE = "Average"
STDDEV = "Standard Deviation"
people = 10000
drivers_values = dict(eSat={AVERAGE: 69, STDDEV: 7}, Career={AVERAGE: 67, STDDEV: 7},
					  Empowerment={AVERAGE: 73, STDDEV: 7},
					  Recognition={AVERAGE: 64, STDDEV: 7},
					  Balance={AVERAGE: 68, STDDEV: 7},
					  Prospects={AVERAGE: 76, STDDEV: 7},
					  Resources={AVERAGE: 71, STDDEV: 6}, Team={AVERAGE: 74, STDDEV: 7},
					  Feedback={AVERAGE: 68, STDDEV: 7})


def random_val(beginning, length):
	defined_val = random.randint(beginning, length)
	return defined_val


def view_scores(scores):
	plt.hist(scores, bins=[1, 2, 3, 4, 5, 6, 7])
	plt.show()


def generate_scores(num_people):
	ranged_esat_values = []
	esat_values = []
	for person in range(num_people):
		for val in drivers_values:
			if val == "eSat":
				temp_val = random.normalvariate(drivers_values[val][AVERAGE], drivers_values[val][
					STDDEV])
				ranged_esat_values.append(temp_val)
				if 94 <= temp_val < 100:
					esat_values.append(7)
				elif 79 <= temp_val < 94:
					chosen_to_go_to_seven = random_val(0, 2)
					if chosen_to_go_to_seven is None:
						esat_values.append(7)
					else:
						print "test"
						esat_values.append(6)
				elif 64 <= temp_val < 79:
					chosen_value_for_five = random_val(0, 3)
					print chosen_value_for_five
					if chosen_value_for_five == 1:
						esat_values.append(4)
					elif chosen_value_for_five == 0:
						print "test"
						esat_values.append(6)
					else:
						esat_values.append(5)
				elif 50 <= temp_val < 64:
					chosen_to_go_to_three = random_val(0, 1)
					if chosen_to_go_to_three:
						esat_values.append(3)
					else:
						esat_values.append(4)
				elif 36 <= temp_val < 50:
					esat_values.append(3)
				elif 20 <= temp_val < 36:
					esat_values.append(2)
				elif 0 <= temp_val < 20:
					esat_values.append(1)
	temp_calc = 0
	for val in esat_values:
		temp_calc += float(val) / 7 * 100

	# temp_calc += (val/7) * 100
	print temp_calc / len(esat_values)
	print reduce(lambda x, y: x + y, ranged_esat_values) / len(ranged_esat_values)

	return esat_values, ranged_esat_values


esat_values, ranged_esat_values = generate_scores(people)
view_scores(esat_values)

with open('survey.csv', 'w') as survey_csv:
	header = ["score"]
	writer = csv.DictWriter(survey_csv, fieldnames=header)
	writer.writeheader()
	for esat_score in esat_values:
		writer.writerow({"score": esat_score})
