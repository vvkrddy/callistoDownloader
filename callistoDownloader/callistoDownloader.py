import requests
import os
import urllib.request
from bs4 import BeautifulSoup
import regex as re
import datetime
import numpy as np


url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'

def years():
	"""

	Returns those years for which any data (irrespective of instruments) is available. 

	Parameters
	----------

	Returns
	-------
	years : list
		a list of strings representing the years for which data is available

	"""

	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	years = []
	for i in range(len(soup.find_all('a'))-6):
		years.append(soup.find_all('a')[5+i].get_text()[0:-1])

	return years


def months(select_year):
	"""

	Returns those months for which any data (irrespective of instruments) is available, in the specified year.
	
	Parameters
	----------
	select_year: 
		int

	Returns
	-------
	months : list
		a list of strings representing the months for which data is available in the given year

	"""

	# error handling
	assert (len(str(select_year)) == 4 and type(select_year) == int), "The only argument year must be a 4-digit integer."
	#

	select_year_str = str(select_year)
	
	# data unavailability
	assert (select_year_str in years()), "The specified year {} doesn't have any data".format(select_year)
	#
		
	url_year = url + select_year_str + '/'
	page = requests.get(url_year)
	soup = BeautifulSoup(page.content, 'html.parser')
	months = []

	for i in range(len(soup.find_all('a'))-5):
		months.append(soup.find_all('a')[5+i].get_text()[0:-1])
		
	return months 


def days(select_year, select_month):
	"""

	Returns those days for which any data (irrespective of instruments) is available, in the specified month and year.

	Parameters
	----------
	select_year: 
		int
	select_month: 
		int
	
	Returns
	-------
	days : list
		a list of strings representing the days for which data is available in the given month and year

	"""

	# error handling
	assert (len(str(select_year)) == 4 and type(select_year) == int), "First argument year must be a 4-digit integer"
	assert (type(select_month) == int), "Second argument month must be a valid integer"
	assert (select_month >= 1 and select_month <=12), "Second argument month must be a valid integer"
	if(datetime.date.today().year == select_year):
		assert (datetime.date.today().month >= select_month), "The month {} in {} has not yet occurred".format(select_month, select_year)
	assert (datetime.date.today().year > select_year), "The year {} has not yet occurred".format(select_year)
	# 

	if select_month < 10:
		select_month_str = '0'+str(select_month)
	else:
		select_month_str = str(select_month)
	select_year_str = str(select_year)
	
	# data unavaiability
	assert (select_year_str in years()), "The specified year {} doesn't have any data".format(select_year)
	assert (select_month_str in months(select_year)), "The specified month {} in {} doesn't have any data".format(select_month, select_year)
	#

	url_month = url + select_year_str + '/' + select_month_str + '/'
	page = requests.get(url_month)
	soup = BeautifulSoup(page.content, 'html.parser')
	days = []
	
	for i in range(len(soup.find_all('a'))-5):
		days.append(soup.find_all('a')[5+i].get_text()[0:-1])

	return days


def which_years():
	"""

	Prints those years for which any data (irrespective of instruments) is available. 

	Parameters
	----------

	Returns
	-------
	None

	"""

	for i in years():
		print(i,end="\t")
	print("\n")	

def which_months(select_year):
	"""

	Prints those months for which any data (irrespective of instruments) is available, in the specified year.
	
	Parameters
	----------
	select_year: 
		int

	Returns
	-------
	None

	"""

	for i in months(select_year):
		print(i,end="\t")
	print("\n")	

def which_days(select_year, select_month):
	"""

	Prints those days for which any data (irrespective of instruments) is available, in the specified month and year.

	Parameters
	----------
	select_year: 
		int
	select_month: 
		int
	
	Returns
	-------
	None

	"""

	for i in days(select_year, select_month):
		print(i,end='\t')
	print("\n")	

