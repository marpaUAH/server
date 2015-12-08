# Import Regexp (re) and urlib2 and datetime
import re
import requests, urllib, urllib2
import datetime
import pdb

# Import MongoDB object
from app import db, lnumbers

# Import from Beebotte
from beebotte import *

# Beebotte object declaration
bclient = BBT('db26c05fa32d1ca054eaf60350914ff9','aa18e56f716b597b2fc0a33bbbdc4dc2d32aff0731edb3bc391fe1282c07f10e')

# Give format to the date
def format_date(sdate):
	d = sdate[0:2]
	m = sdate[2:4]
	y = sdate[4:8]
	return y+'-'+m+'-'+d

def raw_date(sdate):
	return int(sdate[0:4]+sdate[5:7]+sdate[8:10])

# Clean the list in order to get a list on the following form: (date(yyyy-mm-dd), number, serie)
def clean_list(l_num):

	clist = []
	tmp_n = ''
	i = 0

	while len(l_num) != 0:
		if i % 8 == 0:
			clist.append(format_date(l_num.pop(0)))
		elif i % 8 == 1:
			l_num.pop(0)
		elif (i % 8 >= 2) and (i % 8 <= 6):
			if len(tmp_n) == 0:
				tmp_n += l_num.pop(0)
			elif len(tmp_n) < 4:
				tmp_n += l_num.pop(0)
			elif len(tmp_n) == 4:
				tmp_n += l_num.pop(0)
				clist.append(tmp_n)
				tmp_n = ''
		elif i % 8 == 7:
			clist.append(l_num.pop(0))
		i+=1
	
	return clist

# Get HTML code from 2013, 2014 and 2015 numbers
sites = ('2013', '2014', '2015') 
ylist = [] 


for x in sites:

	f = open('sites/n'+x+'.html')
	results = re.findall('<td>.+?</td>', f.read())

	l_num = []

	# Regular expression to match date, numbers and serie
	for x in results:
		if re.match('<td>[0-9]{1,3}</td>|<td>[0-9]{2}/[0-9]{2}/[0-9]{4}</td>', x):
			num = ''
			for n in x:
				if n >= '0' and n <= '9':
					num = num + n
			l_num.append(num)	

	# l_num contains a list like that: (date, x, digit, digit, digit, digit, digit, serie, date, x, and so on...) Where 'x' is a number we aren't interested in
	ylist.append(clean_list(l_num))
# At this point every date has been stored in a list of list with the form: (date, number, serie). One list per year.
# Store all the elements on MongoDB
for x in ylist:
	while len(x) != 0:
		d = x.pop(0)
		n = x.pop(0)
		s = x.pop(0)
		
		doc = {
				'date'   : d,
				'number' : n,
				'serie'  : s 
			  }
		lnumbers.insert_one(doc)
		
		bclient.write('Lottery', 'Date', int(raw_date(d)))
		bclient.write('Lottery', 'Number', int(n))
		bclient.write('Lottery', 'Serie', int(s))
		
