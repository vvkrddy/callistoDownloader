import requests
import os
import urllib.request
from bs4 import BeautifulSoup
import datetime


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

	Prints all instrument codes.

	Instrument codes are codes derived specifically for this package 
	and each code corresponds to one of the instrument-location combination 
	from `link <http://soleil.i4ds.ch/solarradio/data/readme.txt>`.

	Parameters
	----------

	Returns
	-------
	None

	"""


def download(select_year, select_month, select_day, instruments):
	"""

	Downloads files for list of instruments from given list of days of a given month and year

	if select_day = 'ALL', data is downloaded for all the days of the given year and given month for the given list of instruments

	Parameters
	----------
	select_year: int
	select_month: int 
	select_day: 
		int 
		list of int 
		'ALL'
	instruments: 
		str
		list of str 

	Returns
	-------
	None

	"""

	if(select_day != 'ALL'):

		if(type(select_day) != list):
			select_day = [int(str(select_day))] 
		if(type(instruments) != list):
			instruments = [str(instruments)] 

		# error handling
		assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
		assert (select_month >= 1 and select_month <=12 and type(select_month) == int), "Month must be a valid number."
		for instrument in instruments:
			assert (type(instrument) == str), "Instruments must be a string or list of strings"
		for d in select_day:
			assert (type(d) != str), "Days must be an integer or list of integers"
		#

		if select_month < 10:
			select_month_str = '0'+str(select_month)
		else:
			select_month_str = str(select_month)
		select_year_str = str(select_year)
		
		for d in select_day:

			if d < 10:
				d_str = '0'+str(d)
			else:
				d_str = str(d)

			# error handling
			try:
				select_date = datetime.date.fromisoformat('{}-{}-{}'.format(select_year_str, select_month_str, d_str))
			except:
				raise ValueError("{}-{}-{} Date is invalid".format(select_year_str, select_month_str, d_str)) from None
			assert (select_date < datetime.date.today()), "{}-{}-{} The date has not yet occurred".format(select_year_str, select_month_str, d_str)
			#

			url_day = url + select_year_str + '/' + select_month_str + '/' + d_str + '/'
			page = requests.get(url_day)
			soup = BeautifulSoup(page.content, 'html.parser')

			if('404 Not Found' not in soup):
			# print(url)

				counter = 0
				for instrument in instruments:	
					if(str(soup).count(instrument) > 0):
						for n in range(len(soup.find_all('a'))-5):
							if(instrument in soup.find_all('a')[5+n].get_text()):
								fname = soup.find_all('a')[5+n].get_text()
								print(url_day+fname)
								if not os.path.isdir('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,d_str)):
									os.makedirs('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,d_str))
								counter += 1
								if(os.path.exists('e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,d_str,fname))):
									continue
								urllib.request.urlretrieve(url_day+fname, 'e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,d_str,fname)) 

						print('{}-{}-{} {} files downloaded'.format(select_year_str, select_month_str, d_str, instrument))
					else:
						print('{}-{}-{}'.format(select_year_str,select_month_str,d_str), 'No', instrument, 'data for the date')
			else:
				print('{}-{}-{}'.format(select_year_str,select_month_str,d_str), 'No data for the date')
	

	elif(select_day == 'ALL'):

		if(type(instruments) != list):
			instruments = [str(instruments)] 

		# error handling
		assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
		assert (select_month >= 1 and select_month <=12 and type(select_month) == int), "Month must be a valid number."
		for instrument in instruments:
			assert (type(instrument) == str), "Instruments must be a string or list of strings"
		#

		select_day = which_days(select_year, select_month)

		if select_month < 10:
			select_month_str = '0'+str(select_month)
		else:
			select_month_str = str(select_month)
		select_year_str = str(select_year)
		
		for d in select_day:


			# error handling
			try:
				select_date = datetime.date.fromisoformat('{}-{}-{}'.format(select_year_str, select_month_str, d_str))
			except:
				print("{}-{}-{} Date is invalid".format(select_year_str, select_month_str, d_str))
			assert (select_date < datetime.date.today()), "{}-{}-{} The date has not yet occurred".format(select_year_str, select_month_str, d_str)
			#

			url_day = url + select_year_str + '/' + select_month_str + '/' + d_str + '/'
			page = requests.get(url_day)
			soup = BeautifulSoup(page.content, 'html.parser')

			if('404 Not Found' not in soup):
			# print(url)

				counter = 0
				for instrument in instruments:	
					if(str(soup).count(instrument) > 0):
						for n in range(len(soup.find_all('a'))-5):
							if(instrument in soup.find_all('a')[5+n].get_text()):
								fname = soup.find_all('a')[5+n].get_text()
								print(url_day+fname)
								if not os.path.isdir('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,d_str)):
									os.makedirs('e-Callisto/{}/{}/{}'.format(select_year_str,select_month_str,d_str))
								counter += 1
								if(os.path.exists('e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,d_str,fname))):
									continue
								urllib.request.urlretrieve(url_day+fname, 'e-Callisto/{}/{}/{}/{}'.format(select_year_str,select_month_str,d_str,fname)) 

						print('{}-{}-{} {} files downloaded'.format(select_year_str, select_month_str, d_str, instrument))
					else:
						print('{}-{}-{}'.format(select_year_str,select_month_str,d_str), 'No', instrument, 'data for the date')
			else:
				print('{}-{}-{}'.format(select_year_str,select_month_str,d_str), 'No data for the date')



