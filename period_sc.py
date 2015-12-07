# Import Regexp (re) and urlib2 and datetime
import re
import urllib2
import datetime
import pdb

# Import Beebotte module
from beebotte import *

# Import db 
from app import db, lnumbers

# Beebotte object declaration
bclient = BBT('db26c05fa32d1ca054eaf60350914ff9','aa18e56f716b597b2fc0a33bbbdc4dc2d32aff0731edb3bc391fe1282c07f10e')

### Funcion para dar formato a la fecha que llega de la RegExp --> 'XXddmmyyyy' ###
def format_date(sdate):
	year = sdate[6:10]
	month = sdate[4:6]
	day = sdate[2:4]
	return year+'-'+month+'-'+day

### Funcion para obtener un objeto datetime a partir de 'yyyy-mm-dd'
def object_date(fdate):
	return datetime.date(int(fdate[0:4]), int(fdate[5:7]), int(fdate[8:10]))

# Comienzo del script

# First check the last element on DBs

# Beebotte
foundoc_b = bclient.read('Lottery', 'Date', limit=1)
foundoc_b = object_date(foundoc_b[0]['data'])

#MongoDB
one_day = datetime.timedelta(days=1)
today = datetime.date.today()

# Check just the last 6 days
for i in range(6):
	foundoc_m = lnumbers.find_one({ 'date' : (today-i*one_day).strftime('%Y-%m-%d') })
	if foundoc_m != None:
		break
foundoc_m = object_date(foundoc_m['date'])

# Determine the number of dates that are necessary to get from the HTML code based on the difference between the last date stored and the current date
yesterday = today - one_day
b_times = int((yesterday-foundoc_b).days)
m_times = int((yesterday-foundoc_m).days)

# Get the last numbers	from website's HTML code
f = urllib2.urlopen('http://www.resultados11.es')
results = re.findall('<div id="bolas">.+?</div>|<div class="center fs16">.+?</div>|>[0-9]{3}<', f.read())
l_num = []	
pdb.set_trace()
# Clean the list to keep only numbers
for x in results:
	num = ""
	for n in x:
		if n >= '0' and n <= '9':
			num = num + n
	if len(num) != 0:
		l_num.append(num)

### Write on Beebotte database ### 
for x in range(b_times):

	try:
		bclient.write('Lottery', 'Number', l_num[3*x+1])
		bclient.write('Lottery', 'Date', format_date(l_num[3*x]))
		bclient.write('Lottery', 'Serie', l_num[3*x+2])

	except Exception:
		print('Beebotte. Fallo al publicar.')

### Write on MongoBD ###
for x in range(m_times):
	
	doc = {
			'number' : l_num[3*x+1],
			'date'   : format_date(l_num[3*x]),
			'serie'  : l_num[3*x+2]
		  }

	lnumbers.insert_one(doc)


