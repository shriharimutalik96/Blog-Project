from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),
                            Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password  = PasswordField('Password',validators=[DataRequired(),
                            Length(min=8,max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),
                            Length(min=8,max=20),EqualTo('password')])
    submit = SubmitField('SignUp')


    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken ,Please register other one')


    # here the method name should be validate_field(self,filed)
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That Email is already taken , Please register other one')


    # def validate_field(self,field):
    #     field = User.query.filter_by(field=field.data).first()
    #     if field:
    #         raise ValidationError('That Email is already taken , Please register other one')






class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])

    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])

    remember = BooleanField('Remember Me')  # remebering the user using cookies

    submit =SubmitField('Login')







class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),
                            Length(min=2,max=20)])

    email = StringField('Email',validators=[DataRequired(),Email()])

    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')


# Perform validation checks only if the current_user.username and email are different from the original
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken ,Please register other one')


    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That Email is already taken , Please register other one')




class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')
