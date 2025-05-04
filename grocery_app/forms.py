from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from grocery_app.models import ItemCategory, GroceryStore, GroceryItem

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
        