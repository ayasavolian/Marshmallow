# standard for Python comments
# random choice/choose for even chance of list

# Script to auto-generate data for a demo
import random
import csv
import json
import datetime
import urllib
import json
import codecs
import re

class Data(object):
	def __init__(self):

		self.EXCEEDS = "Exceeds"
		self.CUSTOMER_SATISFACTION = "Customer Satisfaction"
		self.SOMEWHAT_EXCEEDS = "Somewhat Exceeds"
		self.MEETS = "Meets"
		self.DOES_NOT_MEET = "Does Not Meet"
		self.PERFORMANCE_RATING = "Performance Rating"
		self.PERFORMANCE_OPTIONS = "Performance Options"
		self.PERFORMANCE_RATING_NAME = "Performance Rating Name"
		self.MINIMUM_GENERATOR = "Minimum Generator"
		self.NUMBER_GENERATOR = "Number Generator"
		self.CUSTOMER_SATISFACTION_NAME = "Customer Satisfaction Name"


		##################################################################################################################################################################
		# @employees : this is the number of employees in the demo. This will eventually be used to calculate all of the locations that will actually be used and also
		# the number of department_depth or the depth of the org hierarchy
		# @department_depth : this is the depth of the org hierarchy. This is based on the number of employees and will be auto-calculated 
		# @employee_count : this is the number of employees in the company and also used as the unique identifier when generating data
		# @hq_split : this is the split of choosing the hq vs. any of the other locations within a state or country. This is based on a scale of 1 to 10
		# @us_split : this is the split between choosing the united states or choosing Canada for NA. This is based on a scale of 1 to 10
		# @remote_employee : this is the chance of choosing a remote employee on a scale of 1 to 10. 
		# @names : these are all of the randomly generated names from the API that we've accumulated so we dont have to call the API every time
		##################################################################################################################################################################

		self.employees = 80000
		self.department_depth = 6
		self.employee_count = 0
		self.hq_split = 5
		self.us_split = 9
		self.remote_employee = 1
		self.names = []

		##################################################################################################################################################################
		# @hierarchy_breakdown : this is the number of reports that will be generated for that manager for each manager. 
		# @exec_position : this is the position of each employee based on the hierarchy_vals
		# @exec_department : this is the department of each of the employees
		# @exec_level : this is the level of every employee 
		# @hierarchy_level_1 : this is the region of every employee
		# @hierarchy_level_2 : this is the country of every employee 
		# @hierarchy_level_3 : this is the city/state of every employee
		##################################################################################################################################################################

		self.hierarchy_breakdown = {}
		self.exec_position = {}
		self.exec_department = {}
		self.exec_level = {}
		self.hierarchy_level_1 = {}
		self.hierarchy_level_2 = {}
		self.hierarchy_level_3 = {}

		# These are the departments that we'll be using throughout the demo
		self.departments = ['Operations', 'Engineering', 'Marketing', 'Support', 'Sales', 'Finance', 'HR']
		# These are all of the countries that can be chosen based on the regions. These locations are based on the hierarchy_vals 
		self.location_regions = {"EMEA" : ["Germany", "UK", "Ireland", "France", "Netherlands", "United Arab Emirates", "South Africa", "Israel"],
			"APAC" : ["Phillippines", "India", "Singapore", "China", "Japan"],
			"NA" : ["US", "CA"]}
		#these are the tiers that will be referenced in the create structure hierarchy build
		self.location_tiers = {"Tier 1" : ["US", "UK", "Singapore"],
			"Tier 2" : ["India", "Ireland", "China", "Israel"],
			"Tier 3" : ["Germany", "Netherlands", "United Arab Emirates", "South Africa", "Phillippines", "Japan", "CA"]}

		##################################################################################################################################################################
		# @location_countries : These are all of the countries taht can be chosen. We added the states in too, so we'll filter down as far as possible to see if keys exist. 
		# If the key doesn't exist then we'll stop and say thats the last of the hierarchy. If the HQ doesn't exist theres a split between the Other locations. If
		# The other locations doesn't exist its a 100% chance to go to the HQ. There are some special cases here that should be taken care of with this methodology,
		# both the United States and Canada have their provinces/states which have their own states within. We'll filter down to those with this methodology
		##################################################################################################################################################################
		
		self.location_countries = {"Phillippines" : {"HQ" : "Manila", "Other" : ["Cebu", "Davao"]}, 
			"India" :  {"HQ" : "Mumbai", "Other" : ["Chennai", "Kolkata", "Delhi"]},
			"Singapore" : {"HQ" : "Singapore City", "Other" : []},
			"China" : {"HQ" : "Shanghai", "Other" : ["Guangzhao", "Beijing", "Shantou"]},
			"Japan" : {"HQ" : "Tokyo", "Other" : ["Yokohama", "Kyoto", "Osaka"]},
			"UK" : {"HQ" : "London", "Other" : ["Birmingham", "Leeds"]},
			"Germany" : {"HQ" : "Berlin", "Other" : ["Munich"]},
			"Ireland" : {"HQ" : "Dublin", "Other" : []},
			"France" : {"HQ" : "Paris", "Other" : ["Lyon"]},
			"Netherlands" : {"HQ" : "Amsterdam", "Other" : ["Rotterdam"]},
			"United Arab Emirates" : {"HQ" : "Dubai", "Other" : []},
			"South Africa" : {"HQ" : "Capetown", "Other" : ["Johannesburg"]},
			"Israel" : {"HQ" : "Tel Aviv", "Other" : ["Jerusalem"]},
			"United States" : {"HQ" : "", "Other" : ["California", "Texas"]},
			"Canada" : {"HQ" : "Ontario", "Other" : ["Alberta", "Quebec", "British Columbia"]},
			"Ontario" : {"HQ" : "Toronto", "Other": []},
			"Alberta" : {"HQ" : "", "Other": ["Calgary"]},
			"Quebec" : {"HQ" : "", "Other": ["Calgary"]},
			"British Columbia" : {"HQ" : "", "Other": ["Vancouver"]},
			"California" : {"HQ" : "San Francisco", "Other" : ["Los Angeles", "San Diego"]},
			"Texas" : {"HQ" : "Austin", "Other" : ["Dallas"]}}

		##################################################################################################################################################################
		# @location_countries : These are all of the remote locations we'll be using for the demo. There is only a partial chance that an employee can place into
		# any of these locations. Currently its a 1/10 chance they can. 
		##################################################################################################################################################################
		
		self.remote_locations = [{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "New York", "Location Hierarchy 4" : "New York City"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Florida", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Illinois", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "New Jersey", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Nebraska", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Ohio", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Maine", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Washington", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "South Carolina", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Maryland", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Georgia", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "United States", "Location Hierarchy 3" : "Texas", "Location Hierarchy 4" : "Jacksonville"},
			{"Location Hierarchy 1" : "NA", "Location Hierarchy 2" : "Mexico", "Location Hierarchy 3" : "Mexico City", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "SA", "Location Hierarchy 2" : "Brazil", "Location Hierarchy 3" : "Sao Paulo", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "SA", "Location Hierarchy 2" : "El Salvador", "Location Hierarchy 3" : "San Salvador", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "SA", "Location Hierarchy 2" : "Colombia", "Location Hierarchy 3" : "Bogota", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "EMEA", "Location Hierarchy 2" : "France", "Location Hierarchy 3" : "Tours", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "EMEA", "Location Hierarchy 2" : "Germany", "Location Hierarchy 3" : "Hamburg", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "EMEA", "Location Hierarchy 2" : "Croatia", "Location Hierarchy 3" : "Split", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "EMEA", "Location Hierarchy 2" : "China", "Location Hierarchy 3" : "Hong Kong", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "APAC", "Location Hierarchy 2" : "Thailand", "Location Hierarchy 3" : "Bangkok", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "APAC", "Location Hierarchy 2" : "South Korea", "Location Hierarchy 3" : "Seoul", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "APAC", "Location Hierarchy 2" : "Malaysia", "Location Hierarchy 3" : "Kuala Lumpur", "Location Hierarchy 4" : ""},
			{"Location Hierarchy 1" : "APAC", "Location Hierarchy 2" : "Indonesia", "Location Hierarchy 3" : "Jakarta", "Location Hierarchy 4" : ""}]

		##################################################################################################################################################################
		# These are the values for the hierarchy that will show up for the different people. Currently the highest level is Chief and then down to the Employee
		# @hierarchy_vals : this has the title of the position and then a number generator which is the likelihood of having the number of positions below it 
		# 	in the dictionary array
		##################################################################################################################################################################
		
		self.hierarchy_vals = []

		##################################################################################################################################################################
		# what we're doing here is adding the attributes for the csv. 
		# @attributes : Fields we're adding...
		# 	@Gender : Male or Female
		# 	@Birth Date : Birth Date is calculated using the random number generator for the year, month, and day. The year is between 1940 and 1993,
		# 		the month is between 1 to 12 and the day is between 1 to 28. 
		# 		(<1946 - Silent Generation - 1%, 1947 - 1965 - Baby Boomer - 5%, 1966 - 1980 - Generation X - 45%, 1981 - 2000 - Generation Y - 50%, >2000 Generation Z)
		# 	@Hire Date : Hire Date is similar to birth date. It uses the random number generator for the values for year, month, and date. The year Date
		# 		has a minimum of 1995 and a max of 2015
		# 	@Location : This is going to reference the dictionary above in location_hierarchy but the original region will be based on a random number generator
		# 		between a score of 0 to 1. If the score is greater than a specific value and less than a specific value it will fall to different areas. Currently
		# 		this is setup so that NA will be 40% of the time, APAC will be 30% of the time, and EMEA will be 30% of the time. 
		##################################################################################################################################################################
		
		self.attributes = {"Gender" : {"Attributes" : ["male", "female"], "Male" : 6}, 
			"Birth Date" : {"Birth Year" : {"Number Generator" : 1993, "Minimum Generator" : 1940, 
					"Generation" : [{"Generation Name" : "Silent Generation", "Minimum Year" : 1940, "Max Year" : 1946, "Minimum Generator" : 0, "Maximum Generator" : 1},
						{"Generation Name" : "Baby Boomer", "Minimum Year" : 1947, "Max Year" : 1965, "Minimum Generator" : 1, "Maximum Generator" : 6},
						{"Generation Name" : "Generation X", "Minimum Year" : 1966, "Max Year" : 1980, "Minimum Generator" : 6, "Maximum Generator" : 51},
						{"Generation Name" : "Generation Y", "Minimum Year" : 1981, "Max Year" : 1992, "Minimum Generator" : 51, "Maximum Generator" : 100}]},
				"Birth Month" : {"Number Generator" : 12, "Minimum Generator" : 1}, 
				"Birth Date" : {"Number Generator" : 28, "Minimum Generator" : 1}},
			"Hire Date" : {"Hire Year" : {"Number Generator" : 1995, "Minimum Generator" : 2015,
					"Tenure" : [{"Tenure Name" : "<1 Year", "Minimum Year" : 0, "Max Year" : 1}, 
						{"Tenure Name" : "1-2 Years", "Minimum Year" : 1, "Max Year" : 2},  
						{"Tenure Name" : "2-3 Years", "Minimum Year" : 2, "Max Year" : 3}, 
						{"Tenure Name" : "3-4 Years", "Minimum Year" : 3, "Max Year" : 4}, 
						{"Tenure Name" : "4-5 Years", "Minimum Year" : 4, "Max Year" : 5}, 
						{"Tenure Name" : "5-7 Years", "Minimum Year" : 5, "Max Year" : 7}, 
						{"Tenure Name" : "7+ Years", "Minimum Year" : 7, "Max Year" : 15}]}, 
				"Hire Month" : {"Number Generator" : 12, "Minimum Generator" : 1}, 
				"Hire Day" : {"Number Generator" : 28, "Minimum Generator" : 1}},
			"Location" : {"Location Generator" : {"EMEA" : {"Minimum" : 4, "Maximum" : 7}, 
					"APAC" : {"Minimum" : 7, "Maximum" : 10},
					"NA" : {"Minimum" : 0, "Maximum" : 4}}, 
				"Number Generator" : 10, 
				"Minimum Generator": 1},
			"Performance Rating" : {"Performance Options" : [{"Performance Rating Name" : "Exceeds", "Minimum Generator" : 0, "Number Generator" : 15},
				{"Performance Rating Name" : "Somewhat Exceeds", "Minimum Generator" : 15, "Number Generator" : 40},
				{"Performance Rating Name" : "Meets", "Minimum Generator" : 40, "Number Generator" : 90},
				{"Performance Rating Name" : "Does Not Meet", "Minimum Generator" : 90, "Number Generator" : 100}]},
			"Customer Satisfaction" : {"Exceeds" : [{"Customer Satisfaction Name" : "Promoter", "Minimum Generator" : 0, "Number Generator" : 100}],
				"Somewhat Exceeds" : [{"Customer Satisfaction Name" : "Promoter", "Minimum Generator" : 0, "Number Generator" : 80},
					{"Customer Satisfaction Name" : "Passive", "Minimum Generator" : 80, "Number Generator" : 100}],
				"Meets" : [{"Customer Satisfaction Name" : "Passive", "Minimum Generator" : 0, "Number Generator" : 60},
					{"Customer Satisfaction Name" : "Detractor", "Minimum Generator" : 60, "Number Generator" : 100}],
				"Does Not Meet" : [{"Customer Satisfaction Name" : "Passive", "Minimum Generator" : 0, "Number Generator" : 100}]}}
		# this is the final hierarchy that we'll be using
		self.hierarchy = []

	##################################################################################################################################################################
	# @create_structure : This creates the structure for the actual demo based on the number of employees. What this does is it says the number of managers in the hierarchy
	# and which manager titles and also the locations that will exist in the demo based on tiering.
	##################################################################################################################################################################

	def create_structure(self):

		def choose_country_tiers(tier):
			temp_tier = []
			for val in tier:
				temp_tier.extend(self.location_tiers[str(val)])
			for val in self.location_regions:
				location_index = -1
				for index in range(len(self.location_regions[val])):
					location_index += 1
					if self.location_regions[val][location_index] not in temp_tier:
						self.location_regions[val].remove(self.location_regions[val][location_index])
						location_index -= 1


		if self.employees < 1000: 
			tier = ["Tier 1"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 2 }, 
			{"Title" : "SVP", "Number Generator" : 2 },
			{"Title" : "VP", "Number Generator" : 3 },
			{"Title" : "Director", "Number Generator" : 5 },
			{"Title" : "Manager", "Number Generator" : 9 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])
		elif self.employees < 3000:
			tier = ["Tier 1"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 2}, 
			{"Title" : "SVP", "Number Generator" : 3 },
			{"Title" : "VP", "Number Generator" : 3 },
			{"Title" : "Sr. Director", "Number Generator" : 3 },
			{"Title" : "Director", "Number Generator" : 6 },
			{"Title" : "Manager", "Number Generator" : 13 },
			{"Title" : "Individual Contributor", "Number Generator" : 0 }])
		elif self.employees < 5000:
			tier = ["Tier 1", "Tier 2"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 2 }, 
			{"Title" : "SVP", "Number Generator" : 3 },
			{"Title" : "VP", "Number Generator" : 3 },
			{"Title" : "Sr. Director", "Number Generator" : 4 },
			{"Title" : "Director", "Number Generator" : 7 },
			{"Title" : "Manager", "Number Generator" : 14 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])
		elif self.employees < 10000:
			tier = ["Tier 1", "Tier 2"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 3 }, 
			{"Title" : "SVP", "Number Generator" : 3 },
			{"Title" : "VP", "Number Generator" : 4 },
			{"Title" : "Sr. Director", "Number Generator" : 5 },
			{"Title" : "Director", "Number Generator" : 8 },
			{"Title" : "Manager", "Number Generator" : 14 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])
		elif self.employees < 20000:
			tier = ["Tier 1", "Tier 2", "Tier 3"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 3 }, 
			{"Title" : "SVP", "Number Generator" : 4 },
			{"Title" : "VP", "Number Generator" : 4 },
			{"Title" : "Sr. Director", "Number Generator" : 7 },
			{"Title" : "Director", "Number Generator" : 9 },
			{"Title" : "Manager", "Number Generator" : 13 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])
		elif self.employees < 30000:
			tier = ["Tier 1", "Tier 2", "Tier 3"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 3 }, 
			{"Title" : "SVP", "Number Generator" : 4 },
			{"Title" : "VP", "Number Generator" : 5 },
			{"Title" : "Sr. Director", "Number Generator" : 8 },
			{"Title" : "Director", "Number Generator" : 9 },
			{"Title" : "Manager", "Number Generator" : 15 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])
		elif self.employees < 50000:
			tier = ["Tier 1", "Tier 2", "Tier 3"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 4 }, 
			{"Title" : "SVP", "Number Generator" : 4 },
			{"Title" : "VP", "Number Generator" : 5 },
			{"Title" : "Sr. Director", "Number Generator" : 10 },
			{"Title" : "Director", "Number Generator" : 12 },
			{"Title" : "Manager", "Number Generator" : 15 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])
		else:
			tier = ["Tier 1", "Tier 2", "Tier 3"]
			choose_country_tiers(tier)
			self.hierarchy_vals.extend([{"Title" : "Chief", "Number Generator" : 5 }, 
			{"Title" : "SVP", "Number Generator" : 5 },
			{"Title" : "VP", "Number Generator" : 7},
			{"Title" : "Sr. Director", "Number Generator" : 11 },
			{"Title" : "Director", "Number Generator" : 13 },
			{"Title" : "Manager", "Number Generator" : 15 },
			{"Title" : "Individual Contributor", "Number Generator" : 1 }])

	##################################################################################################################################################################
	# @pull_names : this pulls the names from the csv file which we've accumulated and adds everyones name to a variable named self.names. We can then use that variable
	# whenever to pull the first and last name of randomly chosen individuals
	##################################################################################################################################################################

	def pull_names(self):
		with codecs.open('employee_names.csv', 'rU', encoding='utf-8', errors='ignore') as file:
			input_file = csv.reader(file, delimiter=",", quotechar='|')
			for row in input_file:
				pattern = re.compile('_')
				if pattern.match(row[0]):
					pass
				else:
					self.names.append(row)

	##################################################################################################################################################################
	# @define_hierarchy : the purpose of this is to be the center point of creating the entire organization hierarchy and all of the attributes using other methods.
	# This will first create the executives in the first for loop, and then keep track of various lists for the executives which are then referenced in the second
	# for loop.
	# The second for loop takes every one of the managers and loops through them. We've already calculated executives so we'll skip them. For every manager it loops 
	# through the number of direct reports they have. It then will continue to go through every hierarchy_vals (every level of the organization) and generate a random number 
	# between the 1 to the highest number in the "Number" Generator" and assign that as the value of the number of direct reports to the specific manager until it gets through 
	# every individual and they're direct reports. So, position is the current individual, and level is the number of direct reports for every level of the entire hierarchy. 
	# At the same time at the end of every end of each manager's directs we will add those individuals to each of the lists so we can then use them in the next round of the
	# hierarchy_breakdown which will grow on itself so it can be properly referenced by the new manager's directs. 
	##################################################################################################################################################################

	def define_hierarchy(self):
		number_of_hierarchy = {}
		for val in self.departments:
			self.hierarchy.append(self.add_position(
				self.hierarchy_vals[0]['Title'], 
				val, 
				0, 
				0, 
				""))
			number_of_hierarchy[self.employee_count] = self.random_val(1, self.hierarchy_vals[0]['Number Generator'])
		self.hierarchy_breakdown = dict((val, range(number_of_hierarchy[val])) for val in number_of_hierarchy)
		self.exec_position = dict((executive['ID'], executive['Position']) for executive in self.hierarchy)
		self.exec_department = dict((executive['ID'], executive['Department']) for executive in self.hierarchy)
		self.exec_level = dict((executive['ID'], executive['Level']) for executive in self.hierarchy)
		# iterate through the list of the entire hierarchy structure
		for index, hierarchy in enumerate(self.hierarchy_vals):
			# if its not the first one because that is executives
			number_of_hierarchy = {}
			if index:
				for position in self.hierarchy_breakdown:
					for level in self.hierarchy_breakdown[position]:
						self.hierarchy.append(self.add_position(
							self.hierarchy_vals[index]['Title'], 
							self.exec_department[position], 
							position, 
							self.exec_level[position]+1, 
							self.exec_department[position] + " Department " + str(level)))
						number_of_hierarchy[self.employee_count] = self.random_val(1, self.hierarchy_vals[index]['Number Generator'])
				self.hierarchy_breakdown = dict((val, range(number_of_hierarchy[val])) for val in number_of_hierarchy)
				self.exec_position = dict((executive['ID'], executive['Position']) for executive in self.hierarchy)
				self.exec_department = dict((executive['ID'], executive['Department']) for executive in self.hierarchy)
				self.exec_level = dict((executive['ID'], executive['Level']) for executive in self.hierarchy)
				self.direct_manager = dict((executive['ID'], executive['Manager']) for executive in self.hierarchy)
				self.hierarchy_level_1 = dict((executive['ID'], executive['Location Hierarchy 1']) for executive in self.hierarchy)
				self.hierarchy_level_2 = dict((executive['ID'], executive['Location Hierarchy 2']) for executive in self.hierarchy)
				self.hierarchy_level_3 = dict((executive['ID'], executive['Location Hierarchy 3']) for executive in self.hierarchy)

	##################################################################################################################################################################
	# @random_val : this going to be a random number generator which will be reference by all of the other methods. This is going to automatically calculate any random
	# number between two values which will be fed into this static method
	##################################################################################################################################################################		

	@staticmethod
	def random_val(beginning, length):
		defined_val = random.randint(beginning, length)
		return defined_val

	##################################################################################################################################################################
	# @add_position : this is going to take into account all of the different fields calculated in define_hierarchy and place them into a dictionary which will be sent 
	# back to the self.hierarchy as another individual. Within here we also calculate the attributes of the individual. So we currently calculate the locations which
	# are added to the positions dictionary and then sent back.
	##################################################################################################################################################################

	def add_position(self, position, department, manager, level, sub_dep):
		self.employee_count += 1
		positions = {
			'Position' : position,
			'Manager' : manager,
			'ID' : self.employee_count,
			'Level' : level,
			'Department' : department,
			'Sub-Department' : sub_dep
		}
		positions.update(self.add_locations(manager, level))
		gender = self.add_gender()
		positions.update(gender)
		positions.update(self.add_birth_date_and_generation())
		positions.update(self.add_hire_date_and_tenure())
		positions.update(self.add_first_and_last_name(gender['Gender']))
		positions.update(self.add_performance_rating_and_customer_satisfaction())
		return positions

	##################################################################################################################################################################
	# @add_locations : This is going to automatically create the location hierarchy for every employee. This is accomplished by using the class variabels for 
	# location_regions, location_countries, and remote_locations. It also takes into account the splits for everything and the remote_location calculation in class variables
	# Using these variables it will correctly assign the region, country, state, city for every employee. It does this by first randomly choosing locations for the executives,
	# svp's, and vp's. After doing that it will choose the down to the country/state for every sr. directors. Every employee under the sr. director will then get the same
	# location as the manager above them, and then employees at the end have a specific chance of being remote based on remote_employee. This function takes into account a couple fields
	# which are passed in, manager and level. These are important because manager is the id of the manager which makes it easier to take the manager's locations and the level is to make
	# sure the person is not a VP when adding their location. 
	# 	@add_random_location : this function will be reused by multiple sections in the add_locations calculation. Its really used to calculate any random location beyond
	# 	the region, so it will calculate it for country, state, city. 
	##################################################################################################################################################################

	def add_locations(self, manager, level):
		locations = {}

		def add_random_location(random_val_start, hierarchy_level, locations):
			hierarchy_level_used = 'Location Hierarchy ' + str(hierarchy_level)
			country_random_val = self.random_val(0, len(self.location_countries[str(locations[hierarchy_level_used])]['Other'])-1)
			hierarchy_level_next = 'Location Hierarchy ' + str(hierarchy_level+1)
			locations[hierarchy_level_next] = self.location_countries[str(locations[hierarchy_level_used])]['Other'][country_random_val]

		if level <= 2:
			region_random_val = self.random_val(self.attributes['Location']['Minimum Generator'], self.attributes['Location']['Number Generator'])
			for val in self.attributes['Location']['Location Generator']:
				if region_random_val > self.attributes['Location']['Location Generator'][val]['Minimum'] and region_random_val <= self.attributes['Location']['Location Generator'][val]['Maximum']:
					locations['Location Hierarchy 1'] = val
			if locations['Location Hierarchy 1'] == "NA":
				country_random_val = self.random_val(0, 10)
				if country_random_val <= self.us_split:
					locations['Location Hierarchy 2'] = "United States"
				else:
					locations['Location Hierarchy 2'] = "Canada"
			else:
				country_random_val = self.random_val(0, len(self.location_regions[str(locations['Location Hierarchy 1'])])-1)
				locations['Location Hierarchy 2'] = self.location_regions[str(locations['Location Hierarchy 1'])][country_random_val]
			hq_random_val = self.random_val(1, 10)
			if (hq_random_val <= self.hq_split and self.location_countries[str(locations['Location Hierarchy 2'])]['HQ']) or len(self.location_countries[str(locations['Location Hierarchy 2'])]['Other']) == 0:
				locations['Location Hierarchy 3'] = self.location_countries[locations['Location Hierarchy 2']]['HQ']
			else:
				add_random_location(0, 2, locations)
			if self.location_countries.get(locations['Location Hierarchy 3']) is None:
				locations['Location Hierarchy 4'] = "" 
			else:
				hq_state_random_val = self.random_val(1, 10)
				if(hq_state_random_val <= self.hq_split and self.location_countries[str(locations['Location Hierarchy 3'])]['HQ']) or len(self.location_countries[str(locations['Location Hierarchy 3'])]['Other']) == 0:
					locations['Location Hierarchy 4'] = self.location_countries[locations['Location Hierarchy 3']]['HQ']
				else:
					add_random_location(0, 3, locations)
		else:
			remote_employee = self.random_val(1, 10)
			if remote_employee == 1 and level == len(self.hierarchy_vals)-1:
				remote_employee_random = self.random_val(0, len(self.remote_locations)-1)
				locations['Location Hierarchy 1'] = self.remote_locations[remote_employee_random]['Location Hierarchy 1']
				locations['Location Hierarchy 2'] = self.remote_locations[remote_employee_random]['Location Hierarchy 2']
				locations['Location Hierarchy 3'] = self.remote_locations[remote_employee_random]['Location Hierarchy 3']
				locations['Location Hierarchy 4'] = self.remote_locations[remote_employee_random]['Location Hierarchy 4']
			else:
				locations['Location Hierarchy 1'] = self.hierarchy_level_1[manager]
				locations['Location Hierarchy 2'] = self.hierarchy_level_2[manager]
				if locations['Location Hierarchy 2'] == "United States":
					locations['Location Hierarchy 3'] = self.hierarchy_level_3[manager]
				else:
					hq_random_val = self.random_val(1, 10)
					if (hq_random_val <= self.hq_split and self.location_countries[str(locations['Location Hierarchy 2'])]['HQ']) or len(self.location_countries[str(locations['Location Hierarchy 2'])]['Other']) == 0:
						locations['Location Hierarchy 3'] = self.location_countries[locations['Location Hierarchy 2']]['HQ']
					else:
						add_random_location(0, 2, locations)
				if self.location_countries.get(locations['Location Hierarchy 3']) is None:
					locations['Location Hierarchy 4'] = "" 
				else:
					hq_state_random_val = self.random_val(1, 10)
					if(hq_state_random_val <= self.hq_split and self.location_countries[str(locations['Location Hierarchy 3'])]['HQ']) or len(self.location_countries[str(locations['Location Hierarchy 3'])]['Other']) == 0:
						locations['Location Hierarchy 4'] = self.location_countries[locations['Location Hierarchy 3']]['HQ']
					else:
						add_random_location(0, 3, locations)
		return locations

	##################################################################################################################################################################
	# @add_gender : this will add the gender of the individual. This is based on a split from the attributes variable which can be adjusted as needed. 
	##################################################################################################################################################################

	def add_gender(self):
		gender_random = self.random_val(1, 10)
		if gender_random <= self.attributes['Gender']['Male']:
			return {
				"Gender" : self.attributes['Gender']['Attributes'][0]
			}
		else:
			return {
				"Gender" : self.attributes['Gender']['Attributes'][1]
			}

	##################################################################################################################################################################
	# @add_birth_date_and_generation : this will add the birth date and the generation based on specific splits in the attributes dictionary. This is based on 
	# information from our current clients for the splits which should be relatively accurate. It first does the random generation of the chance of the individual
	# falling into a specific generation and then based on that takes the minimum year for that generation and the max and generates the year, month and date which
	# is just using the random_val generator
	##################################################################################################################################################################

	def add_birth_date_and_generation(self):
		generation_random = self.random_val(1, 100)
		birth_year = int
		generation = str
		for generation in self.attributes['Birth Date']['Birth Year']['Generation']:
			if generation_random > generation['Minimum Generator'] and generation_random <= generation['Maximum Generator']:
				year_random = self.random_val(generation['Minimum Year'], generation['Max Year'])
				birth_year = year_random
				generation_name = generation['Generation Name']
		birth_month = self.random_val(self.attributes['Birth Date']['Birth Month']['Minimum Generator'], self.attributes['Birth Date']['Birth Month']['Number Generator'])
		birth_date = self.random_val(self.attributes['Birth Date']['Birth Date']['Minimum Generator'], self.attributes['Birth Date']['Birth Date']['Number Generator'])
		return {
			"Birth Date" : "{birth_month}/{birth_date}/{birth_year}".format(birth_date = birth_date, birth_month = birth_month, birth_year = birth_year),
			"Generation" : generation_name
		}

	##################################################################################################################################################################
	# @add_hire_date_and_tenure : this is going to add the hire date and the tenure to the dictionary which is inserted. This is able to generate it by first randomly
	# choosing a tenure from the attributes variable and then after choosing a tenure it chooses a value in the tenure's range and subtracts it from the current year. If
	# the person started the same year as the current year it only calculates the month up to the current month and not beyond. 
	##################################################################################################################################################################

	def add_hire_date_and_tenure(self):
		tenure_random = self.random_val(0, len(self.attributes['Hire Date']['Hire Year']['Tenure'])-1)
		years_at_company_random = self.random_val(self.attributes['Hire Date']['Hire Year']['Tenure'][tenure_random]['Minimum Year'], self.attributes['Hire Date']['Hire Year']['Tenure'][tenure_random]['Max Year'])
		now = datetime.datetime.now()
		start_year = now.year - years_at_company_random
		if start_year == now.year:
			start_month = self.random_val(self.attributes['Hire Date']['Hire Month']['Minimum Generator'], now.month)
		else:
			start_month = self.random_val(self.attributes['Hire Date']['Hire Month']['Minimum Generator'], self.attributes['Hire Date']['Hire Month']['Number Generator'])
		start_day = self.random_val(self.attributes['Hire Date']['Hire Day']['Minimum Generator'], self.attributes['Hire Date']['Hire Day']['Number Generator'])
		return {
			"Hire Date" : "{start_month}/{start_day}/{start_year}".format(start_day = start_day, start_month = start_month, start_year = start_year),
			"Tenure" : self.attributes['Hire Date']['Hire Year']['Tenure'][tenure_random]['Tenure Name']
		}

	##################################################################################################################################################################
	# @add_first_and_last_name : this adds the first and last name of the individual to the hierarchy based on the names csv file which is then passed to the names variable
	# We make sure the gender adds up based on the column in the csv and if it doesnt we rechoose another name based on the length of the csv
	##################################################################################################################################################################

	def add_first_and_last_name(self, gender):
		gender_is_incorrect = True
		while gender_is_incorrect:
			names_random = self.random_val(0, len(self.names)-1)
			random_gender_generated = self.names[names_random][2]
			if random_gender_generated == gender:
				return {
					"First Name" : self.names[names_random][0],
					"Last Name" : self.names[names_random][1][1:]
				}
				gender_is_incorrect = False

	def add_performance_rating_and_customer_satisfaction(self):
		performance_rating_random = self.random_val(0, 100)
		print performance_rating_random, self.PERFORMANCE_OPTIONS, self.PERFORMANCE_RATING
		performance_rating = (val[self.PERFORMANCE_RATING_NAME] for val in self.attributes[self.PERFORMANCE_RATING][self.PERFORMANCE_OPTIONS] if performance_rating_random > val[self.MINIMUM_GENERATOR] and performance_rating_random < val[self.NUMBER_GENERATOR])
		print performance_rating



	##################################################################################################################################################################
	# @print_results : this is going to print the results to a csv called hierarchy_csv
	##################################################################################################################################################################

	def print_results(self):
		with open('hierarchy.csv', 'w') as hierarchy_csv:
			header = ["ID", "First Name", "Last Name", "Department", "Position", "Level", "Sub-Department", "Manager", "Location Hierarchy 1", "Location Hierarchy 2", "Location Hierarchy 3", "Location Hierarchy 4", "Gender", "Birth Date", "Generation", "Hire Date", "Tenure"]
			writer = csv.DictWriter(hierarchy_csv, fieldnames=header)
			writer.writeheader()
			for line in self.hierarchy:
				writer.writerow({'ID': line['ID'], 
					'First Name' : line['First Name'],
					'Last Name' : line['Last Name'],
					'Department': line['Department'], 
					'Position': line['Position'], 
					'Level': line['Level'],
					'Sub-Department': line['Sub-Department'],
					'Manager': line['Manager'],
					'Location Hierarchy 1': line['Location Hierarchy 1'],
					'Location Hierarchy 2': line['Location Hierarchy 2'],
					'Location Hierarchy 3': line['Location Hierarchy 3'],
					'Location Hierarchy 4': line['Location Hierarchy 4'],
					'Gender': line['Gender'],
					'Birth Date' : line['Birth Date'],
					'Generation' : line['Generation'],
					'Hire Date' : line['Hire Date'],
					'Tenure' : line['Tenure']})


data = Data()
data.create_structure() 
data.pull_names()
data.define_hierarchy()
data.print_results()