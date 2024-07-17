from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    translation = SelectField('Bible Translation', choices=[], validators=[DataRequired()])
    book = SelectField('Book', choices=[], validators=[DataRequired()])
    chapter = SelectField('Chapter', choices=[], validators=[DataRequired()])
    start_verse = SelectField('Start Verse', choices=[], validators=[DataRequired()])
    end_verse = SelectField('End Verse', choices=[], validators=[DataRequired()])
    submit = SubmitField('Search')
