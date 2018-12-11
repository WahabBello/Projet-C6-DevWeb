from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lycee.models import User, Classe


class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=30)])
    nom = StringField('Nom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    number = StringField('Phone Number', validators=[DataRequired()])
    niveau = TextAreaField('Niveau Etude', validators=[DataRequired()])
    classe = TextAreaField('Classe', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class UpdateForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=30)])
    nom = StringField('Nom',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    number = StringField('Phone Number', validators=[DataRequired()])
    niveau = StringField('Niveau Etude', validators=[DataRequired()])
    classe = StringField('Classe', validators=[DataRequired()])
    submit = SubmitField('Modifier')



    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ClasseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_title(self, title):
        classe = Classe.query.filter_by(title=title.data).first()
        if classe:
            raise ValidationError('That classe is already created. Please choose a different one.')