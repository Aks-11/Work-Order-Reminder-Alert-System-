from flask_wtf import FlaskForm
from flask_wtf.file import * 
from wtforms import *
from wtforms.validators import *

class purchase_order(FlaskForm):
    Date=DateField('Date', validators=[DataRequired()])
    Purchase_Order_Number=StringField("Purhcase Order Number", validators=[DataRequired()])
    File_Order_Number=StringField("File Order Number", validators=[DataRequired()])
    Subject=TextAreaField("Subject", validators=[DataRequired()])
    Contact=StringField("Contact", [validators.regexp('\d{10}' ,message='Invalid contact number')])
    Amount=FloatField("Amount", validators=[DataRequired()])
    Address=TextAreaField("Address")
    Email=EmailField("Email", validators=[DataRequired(), Email()])
    City=SelectField("City", choices=['NOIDA', 'Lucknow', 'Kanpur', 'Gwalior', 'Meerut', 'Prayagraj','Indore', 'Bhopal','Bhilai','Dehradun'], validators=[DataRequired()])
    File=FileField("Upload File", validators=[FileRequired(),FileAllowed(['pdf'],'pdf only') ])
    # def validate_Contact(field):
    #     try:
    #         input_number=ph
    #         if(field.data)

class work_order(FlaskForm):
    Date=DateField("Date", validators=[DataRequired()])
    Start_Period=DateField("Start Period",validators=[DataRequired()])
    End_Period=DateField("End Period",validators=[DataRequired() ])
    Work_Order_Number=StringField("Work Order Number",validators=[DataRequired()])
    File_Order_Number=StringField("File Order Number",validators=[DataRequired()])
    Subject=StringField("Subject", validators=[DataRequired()])
    Contact=StringField("Contact", [validators.regexp('\d{10}' ,message='Invalid contact number')])
    Amount=FloatField("Amount", validators=[DataRequired()])
    Email=EmailField("Email", validators=[DataRequired(), Email()])
    Address=TextAreaField("Address")
    City=SelectField("City", choices=['NOIDA', 'Lucknow', 'Kanpur', 'Gwalior', 'Meerut', 'Prayagraj','Indore', 'Bhopal','Bhilai','Dehradun'], validators=[DataRequired()])
    File=FileField("Upload File", validators=[FileRequired(),FileAllowed(['pdf'],'pdf only') ])
    
    def validate_End_Period(form, field):
        if field.data < form.Start_Period.data:
            raise ValidationError("End date must not be earlier than start date.")

class search(FlaskForm):
    File_type=SelectField("File_Type", choices=['purchase','work'], validators=[DataRequired()])
    City=SelectField("City", choices=['NOIDA', 'Lucknow', 'Kanpur', 'Gwalior', 'Meerut', 'Prayagraj','Indore', 'Bhopal','Bhilai','Dehradun'], validators=[DataRequired()])
    Order_ID=StringField("Order_ID", validators=[DataRequired()])