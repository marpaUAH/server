# Import flask dependencies
from flask import Blueprint, request, render_template, redirect
from flask import flash, session, g, url_for

# Import datetime
import datetime

# Import the database object from the main app module
from app import db, lnumbers

# Import the beebotte database module
from app import bclient

# Import module forms
from app.mod_iroom.forms import MyForm, histoForm

# Import module models 

# Define the blueprint: 'iroom', set its url prefix: app.url/iroom
mod_iroom = Blueprint('iroom', __name__, url_prefix='/iroom')

# Set today, one_day and yesterday
one_day = datetime.timedelta(days=1)
today = datetime.date.today()
yesterday = today - one_day

# Route '/'
@mod_iroom.route('/', methods=('POST', 'GET'))
def index():

	form = MyForm(request.form)
	
	# Read from MongoDB
	foundoc = lnumbers.find().sort('_id',-1)
	if foundoc == None:
		n = None
		s = None
	else:
		n = foundoc[0]['number']
		s = foundoc[0]['serie']

	if form.validate_on_submit():
		# Check if the number is the winner
		if n == None:
			prize = 'Aun no disponemos del ultimo numero'

		elif n == form.nmbr.data:
			if int(s) == int(form.serie.data):
				prize = 'ha recibido un premio de 35.000 euros y si juega La Paga 3.000 al mes durante 25 anos!'
			else:
				prize = 'ha recibido un premio de 35.000 euros'

		elif (int(n) == int(form.nmbr.data)+1) or (int(n) == int(form.nmbr.data)-1):
			prize = 'ha recibido un premio de 500 euros'
		
		elif n[1:5] == form.nmbr.data[1:5]:
			prize = 'ha recibido un premio de 200 euros'

		elif n[2:5] == form.nmbr.data[2:5]:
			prize = 'ha recibido un premio de 20 euros'

		elif n[3:5] == form.nmbr.data[3:5]:
			prize = 'ha recibido un premio de 6 euros'
		
		elif (n[4] == form.nmbr.data[4]) or (n[0] == form.nmbr.data[0]):
			if int(s) == int(form.serie.data):
				prize = 'ha recibido un premio de 1.50 euros mas 0.50 euros si juega La Paga'
			else:
				prize = 'ha recibido 1.50 euros'
		else:
			prize = 'no ha recibido ningun premio.'

		return render_template('iroom/index.html', form = form, today_date = yesterday.strftime('%a %d/%b/%Y'), n1=n[0], n2=n[1], n3=n[2], n4=n[3], n5=n[4], today_serie = s, res_mssg = prize, n=n)

	return render_template('iroom/index.html', form = form, today_date = yesterday.strftime('%a %d/%b/%Y'), n1=n[0], n2=n[1], n3=n[2], n4=n[3], n5=n[4], today_serie = s, res_mssg = None) 

# Route '/histo_check' 
@mod_iroom.route('/histo_check', methods=('GET', 'POST'))
def histo_check():

	form = histoForm(request.form)
	
	if form.validate_on_submit():

		# Check the number on MongoDB
		foundoc = lnumbers.find_one({ 'date' : form.date.data.strftime('%Y-%m-%d') })
		if foundoc == None:
			n = None
			s = None
		else:
			n = foundoc['number']
			s = foundoc['serie']
		
		# Check if the number is the winner
		if n == None:
			prize = 'Aun no disponemos de este numero'

		elif n == form.nmbr.data:
			if int(s) == int(form.serie.data):
				prize = 'recibio un premio de 35.000 euros y si juega La Paga 3.000 al mes durante 25 anos!'
			else:
				prize = 'recibio un premio de 35.000 euros'

		elif (int(n) == int(form.nmbr.data)+1) or (int(n) == int(form.nmbr.data)+1):
			prize = 'recibio un premio de 500 euros'
		
		elif n[1:5] == form.nmbr.data[1:5]:
			prize = 'recibio un premio de 200 euros'

		elif n[2:5] == form.nmbr.data[2:5]:
			prize = 'recibio un premio de 20 euros'

		elif n[3:5] == form.nmbr.data[3:5]:
			prize = 'recibio un premio de 6 euros'
		
		elif (n[4] == form.nmbr.data[4]) or (n[0] == form.nmbr.data[0]):
			if int(s) == int(form.serie.data):
				prize = 'recibio un premio de 1.50 euros mas 0.50 euros si juega La Paga'
			else:
				prize = 'recibio 1.50 euros'
		else:
			prize = 'no recibio ningun premio.'
		
		if n == None:
			return render_template('iroom/histo_submit.html', form = form, res_mssg = prize, n = n)
		else:
			return render_template('iroom/histo_submit.html', form = form, us_nmbr = form.nmbr.data, us_serie = form.serie.data, n1=n[0], n2=n[1], n3=n[2], n4=n[3], n5=n[4], tdy_serie = s, res_mssg = prize, n=n) 
	
	return render_template('iroom/histo_submit.html', form = form)


@mod_iroom.route('/info_premios')
def info_premios():
	return render_template('/iroom/premios.html')

@mod_iroom.route('/horarios')
def info_horas():
	return render_template('/iroom/horas.html')

@mod_iroom.route('/info_premios/cuponazo')
def cuponazo():
	return render_template('/iroom/cuponazo.html')

@mod_iroom.route('/info_premios/sueldazo')
def sueldazo():
	return render_template('/iroom/sueldazo.html')

