from BeautifulSoup import BeautifulSoup as Soup
import urllib
import mechanize
import getpass
import cookielib
import time
import json
import csv
import glob
import os


br = mechanize.Browser()
cj = cookielib.LWPCookieJar()

def setup_browser():
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def download_classes():
	response = br.open("http://offices.depaul.edu/student-records/schedule-of-classes/Pages/default.aspx")
	
	br.select_form(nr=0)
	control = br.form.find_control('ctl00$ctl29$g_49ceed09_b59e_4457_94a1_a9ea1bd8a6c6$ctl00$ddTerm')
	control.value = ['0965'] #Winter Quarter
	br.submit()

	html = br.response().read()
	soup = Soup(html)

	courses = []

	downloaded = 1

	with open('classes.json','w') as output:

		for ul in soup.findAll('ul',{'class':'columnlist medium'}):
			a = ul.findAll('a')
			for i in a:
				url = 'http://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=getclasses'
				start = i['href'].rindex('?dtl=Y') + 6

				html = urllib.urlopen(i['href'])
				soup = Soup(html)
				course_description = soup.find('p',{'class':'nopadding-top'}).text

				html = urllib.urlopen(url+i['href'][start:])
				data = json.loads(str(Soup(html)))

				print 'Downloaded ' + str(downloaded) + ' url'
				downloaded+=1
				courses.append([i.text,course_description,data])

		json.dump(courses, output)
		format_classes()

def format_classes():
	headers = ['Credit Hours', 'Teacher First Name', 'Teacher Last Name', 'Class Start Time', 'Class End Time', 'Class Section', 'Class Number', 'Location', 'Days']

	with open('classes.json','r') as input:
		class_data = json.load(input)
		for i in range(len(class_data)):

			class_name = str(class_data[i][0])
			class_description = str(class_data[i][1])
			array_of_class_data = []

			for j in range(len(class_data[i][2])):
				days = [0,0,0,0,0,0,0]
				for key, value in class_data[i][2][j].iteritems():
					if key.strip().lower() == 'units_minimum':
						credit_hours = str(value)
					if key.strip().lower() == 'first_name':
						if len(value) == 0: 
							teacher_first_name = 'Staff'
						else:
							teacher_first_name = str(value)
					if key.strip().lower() == 'last_name':
						if len(value) == 0: 
							teacher_last_name = 'Staff'
						else:
							teacher_last_name = str(value)
					if key.strip().lower() == 'meeting_time_start':
						class_start_time = str(value).replace('1/1/1900 ','').replace(':00 ',' ')
					if key.strip().lower() == 'meeting_time_end':
						class_end_time = str(value).replace('1/1/1900 ','').replace(':00 ',' ')
					if key.strip().lower() == 'class_section':
						class_section = str(value)
					if key.strip().lower() == 'class_nbr':
						class_number = str(value)
					if key.strip().lower() == 'location_descr':
						class_location = str(value)

					if key.strip().lower() == 'mon' and value.strip().lower() == 'y':
						days[0] = 'Monday'
					if key.strip().lower() == 'tues' and value.strip().lower() == 'y':
						days[1] = 'Tuesday'
					if key.strip().lower() == 'wed' and value.strip().lower() == 'y':
						days[2] = 'Wednesday'
					if key.strip().lower() == 'thurs' and value.strip().lower() == 'y':
						days[3] = 'Thursday'
					if key.strip().lower() == 'fri' and value.strip().lower() == 'y':
						days[4] = 'Friday'
					if key.strip().lower() == 'sat' and value.strip().lower() == 'y':
						days[5] = 'Saturday'
					if key.strip().lower() == 'sun' and value.strip().lower() == 'y':
						days[6] = 'Sunday'

				days = filter(lambda a: a != 0, days)
				days =','.join(days)

				array_of_class_data.append([credit_hours,teacher_first_name,teacher_last_name,class_start_time,class_end_time,class_section,class_number,class_location,days])
			with open('class_data/'+ class_name.replace('/','').replace(';','') +'.csv','w') as formatted_class:
				writer = csv.writer(formatted_class)
				writer.writerow([class_name])
				writer.writerow([class_description])
				writer.writerow(headers)

				for row in array_of_class_data:
					writer.writerow(row)

def create_webpage(filename):
	with open(filename,'r') as class_data:
		reader = csv.reader(class_data)
		info = list(reader)

		title = info[0][0]
		course_description = info[1][0]
		tags = []

		html = '<!DOCTYPE html><html><head><title>'+title+'</title><link rel="stylesheet" type="text/css" href="../stylesheet.css"></head>'
		html += '<h1>'+title+'</h1><body>'+course_description+'<h2>Available Classes</h2><table class="bordered">'
		html+='<thead><tr>'
		for i in info[2]:
			tags.append(i)
			html+='<th>' + i + '</th>'
		html+=' </tr></thead>'
		
		for i in info[3:]:
			html+='<tr>'
			for j in i:
				tags.append(j)
				html+='<td>' + j + '</td>'
			html+=' </tr>'

		with open('classes/'+title.replace(' ','-').replace('/','').replace(';','')+'.html','w') as output:
			output.write(html)

		tags = list(set(tags))
		tags = filter(None, tags)
		return [title, course_description,tags,('classes/'+title.replace(' ','-').replace('/','').replace(';','')+'.html')]

def create_all_webpages():
	files = []
	for file in os.listdir("class_data"):
		if file.endswith("csv"): 
			files.append(file)
	to_be_indexed = []

	for i in files:
		to_be_indexed.append(create_webpage('class_data/'+i))

	send_to_be_indexed(to_be_indexed)


def send_to_be_indexed(items):

	with open('tipuesearch/tipuesearch_content.js','w') as output:
		output.write('var tipuesearch = {"pages": [\n')
		for i in items:
			title = '""'
			text = '""'
			tags ='""'
			url = '""'

			if i[0]:
				title = '"{0}"'.format(i[0].replace("\"",'').replace("\r\n",'').replace("\n",''))
			if i[1]:
				text = '"{0}"'.format(i[1][:300].replace("\"",'').replace("\r\n",'').replace("\n",''))
			if i[2]:
				tags = ', '.join('{0}'.format(j) for j in set(i[2]))
				tags = '"{0}"'.format(tags.replace("\"",'').replace("\r\n",'').replace("\n",''))
			if i[3]:
				url = '"{0}"'.format(i[3].replace("\"","\'"))

			output.write('{"title":'+ title +',"text":'+ text +',"tags":'+ tags +',"url": '+url+'},\n')
		output.write(']};')


def main():
	download_classes()
	format_classes()
	create_all_webpages()


if __name__ == '__main__':
	main()
