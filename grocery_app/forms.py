from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Optional, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from grocery_app.models import ItemCategory, GroceryStore, GroceryItem, User
from flask_bcrypt import Bcrypt
from grocery_app import bcrypt

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Store Title',
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="Store title must be between 3 and 80 characters")
        ])
    address = StringField('Store Address',
        validators=[
            DataRequired(),
            Length(min=3, max=200, message="Address must be between 3 and 200 characters")
        ])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Item Name',
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="Item name must be between 3 and 80 characters")
        ])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    store = QuerySelectField('Store',
        query_factory=lambda: GroceryStore.query,
        allow_blank=False,
        get_label='title')
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(GroceryItemForm, self).__init__(*args, **kwargs)

# forms for authentication with validations
class SignUpForm(FlaskForm):
    """Form for user signup."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validates that the username is not already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        """Validates that the username exists."""
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        """Validates that the password matches for this username."""
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')