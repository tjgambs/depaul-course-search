# -*- coding: UTF-8 -*-

#Created by Timothy Gamble
#tjgambs@gmail.com

import urllib
import json
import csv

#The id number of your school can be found in the ratemyprofessor link. For example
#the link of a universities page might look like this: 
#		http://www.ratemyprofessors.com/campusRatings.jsp?sid=1389
#The universities id number would be 1389, the number following 'sid='.
school_id_number = '1389'

#Please specify how many teachers you want in your data set. You can have all of 
#them if you enter in 'all' or you can enter in a number with in quotations.
#	Either this: how_many_teachers = '10'
#	or this: how_many_teachers = 'all'
how_many_teachers = 'all' 

#Write true next to the items you want to have and false to the items you do not want.
teacher_id 			= True
teacher_profile			= True
teacher_first_name 		= True
teacher_last_name 		= True
number_of_ratings 		= True
overall_rating 			= True
helpfulness_rating 		= True
clarity_rating 			= True
easiness_rating 		= True


#Creates a url with the predefined url parameters.
def generate_url():
	url ='http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=10&callback=jQuery111003276446736417711_1446762506495&q=*%3A*+AND+schoolid_s%3A' + school_id_number + '&defType=edismax&qf=teacherfullname_t%5E1000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=&siteName=rmp&rows='	
	
	#Adds the amount of teachers wanted to a url paramater
	if(how_many_teachers.lower() == 'all'):
		url += total_teachers() + '&start=0&fl='
	else:
		url += how_many_teachers + '&start=0&fl='

	#Adds the url parameters as specified above
	if(teacher_id):
		url += 'pk_id+'
	if(teacher_first_name):
		url += 'teacherfirstname_t+'
	if(teacher_last_name):
		url += 'teacherlastname_t+'
	if(number_of_ratings):
		url += 'total_number_of_ratings_i+'
	if(overall_rating):
		url += 'averageratingscore_rf+'
	if(helpfulness_rating):
		url += 'averagehelpfulscore_rf+'
	if(clarity_rating):
		url += 'averageclarityscore_rf+'
	if(easiness_rating):
		url += 'averageeasyscore_rf+'
	if(url[-1] == '+'): 
		url = url[:-1]

	return url


#Takes the url generated and takes all of the data to be formatted.
def gather_data():
	url = generate_url()
	#Formats the data to be used in a list
	page_content = urllib.urlopen(url).read()
	begin = page_content.index('"docs":')+7

	#Characters with accents screwing everything up
	page = page_content[begin:-5].replace('í','i') 
	data = json.loads(page)

	#Creates a url for each professor, this is where all of the student reviews can be found
	for key in data:
		key['teacher_profile'] = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='+ str(key['pk_id'])
		key['univerity_id'] = str(school_id_number)
	
	return data


#Totals all of the teachers that are associated with the specified university
def total_teachers():
	url = 'http://search.mtvnservices.com/typeahead/suggest/?callback=jQuery11100050687990384176373_1446754108140&q=*:*+AND+schoolid_s:' + school_id_number + '&siteName=rmp'
	page_content = urllib.urlopen(url).read()

	begin = page_content.index('"numFound":')+11
	end = page_content.index(',"start":')

	return page_content[begin:end]


#Takes all of the data and stores it in a csv called teachers.csv
def export_to_csv():
	data = gather_data()
	keys = data[0].keys()

	with open('teachers.csv', 'wb') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(data)


def main():
	export_to_csv()


if __name__ == '__main__':
	main()
	