def instrument_codes():
	"""

	Instrument codes are codes derived specifically for this package 
	and each code corresponds to one of the instrument-location combination 
	from link http://soleil.i4ds.ch/solarradio/data/readme.txt.

	If the file name is BLEN5M_20090411_100001_58.fit.gz;
	then the instrument code is the characters before the first underscore,
	which in this case is BLEN5M.

	This will download all spectrograms from all antenna types at Blein, Switzerland.

	OR

	From the http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/
	you can choose to visit the webpage of a particular day, say January 01, 2021;

	The particular webpage for the day is http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2021/01/01/

	Suppose, you would want to download files from ALASKA-ANCHORAGE files, 
	then use the instrument code 'ALASKA-ANCHORAGE' as the fourth parameter in the download() function.


	Parameters
	----------

	Returns
	-------
	INSTRUCTIONS

	"""

	s = "http://soleil.i4ds.ch/solarradio/data/readme.txt"
	print("Visit "+s)
	
	print("If the file name is BLEN5M_20090411_100001_58.fit.gz; \
		\nthen the instrument code is the characters before the first underscore.\
		\nwhich in this case is BLEN5M\
		\n\nThis will download all spectrograms from all antenna types at Blein, Switzerland")



def download(select_year, select_month, select_day, instruments):
	"""

	Downloads files for set of instruments for given date.
	The instruments can be a single instrument ID string or a wildcard string.


	Parameters
	----------
	select_year: int
	select_month: int 
	select_day: int 
	instruments: 
		str 

	Returns
	-------
	None

	"""

	assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
	assert (select_month >= 1 and select_month <=12 and type(select_month) == int), "Month must be a valid number."
	assert (select_day >= 1 and select_day <=31 and type(select_day) == int), "Day must be a valid number."
	assert (type(instruments) == str), "Fourth parameter must be a string: either an instrument ID or a wildstring."
	
	if select_month < 10:
			select_month_str = '0'+str(select_month)
	else:
		select_month_str = str(select_month)
	select_year_str = str(select_year)

	if select_day < 10:
		select_day_str = '0'+str(select_day)
	else:
		select_day_str = str(select_day)

	# date error handling 
	try:
		select_date = datetime.date.fromisoformat('{}-{}-{}'.format(select_year_str, select_month_str, select_day_str))
	except:
		raise ValueError("{}-{}-{} Date is invalid".format(select_year_str, select_month_str, d_str)) from None
	assert (select_date < datetime.date.today()), "{}-{}-{} The date has not yet occurred".format(select_year_str, select_month_str, select_day_str)

	url_day = url + select_year_str + '/' + select_month_str + '/' + select_day_str + '/'
	page = requests.get(url_day)
	soup = BeautifulSoup(page.content, 'html.parser')

	# assert '404 Not Found' in soup, '{}-{}-{} No data for the date'.format(select_year_str,select_month_str,select_day_str)

	soup_list = list(soup.find_all('a'))
	
	assert len(soup_list) != 0, '{}-{}-{} No datdda for the date'.format(select_year_str,select_month_str,select_day_str)
	
	all_files = [re.search(r'href="(.*?)"', str(i)).group(1) for i in soup_list \
				if '.fit.gz' in re.search(r'href="(.*?)"', str(i)).group(1)]
	unique_ID = np.unique([i.split('_')[0] for i in all_files]) 


	
	if(instruments not in unique_ID and '*' not in instruments):
		print('No data found for the instrument ID {} on the asked date {}-{}-{}'.format(instruments,select_year_str,select_month_str,select_day_str))
	
	elif(instruments in unique_ID):
		
		counter = 0
		if(sum(instruments in s for s in all_files) > 0):
			print("{} files will be downloaded.".format(sum(instruments in s for s in all_files)))
			for fname in all_files:
				if(n.split('_')[0] == 'instruments'):
					if not os.path.isdir('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str)):
						os.makedirs('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str))
					counter += 1
					if(os.path.exists('e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str,fname))):
						continue
					urllib.request.urlretrieve(url_day+fname, 'e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str,fname)) 

			print('{}-{}-{} {} filsdfes downloaded'.format(select_year_str, select_month_str, select_day_str, instrument))
		
		# no else statement since the instrument is checked in unique_ID before

	elif("*" in instruments):
		
		counter = 0
		if(sum(instruments[:-1] in s for s in all_files) > 0):
			print("{} files will be downloaded.".format(sum(instruments[:-1] in s for s in all_files)))
			for fname in all_files:
				if(fname.startswith(instruments[:-1])):
					if not os.path.isdir('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str)):
						os.makedirs('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str))
					counter += 1
					if(os.path.exists('e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str,fname))):
						continue
					urllib.request.urlretrieve(url_day+fname, 'e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,select_day_str,fname)) 

			print('{}-{}-{} {} files downloaded'.format(select_year_str, select_month_str, select_day_str, instruments))
		
		else:
			print("0 files found with starting string {}".format(instruments[:-1]))