from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class AddMovieForm(FlaskForm):
    title = StringField('영화 제목', validators=[DataRequired(), Length(min=1, max=25)])
    