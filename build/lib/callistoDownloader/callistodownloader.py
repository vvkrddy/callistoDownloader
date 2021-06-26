import requests
import os
import urllib.request
from bs4 import BeautifulSoup
import datetime


url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'

def years():
	"""
	Returns those years for which data is available

	Parameters
	----------

	Returns
	-------
	list
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
	Returns those years for which data is available

	Parameters
	----------
	select_year: int

	Returns
	-------
	list
		a list of strings representing the months for which data is available in the given year
	"""


	# errors handling
	assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
	
	# if this function returns None, then it means there is no data for the year
	
	select_year_str = str(select_year)
	while True:
		try:
			if(select_year_str in years()):
				break
		except:
		# executed if years() hasn't been called before
			return None
			
	# following code is executed only if break occurs in the if conditions above
	url_year = url + select_year_str + '/'
	page = requests.get(url_year)
	soup = BeautifulSoup(page.content, 'html.parser')
	months = []
	for i in range(len(soup.find_all('a'))-5):
		months.append(soup.find_all('a')[5+i].get_text()[0:-1])
		
	return months 


def days(select_year, select_month):
	"""
	Returns those days for which data is available in the given month and year

	Parameters
	----------
	select_year: int
	select_month: int
	
	Returns
	-------
	list
		a list of strings representing the days for which data is available in the given month and year
	"""

	# errors handling
	assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
	assert (select_month >= 1 and select_month <=12 and type(select_month) == int), "Month must be a valid number."
	if(datetime.date.today().year == select_year):
		assert (datetime.date.today().month >= select_month), "The month has not yet occurred"

	# if this function returns None, then it means there is no data for the month in a given year
	
	if select_month < 10:
		select_month_str = '0'+str(select_month)
	else:
		select_month_str = str(select_month)
	select_year_str = str(select_year)
	
	while True:
		try:
			if(select_month_str in months(select_year)):
				break
			else:
				# when the given year doesn't have data for the given month
				return None
		except:
			# when the given year doesn't have any data 
			return None
		
	url_month = url + select_year_str + '/' + select_month_str + '/'
	page = requests.get(url_month)
	soup = BeautifulSoup(page.content, 'html.parser')
	days = []
	
	for i in range(len(soup.find_all('a'))-5):
		days.append(soup.find_all('a')[5+i].get_text()[0:-1])

	return days

def read_instruments():
	url

def which_years():
	for i in years():
		print(i,end="\t")
	print("\n")	

def which_months(select_year):
	for i in months(select_year):
		print(i,end="\t")
	print("\n")	

def which_days(select_year, select_month):
	for i in days(select_year, select_month):
		print(i,end='\t')
	print("\n")	

ALL = 'ALL'

def download(select_year, select_month, select_days, instruments):
	"""
	Downloads files from list of instruments for given list of days of a given month and year

	if select_days = ALL, data is downloaded for all the days of the given year and given month for the given list of instruments

	if select_month = ALL, select_days argument is ignored (but still required; pass a random value) and data is downloaded for all the months of the given year for the given list of instruments  

	Parameters
	----------
	select_year: int
	select_month: int or keyword ALL
	select_days: int or list of int or keyword ALL
	instruments: str or list of str 

	Returns
	-------

	Prints
	-------

	"""


	if(select_days != ALL and select_months != ALL):
		if(type(select_days) != list):
			select_days = [int(str(select_days))] 
		if(type(instruments) != list):
			instruments = [str(instruments)] 

		# errors handling
		assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
		assert (select_month >= 1 and select_month <=12 and type(select_month) == int), "Month must be a valid number."
		for instrument in instruments:
			assert (type(instrument) == str), "Instruments must be a string or list of strings"
		for d in select_days:
			assert (type(d) == str), "Days must be an integer or list of integers"


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

			# errors handling
			try:
				select_date = datetime.date.fromisoformat('{}-{}-{}'.format(select_year_str, select_month_str, d_str))
			except:
				print("{}-{}-{} Date is invalid".format(select_year_str, select_month_str, d_str))
				continue
			
			if(select_date > datetime.date.today()):
				print("{}-{}-{} The date has not yet occurred".format(select_year_str, select_month_str, d_str))
				continue

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
	

	elif(select_month == ALL):

		# errors handling
		assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
		for instrument in instruments:
			assert (type(instrument) == str), "Instruments must be a string or list of strings"

		select_month = which_months(select_year)

		for m in select_month:

			select_days = which_days(select_year, m)

			select_year_str = str(select_year)
			
			for d in select_day:


				# errors handling
				try:
					select_date = datetime.date.fromisoformat('{}-{}-{}'.format(select_year_str, m_str, d_str))
				except:
					print("{}-{}-{} Date is invalid".format(select_year_str, m_str, d_str))
					continue
				
				if(select_date > datetime.date.today()):
					print("{}-{}-{} The date has not yet occurred".format(select_year_str, m_str, d_str))
					continue

				url_day = url + select_year_str + '/' + m_str + '/' + d_str + '/'
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
									if not os.path.isdir('e-Callisto/{}/{}/{}'.format(select_year_str,m_str,d_str)):
										os.makedirs('e-Callisto/{}/{}/{}'.format(select_year_str,m_str,d_str))
									counter += 1
									if(os.path.exists('e-Callisto/{}/{}/{}/{}'.format(select_year_str,m_str,d_str,fname))):
										continue
									urllib.request.urlretrieve(url_day+fname, 'e-Callisto/{}/{}/{}/{}'.format(select_year_str,m_str,d_str,fname)) 

							print('{}-{}-{} {} files downloaded'.format(select_year_str, m_str, d_str, instrument))
						else:
							print('{}-{}-{}'.format(select_year_str,m_str,d_str), 'No', instrument, 'data for the date')
				else:
					print('{}-{}-{}'.format(select_year_str,m_str,d_str), 'No data for the date')

	

	elif(select_days == ALL and select_month != ALL):

		# errors handling
		assert (len(str(select_year)) == 4 and type(select_year) == int), "Year must be a 4-digit integer."
		assert (select_month >= 1 and select_month <=12 and type(select_month) == int), "Month must be a valid number."
		for instrument in instruments:
			assert (type(instrument) == str), "Instruments must be a string or list of strings"

		select_days = which_days(select_year, select_month)


		if select_month < 10:
			select_month_str = '0'+str(select_month)
		else:
			select_month_str = str(select_month)
		select_year_str = str(select_year)
		
		for d in select_days:

			# errors handling
			try:
				select_date = datetime.date.fromisoformat('{}-{}-{}'.format(select_year_str, select_month_str, d_str))
			except:
				print("{}-{}-{} Date is invalid".format(select_year_str, select_month_str, d_str))
				continue
			
			if(select_date > datetime.date.today()):
				print("{}-{}-{} The date has not yet occurred".format(select_year_str, select_month_str, d_str))
				continue

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



