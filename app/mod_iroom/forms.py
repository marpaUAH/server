# Import Form 
from flask.ext.wtf import Form 

# Import Form elements such as TextField 
from wtforms import TextField, RadioField
from wtforms.fields.html5 import DateField

# Import Form validators
from wtforms.validators import Regexp

import datetime

# Define the forms (WTForms)

class MyForm(Form):
	nmbr = TextField('nmbr', validators=[
		   Regexp(regex='[0-9]{5}', message=(u'Introduce un numero correcto')) ])

	serie = TextField('serie', validators=[
		   Regexp(regex='[0-9]{1,3}', message=(u'Introduce una serie correcta')) ])

class histoForm(MyForm):
	date = DateField('nmbr_date'#, validators=[
# DateRange( min=datetime.date(2012,12,31), max=datetime.date.today() ) ]) 
		)

