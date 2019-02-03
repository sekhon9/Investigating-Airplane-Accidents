#importing math and csv libraries
import csv
import math

#importing OrderedDict class from collections
from collections import OrderedDict

#reading in AviationData.txt as a 2D list
f = open('AviationData.txt','r',encoding='utf-8')
csvreader = csv.reader(f, delimiter='\n')
aviation_data = [row for row in csvreader]

#splitting each row in the aviation_data list by " | "
aviation_list = []
for row in aviation_data:
	aviation_list.append(row[0].split(' | ')[:-1])

#finding 'LAX94LA336' in aviation_list and appending rows where 'LAX94LA336' is an element to the lax_code list
lax_code = []
for row in aviation_list:
	for element in row:
		if element == 'LAX94LA336':
			lax_code.append(row)

#Above search was not very time efficient(exponential time efficiency).
#It had to go through each row in the list and then each element in that row to find 'LAX94LA336'.

#linear search algorithm for LAX94LA336'
lax_code = []
for row in aviation_list:
	if row[2] == 'LAX94LA336':
		lax_code.append(row)

#you'd have to know the column in which 'LAX94LA336' exists before had for this algorithm to work

#logarithmic search algorithm for LAX94LA336'
lax_code = []
aviation_list[1:] = sorted(aviation_list[1:], key=lambda l:l[2])
upper_bound = len(aviation_list)-1
lower_bound = 0
index = math.floor((upper_bound+lower_bound)/2)
guess = aviation_list[index][2]
while 'LAX94LA336' != guess:
	if 'LAX94LA336' < guess:
		upper_bound = index - 1
	else:
		lower_bound = index + 1
	index = math.floor((upper_bound+lower_bound)/2)
	guess = aviation_list[index][2]
if 'LAX94LA336' == guess:
	lax_code.append(aviation_list[index])

#In addition to knowing in which column 'LAX94LA336' exists, 
#you'd have to sort the list by the 'LAX94LA336' column for the above algorithm to work

#Creating a list of dictionaries with dictionary keys as column names to store aviation_data 2D list
aviation_dict_list = []
aviation_columns = aviation_data[0][0].split(' | ')[:-1]
for row in aviation_data[1:]:
	split_row = row[0].split(' | ')[:-1]
	row_dict = OrderedDict()
	for i in range(len(aviation_columns)):
		try:	
			row_dict[aviation_columns[i]] = split_row[i]
		except:
			row_dict[aviation_columns[i]] = ''
	aviation_dict_list.append(row_dict)


lax_dict = []
for row in aviation_dict_list:
	for value in row.values():
		if value == 'LAX94LA336':
			lax_dict.append(row)

#Creating a list of dicts provides more structure than list of lists, but the downside is lower space efficiency

#Using aviation_dict_list to find the US state with the highest number of flight accidents
state_accidents = {}
state = aviation_dict_list[0]['Location'].split(', ')[1]
state_accidents[state] = 1
for row in aviation_dict_list[1:]:
	if ', ' in row['Location'] and row['Country'] == 'United States':
		state = row['Location'].split(', ')[1]
		if state in state_accidents:
			state_accidents[state] += 1
		else:
			state_accidents[state] = 1
state_accidents = dict(sorted(state_accidents.items(), key=lambda x:x[1], reverse=True))
print('State with the highest no. of flight accidents: ',max(state_accidents, key=state_accidents.get))

#replacing all blank values in fatal and serious injuries with 0
for row in aviation_dict_list:
	if row['Total Fatal Injuries'] == '':
		row['Total Fatal Injuries'] = 0
	if row['Total Serious Injuries'] == '':
		row['Total Fatal Injuries'] = 0

#calculating total fatal and serious injuries by month and year
months_years = []
injury_counts = []
for row in aviation_dict_list:
	if row['Event Date'] != '':	
		injury_count = int(row['Total Fatal Injuries']) + int(row['Total Fatal Injuries'])
		month_year = (row['Event Date'].split('/')[0], row['Event Date'].split('/')[2])
		if month_year not in months_years:
			months_years.append(month_year)
			injury_counts.append(injury_count)
		else:
			injury_counts[months_years.index(month_year)] += injury_count
print('Injuries due to aviation accidents by month/year:')
for month_year in months_years:
	print('{0}/{1}: {2}'.format(month_year[0], month_year[1], injury_counts[months_years.index(month_year)]))
print('Total: ',sum(injury_counts))