import numpy
import random
import csv
import matplotlib.pyplot as plt

AVERAGE = "Average"
STDDEV = "Standard Deviation"
people = 10000
drivers_values = dict(Operations=dict(eSat={AVERAGE: 59, STDDEV: 13}, Career={AVERAGE: 67, STDDEV: 13},
                                      Empowerment={AVERAGE: 73, STDDEV: 13},
                                      Recognition={AVERAGE: 64, STDDEV: 13},
                                      Balance={AVERAGE: 68, STDDEV: 13},
                                      Prospects={AVERAGE: 76, STDDEV: 13},
                                      Resources={AVERAGE: 71, STDDEV: 8}, Team={AVERAGE: 74, STDDEV: 13},
                                      Feedback={AVERAGE: 68, STDDEV: 13})
                      # Engineering=dict(eSat={AVERAGE: 69, STDDEV: 13},
                      #                  Career={AVERAGE: 67, STDDEV: 13},
                      #                  Empowerment={AVERAGE: 73, STDDEV: 13},
                      #                  Recognition={AVERAGE: 64, STDDEV: 13},
                      #                  Balance={AVERAGE: 68, STDDEV: 13},
                      #                  Prospects={AVERAGE: 76, STDDEV: 13},
                      #                  Resources={AVERAGE: 71, STDDEV: 8},
                      #                  Team={AVERAGE: 74, STDDEV: 13},
                      #                  Feedback={AVERAGE: 68, STDDEV: 13}),
                      # Marketing=dict(eSat={AVERAGE: 69, STDDEV: 13},
                      #                Career={AVERAGE: 67, STDDEV: 13},
                      #                Empowerment={AVERAGE: 73, STDDEV: 13},
                      #                Recognition={AVERAGE: 64, STDDEV: 13},
                      #                Balance={AVERAGE: 68, STDDEV: 13},
                      #                Prospects={AVERAGE: 76, STDDEV: 13},
                      #                Resources={AVERAGE: 71, STDDEV: 8},
                      #                Team={AVERAGE: 74, STDDEV: 13},
                      #                Feedback={AVERAGE: 68, STDDEV: 13}),
                      # Support=dict(eSat={AVERAGE: 69, STDDEV: 13},
                      #              Career={AVERAGE: 67, STDDEV: 13},
                      #              Empowerment={AVERAGE: 73, STDDEV: 13},
                      #              Recognition={AVERAGE: 64, STDDEV: 13},
                      #              Balance={AVERAGE: 68, STDDEV: 13},
                      #              Prospects={AVERAGE: 76, STDDEV: 13},
                      #              Resources={AVERAGE: 71, STDDEV: 8},
                      #              Team={AVERAGE: 74, STDDEV: 13},
                      #              Feedback={AVERAGE: 68, STDDEV: 13}),
                      # Sales=dict(eSat={AVERAGE: 69, STDDEV: 13},
                      #            Career={AVERAGE: 67, STDDEV: 13},
                      #            Empowerment={AVERAGE: 73, STDDEV: 13},
                      #            Recognition={AVERAGE: 64, STDDEV: 13},
                      #            Balance={AVERAGE: 68, STDDEV: 13},
                      #            Prospects={AVERAGE: 76, STDDEV: 13},
                      #            Resources={AVERAGE: 71, STDDEV: 8},
                      #            Team={AVERAGE: 74, STDDEV: 13},
                      #            Feedback={AVERAGE: 68, STDDEV: 13}),
                      # Finance=dict(eSat={AVERAGE: 69, STDDEV: 13},
                      #              Career={AVERAGE: 67, STDDEV: 13},
                      #              Empowerment={AVERAGE: 73, STDDEV: 13},
                      #              Recognition={AVERAGE: 64, STDDEV: 13},
                      #              Balance={AVERAGE: 68, STDDEV: 13},
                      #              Prospects={AVERAGE: 76, STDDEV: 13},
                      #              Resources={AVERAGE: 71, STDDEV: 8},
                      #              Team={AVERAGE: 74, STDDEV: 13},
                      #              Feedback={AVERAGE: 68, STDDEV: 13}),
                      # HR=dict(eSat={AVERAGE: 69, STDDEV: 13},
                      #         Career={AVERAGE: 67, STDDEV: 13},
                      #         Empowerment={AVERAGE: 73, STDDEV: 13},
                      #         Recognition={AVERAGE: 64, STDDEV: 13},
                      #         Balance={AVERAGE: 68, STDDEV: 13},
                      #         Prospects={AVERAGE: 76, STDDEV: 13},
                      #         Resources={AVERAGE: 71, STDDEV: 8},
                      #         Team={AVERAGE: 74, STDDEV: 13},
                      #         Feedback={AVERAGE: 68, STDDEV: 13})
                      )


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
            for driver in drivers_values[val]:
                print driver
                if driver == "eSat":
                    temp_val = random.normalvariate(drivers_values[val][driver][AVERAGE], drivers_values[val][driver][
                        STDDEV])
                    ranged_esat_values.append(temp_val)
                    print temp_val
                    if 94 <= temp_val:
                        esat_values.append(7)
                    elif 79 <= temp_val < 94:
                        esat_values.append(6)
                    elif 64 <= temp_val < 79:
                        esat_values.append(5)
                    elif 50 <= temp_val < 64:
                        esat_values.append(4)
                    elif 36 <= temp_val < 50:
                        esat_values.append(3)
                    elif 20 <= temp_val < 36:
                        esat_values.append(2)
                    elif 0 <= temp_val < 20:
                        esat_values.append(1)
    temp_calc = 0
    print esat_values
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
